Feature: The product service back-end

Background:
    Given the following products
        | name | description | price | available | category |
        | Hat | Straw summer hat | 12.50 | True | CLOTHS |
        | Burger | Delicious beef burger | 8.00 | True | FOOD |

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the name "Hat"
    And I should see the description "Straw summer hat"
    And I should see "True" in the "Available" dropdown

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the name "Hat"
    When I change "Description" to "New description"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the name "Hat"
    And I should see the description "New description"

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the name "Hat"
    When I press the "Delete" button
    Then I should see the message "Product Deleted!"

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see "Hat" in the results
    And I should see "Cloth" in the results

Scenario: Search for Products by Category
    When I visit the "Home Page"
    And I select "CLOTHS" in the "Category" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should not see "Burger" in the results

Scenario: Search for Products by Availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results

Scenario: Search for Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
