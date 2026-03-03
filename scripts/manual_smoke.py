from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    driver.quit()

if __name__ == "__main__":
    main()