import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import math
import json
import os
import re
import random

# ---------- КЛАСС СОВРЕМЕННОЙ КНОПКИ ----------
class ModernButton(tk.Frame):
    """Современная кнопка с градиентом"""
    def __init__(self, parent, text, command, bg_gradient=("#667eea", "#764ba2"), icon="", width=200, height=45):
        super().__init__(parent, width=width, height=height, cursor="hand2")
        self.command = command
        self.text = text
        self.icon = icon
        self.bg_gradient = bg_gradient
        self.normal_width = width
        self.normal_height = height
        
        self.pack_propagate(False)
        
        # Создаем Canvas для градиента
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Текст на кнопке
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(width//2, height//2, text=display_text,
                                fill="white", font=("Segoe UI", 10, "bold"),
                                anchor="center")
        
        # Привязываем события
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.draw_gradient()
    
    def draw_gradient(self):
        """Рисует градиент на кнопке"""
        width = self.normal_width
        height = self.normal_height
        
        self.canvas.delete("all")
        
        for i in range(height):
            ratio = i / height if height > 0 else 0
            color1 = self.bg_gradient[0]
            color2 = self.bg_gradient[1]
            r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
            g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[3:5], 16) * ratio)
            b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)
        
        # Текст
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(width//2, height//2, text=display_text,
                                fill="white", font=("Segoe UI", 10, "bold"), anchor="center")
    
    def on_enter(self, event):
        self.config(bg=self.bg_gradient[1])
    
    def on_leave(self, event):
        self.config(bg=self.bg_gradient[0])
    
    def on_click(self, event):
        if self.command:
            self.command()


# ---------- КЛАСС КАРТОЧКИ-КНОПКИ ДЛЯ ГЛАВНОГО МЕНЮ ----------
class MenuCard(tk.Frame):
    """Красивая карточка-кнопка для главного меню"""
    def __init__(self, parent, title, icon, command, color, width=240, height=110):
        super().__init__(parent, bg=color, cursor="hand2", relief=tk.FLAT, width=width, height=height)
        self.command = command
        self.normal_bg = color
        self.hover_bg = self._darken_color(color)
        
        self.pack_propagate(False)
        
        # Внутренний фрейм с отступами
        inner = tk.Frame(self, bg=color)
        inner.pack(expand=True, fill=tk.BOTH, padx=12, pady=10)
        
        # Иконка
        icon_label = tk.Label(inner, text=icon, font=("Segoe UI", 32), bg=color, fg="white")
        icon_label.pack(pady=(5, 5))
        
        # Заголовок
        title_label = tk.Label(inner, text=title, font=("Segoe UI", 12, "bold"), 
                               bg=color, fg="white")
        title_label.pack()
        
        # Анимация при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        inner.bind("<Enter>", self.on_enter)
        inner.bind("<Leave>", self.on_leave)
        inner.bind("<Button-1>", self.on_click)
        icon_label.bind("<Enter>", self.on_enter)
        icon_label.bind("<Leave>", self.on_leave)
        icon_label.bind("<Button-1>", self.on_click)
        title_label.bind("<Enter>", self.on_enter)
        title_label.bind("<Leave>", self.on_leave)
        title_label.bind("<Button-1>", self.on_click)
        
    def _darken_color(self, color):
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 40)
            g = max(0, g - 40)
            b = max(0, b - 40)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def on_enter(self, event):
        self.configure(bg=self.hover_bg)
        for child in self.winfo_children():
            child.configure(bg=self.hover_bg)
            for grandchild in child.winfo_children():
                grandchild.configure(bg=self.hover_bg)
    
    def on_leave(self, event):
        self.configure(bg=self.normal_bg)
        for child in self.winfo_children():
            child.configure(bg=self.normal_bg)
            for grandchild in child.winfo_children():
                grandchild.configure(bg=self.normal_bg)
    
    def on_click(self, event):
        if self.command:
            self.command()


class Vehicle:
    RATE_MULTIPLIERS = {
        "Легковой": 1.0,
        "Грузовой": 1.5,
        "Мотоцикл": 0.7,
        "Электромобиль": 0.9
    }
    
    def __init__(self, license_plate: str, vehicle_type: str = "Легковой", owner_name: str = ""):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.owner_name = owner_name
        self.entry_time = None

class ParkingSpot:
    STANDARD_WIDTH = 100
    STANDARD_HEIGHT = 60
    
    def __init__(self, spot_id, x, y, width=None, height=None):
        self.spot_id = spot_id
        self.vehicle = None
        self.is_occupied = False
        self.owner_plate = None
        self.x = x
        self.y = y
        self.w = width if width is not None else self.STANDARD_WIDTH
        self.h = height if height is not None else self.STANDARD_HEIGHT
        self.rect_id = None
        self.label_id = None
        self.car_items = []

    def park(self, vehicle, owner_plate):
        self.vehicle = vehicle
        self.is_occupied = True
        self.owner_plate = owner_plate

    def remove(self):
        self.vehicle = None
        self.is_occupied = False
        self.owner_plate = None

class ParkingLot:
    BASE_HOURLY_RATE = 50

    def __init__(self, name, spot_positions):
        self.name = name
        self.spots = []
        self.history = []
        self.spot_positions = spot_positions
        self._create_spots()
        self._load_global_state()

    def _create_spots(self):
        for i, (x, y, w, h) in enumerate(self.spot_positions):
            spot = ParkingSpot(i+1, x, y, w, h)
            self.spots.append(spot)

    def find_spot(self, spot_id):
        if 1 <= spot_id <= len(self.spots):
            return self.spots[spot_id-1]
        return None

    def get_rate_for_type(self, vehicle_type):
        multiplier = Vehicle.RATE_MULTIPLIERS.get(vehicle_type, 1.0)
        return self.BASE_HOURLY_RATE * multiplier

    def calculate_cost(self, entry_time, exit_time, vehicle_type):
        duration = exit_time - entry_time
        minutes = duration.total_seconds() / 60.0
        hours = math.ceil(minutes / 60.0)
        hourly_rate = self.get_rate_for_type(vehicle_type)
        base_cost = hours * hourly_rate
        return base_cost, hours

    def park(self, spot_id, vehicle, entry_time, owner_plate):
        spot = self.find_spot(spot_id)
        if spot and not spot.is_occupied:
            spot.park(vehicle, owner_plate)
            self.history.append({
                "spot_id": spot_id,
                "license_plate": vehicle.license_plate,
                "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "exit_time": None,
                "cost": None,
                "parking_name": self.name,
                "vehicle_type": vehicle.vehicle_type,
                "owner_name": vehicle.owner_name
            })
            self._save_global_state()
            return True
        return False

    def leave(self, spot_id, exit_time, owner_plate):
        spot = self.find_spot(spot_id)
        if not spot or not spot.is_occupied:
            return None
            
        if spot.owner_plate != owner_plate:
            return None
            
        veh = spot.vehicle
        base_cost, hours = self.calculate_cost(veh.entry_time, exit_time, veh.vehicle_type)
        
        # Ищем запись в истории по spot_id и license_plate
        found = False
        for record in self.history:
            if record["spot_id"] == spot_id and record["exit_time"] is None and record["license_plate"] == veh.license_plate:
                record["exit_time"] = exit_time.strftime("%Y-%m-%d %H:%M:%S")
                record["cost"] = base_cost
                found = True
                break
        
        if not found:
            # Если запись не найдена, создаем новую
            self.history.append({
                "spot_id": spot_id,
                "license_plate": veh.license_plate,
                "entry_time": veh.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "cost": base_cost,
                "parking_name": self.name,
                "vehicle_type": veh.vehicle_type,
                "owner_name": veh.owner_name
            })
        
        # Освобождаем место
        spot.remove()
        
        # Сохраняем состояние после освобождения
        self._save_global_state()
        
        return veh, base_cost, hours

    def get_my_active_parking(self, owner_plate):
        for spot in self.spots:
            if spot.is_occupied and spot.owner_plate == owner_plate:
                return spot
        return None

    def _save_global_state(self):
        filename = "parking_global_state.json"
        global_state = {
            "history": self.history,
            "spots": []
        }
        
        for spot in self.spots:
            if spot.is_occupied and spot.vehicle:
                global_state["spots"].append({
                    "spot_id": spot.spot_id,
                    "license_plate": spot.vehicle.license_plate,
                    "vehicle_type": spot.vehicle.vehicle_type,
                    "owner_name": spot.vehicle.owner_name,
                    "owner_plate": spot.owner_plate,
                    "entry_time": spot.vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S") if spot.vehicle.entry_time else None
                })
        
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    all_data = json.load(f)
                    all_data[self.name] = global_state
            except:
                all_data = {self.name: global_state}
        else:
            all_data = {self.name: global_state}
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

    def _load_global_state(self):
        filename = "parking_global_state.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    all_data = json.load(f)
                    if self.name in all_data:
                        lot_data = all_data[self.name]
                        self.history = lot_data.get("history", [])
                        
                        # Сначала очищаем все места
                        for spot in self.spots:
                            if spot.is_occupied:
                                spot.remove()
                        
                        # Затем загружаем только актуальные парковки
                        for spot_info in lot_data.get("spots", []):
                            spot = self.find_spot(spot_info["spot_id"])
                            if spot and not spot.is_occupied:
                                entry_dt = datetime.strptime(spot_info["entry_time"], "%Y-%m-%d %H:%M:%S") if spot_info["entry_time"] else datetime.now()
                                veh = Vehicle(spot_info["license_plate"], spot_info.get("vehicle_type", "Легковой"), spot_info.get("owner_name", ""))
                                veh.entry_time = entry_dt
                                spot.park(veh, spot_info["owner_plate"])
            except:
                pass


