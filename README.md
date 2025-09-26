# TAREA3_PCD: Users API

Este proyecto implementa una API REST para la gestión de usuarios, construida con **FastAPI** como framework, **Pydantic** para la validación de datos y **SQLAlchemy** como ORM para la persistencia en base de datos. La seguridad de las rutas principales se garantiza mediante una clave de API.

---

## Instalación y configuración

El proyecto utiliza **uv** como gestor de dependencias y requiere **Python 3.13**.

### 1. Requisitos previos
Verificar que la versión de Python instalada sea la indicada y contar con la herramienta `uv`.

### 2. Creación del entorno virtual e instalación de dependencias
A partir del archivo `uv.lock` es posible instalar todas las dependencias en un entorno virtual:

```bash
# Sincronizar dependencias e instalar el entorno virtual
uv sync

# Activar el entorno virtual antes de ejecutar la aplicación
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
