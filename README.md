# Data Processor — Contenedor Docker para procesamiento de CSV

Script de Python que lee un CSV, elimina filas duplicadas, añade una columna con la marca de tiempo del procesamiento y escribe el resultado en otra ruta. Todo empaquetado en una imagen Docker publicada en Docker Hub.

Las rutas de entrada y salida **no están fijas en el código**: se configuran mediante variables de entorno, y los datos se intercambian con el host mediante un *bind mount*.

## Estructura del repositorio

```
archivos/
├── process.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── datos/
    └── input.csv        # CSV
```

## Imagen publicada

- Docker Hub: `ronnypin/data-processor:v1.0.0`
- Enlace: https://hub.docker.com/r/ronnypin/data-processor
- Evidencia de publicación: [`docs/dockerhub-evidencia.png`](docs/dockerhub-evidencia.png)

## Requisitos previos

- Docker instalado y en ejecución (no se necesita Python ni pandas en el host).

## Variables de entorno

| Variable | Descripción | Obligatoria | Valor por defecto |
|----------|-------------|-------------|-------------------|
| `INPUT_PATH` | Ruta del CSV de entrada **dentro del contenedor** | No | `/data/input.csv` |
| `OUTPUT_PATH` | Ruta del CSV de salida **dentro del contenedor** | No | `/data/output.csv` |

## Volúmenes

| Ruta en el contenedor | Uso | Modo sugerido |
|-----------------------|-----|---------------|
| `/data` | Directorio donde viven el CSV de entrada y el de salida | Lectura/escritura (`-v host:/data`) |

El contenedor se ejecuta con un usuario sin privilegios (`appuser`), por lo que el directorio montado debe permitir la escritura a ese usuario (en Windows/macOS con Docker Desktop no requiere configuración adicional).

## Puertos

**No aplica.** El script es un proceso por lotes (*batch*) que no expone ningún servicio de red ni escucha en ningún puerto.

## Construcción

Desde la raíz del repositorio:

```bash
docker build -t ronnypin/data-processor:v1.0.0 .

## Ejecución con los datos de ejemplo

El repositorio incluye `datos/input.csv`, por lo que no hace falta preparar nada:

```bash
docker run --rm \
  -v $(pwd)/datos:/data \
  -e INPUT_PATH=/data/input.csv \
  -e OUTPUT_PATH=/data/output.csv \
  ronnypin/data-processor:v1.0.0
```

En **Windows PowerShell** sustituye `$(pwd)` por `${PWD}` y las barras invertidas por acentos graves (`` ` ``) para continuar líneas.

### Contenido de `datos/input.csv`

```csv
id,nombre,valor
1,Alice,100
2,Bob,200
1,Alice,100
4,Carol,300
```

## Ejecución con tus propios datos

Monta cualquier carpeta del host en `/data` y ajusta las rutas:

```bash
docker run --rm \
  -v /ruta/a/mis/csv:/data \
  -e INPUT_PATH=/data/mi_archivo.csv \
  -e OUTPUT_PATH=/data/mi_resultado.csv \
  ronnypin/data-processor:v1.0.0
```

## Salida esperada

Salida por consola (la marca de tiempo variará):

```
[2026-11-19 10:30:00.123456] Iniciando procesamiento...
Entrada: /data/input.csv
Salida: /data/output.csv
Procesamiento completado. Filas: 3. Archivo escrito en: /data/output.csv
```

Contenido generado en `datos/output.csv` (la fila duplicada `1,Alice,100` fue eliminada y se añadió la columna `processed_at`):

```csv
id,nombre,valor,processed_at
1,Alice,100,2026-11-19T10:30:00.123456
2,Bob,200,2026-11-19T10:30:00.123456
4,Carol,300,2026-11-19T10:30:00.123456
```

## Publicación de la imagen (referencia)

```bash
docker login
docker build -t ronnypin/data-processor:v1.0.0 .
docker push ronnypin/data-processor:v1.0.0
```

## Decisiones de diseño del Dockerfile

- **Base fija y slim:** `python:3.11-slim`, evitando `latest` para garantizar builds reproducibles.
- **Caché de capas:** `requirements.txt` se copia e instala **antes** de copiar `process.py`, de modo que cambiar el código no invalida la capa de dependencias.
- **Usuario sin privilegios:** se crea `appuser` y se activa con `USER appuser`; el contenedor no se ejecuta como root.
- **`CMD` en forma exec:** `CMD ["python", "process.py"]`, para que el proceso reciba correctamente las señales del sistema.
- **`.dockerignore`:** excluye `.git`, `.env`, entornos virtuales, `__pycache__`, la carpeta `datos/` y los `*.csv`, evitando meter datos en la imagen.

## Prueba de aceptación realizada

1. `docker rmi ronnypin/data-processor:v1.0.0` (se elimina la imagen local).
2. `docker pull ronnypin/data-processor:v1.0.0` (se descarga desde el registro).
3. Se ejecuta el comando de la sección **Ejecución con los datos de ejemplo**.

Resultado: el proceso finaliza correctamente y `datos/output.csv` se genera con el contenido mostrado arriba.