# ---------- ГЛАВНОЕ ПРИЛОЖЕНИЕ ----------
class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моя парковка - Таганрог")
        self.root.configure(bg="#0a0a0f")
        
        self.is_fullscreen = True
        self.root.attributes("-fullscreen", True)
        
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", font=('Segoe UI', 11), rowheight=35, 
                           background="#1a1a2e", fieldbackground="#1a1a2e", 
                           foreground="#ffffff", borderwidth=0)
        self.style.configure("Treeview.Heading", font=('Segoe UI', 12, 'bold'), 
                           background="#16213e", foreground="#f1c40f", 
                           borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#2c3e50')])

        self.client_plate = None
        self.client_name = ""
        
        self.lots = {
            "ул. Петровская": ParkingLot("ул. Петровская", []),
            "ул. Чехова": ParkingLot("ул. Чехова", []),
            "ул. Дзержинского": ParkingLot("ул. Дзержинского", [])
        }
        self.current_lot = None
        self.current_frame = None
        self.last_parking_name = None
        self._return_to_parking = None
        
        self.show_auth_screen()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)

    # ---------- ГЕНЕРАЦИЯ ПАРКОВОК ----------
    def generate_petrovskaya_spots(self, width, height):
        spots = []
        w, h = 130, 75
        spacing = w + 20
        cols = 8
        rows = 4
        total_width = cols * spacing - 20
        start_x = (width - total_width) // 2
        start_y = 120
        row_spacing = h + 40
        
        for row in range(rows):
            y = start_y + row * row_spacing
            for i in range(cols):
                x = start_x + i * spacing
                spots.append((x, y, w, h))
        return spots

    def generate_chekhova_spots(self, width, height):
        spots = []
        w, h = 130, 75
        spacing = w + 20
        cols = 7
        rows = 5
        total_width = cols * spacing - 20
        start_x = (width - total_width) // 2
        start_y = 120
        row_spacing = h + 40
        
        for row in range(rows):
            y = start_y + row * row_spacing
            for i in range(cols):
                x = start_x + i * spacing
                spots.append((x, y, w, h))
        return spots

    def generate_dzerzhinskogo_spots(self, width, height):
        spots = []
        w, h = 130, 75
        spacing = w + 20
        cols = 6
        rows = 6
        total_width = cols * spacing - 20
        start_x = (width - total_width) // 2
        start_y = 120
        row_spacing = h + 40
        
        for row in range(rows):
            y = start_y + row * row_spacing
            for i in range(cols):
                x = start_x + i * spacing
                spots.append((x, y, w, h))
        return spots

    # ---------- АВТОРИЗАЦИЯ ----------
    def show_auth_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(self.current_frame, bg="#0a0a0f", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(30, 10), pady=30)
        left_panel.pack_propagate(False)
        
        left_content = tk.Frame(left_panel, bg="#0a0a0f")
        left_content.pack(fill=tk.BOTH, expand=True)
        
        advantages_title = tk.Label(left_content, text="✨ ПРЕИМУЩЕСТВА", 
                                    font=("Segoe UI", 14, "bold"),
                                    bg="#0a0a0f", fg="#f1c40f")
        advantages_title.pack(anchor=tk.W, pady=(0, 15))
        
        advantages = [
            ("🅿️", "40+ парковочных мест", "Удобное расположение в центре"),
            ("📱", "Умная система бронирования", "Бронируйте место заранее"),
            ("🔒", "Круглосуточная охрана", "Видеонаблюдение 24/7"),
            ("⚡", "Зарядки для электромобилей", "Бесплатная зарядка"),
            ("🔄", "Гибкая тарификация", "Экономия до 30%"),
            ("⭐", "Бонусная программа", "Каждая 10-я парковка бесплатно")
        ]
        
        for icon, title, desc in advantages:
            adv_card = tk.Frame(left_content, bg="#1a1a2e", padx=12, pady=8, relief=tk.FLAT)
            adv_card.pack(fill=tk.X, pady=5)
            
            icon_label = tk.Label(adv_card, text=icon, font=("Segoe UI", 18), 
                                  bg="#1a1a2e", fg="#f1c40f")
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
            
            text_frame = tk.Frame(adv_card, bg="#1a1a2e")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            title_label = tk.Label(text_frame, text=title, font=("Segoe UI", 11, "bold"),
                                   bg="#1a1a2e", fg="white")
            title_label.pack(anchor=tk.W)
            
            desc_label = tk.Label(text_frame, text=desc, font=("Segoe UI", 9),
                                  bg="#1a1a2e", fg="#7f8c8d")
            desc_label.pack(anchor=tk.W)
        
        right_panel = tk.Frame(self.current_frame, bg="#0a0a0f", width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 30), pady=30)
        right_panel.pack_propagate(False)
        
        right_content = tk.Frame(right_panel, bg="#0a0a0f")
        right_content.pack(fill=tk.BOTH, expand=True)
        
        weather_frame = tk.Frame(right_content, bg="#1a1a2e", padx=15, pady=12)
        weather_frame.pack(fill=tk.X, pady=(0, 15))
        
        weather_title = tk.Label(weather_frame, text="🌤 ПОГОДА", font=("Segoe UI", 11, "bold"),
                                 bg="#1a1a2e", fg="#f1c40f")
        weather_title.pack(anchor=tk.W, pady=(0, 8))
        
        weather_info = tk.Frame(weather_frame, bg="#1a1a2e")
        weather_info.pack(fill=tk.X)
        
        weather_icon = tk.Label(weather_info, text="☀️", font=("Segoe UI", 32),
                                bg="#1a1a2e", fg="#f39c12")
        weather_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        weather_text_frame = tk.Frame(weather_info, bg="#1a1a2e")
        weather_text_frame.pack(side=tk.LEFT)
        
        tk.Label(weather_text_frame, text="+18°C", font=("Segoe UI", 18, "bold"),
                bg="#1a1a2e", fg="white").pack(anchor=tk.W)
        tk.Label(weather_text_frame, text="Ясно", font=("Segoe UI", 10),
                bg="#1a1a2e", fg="#7f8c8d").pack(anchor=tk.W)
        
        news_frame = tk.Frame(right_content, bg="#1a1a2e", padx=15, pady=12)
        news_frame.pack(fill=tk.X, pady=(0, 15))
        
        news_title = tk.Label(news_frame, text="🎉 АКЦИИ", font=("Segoe UI", 11, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        news_title.pack(anchor=tk.W, pady=(0, 8))
        
        news_items = [
            ("🔥 Скидка 20%", "На выходные"),
            ("⭐ Накопительная", "10-я парковка бесплатно"),
            ("🎓 Студентам", "Скидка 15%")
        ]
        
        for title, desc in news_items:
            news_card = tk.Frame(news_frame, bg="#2d2d3d", padx=10, pady=6)
            news_card.pack(fill=tk.X, pady=4)
            tk.Label(news_card, text=title, font=("Segoe UI", 11, "bold"),
                    bg="#2d2d3d", fg="#f1c40f").pack(anchor=tk.W)
            tk.Label(news_card, text=desc, font=("Segoe UI", 9),
                    bg="#2d2d3d", fg="#bdc3c7").pack(anchor=tk.W)
        
        howto_frame = tk.Frame(right_content, bg="#1a1a2e", padx=15, pady=12)
        howto_frame.pack(fill=tk.X)
        
        howto_title = tk.Label(howto_frame, text="📌 КАК ЭТО РАБОТАЕТ", font=("Segoe UI", 11, "bold"),
                               bg="#1a1a2e", fg="#f1c40f")
        howto_title.pack(anchor=tk.W, pady=(0, 8))
        
        steps = [
            ("1", "Введите номер авто", "🔹"),
            ("2", "Выберите парковку", "🔹"),
            ("3", "Нажмите на место", "🔹"),
            ("4", "Оплатите при выезде", "🔹")
        ]
        
        for num, text, bullet in steps:
            step_frame = tk.Frame(howto_frame, bg="#1a1a2e")
            step_frame.pack(anchor=tk.W, pady=3)
            tk.Label(step_frame, text=bullet, font=("Segoe UI", 11),
                    bg="#1a1a2e", fg="#f1c40f").pack(side=tk.LEFT)
            tk.Label(step_frame, text=f" {num}. {text}", font=("Segoe UI", 10),
                    bg="#1a1a2e", fg="#bdc3c7").pack(side=tk.LEFT)
        
        center_container = tk.Frame(self.current_frame, bg="#0a0a0f")
        center_container.pack(expand=True, fill=tk.BOTH)
        
        card_container = tk.Frame(center_container, bg="#0a0a0f")
        card_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        card = tk.Frame(card_container, bg="#1a1a2e", padx=60, pady=50, relief=tk.FLAT,
                       highlightbackground="#f1c40f", highlightthickness=3)
        card.pack()
        
        neon_frame = tk.Frame(card, bg="#f1c40f", height=4)
        neon_frame.pack(fill=tk.X, padx=0, pady=(0, 20))
        
        logo_label = tk.Label(card, text="🅿️", font=("Segoe UI", 56), 
                             bg="#1a1a2e", fg="#f1c40f")
        logo_label.pack(pady=(20, 5))
        
        title_label = tk.Label(card, text="МОЯ ПАРКОВКА", font=("Segoe UI", 26, "bold"), 
                              bg="#1a1a2e", fg="white")
        title_label.pack()
        
        subtitle_label = tk.Label(card, text="Таганрог • 2026", font=("Segoe UI", 12), 
                                 bg="#1a1a2e", fg="#7f8c8d")
        subtitle_label.pack(pady=(5, 20))
        
        name_label = tk.Label(card, text="Ваше имя", font=("Segoe UI", 12),
                             bg="#1a1a2e", fg="#bdc3c7")
        name_label.pack(anchor=tk.W, pady=(0, 5))
        
        name_entry_frame = tk.Frame(card, bg="#0d0d1a")
        name_entry_frame.pack(pady=(0, 15), fill=tk.X)
        
        self.name_entry = tk.Entry(name_entry_frame, width=30, font=("Segoe UI", 14),
                                  bg="#0d0d1a", fg="white", insertbackground="white",
                                  relief=tk.FLAT, bd=0)
        self.name_entry.pack(side=tk.LEFT, padx=(10, 0), ipady=8, expand=True, fill=tk.X)
        self.name_entry.insert(0, "Алексей")
        
        plate_label = tk.Label(card, text="Госномер автомобиля", font=("Segoe UI", 12),
                              bg="#1a1a2e", fg="#bdc3c7")
        plate_label.pack(anchor=tk.W, pady=(0, 5))
        
        plate_entry_frame = tk.Frame(card, bg="#0d0d1a")
        plate_entry_frame.pack(pady=(0, 8), fill=tk.X)
        
        self.plate_entry = tk.Entry(plate_entry_frame, width=30, font=("Segoe UI", 14),
                                   bg="#0d0d1a", fg="white", insertbackground="white",
                                   relief=tk.FLAT, bd=0)
        self.plate_entry.pack(side=tk.LEFT, padx=(10, 0), ipady=8, expand=True, fill=tk.X)
        self.plate_entry.insert(0, "А123ВС161")
        
        example_label = tk.Label(card, text="Пример: А123ВС 161", font=("Segoe UI", 9),
                                bg="#1a1a2e", fg="#7f8c8d")
        example_label.pack(pady=(0, 15))
        
        self.auth_error = tk.Label(card, text="", font=("Segoe UI", 10), 
                                   fg="#e74c3c", bg="#1a1a2e")
        self.auth_error.pack()
        
        btn_frame = tk.Frame(card, bg="#1a1a2e")
        btn_frame.pack(pady=(15, 0))
        
        def on_login():
            name = self.name_entry.get().strip()
            plate = self.plate_entry.get().strip()
            
            if not name:
                self.auth_error.config(text="❌ Введите ваше имя")
                return
            
            is_valid, formatted_plate, _ = self.validate_license_plate(plate)
            if not is_valid:
                self.auth_error.config(text="❌ Неверный формат госномера")
                return
            
            self.client_name = name
            self.client_plate = formatted_plate
            self.show_main_menu()
        
        login_btn = ModernButton(btn_frame, "ВОЙТИ", on_login, 
                                bg_gradient=("#27ae60", "#2ecc71"), icon="→", width=200, height=45)
        login_btn.pack(side=tk.LEFT, padx=8, pady=5)
        
        exit_btn = ModernButton(btn_frame, "ВЫХОД", self.root.quit,
                               bg_gradient=("#e74c3c", "#c0392b"), icon="✕", width=200, height=45)
        exit_btn.pack(side=tk.LEFT, padx=8, pady=5)

    def validate_license_plate(self, plate):
        plate = plate.strip().upper()
        clean_plate = re.sub(r'[\s\-]', '', plate)
        pattern = r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}(\d{2,3})$'
        match = re.match(pattern, clean_plate)
        if match:
            region_code = match.group(1)
            if self.is_valid_region(region_code):
                formatted = f"{clean_plate[:4]} {clean_plate[4:6]} {region_code}"
                return True, formatted, region_code
        return False, plate, None
    
    def is_valid_region(self, region_code):
        valid_regions = set(str(i).zfill(2) for i in range(1, 100))
        valid_regions.update(['102', '113', '116', '118', '121', '122', '123', '124', '125', '126',
                              '127', '128', '129', '130', '131', '132', '133', '134', '135', '136',
                              '137', '138', '139', '142', '147', '150', '152', '154', '156', '159',
                              '161', '163', '164', '165', '169', '173', '174', '177', '178', '186',
                              '190', '192', '193', '196', '197', '199', '702', '716', '725', '750',
                              '761', '763', '774', '777', '790', '797', '799'])
        return region_code in valid_regions

    # ---------- ГЛАВНОЕ МЕНЮ ----------
    def show_main_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_lot = None
        self.last_parking_name = None
        self._return_to_parking = None
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=85)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        logo_frame = tk.Frame(top_panel, bg="#1a1a2e")
        logo_frame.pack(side=tk.LEFT, padx=30, pady=15)
        
        logo_icon = tk.Label(logo_frame, text="🅿️", font=("Segoe UI", 34), 
                            bg="#1a1a2e", fg="#f1c40f")
        logo_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        logo_text = tk.Label(logo_frame, text="МОЯ ПАРКОВКА", font=("Segoe UI", 22, "bold"),
                            bg="#1a1a2e", fg="white")
        logo_text.pack(side=tk.LEFT)
        
        profile_frame = tk.Frame(top_panel, bg="#1a1a2e")
        profile_frame.pack(side=tk.RIGHT, padx=30, pady=15)
        
        avatar_frame = tk.Frame(profile_frame, bg="#2d2d3d", width=50, height=50, relief=tk.FLAT)
        avatar_frame.pack(side=tk.LEFT, padx=5)
        avatar_frame.pack_propagate(False)
        avatar_label = tk.Label(avatar_frame, text="👤", font=("Segoe UI", 22), 
                               bg="#2d2d3d", fg="#f1c40f")
        avatar_label.pack(expand=True)
        
        user_info = tk.Frame(profile_frame, bg="#1a1a2e")
        user_info.pack(side=tk.LEFT, padx=10)
        
        user_name = tk.Label(user_info, text=self.client_name, font=("Segoe UI", 14, "bold"),
                            bg="#1a1a2e", fg="#f1c40f")
        user_name.pack(anchor=tk.W)
        
        car_plate = tk.Label(user_info, text=self.client_plate, font=("Segoe UI", 11),
                            bg="#1a1a2e", fg="#bdc3c7")
        car_plate.pack(anchor=tk.W)
        
        switch_btn = tk.Button(profile_frame, text="Сменить", command=self.show_auth_screen,
                               bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                               padx=15, pady=6, bd=0, cursor="hand2", relief=tk.FLAT)
        switch_btn.pack(side=tk.LEFT, padx=10)
        
        left_panel = tk.Frame(self.current_frame, bg="#0a0a0f", width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)
        left_panel.pack_propagate(False)
        
        left_content = tk.Frame(left_panel, bg="#0a0a0f")
        left_content.pack(fill=tk.BOTH, expand=True)
        
        left_title = tk.Label(left_content, text="📊 МОЯ СТАТИСТИКА", font=("Segoe UI", 13, "bold"),
                              bg="#0a0a0f", fg="#f1c40f")
        left_title.pack(anchor=tk.W, pady=(0, 12))
        
        total_parking_count = 0
        total_spent = 0
        for lot in self.lots.values():
            for rec in lot.history:
                if rec.get("license_plate") == self.client_plate and rec.get("exit_time"):
                    total_parking_count += 1
                    total_spent += rec.get("cost", 0)
        
        my_active = None
        for name, lot in self.lots.items():
            spot = lot.get_my_active_parking(self.client_plate)
            if spot:
                my_active = spot
                break
        
        stats_card = tk.Frame(left_content, bg="#1a1a2e", padx=15, pady=12, relief=tk.FLAT)
        stats_card.pack(fill=tk.X, pady=6)
        
        stat_items = [
            ("🚗 Всего парковок:", f"{total_parking_count}"),
            ("💰 Всего потрачено:", f"{total_spent:.0f} ₽"),
            ("🎫 Активных парковок:", "1" if my_active else "0")
        ]
        
        for label, value in stat_items:
            stat_row = tk.Frame(stats_card, bg="#1a1a2e")
            stat_row.pack(fill=tk.X, pady=3)
            tk.Label(stat_row, text=label, font=("Segoe UI", 10), bg="#1a1a2e", fg="#bdc3c7").pack(side=tk.LEFT)
            tk.Label(stat_row, text=value, font=("Segoe UI", 10, "bold"), bg="#1a1a2e", fg="#f1c40f").pack(side=tk.RIGHT)
        
        level = min(total_parking_count // 5 + 1, 10)
        level_name = ["Новичок", "Любитель", "Знаток", "Эксперт", "Профи", 
                      "Мастер", "Гранд", "Легенда", "Титан", "БОГ"][level-1]
        
        level_frame = tk.Frame(left_content, bg="#1a1a2e", padx=15, pady=10)
        level_frame.pack(fill=tk.X, pady=6)
        
        tk.Label(level_frame, text="🏆 УРОВЕНЬ", font=("Segoe UI", 10, "bold"),
                bg="#1a1a2e", fg="#f1c40f").pack(anchor=tk.W)
        tk.Label(level_frame, text=f"{level_name} ({level}/10)", font=("Segoe UI", 11, "bold"),
                bg="#1a1a2e", fg="white").pack(anchor=tk.W, pady=(3, 0))
        
        discount = min(level * 2, 30)
        discount_frame = tk.Frame(left_content, bg="#1a1a2e", padx=15, pady=10)
        discount_frame.pack(fill=tk.X, pady=6)
        
        tk.Label(discount_frame, text="🎁 ВАША СКИДКА", font=("Segoe UI", 10, "bold"),
                bg="#1a1a2e", fg="#f1c40f").pack(anchor=tk.W)
        tk.Label(discount_frame, text=f"{discount}%", font=("Segoe UI", 20, "bold"),
                bg="#1a1a2e", fg="#2ecc71").pack(anchor=tk.W)
        
        right_panel = tk.Frame(self.current_frame, bg="#0a0a0f", width=280)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 20), pady=20)
        right_panel.pack_propagate(False)
        
        right_content = tk.Frame(right_panel, bg="#0a0a0f")
        right_content.pack(fill=tk.BOTH, expand=True)
        
        time_frame = tk.Frame(right_content, bg="#1a1a2e", padx=15, pady=12)
        time_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(time_frame, text="🕐 ТЕКУЩЕЕ ВРЕМЯ", font=("Segoe UI", 10, "bold"),
                bg="#1a1a2e", fg="#f1c40f").pack(anchor=tk.W)
        
        self.main_clock_label = tk.Label(time_frame, font=("Segoe UI", 20, "bold"),
                                         bg="#1a1a2e", fg="white")
        self.main_clock_label.pack(anchor=tk.W, pady=5)
        self._update_main_clock()
        
        tk.Label(time_frame, text=datetime.now().strftime("%d.%m.%Y"), font=("Segoe UI", 11),
                bg="#1a1a2e", fg="#7f8c8d").pack(anchor=tk.W)
        
        tip_frame = tk.Frame(right_content, bg="#1a1a2e", padx=15, pady=12)
        tip_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(tip_frame, text="💡 СОВЕТ", font=("Segoe UI", 10, "bold"),
                bg="#1a1a2e", fg="#f1c40f").pack(anchor=tk.W)
        
        tips = ["Чем чаще паркуетесь, тем выше скидка!", "В выходные скидка 20%", "Электромобили получают скидку 10%"]
        tk.Label(tip_frame, text=random.choice(tips), font=("Segoe UI", 10),
                bg="#1a1a2e", fg="#bdc3c7", wraplength=240, justify=tk.LEFT).pack(anchor=tk.W, pady=5)
        
        main_container = tk.Frame(self.current_frame, bg="#0a0a0f")
        main_container.pack(expand=True, fill=tk.BOTH)
        
        center_frame = tk.Frame(main_container, bg="#0a0a0f")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        active_spots = []
        for lot_name, lot in self.lots.items():
            spot = lot.get_my_active_parking(self.client_plate)
            if spot:
                active_spots.append((lot_name, spot))
        
        if active_spots:
            status_card = tk.Frame(center_frame, bg="#1a1a2e", relief=tk.FLAT,
                                   highlightbackground="#2ecc71", highlightthickness=2)
            status_card.pack(fill=tk.X, pady=(0, 25))
            
            status_text = f"🚗 Ваш автомобиль припаркован на {active_spots[0][0]}, место №{active_spots[0][1].spot_id}"
            status_label = tk.Label(status_card, text=status_text, font=("Segoe UI", 12, "bold"),
                                   bg="#1a1a2e", fg="#2ecc71", padx=25, pady=10)
            status_label.pack()
        
        welcome_label = tk.Label(center_frame, text=f"Добро пожаловать, {self.client_name}!", 
                                font=("Segoe UI", 22, "bold"), bg="#0a0a0f", fg="white")
        welcome_label.pack(pady=(0, 8))
        
        subtitle_label = tk.Label(center_frame, text="Выберите действие", 
                                 font=("Segoe UI", 13), bg="#0a0a0f", fg="#7f8c8d")
        subtitle_label.pack(pady=(0, 30))
        
        cards = [
            ("ПРИПАРКОВАТЬ", "🚗", self.show_parking_choice, "#27ae60"),
            ("ОСВОБОДИТЬ", "🚙", self.show_leave_choice, "#e67e22"),
            ("ГДЕ МАШИНА?", "📍", self.show_my_cars, "#9b59b6"),
            ("ИСТОРИЯ", "📋", self.show_history, "#3498db"),
            ("ТАРИФЫ", "💰", self.show_tariffs, "#f39c12"),
            ("ВЫХОД", "❌", self.root.quit, "#e74c3c")
        ]
        
        for row_idx in range(2):
            row_frame = tk.Frame(center_frame, bg="#0a0a0f")
            row_frame.pack(pady=6)
            for col_idx in range(3):
                card_idx = row_idx * 3 + col_idx
                if card_idx < len(cards):
                    title, icon, command, color = cards[card_idx]
                    card = MenuCard(row_frame, title, icon, command, color, width=240, height=110)
                    card.pack(side=tk.LEFT, padx=10)
        
        info_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=80)
        info_panel.pack(fill=tk.X, side=tk.BOTTOM)
        info_panel.pack_propagate(False)
        
        info_content = tk.Frame(info_panel, bg="#1a1a2e")
        info_content.pack(expand=True, padx=25, pady=10)
        
        for name, lot in self.lots.items():
            occupied = sum(1 for spot in lot.spots if spot.is_occupied)
            total = len(lot.spots) if lot.spots else 40
            free = total - occupied
            my_spot = lot.get_my_active_parking(self.client_plate)
            my_text = f" | ⭐ Ваше: {my_spot.spot_id}" if my_spot else ""
            
            lot_frame = tk.Frame(info_content, bg="#2d2d3d", padx=12, pady=6, relief=tk.FLAT,
                                highlightbackground="#f1c40f", highlightthickness=1)
            lot_frame.pack(side=tk.LEFT, padx=8, expand=True, fill=tk.X)
            
            tk.Label(lot_frame, text=name, font=("Segoe UI", 10, "bold"),
                    bg="#2d2d3d", fg="#f1c40f").pack(anchor=tk.W)
            
            status_text = f"🟢 {free}  🔴 {occupied}{my_text}"
            tk.Label(lot_frame, text=status_text, font=("Segoe UI", 9),
                    bg="#2d2d3d", fg="#bdc3c7").pack(anchor=tk.W)
        
        footer = tk.Frame(self.current_frame, bg="#0a0a0f", height=28)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        tk.Label(footer, text="F11 - выключить полный экран | Esc - выход", 
                font=("Segoe UI", 8), bg="#0a0a0f", fg="#555").pack(pady=5)

    def _update_main_clock(self):
        try:
            if hasattr(self, 'main_clock_label') and self.main_clock_label.winfo_exists():
                self.main_clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
                self.root.after(1000, self._update_main_clock)
        except:
            pass

    # ---------- ВЫБОР ПАРКОВКИ ----------
    def show_parking_choice(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="🚗", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_text = tk.Label(title_frame, text="ВЫБОР ПАРКОВКИ", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_text.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        if hasattr(self, '_return_to_parking') and self._return_to_parking:
            back_cmd = self._return_to_parking_scheme
        else:
            back_cmd = self.show_main_menu
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", back_cmd,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=110, height=35)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        main_container = tk.Frame(self.current_frame, bg="#0a0a0f")
        main_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        cards_frame = tk.Frame(main_container, bg="#0a0a0f")
        cards_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_info = tk.Frame(main_container, bg="#0a0a0f", width=280)
        right_info.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        right_info.pack_propagate(False)
        
        info_card = tk.Frame(right_info, bg="#1a1a2e", padx=15, pady=15, relief=tk.FLAT,
                            highlightbackground="#f1c40f", highlightthickness=1)
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_card, text="ℹ️ ИНФОРМАЦИЯ", font=("Segoe UI", 11, "bold"),
                bg="#1a1a2e", fg="#f1c40f").pack(anchor=tk.W, pady=(0, 10))
        
        tk.Label(info_card, text="🕐 Время работы:", font=("Segoe UI", 9, "bold"),
                bg="#1a1a2e", fg="white").pack(anchor=tk.W)
        tk.Label(info_card, text="Круглосуточно", font=("Segoe UI", 9),
                bg="#1a1a2e", fg="#bdc3c7").pack(anchor=tk.W, pady=(0, 8))
        
        tk.Label(info_card, text="💰 Оплата:", font=("Segoe UI", 9, "bold"),
                bg="#1a1a2e", fg="white").pack(anchor=tk.W)
        tk.Label(info_card, text="Наличные, карта, онлайн", font=("Segoe UI", 9),
                bg="#1a1a2e", fg="#bdc3c7").pack(anchor=tk.W, pady=(0, 8))
        
        tk.Label(info_card, text="🔒 Безопасность:", font=("Segoe UI", 9, "bold"),
                bg="#1a1a2e", fg="white").pack(anchor=tk.W)
        tk.Label(info_card, text="Видеонаблюдение 24/7", font=("Segoe UI", 9),
                bg="#1a1a2e", fg="#bdc3c7").pack(anchor=tk.W)
        
        tips_card = tk.Frame(right_info, bg="#1a1a2e", padx=15, pady=12, relief=tk.FLAT,
                            highlightbackground="#2ecc71", highlightthickness=1)
        tips_card.pack(fill=tk.X)
        
        tk.Label(tips_card, text="💡 ПОЛЕЗНЫЙ СОВЕТ", font=("Segoe UI", 10, "bold"),
                bg="#1a1a2e", fg="#2ecc71").pack(anchor=tk.W, pady=(0, 8))
        
        tips_text = "• Чем чаще паркуетесь, тем выше ваша скидка!\n\n• Электромобили получают скидку 10%\n\n• В выходные действует скидка 20%\n\n• Каждая 10-я парковка бесплатно"
        tk.Label(tips_card, text=tips_text, font=("Segoe UI", 9),
                bg="#1a1a2e", fg="#bdc3c7", justify=tk.LEFT).pack(anchor=tk.W)
        
        parking_data = [
            {"name": "ул. Петровская", "icon": "🏛️", "color": "#27ae60", "desc": "Центральная парковка", "price": "50 ₽/час", "rating": 4.9},
            {"name": "ул. Чехова", "icon": "📚", "color": "#2980b9", "desc": "Рядом с театром", "price": "45 ₽/час", "rating": 4.7},
            {"name": "ул. Дзержинского", "icon": "🏢", "color": "#e67e22", "desc": "Деловой квартал", "price": "55 ₽/час", "rating": 4.8}
        ]
        
        for card_data in parking_data:
            lot = self.lots[card_data["name"]]
            occupied = sum(1 for spot in lot.spots if spot.is_occupied)
            total = len(lot.spots) if lot.spots else 40
            free = total - occupied
            occupancy_percent = (occupied / total) * 100 if total > 0 else 0
            
            if occupancy_percent < 30:
                status_color = "#2ecc71"
                status_text = "Низкая"
                status_icon = "🟢"
            elif occupancy_percent < 70:
                status_color = "#f39c12"
                status_text = "Средняя"
                status_icon = "🟡"
            else:
                status_color = "#e74c3c"
                status_text = "Высокая"
                status_icon = "🔴"
            
            card = tk.Frame(cards_frame, bg="#1a1a2e", relief=tk.FLAT,
                           highlightbackground=card_data["color"], highlightthickness=2)
            card.pack(fill=tk.X, pady=8)
            
            left_part = tk.Frame(card, bg="#1a1a2e", width=70)
            left_part.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=12)
            left_part.pack_propagate(False)
            
            icon_label = tk.Label(left_part, text=card_data["icon"], font=("Segoe UI", 32),
                                 bg="#1a1a2e", fg=card_data["color"])
            icon_label.pack(expand=True)
            
            right_part = tk.Frame(card, bg="#1a1a2e")
            right_part.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=12)
            
            title_frame = tk.Frame(right_part, bg="#1a1a2e")
            title_frame.pack(fill=tk.X, pady=(0, 5))
            
            name_label = tk.Label(title_frame, text=card_data["name"], font=("Segoe UI", 14, "bold"),
                                 bg="#1a1a2e", fg="white")
            name_label.pack(side=tk.LEFT)
            
            rating_label = tk.Label(title_frame, text=f"⭐ {card_data['rating']}", font=("Segoe UI", 9),
                                   bg="#1a1a2e", fg="#f1c40f")
            rating_label.pack(side=tk.LEFT, padx=(10, 0))
            
            desc_label = tk.Label(right_part, text=card_data["desc"], font=("Segoe UI", 9),
                                 bg="#1a1a2e", fg="#bdc3c7", anchor=tk.W)
            desc_label.pack(anchor=tk.W, pady=(0, 6))
            
            status_row = tk.Frame(right_part, bg="#1a1a2e")
            status_row.pack(fill=tk.X, pady=(0, 5))
            
            tk.Label(status_row, text=f"{status_icon} {status_text}", font=("Segoe UI", 9, "bold"),
                    bg="#1a1a2e", fg=status_color).pack(side=tk.LEFT)
            
            tk.Label(status_row, text=f"  |  🟢 Свободно: {free}  |  🔴 Занято: {occupied}",
                    font=("Segoe UI", 9), bg="#1a1a2e", fg="#bdc3c7").pack(side=tk.LEFT)
            
            price_label = tk.Label(right_part, text=f"💰 {card_data['price']}", font=("Segoe UI", 11, "bold"),
                                  bg="#1a1a2e", fg="#f1c40f")
            price_label.pack(anchor=tk.W, pady=(0, 8))
            
            select_btn = ModernButton(right_part, "ВЫБРАТЬ", 
                                     lambda n=card_data["name"]: self.go_to_parking(n),
                                     bg_gradient=(card_data["color"], self._darken_color(card_data["color"])), 
                                     icon="→", width=140, height=32)
            select_btn.pack(anchor=tk.E)
            
            my_spot = lot.get_my_active_parking(self.client_plate)
            if my_spot:
                my_label = tk.Label(right_part, text=f"⭐ Ваше место: №{my_spot.spot_id}", 
                                   font=("Segoe UI", 8, "bold"), bg="#2d2d3d", fg="#f1c40f", padx=6, pady=2)
                my_label.pack(anchor=tk.W, pady=(5, 0))

    def _darken_color(self, color):
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color

    # ---------- ОСТАЛЬНЫЕ МЕТОДЫ ----------
    def show_leave_choice(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="🚙", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="ОСВОБОЖДЕНИЕ МЕСТА", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)
        
        info_label = tk.Label(content, text="Выберите парковку для освобождения места", 
                             font=("Segoe UI", 14, "bold"), bg="#0a0a0f", fg="white")
        info_label.pack(pady=(0, 20))
        
        found_any = False
        for name in self.lots.keys():
            lot = self.lots[name]
            my_spot = lot.get_my_active_parking(self.client_plate)
            if my_spot:
                found_any = True
                btn_text = f"{name} - место {my_spot.spot_id}"
                btn = ModernButton(content, btn_text, lambda n=name, s=my_spot.spot_id: self.go_to_parking_for_leave(n, s),
                                  bg_gradient=("#e67e22", "#f39c12"), icon="🚙", width=400, height=50)
                btn.pack(pady=10)
        
        if not found_any:
            no_parking_label = tk.Label(content, text="У вас нет активных парковок", 
                                       font=("Segoe UI", 13), bg="#0a0a0f", fg="#7f8c8d")
            no_parking_label.pack(pady=40)

    def go_to_parking(self, parking_name):
        self.current_lot = self.lots[parking_name]
        self.last_parking_name = parking_name
        self._return_to_parking = parking_name
        self._show_parking_scheme()

    def go_to_parking_for_leave(self, parking_name, spot_id):
        self.current_lot = self.lots[parking_name]
        self.last_parking_name = parking_name
        self._return_to_parking = parking_name
        self._show_parking_scheme()
        self.root.after(300, lambda: self._open_leave_form(spot_id))

    def _show_parking_scheme(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        toolbar = tk.Frame(self.current_frame, bg="#1a1a2e", height=55)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)
        
        top_border = tk.Frame(toolbar, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)

        left_buttons = tk.Frame(toolbar, bg="#1a1a2e")
        left_buttons.pack(side=tk.LEFT, padx=10, pady=8)
        
        main_menu_btn = ModernButton(left_buttons, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=150, height=38)
        main_menu_btn.pack(side=tk.LEFT, padx=4)
        
        change_parking_btn = ModernButton(left_buttons, "СМЕНИТЬ ПАРКОВКУ", 
                                         lambda: self._handle_parking_action(self.show_parking_choice),
                                         bg_gradient=("#3498db", "#2980b9"), icon="🔄", width=170, height=38)
        change_parking_btn.pack(side=tk.LEFT, padx=4)
        
        park_btn = ModernButton(left_buttons, "ПРИПАРКОВАТЬ",
                               lambda: self._handle_parking_action(self.show_parking_choice),
                               bg_gradient=("#27ae60", "#2ecc71"), icon="🚗", width=160, height=38)
        park_btn.pack(side=tk.LEFT, padx=4)
        
        leave_btn = ModernButton(left_buttons, "ОСВОБОДИТЬ",
                                lambda: self._handle_parking_action(self.show_leave_choice),
                                bg_gradient=("#e67e22", "#f39c12"), icon="🚙", width=150, height=38)
        leave_btn.pack(side=tk.LEFT, padx=4)
        
        right_buttons = tk.Frame(toolbar, bg="#1a1a2e")
        right_buttons.pack(side=tk.RIGHT, padx=10, pady=8)
        
        my_car_btn = ModernButton(right_buttons, "ГДЕ МАШИНА?",
                                 lambda: self._handle_parking_action(self.show_my_cars),
                                 bg_gradient=("#9b59b6", "#8e44ad"), icon="📍", width=140, height=38)
        my_car_btn.pack(side=tk.LEFT, padx=4)
        
        history_btn = ModernButton(right_buttons, "ИСТОРИЯ",
                                  lambda: self._handle_parking_action(self.show_history),
                                  bg_gradient=("#2980b9", "#2471a3"), icon="📋", width=120, height=38)
        history_btn.pack(side=tk.LEFT, padx=4)
        
        tariffs_btn = ModernButton(right_buttons, "ТАРИФЫ",
                                  lambda: self._handle_parking_action(self.show_tariffs),
                                  bg_gradient=("#f39c12", "#e67e22"), icon="💰", width=120, height=38)
        tariffs_btn.pack(side=tk.LEFT, padx=4)

        my_active = self.current_lot.get_my_active_parking(self.client_plate)
        if my_active:
            active_spot_btn = ModernButton(toolbar, f"МЕСТО {my_active.spot_id}",
                                          lambda sid=my_active.spot_id: self._open_leave_form(sid),
                                          bg_gradient=("#e74c3c", "#c0392b"), icon="⚠️", width=120, height=38)
            active_spot_btn.pack(side=tk.RIGHT, padx=10)

        self.clock_label = tk.Label(toolbar, font=("Segoe UI", 12, "bold"), 
                                   bg="#1a1a2e", fg="#f1c40f")
        self.clock_label.pack(side=tk.RIGHT, padx=15)
        self._update_clock()

        canvas_container = tk.Frame(self.current_frame, bg="#0a0a0f")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 10))
        
        self.canvas = tk.Canvas(canvas_container, bg="#2d2d3d", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.info_label = tk.Label(self.current_frame, 
                                   text=f"Парковка: {self.current_lot.name} | Нажмите на место",
                                   font=("Segoe UI", 11), 
                                   bg="#1a1a2e", fg="#bdc3c7", 
                                   padx=15, pady=6, anchor="w")
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.bind("<Button-1>", self._on_click_parking)
        self.root.after(100, self._generate_and_draw_parking)
    
    def _generate_and_draw_parking(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 100 or height < 100:
            self.root.after(200, self._generate_and_draw_parking)
            return
        
        if self.current_lot.name == "ул. Петровская":
            spots_data = self.generate_petrovskaya_spots(width, height)
        elif self.current_lot.name == "ул. Чехова":
            spots_data = self.generate_chekhova_spots(width, height)
        else:
            spots_data = self.generate_dzerzhinskogo_spots(width, height)
        
        self.current_lot.spots = []
        for i, (x, y, w, h) in enumerate(spots_data):
            spot = ParkingSpot(i+1, x, y, w, h)
            self.current_lot.spots.append(spot)
        
        self.current_lot._load_global_state()
        self._draw_parking_scheme_centered()
    
    def _handle_parking_action(self, action_func):
        action_func()
    
    def _return_to_parking_scheme(self):
        # Перезагружаем состояние парковки перед возвратом
        if self.last_parking_name and self.last_parking_name in self.lots:
            self.current_lot = self.lots[self.last_parking_name]
            # Перезагружаем актуальное состояние из файла
            self.current_lot._load_global_state()
            self._show_parking_scheme()

    def _draw_parking_scheme_centered(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 100 or height < 100:
            self.root.after(200, self._draw_parking_scheme_centered)
            return
        
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, width, height, fill="#2d2d3d", outline="")
        
        for _ in range(80):
            x = random.randint(10, width - 10)
            y = random.randint(10, height - 10)
            self.canvas.create_oval(x, y, x + 2, y + 2, fill="#3d3d4d", outline="")
        
        for spot in self.current_lot.spots:
            x1, y1 = spot.x, spot.y
            x2, y2 = spot.x + spot.w, spot.y + spot.h
            
            if spot.is_occupied:
                fill_color = "#e74c3c"
                status_text = "ЗАНЯТО"
                text_color = "white"
            else:
                fill_color = "#27ae60"
                status_text = "СВОБОДНО"
                text_color = "#f1c40f"
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#f1c40f", width=2)
            spot.rect_id = rect
            
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            label = self.canvas.create_text(center_x, center_y - 10, text=str(spot.spot_id),
                                            font=("Segoe UI", 14, "bold"), fill=text_color)
            spot.label_id = label
            
            status = self.canvas.create_text(center_x, center_y + 14, text=status_text,
                                            font=("Segoe UI", 8, "bold"), fill="white")
            spot.car_items.append(status)
            
            if spot.is_occupied:
                self._draw_parking_car(spot, center_x, center_y)
        
        self.canvas.create_rectangle(width//2 - 150, 10, width//2 + 150, 45, fill="#1a1a2e", outline="#f1c40f", width=2)
        self.canvas.create_text(width // 2, 28, text=self.current_lot.name, 
                                fill="#f1c40f", font=("Segoe UI", 16, "bold"))
        
        occupied = sum(1 for spot in self.current_lot.spots if spot.is_occupied)
        total = len(self.current_lot.spots)
        self.canvas.create_rectangle(width//2 - 110, 50, width//2 + 110, 72, fill="#1a1a2e", outline="#f1c40f", width=1)
        self.canvas.create_text(width // 2, 61, 
                                text=f"🟢 Свободно: {total - occupied}  |  🔴 Занято: {occupied}",
                                fill="white", font=("Segoe UI", 9))
        
        legend_x = 20
        legend_y = 55
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 130, legend_y + 35, 
                                      fill="#1a1a2e", outline="#f1c40f", width=1)
        self.canvas.create_text(legend_x + 10, legend_y + 12, text="🟢 Свободно", 
                                font=("Segoe UI", 8), fill="white", anchor=tk.W)
        self.canvas.create_text(legend_x + 10, legend_y + 26, text="🔴 Занято", 
                                font=("Segoe UI", 8), fill="white", anchor=tk.W)

    def _draw_parking_car(self, spot, center_x, center_y):
        vehicle_type = spot.vehicle.vehicle_type
        sticker_map = {"Легковой": "🚗", "Грузовой": "🚚", "Мотоцикл": "🏍️", "Электромобиль": "🔋"}
        sticker_text = sticker_map.get(vehicle_type, "🚗")
        
        if spot.owner_plate == self.client_plate:
            sticker_text = "⭐ " + sticker_text
        
        car_icon = self.canvas.create_text(center_x, center_y - 12, text=sticker_text, 
                                           font=("Segoe UI", 16), fill="white")
        spot.car_items.append(car_icon)
        
        plate_text = spot.vehicle.license_plate[-6:] if len(spot.vehicle.license_plate) > 6 else spot.vehicle.license_plate
        plate = self.canvas.create_rectangle(center_x - 22, center_y + 5, center_x + 22, center_y + 12,
                                              fill="white", outline="#333", width=1)
        plate_label = self.canvas.create_text(center_x, center_y + 8, text=plate_text,
                                              font=("Arial", 6, "bold"), fill="black")
        spot.car_items.extend([plate, plate_label])

    def _on_click_parking(self, event):
        for spot in self.current_lot.spots:
            if spot.x <= event.x <= spot.x + spot.w and spot.y <= event.y <= spot.y + spot.h:
                if spot.is_occupied:
                    if spot.owner_plate == self.client_plate:
                        # Сразу открываем форму освобождения без подтверждения
                        self._open_leave_form(spot.spot_id)
                    else:
                        # Показываем информацию о занятости внутри интерфейса
                        self.info_label.config(text=f"❌ Место {spot.spot_id} занято автомобилем {spot.vehicle.license_plate}")
                else:
                    # Сразу открываем форму парковки без подтверждения
                    self._open_park_form(spot.spot_id)
                return
        self.info_label.config(text="Нажмите на парковочное место")

    def _open_park_form(self, spot_id):
        # Проверяем, есть ли уже активная парковка
        for lot in self.lots.values():
            if lot.get_my_active_parking(self.client_plate):
                self.info_label.config(text="❌ Ошибка: Ваш автомобиль уже припаркован! Сначала освободите текущее место.")
                return
        
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="🚗", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text=f"ПАРКОВКА - МЕСТО {spot_id}", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", self._return_to_parking_scheme,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=110, height=35)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=40, pady=25)
        
        main = tk.Frame(content, bg="#1a1a2e", padx=25, pady=20)
        main.pack(expand=True)
        
        spot_label = tk.Label(main, text=f"Место №{spot_id}", font=("Segoe UI", 16, "bold"),
                             bg="#1a1a2e", fg="#f1c40f")
        spot_label.pack(pady=(0, 12))
        
        type_label = tk.Label(main, text="Тип транспорта", font=("Segoe UI", 10), bg="#1a1a2e", fg="#bdc3c7")
        type_label.pack(anchor=tk.W)
        
        vehicle_type = tk.StringVar(value="Легковой")
        types_frame = tk.Frame(main, bg="#1a1a2e")
        types_frame.pack(fill=tk.X, pady=6)
        for t in ["Легковой", "Грузовой", "Мотоцикл", "Электромобиль"]:
            rb = tk.Radiobutton(types_frame, text=t, variable=vehicle_type, value=t,
                               bg="#1a1a2e", fg="white", selectcolor="#1a1a2e", font=("Segoe UI", 9))
            rb.pack(side=tk.LEFT, padx=8)
        
        datetime_label = tk.Label(main, text="Дата и время заезда", font=("Segoe UI", 10), bg="#1a1a2e", fg="#bdc3c7")
        datetime_label.pack(anchor=tk.W, pady=(8, 3))
        
        datetime_frame = tk.Frame(main, bg="#1a1a2e")
        datetime_frame.pack(fill=tk.X)
        
        date_entry = tk.Entry(datetime_frame, width=12, font=("Segoe UI", 9), bg="#0d0d1a", fg="white", insertbackground="white")
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(side=tk.LEFT, padx=5)
        
        time_entry = tk.Entry(datetime_frame, width=8, font=("Segoe UI", 9), bg="#0d0d1a", fg="white", insertbackground="white")
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        time_entry.pack(side=tk.LEFT, padx=5)
        
        def set_now():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            time_entry.delete(0, tk.END)
            time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        now_btn = tk.Button(datetime_frame, text="Сейчас", command=set_now,
                           bg="#2980b9", fg="white", font=("Segoe UI", 8), padx=10, bd=0, cursor="hand2")
        now_btn.pack(side=tk.LEFT, padx=5)
        
        info_frame = tk.Frame(main, bg="#0d0d1a", padx=10, pady=6)
        info_frame.pack(fill=tk.X, pady=12)
        rate_label = tk.Label(info_frame, text=f"Тариф: {self.current_lot.get_rate_for_type('Легковой'):.0f} руб/час",
                             bg="#0d0d1a", fg="#f1c40f", font=("Segoe UI", 9))
        rate_label.pack()
        
        def update_rate(*args):
            rate = self.current_lot.get_rate_for_type(vehicle_type.get())
            rate_label.config(text=f"Тариф: {rate:.0f} руб/час")
        vehicle_type.trace('w', update_rate)
        
        # Сообщение об успехе/ошибке
        result_label = tk.Label(main, text="", font=("Segoe UI", 11), bg="#1a1a2e")
        result_label.pack(pady=5)
        
        def confirm():
            try:
                dt = datetime.strptime(f"{date_entry.get()} {time_entry.get()}", "%Y-%m-%d %H:%M")
                if dt > datetime.now():
                    result_label.config(text="❌ Время не может быть в будущем", fg="#e74c3c")
                    return
            except:
                result_label.config(text="❌ Неверный формат даты/времени", fg="#e74c3c")
                return
            
            vehicle = Vehicle(self.client_plate, vehicle_type.get(), self.client_name)
            vehicle.entry_time = dt
            
            if self.current_lot.park(spot_id, vehicle, dt, self.client_plate):
                result_label.config(text=f"✅ Автомобиль успешно припаркован на место {spot_id}!", fg="#2ecc71")
                self.root.after(1500, self._return_to_parking_scheme)
            else:
                result_label.config(text=f"❌ Место {spot_id} уже занято", fg="#e74c3c")
        
        confirm_btn = ModernButton(main, "ПРИПАРКОВАТЬ", confirm,
                                  bg_gradient=("#27ae60", "#2ecc71"), icon="✓", width=220, height=38)
        confirm_btn.pack(pady=(12, 5))

    def _open_leave_form(self, spot_id):
        spot = self.current_lot.find_spot(spot_id)
        if not spot or not spot.is_occupied:
            self.info_label.config(text="❌ Место уже свободно")
            self._return_to_parking_scheme()
            return
        
        if spot.owner_plate != self.client_plate:
            self.info_label.config(text="❌ Это не ваше место!")
            self._return_to_parking_scheme()
            return
        
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="🚙", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text=f"ОСВОБОЖДЕНИЕ - МЕСТО {spot_id}", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", self._return_to_parking_scheme,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=110, height=35)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=40, pady=25)
        
        main = tk.Frame(content, bg="#1a1a2e", padx=25, pady=20)
        main.pack(expand=True)
        
        info_frame = tk.Frame(main, bg="#0d0d1a", padx=12, pady=8)
        info_frame.pack(fill=tk.X, pady=8)
        
        car_label = tk.Label(info_frame, text=f"🚗 {spot.vehicle.license_plate}", bg="#0d0d1a", fg="white", font=("Segoe UI", 11))
        car_label.pack()
        type_label = tk.Label(info_frame, text=f"📋 Тип: {spot.vehicle.vehicle_type}", bg="#0d0d1a", fg="#bdc3c7", font=("Segoe UI", 9))
        type_label.pack()
        time_label = tk.Label(info_frame, text=f"🕐 Заехал: {spot.vehicle.entry_time.strftime('%Y-%m-%d %H:%M')}", 
                             bg="#0d0d1a", fg="#bdc3c7", font=("Segoe UI", 9))
        time_label.pack()
        
        exit_label = tk.Label(main, text="Дата и время выезда", font=("Segoe UI", 10), bg="#1a1a2e", fg="#bdc3c7")
        exit_label.pack(anchor=tk.W, pady=(8, 3))
        
        time_frame = tk.Frame(main, bg="#1a1a2e")
        time_frame.pack(fill=tk.X)
        
        date_entry = tk.Entry(time_frame, width=12, font=("Segoe UI", 9), bg="#0d0d1a", fg="white", insertbackground="white")
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(side=tk.LEFT, padx=5)
        
        time_entry = tk.Entry(time_frame, width=8, font=("Segoe UI", 9), bg="#0d0d1a", fg="white", insertbackground="white")
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        time_entry.pack(side=tk.LEFT, padx=5)
        
        def set_now():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            time_entry.delete(0, tk.END)
            time_entry.insert(0, datetime.now().strftime("%H:%M"))
            calc()
        
        now_btn = tk.Button(time_frame, text="Сейчас", command=set_now, bg="#2980b9", fg="white", font=("Segoe UI", 8), padx=10, bd=0, cursor="hand2")
        now_btn.pack(side=tk.LEFT, padx=5)
        
        calc_frame = tk.Frame(main, bg="#0d0d1a", padx=10, pady=8)
        calc_frame.pack(fill=tk.X, pady=12)
        calc_label = tk.Label(calc_frame, text="", bg="#0d0d1a", fg="#f1c40f", font=("Segoe UI", 11, "bold"))
        calc_label.pack()
        
        def calc(*args):
            try:
                exit_dt = datetime.strptime(f"{date_entry.get()} {time_entry.get()}", "%Y-%m-%d %H:%M")
                if exit_dt < spot.vehicle.entry_time:
                    calc_label.config(text="❌ Ошибка: время выезда раньше заезда")
                    return
                duration = exit_dt - spot.vehicle.entry_time
                hours = math.ceil(duration.total_seconds() / 3600)
                rate = self.current_lot.get_rate_for_type(spot.vehicle.vehicle_type)
                cost = hours * rate
                calc_label.config(text=f"💰 К оплате: {cost:.2f} руб | ⏱️ Время: {hours} ч")
            except:
                calc_label.config(text="Введите корректную дату")
        
        date_entry.bind("<KeyRelease>", lambda e: calc())
        time_entry.bind("<KeyRelease>", lambda e: calc())
        calc()
        
        # Сообщение об успехе/ошибке
        result_label = tk.Label(main, text="", font=("Segoe UI", 11), bg="#1a1a2e")
        result_label.pack(pady=5)
        
        def confirm():
            try:
                exit_dt = datetime.strptime(f"{date_entry.get()} {time_entry.get()}", "%Y-%m-%d %H:%M")
            except:
                result_label.config(text="❌ Неверный формат", fg="#e74c3c")
                return
            if exit_dt < spot.vehicle.entry_time:
                result_label.config(text="❌ Время выезда не может быть раньше заезда", fg="#e74c3c")
                return
            
            result = self.current_lot.leave(spot_id, exit_dt, self.client_plate)
            if result:
                vehicle, cost, hours = result
                result_label.config(text=f"✅ Парковка завершена! {vehicle.license_plate} | {hours} ч | {cost:.2f} руб", fg="#2ecc71")
                # После успешного освобождения перезагружаем состояние и обновляем отображение
                self.current_lot._load_global_state()
                self.root.after(2000, self._return_to_parking_scheme)
            else:
                result_label.config(text="❌ Не удалось освободить место", fg="#e74c3c")
        
        confirm_btn = ModernButton(main, "ОСВОБОДИТЬ И ОПЛАТИТЬ", confirm,
                                  bg_gradient=("#e67e22", "#f39c12"), icon="✓", width=220, height=38)
        confirm_btn.pack(pady=(12, 5))

    def show_history(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="📋", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="МОЯ ИСТОРИЯ", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        if hasattr(self, '_return_to_parking') and self._return_to_parking:
            back_cmd = self._return_to_parking_scheme
        else:
            back_cmd = self.show_main_menu
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", back_cmd,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=110, height=35)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        filter_frame = tk.Frame(content, bg="#0a0a0f")
        filter_frame.pack(fill=tk.X, pady=(0, 12))
        
        filter_label = tk.Label(filter_frame, text="Парковка:", font=("Segoe UI", 10), bg="#0a0a0f", fg="white")
        filter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        history_parking_var = tk.StringVar(value=list(self.lots.keys())[0])
        parking_combo = ttk.Combobox(filter_frame, textvariable=history_parking_var,
                                     values=list(self.lots.keys()), state="readonly", width=25, font=("Segoe UI", 10))
        parking_combo.pack(side=tk.LEFT)
        
        tree_frame = tk.Frame(content, bg="#0a0a0f")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        columns = ("Место", "Тип ТС", "Время заезда", "Время выезда", "Длительность", "Стоимость (руб)")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12,
                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor=tk.CENTER)
        
        tree.tag_configure('active', background='#2d2d4d')
        
        total_label = tk.Label(content, text="", font=("Segoe UI", 11, "bold"),
                               bg="#0a0a0f", fg="#f1c40f")
        total_label.pack(pady=(8, 0))
        
        def refresh_history(*args):
            for row in tree.get_children():
                tree.delete(row)
            
            parking_name = history_parking_var.get()
            parking = self.lots[parking_name]
            
            total_spent = 0
            for rec in parking.history:
                if rec.get("license_plate") != self.client_plate:
                    continue
                    
                if rec["exit_time"]:
                    exit_dt = datetime.strptime(rec["exit_time"], "%Y-%m-%d %H:%M:%S")
                    entry_dt = datetime.strptime(rec["entry_time"], "%Y-%m-%d %H:%M:%S")
                    duration = exit_dt - entry_dt
                    hours = math.ceil(duration.total_seconds() / 3600)
                    dur_str = f"{hours} ч" if hours > 0 else "<1 ч"
                    cost = rec["cost"] if rec["cost"] else 0
                    total_spent += cost
                    exit_display = rec["exit_time"][5:16]
                    tag = ''
                else:
                    exit_display = "Активна"
                    dur_str = "—"
                    cost = "—"
                    tag = 'active'
                
                tree.insert("", tk.END, values=(
                    rec["spot_id"],
                    rec.get("vehicle_type", "Легковой"),
                    rec["entry_time"][5:16],
                    exit_display,
                    dur_str,
                    cost if cost != "—" else "—"
                ), tags=(tag,))
            
            total_label.config(text=f"💰 Всего оплачено: {total_spent:.2f} руб")
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)
        
        parking_combo.bind("<<ComboboxSelected>>", lambda e: refresh_history())
        refresh_history()

    def show_tariffs(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=70)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=30, pady=15)
        
        title_icon = tk.Label(title_frame, text="💰", font=("Segoe UI", 28), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(title_frame, text="ТАРИФЫ", font=("Segoe UI", 20, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=30, pady=15)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=160, height=40)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        if hasattr(self, '_return_to_parking') and self._return_to_parking:
            back_cmd = self._return_to_parking_scheme
        else:
            back_cmd = self.show_main_menu
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", back_cmd,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=130, height=40)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)
        
        info_label = tk.Label(content, text="Стоимость парковки по типам транспорта", 
                             font=("Segoe UI", 18, "bold"), bg="#0a0a0f", fg="white")
        info_label.pack(pady=(0, 20))
        
        columns = ("Тип транспорта", "Ставка (руб/час)", "Коэффициент", "Примечание")
        tree = ttk.Treeview(content, columns=columns, show="headings", height=5)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Segoe UI', 13, 'bold'))
        style.configure("Treeview", font=('Segoe UI', 12), rowheight=40)
        
        tree.heading("Тип транспорта", text="Тип транспорта")
        tree.heading("Ставка (руб/час)", text="Ставка (руб/час)")
        tree.heading("Коэффициент", text="Коэффициент")
        tree.heading("Примечание", text="Примечание")
        
        tree.column("Тип транспорта", width=220, anchor=tk.CENTER)
        tree.column("Ставка (руб/час)", width=160, anchor=tk.CENTER)
        tree.column("Коэффициент", width=130, anchor=tk.CENTER)
        tree.column("Примечание", width=280, anchor=tk.W)
        
        rates = [
            ("🚗 Легковой", f"{ParkingLot.BASE_HOURLY_RATE}", "1.0", "Базовый тариф"),
            ("🚚 Грузовой", f"{ParkingLot.BASE_HOURLY_RATE * 1.5:.0f}", "1.5", "+50% к базовому"),
            ("🏍️ Мотоцикл", f"{ParkingLot.BASE_HOURLY_RATE * 0.7:.0f}", "0.7", "-30% к базовому"),
            ("🔋 Электромобиль", f"{ParkingLot.BASE_HOURLY_RATE * 0.9:.0f}", "0.9", "-10% к базовому")
        ]
        for r in rates:
            tree.insert("", tk.END, values=r)
        tree.pack(pady=20, ipady=5)
        
        info_frame = tk.Frame(content, bg="#1a1a2e", padx=20, pady=15)
        info_frame.pack(fill=tk.X, pady=15)
        
        info_title = tk.Label(info_frame, text="ℹ️ Информация", font=("Segoe UI", 13, "bold"),
                             bg="#1a1a2e", fg="#f1c40f")
        info_title.pack(anchor=tk.W, pady=(0, 8))
        
        info1 = tk.Label(info_frame, text="• Время округляется до полного часа вверх",
                        font=("Segoe UI", 11), bg="#1a1a2e", fg="#bdc3c7")
        info1.pack(anchor=tk.W, pady=3)
        
        info2 = tk.Label(info_frame, text="• Оплата производится при выезде с парковки",
                        font=("Segoe UI", 11), bg="#1a1a2e", fg="#bdc3c7")
        info2.pack(anchor=tk.W, pady=3)
        
        info3 = tk.Label(info_frame, text="• Действует накопительная система скидок",
                        font=("Segoe UI", 11), bg="#1a1a2e", fg="#bdc3c7")
        info3.pack(anchor=tk.W, pady=3)
        
        info4 = tk.Label(info_frame, text="• Каждая 10-я парковка бесплатно",
                        font=("Segoe UI", 11), bg="#1a1a2e", fg="#bdc3c7")
        info4.pack(anchor=tk.W, pady=3)

    def show_my_cars(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        active_spots = []
        for lot_name, lot in self.lots.items():
            spot = lot.get_my_active_parking(self.client_plate)
            if spot:
                active_spots.append((lot_name, spot))
        
        self.current_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        top_panel = tk.Frame(self.current_frame, bg="#1a1a2e", height=60)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        top_border = tk.Frame(top_panel, bg="#f1c40f", height=3)
        top_border.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(top_panel, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT, padx=25, pady=12)
        
        title_icon = tk.Label(title_frame, text="📍", font=("Segoe UI", 22), 
                             bg="#1a1a2e", fg="#f1c40f")
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="ГДЕ МОЯ МАШИНА?", font=("Segoe UI", 16, "bold"),
                              bg="#1a1a2e", fg="#f1c40f")
        title_label.pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(top_panel, bg="#1a1a2e")
        buttons_frame.pack(side=tk.RIGHT, padx=25, pady=12)
        
        main_menu_btn = ModernButton(buttons_frame, "ГЛАВНОЕ МЕНЮ", self.show_main_menu,
                                    bg_gradient=("#2c3e50", "#34495e"), icon="🏠", width=140, height=35)
        main_menu_btn.pack(side=tk.LEFT, padx=5)
        
        if hasattr(self, '_return_to_parking') and self._return_to_parking:
            back_cmd = self._return_to_parking_scheme
        else:
            back_cmd = self.show_main_menu
        
        back_btn = ModernButton(buttons_frame, "НАЗАД", back_cmd,
                               bg_gradient=("#c0392b", "#e74c3c"), icon="◀", width=110, height=35)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        content = tk.Frame(self.current_frame, bg="#0a0a0f")
        content.pack(expand=True, fill=tk.BOTH, padx=40, pady=25)
        
        car_label = tk.Label(content, text=f"Автомобиль: {self.client_plate}", font=("Segoe UI", 13, "bold"),
                            bg="#0a0a0f", fg="white")
        car_label.pack(pady=(0, 20))
        
        if not active_spots:
            no_parking_label = tk.Label(content, text="Нет активных парковок", font=("Segoe UI", 12),
                                       bg="#0a0a0f", fg="#7f8c8d")
            no_parking_label.pack(pady=40)
        else:
            for lot_name, spot in active_spots:
                card = tk.Frame(content, bg="#1a1a2e", padx=15, pady=12, relief=tk.FLAT,
                               highlightbackground="#f1c40f", highlightthickness=1)
                card.pack(fill=tk.X, pady=8)
                
                info_text = f"📍 {lot_name}  |  Место №{spot.spot_id}  |  🚗 {spot.vehicle.vehicle_type}"
                if spot.vehicle and spot.vehicle.entry_time:
                    info_text += f"  |  🕐 Заехал: {spot.vehicle.entry_time.strftime('%H:%M %d.%m.%Y')}"
                
                info_label = tk.Label(card, text=info_text, font=("Segoe UI", 10),
                                     bg="#1a1a2e", fg="#bdc3c7")
                info_label.pack(anchor=tk.W, pady=4)
                
                btn_frame = tk.Frame(card, bg="#1a1a2e")
                btn_frame.pack(pady=(8, 0))
                
                go_btn = tk.Button(btn_frame, text="ПЕРЕЙТИ НА ПАРКОВКУ", 
                                  command=lambda l=lot_name: self.go_to_parking(l),
                                  bg="#2980b9", fg="white", font=("Segoe UI", 9, "bold"),
                                  padx=15, pady=4, bd=0, cursor="hand2", relief=tk.FLAT)
                go_btn.pack(side=tk.LEFT, padx=5)
                
                leave_btn = tk.Button(btn_frame, text="ОСВОБОДИТЬ МЕСТО", 
                                     command=lambda l=lot_name, s=spot.spot_id: self.go_to_parking_for_leave(l, s),
                                     bg="#e67e22", fg="white", font=("Segoe UI", 9, "bold"),
                                     padx=15, pady=4, bd=0, cursor="hand2", relief=tk.FLAT)
                leave_btn.pack(side=tk.LEFT, padx=5)

    def _update_clock(self):
        try:
            if hasattr(self, 'clock_label') and self.clock_label.winfo_exists():
                self.clock_label.config(text=datetime.now().strftime("%H:%M:%S  %d.%m.%Y"))
                self.root.after(1000, self._update_clock)
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()