
:construction: Under construction :construction:

### Puppy watch :dog: :camera:

A setup for taking photos every nth minute of a puppy. 

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

Install Picamera2 with `apt` (recommended). 

```
sudo apt install -y python3-picamera2
```

### Code editor

I use the SSH-extension in VS Code for working. 

### :desktop_computer: :no_entry_sign: Headless setup

The code in this project is made to work headlessly (no monitor). Note that the Pi will crash if you run `rpicam-hello` or other example codes that starts a preview screen. 

### :snake: Python project

When installing from `requirements.txt`, you need to make `libcamera` (and other system packages) visible inside `.venv`, in order to make `libcamera` work inside `.venv`:

```
python3 -m venv .venv --system-site-packages
```



### :rocket: Execution

```python3 src/main.py```
