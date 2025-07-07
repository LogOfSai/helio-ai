import tkinter as tk
from tkinter import ttk
import math
import colorsys
import random  # Added missing import

class BreathingExercises:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Breathing Exercises")
        self.window.geometry("900x700")
        self.window.configure(bg="#1a1a2e")
        
        self.current_exercise = None
        self.animation_id = None
        self.animation_time = 0
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with dark theme
        self.main_frame = ttk.Frame(self.window, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section with gradient background
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create gradient header
        header_canvas = tk.Canvas(
            header_frame,
            height=100,
            bg="#1a1a2e",
            highlightthickness=0
        )
        header_canvas.pack(fill=tk.X)
        
        # Create gradient
        for i in range(100):
            color = self._interpolate_color("#1a1a2e", "#16213e", i/100)
            header_canvas.create_line(0, i, 900, i, fill=color)
        
        # Title with custom font and shadow effect
        title_text = header_canvas.create_text(
            450, 50,
            text="🧘 Mindful Breathing",
            font=("Arial", 24, "bold"),
            fill="#ffffff"
        )
        
        # Add shadow effect
        header_canvas.create_text(
            452, 52,
            text="🧘 Mindful Breathing",
            font=("Arial", 24, "bold"),
            fill="#1a1a2e"
        )
        header_canvas.tag_lower("shadow")
        
        # Exercise selection frame with modern cards
        exercise_frame = ttk.Frame(self.main_frame)
        exercise_frame.pack(fill=tk.X, pady=(0, 20))
        
        exercises = [
            ("4-7-8 Breathing", "Inhale for 4, hold for 7, exhale for 8", "#4a90e2"),
            ("Box Breathing", "Equal duration for inhale, hold, exhale, and hold", "#50c878"),
            ("Deep Breathing", "Long, deep breaths with natural pauses", "#9b59b6"),
            ("Equal Breathing", "Equal duration for inhale and exhale", "#e67e22"),
            ("Alternate Nostril", "Alternating breath between nostrils", "#e74c3c")
        ]
        
        # Create exercise cards in a grid
        for i, (title, desc, color) in enumerate(exercises):
            self.create_exercise_card(exercise_frame, title, desc, color, i)
        
        # Animation canvas with increased size
        self.canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=400,
            bg="#1a1a2e",
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        # Instruction label with modern styling
        self.instruction_label = tk.Label(
            self.main_frame,
            text="Select a breathing exercise to begin",
            font=("Arial", 16),
            bg="#1a1a2e",
            fg="white"
        )
        self.instruction_label.pack(pady=20)
        
    def create_exercise_card(self, parent, title, description, color, index):
        # Card frame with hover effect
        card = tk.Frame(
            parent,
            bg="#16213e",
            padx=15,
            pady=15,
            cursor="hand2"
        )
        card.grid(row=index//3, column=index%3, padx=10, pady=10, sticky="ew")
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        
        # Add hover effect
        def on_enter(e):
            card.configure(bg="#1e2d4a")
            
        def on_leave(e):
            card.configure(bg="#16213e")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e, t=title: self.start_exercise(t))
        
        # Title with color accent
        title_frame = tk.Frame(card, bg="#16213e")
        title_frame.pack(fill=tk.X)
        
        accent = tk.Frame(title_frame, width=4, height=24, bg=color)
        accent.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            title_frame,
            text=title,
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # Description
        tk.Label(
            card,
            text=description,
            font=("Arial", 11),
            bg="#16213e",
            fg="#a0a0a0",
            wraplength=200,
            justify="left"
        ).pack(fill=tk.X, pady=(5, 0))
        
    def _interpolate_color(self, color1, color2, factor):
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to hex
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        c1 = hex_to_rgb(color1)
        c2 = hex_to_rgb(color2)
        
        rgb = [int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3)]
        return rgb_to_hex(rgb)
        
    def create_gradient_circle(self, x, y, radius, start_color, end_color, progress=1.0):
        steps = 50
        for i in range(steps):
            ratio = i / steps
            # Create shimmering effect
            shimmer = math.sin(ratio * math.pi + self.animation_time * 2) * 0.1
            current_ratio = ratio + shimmer
            
            # Interpolate between colors with shimmer
            color = self._interpolate_color(start_color, end_color, current_ratio)
            
            # Add pulsing effect to radius
            pulse = math.sin(self.animation_time * 3) * 5
            current_radius = radius * (1 - ratio) * progress + pulse
            
            # Create oval with gradient and effects
            self.canvas.create_oval(
                x - current_radius, y - current_radius,
                x + current_radius, y + current_radius,
                fill=color,
                outline=color
            )
            
            # Add particle effects
            if random.random() < 0.1:
                particle_size = random.randint(2, 5)
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, current_radius)
                px = x + math.cos(angle) * distance
                py = y + math.sin(angle) * distance
                particle_color = self._interpolate_color(start_color, end_color, random.random())
                self.canvas.create_oval(
                    px - particle_size, py - particle_size,
                    px + particle_size, py + particle_size,
                    fill=particle_color,
                    outline=""
                )
    
    def animate_breathing(self, phase, duration, max_radius, color_scheme, text=""):
        center_x = 400
        center_y = 200
        
        if not hasattr(self, 'animation_time'):
            self.animation_time = 0
        
        def update(step):
            if step >= duration:
                return
            
            self.animation_time += 0.1
            progress = step / duration
            
            if phase == "inhale":
                size = self._ease_in_out(progress)
                text_prefix = "Inhale"
            elif phase == "hold":
                size = 1.0
                text_prefix = "Hold"
            else:  # exhale
                size = 1.0 - self._ease_in_out(progress)
                text_prefix = "Exhale"
            
            self.canvas.delete("all")
            
            # Add background glow
            glow_radius = max_radius * 1.5 * size
            self.canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill=color_scheme[0],
                stipple="gray50"
            )
            
            # Create main breathing circle
            self.create_gradient_circle(
                center_x, center_y,
                max_radius, color_scheme[0], color_scheme[1],
                size
            )
            
            # Add instruction text with shadow
            self.canvas.create_text(
                center_x + 2, center_y + 2,
                text=f"{text_prefix}...\n{text}",
                font=("Arial", 20, "bold"),
                fill="#1a1a2e",
                justify="center"
            )
            self.canvas.create_text(
                center_x, center_y,
                text=f"{text_prefix}...\n{text}",
                font=("Arial", 20, "bold"),
                fill="white",
                justify="center"
            )
            
            self.animation_id = self.window.after(16, lambda: update(step + 1))
            
        update(0)
    
    def _ease_in_out(self, t):
        # Smooth easing function for animations
        return 0.5 * (1 - math.cos(math.pi * t))
    
    def start_exercise(self, exercise_type):
        # Stop any current animation
        if self.animation_id:
            self.window.after_cancel(self.animation_id)
            self.animation_id = None
        
        # Clear any previous content
        self.canvas.delete("all")
        
        # Reset animation time
        self.animation_time = 0
        
        # Update current exercise
        self.current_exercise = exercise_type
        
        # Start the appropriate exercise
        if exercise_type == "4-7-8 Breathing":
            self.start_478_breathing()
        elif exercise_type == "Box Breathing":
            self.start_box_breathing()
        elif exercise_type == "Deep Breathing":
            self.start_deep_breathing()
        elif exercise_type == "Equal Breathing":
            self.start_equal_breathing()
        elif exercise_type == "Alternate Nostril":
            self.start_alternate_nostril()
            
        # Update instruction label
        self.instruction_label.config(
            text=f"Follow the animation for {exercise_type}"
        )
    
    def start_478_breathing(self):
        def cycle(phase=0):
            if self.current_exercise != "4-7-8 Breathing":
                return
                
            if phase == 0:  # Inhale
                self.animate_breathing("inhale", 240, 150, ("#3498db", "#2980b9"), "4 seconds")
                self.animation_id = self.window.after(4000, lambda: cycle(1))
            elif phase == 1:  # Hold
                self.animate_breathing("hold", 420, 150, ("#2ecc71", "#27ae60"), "7 seconds")
                self.animation_id = self.window.after(7000, lambda: cycle(2))
            else:  # Exhale
                self.animate_breathing("exhale", 480, 150, ("#e74c3c", "#c0392b"), "8 seconds")
                self.animation_id = self.window.after(8000, lambda: cycle(0))
        
        cycle()
    
    def start_box_breathing(self):
        def cycle(phase=0):
            if self.current_exercise != "Box Breathing":
                return
                
            duration = 4000  # 4 seconds each phase
            if phase == 0:  # Inhale
                self.animate_breathing("inhale", 240, 150, ("#3498db", "#2980b9"), "4 seconds")
                self.animation_id = self.window.after(duration, lambda: cycle(1))
            elif phase == 1:  # Hold
                self.animate_breathing("hold", 240, 150, ("#2ecc71", "#27ae60"), "4 seconds")
                self.animation_id = self.window.after(duration, lambda: cycle(2))
            elif phase == 2:  # Exhale
                self.animate_breathing("exhale", 240, 150, ("#e74c3c", "#c0392b"), "4 seconds")
                self.animation_id = self.window.after(duration, lambda: cycle(3))
            else:  # Hold
                self.animate_breathing("hold", 240, 150, ("#9b59b6", "#8e44ad"), "4 seconds")
                self.animation_id = self.window.after(duration, lambda: cycle(0))
        
        cycle()
    
    def start_deep_breathing(self):
        def cycle(phase=0):
            if self.current_exercise != "Deep Breathing":
                return
                
            if phase == 0:  # Inhale
                self.animate_breathing("inhale", 300, 150, ("#3498db", "#2980b9"), "5 seconds")
                self.animation_id = self.window.after(5000, lambda: cycle(1))
            else:  # Exhale
                self.animate_breathing("exhale", 300, 150, ("#e74c3c", "#c0392b"), "5 seconds")
                self.animation_id = self.window.after(5000, lambda: cycle(0))
        
        cycle()
    
    def start_equal_breathing(self):
        def cycle(phase=0):
            if self.current_exercise != "Equal Breathing":
                return
                
            if phase == 0:  # Inhale
                self.animate_breathing("inhale", 240, 150, ("#3498db", "#2980b9"), "4 seconds")
                self.animation_id = self.window.after(4000, lambda: cycle(1))
            else:  # Exhale
                self.animate_breathing("exhale", 240, 150, ("#e74c3c", "#c0392b"), "4 seconds")
                self.animation_id = self.window.after(4000, lambda: cycle(0))
        
        cycle()
    
    def start_alternate_nostril(self):
        def cycle(phase=0):
            if self.current_exercise != "Alternate Nostril":
                return
                
            if phase == 0:  # Right nostril inhale
                self.animate_breathing("inhale", 240, 150, ("#3498db", "#2980b9"), "Right nostril")
                self.animation_id = self.window.after(4000, lambda: cycle(1))
            elif phase == 1:  # Hold
                self.animate_breathing("hold", 240, 150, ("#2ecc71", "#27ae60"), "Hold")
                self.animation_id = self.window.after(4000, lambda: cycle(2))
            elif phase == 2:  # Left nostril exhale
                self.animate_breathing("exhale", 240, 150, ("#e74c3c", "#c0392b"), "Left nostril")
                self.animation_id = self.window.after(4000, lambda: cycle(3))
            elif phase == 3:  # Left nostril inhale
                self.animate_breathing("inhale", 240, 150, ("#9b59b6", "#8e44ad"), "Left nostril")
                self.animation_id = self.window.after(4000, lambda: cycle(4))
            elif phase == 4:  # Hold
                self.animate_breathing("hold", 240, 150, ("#f1c40f", "#f39c12"), "Hold")
                self.animation_id = self.window.after(4000, lambda: cycle(5))
            else:  # Right nostril exhale
                self.animate_breathing("exhale", 240, 150, ("#1abc9c", "#16a085"), "Right nostril")
                self.animation_id = self.window.after(4000, lambda: cycle(0))
        
        cycle()