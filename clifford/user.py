import rclpy
import serial 

from rclpy.node import Node
from std_msgs.msg import String

class User(Node):
    def __init__(self):
        super().__init__('user_node')

        self.publisher_ = self.create_publisher(String, 'user', 10)
        
        self.x = 0
        self.y = 0
        self.z = 0

        self.desirte_points = []

        self.desirte_points = self.command_user2robot()
        print(f"los puntos son {self.desirte_points}")

        self.point_1 = self.desirte_points[0]
        self.point_2 = self.desirte_points[1]
        self.point_3 = self.desirte_points[2]

        self.timer = self.create_timer(2.0, self.publish_message)

    def publish_message(self):

        message_data = f'puntos: {self.point_1},{self.point_1}, {self.point_1}'
        msg = String
        msg.data = message_data

        self.publisher_.publish(msg)

        self.get_logger().info(f'Publicando: "{message_data}"')
        print(f'Se envía al Arduino: {message_data}')


    def command_user2robot(self):
 
        desirte_points = []

        print("Bienvenidos a clifford \n")
        print("\n")
        print("Ingrese alguno de los siguientes comandos: \n")
        print("\n")

        command = input("Ingrese alguno de los siguientes comandos: Home, parado, trote estatico, caminar")

        print("\n")

        if command == "parado":

            x = 12
            y = 12
            z = 12

            desirte_points = [x, y, z]
        
        return desirte_points



def main(args=None):

    rclpy.init(args=args)
    #node = rclpy.create_node('user_node')
    commands_publisher = User()

    rclpy.spin(commands_publisher)

    commands_publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
        