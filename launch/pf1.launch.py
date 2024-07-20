import os, xacro

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
    pf1_dir = get_package_share_directory('pf1')
    urdf_file = os.path.join(pf1_dir, 'urdf', 's1.urdf')  # Generate by `xacro urdf/s1.urdf.xacro -o urdf/s1.urdf`
    nav2_dir = get_package_share_directory('nav2_bringup')
    nav2_launch_dir = os.path.join(nav2_dir, 'launch')
    map_file = os.path.join(pf1_dir, 'maps', 'map.yaml')
    nav_param_file = os.path.join(pf1_dir, 'config', 'nav2_params.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')


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

    slam_cmd = Node(
        package="slam_toolbox",
        executable="sync_slam_toolbox_node",
        parameters=[{
            "use_sim_time": True,
            "base_frame": "base_footprint",
            "odom_frame": "odom",
            "map_frame": "map"
        }]
    )

    navigation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_launch_dir, '/bringup_launch.py']),
        launch_arguments={
            'map': map_file,
            'use_sim_time': use_sim_time,
            'params_file': nav_param_file}.items(),
    )

    # Define LaunchDescription variable
    ld = LaunchDescription()

    ld.add_action(ros_arduino_python_node)
    ld.add_action(usbcam_cmd)
    ld.add_action(ldlidar_cmd)
    ld.add_action(rsp_cmd)
    ld.add_action(jsp_cmd)
    #ld.add_action(jsp_gui_cmd)
    ld.add_action(slam_cmd)
    ld.add_action(navigation_cmd)

    return ld