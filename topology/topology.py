from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


class AdaptiveTopo(Topo):

    def build(self):

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')

        self.addLink(h1, s1)

        self.addLink(s1, s2)
        self.addLink(s1, s3)

        self.addLink(s2, s4)
        self.addLink(s3, s4)

        self.addLink(s4, h2)


def run():

    topo = AdaptiveTopo()

    net = Mininet(
        topo=topo,
        controller=None
    )

    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6653
    )

    net.start()

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
