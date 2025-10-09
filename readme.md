
:construction: Under construction :construction:

### Puppy watch :dog: :camera:

A setup for taking photos every nth minute of a puppy.

The images are appended into a .gif, and the gif is pushed to an album in Google Photos.
#### :gear: Hardware

- :computer: Raspberry Pi 4 model B (with a faulty SD-slot)
- :floppy_disk: Micro SD 32 GB
- :camera: Raspberry Pi Camera Module 2 NoIR

#### Software

Make sure that you run `Bullseye` or later versions.

Check with `cat /etc/os-release`

```
PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
NAME="Debian GNU/Linux"
VERSION_ID="13"
VERSION="13 (trixie)"
VERSION_CODENAME=trixie
DEBIAN_VERSION_FULL=13.1
ID=debian
```

#### :closed_book: Guides

- [Getting started with Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html)
- [Getting started with the Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/3)
- [Install the camera](https://www.raspberrypi.com/documentation/accessories/camera.html#install-a-raspberry-pi-camera)
- [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/accessories/camera.html#about-the-camera-modules)
- [Picamera2 library](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)

### :package: Packages

Make sure that everything is up to date

```
sudo apt update

sudo apt full-upgrade

```

Install Picamera2 with `apt`, not of `pip`. 

```
sudo apt install -y python3-picamera2
```

### Code editor

I use the SSH-extension in VS Code for writing code. 

### :desktop_computer: :no_entry_sign: Headless setup

The code in this project is made to work headlessly (no monitor). Note that the Pi will crash if you run `rpicam-hello` or other example codes that starts a preview screen. 

### :snake: Python project

When installing from `requirements.txt`, you need to make `libcamera` (and other system packages) visible inside `.venv`, in order to make `libcamera` work inside `.venv`:

```
python3 -m venv .venv --system-site-packages
```

### :rocket: Execution

```python3 src/main.py```


### :loop: Planned/regular execution

NOTE: At the moment `src/main.py` is run directly in `systemd/`

Create a config file in your user root.

```
# ~/.vaplevakt_config
PROJECT_PATH=/home/pi/projects/valpevakt
CONFIG_PATH=/home/pi/projects/valpevakt/config/settings.yaml
```

The paths are read in `run_main.sh`.

`run_main.sh` is a wrapper script for executing `main.py` regularly.

Make sure that `run_main.sh` is executable: `chmod +x run_main.sh`.


```
# Copy systemd files to /etc/systemd/system
sudo cp systemd/rpi_cam.service /etc/systemd/system/
sudo cp systemd/rpi_cam.timer /etc/systemd/system/

# Reload systemd daemons
sudo systemctl daemon-reload

# Enable and start the timer
sudo systemctl enable rpi_cam.timer
sudo systemctl start rpi_cam.timer

# Check timers
systemctl list-timers | grep rpi_cam


```

### Google Photos Library API

[The Photos Library API](https://developers.google.com/photos/library/reference/rest) is used to push the images/gifs to an album in Google Photos. 

Resources:
- [Configure your app](https://developers.google.com/photos/overview/configure-your-app)
- The code suggestions from ChatGPT were quite good. (Yeah, sure I know)

Steps:
1. Follow the instructions for how to configure your app and creating OAuth 2.0 Client ID.
2. Run `src/storage/authorize_photos.py` for authenticating and creating token. You`ll need a screen. 
3. Run `src/storage/create_album.py` for creating and album and the album ID. 


### Debugging

Check `logs/app.log`.

```

# Check the log for issues
journalctl -u rpi_cam.service -n 50

$ Check status of service
sudo systemctl status rpi_cam.service
sudo systemctl status rpi_cam.timer

```