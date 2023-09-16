## Observaciones
Por ahora se ejecuta desde directorio raiz como:
```python src/upload.py -v -H host -p puerto```
TODO: Cambiarlo a como lo pide el enunciado, ```python upload ...```, es cambiando la ubicacion de los archivos? poner un init.py?

---

## Interfaz del cliente
La funcionalidad del cliente se divide en dos aplicaciónes de línea de comandos: upload y download

### Upload
Para enviar un archivo al servidor y que sea guardado con un nombre especificado

```bash
> python upload -h
usage : upload [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s FILEPATH ] [-n FILENAME ]
<command description >
optional arguments :
-h, --help show this help message and exit
-v, -- verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-s, --src source file path
-n, --name file name
```


### Download
Para enviar un archivo al servidor y que sea guardado con un nombre especificado

```bash
> python download -h
usage : download [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-d FILEPATH ] [-n FILENAME ]
<command description >
optional arguments :
-h, --help show this help message and exit
-v, -- verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-d, --dst destination file path
-n, --name file name
```

## Interfaz del servidor
El servidor provee el servicio de almacenamiento y descarga de archivos

```bash
> python start - server -h
usage : start - server [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s DIRPATH ]
<command description >
optional arguments :
-h, --help show this help message and exit
-v, -- verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host service IP address
-p, --port service port
-s, -- storage storage dir path
```