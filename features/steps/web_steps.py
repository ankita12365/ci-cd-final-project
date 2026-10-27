from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from compare import expect

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + "-btn"
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    element.click()

@then('I should see "{text}" in the results')
def step_impl(context, text):
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "search_results"), text)
    )
    expect(element).to_be(True)

@then('I should not see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element(By.ID, "search_results")
    expect(text not in element.text).to_be(True)

@then('I should see the message "{message}"')
def step_impl(context, message):
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    expect(element).to_be(True)
