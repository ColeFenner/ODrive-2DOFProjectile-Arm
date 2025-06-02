import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
from std_srvs.srv import SetBool

from odrive_projectile_srv.srv import SetVelocities

import requests

class VelocityTriggerController(Node):
    def __init__(self):
        super().__init__('velocity_trigger_controller')

        qos = QoSProfile(depth=10)
        self.publisher = self.create_publisher(Float64MultiArray, '/cmd_velocities', qos)
        self.release_publisher = self.create_publisher(Bool, '/release_trigger', qos)

        self.velocities = [0.0, 0.0]
        self.active = False
        self.released = False

        self.timer = self.create_timer(0.5, self.timer_callback)

        # Services
        self.create_service(SetBool, '/active_vel', self.active_callback)
        self.create_service(SetBool, '/release', self.release_callback)

        self.srv = self.create_service(SetVelocities, 'set_velocities', self.set_velocities_callback)

        self.get_logger().info('VelocityTriggerController initialized.')

    def timer_callback(self):

        if self.released:
            return

        msg = Float64MultiArray()
        if self.active:
            msg.data = self.velocities
            self.publisher.publish(msg)
            self.get_logger().info(f'Set Velocites: {self.velocities}')
        else:
            msg.data = [0.0, 0.0]
            self.publisher.publish(msg)
            self.get_logger().info(f'Not Active Arm: {self.velocities}')

    def active_callback(self, request, response):
        self.active = request.data
        response.success = True
        response.message = "Arm Velocities Zero" if self.active else "Arm Velocities Active"
        return response

    def release_callback(self, request, response):
        esp32_ip = "http://10.0.0.169/toggle"  

        try:
            self.released = True

            http_response  = requests.get(esp32_ip, timeout=2)
            self.get_logger().info(f"Toggled switch, ESP32 responded: {http_response.text}")
        except Exception as e:
            self.get_logger().error(f"Failed to contact ESP32: {e}")
            self.released = False
        response.success = True
        response.message = "Released a one-shot command" if self.released else "Release canceled"
        return response

    def set_velocities_callback(self, request, response):
        self.velocity1 = request.velocity1
        self.velocity2 = request.velocity2
        self.velocities = [self.velocity1, self.velocity2]
        self.get_logger().info(f'Setting velocities: {self.velocity1}, {self.velocity2}')
        response.success = True
        response.message = 'Velocities updated'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = VelocityTriggerController()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()