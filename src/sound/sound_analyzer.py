#!/usr/bin/env python3
"""
Analyze stored sound events
View statistics and summaries of dog barking detections
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_events(date_str: str = None, data_dir: str = "data/sound"):
    """Load sound events from JSON files"""
    data_path = Path(data_dir)
    events = []
    
    if date_str:
        # Load specific date
        json_file = data_path / f"sound_events_{date_str}.json"
        if json_file.exists():
            with open(json_file, 'r') as f:
                events = json.load(f)
    else:
        # Load all files
        for json_file in sorted(data_path.glob("sound_events_*.json")):
            try:
                with open(json_file, 'r') as f:
                    file_events = json.load(f)
                    events.extend(file_events)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
    
    return events

def analyze_events(events, date_str: str = None):
    """Analyze and display statistics
    
    Args:
        events: List of event dictionaries
        date_str: Optional date string (YYYYMMDD) to display in output
    """
    if not events:
        print("=" * 60)
        print("Sound Detection Analysis")
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                print(f"Date: {date_obj.strftime('%Y-%m-%d (%A)')}")
            except:
                print(f"Date: {date_str}")
        print("=" * 60)
        print("No events found")
        return
    
    print("=" * 60)
    print("Sound Detection Analysis")
    if date_str:
        # Format date nicely
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            print(f"Date: {date_obj.strftime('%Y-%m-%d (%A)')}")
        except:
            print(f"Date: {date_str}")
    print("=" * 60)
    print(f"Total events: {len(events)}")
    print()
    
    # Count by type
    analog_count = sum(1 for e in events if e.get('analog_detected', False))
    digital_count = sum(1 for e in events if e.get('digital_detected', False))
    
    print("Detection Types:")
    print(f"  Analog threshold: {analog_count}")
    print(f"  Digital output: {digital_count}")
    print()
    
    # Time range
    timestamps = [datetime.fromisoformat(e['timestamp']) for e in events]
    if timestamps:
        print("Time Range:")
        print(f"  First: {min(timestamps).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Last:  {max(timestamps).strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    # Statistics
    adc_values = [e['adc'] for e in events]
    db_values = [e['decibels'] for e in events]
    
    print("ADC Statistics:")
    print(f"  Min: {min(adc_values)}, Max: {max(adc_values)}, Avg: {sum(adc_values)/len(adc_values):.1f}")
    print()
    
    print("Decibel Statistics:")
    print(f"  Min: {min(db_values):.1f} dB, Max: {max(db_values):.1f} dB")
    print(f"  Average: {sum(db_values)/len(db_values):.1f} dB")
    print()
    
    # Hourly distribution
    hourly = defaultdict(int)
    for ts in timestamps:
        hourly[ts.hour] += 1
    
    print("Hourly Distribution:")
    for hour in sorted(hourly.keys()):
        count = hourly[hour]
        bar = "█" * (count // max(1, max(hourly.values()) // 20))
        print(f"  {hour:02d}:00 - {count:4d} events {bar}")
    print()
    
    # Recent events
    print("Recent Events (last 10):")
    for event in events[-10:]:
        ts = datetime.fromisoformat(event['timestamp'])
        detection_types = []
        if event.get('analog_detected'):
            detection_types.append("A")
        if event.get('digital_detected'):
            detection_types.append("D")
        print(f"  {ts.strftime('%H:%M:%S')} - ADC: {event['adc']:4d}, "
              f"{event['decibels']:5.1f} dB ({'+'.join(detection_types)})")
    print("=" * 60)

def main():
    """Main function"""
    date_str = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--today":
            date_str = datetime.now().strftime('%Y%m%d')
            events = load_events(date_str)
        elif sys.argv[1] == "--date":
            if len(sys.argv) < 3:
                print("Usage: --date YYYYMMDD")
                sys.exit(1)
            date_str = sys.argv[2]
            events = load_events(date_str)
        elif sys.argv[1] == "--all":
            events = load_events()
        elif sys.argv[1] in ["--help", "-h"]:
            print("Usage: python3 sound_analyzer.py [OPTIONS]")
            print("\nOptions:")
            print("  --today              Analyze today's events")
            print("  --date YYYYMMDD      Analyze specific date (e.g., 20241204)")
            print("  YYYYMMDD             Analyze specific date (e.g., 20241204)")
            print("  --all                Analyze all events")
            print("  --help, -h           Show this help")
            print("\nExamples:")
            print("  python3 sound_analyzer.py")
            print("  python3 sound_analyzer.py --today")
            print("  python3 sound_analyzer.py 20241204")
            print("  python3 sound_analyzer.py --date 20241204")
            sys.exit(0)
        else:
            # Try to parse as date directly (YYYYMMDD format)
            if len(sys.argv[1]) == 8 and sys.argv[1].isdigit():
                date_str = sys.argv[1]
                events = load_events(date_str)
            else:
                print(f"Unknown option: {sys.argv[1]}")
                print("Usage: python3 sound_analyzer.py [--today|--date YYYYMMDD|YYYYMMDD|--all]")
                print("Use --help for more information")
                sys.exit(1)
    else:
        # Default: today
        date_str = datetime.now().strftime('%Y%m%d')
        events = load_events(date_str)
    
    analyze_events(events, date_str)

if __name__ == "__main__":
    main()

