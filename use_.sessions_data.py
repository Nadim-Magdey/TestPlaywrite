# from playwright.sync_api import sync_playwright
# import os
#
# # --- CONFIGURATION (CHANGE THESE FOR EACH NEW ACCOUNT) ---
# MASTER_AUTH_FILE = "master_auth_key.json"  # The key created in Script 1
# NEW_ACCOUNT_EMAIL = "new.user.20253@gmail.com"  # The actual email for the NEW account
# # ⬇️ The final, unique file for this new user:
# NEW_ACCOUNT_AUTH_FILE = f"auth_files/{NEW_ACCOUNT_EMAIL}_auth.json"
#
#
# # --------------------------------------------------------
#
# def authenticate_new_account():
#     print(f"--- 2. AUTHENTICATING NEW ACCOUNT: {NEW_ACCOUNT_EMAIL} ---")
#
#     # Check for the master key
#     if not os.path.exists(MASTER_AUTH_FILE):
#         print(f"ERROR: Master Auth file '{MASTER_AUTH_FILE}' not found. Run Script 1 first!")
#         return
#
#     with sync_playwright() as p:
#         # 1. Launch a STANDARD, fast browser
#         browser = p.chromium.launch(headless=False)
#
#         # 2. Load the Master Key to pass the initial 'secure browser' check
#         context = browser.new_context(storage_state=MASTER_AUTH_FILE)
#
#         # 1. Block large, non-essential files to save bandwidth/rendering time
#         context.route(
#             "**/*.{png,jpg,jpeg,webp,svg,gif,woff,woff2,ttf,mp4,webm}",
#             lambda route: route.abort()
#         )
#
#         # Add stealth scripts (optional here, but keeps defenses up)
#         context.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
#         """)
#
#         page = context.new_page()
#
#         # 3. Perform the actual login for the NEW account
#         page.goto("https://accounts.google.com/signin", wait_until="domcontentloaded")
#
#         print("\n\n🛑 Manually enter username, password, and 2FA for the NEW account.")
#
#         # You need to manually perform the login steps here for the new user.
#         input("✅ Press Enter AFTER the NEW account is fully logged in...")
#
#         # 4. SAVE the new, unique session state
#         os.makedirs("auth_files", exist_ok=True)
#         context.storage_state(path=NEW_ACCOUNT_AUTH_FILE)
#         print(f"\n✅ New account state SAVED to {NEW_ACCOUNT_AUTH_FILE}")
#
#         browser.close()
#
#
# if __name__ == '__main__':
#     authenticate_new_account()
from playwright.sync_api import sync_playwright
import os

# --- CONFIGURATION (CHANGE THESE FOR EACH NEW ACCOUNT) ---
MASTER_AUTH_FILE = "master_auth_key.json"
NEW_ACCOUNT_EMAIL = "reply162@pdfffs.com"
NEW_ACCOUNT_AUTH_FILE = f"auth_files/{NEW_ACCOUNT_EMAIL}_auth.json"


# --------------------------------------------------------

def authenticate_new_account():
    print(f"--- 2. AUTHENTICATING NEW ACCOUNT: {NEW_ACCOUNT_EMAIL} (Optimized) ---")

    if not os.path.exists(MASTER_AUTH_FILE):
        print(f"ERROR: Master Auth file '{MASTER_AUTH_FILE}' not found. Run Script 1 first!")
        return

    with sync_playwright() as p:
        # 1. LAUNCH CLEAN AND HEADFUL (As requested for testing)
        # Removed all custom arguments for optimization (e.g., --start-maximized)
        browser = p.chromium.launch(headless=False,
                                    args=["--use-gl=swiftshader"] )

        # 2. LOAD MASTER KEY
        context = browser.new_context(
            storage_state=MASTER_AUTH_FILE
        )

        # 3. MINIMAL JAVASCRIPT STEALTH (Only the absolute essential)
        # This reduces CPU load compared to the full stealth suite.
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()

        # first page
        page.goto("https://mail.google.com", wait_until="domcontentloaded")

        # page.goto("https://accounts.google.com/Logout", wait_until="domcontentloaded")
        # page.wait_for_timeout(1000)
        # page.goto(
        #     "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Ftwosv%3Fpli%3D1%26rapt%3DAEjHL4MbHS9Ks5mbZqQzIwUaJQAc1_CRqh6sxPz0pREIifauyxUUisVbgi7GWczcV8ubHN5nklMSolNxng0lT-C3lxT9iAQ-fg9p9JH_pOUC0DVvRPtR4fM&dsh=S1864866673%3A1759638804548635&followup=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Ftwosv%3Fpli%3D1%26rapt%3DAEjHL4MbHS9Ks5mbZqQzIwUaJQAc1_CRqh6sxPz0pREIifauyxUUisVbgi7GWczcV8ubHN5nklMSolNxng0lT-C3lxT9iAQ-fg9p9JH_pOUC0DVvRPtR4fM&ifkv=AfYwgwWfujn8J4TcVH5IO_HIHH6mHXlVd3h40XnjUaKfkwEZzCcDSVTKFNgx3loL1HqJyfDcbQcchQ&osid=1&passive=1209600&rart=ANgoxcfQotkt7oQGVKpnv2SIOqzvSeNeEZsFqkhnJMHgW0IwWlwXi67fzz0MhvnmvLNnOv7pw9zhxidWmE4Bk931s0KNGXZgEKyvPjtqLD1jB_BtAYy_Dg0&flowName=GlifWebSignIn&flowEntry=ServiceLogin", wait_until="domcontentloaded")
        # page.get_by_role("textbox", name="Email or phone").click()
        # page.get_by_role("textbox", name="Email or phone").fill(NEW_ACCOUNT_EMAIL)
        # page.get_by_role("button", name="Next").click()


        print("\n\n🛑 Manually enter username, password, and 2FA for the NEW account.")

        # 5. NO UNNECESSARY EVENT LISTENERS
        # Removed any debugging event listeners (page.on(...)) to minimize communication overhead.

        # Manual login steps here...
        input("✅ Press Enter AFTER the NEW account is fully logged in...")

        # 6. SAVE the new, unique session state
        os.makedirs("auth_files", exist_ok=True)
        context.storage_state(path=NEW_ACCOUNT_AUTH_FILE)
        print(f"\n✅ New account state SAVED to {NEW_ACCOUNT_AUTH_FILE}")

        browser.close()


if __name__ == '__main__':
    authenticate_new_account()


