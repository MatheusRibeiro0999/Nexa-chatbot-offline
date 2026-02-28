import customtkinter as ctk
from PIL import Image, ImageTk
import os
import threading
from chat_engine import ChatEngine
import random
import sys

class ChatUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.title("NEXA")
        self.geometry("520x850")
        self.minsize(520, 850)
        self.configure(fg_color="#0E0E10")
        # ================= TOP BAR =================
        self.top_bar = ctk.CTkFrame(
            self,
            height=40,
            fg_color="#111114",
            corner_radius=0
        )
        self.top_bar.pack(fill="x")

        self.top_bar.bind("<Button-1>", self.start_move)
        self.top_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.top_bar.bind("<B1-Motion>", self.do_move)

        self.title_label = ctk.CTkLabel(
            self.top_bar,
            text="  NEXA",
            font=("Arial", 14, "bold"),
            text_color="#3B8ED0"
        )
        self.title_label.pack(side="left", padx=10)

        self.close_button = ctk.CTkButton(
            self.top_bar,
            text="✕",
            width=40,
            height=28,
            fg_color="transparent",
            hover_color="#E74C3C",
            command=self.destroy
        )
        self.close_button.pack(side="right", padx=5, pady=5)
        self.state_speeds = {
            "idle": 300,
            "thinking": 1000,     # mais lento (parece raciocinando)
            "speaking": 100,     # mais rápido (parece falando)
            "listening": 1000,
            "error": 600
        }

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        ctk.set_appearance_mode("dark")

        self.chat_engine = ChatEngine()

        # ================= AVATAR FRAME =================
        # Sombra
        self.avatar_shadow = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#0A0A0C"
        )
        self.avatar_shadow.pack(fill="x", padx=30, pady=(30, 10))
        self.avatar_shadow.configure(height=420)
        self.avatar_shadow.pack_propagate(False)

        # Frame principal
        self.avatar_frame = ctk.CTkFrame(
            self.avatar_shadow,
            corner_radius=25,
            border_width=2,
            border_color="#3B8ED0",
            fg_color="#151518"
        )
        self.avatar_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self.avatar_frame.pack(fill="both", expand=False, padx=20, pady=(20, 10))

        self.avatar_label = ctk.CTkLabel(self.avatar_frame, text="")
        self.avatar_label.pack(expand=True, pady=20)
        
        self.avatar_states = {}
        self.load_all_states()

        self.current_state = "idle"
        self.current_frame_index = 0

        self.animate_avatar()

        # ================= CHAT BOX =================
        self.chat_box = ctk.CTkTextbox(
            self,
            corner_radius=15,
            fg_color="#1A1A1D",
            border_width=1,
            border_color="#2A2A2E",
            wrap="word"
        )
        self.chat_box.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        # tags
        self.chat_box._textbox.tag_configure(
            "user_name",
            foreground="#0E0E10",
            background="#3B8ED0"
        )

        self.chat_box._textbox.tag_configure(
            "bot_name",
            foreground="#0E0E10",
            background="#2ECC71"
        )

        self.chat_box.configure(state="disabled")

        # ================= INPUT AREA =================
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", side="bottom", pady=15)

        self.bottom_frame.configure(height=55)  
        self.bottom_frame.pack_propagate(False)

        self.entry = ctk.CTkEntry(
            self.bottom_frame,
            width=320,
            height=55,  
            corner_radius=10,
            font=("Arial", 16)
        )

        self.entry.pack(side="left", padx=8)
        self.entry.bind("<Return>", self.handle_send)

        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Enviar",
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#3B8ED0",
            hover_color="#1F6AA5",
            command=self.handle_send
        )
        self.send_button.pack(side="left", padx=8)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

   
    # CARREGAR ESTADOS
    def load_all_states(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, "assets")
        else:
            base_path = "assets"

        for state in os.listdir(base_path):
            state_path = os.path.join(base_path, state)

            if os.path.isdir(state_path):
                images = []
                files = sorted(os.listdir(state_path))

                for file in files:
                    if file.endswith(".png"):
                        img_path = os.path.join(state_path, file)
                        image = Image.open(img_path)
                        image = image.resize((380, 380))
                        images.append(ImageTk.PhotoImage(image))

                self.avatar_states[state] = images

    
    # ANIMAÇÃO
    def animate_avatar(self):
        print("Estado atual:", self.current_state)
        frames = self.avatar_states.get(self.current_state, [])

        if not frames:
            self.after(300, self.animate_avatar)
            return

        # 🔥 CASO ESPECIAL: LISTENING (piscada)
        if self.current_state == "listening" and len(frames) >= 2:

            if self.current_frame_index >= len(frames):
                self.current_frame_index = 0

            frame = frames[self.current_frame_index]
            self.avatar_label.configure(image=frame)

            if self.current_frame_index == 0:
                delay = random.randint(2500, 4000)
                self.current_frame_index = 1
            else:
                delay = 300
                self.current_frame_index = 0

            self.after(delay, self.animate_avatar)
            return

        # CASO SPEAKING (randomizado)
        if self.current_state == "speaking" and len(frames) > 1:
          
            self.current_frame_index = random.randint(0, len(frames) - 1)
        else:
            self.current_frame_index = (self.current_frame_index + 1) % len(frames)

        frame = frames[self.current_frame_index]
        self.avatar_label.configure(image=frame)

        speed = self.state_speeds.get(self.current_state, 300)
        self.after(speed, self.animate_avatar)

    def set_state(self, state):
        if state in self.avatar_states:
            self.current_state = state
            self.current_frame_index = 0

            # mudar cor da borda conforme estado
            if state == "thinking":
                self.avatar_frame.configure(border_color="#EAA221")
            elif state == "speaking":
                self.avatar_frame.configure(border_color="#2ECC71")
            elif state == "error":
                self.avatar_frame.configure(border_color="#E74C3C")
            else:
                self.avatar_frame.configure(border_color="#3B8ED0")

    
    # CHAT
    def handle_send(self, event=None):
        user_input = self.entry.get()

        if not user_input.strip():
            return

        self.entry.delete(0, "end")

        self.insert_user_message(user_input)

        threading.Thread(
            target=self.process_message,
            args=(user_input,),
            daemon=True
        ).start()

    def insert_user_message(self, text):
        self.chat_box.configure(state="normal")

        self.chat_box.insert("end", " Você ", "user_name")
        self.chat_box.insert("end", f": {text}\n")

        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def process_message(self, user_input):
        try:
            self.after(0, lambda: self.set_state("thinking"))

            reply = self.chat_engine.ask(user_input)  

            self.after(0, lambda: self.show_reply(reply))

        except Exception as e:
            error_message = str(e)
            self.after(0, lambda: self.show_error(error_message))

    def show_reply(self, reply):
        self.set_state("speaking")

        self.insert_bot_prefix()

        self.type_text(reply, 0)

    def insert_bot_prefix(self):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", " Nexa ", "bot_name")
        self.chat_box.insert("end", ": ")
        self.chat_box.configure(state="disabled")

    def type_text(self, text, index):
        if index < len(text):
            self.chat_box.configure(state="normal")
            self.chat_box.insert("end", text[index])
            self.chat_box.configure(state="disabled")
            self.chat_box.see("end")

            char = text[index]

            if char in ".!?":
                delay = 200
            elif char == ",":
                delay = 100
            else:
                delay = random.randint(15, 40)

            self.after(delay, lambda: self.type_text(text, index + 1))

        else:
            self.chat_box.configure(state="normal")
            self.chat_box.insert("end", "\n\n")
            self.chat_box.configure(state="disabled")
            self.chat_box.see("end")

            self.set_state("listening")

    def show_error(self, error_msg):
        self.set_state("error")
        self.update_chat(f"Erro: {error_msg}\n\n")
        self.after(2000, lambda: self.set_state("idle"))

    def update_chat(self, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", text)
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")