import os, xacro

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # usbcam_dir = get_package_share_directory('usb_cam')
    # ldlidar_dir = get_package_share_directory('ldlidar')
    pf1_dir = get_package_share_directory('pf1')
    urdf_file = os.path.join(pf1_dir, 'urdf', 's1.urdf')  # Generate by `xacro urdf/s1.urdf.xacro -o urdf/s1.urdf``

    # usbcam_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(usbcam_dir, 'launch', 'camera.launch.py')
    #     )
    # )

    # ldlidar_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(ldlidar_dir, 'launch', 'ld14p.launch.py')
    #     )
    # )
    
    # ros_arduino_python_node = Node(
    #     package='ros_arduino_python',
    #     executable='ros_arduino_python',
    #     name='ros_arduino_python_publisher',
    #     output='screen',
    #     parameters=[
    #     ]
    # )

    # Process the URDF file
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
        doc = xacro.parse(robot_desc)
        xacro.process_doc(doc)
        robot_desc = doc.toxml()
    rsp_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            # {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    jsp_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    jsp_gui_cmd = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    # Define LaunchDescription variable
    ld = LaunchDescription()

    # ld.add_action(ros_arduino_python_node)
    # ld.add_action(usbcam_cmd)
    # ld.add_action(ldlidar_cmd)
    ld.add_action(rsp_cmd)
    ld.add_action(jsp_cmd)
    #ld.add_action(jsp_gui_cmd)

    return ld