# 🏗️ Banco de Ensayo – Viga Simplemente Apoyada

Aplicación en Python para el control y visualización de un banco de ensayo de una viga simplemente apoyada, desarrollada como herramienta didáctica para laboratorio de Física.

---

## 🎯 Objetivo

Permitir:

- Control del banco de ensayo mediante Arduino
- Visualización en tiempo real de magnitudes físicas
- Interfaz gráfica clara y robusta para laboratorio
- Compatibilidad Windows ↔ Raspberry Pi

---

## 🖥️ Tecnologías utilizadas

- Python 3.11
- PySide6 (GUI)
- PySerial (comunicación serie)
- Arduino (control y adquisición)

---

## 🧩 Arquitectura del proyecto

```text
beam_app/
│
├── main.py
│
├── ui/
│   ├── main_window.py
│   └── graphics.py
│
├── controllers/
│   └── main_controller.py
│
├── core/
│   └── serial_manager.py
│
├── config/
│   └── app_config.py
│
├── assets/
│   └── images/
│       ├── app.png
│       └── udemm_logo.png
│
├── run.bat
├── run.sh
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

### Windows

```bash
run.bat
```

### Linux / Raspberry Pi

```bash
chmod +x run.sh
./run.sh
```

O manual:

```bash
python main.py
```

---

## 🔌 Comunicación con Arduino

La comunicación se realiza vía puerto serie usando **PySerial** y un hilo de lectura dedicado.

### Comandos enviados

```json
{"info":"status"}
{"info":"all-params"}
{"distance":500}
{"force":2500}
{"cmd":"start"}
```

### Respuestas del Arduino

```json
{"info":"status","status":0}

{"info":"all-params",
 "distance":500,
 "force":2500,
 "reaction_one":1250,
 "reaction_two":1250,
 "flexion":2120.082,
 "st_test":0
}

{"cmd":"start","result":"ack"}

{"st_test":0}
```

---

## 🧠 Lógica actual del sistema

### Botón **Refrescar**

1. Envía `{"info":"status"}`
2. Si `status == 0`, envía `{"info":"all-params"}`
3. Actualiza la interfaz con:
   - distancia
   - carga
   - reacción 1
   - reacción 2
   - flexión
   - estado del ensayo

### Botón **Iniciar**

1. Verifica estado con `{"info":"status"}`
2. Si el ensayo está apagado:
   - envía distancia en mm
   - envía carga en g
   - envía `{"cmd":"start"}`
3. La GUI cambia a estado encendido al recibir `ack`
4. Al recibir `{"st_test":0}`, la GUI vuelve a apagado

### Parsing serie

El controlador reconstruye los JSON desde el stream serie, soportando múltiples objetos consecutivos en la misma ráfaga de datos.

---

## 📊 Funcionalidades actuales

- Interfaz gráfica moderna en PySide6
- Conexión y desconexión por puerto serie
- Refresco inteligente de parámetros
- Inicio de ensayo desde GUI
- Visualización de:
  - fuerza de reacción 1
  - fuerza de reacción 2
  - flexión
  - estado del ensayo
- Gauges analógicos configurables
- Auto-actualización del estado al finalizar un ensayo
- Logs de depuración del flujo serie

---

## ⚙️ Configuración

La configuración principal está centralizada en:

```python
config/app_config.py
```

Ejemplos de parámetros configurables:

```python
DEFAULT_DISTANCE = "500"
DEFAULT_LOAD = "2500"

LOAD_OPTIONS = ["0", "500", "1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000"]

UNIT_FORCE = "g"
UNIT_FLEX = "mm"

REACTION_GAUGE_MIN = 0
REACTION_GAUGE_MAX = 8000
REACTION_GAUGE_INITIAL = 0
```

---

## 🖼️ Captura de la aplicación

![Captura de la aplicación](assets/images/app.png)
---

## 🚧 Estado del proyecto

Base funcional completa:

- ✅ Comunicación estable con Arduino
- ✅ Flujo de refresco operativo
- ✅ Inicio de ensayo desde GUI
- ✅ Parsing robusto de respuestas JSON
- ✅ Visualización del estado del ensayo

Pendiente:

- [ ] Registro de datos a archivo
- [ ] Exportación de resultados
- [ ] Curvas de ensayo
- [ ] Ajustes finales de UX para laboratorio

---


## 🔧 Simulación Arduino

El repositorio incluye un simulador del banco de ensayo desarrollado en Arduino:

```text
flexion_viga_simulacion/

Este módulo permite:

Simular el comportamiento del banco sin hardware real
Probar la comunicación serie desde la aplicación Python
Validar el flujo completo del ensayo
▶️ Uso
Abrir el archivo:
flexion_viga_simulacion/flexion_viga.ino
Compilar y cargar en una placa Arduino
Conectar la aplicación Python al puerto serie correspondiente
📌 Nota

Las librerías utilizadas deben instalarse desde el Arduino IDE (Library Manager) si no están disponibles en el entorno local.

## 🧠 Contexto académico

Aplicación orientada al estudio de:

- Vigas simplemente apoyadas
- Equilibrio estático
- Reacciones en apoyos
- Flexión y deformación

---

## 🤝 Contribuciones

Proyecto en desarrollo activo.  
Las sugerencias y mejoras son bienvenidas.

---

## 📄 Licencia

Uso académico / educativo.
