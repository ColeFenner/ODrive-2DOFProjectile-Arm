from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='odrive_projectile',
            executable='dual_velocity',
            name='dual_velocity_node',
            output='screen'
        ),
        Node(
            package='odrive_projectile',
            executable='projectile_service',
            name='projectile_service_node',
            output='screen'
        )
    ])
