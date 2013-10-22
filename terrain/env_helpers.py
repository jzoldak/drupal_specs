import os
from sauce_helpers import ParseSauceUrl


class BrowserEnv(object):
    """
    Class to hold the browser environment settings.
    These are determined by OS environment values that are
    set locally, by Jenkins, and by the SauceLabs Jenkins plugin.
    """
    def __init__(self):

        # Take a local copy of the OS environment because we do
        # not need to change the values for this shell
        osenv = os.environ.copy()

        # When started by a Jenkins job, the following environment variables will
        # automatically be set by the SauceLabs plugin from the matrix choice made:
        # SELENIUM_BROWSER, SELENIUM_VERSION, and SELENIUM_PLATFORM
        # When configuring the Jenkins job, note that we use Sauce OnDemand
        # WebDriver tests, not Sauce OnDemand SeleniumRC tests.
        #
        # If you want to run on an alternate Selenium Grid (e.g. a local one) then
        # set up these environment variables yourself.
        # Only selenium_browser is used for a local webdriver, so
        # give that a default of firefox if it was not defined.
        self.selenium_platform = osenv.get('SELENIUM_PLATFORM')
        self.selenium_version = osenv.get('SELENIUM_VERSION')
        self.selenium_browser = osenv.get('SELENIUM_BROWSER', 'firefox')

        # Define these environment variables yourself if you want to run
        # off an alternate grid, for example a local one.
        # If you are running on Jenkins with the SauceLabs plugin
        # the values will be populated for you.
        # If you want to run a local browser, you do not need to set these.
        self.selenium_host = osenv.get('SELENIUM_HOST')
        self.selenium_port = osenv.get('SELENIUM_PORT')

        # The SauceLabs Jenkins plugin also overwrites the values of
        # the following environment variables:
        self.selenium_driver = osenv.get('SELENIUM_DRIVER')
        self.sauce_user_name = osenv.get('SAUCE_USER_NAME')
        self.sauce_api_key = osenv.get('SAUCE_API_KEY')
        self.run_on_saucelabs = bool(
            self.selenium_host == 'ondemand.saucelabs.com'
            or self.selenium_driver
            )

        # BUILD_NUMBER and JOB_NAME get set by Jenkins itself.
        # Not needed for private grid or local browser.
        self.run_on_jenkins = bool(osenv.get('JOB_NAME'))
        self.build_number = osenv.get('BUILD_NUMBER', 'local harvest')
        self.job_name = osenv.get('JOB_NAME', 'acceptance tests')

        # This will be filled in later once the webdriver starts up.
        # It is used to communicate with SauceLabs to update the
        # job, for example with the pass/fail status.
        self.session_id = None

        # When run as a multi-configuration project on Jenkins the
        # SELENIUM_DRIVER url will be populated and its values
        # need to be extracted and used instead of the individual
        # os environment values.
        # example url: sauce-ondemand:?os=Linux&browser=chrome&browser-version=28&username=foo&access-key=bar
        if self.selenium_driver:
            parse = ParseSauceUrl(self.selenium_driver)
            self.sauce_user_name = parse.get_value('username')
            self.sauce_api_key = parse.get_value('access-key')
            self.selenium_browser = parse.get_value('browser')
            self.selenium_version = parse.get_value('browser-version')
            sauce_driver_os = parse.get_value('os')
            if 'Windows 2003' in sauce_driver_os:
                self.selenium_platform = 'XP'
            elif 'Windows 2008' in sauce_driver_os:
                self.selenium_platform = 'VISTA'
            elif 'Linux' in sauce_driver_os:
                self.selenium_platform = 'LINUX'
            else:
                self.selenium_platform = sauce_driver_os
