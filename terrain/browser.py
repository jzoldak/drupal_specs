"""
Browser set up for drupal acceptance tests
"""

#pylint: disable=E1101
#pylint: disable=W0613

from lettuce import before, after, world
from splinter.browser import Browser
from logging import getLogger
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from uuid import uuid4
import os
from json import dumps
from base64 import encodestring
from requests import put


LOGGER = getLogger(__name__)
LOGGER.info("Loading the lettuce acceptance testing terrain file...")

SAUCE_ENABLED = os.environ.get('SAUCE_ENABLED')
SAUCE_USER = os.environ.get('SAUCE_USERNAME')
SAUCE_API_KEY = os.environ.get('SAUCE_API_KEY')
LOCAL_BROWSER_APP = os.environ.get('LOCAL_BROWSER', 'chrome')  # Used if running locally not in SauceLabs

world.SAUCE_ENABLED = SAUCE_ENABLED
world.BASE_URL = os.environ.get('BASE_URL')

DESIRED_CAPABILITIES = {
    'chrome': DesiredCapabilities.CHROME,
    'internetexplorer': DesiredCapabilities.INTERNETEXPLORER,
    'firefox': DesiredCapabilities.FIREFOX,
    'opera': DesiredCapabilities.OPERA,
    'iphone': DesiredCapabilities.IPHONE,
    'ipad': DesiredCapabilities.IPAD,
    'safari': DesiredCapabilities.SAFARI,
    'android': DesiredCapabilities.ANDROID
}

# All keys must be URL and JSON encodable
# PLATFORM-BROWSER-VERSION_NUM-DEVICE
ALL_CONFIG = {
    'Linux-chrome--': ['Linux', 'chrome', '', ''],
    'Windows 8-chrome--': ['Windows 8', 'chrome', '', ''],
    'Windows 7-chrome--': ['Windows 7', 'chrome', '', ''],
    'Windows XP-chrome--': ['Windows XP', 'chrome', '', ''],
    'OS X 10.8-chrome--': ['OS X 10.8', 'chrome', '', ''],
    'OS X 10.6-chrome--': ['OS X 10.6', 'chrome', '', ''],

    'Linux-firefox-23-': ['Linux', 'firefox', '23', ''],
    'Windows 8-firefox-23-': ['Windows 8', 'firefox', '23', ''],
    'Windows 7-firefox-23-': ['Windows 7', 'firefox', '23', ''],
    'Windows XP-firefox-23-': ['Windows XP', 'firefox', '23', ''],

    'OS X 10.8-safari-6-': ['OS X 10.8', 'safari', '6', ''],

    'Windows 8-internetexplorer-10-': ['Windows 8', 'internetexplorer', '10', ''],
}

SAUCE_INFO = ALL_CONFIG.get(os.environ.get('SAUCE_INFO', 'Linux-chrome--'))

def make_desired_capabilities():
    """
    Returns a DesiredCapabilities object corresponding to the environment sauce parameters
    """
    desired_capabilities = DESIRED_CAPABILITIES.get(SAUCE_INFO[1])
    desired_capabilities['platform'] = SAUCE_INFO[0]
    desired_capabilities['version'] = SAUCE_INFO[2]
    desired_capabilities['device-type'] = SAUCE_INFO[3]
    desired_capabilities['name'] = "Drupal Acceptance Test"
    desired_capabilities['build'] = uuid4().hex  # HACK fix later.
    desired_capabilities['video-upload-on-pass'] = False
    desired_capabilities['sauce-advisor'] = False
    desired_capabilities['record-screenshots'] = False
    desired_capabilities['selenium-version'] = "2.34.0"
    desired_capabilities['max-duration'] = 600
    desired_capabilities['public'] = 'private'
    return desired_capabilities


def set_job_status(jobid, passed=True):
    """
    Sets the job status on sauce labs
    """
    body_content = dumps({"passed": passed})
    config = {'username': SAUCE_USER, 'access-key': SAUCE_API_KEY}
    base64string = encodestring('{}:{}'.format(config['username'], config['access-key']))[:-1]
    result = put('http://saucelabs.com/rest/v1/{}/jobs/{}'.format(config['username'], world.jobid),
        data=body_content,
        headers={"Authorization": "Basic {}".format(base64string)})
    return result.status_code == 200


@before.all
def launch_browser():
    """
    Launch the browser once before executing the tests.
    """
    if not SAUCE_ENABLED:
        browser_driver = LOCAL_BROWSER_APP
        world.browser = Browser(browser_driver)
        world.browser.driver.set_window_size(1280, 1024)

    else:
        world.browser = Browser(
            'remote',
            url="http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(
                SAUCE_USER, SAUCE_API_KEY),
            **make_desired_capabilities()
        )

    world.absorb(world.browser.driver.session_id, 'jobid')
    world.browser.driver.implicitly_wait(30)

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
def teardown_browser(total):
    """
    Quit the browser after executing the tests.
    """
    if SAUCE_ENABLED:
        set_job_status(world.jobid, total.scenarios_ran == total.scenarios_passed)
    world.browser.quit()
