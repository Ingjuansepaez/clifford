from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    package = 'clifford'

    param_declare_arg = DeclareLaunchArgument('modo',
                                              default_value='home',
                                              description='nombre del parametro a cambiar'
                                              )

    nodo_parametro = Node(
        package='clifford',
        executable='locomotion_node_2',
        name='locomotion_unique',
        output='screen',
        parameters=[{
            'modo': LaunchConfiguration(
                'modo'
            )
        }]
    )

    return LaunchDescription([
        LogInfo(msg="INICIANDO EL LAUNCH PARA LA LOCOMOCION"),
        LogInfo(msg="--------------------------------------"),
        LogInfo(msg="--------------------------------------"),
        param_declare_arg,
        nodo_parametro,

    ])

    