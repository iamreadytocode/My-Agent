import flet as ft
import os
import time
from firebase_admin import firestore

class OnboardingView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/onboarding", padding=0, bgcolor="#09090e")
        
        # Connect to your specific database
        self.db = firestore.client(database_id="d4as1")
        
        # --- STYLING ---
        input_style = {
            "border": ft.InputBorder.NONE,
            "bgcolor": ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            "border_radius": 10,
            "content_padding": ft.padding.all(15),
            "color": ft.Colors.WHITE,
            "text_size": 14,
        }
        
        # --- FITNESS FORM FIELDS ---
        self.age = ft.TextField(hint_text="Age", width=140, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
        self.gender = ft.Dropdown(
            hint_text="Gender", 
            width=140,
            options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female"), ft.dropdown.Option("Other")],
            **input_style
        )
        self.weight = ft.TextField(hint_text="Weight (kg)", width=140, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
        self.height = ft.TextField(hint_text="Height (cm)", width=140, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
        
        self.goals = ft.Dropdown(
            hint_text="Primary Goal",
            options=[
                ft.dropdown.Option("Stay Fit"),
                ft.dropdown.Option("Muscle Gain"),
                ft.dropdown.Option("Weight Loss"),
                ft.dropdown.Option("Endurance")
            ],
            **input_style
        )
        
        self.error_text = ft.Text("", color=ft.Colors.RED_400, size=13)

        # --- INTERACTIVE BUTTON ---
        self.loading_ring = ft.ProgressRing(width=20, height=20, stroke_width=2, color=ft.Colors.WHITE, visible=False)
        self.btn_text = ft.Text("Initialize Profile", size=16, weight=ft.FontWeight.BOLD)
        
        self.init_btn = ft.ElevatedButton(
            width=300,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_ACCENT_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=self.save_user_data,
            content=ft.Row([self.loading_ring, self.btn_text], alignment=ft.MainAxisAlignment.CENTER)
        )

        # --- THE GLASS CARD ---
        card = ft.Container(
            width=500,
            padding=ft.padding.all(40),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            blur=ft.Blur(15, 15, ft.BlurTileMode.CLAMP),
            content=ft.Column([
                ft.Icon(ft.Icons.FITNESS_CENTER, size=40, color=ft.Colors.PURPLE_ACCENT_400),
                ft.Text("Physical Calibration", size=28, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
                ft.Text("Provide your metrics so Viki can personalize your regimen.", color=ft.Colors.WHITE_54, size=13),
                ft.Container(height=20),
                
                ft.Row([self.age, self.gender], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                ft.Row([self.weight, self.height], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                self.goals,
                
                ft.Container(content=self.error_text, margin=ft.margin.only(top=10, bottom=10)),
                
                ft.Row([self.init_btn], alignment=ft.MainAxisAlignment.CENTER)
            ])
        )

        self.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1.0, -1.0),
                    end=ft.Alignment(1.0, 1.0),
                    colors=["#09090e", "#1a1025", "#09090e"]
                ),
                content=card
            )
        )

    def save_user_data(self, e):
        # 1. Validation
        if not all([self.age.value, self.gender.value, self.weight.value, self.height.value, self.goals.value]):
            self.error_text.value = "Error: Please complete all physical metrics."
            e.page.update()
            return
            
        self.error_text.value = ""

        # 2. Trigger Booting Animation
        self.loading_ring.visible = True
        self.btn_text.value = "Saving Metrics..."
        self.init_btn.disabled = True
        e.page.update()
        
        time.sleep(1.0) 

        # 3. Retrieve local session
        if not os.path.exists("session.txt"):
            self.error_text.value = "Session error. Please restart."
            self.loading_ring.visible = False
            self.btn_text.value = "Initialize Profile"
            self.init_btn.disabled = False
            e.page.update()
            return
            
        with open("session.txt", "r") as f:
            username = f.read().strip()
            
        # 4. Save to Firestore
        try:
            user_ref = self.db.collection("users").document(username)
            user_ref.set({
                "age": int(self.age.value),
                "gender": self.gender.value,
                "weight": float(self.weight.value),
                "height": float(self.height.value),
                "fitness_goal": self.goals.value,
                "onboarding_complete": True
            },
            merge=True)  # Use merge to avoid overwriting existing data
            
            # 5. Launch into Chat
            e.page.go("/chat")
        except Exception as ex:
            self.error_text.value = f"Database Error: {str(ex)}"
            self.loading_ring.visible = False
            self.btn_text.value = "Initialize Profile"
            self.init_btn.disabled = False
            e.page.update()