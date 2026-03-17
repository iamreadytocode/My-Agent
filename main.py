import flet as ft
from views.login_view import LoginView
from views.onboarding_view import OnboardingView
from views.chat_view import ChatView
import os

def main(page: ft.Page):
    page.title = "Viki AI"
    # Widened for the split-screen layout
    page.window_width = 1000  
    page.window_height = 650
    page.theme_mode = "dark"

    def route_change(e):
        print(f"🔄 [Router] Navigating to: {page.route}")
        page.views.clear()
        
        if page.route == "/":
            print("📦 [Router] Loading LoginView...")
            page.views.append(LoginView(page))
            
        elif page.route == "/onboarding":
            print("📦 [Router] Loading OnboardingView...")
            page.views.append(OnboardingView(page))
            
        elif page.route == "/chat":
            print("📦 [Router] Loading ChatView...")
            chat_view = ChatView(page)              
            page.views.append(chat_view)            
            
            # 🚨 THE FIX: Force the page to draw the view FIRST
            page.update()                           
            
            # Now that it actually exists on the screen, start the animation!
            chat_view.trigger_bg_animation(None)    
            return  # Exit the function so we don't double-update
            
        page.update()
        print("✅ [Router] Screen updated and rendered!")

    # Assign the router
    page.on_route_change = route_change
    
    # ==========================================
    # 🚨 SMART AUTH: CHECK FOR SAVED SESSION
    # ==========================================
    saved_user = None
    if os.path.exists("session.txt"):
        with open("session.txt", "r") as f:
            saved_user = f.read().strip()
    
    if saved_user:
        print(f"🔓 Auto-login successful for: {saved_user}")
        page.route = "/chat"
    else:
        print("🔒 No saved session found. Loading LoginView...")
        page.route = "/"
        
    # Trigger the initial route manually
    route_change(None)

if __name__ == "__main__":
    # Also fixed your DeprecationWarning here!
    ft.run(main)