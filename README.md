# CS433_Assignment-2
This repository contains the submissions for assignment 2 of CS433 (https://docs.google.com/document/d/1d2-9nIXBMrXnIJEmeEHZ5eNNO7k5iLcC4R52v454-Ik/edit) 

| Team Member Name | Roll Number |
| ------------- | ------------- |
| Kaushal Kothiya  | 21110107  |
| Mithil Pechimuthu  | 21110129  |

Please find the answers to the assignment in the "WriteUp.pdf" file. 

## Instruction
--------------- 
### 1. Clone the repository
Run
```shell
git clone https://github.com/PechimuthuMithil/CS433_Assignment-2.git 
```
### 2. Part 1
Start Openv Switch
```shell
sudo systemctl start openvswitch-switch.service
```
Run Part1.py
```shell
 sudo python3 Part1.py
```
In the mininet prompt type
'''shell
pingall
```
to test the ping reachability 

To change the routing path of routing from subnet A to subnet C through B, open `xterm ra` and run 
```shell
ip route change 10.2.0.0/24 via 10.100.1.10 dev ra-eth2
```
and open `xterm rc` and run 
```shell
ip route change 10.0.0.0/24 via 10.102.3.10 dev rc-eth3
```
Verify the path by running the following on xterm h1
```shell
traceroute 10.2.0.252
```
One can also view the routing table of the routers by opening their respective xterms and running
```shell
ip route
```
