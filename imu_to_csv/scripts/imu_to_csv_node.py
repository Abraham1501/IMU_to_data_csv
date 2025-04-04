#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import csv
from sensor_msgs.msg import Imu

class ImuToCSV(Node):
    def __init__(self):
        super().__init__('imu_to_csv')
        # Change '/imu_topic' to the name of your actual IMU topic
        self.subscription = self.create_subscription(
            Imu,
            '/vectornav/imu',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Open CSV file and write header
        self.csv_file = open('imu_data_InMove.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow([
            'stamp_sec', 'stamp_nsec', 'frame_id',
            'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w',
            'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
            'linear_acceleration_x', 'linear_acceleration_y', 'linear_acceleration_z'
        ])
        self.get_logger().info("IMU to CSV node has been started.")

    def listener_callback(self, msg):
        # Extract header data
        stamp_sec = msg.header.stamp.sec
        stamp_nsec = msg.header.stamp.nanosec
        frame_id = msg.header.frame_id

        # Extract orientation data
        orientation = msg.orientation

        # Extract angular velocity data
        angular_velocity = msg.angular_velocity

        # Extract linear acceleration data
        linear_acceleration = msg.linear_acceleration

        # Write a row with the relevant data
        self.csv_writer.writerow([
            stamp_sec,
            stamp_nsec,
            frame_id,
            orientation.x, orientation.y, orientation.z, orientation.w,
            angular_velocity.x, angular_velocity.y, angular_velocity.z,
            linear_acceleration.x, linear_acceleration.y, linear_acceleration.z
        ])
        self.get_logger().info('IMU data written to CSV.')

    def destroy_node(self):
        # Ensure the CSV file is closed when the node shuts down
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImuToCSV()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
