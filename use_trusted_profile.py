from idlelib import browser

from playwright.sync_api import sync_playwright

#basic variables
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_path = "initial_login_profile"
context = None
Emails = list()

probe_script = r"""
() => {
  // safe helpers
  const tryGet = (fn, fallback=null) => {
    try { return fn(); } catch (e) { return fallback; }
  };
  
  // WebGL info
  const webgl = tryGet(() => {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) return null;
    return {
      renderer: tryGet(() => gl.getParameter(gl.RENDERER)),
      vendor: tryGet(() => gl.getParameter(gl.VENDOR)),
      version: tryGet(() => gl.getParameter(gl.VERSION)),
      shadingLanguageVersion: tryGet(() => gl.getParameter(gl.SHADING_LANGUAGE_VERSION))
    };
  });

  // Canvas fingerprint basic test (not full hash)
  const canvasFP = tryGet(() => {
    const c = document.createElement('canvas');
    const ctx = c.getContext('2d');
    ctx.textBaseline = "top";
    ctx.font = "14px 'Arial'";
    ctx.fillStyle = "#f60";
    ctx.fillRect(125,1,62,20);
    ctx.fillStyle = "#069";
    ctx.fillText("playwright-test", 2, 15);
    return c.toDataURL();
  });

  // Audio context availability
  const audio = tryGet(() => {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return null;
    const actx = new AudioCtx();
    const sampleRate = actx.sampleRate || null;
    actx.close && actx.close();
    return { sampleRate };
  });

  // media devices
  const mediaDevices = tryGet(() => navigator.mediaDevices && navigator.mediaDevices.enumerateDevices
    ? navigator.mediaDevices.enumerateDevices().then(list => list.map(d => ({kind:d.kind, label: d.label||'', deviceId: d.deviceId})))
    : null
  );

  // permissions query helper (non-blocking)
  const perm = (name) => tryGet(() => navigator.permissions && navigator.permissions.query
    ? navigator.permissions.query({name}).then(s => s.state).catch(_ => null)
    : null);

  // Basic synchronous properties
  const out = {
    timestamp: Date.now(),
    url: location.href,
    userAgent: tryGet(() => navigator.userAgent, null),
    webdriver: tryGet(() => navigator.webdriver, null),
    languages: tryGet(() => navigator.languages || null, null),
    plugins_length: tryGet(() => navigator.plugins && navigator.plugins.length || 0, null),
    mimeTypes_length: tryGet(() => navigator.mimeTypes && navigator.mimeTypes.length || 0, null),
    chrome_present: tryGet(() => !!window.chrome, null),
    outerWidth: tryGet(() => window.outerWidth, null),
    outerHeight: tryGet(() => window.outerHeight, null),
    innerWidth: tryGet(() => window.innerWidth, null),
    innerHeight: tryGet(() => window.innerHeight, null),
    screen_width: tryGet(() => screen.width, null),
    screen_height: tryGet(() => screen.height, null),
    screen_availWidth: tryGet(() => screen.availWidth, null),
    screen_availHeight: tryGet(() => screen.availHeight, null),
    devicePixelRatio: tryGet(() => window.devicePixelRatio, null),
    hasFocus: tryGet(() => document.hasFocus(), null),
    visibilityState: tryGet(() => document.visibilityState, null),
    visibilityHidden: tryGet(() => document.hidden, null),
    cookiesEnabled: tryGet(() => navigator.cookieEnabled, null),
    maxTouchPoints: tryGet(() => navigator.maxTouchPoints, null),
    hardwareConcurrency: tryGet(() => navigator.hardwareConcurrency, null),
    userAgentData: tryGet(() => navigator.userAgentData ? {brands: navigator.userAgentData.brands, mobile: navigator.userAgentData.mobile} : null, null),
    connection: tryGet(() => navigator.connection ? {effectiveType: navigator.connection.effectiveType, downlink: navigator.connection.downlink} : null, null),
    // feature availability
    webgl,
    canvasFP,
    audio,
    // asynchronous results will be returned as promises; gather them:
    mediaDevicesPromise: mediaDevices,
    permissionsPromises: {
       notifications: perm('notifications'),
       camera: perm('camera'),
       microphone: perm('microphone')
    }
  };

  // If there are promises, return them as resolved values
  return Promise.all([
    Promise.resolve(out),
    mediaDevices ? mediaDevices : Promise.resolve(null),
    perm('notifications'), perm('camera'), perm('microphone')
  ]).then(([o, media, n, c, m]) => {
    o.mediaDevices = media;
    o.permissions = {notifications: n, camera: c, microphone: m};
    delete o.mediaDevicesPromise;
    delete o.permissionsPromises;
    return o;
  }).catch(e => ( { error: String(e) } ));
}
"""

def handle_speed_pump(page):
    if "speedbump/gaplustos" in page.url:
        page.locator('input#confirm').click()

def fill_emails(path):
    with open(path, "r") as f:
        for line in f:
            splitted_line = line.split(",")
            email = splitted_line[2]
            password = splitted_line[3]
            Emails.append((email, password))

