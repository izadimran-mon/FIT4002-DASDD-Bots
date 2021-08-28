"""
Module for app configuration.
"""
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as GeckoOptions
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('path_to_chromedriver',
                    'webdrivers/chromedriver', 'Pass in the path to chromedriver.')
flags.DEFINE_string('path_to_geckodriver',
                    'webdrivers/geckodriver', 'Pass in the path to geckodriver.')

WEBDRIVER_OPTIONS = [
    '--disable-blink-features=AutomationControlled',
    # '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--window-size=1280x720',
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
]


def create_chromedriver() -> Chrome:
  op = ChromeOptions()
  for arg in WEBDRIVER_OPTIONS:
    op.add_argument(arg)
  return Chrome(executable_path=FLAGS.path_to_chromedriver, options=op)


def create_geckodriver() -> Firefox:
  op = GeckoOptions()
  for arg in WEBDRIVER_OPTIONS:
    op.add_argument(arg)
  return Firefox(executable_path=FLAGS.path_to_geckodriver, options=op)
