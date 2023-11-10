from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import makeTerm

server_command = "iperf -s -p 5001,5002,5003 -t 20 "
client_command = None

class NetworkTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        s1, s2 = [self.addSwitch(s) for s in ('s1', 's2')]
        h1 = self.addHost(name='h1', ip='192.168.1.100/24')
        h2 = self.addHost(name='h2', ip='192.168.1.101/24')
        h3 = self.addHost(name='h3', ip='192.168.1.102/24')
        h4 = self.addHost(name='h4', ip='192.168.1.103/24')
        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2)]:
            self.addLink(h, s)
        self.addLink(s1, s2)

def function4(net, iperf_port):
    global server_command
    makeTerm(node=net['h4'], cmd=f"{server_command} ")

def function1(net, server_ip, iperf_port, congestion_scheme):
    global client_command
    client_command = f"iperf -c {server_ip} -p {iperf_port} -Z {congestion_scheme} " \
                     f"> client_output1.txt 2>&1 & " \
                     f"tcpdump -i any -w client1_capture.pcap &"
    makeTerm(node=net['h1'], cmd=client_command)

def function2(net, server_ip, iperf_port, congestion_scheme):
    global client_command
    client_command = f"iperf -c {server_ip} -p {iperf_port} -Z {congestion_scheme} " \
                     f"> client_output2.txt 2>&1 & " \
                     f"tcpdump -i any -w client2_capture.pcap "
    makeTerm(node=net['h2'], cmd=client_command)

def function3(net, server_ip, iperf_port, congestion_scheme):
    global client_command
    client_command = f"iperf -c {server_ip} -p {iperf_port} -Z {congestion_scheme} " \
                     f"> client_output3.txt 2>&1 & " \
                     f"tcpdump -i any -w client3_capture.pcap "
    makeTerm(node=net['h3'], cmd=client_command)

def run(config, congestion_scheme):
    topo = NetworkTopo()
    net = Mininet(topo)
    net.start()
    if config == 'b':
        h1 = net.get('h1')
        h4 = net.get('h4')
        server_ip = h4.IP()
        iperf_port = 5001
        function4(net, iperf_port)
        function1(net, server_ip, iperf_port, congestion_scheme)
        
    elif config == 'c':
        h4 = net.get('h4')
        server_ip = h4.IP()
        iperf_port = 5001
        function4(net, iperf_port)
        function1(net, server_ip, iperf_port, congestion_scheme)
        function2(net, server_ip, iperf_port, congestion_scheme)
        function3(net, server_ip, iperf_port, congestion_scheme)
    CLI(net)
    net.stop()

a = input("Enter configuration: ")
b = input("Enter congestion control scheme: ")
if __name__ == '__main__':
    setLogLevel('info')
    run(a, b)
