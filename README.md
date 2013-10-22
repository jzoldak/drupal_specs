## Installation:
```
mkvirtualenv drupal_specs
workon drupal_specs
pip install -r requirements.txt
```

## Setup:
### Local
No environment variables need to be set up. If you want to specify the browser version, you can do it like so:
```
os.environ['SELENIUM_BROWSER'] = 'chrome'
```

### Private Selenium Grid
Start up the selenium server (E.g. at port 4444, localhost). Start up some selenium nodes to take the traffic (E.g. port 5555, localhost).

Use environment variables to specify the selenium grid host and port, and the
browser version to test:
```
os.environ['SELENIUM_BROWSER'] = 'firefox'
os.environ['SELENIUM_HOST'] = 'localhost'
os.environ['SELENIUM_PORT'] = '4444'
```

### Sauce Labs
Start up the SauceConnect tunnel. Use environment variables to point over to Sauce Labs, the authentication credentials, and the browser version to test:
```
os.environ['SELENIUM_BROWSER'] = 'firefox'
os.environ['SELENIUM_PLATFORM'] = 'LINUX'
os.environ['SELENIUM_HOST'] = 'ondemand.saucelabs.com'
os.environ['SELENIUM_PORT'] = '80'
os.environ['SAUCE_USER_NAME'] = 'foo'
os.environ['SAUCE_API_KEY'] = 'bar'
```

## Execution:
`lettuce features/`


## References:
* [lettuce](http://lettuce.it/)
