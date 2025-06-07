import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
from std_srvs.srv import SetBool
from odrive_projectile_srv.srv import SetVelocities
import requests

from odrive_can.srv import AxisState
from time import sleep
from std_srvs.srv import Trigger


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

        self.create_service(SetBool, '/active_vel', self.active_callback)
        self.create_service(SetBool, '/release', self.release_callback)

        self.srv = self.create_service(SetVelocities, 'set_velocities', self.set_velocities_callback)

        self.create_service(Trigger, '/run_velocity_sequence', self.sequence_callback)


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
    
    def sequence_callback(self, request, response):

        self.get_logger().info("Starting velocity sequence...")

        # 1. Set velocities (assume already set via /set_velocities service)
        if self.velocities == [0.0, 0.0]:
            response.success = False
            response.message = "Velocities not set before sequence."
            return response

        # 2. Activate spinning
        self.active = True
        self.get_logger().info("Velocities activated.")
        sleep(3.0)  

        # 3. Trigger release
        try:
            esp32_ip = "http://10.0.0.169/toggle"
            http_response = requests.get(esp32_ip, timeout=2)
            self.get_logger().info(f"Release sent. ESP32 responded: {http_response.text}")
        except Exception as e:
            self.get_logger().error(f"Failed to send release signal: {e}")
            response.success = False
            response.message = "Release failed."
            return response

        # 4. Deactivate spinning
        sleep(1.0)
        self.active = False
        self.get_logger().info("Velocities deactivated.")

        response.success = True
        response.message = "Velocity sequence complete."
        return response


    def send_odrive_axis_state(self):
        request = AxisState.Request()
        request.axis_requested_state = 8  # For example: 8 = CLOSED_LOOP_CONTROL

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info('Service call succeeded')
        else:
            self.get_logger().error('Service call failed %r' % (future.exception(),))


def main(args=None):
    rclpy.init(args=args)
    node = VelocityTriggerController()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()