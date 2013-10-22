#pylint: disable=C0111
#pylint: disable=W0621

# Disable the "wildcard import" warning so we can bring in all methods from
# course helpers and ui helpers
#pylint: disable=W0401

# Disable the "Unused import %s from wildcard import" warning
#pylint: disable=W0614

# Disable the "unused argument" warning because lettuce uses "step"
#pylint: disable=W0613

from lettuce import world, step
from .ui_helpers import *
from nose.tools import assert_equal

from logging import getLogger
logger = getLogger(__name__)


@step(r'I wait (?:for )?"(\d+)" seconds?$')
def wait(step, seconds):
    world.wait(seconds)


@step('I reload the page$')
def reload_the_page(step):
    world.browser.reload()


@step('I press the browser back button$')
def browser_back(step):
    world.browser.driver.back()


@step('I (?:visit|access|open) the homepage$')
def i_visit_the_homepage(step):
    world.visit('/')
    assert_equal(world.browser.title, 'edX')


@step(u'I (?:visit|access|open) the course list page$')
def i_am_on_the_course_list_page(step):
    world.visit('/course-list')
    assert world.is_css_present('div.view-course')


@step(u'I press the "([^"]*)" button$')
def and_i_press_the_button(step, value):
    button_css = 'input[value="%s"]' % value
    world.css_click(button_css)


@step(u'I click the link with the text "([^"]*)"$')
def click_the_link_with_the_text_group1(step, linktext):
    world.click_link(linktext)


@step('I should see that the path is "([^"]*)"$')
def i_should_see_that_the_path_is(step, path):
    assert world.url_equals(path)


@step(u'the page title should be "([^"]*)"$')
def the_page_title_should_be(step, title):
    assert_equal(world.browser.title, title)


@step(u'the page title should contain "([^"]*)"$')
def the_page_title_should_contain(step, title):
    assert(title in world.browser.title)


@step('I am not logged in$')
def i_am_not_logged_in(step):
    world.browser.cookies.delete()


@step(r'click (?:the|a) link (?:called|with the text) "([^"]*)"$')
def click_the_link_called(step, text):
    world.click_link(text)


@step(r'should see that the url is "([^"]*)"$')
def should_have_the_url(step, url):
    assert_equal(world.browser.url, url)


@step(r'should see (?:the|a) link (?:called|with the text) "([^"]*)"$')
def should_see_a_link_called(step, text):
    assert len(world.browser.find_link_by_text(text)) > 0


@step(r'should see (?:the|a) link with the id "([^"]*)" called "([^"]*)"$')
def should_have_link_with_id_and_text(step, link_id, text):
    link = world.browser.find_by_id(link_id)
    assert len(link) > 0
    assert_equal(link.text, text)


@step(r'should see a link to "([^"]*)" with the text "([^"]*)"$')
def should_have_link_with_path_and_text(step, path, text):
    link = world.browser.find_link_by_text(text)
    assert len(link) > 0
    assert_equal(link.first["href"], 'TODO: fixme')


@step(r'should( not)? see "(.*)" (?:somewhere|anywhere) (?:in|on) (?:the|this) page')
def should_see_in_the_page(step, doesnt_appear, text):
    if doesnt_appear:
        assert world.browser.is_text_not_present(text, wait_time=5)
    else:
        assert world.browser.is_text_present(text, wait_time=5)


@step(u'visit the url "([^"]*)"')
def visit_url(step, url):
    world.visit(url)
