import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState

import math
import numpy as np
import sympy as sp


class directKinematic(Node):
    def __init__(self):
        super().__init__('cinematica_directa')

        self.theta1 = sp.symbols('q1') 
        self.theta2 = sp.symbols('q2') 
        self.theta3 = sp.symbols('q3') 

        #self.d1 = sp.symbols('d1')
        #self.d2 = sp.symbols('d2')
        #self.d3 = sp.symbols('d3') 

        self.a1 = sp.symbols('l1') 
        self.a2 = sp.symbols('l2') 
        self.a3 = sp.symbols('l3')

        #self.alpha1 = sp.symbols('a1')
        #self.alpha2 = sp.symbols('a2')
        #self.alpha3 = sp.symbols('a3')

        self.publisher_= self.create_publisher(JointState, '/joint_states', 10)
        
        self.T1 = self.matriz_dh(self.theta1, self.a1)
        self.T2 = self.matriz_dh(self.theta2, self.a2)
        self.T3 = self.matriz_dh(self.theta3, self.a3)

        self.T_total = self.T1 * self.T2 * self.T3
        self.T_total_simp = sp.simplify(self.T_total)
        
        self.get_logger().info(f"{self.T_total_simp}")


    def matriz_dh(self, theta, a ):
        return sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0, a*sp.cos(theta)],
        [sp.sin(theta), sp.cos(theta),  0, a*sp.sin(theta)],
        [0,             0,              1, 0],
        [0,             0,              0, 1]
    ])


def main(args=None):
    rclpy.init(args=args)
    node = directKinematic()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()