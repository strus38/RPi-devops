# Personal & Transportable DevOps Cluster

Let me introduce you the new dev/ops way … My ‘Personal & Transportable DevOps Cluster'

## Description
 
In a single (and geek) packaging you get:
Infra:
- 3 Raspberry Pi (mix of them)
- Managed 8 Ports Switch
- LCD screen  to get the IP of the Master node.
- Flexibility: add more node by adding more RPIs…
 
DevOps Environment
- A fully functional Docker swarm cluster spread on X (here x=3) RPi nodes
- A gitlab env. to host the SRC, Build and automatically test your code
- Rules to automatically test your CI code on the swarm cluster
- Collectd for remote monitoring with Grafana or your tool of choice (Graphite)
- The Docker Swarm cluster is running on an Internal network using VLANs
 
To add:
- A 2.5"HDD to host the GitLab DB for more reliability

## Pictures

![alt tag](./img/pict1.png)
![alt tag](./img/pict2.png)
![alt tag](./img/pict3.png)
![alt tag](./img/pict4.png)
![alt tag](./img/pict5.png)


## Test

```
root@swarm1-pearl in ~
$ docker run -ti --rm hypriot/rpi-consul members -detailed -rpc-addr=192.168.200.1:8400
Node          Address             Status  Tags
black-pearl   192.168.1.99:8301   alive   role=consul,dc=dc1,vsn=2,vsn_min=1,vsn_max=2,build=0.5.0:0c7ca91c,port=8300,bootstrap=1
swarm1-pearl  192.168.1.197:8301  alive   role=consul,dc=dc1,vsn=2,vsn_min=1,vsn_max=2,build=0.5.0:0c7ca91c,port=8300
swarm2-pearl  192.168.1.198:8301  alive   build=0.5.0:0c7ca91c,port=8300,role=consul,dc=dc1,vsn=2,vsn_min=1,vsn_max=2

root@swarm1-pearl in ~
$ docker -H black-pearl:2378 run -d -p 9000:9000 --env="constraint:node==swarm1-pearl" --name dockerui hypriot/rpi-dockerui -e http://192.168.200.1:2378
db3638853b2cf20ad15807686efce3567d3c6e7783cc5473ad1bc2d2ab7e9d61

root@swarm1-pearl in ~
$ docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
db3638853b2c        hypriot/rpi-dockerui   "/dockerui -e http://"   9 seconds ago       Up 3 seconds        0.0.0.0:9000->9000/tcp   dockerui
239df7402319        hypriot/rpi-consul     "/consul agent -serve"   7 hours ago         Up 15 minutes                                bin_consul_1
5ec8d4dc937d        hypriot/rpi-swarm      "/swarm join --advert"   7 hours ago         Up 14 minutes       2375/tcp                 bin_swarm_1
```

## Docker on RPi is provided by Hypriot ![Hypriot downloads](http://blog.hypriot.com/downloads/)
