# Game Launcher 🎮

Un lanzador de juegos arcade interactivo construido con Pygame. Este proyecto proporciona una interfaz visual elegante para seleccionar y ejecutar múltiples juegos.

## 🎯 Características

- **Interfaz Gráfica Moderna**: Diseño elegante con tarjetas visuales para cada juego
- **Soporte para Joystick/Gamepad**: Navegación completa con controles de gamepad
- **Pantalla Completa**: Experiencia inmersiva en modo fullscreen
- **Imagenes de Portada**: Cada juego puede tener su propia imagen de portada
- **Esquema de Colores Personalizables**: Paleta de colores configurable

## 📋 Requisitos

- Python 3.7+
- Pygame

## ⚙️ Instalación

1. Clonar el repositorio:

```bash
git clone <repository-url>
cd game-launcher
```

2. Instalar dependencias:

```bash
pip install pygame
```

3. Configurar los juegos en `main.py` según necesites (ver sección de Configuración)

## 🚀 Uso

Ejecutar el lanzador:

```bash
python main.py
```

### Controles

- **Flechas Izquierda/Derecha**: Navegar entre juegos
- **Enter/Space**: Seleccionar y ejecutar juego
- **ESC**: Salir del lanzador
- **Gamepad**: Controles analógicos y botones

## ⚙️ Configuración

En `main.py`, puedes personalizar los juegos editando la lista `GAMES`:

```python
GAMES = [
    {
        "title": "Nombre del Juego",
        "subtitle": "Categoría / Género",
        "command": ["python3", "ruta/al/juego/main.py"],
        "image": "ruta/a/imagen.jpg",
        "color": (R, G, B),  # Color de la tarjeta
    },
    # ... más juegos
]
```

### Variables de Configuración

- `FPS`: Fotogramas por segundo (por defecto: 60)
- `MOVE_COOLDOWN_MS`: Tiempo entre movimientos de navegación (ms)
- `CONFIRM_COOLDOWN_MS`: Tiempo entre confirmaciones (ms)
- `BASE_DIR`: Directorio base donde están los juegos
- Colores personalizables para la interfaz

## 📁 Estructura del Proyecto

```
game-launcher/
├── main.py           # Archivo principal del lanzador
├── assets/           # Carpeta para imágenes de portadas
│   ├── astrorehab.jpg
│   └── surferrehab.jpg
└── README.md         # Este archivo
```

## 🎨 Personalización de Colores

Edita las constantes de color en `main.py`:

```python
COLOR_BG = (16, 18, 24)           # Fondo
COLOR_PANEL = (28, 30, 38)        # Panel
COLOR_CARD = (45, 48, 60)         # Tarjeta
COLOR_TEXT = (245, 245, 245)      # Texto principal
COLOR_SUBTEXT = (170, 175, 185)   # Subtexto
COLOR_HIGHLIGHT = (255, 210, 90)  # Resaltado
COLOR_EXIT = (130, 60, 60)        # Botón salir
```

## 💡 Notas

- Los juegos deben ser ejecutables mediante línea de comandos
- Las imágenes de portada se escalarán automáticamente
- El lanzador se adapta a cualquier resolución de pantalla

## 📄 Licencia

Este proyecto está disponible bajo la licencia que prefieras.

## 👨‍💻 Autor

Proyecto personal de juegos arcade.

---

¡Disfruta jugando! 🎮
