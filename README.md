# ROS2 Package for Control of Two ODrive Motors and an ESP32 Trigger

This reposity builds upon [ros_odrive](https://github.com/odriverobotics/ros_odrive) package to implement control of two odrive motor controllers ulitizing the odrive_node. This system in robotic arm apart of Oregon State's LRAM Lab under Ross Hatton

Required Package:

- [ros_odrive](https://github.com/odriverobotics/ros_odrive)

## System Requirements

- Ubuntu >= 24.04
- ROS2 >= Jazzy

# Software Setup
Clone this repository and the [ros_odrive](https://github.com/odriverobotics/ros_odrive) package into your workspace

Extract out the odrive_projectile_srv zip file in the odrive_projectile package into your package directory

Add the esp32_code onto an esp32 using arduino IDE. Make sure to edit the wifi username and password matching that of your computer

For more information in general Odrive ROS2 CAN control, refer to official documentation: [ROS2 CAN Package](https://docs.odriverobotics.com/v/latest/guides/ros-package.html)

-----------------------
As the odrive_ros2_control package in ros_drive does not build properly with this ROS2 version, we build what is required:
-----------------------
```
colcon build --packages-select odrive_can odrive_projectile odrive_projectile_srv 
source install/setup.bash
```
-----------------------
Lauch Up the Velocity Controller & Service Manager:
-----------------------
```
ros2 launch odrive_projectile odrive_projectile_launch.py
```
-----------------------
Set up ramping velocity control on both axis:
-----------------------
```
ros2 service call /odrive_axis0/request_axis_state odrive_can/srv/AxisState "{axis_requested_state: 8}"
ros2 service call /odrive_axis1/request_axis_state odrive_can/srv/AxisState "{axis_requested_state: 8}"
```
-----------------------
Check Service Calls Interact With Velocity Control:
-----------------------

## Set the target velocities the arm will swing too
```
ros2 service call /set_velocities odrive_projectile_srv/srv/SetVelocities "{velocity1: 1.5, velocity2: -1.2}"
```

## Switch from [0,0] Velocity to Target Velocity:
```
ros2 service call /active_vel std_srvs/srv/SetBool "{data: true}"
ros2 service call /active_vel std_srvs/srv/SetBool "{data: false}"
```
## Send a release toggle signal:
```
ros2 service call /release std_srvs/srv/SetBool
```
## Service Call throwing sequence of the combined actions above:
```
ros2 service call /run_velocity_sequence std_srvs/srv/Trigger
```

-----------------------
To Run the example v(t) velocity input, launch up another file for sin velocity motion being called to both motors: 
-----------------------
```
ros2 launch odrive_projectile example_velocity_launch.py

ros2 service call /odrive_axis0/request_axis_state odrive_can/srv/AxisState "{axis_requested_state: 8}"
ros2 service call /odrive_axis1/request_axis_state odrive_can/srv/AxisState "{axis_requested_state: 8}"
```
