import rclpy

from rclpy.node import Node


class nodeNumericMethod(Node):
    def __init__(self):
        super.__init__('Nodo metodo numerico')

    





def main(args=None):
    rclpy.init(args=args)
    node = nodeNumericMethod()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()