# trabajo-practico-topologia
Topologia del trabajo practico

## Prerrequisitos de instalacion en Ubuntu para mininet

```
sudo apt-get -y install xterm
```

## Instalación de mininet en Ubuntu

```
sudo apt-get install mininet
```

## Como correr la topologia 

Desde la consola ejecutar (por ejemplo con 2 hosts y con un 10% de pérdida de paquetes):

```
python3 create_topology_from_scratch.py 2 10
```

El parámetro es referido a la cantidad de hosts, y tiene que ser un número positivo, mayor a 2 y menor a 10. Debe ser mayor a 2 para que puedan realizarse transferencias.

## Como utilizar mininet

Para correr la consola de un host:

```
h1 xterm &
```

## Logs creados

Se crearán dos archivos con los sobre la cantidad de hosts y porcentajes de pérdidas de paquetes definidos.

## Troubleshoot

En caso de que no corra mininet con un error relacionado a los controllers, intentar con este comando:

```
sudo fuser -k 6653/tcp
```
