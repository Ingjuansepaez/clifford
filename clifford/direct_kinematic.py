import rclpy

from rclpy.node import Node
from sensor_msgs.msg import JointState

import math
import numpy as np


class directKinematic(Node):
    def __init__(self):
        super().__init__('cinematica_directa')

        self.theta_mundo = np.radians(0)
        self.theta1 = np.radians(0)  
        self.theta2 = np.radians(0)
        self.theta3 = np.radians(0)

        self.d_mundo = 0
        self.d1 = 0
        self.d2 = 0
        self.d3 = 0

        self.a_mundo = 0
        self.a1 = 1 
        self.a2 = 1
        self.a3 = 1

        self.alpha1 = np.radians(-90)
        self.alpha2 = np.radians(0)
        self.alpha3 = np.radians(0)

        self.publisher_= self.create_publisher(JointState, '/joint_states', 10)

        self.T_new_y = np.array([[np.cos(np.radians(90)), 0, np.sin(np.radians(90)), 0],
                                 [0, 1, 0, 0],
                                 [-np.sin(np.radians(90)), 0, np.cos(np.radians(90)), 0],
                                 [0, 0, 0, 1]])
        
        self.T1 = self.denavit(self.theta1, self.d1, self.a1, self.alpha1)
        self.T2 = self.denavit(self.theta2, self.d2, self.a2, self.alpha2)
        self.T3 = self.denavit(self.theta3, self.d3, self.a3, self.alpha3)

        self.T_total = np.dot(np.dot(self.T1, self.T2), self.T3)
        self.T_total = np.dot(self.T_new_y, self.T_total)

        self.PX = self.T_total[0,3] 
        self.PY = self.T_total[1,3]
        self.PZ = self.T_total[2,3]

        self.get_logger().info(f"{self.T_total}")
        self.get_logger().info("PARA LA ULTIMA COLUMNA FILA 1, 2, 4")
        self.get_logger().info(f"{self.PX, self.PY, self.PZ}")

        print("\n")
        print("\n")
        print(self.PX)
        print(self.PY)
        print(self.PZ)


    def denavit(self, teta, d, a, alfa):
        dh = np.array([[np.cos(teta), -np.cos(alfa)*np.sin(teta), np.sin(alfa)*np.sin(teta), a*np.cos(teta)],
                      [np.sin(teta), np.cos(alfa)*np.cos(teta), -np.sin(alfa)*np.cos(teta), a*np.sin(teta)],
                      [0, np.sin(alfa), np.cos(alfa), d],
                      [0, 0, 0, 1]])
        
        return dh

    def send_attributes(self):

        PX = self.PX
        PY = self.PY
        PZ = self.PZ

        return PX, PY, PZ



def main(args=None):
    rclpy.init(args=args)
    node = directKinematic()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()