Feature: Items
  As a api consumer,
  I want the app serve me with information about items and I'm able to create or update an item

  Scenario: Get all items
    Given DB has 3 items
    When sending GET request to /items
    Then receive a list of 3 available items

  Scenario: Get latest items
    Given DB has 3 items
    When sending a GET request to /items?mode=latest&limit=2
    Then receive a list of 2 most recent items

  Scenario: Get details for a item
    Given DB has 1 item which has id = 1
    When sending a GET request to /items/1
    Then receive details for the right item

  Scenario: Get details for an unknown item
    Given DB does not have any item which has id = 123
    When sending GET request to /items/123
    Then receive 400 error code for unknown item

  Scenario: Add an valid item
    Given DB does not have any item which has the name Item 1
    When sending a POST request to /items to add an item with the name Item 1
    Then receive 200 status code and item details

  Scenario: Add an invalid item
    Given DB has an item which has the name Item 1
    When sending a POST request to /items to add an item with the name Item 1
    Then receive 400 status code because of the invalid name