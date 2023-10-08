from mininet.topo import Topo
from mininet.link import TCLink
import sys

PACKAGE_LOSS_PATH = "package_loss.txt"
HOSTS_AMOUNT_PATH = "amount_hosts.txt"

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

        num_hosts = get_first_value_from_file(HOSTS_AMOUNT_PATH)
        package_loss = get_first_value_from_file(PACKAGE_LOSS_PATH)

        # Add hosts
        for i in range(1, num_hosts + 1):
            host = self.addHost("h{0}".format(i), ip="10.0.0.{0}".format(i))

        # Add switch
        s1 = self.addSwitch('s1')

        # Add links from hosts to switch without specifying loss
        for i in range(1, num_hosts + 1):
            self.addLink("h{0}".format(i), s1, cls=TCLink)

        # Add package loss to the first host's interface.
        # First host should act as server.
        h1_intf = s1.intf('s1-eth1')
        h1_intf.config(loss=package_loss)

topos = {'project': (lambda: Project())}
