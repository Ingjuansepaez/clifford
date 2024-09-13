import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import math
import numpy as np

class locomocion(Node):
    def __init__(self):
        super().__init__('locomocion_node')

        self.declare_parameter('modo', 'home')
        self.L_list = [0.100, 0.140, 0.120]
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        param_value = self.get_parameter('modo').get_parameter_value().string_value
        self.get_logger().info(f'el valor del parametro es {param_value}')
        self.user_commands_dog_state(param_value)

        self.joint_names = JointState()

        self.joint_names = [
            "hombro_1_joint", "codo_1_joint", "muneca_1_joint",
            "hombro_2_joint", "codo_2_joint", "muneca_2_joint",
            "hombro_3_joint", "codo_3_joint", "muneca_3_joint",
            "hombro_4_joint", "codo_4_joint", "muneca_4_joint",
        ]

        self.timer = self.create_timer(0.1, self.timer_callback)

    
    def timer_callback(self):

        hombro_q1 = self.q1 
        codo_q2 = self.q2
        muneca_q3 = self.q3

        self.values_in_joints = [
            hombro_q1,
            codo_q2, 
            muneca_q3,
            hombro_q1,
            codo_q2, 
            muneca_q3,
            hombro_q1,
            codo_q2, 
            muneca_q3,
            hombro_q1,
            codo_q2, 
            muneca_q3,
        ] 

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names
        joint_state.position = self.values_in_joints

        self.publisher_.publish(joint_state)



    def user_commands_dog_state(self, param_value):

        if param_value == 'home':
            self.print_values_parameters_home()
        elif param_value == 'levantado':
            self.print_values_parameters_up()
        elif param_value == 'marcha':
            self.print_values_parameters_march()

    def print_values_parameters_home(self):
        self.get_logger().info("EL PERRO ESTA EN HOME")
        desired_point = [0, 0, 0]
        q = self.compute_inverse_kinematic(desired_point, self.L_list) 
        self.get_logger().info(f"El valor de los angulos es {q[0], q[1], q[2]}") 

    
    def print_values_parameters_up(self):
        self.get_logger().info("EL PERRO SE ESTA LEVANTANDO")
        desired_point = [0, 0, 0]
        q = self.compute_inverse_kinematic(desired_point, self.L_list) 
        self.get_logger().info(f"El valor de los angulos es {q[0], q[1], q[2]}")


    def print_values_parameters_march(self):
        self.get_logger().info("EL PERRO CAMINARA")  
        desired_point = [0, 0, 0]
        q = self.compute_inverse_kinematic(desired_point, self.L_list) 
        self.get_logger().info(f"El valor de los angulos es {q[0], q[1], q[2]}") 

    
    def compute_inverse_kinematic(self, desired_point, L_list):

        L0 = L_list[0]
        L1 = L_list[1]
        L2 = L_list[2]

        # desired_x = desired_htm[0, 3]
        # print(f"\nDesired X: {desired_x}")
        # desired_y = desired_htm[1, 3]
        # print(f"Desired Y: {desired_y}")
        # desired_z = desired_htm[2, 3]
        # print(f"Desired Z: {desired_z}")

        desired_x = desired_point[0]
        #print(f"\nDesired X: {desired_x}")
        desired_y = desired_point[1]
        #print(f"Desired Y: {desired_y}")
        desired_z = desired_point[2]
        #print(f"Desired Z: {desired_z}")

    
        self.q1 = math.atan2(desired_z, desired_y)+math.radians(90)
        #print(f"\nQ1: {math.degrees(q1)} °")
        cos_q1 = math.cos(self.q1)
        sin_q1 = math.sin(self.q1)
        cc=math.sqrt(desired_x**2+(math.fabs(desired_y)-math.fabs(L0*sin_q1))**2+(math.fabs(desired_z)-math.fabs(L0*cos_q1))**2)-0.00000001
        #if cos_q1<=1.0e-19:
        #    cos_q1=1.0e-10 
        #print(f"\ncc: {cc}")
        cos_a=(L1**2+cc**2-L2**2)/(2*L1*cc)
        #print(f"\ncos_a: {cos_a} °")
        if cos_a >= 1:
            cos_a = 1
        elif cos_a <= -1:
            cos_a = -1
        A = math.acos(cos_a)
    

        self.q2 = math.asin(-desired_x/cc)-A
        cos_q3=(L1**2+L2**2-cc**2)/(2*L1*L2)
        if cos_q3>1:
            cos_q3=1
        elif cos_q3<-1:
            cos_q3=-1
        self.q3 = -math.acos(cos_q3)+math.radians(180)


        q_list = np.array([self.q1, self.q2, self.q3]).T
        return (q_list)


def main(args=None):
    rclpy.init(args=args)
    node = locomocion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

