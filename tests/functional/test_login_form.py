from __future__ import annotations

import pytest


@pytest.mark.functional
@pytest.mark.usefixtures("browser")
def test_login_form_accepts_input(browser, local_login_page):
    selenium = pytest.importorskip("selenium")
    from selenium.webdriver.common.by import By

    browser.get(local_login_page.as_uri())

    username = browser.find_element(By.ID, "username")
    password = browser.find_element(By.ID, "password")
    remember = browser.find_element(By.ID, "remember")
    submit = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username.send_keys("student@example.com")
    password.send_keys("super_secret")
    remember.click()
    submit.click()

    assert username.get_attribute("value") == "student@example.com"
    assert password.get_attribute("value") == "super_secret"
    assert remember.is_selected()
