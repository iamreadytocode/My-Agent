import flet as ft
from viki_engine import get_viki_response, start_voice_interaction
import os
# ==========================================
# 1. THE GLASSMORPHISM CHAT BUBBLE
# ==========================================
class ChatMessage(ft.Row):
    def __init__(self, text: str, is_user: bool = False):
        super().__init__()
        self.text = text
        self.is_user = is_user
        
        self.alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        avatar_initial = "U" if is_user else "V"
        avatar_bg = ft.Colors.BLUE_ACCENT_700 if is_user else ft.Colors.PURPLE_ACCENT_700
        
        # FIXED: Removed 'shadow' property which CircleAvatar does not support
        avatar = ft.CircleAvatar(
            content=ft.Text(avatar_initial, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=avatar_bg,
            radius=18
        )
        
        if self.is_user:
            msg_content = ft.Text(self.text, color=ft.Colors.WHITE, selectable=True)
        else:
            msg_content = ft.Markdown(
                self.text, 
                selectable=True, 
                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
                code_theme="atom-one-dark" 
            )

        bubble = ft.Container(
            content=msg_content,
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE if is_user else ft.Colors.DEEP_PURPLE_200),
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE if is_user else ft.Colors.PURPLE_ACCENT_200)),
            border_radius=ft.border_radius.all(20),
            padding=ft.padding.all(15),
            width=500 if not is_user else None,
            blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP)
        )

        if self.is_user:
            self.controls = [bubble, avatar]
        else:
            self.controls = [avatar, bubble]
    

# ==========================================
# 2. THE MAIN VIEW WITH ANIMATED BACKGROUND
# ==========================================
class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/chat", padding=0)
        
        self.color_set_1 = ["#09090e", "#1a1025", "#09090e"] 
        self.color_set_2 = ["#09090e", "#0d1b2a", "#09090e"] 
        self.gradient_state = True

        # --- THE BREATHING BACKGROUND ---
        self.animated_bg = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                # FIXED: Bypassed buggy Flet modules and used raw coordinates
                begin=ft.Alignment(-1.0, -1.0), # Top-Left
                end=ft.Alignment(1.0, 1.0),     # Bottom-Right
                colors=self.color_set_1
            ),
            # FIXED: Used an integer duration to bypass Animation class bugs
            animate=4000, 
            on_animation_end=self.trigger_bg_animation
        )
        # --- FOREGROUND UI ---
        self.appbar = ft.AppBar(
            # Your awesome custom title
            title=ft.Row([
                ft.Icon(ft.Icons.FINGERPRINT, color=ft.Colors.PURPLE_ACCENT_400),
                ft.Text("Viki OS Core", weight=ft.FontWeight.W_800, color=ft.Colors.WHITE),
                ft.Container(
                    bgcolor=ft.Colors.GREEN_ACCENT_400, 
                    width=8, height=8, 
                    border_radius=4, 
                    margin=ft.margin.only(left=5),
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREEN_ACCENT_400)
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            center_title=False,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            elevation=0,
            
            # The Logout Button attached to the right side!
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT, 
                    icon_color=ft.Colors.RED_400, 
                    tooltip="Sign Out", 
                    on_click=self.logout
                ),
                ft.Container(width=10) # Breathing room on the right side
            ]
        )
        self.chat_history = ft.ListView(
            expand=True, 
            spacing=20, 
            auto_scroll=True,
            padding=30
        )
        self.chat_history.controls.append(ChatMessage("Neural link established. How can I assist you today?", is_user=False))

        # --- GLASSMORPHISM INPUT BAR ---
        self.text_input = ft.TextField(
            hint_text="Initialize command...",
            hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
            expand=True,
            on_submit=self.send_text_message,
            border="none",
            bgcolor=ft.Colors.TRANSPARENT,
            content_padding=ft.padding.only(left=20, top=15, bottom=15),
            color=ft.Colors.WHITE
        )
        
        self.send_btn = ft.IconButton(icon=ft.Icons.SEND_ROUNDED, icon_color=ft.Colors.BLUE_ACCENT_200, on_click=self.send_text_message)
        self.mic_btn = ft.IconButton(icon=ft.Icons.MIC_NONE_ROUNDED, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), on_click=self.send_voice_message)
        
        self.input_container = ft.Container(
            content=ft.Row([self.text_input, self.send_btn, self.mic_btn], spacing=0),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            border_radius=30,
            margin=ft.margin.only(left=30, right=30, bottom=30),
            padding=ft.padding.only(right=5),
            blur=ft.Blur(15, 15, ft.BlurTileMode.CLAMP)
        )

        # --- LAYOUT STACK ---
        self.main_stack = ft.Stack(
            controls=[
                self.animated_bg,
                ft.Column([
                    self.appbar,
                    self.chat_history,
                    self.input_container
                ], expand=True)
            ],
            expand=True
        )

        self.controls.append(self.main_stack)
    
    def logout(self, e):
        print("🔒 Initiating logout sequence...")
        
        # 1. Delete the session file
        if os.path.exists("session.txt"):
            os.remove("session.txt")
            
        # 2. Aggressively clear Flet's internal memory
        e.page.views.clear()
        
        # 3. Force the route back to login
        e.page.go("/")

    def trigger_bg_animation(self, e=None):
        self.gradient_state = not self.gradient_state
        self.animated_bg.gradient.colors = self.color_set_2 if self.gradient_state else self.color_set_1
        self.animated_bg.update()

    def send_text_message(self, e):
        user_text = self.text_input.value.strip()
        if not user_text:
            return
            
        self.chat_history.controls.append(ChatMessage(user_text, is_user=True))
        self.text_input.value = ""
        e.page.update()
        
        thinking_bubble = ChatMessage("⚙️ *Synthesizing response...*", is_user=False)
        self.chat_history.controls.append(thinking_bubble)
        e.page.update()
        
        response = get_viki_response(user_text)
        
        self.chat_history.controls.remove(thinking_bubble)
        self.chat_history.controls.append(ChatMessage(response, is_user=False))
        e.page.update()

    def send_voice_message(self, e):
        self.mic_btn.icon_color = ft.Colors.RED_ACCENT_400
        self.mic_btn.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.RED)
        self.text_input.disabled = True
        listening_bubble = ChatMessage("🎤 *Audio feed active...*", is_user=False)
        self.chat_history.controls.append(listening_bubble)
        e.page.update()
        
        user_said, response = start_voice_interaction()
        
        self.mic_btn.icon_color = ft.Colors.WHITE
        self.mic_btn.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
        self.text_input.disabled = False
        self.chat_history.controls.remove(listening_bubble)
        
        if user_said and user_said != "Voice Error":
            self.chat_history.controls.append(ChatMessage(user_said, is_user=True))
            
        self.chat_history.controls.append(ChatMessage(response, is_user=False))
        e.page.update()