# SIRC - Sistema Inteligente de Respaldo y Compresión

## Descripción

SIRC es un sistema de respaldo inteligente que utiliza paralelización con Dask para optimizar las operaciones de compresión y cifrado de archivos. El sistema permite crear respaldos seguros con múltiples algoritmos de compresión y cifrado AES-256, con integración opcional a Dropbox.

## Características

- **Compresión paralela** con Dask (ZIP, GZIP, BZIP2)
- **Cifrado AES-256** con derivación de claves PBKDF2
- **Interfaz gráfica** intuitiva con Tkinter
- **Integración con Dropbox** para almacenamiento en la nube
- **Procesamiento paralelo** de múltiples archivos y carpetas
- **Arquitectura modular** y extensible

## Requisitos del Sistema

### Software Requerido
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias
Las dependencias se instalan automáticamente desde \`requirements.txt\`:

\`\`\`
dask[complete]
cryptography
tk
pyzipper
dropbox
python-dotenv
\`\`\`

## Instalación

### 1. Clonar el repositorio
\`\`\`bash
git clone <url-del-repositorio>
cd sirc-backup-system
\`\`\`

### 2. Crear entorno virtual (recomendado)
\`\`\`bash
python -m venv venv

# En Windows
venv\\Scripts\\activate

# En Linux/macOS
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configuración de Dropbox (opcional)
Si deseas usar la integración con Dropbox:

1. Crea una aplicación en [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Obtén tu token de acceso
3. Crea un archivo \`.env\` en el directorio raíz:
\`\`\`
DROPBOX_TOKEN=tu_token_aqui
\`\`\`

## Uso

### Ejecutar la aplicación
\`\`\`bash
python gui.py
\`\`\`

### Funcionalidades principales

1. **Seleccionar archivos/carpetas**: Usa los botones para seleccionar los elementos a respaldar
2. **Elegir compresión**: Selecciona entre ZIP, GZIP o BZIP2
3. **Cifrado opcional**: Activa el cifrado y establece una contraseña
4. **Crear respaldo**: Ejecuta el proceso de respaldo
5. **Subir a Dropbox**: Opcionalmente sube el respaldo a la nube
6. **Descifrar archivos**: Usa la función de descifrado para recuperar archivos

### Uso programático

#### Compresión básica
\`\`\`python
from compression_dask import compress_all_to_one

paths = ['/ruta/archivo1.txt', '/ruta/carpeta1']
compress_all_to_one(paths, 'respaldo.zip', 'zip')
\`\`\`

#### Cifrado de archivos
\`\`\`python
from encryption_dask import encrypt_file_dask
from dask import compute

task = encrypt_file_dask('archivo.txt', 'archivo.enc', key, iv)
compute(task)
\`\`\`

## Arquitectura del Sistema

### Módulos principales

- **\`gui.py\`**: Interfaz gráfica principal
- **\`compression_dask.py\`**: Compresión paralela con Dask
- **\`encryption_dask.py\`**: Cifrado paralelo con Dask
- **\`parallel_utils.py\`**: Utilidades para procesamiento paralelo
- **\`compression.py\`**: Funciones de compresión básicas
- **\`encryption.py\`**: Funciones de cifrado básicas

### Flujo de trabajo

1. **Selección**: El usuario selecciona archivos/carpetas
2. **Preparación**: Los archivos se copian a un directorio temporal
3. **Compresión**: Se aplica compresión paralela usando Dask
4. **Cifrado**: Opcionalmente se cifra el archivo resultante
5. **Almacenamiento**: Se guarda localmente y/o se sube a Dropbox

## Resolución de Problemas

### Errores comunes

1. **Error de importación de tkinter**:
   \`\`\`bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   \`\`\`

2. **Error de permisos**:
   - Asegúrate de tener permisos de lectura en los archivos fuente
   - Verifica permisos de escritura en el directorio destino

3. **Error de memoria**:
   - Para archivos muy grandes, considera aumentar la memoria disponible
   - Ajusta el tamaño de bloque en \`BLOCK_SIZE\`

### Logs y depuración

El sistema utiliza el logging estándar de Python. Para habilitar logs detallados:

\`\`\`python
import logging
logging.basicConfig(level=logging.DEBUG)
\`\`\`

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (\`git checkout -b feature/nueva-funcionalidad\`)
3. Commit tus cambios (\`git commit -am 'Agrega nueva funcionalidad'\`)
4. Push a la rama (\`git push origin feature/nueva-funcionalidad\`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor crea un issue en el repositorio del proyecto.
\`\`\`
