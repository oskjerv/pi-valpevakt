#!/usr/bin/env python3
"""
Sound monitoring module for dog barking detection
Continuously monitors sound levels and logs detections
"""

import RPi.GPIO as GPIO
import spidev
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# GPIO pin configuration
SOUND_SENSOR_DO = 15  # GPIO 15 - Digital output from sound sensor
MCP3008_CS = 8  # GPIO 8 (CE0) - Hardware chip select
ADC_CHANNEL = 0  # MCP3008 CH0 for sound sensor analog output

class SoundMonitor:
    """Monitor sound levels and detect barking"""
    
    def __init__(self, config: Dict):
        """Initialize sound monitor with configuration"""
        self.config = config
        self.analog_threshold = config.get('analog_threshold', 5)
        self.use_analog_threshold = config.get('use_analog_threshold', True)
        self.sample_interval = config.get('sample_interval', 0.1)  # seconds
        
        # Statistics
        self.analog_detections = 0
        self.digital_detections = 0
        self.last_digital_state = GPIO.LOW
        self.last_analog_above_threshold = False
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SOUND_SENSOR_DO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Initialize SPI for MCP3008
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
        self.spi.bits_per_word = 8
        
        # Storage
        self.data_dir = Path(config.get('data_dir', 'data/sound'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logging.info("Sound monitor initialized")
    
    def read_adc(self, channel: int) -> Optional[int]:
        """Read analog value from MCP3008 ADC"""
        try:
            cmd = [1, (8 + channel) << 4, 0]
            adc_data = self.spi.xfer2(cmd)
            if len(adc_data) >= 3:
                adc_value = ((adc_data[1] & 3) << 8) + adc_data[2]
                return adc_value
            return None
        except Exception as e:
            logging.error(f"Error reading ADC: {e}")
            return None
    
    def adc_to_voltage(self, adc_value: int, vref: float = 3.3) -> float:
        """Convert ADC value to voltage"""
        return (adc_value / 1023.0) * vref
    
    def voltage_to_decibels(self, voltage: float, vref: float = 3.3) -> float:
        """Convert voltage to approximate decibels"""
        import math
        if voltage <= 0:
            return 30.0
        
        min_voltage = 0.001
        voltage = max(voltage, min_voltage)
        reference_voltage = 0.005
        base_dB = 30
        
        db = 20 * math.log10(voltage / reference_voltage) + base_dB
        return max(30.0, min(120.0, db))
    
    def check_sound(self) -> Optional[Dict]:
        """Check for sound detection, returns event dict if detected"""
        # Read digital input
        digital_state = GPIO.input(SOUND_SENSOR_DO)
        
        # Read analog value
        adc_value = self.read_adc(ADC_CHANNEL)
        
        if adc_value is None:
            return None
        
        voltage = self.adc_to_voltage(adc_value)
        db = self.voltage_to_decibels(voltage)
        
        # Check analog threshold
        analog_above_threshold = adc_value >= self.analog_threshold
        analog_detected = False
        digital_detected = False
        
        # Detect analog threshold crossing
        if self.use_analog_threshold:
            if analog_above_threshold and not self.last_analog_above_threshold:
                analog_detected = True
                self.analog_detections += 1
        
        # Detect digital output rising edge
        if digital_state == GPIO.HIGH and self.last_digital_state == GPIO.LOW:
            digital_detected = True
            self.digital_detections += 1
        
        # Update state
        self.last_analog_above_threshold = analog_above_threshold
        self.last_digital_state = digital_state
        
        # Return event if detected
        if analog_detected or digital_detected:
            return {
                'timestamp': datetime.now().isoformat(),
                'adc': adc_value,
                'voltage': round(voltage, 4),
                'decibels': round(db, 1),
                'analog_detected': analog_detected,
                'digital_detected': digital_detected,
                'total_analog': self.analog_detections,
                'total_digital': self.digital_detections
            }
        
        return None
    
    def save_event(self, event: Dict):
        """Save sound event to file"""
        # Save to daily JSON file
        date_str = datetime.now().strftime('%Y%m%d')
        json_file = self.data_dir / f"sound_events_{date_str}.json"
        
        # Load existing events
        events = []
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    events = json.load(f)
            except:
                events = []
        
        # Append new event
        events.append(event)
        
        # Save back
        try:
            with open(json_file, 'w') as f:
                json.dump(events, f, indent=2)
            logging.info(f"Sound event saved: {event['timestamp']}")
        except Exception as e:
            logging.error(f"Error saving event: {e}")
    
    def monitor_continuous(self):
        """Continuously monitor for sounds"""
        logging.info("Starting continuous sound monitoring")
        
        try:
            while True:
                event = self.check_sound()
                if event:
                    self.save_event(event)
                    logging.info(
                        f"Sound detected - ADC: {event['adc']}, "
                        f"dB: {event['decibels']}, "
                        f"Analog: {event['analog_detected']}, "
                        f"Digital: {event['digital_detected']}"
                    )
                
                time.sleep(self.sample_interval)
        
        except KeyboardInterrupt:
            logging.info("Sound monitoring stopped by user")
        finally:
            self.cleanup()
    
    def monitor_duration(self, duration_seconds: int):
        """Monitor for a specific duration"""
        logging.info(f"Starting sound monitoring for {duration_seconds} seconds")
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration_seconds:
                event = self.check_sound()
                if event:
                    self.save_event(event)
                    logging.info(
                        f"Sound detected - ADC: {event['adc']}, "
                        f"dB: {event['decibels']}, "
                        f"Analog: {event['analog_detected']}, "
                        f"Digital: {event['digital_detected']}"
                    )
                
                time.sleep(self.sample_interval)
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO and SPI resources"""
        try:
            self.spi.close()
            GPIO.cleanup()
            logging.info("Sound monitor cleanup complete")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

