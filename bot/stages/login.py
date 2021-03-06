"""
Module for logging into a Twitter account.
"""
import time
from typing import Union

from absl import logging, flags
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bot.stages.scraping_util import wait_for_page_load

FLAGS = flags.FLAGS

TWITTER_LOGIN_URL = 'https://twitter.com/login'

LOGIN_WAIT = 10
VERIFICATION_WAIT = 3

# The same phone number is used for all bots.
ACCOUNT_PHONE_NUMBER = '+60162289138'


def login_or_die(driver: Union[Firefox, Chrome], username: str, password: str):
    if not _login(driver, username, password):
        raise Exception('FAILURE. Log in was not successful.')


def _login(driver: Union[Firefox, Chrome], username: str, password: str) -> bool:
    try:
        driver.get(TWITTER_LOGIN_URL)

        e_username = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.visibility_of_element_located((By.NAME, 'session[username_or_email]')))
        e_pw = driver.find_element_by_name('session[password]')

        e_username.send_keys(username)
        e_pw.send_keys(password)
        e_pw.send_keys(Keys.RETURN)

        # Pass phone number in for verification
        time.sleep(VERIFICATION_WAIT)
        verify_phone_number(driver)

        if wait_for_page_load(driver):
            logging.info('Successfully logged in.')
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def verify_phone_number(driver: Union[Firefox, Chrome]) -> None:
    """Key-in phone number if phone number verification is presented."""
    try:
        # To ensure that the verification required is phone number verification.
        hint = driver.find_element_by_xpath("//strong[contains(text(), 'Your phone number ends in 38')]")

        # Find the element to fill the phone number detail.
        phone_number = driver.find_element_by_name('challenge_response')

        # Fill in the element with phone number.
        phone_number.send_keys(ACCOUNT_PHONE_NUMBER)

        # Hit enter.
        phone_number.send_keys(Keys.RETURN)
        logging.info('Keyed in phone number for verification.')
    except:
        # We didn't need to verify phone number, continue as normal.
        return
