from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    gui_arg = DeclareLaunchArgument(
        "gui",
        default_value="true",
        description="Launch joint_state_publisher_gui to move the joints with sliders",
    )
    gui = LaunchConfiguration("gui")

    urdf_path = PathJoinSubstitution(
        [FindPackageShare("arm_description"), "urdf", "arm.urdf"]
    )
    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare("arm_description"), "rviz", "display.rviz"]
    )
    robot_description = {"robot_description": Command(["xacro ", urdf_path])}

    return LaunchDescription(
        [
            gui_arg,
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[robot_description],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                condition=IfCondition(gui),
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                condition=UnlessCondition(gui),
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", rviz_config_path],
                output="screen",
            ),
        ]
    )
