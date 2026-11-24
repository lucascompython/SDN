#!/usr/bin/env python3

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo


class DoisSites(Topo):
    """n hosts em cada site; s1-s2 é a ligação WAN."""

    def build(self, n=2, bw=100, delay="2ms", loss=0):
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        for i in range(1, n + 1):
            self.addLink(self.addHost(f"a{i}"), s1)
            self.addLink(self.addHost(f"b{i}"), s2)
        self.addLink(s1, s2, bw=bw, delay=delay, loss=loss)


# permite: sudo mn --custom dois_sites.py --topo doissites,3 --link tc
topos = {"doissites": DoisSites}
if __name__ == "__main__":
    setLogLevel("info")
    net = Mininet(topo=DoisSites(n=2, bw=10, delay="20ms"), link=TCLink)
    net.start()
    net.pingAll()
    a1, b1 = net.get("a1", "b1")
    net.iperf((a1, b1))
    CLI(net)
    net.stop()
