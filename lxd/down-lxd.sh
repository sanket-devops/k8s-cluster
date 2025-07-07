#!/bin/sh

which lxc
lxc --version

echo "Stop and delete container"
lxc stop k8s-node1 || true && lxc delete k8s-node1
lxc stop k8s-node2 || true && lxc delete k8s-node2
lxc stop k8s-node3 || true && lxc delete k8s-node3

echo "Delete profile and network"
lxc profile delete k8s 2>/dev/null || true
lxc network delete natbr0 2>/dev/null || true




