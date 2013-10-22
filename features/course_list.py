from lettuce import world, step
from nose.tools import assert_equals, assert_in, assert_greater, assert_true
import re


@step(u'the "([^"]*)" filter link is active$')
def the_foo_filter_link_is_active(step, link_text):
    link_css = 'form#coursefilter-form a.active'
    assert_true(world.css_has_text(link_css, link_text),
        msg='The "{}" filter link is not active'.format(link_text))


@step(u'the total number of courses is "([^"]*)"$')
def the_total_number_of_courses_is_foo(step, count):
    div_css = 'div.view-header'

    # should return something like: 'Showing 1 - 15 of 62'
    div_text = world.css_text(div_css)
    pattern = re.compile(r'Courses: Showing (?P<first>\d+) - (?P<last>\d+) of (?P<total>\d+)')
    matched_text = re.match(pattern, div_text)

    assert matched_text
    assert_equals(matched_text.group('total'), count)


@step(u'"([^"]*)" is shown in the "([^"]*)" filter dropdown')
def foo_is_shown_in_the_bar_filter_dropdown(step, dd_value, dd_name):

    # the only 2 filters on the page are subject and school
    assert_in(dd_name, ['subject', 'school'])

    dd_css = 'select#edit-{dd_name}.form-select'.format(dd_name=dd_name)
    selected_css = "option[selected='selected']"
    full_css = '{dd} {selected}'.format(dd=dd_css, selected=selected_css)

    assert world.css_has_text(full_css, dd_value)


def get_schools_from_course_list():
    course_css = "div.course-tile div.views-fieldset"
    school_links_css = '{} ul li {}'.format(course_css, "a")

    schools = world.css_find(school_links_css)
    school_set = set()
    for school in schools:
        school_set.add(school.value)

    return school_set


@step(u'I see courses from different schools$')
def i_see_courses_from_different_schools(step):
    found_school_set = get_schools_from_course_list()
    assert_greater(len(found_school_set),1)


@step(u'I choose the "([^"]*)" filter with the value "([^"]*)"$')
def i_choose_the_foo_filter_bar(step, dd_name, dd_text):

    # the only 2 filters on the page are subject and school
    assert_in(dd_name, ['subject', 'school'])
    world.browser.select(dd_name, dd_text)


@step(u'I apply the "([^"]*)" filter with the value "([^"]*)"$')
def i_apply_the_foo_filter_bar(step, dd_name, dd_text):

    step.given('I choose the "{name}" filter with the value "{text}"'.format(
        name=dd_name,
        text=dd_text))
    filter_css = 'input#edit-submit.form-submit'
    world.css_click(filter_css)

    # Submitting the form causes a redirect.
    # Make sure the page redraws before continuing on
    form_css = "form#coursefilter-form"
    assert world.css_find(form_css)


@step(u'I should see the following courses in the listing$')
def i_should_see_the_following_courses_in_the_listing(step):
    course_title_css = "div.course-tile div.views-fieldset h2"

    courses = world.css_find(course_title_css)
    course_list = []
    for c in courses:
        title = c.text.split(':')[0]
        course_list.append(title)

    for row in step.hashes:
        assert_in(row['course'], course_list)


@step(u'I should only see courses for "([^"]*)"$')
def should_only_see_courses_for_foo(step, school):
    found_school_set = get_schools_from_course_list()
    assert_equals(len(found_school_set),1)
    assert(school in found_school_set)


@step(u'I click the "([^"]*)" filter link$')
def i_click_the_foo_filter_link(step, text):
    link_css = 'form#coursefilter-form a'
    # For synchronization purposes, make sure the links
    # are there first
    world.css_find(link_css)
    if text in ['current', 'past', 'new']:
        text = text.upper()
    world.browser.find_link_by_text(text).click()


@step(u'all the courses listed have NEW icons$')
def all_the_courses_listed_have_new_icons(step):
    course_row_css = "div.course-tile"
    courses = world.css_find(course_row_css)
    for course in courses:
        # splinter returns an empty list if the element is not found
        new_course_img = course.find_by_css('div.new-course-ribbon')
        assert_greater(len(new_course_img), 0)
