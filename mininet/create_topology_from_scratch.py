import os
import sys
import subprocess

ARGUMENTS_AMOUNT = 3
PACKAGE_LOSS_PATH = "package_loss.txt"
HOSTS_AMOUT_PATH = "amount_hosts.txt"


def append_logs(log, path):
    try:
        with open(path, "r") as f:
            old_content = f.read()
            with open(path, "w") as f:
                f.write(log)
                f.write("\n")
                f.write(old_content)
    except FileNotFoundError:
        with open(path, "w") as f:
            f.write(log)


def create_logs(package_loss, hosts_amount):
    print("La probabilidad de la perdida de paquetes sera: {0}".format(package_loss))
    print("El numero de hosts sera: {0}".format(hosts_amount))
    append_logs(str(hosts_amount), HOSTS_AMOUT_PATH)
    append_logs(str(package_loss), PACKAGE_LOSS_PATH)


if len(sys.argv) != ARGUMENTS_AMOUNT:
    print("Por favor ingresa como primer parametro la cantidad de hosts (entre 2 y 10) y como segundo parametro, el porcentaje de package loss (entre 0 y 100.")
    hosts_parameter = input("Ingrese la cantidad de hosts: ")
    package_loss_parameter = input("Ingrese el porcentaje de perdida de paquetes: ")
else:
    hosts_parameter = sys.argv[1]
    package_loss_parameter = sys.argv[2]

    if hosts_parameter.isdigit() and package_loss_parameter.isdigit():
        package_loss = int(package_loss_parameter)
        hosts_amount = int(hosts_parameter)
        if package_loss >= 0 and package_loss <= 100:
            if hosts_amount >= 1 and hosts_amount <= 10:
                create_logs(package_loss, hosts_amount)
                mn_command = ["sudo", "mn", "--custom", "topology.py", "--topo", "project"]
                subprocess.run(mn_command)
            else:
                print("Error: el primer parametro (cantidad de hosts) tiene que estar entre 2 y 10.")
        else:
            print("Error: el segundo parametro (procentaje de la perdida de paquetes) tiene que estar entre 0 y 100.")
    else:
        print("Error: Todos los inputs deben ser numeros.")
