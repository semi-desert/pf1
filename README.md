# PF1

Path Finder 1 Gen

# Configuration

* Upper computer: Raspberry Pi 4B+
* Lower computer: Arduino Mega 2560
* Radar: LeDong LD140P
* Motor: JGB37-520 12V/110rpm with a reduction ratio of 90
* Motor driver board: TB6612 (Model D24A)
* Battery: 12V 6000mAh Lithium Iron Phosphate
* Camera: Standard USB-HD Camera

# Version

* ROS2 Humble


# Install Dependencies

* `pip install pyserial transforms3d`
* `sudo apt install ros-humble-diagnostic-updater`
* `sudo apt install ros-humble-tf-transformations`
* `sudo apt install ros-humble-control-msgsy`
* `sudo apt install ros-humble-usb-cam`
* `sudo apt install ros-humble-xacro`
* `sudo apt install ros-humble-joint-state-publisher-gui`
* `sudo apt install ros-humble-slam-toolbox`
* `sudo apt install ros-humble-navigation2`
* `sudo apt install ros-humble-nav2-bringup`