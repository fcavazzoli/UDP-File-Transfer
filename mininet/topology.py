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
        # First host should act as server.
        for i in range(1, num_hosts + 1):
            host = self.addHost("h{0}".format(i), ip="10.0.0.{0}".format(i))

        # Add switch
        print("Adding switch s1..")
        s1 = self.addSwitch('s1')

        # Add links from hosts to switch.
        # Add package loss to the first host only regarding on package_loss value.
        for i in range(1, num_hosts + 1):
            if i == 1:
            	print("Adding server h{0}..".format(i))
            	self.addLink("h{0}".format(i), s1, cls=TCLink, loss=package_loss)
            else:
            	print("Adding host h{0}..".format(i))
            	self.addLink("h{0}".format(i), s1, cls=TCLink)
            	
topos = {'project': (lambda: Project())}