import rclpy
from rclpy.node import Node
import requests

class SwitchTriggerNode(Node):
    def __init__(self):
        super().__init__('switch_trigger_node')
        self.get_logger().info('Switch Trigger Node Started')
        # You can add a timer or subscription to trigger the HTTP call
        # For demo, call toggle every 5 seconds
        self.create_timer(5.0, self.send_toggle)

    def send_toggle(self):
        esp32_ip = "http://10.0.0.169/toggle"  

        try:
            response = requests.get(esp32_ip, timeout=2)
            self.get_logger().info(f"Toggled switch, ESP32 responded: {response.text}")
        except Exception as e:
            self.get_logger().error(f"Failed to contact ESP32: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SwitchTriggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
