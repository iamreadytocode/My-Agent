import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# Setup
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose"
]

def main():
    print(f"🕵️‍♂️ SEARCHING: {os.getcwd()}")
    
    # 1. LIST ALL FILES (Prove what exists)
    files = os.listdir()
    print("📂 Files found in folder:")
    for f in files:
        if "token" in f or "json" in f:
            print(f"   - {f}")

    # 2. FORCE DELETE TOKEN
    if "token.json" in files:
        print("\n⚠️  FOUND IT! 'token.json' exists.")
        try:
            # Check content to confirm corruption
            with open("token.json", "r") as f:
                content = f.read(10)
                print(f"   File starts with: {content} (If this is '{{', it is corrupted)")
        except:
            print("   (Could not read content, binary format?)")
            
        print("🗑️  Deleting 'token.json' now...")
        os.remove("token.json")
        print("✅  Deleted.")
    else:
        print("\n✅  Good. No 'token.json' found.")

    # 3. AUTHENTICATE
    if "credentials.json" not in files:
        print("\n❌ STOP: 'credentials.json' is missing.")
        print("   Please rename 'client_secrets.json' to 'credentials.json'")
        return

    print("\n🚀 Starting Login with 'credentials.json'...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        
        # 4. SAVE CORRECTLY (As Pickle Binary)
        with open("token.json", "wb") as token:
            pickle.dump(creds, token)
        print("\n🎉 SUCCESS! A new, binary 'token.json' has been forged.")
        print("👉 You can now run your agent test.")
        
    except Exception as e:
        print(f"\n❌ Login Failed: {str(e)}")

if __name__ == "__main__":
    main()