def write_result(email, password, passk_key):
    with open("result.txt", "a") as f:
        f.write(f"{email},{password},{passk_key}\n")

def create_context(p):
    global context
    """
    generate new context
    :param p: sync_playwright object
    :return: new context
    """
    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        executable_path=chrome_exe,
        headless=False,
        args=[
            "--start-maximized", "--disable-blink-features=AutomationControlled",
            "--disable-infobars",  "--no-default-browser-check", "--no-first-run"]
    )

def login(page, email, password):
    """
    login to page using email, password
    :param page:
    :return:
    """
    page.goto("https://mail.google.com")
    print("🔃 Logging out of any current Gmail session...")

    # logout
    page.goto("https://accounts.google.com/Logout", wait_until="load")

    #  use another account
    page.wait_for_selector("text=Use another account", timeout=10000)
    page.locator("text=Use another account").click()
    page.wait_for_url("**/identifier*", timeout=10000)

    # fill email
    page.get_by_role("textbox", name="Email or phone").fill(email)
    page.get_by_role("button", name="Next").click()

    # fill password
    page.wait_for_selector('input[type="password"]', timeout=10000)
    page.locator('input[type="password"]').fill(password)
    page.get_by_role("button", name="Next").click()

    try:
        # confirm greeting
        page.wait_for_selector("#confirm", timeout=10000)
        page.locator("#confirm").click()
    except:
        page.screenshot(path="screenshot.png")

def enable_2step_auth(page):
    """
    enable two step varification
    :param page:
    :return: None
    """
    # page.wait_for_selector("#acceptButton", timeout=10000)
    page.goto(
        "https://myaccount.google.com/signinoptions/twosv?pli=1&rapt=AEjHL4O5yERC3NK2QztSX5b7iu7e70zuWzCBgzNJk071Cm2__PrQxd_9ASPZtvt34i2j_E9O1JDVtoR81Zfq5s8fB6lCG_U_gKNYbg_RrR565TJuCfrrxUw?",
        wait_until="load")

    #handle speedpumb
    # handle speedpump
    handle_speed_pump(page)


    # page.locator('button[jsname="Pr7Yme"]').click()
    page.locator('button[jscontroller="O626Fe"][jsname="Pr7Yme"]').click()

    # fill phone number
    page.wait_for_selector("#c5")
    page.locator("#c5").fill("12124567890")

    # first click
    page.wait_for_selector('button[jscontroller="O626Fe"][data-mdc-dialog-action="OCpkoe"]', timeout=10000)
    page.locator('button[jscontroller="O626Fe"][data-mdc-dialog-action="OCpkoe"]').click()

    # second click
    page.wait_for_selector('button[jscontroller="O626Fe"][data-mdc-dialog-action="x8hlje"]', timeout=10000)
    page.locator('button[jscontroller="O626Fe"][data-mdc-dialog-action="x8hlje"]').click()

    # third click
    page.wait_for_selector('button[jscontroller="O626Fe"][data-mdc-dialog-action="AHldd"]', timeout=10000)
    page.locator('button[jscontroller="O626Fe"][data-mdc-dialog-action="AHldd"]').click()


def get_pass_key(page):
    """
    extract passkey
    :param page:
    :return: (string) pEmail App Passkey
    """
    # app pass page
    page.goto("https://myaccount.google.com/apppasswords", wait_until="load")

    result = page.evaluate("""
    () => ({
      webdriver: navigator.webdriver,
      visibility: document.visibilityState,
      hasFocus: document.hasFocus(),
      plugins: navigator.plugins.length,
      languages: navigator.languages,
      chrome: !!window.chrome,
      width: window.outerWidth,
      height: window.outerHeight,
    })
    """)
    print("runtime properties :")
    print(result)
    # fill text(name)
    page.wait_for_selector("#i4", timeout=10000).fill("Azokels")

    # Wait until button exists and visible
    buttons = page.locator('button[jscontroller="O626Fe"]:visible')
    buttons.nth(1).click()

    # get app passcode
    page.wait_for_selector("article")
    # Extract and join all span text inside the article
    pass_key = page.eval_on_selector_all(
        "article span",
        "spans => spans.map(s => s.textContent.trim()).join('')"
    )


    return pass_key


def Extract(email, password):
    global context
    """
    :param email:
    :return:
    """
    pass_key = None
    with sync_playwright() as p:
        create_context(p)

        page = context.pages[0] if context.pages else context.new_page()

        #hide automation flags
        page.add_init_script(
            """ 
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); 
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] }); 
            window.chrome = { runtime: {} }; 
            """)

        #read properties
        login(page, email, password)
        enable_2step_auth(page)
        pass_key = get_pass_key(page)

        context.close()

    return pass_key


if __name__ == '__main__':
    fill_emails("emails.txt")

    for email, password in Emails:
        try:
            pass_key = Extract(email, password)
            print(f"Done!, email: {email}, passkey: {pass_key}")
            write_result(email, pass_key, pass_key)
        except Exception as e:
            print("error with message: ",e)
            continue

