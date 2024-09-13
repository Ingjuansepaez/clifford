import rclpy

from rclpy.node import Node
from std_msgs.msg import String

class RecieveNode(Node):
    def __init__(self):
        super().__init__('suscriber')
        self.suscriber = self.create_subscription(String, 'user', self.listener_callback, 10)

    def listener_callback(self, msg):

        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):

    rclpy.init(args=args)
    suscriber = RecieveNode()
    
    rclpy.spin(suscriber)

    suscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()