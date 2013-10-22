Feature: Course list page
  In order to find a course I want to take
  As a an anonymous web user
  I want to search for courses


  Scenario: All courses are shown by default
    Given I visit the course list page
    Then the "all" filter link is active
    And the total number of courses is "62"
    And "all subjects" is shown in the "subject" filter dropdown
    And "all schools" is shown in the "school" filter dropdown
    And I see courses from different schools


  Scenario: User can filter courses by subject
    Given I visit the course list page
    When I apply the "subject" filter with the value "ethics"
    Then the total number of courses is "5"
    And I see courses from different schools
    And I should see the following courses in the listing
    | course     |
    | edXDEMO101 |
    | 24.00x     |
    | PHLX101-01 |
    | SOC108x    |
    | ER22x      |


  Scenario: User can filter courses by school
    Given I visit the course list page
    When I apply the "school" filter with the value "mitx"
    Then I should only see courses for "MITx"


  Scenario Outline: User can filter courses by chronology
    Given I visit the course list page
    When I click the "<link>" filter link
    Then the "<link>" filter link is active
    And the total number of courses is "<num_courses>"
  Examples:
    | link    | num_courses |
    | current | 4           |
    | new     | 43          |
    | past    | 15          |


  Scenario: Pressing a chronology link does not reset the subject and school filters
    Given I visit the course list page
    And I apply the "subject" filter with the value "computer-science"
    And I apply the "school" filter with the value "uc-berkeleyx"
    When I click the "past" filter link
    Then the "past" filter link is active
    And "Computer Science" is shown in the "subject" filter dropdown
    And "UC BerkeleyX" is shown in the "school" filter dropdown
    And all the courses listed have NEW icons


  Scenario: User can filter by subject and chronology
    Given I visit the course list page
    When I apply the "subject" filter with the value "history"
    And I click the "new" filter link
    Then the total number of courses is "10"
    And all the courses listed have NEW icons
    And I see courses from different schools


  Scenario: User can filter by school and chronology
    Given I visit the course list page
    When I click the "current" filter link
    And I apply the "school" filter with the value "mitx"
    Then the total number of courses is "1"
    And I should only see courses for "MITx"


  Scenario: User can filter by subject and school and chronology
    Given I visit the course list page
    When I choose the "school" filter with the value "harvardx"
    And I apply the "subject" filter with the value "humanities"
    And I click the "new" filter link
    Then the total number of courses is "5"
    And I should only see courses for "HarvardX"
    And I should see the following courses in the listing
    | course      |
    | CB22.1x     |
    | SW12x       |
    | AI12.1x     |
    | AI12.2x     |
    | HDS1544.1x  |


  Scenario: Pressing the "all" link resets all filters
    Given I visit the course list page
    And I apply the "school" filter with the value "harvardx"
    And I apply the "subject" filter with the value "humanities"
    And I click the "new" filter link
    When I click the "all" filter link
    Then the "all" filter link is active
    And the total number of courses is "62"
    And "all subjects" is shown in the "subject" filter dropdown
    And "all schools" is shown in the "school" filter dropdown
