#Make sure both motor Ross Nodes are live


import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time


class example_velocity_input(Node):
	def __init__(self):
		super().__init__('example_velocity_input')

		self.publisher = self.create_publisher(Float64MultiArray, '/cmd_velocities', 10)
		self.velocities = [0.0, 0.0]
		self.timer = self.create_timer(0.1, self.timer_callback)
		self.get_logger().info('example_velocity_input initialized.')
		
		self.sin_vaule = 0
		self.start_time = time.time()
		self.max_velocity = 5

	def timer_callback(self):
		
		current_time = float(time.time() - self.start_time)
		self.velocity1 = self.sin_vaule = math.sin(2 * math.pi * current_time * self.max_velocity) #Sin Vaule
		self.velocity2 = self.sin_vaule = math.sin(2 * math.pi * current_time * self.max_velocity - math.pi) #Sin Vaule Offset 180

		self.velocities = [self.velocity1, self.velocity2]
		msg = Float64MultiArray()

		msg.data = self.velocities
		self.publisher.publish(msg)
		self.get_logger().info(f'Sending Velocites: {self.velocities}')
	

def main(args=None):
	rclpy.init(args=args)
	node = example_velocity_input()
	rclpy.spin(node)
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()