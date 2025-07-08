#!/usr/bin/env bash

which lxc
lxc --version

nodes=(
  "k8s-node1 00:16:3e:aa:bb:01 192.168.56.101"
  "k8s-node2 00:16:3e:aa:bb:02 192.168.56.102"
  "k8s-node3 00:16:3e:aa:bb:03 192.168.56.103"
)

for node in "${nodes[@]}"; do
  name=$(echo $node | awk '{print $1}')
  mac=$(echo $node | awk '{print $2}')
  ip=$(echo $node | awk '{print $3}')
  
  echo "Stop and delete container $name"
  lxc stop $name || true && lxc delete $name

  ssh-keygen -R $ip

done

echo "Delete profile and network"
lxc profile delete k8s 2>/dev/null || true
lxc network delete natbr0 2>/dev/null || true




