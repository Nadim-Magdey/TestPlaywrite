from playwright.sync_api import sync_playwright

# --- CONFIGURATION (RUN ONCE) ---
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_path = r"initial_login_profile"  # TEMPORARY, DISPOSABLE profile folder
MASTER_AUTH_FILE = "master_auth_key.json"  # THE FILE TO REUSE FOR ALL ACCOUNTS

# -------------------------------

def create_master_auth_file():
    print("--- 1. CREATING MASTER AUTH KEY (Run ONLY Once) ---")

    with sync_playwright() as p:
        # Launch the trusted persistent context to pass security checks
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            executable_path=chrome_path,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )

        # Inject JavaScript stealth code here... (omitted for brevity)
        # You must manually log in and complete 2FA for ONE account during this run!

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://mail.google.com")

        print("\n\n🛑 MANUALLY LOG IN FOR A *SINGLE* ACCOUNT TO GENERATE THE KEY.")
        input("✅ Press Enter AFTER you are fully logged in...")

        # SAVE THE AUTHENTICATION PROOF
        browser.storage_state(path=MASTER_AUTH_FILE)
        print(f"\n✅ MASTER AUTH KEY saved to {MASTER_AUTH_FILE}")

        browser.close()



if __name__ == '__main__':
    create_master_auth_file()
