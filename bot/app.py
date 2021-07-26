"""
Entry point.
"""
from schedule import every, repeat, run_pending
import time

from absl import app
from absl import flags
from absl import logging

from bot.stages.config import create_chromedriver
from bot.stages.login import login_or_die
from bot.stages.interact import interact

FLAGS = flags.FLAGS

flags.DEFINE_bool('debug', True, 'Whether to run in debug mode.')
flags.DEFINE_string('bot_username', None, 'Pass in bot username (required)')
flags.DEFINE_string('bot_password', None, 'Pass in bot password (required)')

flags.register_validator('bot_username', lambda username: username and len(username) > 0,
                         message='Invalid username detected.')
flags.register_validator('bot_password', lambda pw: pw and len(pw) > 0, message='Invalid password detected.')

flags.mark_flags_as_required(['bot_username', 'bot_password'])


def main(argv):
    del argv  # Unused.
    _main()
    while True:
        run_pending()
        time.sleep(1)


# Bot flow should run periodically.
@repeat(every().hour)
def _main():
    logging.info(f'Started bot: {FLAGS.bot_username}')

    # Create the driver.
    driver = create_chromedriver()
    # Login.
    login_or_die(driver, FLAGS.bot_username, FLAGS.bot_password)
    # Interact and Scrape.
    time.sleep(5)
    interact(driver)
    # Cleanup.
    driver.quit()


if __name__ == '__main__':
    app.run(main)