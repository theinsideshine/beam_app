import json
import serial.tools.list_ports

from core.serial_manager import SerialManager


class MainController:
    def __init__(self, view):
        self.view = view
        self.serial_manager = SerialManager()

        self._json_buffer = []
        self._receiving_json = False
        self._pending_start = False

        self.setup_connections()
        self.refresh_ports()
        self.update_ui_state()
        self._waiting_manual_response = False
        self._auto_refresh_done = False

    def setup_connections(self):
        self.view.btn_actualizar.clicked.connect(self.refresh_ports)
        self.view.btn_conectar.clicked.connect(self.connect_serial)
        self.view.btn_desconectar.clicked.connect(self.disconnect_serial)
        self.view.btn_refrescar.clicked.connect(self.refresh_data)
        self.view.btn_iniciar.clicked.connect(self.start_test)

    # -----------------------------------------
    # PUERTOS
    # -----------------------------------------
    def refresh_ports(self):
        puerto_actual = self.view.puerto_combo.currentText()

        self.view.puerto_combo.clear()
        ports = serial.tools.list_ports.comports()

        for port in ports:
            self.view.puerto_combo.addItem(port.device)

        if puerto_actual:
            index = self.view.puerto_combo.findText(puerto_actual)
            if index >= 0:
                self.view.puerto_combo.setCurrentIndex(index)

        if not ports:
            self.view.status_label.setText("Sin puertos disponibles")
            print("No se encontraron puertos serie")
        else:
            self.view.status_label.setText("Puertos actualizados")

    # -----------------------------------------
    # CONEXIÓN
    # -----------------------------------------
    def connect_serial(self):
        print("[UI] Botón: Conectar")

        if self.serial_manager.is_connected():
            self.view.status_label.setText("Ya conectado")
            return

        port = self.view.puerto_combo.currentText().strip()
        if not port:
            self.view.status_label.setText("Seleccione un puerto")
            print("No hay puerto seleccionado")
            return

        success = self.serial_manager.connect(port)

        if not success:
            self.view.status_label.setText(f"Error al conectar a {port}")
            print(f"No se pudo conectar a {port}")
            self.update_ui_state()
            return

        self.view.status_label.setText(f"Conectado a {port}")
        print(f"Conectado a {port}")

        self.serial_manager.read_lines(self.handle_serial_data)
        self.update_ui_state()

    def disconnect_serial(self):
        print("[UI] Botón: Desconectar")

        if not self.serial_manager.is_connected():
            self.view.status_label.setText("No hay conexión activa")
            self.update_ui_state()
            return

        self.serial_manager.disconnect()
        self.view.status_label.setText("Desconectado")
        print("Desconectado del puerto serie")

        self._json_buffer.clear()
        self._receiving_json = False
        self._pending_start = False

        self.update_status_indicator(0)
        self.reset_outputs()
        self.update_ui_state()

    # -----------------------------------------
    # REFRESH
    # -----------------------------------------
    def refresh_data(self):
        print("[UI] Botón: Refrescar")

        if not self.serial_manager.is_connected():
            print("[FLOW] Refresh cancelado: serial desconectado")
            self.view.status_label.setText("Apagado")
            self.update_status_indicator(0)
            return

        print("[FLOW] Refresh -> request_status()")
        self._waiting_manual_response = True
        self.request_status()

    # -----------------------------------------
    # INICIAR ENSAYO
    # -----------------------------------------
    def start_test(self):
        print("[UI] Botón: Iniciar")

        if not self.serial_manager.is_connected():
            print("[FLOW] Start cancelado: serial desconectado")
            self.view.status_label.setText("Apagado")
            self.update_status_indicator(0)
            return

        self._pending_start = True
        self._auto_refresh_done = False
        print("[FLOW] Start -> pending_start=True -> request_status()")
        self._waiting_manual_response = True
        self.request_status()

    # -----------------------------------------
    # ENVÍO DE COMANDOS
    # -----------------------------------------
    def request_status(self):
        command = json.dumps({"info": "status"})
        ok = self.serial_manager.send_command(command)

        if ok:
            self.view.status_label.setText("Consultando estado...")
        else:
            self.view.status_label.setText("Error enviando status")

    def request_all_params(self):
        command = json.dumps({"info": "all-params"})
        ok = self.serial_manager.send_command(command)

        if ok:
            self.view.status_label.setText("Solicitando parámetros...")
        else:
            self.view.status_label.setText("Error enviando parámetros")

    def send_distance(self, distance_mm):
        command = json.dumps({"distance": int(distance_mm)})
        return self.serial_manager.send_command(command)

    def send_force(self, force_g):
        command = json.dumps({"force": int(force_g)})
        return self.serial_manager.send_command(command)

    def send_start_command(self):
        command = json.dumps({"cmd": "start"})
        return self.serial_manager.send_command(command)

    # -----------------------------------------
    # RECEPCIÓN
    # -----------------------------------------
    def handle_serial_data(self, line):
        line = line.strip()
        if not line:
            return

        print(f"Recibido: {line}")

        # vamos acumulando todo como stream
        self._json_buffer.append(line)
        self._try_parse_json_buffer()


    def _try_parse_json_buffer(self):
        raw = "".join(self._json_buffer)

        objects = []
        current = []
        depth = 0
        in_json = False

        for ch in raw:
            if ch == "{":
                depth += 1
                in_json = True

            if in_json:
                current.append(ch)

            if ch == "}":
                depth -= 1

                if in_json and depth == 0:
                    obj_text = "".join(current).strip()
                    if obj_text:
                        objects.append(obj_text)
                    current = []
                    in_json = False

        # si quedó algo incompleto, lo preservamos
        remainder = "".join(current).strip()
        self._json_buffer = [remainder] if remainder else []

        for obj_text in objects:
            try:
                data = json.loads(obj_text)
            except json.JSONDecodeError:
                print(f"[JSON] Error parseando: {obj_text}")
                continue

            self.process_json_data(data)

    # -----------------------------------------
    # PROCESAMIENTO JSON
    # -----------------------------------------
    def process_json_data(self, data):
        print(f"[JSON] process_json_data -> {data}")

        info = data.get("info")

        if info == "status":
            print("[JSON] Detectado info=status")
            self.process_status_response(data)
            return

        if info == "all-params":
            print("[JSON] Detectado info=all-params")
            self.process_all_params_response(data)
            return

        if "st_test" in data:
            print(f"[JSON] Detectado st_test suelto -> {data.get('st_test')}")

            try:
                st_test = int(data.get("st_test", 0))
            except:
                st_test = 0

            self.update_status_indicator(st_test)

            if st_test == 0:
                self.view.status_label.setText("Ensayo finalizado")

                if not self._waiting_manual_response and not self._auto_refresh_done:
                    print("[FLOW] Auto refresh por fin de ensayo")
                    self._auto_refresh_done = True
                    self.request_status()
            else:
                self.view.status_label.setText(f"Ensayo activo ({st_test})")

            return

        if data.get("result") == "ok":
            print("[JSON] Detectado result=ok")
            self.view.status_label.setText("Comando OK")
            return

        if data.get("result") == "ack":
            print("[JSON] Detectado result=ack")

            if data.get("cmd") == "start":
                self.update_status_indicator(1)
                self.view.status_label.setText("Ensayo iniciado")
            else:
                self.view.status_label.setText("Comando ACK")

            return

        print("[JSON] Mensaje no manejado")

    def process_status_response(self, data):
        print(f"[FLOW] process_status_response entrada -> {data}")

        status = data.get("status", 0)

        try:
            status = int(status)
            if status != 0:
                self._waiting_manual_response = False
        except (TypeError, ValueError):
            print("[FLOW] status inválido")
            self.view.status_label.setText("Estado inválido")
            self._pending_start = False
            return

        print(f"[FLOW] status parseado = {status}, pending_start = {self._pending_start}")

        self.update_status_indicator(status)

        if self._pending_start:
            if status == 0:
                print("[FLOW] pending_start=True y status=0 -> start_sequence()")
                self._pending_start = False
                self.start_sequence()
            else:
                print("[FLOW] pending_start=True pero status!=0 -> ensayo ya activo")
                self._pending_start = False
                self.view.status_label.setText(f"Ensayo activo (status={status})")
            return

        if status == 0:
            print("[FLOW] Refresh normal y status=0 -> request_all_params()")
            self.view.status_label.setText("Ensayo apagado, leyendo parámetros...")
            self.request_all_params()
        else:
            print("[FLOW] Refresh normal y status!=0 -> no pide parámetros")
            self.view.status_label.setText(f"Ensayo activo (status={status})")

    def process_all_params_response(self, data):
        print(f"[FLOW] process_all_params_response -> {data}")

        self.update_measurements(data)
        self.update_inputs(data)

        print("[FLOW] UI actualizada con all-params")
        self._waiting_manual_response = False
        self.view.status_label.setText("Parámetros actualizados")

    # -----------------------------------------
    # SECUENCIA DE INICIO
    # -----------------------------------------
    def start_sequence(self):
        distance_text = self.view.distance_input.text().strip()
        force_text = self.view.load_combo.currentText().strip()

        try:
            distance_mm = int(distance_text)
        except ValueError:
            self.view.status_label.setText("Distancia inválida")
            return

        try:
            force_g = int(force_text)
        except ValueError:
            self.view.status_label.setText("Carga inválida")
            return

        print(f"[FLOW] start_sequence -> distance={distance_mm} mm, force={force_g} g")

        ok_distance = self.send_distance(distance_mm)
        ok_force = self.send_force(force_g)
        ok_start = self.send_start_command()

        if ok_distance and ok_force and ok_start:
            self.view.status_label.setText("Comando de inicio enviado")
        else:
            self.view.status_label.setText("Error iniciando ensayo")

    # -----------------------------------------
    # UI
    # -----------------------------------------
    def update_status_indicator(self, status):
        if status == 0:
            self.view.card_status.set_value("Apagado")
        else:
            self.view.card_status.set_value(f"Encendido ({status})")

    def update_measurements(self, data):
        reaction_one = self._to_float(data.get("reaction_one", 0))
        reaction_two = self._to_float(data.get("reaction_two", 0))
        flexion = self._to_float(data.get("flexion", 0))

        self.view.card_r1.set_value(f"{reaction_one:.1f}")
        self.view.card_r1.set_gauge_value(reaction_one)

        self.view.card_r2.set_value(f"{reaction_two:.1f}")
        self.view.card_r2.set_gauge_value(reaction_two)

        if getattr(self.view, "card_flex", None) is not None:
            self.view.card_flex.set_value(f"{flexion:.2f}")
            self.view.card_flex.set_gauge_value(flexion)

    def update_inputs(self, data):
        distance = data.get("distance")
        force = data.get("force")

        if distance is not None:
            self.view.distance_input.setText(str(distance))

        if force is not None:
            force_text = str(force)
            idx = self.view.load_combo.findText(force_text)
            if idx >= 0:
                self.view.load_combo.setCurrentIndex(idx)
            else:
                self.view.load_combo.addItem(force_text)
                self.view.load_combo.setCurrentText(force_text)

    def reset_outputs(self):
        self.view.card_r1.set_value("0.0")
        self.view.card_r1.set_gauge_value(0)

        self.view.card_r2.set_value("0.0")
        self.view.card_r2.set_gauge_value(0)

        if getattr(self.view, "card_flex", None) is not None:
            self.view.card_flex.set_value("0.0")
            self.view.card_flex.set_gauge_value(0)

    def _to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def update_ui_state(self):
        conectado = self.serial_manager.is_connected()

        self.view.btn_conectar.setEnabled(not conectado)
        self.view.btn_desconectar.setEnabled(conectado)
        self.view.puerto_combo.setEnabled(not conectado)
        self.view.btn_actualizar.setEnabled(not conectado)
        self.view.btn_refrescar.setEnabled(True)
        self.view.btn_iniciar.setEnabled(True)