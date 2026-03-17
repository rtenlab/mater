# This is an auto generated Dockerfile for ros:ros-base
# generated from docker_images/create_ros_image.Dockerfile.em
FROM ros:noetic-ros-core-focal

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    gnome-terminal \
    python3-rosdep \
    python3-rosinstall \
    python3-vcstools \
    git \
    python3 \
    python3-pip \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# bootstrap rosdep
RUN rosdep init && \
  rosdep update --rosdistro $ROS_DISTRO

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-ros-base=1.5.0-1* 

# copy the directory
COPY ./mater /root/mater

# Run the dependency installation
RUN apt-get update && apt-get install -y libgazebo11-dev \
    ros-noetic-gazebo-ros-pkgs ros-noetic-gazebo-ros-control ros-noetic-moveit \
    ros-noetic-rosbridge-server \
    -y ros-noetic-tf2-web-republisher

# Install the dependencies for ros_kortex
RUN python3 -m pip install conan==1.59
RUN conan config set general.revisions_enabled=1
RUN conan profile new default --detect > /dev/null
RUN conan profile update settings.compiler.libcxx=libstdc++11 default
RUN cd /root/mater/robot && rosdep install --from-paths src --ignore-src -y

# cakin_make and setup.bash
WORKDIR /root/mater/robot
RUN rm -rf build devel && . /opt/ros/noetic/setup.sh && catkin_make