import socket
from threading import Thread
import json
import roslibpy
import time

import numpy as np
import csv
import argparse

from statistics import mean

def xr_to_robot(xr, port, robot='', period=1):
    count = 0
    client = roslibpy.Ros(host=xr, port=port)
    client.run()

    talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')

    while client.is_connected:
        count += 1
        message_id = count
        time1 = time.time()

        with open('../depthai_hand_tracker/hand_data', 'r') as file:
            data_string = file.read().strip()

        message_data = {
            'message_id': message_id,
            'fused_pose': data_string,
            'time1': time1
        }

        talker.publish(roslibpy.Message({'data': json.dumps(message_data)}))

        # Log sent IDs
        with open('sent_ids', 'a') as file:
            file.write(f"{message_id}\n")

        print(f"Sent: ID {message_id}, data: {data_string}")

        time.sleep(period)

    talker.unadvertise()
    client.terminate()

def listen_from_robot(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        e2e_lats = []
        positional_diffs = []
        count = 0
        data_log = []
        output_file = 'result.csv'

        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    data_string = data.decode()
                    time_string, pose_string = data_string.split(":", 1)
                    with open('data', 'w') as file:
                        file.write(pose_string)
                        # print("Count: ", count)
                        count += 1
                    # calculate e2e lat
                    time1 = float(time_string)
                    e2e_lat = time.time() - time1
                    if e2e_lat < 2:
                        e2e_lats.append(e2e_lat)
                    
                    #  calculate diff between usr and robot pose
                    vbot_pose = []
                    usr_pose = []
                    if pose_string != None:
                        vbot_pose = eval(pose_string)
                        with open('../depthai_hand_tracker/hand_data') as file:
                            usr_pose_string = file.read().strip()
                            if usr_pose_string != None:
                                usr_pose = eval(usr_pose_string)
                    
                    # Calculate positional difference between usr_pose and vbot_pose
                    if usr_pose and vbot_pose:
                        usr_pose_xyz = np.array(usr_pose[:3])  # Extract x, y, z from user pose
                        vbot_pose_xyz = np.array(vbot_pose[:3])  # Extract x, y, z from robot pose
                        
                        # Compute Euclidean distance
                        positional_diff = np.linalg.norm(usr_pose_xyz - vbot_pose_xyz)
                        positional_diffs.append(positional_diff)

                    data_log.append([time_string, usr_pose_string, pose_string, e2e_lat, positional_diff])
                    # print("Appended to data_log")
                    
                    if count % 10 == 0:
                        print(f"E2E Lat: Avg {mean(e2e_lats[8:]):.6f}| Max {max(e2e_lats[8:]):.6f} | Min {min(e2e_lats[8:]):.6f}")
                        # Print or save the positional difference
                        print(f"Positional difference between user pose and robot pose: {positional_diff}")
                        with open(output_file, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(["Time1", "usr_pose", "vbot_pose", "e2e_lat", "usr_vbot_diff"])
                            writer.writerows(data_log)
                    
                    # time.sleep(0.01)
                    
                except (ValueError, SyntaxError):
                    continue

if __name__ == "__main__":
    print("Starting XR bridge...")
    # add a mandatory ip_address of xr argument
    parser = argparse.ArgumentParser(description='XR listener')
    parser.add_argument('xr_ip', metavar='xr_ip', type=str, help='IP address of the XR device')
    args = parser.parse_args()
    # get the ip_address value
    xr_ip = args.xr_ip
    port = 9091 # for robot to xr communication (robot pose posting)

    # xr_thread = Thread(target=xr_to_robot, args=("localhost", 9090, "", 0.05))  # 50ms period
    listen_thread = Thread(target=listen_from_robot, args=(xr_ip, port))

    # xr_thread.start()
    listen_thread.start()

    # xr_thread.join()
    listen_thread.join()
