# Welcome Robot
## How to configure the environment in your computer
- After cloning, rename the folder as ```welRobot_ws```.
- Build and set environment variables: 
	```bash
	cd ~/welRobot_ws/
	catkin_make
	source devel/setup.bash
	```
- Install dependencies:
	```bash
	cd ~/welRobot_ws/
	rosdep install --from-paths src -i
	catkin_make
	```
- Configure Turtlebot3's model:
	```bash
	mkdir -p ~/.gazebo/models/
	cp -r ~/welRobot_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_burger ~/.gazebo/models/
	```
- Add environment variables:
	```bash
	gedit ~/.bashrc
	```
	Add this code to ```~/.bashrc```:
	```bash
	# export TURTLEBOT3_MODEL=burger # without camera
	export TURTLEBOT3_MODEL=waffle
	```
- Test by launch a world:
	```bash
	roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
	```
## Test
### Face detection and face comperation
```bash
roscore
rosrun face facepp.py
rosrun smach_state face_detect_client.py 'welRobot_ws/src/face/face_data/face1.jpg'
rosrun smach_state face_compare_client.py 'welRobot_ws/src/face/face_data/face1.jpg' 'welRobot_ws/src/face/face_data/face1.jpg'
```
