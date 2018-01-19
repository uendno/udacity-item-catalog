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
    Then remove all items

  Scenario: Get details for an unknown item
    Given DB does not have any item which has id = 123
    When sending GET request to /items/123
    Then receive 400 error code for unknown item

  Scenario: Add an valid item
    Given DB does not have any item which has the name Item 1
    When sending a POST request to /items to add an item with the name Item 1
    Then receive 200 status code

  Scenario: Add an invalid item
    Given DB has an item which has the name Item 1 and category_id=1
    When sending a POST request to /items to add an item with the name Item 1
    Then receive 400 status code
    Then remove all items

  Scenario: Update an item with valid category_id
    Given DB has an item which has the name Item 1 and category_id=1
    When sending a PUT request to/items/1 to update category_id to 2
    Then receive 200 status code

  Scenario: Update an item with invalid category_id
    Given DB has an item which has the name Item 1 and category_id=1
    When sending a PUT request to/items/100 to update category_id to 100
    Then receive 400 status code


  Scenario: Delete an valid item
    Given DB has an item which has the name Item 1 and category_id=1
    When sending a DELETE request to/items/1 to delete the item
    Then receive 200 status code

  Scenario: Delete an invalid item
    Given DB dose not an item which has id=1
    When sending a DELETE request to/items/1 to delete the item
    Then receive 400 status code

