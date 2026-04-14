from pathlib import Path
import platform


# =========================
# RUTAS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
LOGO_PATH = IMAGES_DIR / "udemm_logo.png"


# =========================
# DATOS DE APP
# =========================
WINDOW_TITLE = "Banco de Ensayo - Viga Simplemente Apoyada"
APP_SUBTITLE = "FACULTAD DE INGENIERÍA - FÍSICA 1"
APP_TITLE = "VIGA SIMPLEMENTE APOYADA"
APP_VERSION = "v0.1.0"
GITHUB_URL = "https://github.com/"


# =========================
# PLATAFORMA
# =========================
SYSTEM_NAME = platform.system().lower()
IS_WINDOWS = SYSTEM_NAME == "windows"
IS_LINUX = SYSTEM_NAME == "linux"


# =========================
# SERIAL
# =========================
DEFAULT_BAUDRATE = 115200

if IS_WINDOWS:
    DEFAULT_SERIAL_PORT = "COM3"
    SERIAL_PORT_OPTIONS = ["COM3", "COM4", "COM5", "COM6"]
elif IS_LINUX:
    DEFAULT_SERIAL_PORT = "/dev/ttyACM0"
    SERIAL_PORT_OPTIONS = ["/dev/ttyACM0", "/dev/ttyUSB0", "/dev/ttyUSB1"]
else:
    DEFAULT_SERIAL_PORT = ""
    SERIAL_PORT_OPTIONS = []


# =========================
# FLAGS VISUALES
# =========================
SHOW_FLEX_SECTION  = False
SHOW_REACTION_GAUGES = True


# =========================
# TEXTOS DE UI
# =========================
SECTION_INPUTS = "Entradas del ensayo"
SECTION_OUTPUTS = "Salidas del ensayo"

LABEL_DISTANCE = "Distancia (mm)"
LABEL_LOAD = "Carga (kg)"
LABEL_PORT = "Puerto:"

CARD_R1_TITLE = "Fuerza de reacción 1"
CARD_R2_TITLE = "Fuerza de reacción 2"
CARD_FLEX_TITLE = "Flexión"
CARD_STATUS_TITLE = "Status del ensayo"

STATUS_READY = "Listo"
STATUS_GUI_ONLY = "Estado: GUI sin lógica"

BUTTON_GITHUB = "GitHub"
BUTTON_REFRESH_PORTS = "Actualizar COMs"
BUTTON_CONNECT = "Conectar"
BUTTON_DISCONNECT = "Desconectar"
BUTTON_START = "Iniciar"
BUTTON_REFRESH = "Refrescar"


# =========================
# VALORES INICIALES
# =========================
DEFAULT_DISTANCE = "0"
DEFAULT_LOAD = "0"
LOAD_OPTIONS = ["0", "1", "2", "5", "10"]


UNIT_FORCE = "kg"
UNIT_FLEX = "mm"

INITIAL_R1_VALUE = f"0.0 {UNIT_FORCE}"
INITIAL_R2_VALUE = f"0.0 {UNIT_FORCE}"
INITIAL_FLEX_VALUE = f"0.0 {UNIT_FLEX}"
INITIAL_STATUS_VALUE = STATUS_READY