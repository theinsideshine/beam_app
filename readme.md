# 🏗️ Banco de Ensayo – Viga Simplemente Apoyada

Aplicación en Python para el control y visualización de un banco de ensayo de una viga simplemente apoyada, desarrollada como herramienta didáctica para laboratorio de Física.

---

## 🎯 Objetivo

Permitir:

* Control del banco de ensayo mediante Arduino
* Visualización en tiempo real de magnitudes físicas
* Interfaz gráfica simple y clara para uso en laboratorio
* Compatibilidad entre desarrollo en Windows y ejecución en Raspberry Pi

---

## 🖥️ Tecnologías utilizadas

* Python 3.11
* PySide6 (GUI)
* PySerial (comunicación serie)
* Python-dotenv (configuración)
* Arduino (hardware de adquisición/control)

---

## 🧩 Arquitectura del proyecto

```text
beam_app/
│
├── main.py                # Punto de entrada
│
├── ui/                    # Interfaz gráfica
│   ├── main_window.py
│   └── graphics.py
│
├── core/                  # Lógica base
│   └── serial_manager.py
│
├── config/                # Configuración centralizada
│   └── app_config.py
│
├── assets/
│   └── images/            # Recursos gráficos
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/beam_app.git
cd beam_app
```

---

### 2. Crear entorno virtual

#### Windows

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

#### Linux / Raspberry Pi

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python main.py
```

---

## 🔌 Comunicación con Arduino

El sistema se conecta mediante puerto serie.

Configuración desde:

```python
config/app_config.py
```

Ejemplo:

```python
DEFAULT_SERIAL_PORT = "COM3"        # Windows
# DEFAULT_SERIAL_PORT = "/dev/ttyACM0"  # Linux / Raspberry
```

---

## 📊 Funcionalidades actuales

* Interfaz gráfica moderna
* Visualización de:

  * Fuerzas de reacción
  * Estado del ensayo
* Gauges analógicos (widgets personalizados)
* Configuración centralizada
* Base para lectura en tiempo real

---

## 🚧 Estado del proyecto

En desarrollo activo:

* [ ] Integración completa con Arduino
* [ ] Lectura en tiempo real
* [ ] Automatización del ensayo
* [ ] Registro de datos
* [ ] Exportación de resultados

---

## 🧠 Contexto académico

Este proyecto se enmarca en el estudio de:

* Vigas simplemente apoyadas
* Equilibrio estático
* Reacciones en apoyos
* Deformaciones (flexión)

---

## 🤝 Contribuciones

Proyecto en desarrollo. Cualquier sugerencia o mejora es bienvenida.

---

## 📄 Licencia

Uso académico / educativo.
