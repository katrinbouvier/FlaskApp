from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


@given('website "{url}"')
def step(context, url):
    context.browser = webdriver.Firefox(
        executable_path='C:/webdrivers/geckodriver.exe',
        firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')
    context.browser.maximize_window()
    context.browser.get("http://127.0.0.1:5000/")


@then("push button with text '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 120).until(
        EC.element_to_be_clickable((By.XPATH, '//button'))
    )
    context.browser.find_element_by_xpath('//button').click()


@then("page include text '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 120).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)
    context.browser.quit()
