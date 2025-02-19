import time
import psutil
import pygetwindow as gw
import pydirectinput
import keyboard
import random
import threading
import os
import customtkinter as ctk

# Configurar tema
ctk.set_appearance_mode("Dark")  # Opciones: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")

ROBLOX_PROCESS = "RobloxPlayerBeta.exe"
paused = False
running = False
log_file = "roblox_bot_log.txt"
messages = []

def is_roblox_running():
    return any(process.info['name'] == ROBLOX_PROCESS for process in psutil.process_iter(['name']))

def is_roblox_active():
    active_window = gw.getActiveWindow()
    return active_window and active_window.title and "Roblox" in active_window.title

def toggle_pause():
    global paused
    paused = not paused
    update_status("PAUSADO" if paused else "EJECUTANDO", "orange" if paused else "green")
    log(f"Script {'PAUSADO' if paused else 'REANUDADO'}.")

def write_text(text):
    keyboard.write(text, delay=0.05)

def send_message(text):
    pydirectinput.press('/')
    time.sleep(0.5)
    write_text(text)
    pydirectinput.press('enter')
    time.sleep(1)

def log(message):
    log_box.insert("end", message + '\n')
    log_box.yview("end")
    with open(log_file, "a") as f:
        f.write(message + "\n")

def load_messages():
    global messages
    if os.path.exists("messages.txt"):
        with open("messages.txt", "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
    else:
        with open("messages.txt", "w", encoding="utf-8") as f:
            default_messages = [
                "Hola, me pueden donar?",
                "Serían tan amables de donar?",
                "Gracias por su apoyo!",
                "/e hello",
                "/e point2",
                "Tu ayuda hace la diferencia!",
                "Dona si te gusta mi stand!",
                "Toda contribución es bienvenida!",
                "Apoya el contenido con tu donación!",
                "Que tengas un gran día!",
                "Juntos hacemos la comunidad mejor!",
                "Agradezco cualquier donación!",
                "Si te sobra algo, considera donarme!",
                "Ayúdame a alcanzar mi meta!",
                "Gracias por estar aquí!"
            ]
            f.write("\n".join(default_messages))
            messages = default_messages
    log("Mensajes cargados desde archivo.")

def start_script():
    global running, paused
    if running:
        return
    running = True
    paused = False
    threading.Thread(target=main_loop, daemon=True).start()
    threading.Thread(target=anti_afk, daemon=True).start()
    update_status("EJECUTANDO", "green")
    log("Script iniciado.")

def stop_script():
    global running
    running = False
    update_status("DETENIDO", "red")
    log("Script detenido.")

def anti_afk():
    while running:
        if not paused and is_roblox_running() and is_roblox_active():
            log("Anti-AFK activado: moviendo al personaje.")
            pydirectinput.press('space')
        time.sleep(300)

def main_loop():
    message_interval = int(message_interval_entry.get())
    ad_interval = int(ad_interval_entry.get())
    while running:
        if paused:
            log("Pausado...")
            time.sleep(1)
            continue
        if is_roblox_running():
            if is_roblox_active():
                log("Roblox en primer plano. Enviando mensajes...")
                next_message_time = time.time()
                next_ad_time = time.time() + ad_interval
                while is_roblox_active() and running and not paused:
                    current_time = time.time()
                    if current_time >= next_message_time:
                        message = random.choice(messages)
                        log(f"Enviando: {message}")
                        send_message(message)
                        next_message_time = current_time + message_interval
                    if current_time >= next_ad_time:
                        log("Enviando: Visita mi stand en Pls Donate")
                        send_message("Visita mi stand en Pls Donate")
                        next_ad_time = current_time + ad_interval
                    time.sleep(1)
            else:
                log("Roblox en segundo plano, esperando...")
                time.sleep(1)
        else:
            log("Roblox no está en ejecución. Esperando...")
            time.sleep(5)

def update_status(text, color):
    status_label.configure(text=f"Estado: {text}", text_color=color)

if not os.path.exists(log_file):
    open(log_file, 'w').close()

# Crear ventana principal
root = ctk.CTk()
root.title("Roblox Auto Chat Bot")
root.geometry("450x550")

# Estado
status_label = ctk.CTkLabel(root, text="Estado: DETENIDO", text_color="red", font=("Arial", 14, "bold"))
status_label.pack(pady=5)

# Cuadro de logs
log_box = ctk.CTkTextbox(root, height=200, width=400, wrap="word")
log_box.pack(pady=10)

# Cargar mensajes
load_messages()

# Entradas de configuración
frame_config = ctk.CTkFrame(root)
frame_config.pack(pady=10)

ctk.CTkLabel(frame_config, text="Tiempo entre mensajes (segundos):").grid(row=0, column=0, padx=5, pady=5)
message_interval_entry = ctk.CTkEntry(frame_config, width=50)
message_interval_entry.grid(row=0, column=1, padx=5)
message_interval_entry.insert(0, "60")

ctk.CTkLabel(frame_config, text="Tiempo entre anuncios (segundos):").grid(row=1, column=0, padx=5, pady=5)
ad_interval_entry = ctk.CTkEntry(frame_config, width=50)
ad_interval_entry.grid(row=1, column=1, padx=5)
ad_interval_entry.insert(0, "180")

# Botones
frame_buttons = ctk.CTkFrame(root)
frame_buttons.pack(pady=10)

ctk.CTkButton(frame_buttons, text="Iniciar", command=start_script, fg_color="green").grid(row=0, column=0, padx=5, pady=5)
ctk.CTkButton(frame_buttons, text="Pausar/Reanudar", command=toggle_pause, fg_color="orange").grid(row=0, column=1, padx=5, pady=5)
ctk.CTkButton(frame_buttons, text="Detener", command=stop_script, fg_color="red").grid(row=0, column=2, padx=5, pady=5)

# Modo oscuro/claro
def toggle_mode():
    ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")

ctk.CTkButton(root, text="Modo Claro/Oscuro", command=toggle_mode).pack(pady=10)

# Atajo de teclado
ctk.CTkLabel(root, text="Presiona Shift+P para pausar/reanudar").pack()
keyboard.add_hotkey("shift+p", toggle_pause)

root.mainloop()
