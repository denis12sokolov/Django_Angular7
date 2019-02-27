import os
import platform

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, FirefoxProfile
from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.chrome.options import Options as chrome_options


def hide_webdriver(driver):
    driver.execute_script("""const setProperty = () => {
        Object.defineProperty(navigator, "languages", {
            get: function() {
                return ["en-US", "en", "es"];
            }
        });

        // Overwrite the `plugins` property to use a custom getter.
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });

        // Pass the Webdriver test
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined,
        });
    };
    setProperty();""")


def get_page_by_selenium(url):
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    if platform.system() == "Linux":
        path = r"./driver/chromedriver"
    else:
        path = r"./driver/chromedriver_mac"
    driver = webdriver.Chrome(path, desired_capabilities=caps)
    driver.implicitly_wait(1)
    driver.get(url)
    return driver


def get_chrome_driver():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    options = chrome_options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    if os.environ.get("DEV"):
        options.add_argument("--proxy-server=socks5://127.0.0.1:8050")
    options.add_argument('start-maximized')
    options.add_argument(f'user-agent={user_agent}')
    path = os.path.dirname(__file__)
    if platform.system() == "Linux":
        path = os.path.join(path, r"driver/chromedriver")
    else:
        path = os.path.join(path, r"driver/chromedriver_mac")
    driver = webdriver.Chrome(executable_path=path, desired_capabilities=caps, chrome_options=options)
    driver.set_window_size(1920, 1080)
    hide_webdriver(driver)
    return driver


def get_firefox_driver():
    profile = FirefoxProfile()
    profile.set_preference('browser.cache.disk.enable', False)
    profile.set_preference('browser.cache.memory.enable', False)
    profile.set_preference('browser.cache.offline.enable', False)
    profile.set_preference('network.cookie.cookieBehavior', 2)
    if os.environ.get("DEV"):
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", 8050)
        profile.set_preference("network.proxy.socks_version", 5)
    profile.update_preferences()
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "none"
    options = firefox_options()
    options.headless = True
    options.add_argument('start-maximized')
    path = os.path.dirname(__file__)
    if platform.system() == "Linux":
        path = os.path.join(path, r"driver/geckodriver")
    else:
        path = os.path.join(path, r"driver/geckodriver_mac")
    driver = webdriver.Firefox(executable_path=path, firefox_options=options, desired_capabilities=caps, firefox_profile=profile)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(1)
    return driver
