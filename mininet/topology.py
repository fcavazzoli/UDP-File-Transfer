from mininet.topo import Topo
from mininet.link import TCLink
import sys

PACKAGE_LOSS_PATH = "package_loss.txt"
HOSTS_AMOUT_PATH = "amount_hosts.txt"


def get_first_value_from_file(path):
    try:
        with open(path, "r") as f:
            return int(f.readline())
    except FileNotFoundError:
        print("Error: El archivo ha sido eliminado durante la ejecución. Vuelva a intentar.")


class Project(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        num_hosts = get_first_value_from_file(HOSTS_AMOUT_PATH)
        package_loss = get_first_value_from_file(PACKAGE_LOSS_PATH)

        # Add hosts
        for i in range(1, num_hosts + 1):
            host = self.addHost(F"h{i}", ip=F"10.0.0.{i}")

        # Add switch
        s1 = self.addSwitch('s1')

        # Add links
        for i in range(1, num_hosts + 1):
            self.addLink(F"h{i}", s1, cls=TCLink, loss=package_loss)


topos = {'project': (lambda: Project())}
