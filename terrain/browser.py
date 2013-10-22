"""
Browser set up for lettuce acceptance tests
"""
from lettuce import before, after, world
import logging
import os
from splinter.browser import Browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sauce_helpers import SauceRestApi
from env_helpers import BrowserEnv

LOGGER = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)
LOGGER.setLevel(logging.DEBUG)

LOGGER.info("Loading the lettuce acceptance testing terrain module...")

osenv = os.environ.copy()
world.BASE_URL = osenv.get('BASE_URL', 'https://www.edx.org')


def make_desired_capabilities(env):
    """
    Compose and return a DesiredCapabilities object with the
    browser attributes that you want.
    """
    # Figure out the starting desired capablilities from the browser choice.
    # Note that this pulls in the defaults for browserName,
    # version, platform, and javascriptEnabled from selenium.
    desired_capabilities = {}
    if env.selenium_browser == 'android':
        desired_capabilities = DesiredCapabilities.ANDROID
    elif env.selenium_browser == 'chrome':
        desired_capabilities = DesiredCapabilities.CHROME
    elif env.selenium_browser == 'firefox':
        desired_capabilities = DesiredCapabilities.FIREFOX
    elif env.selenium_browser == 'htmlunit':
        desired_capabilities = DesiredCapabilities.HTMLUNIT
    elif env.selenium_browser == 'iexplore':
        desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
    elif env.selenium_browser == 'iphone':
        desired_capabilities = DesiredCapabilities.IPHONE
    else:
        desired_capabilities = DesiredCapabilities.FIREFOX

    if env.selenium_version:
        desired_capabilities['version'] = env.selenium_version
    if env.selenium_platform:
        desired_capabilities['platform'] = env.selenium_platform

    if env.run_on_saucelabs:
        desired_capabilities['video-upload-on-pass'] = False
        desired_capabilities['sauce-advisor'] = False
        desired_capabilities['capture-html'] = True
        desired_capabilities['record-screenshots'] = True
        desired_capabilities['max-duration'] = 600
        desired_capabilities['public'] = 'public restricted'
        desired_capabilities['build'] = env.build_number
        desired_capabilities['name'] = env.job_name

    return desired_capabilities


def make_sauce_browser(env):
    """
    Start up the remote webdriver at SauceLabs.
    This expects SauceConnect to be running.
    """
    capabilities = make_desired_capabilities(env)
    url = "http://{user}:{key}@{host}:{port}/wd/hub".format(
        user=env.sauce_user_name,
        key=env.sauce_api_key,
        host=env.selenium_host,
        port=env.selenium_port
        )

    return Browser('remote', url=url, **capabilities)


def make_remote_browser(env):
    """
    Start up the remote webdriver.
    """
    capabilities = make_desired_capabilities(env)
    url = "http://{host}:{port}/wd/hub".format(
        host=env.selenium_host,
        port=env.selenium_port
        )

    return Browser('remote', url=url, **capabilities)


def make_local_browser(env):
    """
    Start up a local browser instance
    """
    return Browser(env.selenium_browser)


@before.all
def setup_and_launch_browser():
    """
    Use the environment variables to determine the type of
    browser we want, then launch the browser before executing the tests.
    """
    env = BrowserEnv()

    if env.run_on_saucelabs:
        world.browser = make_sauce_browser(env)
        env.session_id = world.browser.driver.session_id

        # As part of the post build activities, the Sauce plugin will parse the test result files.
        # It attempts to identify lines in the stdout or stderr that are in the following format:
        # SauceOnDemandSessionID=<some session id> job-name=<some job name>
        # so we need to output this to the console for jenkins to pick up.
        print 'SauceOnDemandSessionID={} job-name={}'.format(env.session_id, env.job_name)

    elif env.selenium_host and env.selenium_port:
        world.browser = make_remote_browser(env)

    else:
        world.browser = make_local_browser(env)

    world.browser.driver.implicitly_wait(30)

    # Absorb the contents of the env object into world
    # so it can be accessed later in the teardown.
    world.absorb(env, 'env')


@before.each_scenario
def reset_data(scenario):
    """
    Initialize the dict of scenario variables
    """
    world.absorb({}, 'scenario_dict')


@after.each_scenario
def clear_data(scenario):
    """
    Clean out the dict of scenario variables
    """
    world.spew('scenario_dict')


@after.all
def teardown(total):
    """
    Set the status at Sauce Labs and quit the browser.
    """
    if world.env.run_on_saucelabs:
        result = bool(total.features_passed == total.features_ran)
        sra = SauceRestApi(user=world.env.sauce_user_name, key=world.env.sauce_api_key)
        sra.update_job(world.env.session_id, {'passed': result})

    world.browser.quit()
