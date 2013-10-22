Feature: Homepage for web users
  In order to get an idea what edX is about
  As a an anonymous web user
  I want to check the information on the home page


  Scenario: User can see the "Login" button
    Given I visit the homepage
    Then I should see a link called "log in"


  Scenario: User can navigate via the header
    Given I visit the homepage
    Then I should see the following links and ids
    | id           | Link         |
    | how-it-works | How It Works |
    | course-list  | Courses      |
    | schools      | Schools      |
    | register     | Register Now |


  Scenario: User can navigate via the footer
    Given I visit the homepage
    Then I should see the following links and ids
    | id          | Link     |
    | about-us    | About Us |
    | jobs        | Jobs     |
    | news        | Press    |
    | student-faq | FAQ      |
    | contact-us  | Contact  |


  Scenario: User can get to the course listing
    Given I visit the homepage
    Then I should see the following links and ids
    | id           | Link                           |
    | course-list  | Find a Course & Start Learning |
    | course-list  | see all courses                |


  Scenario: User can get to news about edX
    Given I visit the homepage
    Then I should see the following links and ids
    | id    | Link      |
    | news  | more news |


  Scenario: User can see the first 4 partner institutions
    Given I visit the homepage
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Massachusetts Institute of Technology          |
    | Harvard University                             |
    | UC Berkeley                                    |
    | University of Texas System                     |


  Scenario: User can see the second 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "1" time
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Australian National University                 |
    | Delft University of Technology                 |
    | EPFL                                           |
    | Georgetown University                          |


  Scenario: User can see the third 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "2" times
    Then I should see the following Partners in the Partners section
    | McGill University                              |
    | Rice University                                |
    | University of Toronto                          |
    | Wellesley College                              |


  Scenario: User can see the fourth 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "3" times
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Berklee College of Music                       |
    | Boston University                              |
    | Cornell University                             |
    | Davidson College                               |


  Scenario: User can see the fifth 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "4" times
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | University of Hong Kong                        |
    | Hong Kong University of Science and Technology |
    | IITBombay                                      |
    | Karolinska Institutet                          |


  Scenario: User can see the sixth 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "5" times
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Kyoto University                               |
    | Université catholique de Louvain               |
    | Peking University                              |
    | Seoul National University                      |


  Scenario: User can see the seventh 4 partner institutions
    Given I visit the homepage
    When I click the right pager arrow "6" times
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Tsinghua University                            |
    | Technische Universität München                 |
    | University of Queensland                       |
    | University of Washington                       |
