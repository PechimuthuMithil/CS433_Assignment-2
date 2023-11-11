from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
import sys


class NetworkTopo(Topo):
    def __init__(self,link_loss=None):
        Topo.__init__(self)
        s1, s2 = [self.addSwitch(s) for s in ('s1', 's2')]
        h1 = self.addHost(name='h1', ip='192.168.1.100/24')
        h2 = self.addHost(name='h2', ip='192.168.1.101/24')
        h3 = self.addHost(name='h3', ip='192.168.1.102/24')
        h4 = self.addHost(name='h4', ip='192.168.1.103/24')
        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2)]:
            self.addLink(h, s)
        self.addLink(s1, s2,loss=link_loss)


def run(config, congestion_scheme,linkloss):
    topo = NetworkTopo(link_loss=linkloss)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    if config == 'b':
        h1 = net.get('h1')
        h4 = net.get('h4')
        server_ip = h4.IP()
        iperf_port = 5001
        net['h4'].cmd("iperf -s -p 5001,5002,5003 &")

        net['h4'].cmd("timeout 15000 tcpdump -i h4-eth0 -w server_h4.pcap &")
        net['h1'].cmd("timeout 10000 tcpdump -i h1-eth0 -w c1ient_h1.pcap &") 

        net['h1'].cmd("iperf -c 192.168.1.103 -p 5001 -t 5 -Z {} &".format(congestion_scheme))
        
    elif config == 'c':
        h4 = net.get('h4')
        server_ip = h4.IP()
        iperf_port = 5001
        net['h4'].cmd("iperf -s -p 5001,5002,5003 &")

        net['h4'].cmd("timeout 10000 tcpdump -i h4-eth0 -w server_h4.pcap &")
        net['h1'].cmd("timeout 7000 tcpdump -i h1-eth0 -w client_h1.pcap &") 
        net['h2'].cmd("timeout 7000 tcpdump -i h2-eth0 -w client_h2.pcap &") 
        net['h3'].cmd("timeout 7000 tcpdump -i h3-eth0 -w client_h3.pcap &") 

        net['h1'].cmd("iperf -c 192.168.1.103 -p 5001 -t 5 -Z {} &".format(congestion_scheme))
        net['h2'].cmd("iperf -c 192.168.1.103 -p 5002 -t 5 -Z {} &".format(congestion_scheme))
        net['h3'].cmd("iperf -c 192.168.1.103 -p 5003 -t 5 -Z {} &".format(congestion_scheme))
    else:
        print("Invalid configuration specified!\nChoose from b or c\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    n = len(sys.argv)
    config = ''
    congestion = ''
    linkloss = 0
    for i in sys.argv[1:]:
        if i.startswith('--config='):
            config = i[9:]
        elif (i.startswith('--congestion=')):
            congestion = i[13:]
        else: # --linkloss=
            linkloss = int(i[11:])
    a=config
    b=congestion
    print("Recived parameters:\n")
    print("Configuration --> ",a)
    print("Congestion scheme --> ",b)
    print("link loss % -->",linkloss,"\n")
    print("Running mininet...")
    run(a, b,linkloss)
