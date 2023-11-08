#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

TOPOS = {'mytopo' : (lambda : NetworkTopo())}


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class Topology(Topo):
    def build(self, **_opts):
        ra = self.addHost('ra', cls=LinuxRouter, ip='10.0.0.1/24')
        rb = self.addHost('rb', cls=LinuxRouter, ip='10.1.0.1/24')
        rc = self.addHost('rc', cls=LinuxRouter, ip='10.2.0.1/24')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(s1,
                     ra,
                     intfName2='ra-eth1',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(s2,
                     rb,
                     intfName2='rb-eth1',
                     params2={'ip': '10.1.0.1/24'})
        
        self.addLink(s3,
                     rc,
                     intfName2='rc-eth1',
                     params2={'ip': '10.2.0.1/24'})

        self.addLink(ra,
                     rb,
                     intfName1='ra-eth2',
                     intfName2='rb-eth2',
                     params1={'ip': '10.100.1.10/24'},
                     params2={'ip': '10.100.1.20/24'})
        
        self.addLink(ra,
                     rc,
                     intfName1='ra-eth3',
                     intfName2='rc-eth2',
                     params1={'ip': '10.101.2.10/24'},
                     params2={'ip': '10.101.2.20/24'})

        self.addLink(rb,
                     rc,
                     intfName1='rb-eth3',
                     intfName2='rc-eth3',
                     params1={'ip': '10.102.3.10/24'},
                     params2={'ip': '10.102.3.20/24'})

        h1 = self.addHost(name='h1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2',
                          ip='10.0.0.252/24',
                          defaultRoute='via 10.0.0.1')
        h3 = self.addHost(name='h3',
                          ip='10.1.0.251/24',
                          defaultRoute='via 10.1.0.1')
        h4 = self.addHost(name='h4',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        h5 = self.addHost(name='h5',
                          ip='10.2.0.251/24',
                          defaultRoute='via 10.2.0.1')
        h6 = self.addHost(name='h6',
                          ip='10.2.0.252/24',
                          defaultRoute='via 10.2.0.1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)

def run():
    topo = Topology()
    net = Mininet(topo)
    net.start()
    info(net['ra'].cmd('ip route add 10.1.0.0/24 via 10.100.1.20 dev ra-eth2'))
    info(net['ra'].cmd('ip route add 10.2.0.0/24 via 10.101.2.20 dev ra-eth3'))
    info(net['rb'].cmd('ip route add 10.0.0.0/24 via 10.100.1.10 dev rb-eth2'))
    info(net['rb'].cmd('ip route add 10.2.0.0/24 via 10.102.3.20 dev rb-eth3'))
    info(net['rc'].cmd('ip route add 10.0.0.0/24 via 10.101.2.10 dev rc-eth2'))
    info(net['rc'].cmd('ip route add 10.1.0.0/24 via 10.102.3.10 dev rc-eth3'))
    CLI(net) 

if __name__ == '__main__':
    setLogLevel('info')
    run()
