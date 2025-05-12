import sys
import os
from pathlib import Path

# Añadir el directorio padre al PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from src.infrastructure.api.server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
