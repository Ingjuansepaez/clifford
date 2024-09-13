import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'clifford'
    file = 'description/clifford.urdf.xacro'

    world_file_path = os.path.join(
        os.getenv('HOME'),
        'clifford_ws', 'src', 'clifford', 'worlds', 'empty.world'
    )

    xacro_file = os.path.join(get_package_share_directory(package_name), file)
    robot_description = xacro.process_file(xacro_file).toxml()

    sdf_path = os.path.join(
        os.getenv('HOME'), 
        'clifford_ws', 'src', 'clifford', 'description', 'clifford.sdf'
    )

    # Gazebo launch
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose',world_file_path,  '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', sdf_path],
        output='screen'
    )

    # Node to publish the robot state
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # Spawn the robot entity in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description', '-entity', 'clifford'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])
