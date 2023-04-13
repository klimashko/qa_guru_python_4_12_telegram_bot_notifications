import allure
from selene.support.shared import browser
from selene import have
from selene import command
import os
from selenium.webdriver.chrome.options import Options

import tests
import pytest
from selenium import webdriver
from tests.utils import attach


@pytest.fixture(scope="function", autouse=True)
def open_browser():
    browser.config.base_url = 'https://demoqa.com'

    yield

    browser.quit()


def test_student_registration_form():
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options)

    browser.config.driver = driver

    with allure.step('Open registration form'):
        browser.open('/automation-practice-form')

        browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    # WHEN
    with allure.step('Fill registration form'):
        browser.element('#firstName').type('Olga')
        browser.element('#lastName').type('YA')
        browser.all('[name=gender]').element_by(have.value('Female')).element(
            '..').click()

        browser.element('#userNumber').type('1234567891')
        browser.element('#userEmail').type('name@example.com')

        browser.element('[for=hobbies-checkbox-2]').perform(
            command.js.scroll_into_view)
        browser.element('[for=hobbies-checkbox-2]').click()

        browser.element('#currentAddress').type('Moscowskaya Street 18')

        browser.element('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text('NCR')
        ).click()

        browser.element('#city').click()
        browser.element('#react-select-4-option-0').click()

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type('May')
        browser.element('.react-datepicker__year-select').type('1999')
        browser.element(f'.react-datepicker__day--0{11}').click()

        browser.element('#subjectsInput').type('Computer Science').press_enter()

        browser.element('#uploadPicture').set_value(
            os.path.abspath(
                os.path.join(os.path.dirname(tests.__file__),
                             '../tests/resources/foto.jpg')
            )
        )

        browser.element('#submit').press_enter()

    # THEN
    with allure.step('Verify registration form'):
        browser.element('.table').all('td').even.should(
            have.exact_texts(
                'Olga YA',
                'name@example.com',
                'Female',
                '1234567891',
                '11 May,1999',
                'Computer Science',
                'Reading',
                'foto.jpg',
                'Moscowskaya Street 18',
                'NCR Delhi',
            )
        )

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)


