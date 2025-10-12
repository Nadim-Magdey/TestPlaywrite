from  bs4 import BeautifulSoup

def extract_key(html):
    """
    extract key from html
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")

    # Select all spans inside that structure
    letters = [span.get_text(strip=True) for span in soup.select("article span")]
    word = "".join(letters)

    return word


def wait_click_selector(page, **kwargs):
    pass

def wait_fill_selector(page, text, **kwargs):
    pass

def insert_init_script(code):
    pass

