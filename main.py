import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import smtplib
import ssl
from email.message import EmailMessage


def get_driver(country_name):
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')  # disable sidebars
    options.add_argument('start-maximized')  # chrome start on full size
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    service = Service("chromedriver.exe")
    url = "https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6"

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)  # link
    return driver


def get_data():
    driver = get_driver("turkey")
    time.sleep(2)
    stock_value = driver.find_element(by="xpath", value="//*[@id='app_indeks']/section[1]/div/div/div[2]/div/span").text
    stock_change = driver.find_element(by="xpath", value="//*[@id='app_indeks']/section[1]/div/div/div[2]/span").text
    return {stock_value, stock_change}


def send_email():
    email_sender = "xxx@gmail.com"
    email_receiver = "xxx@gmail.com"
    email_password = "xxx"

    stock_change, stock_value = get_data()
    subject = "Increase on the stock"
    body = f"CROBEX up trending by {stock_change} and new stock value is {stock_value}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    security = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=security) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


if __name__ == "__main__":
    get_data()
