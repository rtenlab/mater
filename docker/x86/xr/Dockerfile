FROM ubuntu:focal

USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install curl wget apt-transport-https lsb-core

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:monado-xr/monado -y -u
RUN wget -nv https://monado.freedesktop.org/keys/monado-ci.asc -O /etc/apt/trusted.gpg.d/monado-ci.asc
RUN echo 'deb https://monado.pages.freedesktop.org/monado/apt focal main' | tee /etc/apt/sources.list.d/monado-ci.list
RUN apt update
RUN apt-get -y install libglew-dev libglu1-mesa-dev libsqlite3-dev libx11-dev libgl1-mesa-dev git libboost-all-dev libeigen3-dev glslang-dev glslang-tools libgflags-dev libjpeg-dev libpng-dev libtiff-dev udev libudev-dev libwayland-dev wayland-protocols libx11-xcb-dev libxcb-glx0-dev libxcb-randr0-dev libxkbcommon-dev libopenxr-dev libopenxr1-monado libvulkan-dev libsdl2-dev cmake g++ extra-cmake-modules libopencv-dev libglfw3-dev pkg-config libusb-1.0.0-dev patch libfmt-dev libgoogle-glog-dev libssl-dev libsdl2-dev libprotobuf-dev libprotoc-dev protobuf-compiler graphviz zlib1g-dev qtbase5-dev libhdf5-dev libcurl4-openssl-dev libqwt-qt5-dev libyaml-cpp-dev librealsense2-dev librealsense2-gl-dev
RUN useradd -ms /bin/bash illixr

USER illixr
WORKDIR /home/illixr
RUN git clone -b convertBuildToCmake https://github.com/ILLIXR/ILLIXR.git