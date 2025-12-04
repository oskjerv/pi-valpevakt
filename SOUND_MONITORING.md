# Sound Monitoring System - Dog Barking Detection

This system continuously monitors sound levels to detect when your dog is barking while you're away.

## Features

- **Continuous monitoring** - Runs 24/7 to detect all barking events
- **Dual detection** - Uses both analog threshold (sensitive) and digital output
- **Event logging** - Stores all detections with timestamps, ADC values, and decibel levels
- **Daily files** - Organizes events by date for easy analysis
- **Statistics** - View summaries and hourly distributions

## Setup

### 1. Create Configuration

Copy the example config:
```bash
cp config/sound_settings_example.yaml config/sound_settings.yaml
```

Edit `config/sound_settings.yaml` to adjust sensitivity:
- `analog_threshold`: Lower = more sensitive (3-10 recommended for barking)
- `sample_interval`: How often to check (0.1 seconds = 10 times per second)

### 2. Test the System

Run manually to test:
```bash
python3 src/sound/sound_service.py
```

This will start monitoring and save events to `data/sound/sound_events_YYYYMMDD.json`

### 3. Install as Systemd Service (Recommended)

To run continuously in the background:

```bash
# Copy service file
sudo cp systemd/sound_monitor.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (starts on boot)
sudo systemctl enable sound_monitor.service

# Start service
sudo systemctl start sound_monitor.service

# Check status
sudo systemctl status sound_monitor.service

# View logs
journalctl -u sound_monitor.service -f
```

## Usage

### View Today's Events

```bash
python3 src/sound/sound_analyzer.py --today
```

### View Specific Date

```bash
python3 src/sound/sound_analyzer.py --date 20241203
```

### View All Events

```bash
python3 src/sound/sound_analyzer.py --all
```

## Data Storage

Events are stored in JSON format in `data/sound/`:
- One file per day: `sound_events_YYYYMMDD.json`
- Each event contains:
  - Timestamp (ISO format)
  - ADC value (0-1023)
  - Voltage reading
  - Decibel level
  - Detection type (analog/digital)
  - Running totals

Example event:
```json
{
  "timestamp": "2024-12-03T14:23:45.123456",
  "adc": 45,
  "voltage": 0.0145,
  "decibels": 39.2,
  "analog_detected": true,
  "digital_detected": false,
  "total_analog": 15,
  "total_digital": 3
}
```

## Adjusting Sensitivity

### Too Many False Positives?
- Increase `analog_threshold` in config (try 8-15)
- Turn potentiometer on sensor counter-clockwise

### Missing Barking Events?
- Decrease `analog_threshold` in config (try 3-5)
- Turn potentiometer on sensor clockwise
- Check sensor placement (closer to dog's area)

## Integration Ideas

### 1. Trigger Camera on Barking
Modify `src/main.py` to check for recent sound events before taking photos.

### 2. Send Notifications
Add email/SMS notifications when barking is detected (e.g., using Twilio, email).

### 3. Daily Reports
Create a script to email daily summaries of barking activity.

### 4. Web Dashboard
Create a simple web interface to view real-time and historical data.

## Troubleshooting

### Service Not Starting
```bash
# Check logs
journalctl -u sound_monitor.service -n 50

# Check if SPI is enabled
ls -la /dev/spi*

# Verify config file exists
ls -la config/sound_settings.yaml
```

### No Events Being Detected
1. Check sensor connections
2. Verify ADC is reading values (run test script)
3. Lower `analog_threshold` in config
4. Adjust sensor potentiometer

### Too Many Events
1. Increase `analog_threshold` in config
2. Adjust sensor potentiometer
3. Check for background noise sources

## File Structure

```
src/sound/
├── sound_monitor.py    # Core monitoring class
├── sound_service.py    # Service entry point
└── sound_analyzer.py   # Analysis and statistics tool

data/sound/
└── sound_events_*.json # Daily event files

config/
└── sound_settings.yaml # Configuration

systemd/
└── sound_monitor.service # Systemd service file
```

