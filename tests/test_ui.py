from ui import UI, Page

def test_get_page():
    pages = {
        "home": Page(1.5, "Home page content"),
        "about": Page(1.2, "About page content")
    }
    ui = UI(pages)
    assert ui.get_page("home").load_time == 1.5
    assert ui.get_page("about").content == "About page content"
    assert ui.get_page("contact") is None

def test_is_responsive():
    pages = {
        "home": Page(1.5, "Home page content"),
        "about": Page(2.5, "About page content")
    }
    ui = UI(pages)
    assert ui.is_responsive("home") is True
    assert ui.is_responsive("about") is False
    assert ui.is_responsive("contact") is False

def test_is_clean():
    pages = {
        "home": Page(1.5, "Home page content"),
        "about": Page(1.2, "")
    }
    ui = UI(pages)
    assert ui.is_clean("home") is True
    assert ui.is_clean("about") is False
    assert ui.is_clean("contact") is False
