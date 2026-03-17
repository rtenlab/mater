#!/bin/bash
XR_IP=<YOUR_XR_IP>

# Launch all scripts in separate terminals
echo "Starting the Kinova GEN3 driver..."

gnome-terminal -- bash -c "./2_1_run_gen3.sh; exec bash" &
echo "SUCCESS: roslaunch kortex_driver kortex_driver.launch"
sleep 1

gnome-terminal -- bash -c "./2_2_run_rosbridge.sh; exec bash" &
echo "SUCCESS: roslaunch rosbridge_server rosbridge_websocket.launch"
sleep 1

gnome-terminal -- bash -c "./2_3_run_web_repuiblisher.sh; exec bash" &
echo "SUCCESS: rosrun tf2_web_republisher tf2_web_republisher"
sleep 3

gnome-terminal -- bash -c "./2_4_run_forward_recorder.sh $XR_IP; exec bash" &
echo "SUCCESS: ./forward_recorder.py $XR_IP"
sleep 1

gnome-terminal -- bash -c "./2_5_run_move_gen3.sh $XR_IP; exec bash" &
echo "SUCCESS: ./move_gen3.py $XR_IP"
sleep 1

echo "MATER robot side run sequecne complete! Please Add RobotModel in RViz"