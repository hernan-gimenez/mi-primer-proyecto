# Gestor de Enlaces

Aplicación web para guardar y gestionar enlaces importantes.

## Características

- Guarda enlaces con título y descripción
- Lista todos los enlaces guardados
- Elimina enlaces que ya no necesites
- Interfaz web sencilla e intuitiva
- Base de datos SQLite para persistencia de datos
- Arquitectura hexagonal para mejor mantenibilidad

## Requisitos

- Python 3.9 o superior
- Docker y Docker Compose (opcional)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/mi-primer-proyecto.git
cd mi-primer-proyecto
```

2. Crea y activa un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Opción 1: Ejecución local

1. Inicia la aplicación:
```bash
uvicorn src.main:app --reload
```

2. Abre tu navegador en:
```
http://localhost:8000
```

### Opción 2: Usando Docker

1. Construye y ejecuta los contenedores:
```bash
docker-compose up --build
```

2. La aplicación estará disponible en:
```
http://localhost:8000
```

## Estructura del Proyecto

```
src/
├── domain/           # Entidades y objetos de valor
├── application/      # Casos de uso y puertos
└── infrastructure/   # Implementaciones concretas
    ├── database/     # Configuración de la base de datos
    ├── repositories/ # Implementaciones de repositorios
    └── api/         # API REST
```

## API Endpoints

- `GET /` - Página de inicio
- `GET /api/links/` - Obtener todos los enlaces
- `POST /api/links/` - Crear un nuevo enlace
- `DELETE /api/links/{id}` - Eliminar un enlace

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
