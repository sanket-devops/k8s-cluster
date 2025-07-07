#!/bin/sh

which lxc
lxc --version

echo "Create network"
lxc network create natbr0
lxc network edit natbr0 < network.yaml
# List created network
lxc network list | grep natbr0


echo "Create profile"
lxc profile create k8s
lxc profile edit k8s < k8s-profile-config.yaml
# List created profile
lxc profile list

echo "Launch containers"
./launch_k8s_nodes.sh

