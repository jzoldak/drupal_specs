Feature: Schools page
  In order to see what universities involved
  As a an anonymous web user
  I want to see the list of X-consortium members


  Scenario: User can see the partner institutions
    Given I visit the homepage
    When I click on the "schools" link
    Then I should see the following Partners in the Partners section
    | Partner                                        |
    | Massachusetts Institute of Technology          |
    | Harvard University                             |
    | UC Berkeley                                    |
    | University of Texas System                     |
    | Australian National University                 |
    | Delft University of Technology                 |
    | EPFL                                           |
    | Georgetown University                          |
    | McGill University                              |
    | Rice University                                |
    | University of Toronto                          |
    | Wellesley College                              |
    | Berklee College of Music                       |
    | Boston University                              |
    | Cornell University                             |
    | Davidson College                               |
    | University of Hong Kong                        |
    | Hong Kong University of Science and Technology |
    | IITBombay                                      |
    | Karolinska Institutet                          |
    | Kyoto University                               |
    | Université catholique de Louvain               |
    | Peking University                              |
    | Seoul National University                      |
    | Tsinghua University                            |
    | Technische Universität München                 |
    | University of Queensland                       |
    | University of Washington                       |
    | University of Texas at Austin                  |
