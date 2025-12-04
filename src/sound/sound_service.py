#!/usr/bin/env python3
"""
Sound monitoring service - runs continuously to detect dog barking
Can be run as a systemd service
"""

import yaml
import logging
import sys
from pathlib import Path

# Add src directory to path for imports
# This allows importing from sound module when running from project root
project_root = Path(__file__).parent.parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from sound.sound_monitor import SoundMonitor

# Setup logging (relative to project root)
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(log_dir / "sound_monitor.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main service function"""
    # Load configuration (relative to project root)
    config_path = project_root / "config" / "sound_settings.yaml"
    if not config_path.exists():
        logging.error(f"Config file not found: {config_path}")
        print(f"❌ Config file not found: {config_path}")
        print("   Create config/sound_settings.yaml (see config/sound_settings_example.yaml)")
        sys.exit(1)
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Create monitor
    monitor = SoundMonitor(config)
    
    # Start monitoring
    if config.get('continuous', True):
        monitor.monitor_continuous()
    else:
        duration = config.get('duration_seconds', 3600)  # Default 1 hour
        monitor.monitor_duration(duration)

if __name__ == "__main__":
    main()

