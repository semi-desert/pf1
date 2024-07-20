import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    usbcam_dir = get_package_share_directory('usb_cam')
    ldlidar_dir = get_package_share_directory('ldlidar')

    usbcam_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(usbcam_dir, 'launch', 'camera.launch.py')
        )
    )

    ldlidar_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ldlidar_dir, 'launch', 'ld14p.launch.py')
        )
    )
    
    ros_arduino_python_node = Node(
        package='ros_arduino_python',
        executable='ros_arduino_python',
        name='ros_arduino_python_publisher',
        output='screen',
        parameters=[
        ]
    )

    # Define LaunchDescription variable
    ld = LaunchDescription()

    ld.add_action(ros_arduino_python_node)
    ld.add_action(usbcam_cmd)
    ld.add_action(ldlidar_cmd)

    return ld