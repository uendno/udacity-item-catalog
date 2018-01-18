Feature: Authentication
  In order to secure the app,
  As a api consumer,
  I want the app to decide whether I'm able to access a route

  Scenario: Access a public route without access token
    Given no access token provided
    When sending a GET request to /items?mode=latest
    Then receive 200 code

  Scenario: Access a protected route without access token
    Given no access token provided
    When sending a DELETE request to /items/1
    Then receive 401 error code


  Scenario: Access a protected route with a valid access token
    Given a valid access token
    When sending a DELETE request to /items/1
    Then response status code is not 401