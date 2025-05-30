import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from odrive_can.msg import ControlMessage

class DualOdrivePublisher(Node):

    def __init__(self):
        super().__init__('dual_odrive_publisher')

        # Create publishers for each axis
        self.pub_axis0 = self.create_publisher(ControlMessage, '/odrive_axis0/control_message', 10)
        self.pub_axis1 = self.create_publisher(ControlMessage, '/odrive_axis1/control_message', 10)

        #timer_period = 0.1  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)



        self.subscription = self.create_subscription(
            Float64MultiArray,
            '/cmd_velocities',
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info('Waiting for velocity commands on /cmd_velocities...')
        
        self.velocity1 = 0.0  # rad/s
        self.velocity2 = 0.0

    def cmd_vel_callback(self, msg):

        if len(msg.data) < 2:
            self.get_logger().warn('Expected 2 velocities but got fewer.')
            return

        self.velocity1 = msg.data[0]
        self.velocity2 = msg.data[1]

        msg0 = ControlMessage()
        msg0.control_mode = 2     # Velocity Control
        msg0.input_mode = 1       # Input velocity mode
        msg0.input_pos = 0.0
        msg0.input_vel = self.velocity1
        msg0.input_torque = 0.0
        self.pub_axis0.publish(msg0)

        msg1 = ControlMessage()
        msg1.control_mode = 2
        msg1.input_mode = 1
        msg1.input_pos = 0.0
        msg1.input_vel = self.velocity2
        msg1.input_torque = 0.0
        self.pub_axis1.publish(msg1)

        self.get_logger().info(f'Odrive velocities: {self.velocity1}, {self.velocity2}')

def main(args=None):
    rclpy.init(args=args)
    node = DualOdrivePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
