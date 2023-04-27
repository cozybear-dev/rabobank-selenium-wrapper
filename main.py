from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import logging

def setup_driver():
    #yay -S chromium
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    return driver

def login(driver):
    driver.get("https://bankieren.rabobank.nl/online/nl/dashboard")
    wait = WebDriverWait(driver, 30)
    wait.until(EC.title_is('Overzicht'))
    return

def get_accounts(driver):
    driver.get("https://bankieren.rabobank.nl/api/msp/payments-savings/accounts?source=rbo-overview")
    account_details = json.loads(driver.find_element(By.TAG_NAME, "pre").text)
    return account_details["authorizedAccounts"]

def get_latest_transactions(driver, account_id):
    driver.get(f"https://bankieren.rabobank.nl/api/msp/payments-savings/accounts/{account_id}/transactions")
    return json.loads(driver.find_element(By.TAG_NAME, "pre").text) 

# def send_transaction(driver, from_iban, to_iban, to_name, amount)
#     https://bankieren.rabobank.nl/api/msp/payments-savings/orders

# def create_payment_request(driver)
#     https://bankieren.rabobank.nl/api/msp/payments/payment-requests

def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    driver = setup_driver()
    login(driver)

    for account in get_accounts(driver):
        logging.info(f'Account found: {account}')
        account_id = account["accountId"]
        latest_transactions = get_latest_transactions(driver, account_id)
        logging.info(f'Transaction details for account {account_id}: {latest_transactions}')

if __name__ == '__main__':
    main()