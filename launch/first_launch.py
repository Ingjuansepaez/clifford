from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node 

def generate_launch_description():

    return LaunchDescription([

        LogInfo(msg = "Iniciando el lanzamiento del nodo user.py"),

        Node(
            package='clifford',
            executable='user_node',
            name= 'user',
            output='screen'
        ),

        LogInfo(msg="Lanzamiento completado"),

    ])



