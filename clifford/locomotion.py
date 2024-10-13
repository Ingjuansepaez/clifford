import rclpy

from clifford.inverse_kinematic import InverseKinematic
from clifford.direct_kinematic import directKinematic
from clifford.numeric_method import nodeNumericMethod

from sensor_msgs.msg import JointState
from rclpy.node import Node


class CommandUserLocomotion(Node):
    def __init__(self):
        super().__init__("Nodo_de_tipo_de_locomocion")

        self.declare_parameter('modo', 'home')

        self.q_list = [0.0, 0.0, 0.0]
        self.l_list = [1, 1, 1]

        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        self.joint_names = JointState()
        self.direct_kinematic = directKinematic()
        self.inverse_kinematic = InverseKinematic()

        self.current_leg_id = 0
        self.px, self.py, self.pz = self.direct_kinematic.send_attributes()

        param_value = self.get_parameter('modo').get_parameter_value().string_value
        self.get_logger().info(f'el valor del parametro es {param_value}')
        self.user_commands_dog_state(param_value)

        self.joint_names = [
            "hombro_1_joint", "codo_1_joint", "muneca_1_joint",
            "hombro_2_joint", "codo_2_joint", "muneca_2_joint",
            "hombro_3_joint", "codo_3_joint", "muneca_3_joint",
            "hombro_4_joint", "codo_4_joint", "muneca_4_joint",
        ]

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):

        q1 = self.q_list[0]
        q2 = self.q_list[1]
        q3 = self.q_list[2]

        self.values_in_joints = [
            q1,
            q2,
            q3,
            q1,
            q2,
            q3,
            q1,
            q2,
            q3,
            q1,
            q2,
            q3
        ]

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names
        joint_state.position = self.values_in_joints

        self.publisher_.publish(joint_state)
    
    def user_commands_dog_state(self, param_value):
        
        dog_state = param_value

        if dog_state == 'home':
            self.command_home()
            return
        elif dog_state == 'levantado':
            return
        elif dog_state == 'marcha':
            return
        elif dog_state == 'caminata':
            return

    def command_home(self):

        desired_points = [self.px, self.py, self.pz]
        L_list = self.l_list
        self.q_list = self.inverse_kinematic.compute_inverse_kinematic(L_list, desired_points)
        self.get_logger().info(f"Posiciones deseadas {desired_points}")
        self.get_logger().info(f"Valores de los angulos {self.q_list}")
        return
    def command_up(self):
        return
    def command_march(self):
        return
    def command_walk(self):
        return

    
def main(args=None):
    rclpy.init(args=args)
    node = CommandUserLocomotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()