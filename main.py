from selenium.webdriver.common.by import By
from selenium import webdriver
import time, os, yagmail


#add all of these options to a function to keep things organized
def get_driver():
  options = webdriver.ChromeOptions()

  #website infobars can confuse the cursor when trying to scrape data, so we disable it
  options.add_argument("disable-infobars")

  #starts the browser as maximized, some web pages change the content based on the size
  options.add_argument("start-maximized")

  #avoids potential issues when interacting with a browser on a linux computer
  options.add_argument("disable-dev-shm-usage")

  #browsers, for security, use something called sandboxing.
  #disabling this gives the scraper more privileges on the page
  options.add_argument("no-sandbox")

  #the following experimental option helps selenium avoid detection by the browser
  #some pages do not like scripts
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  #the options variable contains all of the arguments above
  driver = webdriver.Chrome(options=options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  return driver


def clean_text(text):
  """Extract only the temperature(dynamic value) from text"""
  #Split the text input using the colon and space delimiter and get the index at 1, convert to a float to be more inclusive
  output = float(text.split(" ")[0])
  return output


def email_notifier(percentage):
  sender = os.getenv('EMAIL_SENDER')
  receiver = os.getenv("EMAIL_RECEIVER")
  subject = "Crobex stock price has dropped below -0.04%"
  contents = f"The current Crobex stock price is at {percentage}%."

  yag = yagmail.SMTP(user=sender, password=os.getenv('PASSWORD'))
  yag.send(to=receiver, subject=subject, contents=contents)


def main():
  driver = get_driver()
  #xpath can be found by inspecting the element you are looking to scrape and right-clicking to copy the xpath
  #here I am causing the script to sleep for 2 seconds before grabbing the dynamic value from the page, otherwise it will be blank
  while True:
    time.sleep(2)
    element = driver.find_element(
      by=By.XPATH,
      value="/html/body/div[2]/div/section[1]/div/div/div[2]/span")

    percentage = clean_text(element.text)
    if percentage < -0.04:
      email_notifier(percentage)
      continue
    else:
      continue

  return clean_text(element.text)


print(main())
