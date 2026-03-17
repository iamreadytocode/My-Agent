import flet as ft
import os
import requests
from firebase_admin import firestore
# 🚨 PASTE YOUR FIREBASE WEB API KEY HERE
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/", padding=0, bgcolor="#15151a")
        
        # 🚨 THE FIX: Re-connect the view to your Firestore database!
        self.db = firestore.client(database_id="d4as1")
        
        # --- INPUT FIELDS ---
        input_style = {
            "border": ft.InputBorder.NONE,
            "bgcolor": "#2a2b36",
            "border_radius": 10,
            "content_padding": ft.padding.only(left=20, top=15, bottom=15, right=20),
            "color": ft.Colors.WHITE,
        }

        self.email = ft.TextField(hint_text="name@university.edu", **input_style)
        
        # Changed Username to a secure Password field
        self.password = ft.TextField(
            hint_text="••••••••", 
            password=True, 
            can_reveal_password=True, 
            **input_style
        )
        
        # Added a text widget to display login errors directly on the UI
        self.error_text = ft.Text("", color=ft.Colors.RED_400, size=13)

        # --- LEFT SIDE: HERO GRADIENT & BRANDING ---
        left_side = ft.Container(
            expand=5, 
            # We use the raw coordinates to avoid Flet alignment bugs
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, -1.0),
                end=ft.Alignment(1.0, 1.0),
                colors=["#09090e", "#1a1025", "#09090e"]
            ),
            padding=ft.padding.all(50),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.FINGERPRINT, color=ft.Colors.PURPLE_ACCENT_400, size=40),
                    ft.Text("VIKI OS", size=24, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
                ]),
                ft.Container(height=40),
                ft.Text("Initialize your\ndigital ecosystem.", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(height=10),
                ft.Text(
                    "The centralized AI operating platform to automate, orchestrate, and manage your daily engineering workflows.",
                    size=16, color=ft.Colors.WHITE70
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        # --- RIGHT SIDE: LOGIN FORM ---
        right_side = ft.Container(
            expand=5, 
            bgcolor="#1e1e24", 
            padding=ft.padding.all(60),
            content=ft.Column([
                ft.Text("Welcome back", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Initialize credentials to access the core.", size=14, color=ft.Colors.WHITE_54),
                ft.Container(height=30),
                
                ft.Text("Email Address", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE_70),
                self.email,
                ft.Container(height=10),
                
                ft.Text("Password", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE_70),
                self.password,
                
                # Error text sits right below the password field
                ft.Container(content=self.error_text, margin=ft.margin.only(top=5, bottom=5)), 
                
                ft.ElevatedButton(
                    "Initialize Session", 
                    width=float('inf'), 
                    height=50, 
                    on_click=self.handle_auth, 
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_ACCENT_700, 
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START)
        )

        self.controls.append(ft.Row([left_side, right_side], expand=True, spacing=0))

    def handle_auth(self, e):
        email_val = self.email.value.strip()
        password_val = self.password.value.strip()
        
        if not email_val or not password_val:
            self.error_text.value = "Error: Please enter both email and password."
            e.page.update()
            return

        self.error_text.value = "Authenticating..."
        self.error_text.color = ft.Colors.BLUE_400
        e.page.update()

        # 1. TRY TO SIGN IN VIA FIREBASE API
        login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {"email": email_val, "password": password_val, "returnSecureToken": True}
        
        response = requests.post(login_url, json=payload).json()
        
        # Automatically generate a username from the email
        username_val = email_val.split('@')[0]
        
        # --- ERROR HANDLING & SIGN UP ---
        if "error" in response:
            error_msg = response["error"]["message"]
            
            # Catch both the old error and Google's new security error
            if error_msg in ["EMAIL_NOT_FOUND", "INVALID_LOGIN_CREDENTIALS"]:
                self.error_text.value = "Checking credentials..."
                e.page.update()
                
                # Attempt to Sign Up
                signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
                signup_response = requests.post(signup_url, json=payload).json()
                
                if "error" in signup_response:
                    signup_error = signup_response['error']['message']
                    self.error_text.color = ft.Colors.RED_400
                    
                    # If Sign Up fails because they exist, they just typed the wrong password!
                    if signup_error == "EMAIL_EXISTS":
                        self.error_text.value = "Incorrect password. Please try again."
                    else:
                        self.error_text.value = f"Error: {signup_error.replace('_', ' ')}"
                    e.page.update()
                    return
                
                # Successful Sign Up! Save to Firestore
                user_ref = self.db.collection("users").document(username_val)
                user_ref.set({
                    "email": email_val,
                    "username": username_val,
                    "onboarding_complete": False
                })
                
                with open("session.txt", "w") as f:
                    f.write(username_val)
                    
                e.page.go("/onboarding")
                return
                
            # Handle bad email formats
            self.error_text.color = ft.Colors.RED_400
            if error_msg == "INVALID_EMAIL":
                self.error_text.value = "Invalid email format."
            else:
                self.error_text.value = f"Error: {error_msg.replace('_', ' ')}"
            
            e.page.update()
            return

        # --- SIGN IN SUCCESSFUL ---
        print(f"✅ User {username_val} signed in successfully!")
        
        # Check Firestore to see if they completed onboarding
        user_ref = self.db.collection("users").document(username_val)
        user_doc = user_ref.get()
        
        with open("session.txt", "w") as f:
            f.write(username_val)
            
        if user_doc.exists and user_doc.to_dict().get("onboarding_complete", False):
            e.page.go("/chat")
        else:
            e.page.go("/onboarding")