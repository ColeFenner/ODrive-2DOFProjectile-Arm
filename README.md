-----------------------
Required Packages:
-----------------------

ros_odrive

-----------------------
Currently The Odrive_ros2_control included package does not build properly, so:
-----------------------

colcon build --packages-select odrive_can odrive_projectile odrive_projectile_srv 

or

colcon build --packages-ignore odrive_ros2_control

-----------------------
Lauch Up the Velocity Controller & Interpeter:
-----------------------

ros2 launch odrive_projectile odrive_projectile_launch.py


-----------------------
Check Service Calls Interact With Velocity Control:
-----------------------

#Set the target velocities the arm will swing too

ros2 service call /set_velocities odrive_projectile_srv/srv/SetVelocities "{velocity1: 1.5, velocity2: -1.2}"


#Switch from [0,0] Velocity to Target Velocity

ros2 service call /active_vel std_srvs/srv/SetBool "{data: true}"
ros2 service call /active_vel std_srvs/srv/SetBool "{data: false}"


#Send a release signal and stop messages
ros2 service call /release std_srvs/srv/SetBool "{data: true}"
ros2 service call /release std_srvs/srv/SetBool "{data: false}"


Validated Two Nodes!




-----------------------
Good Commands in Testing:
-----------------------



cd ~/ros2_ws/src/odrive_projectile

git pull

colcon build --packages-ignore odrive_ros2_control

colcon build --packages-select odrive_can odrive_projectile odrive_projectile_srv 

colcon build --packages-select odrive_can 


colcon build --packages-select odrive_projectile  

colcon build --packages-select odrive_projectile_srv 


source ./install/setup.bash

ros2 launch odrive_projectile odrive_projectile_launch.py


ros2 run odrive_projectile dual_velocity


ros2 service call /active_vel std_srvs/srv/SetBool "{data: true}"
ros2 service call /active_vel std_srvs/srv/SetBool "{data: false}"


ros2 service call /release std_srvs/srv/SetBool "{data: true}"

ros2 service call /set_velocities odrive_projectile_srv/srv/SetVelocities "{velocity1: 1.5, velocity2: -1.2}"
