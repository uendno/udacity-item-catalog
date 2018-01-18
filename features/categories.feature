Feature: Categories
  As a api consumer,
  I want the app serve me with information about categories

  Scenario: Get all categories
    When sending GET request to /categories
    Then receive a list of 9 available categories

  Scenario: Get details for a category
    When sending a GET request to /categories/soccer
    Then receive details for Soccer category

  Scenario: Get details for an unknown category
    When sending GET request to /categories/unknown
    Then receive 400 error code for unknown category