import unittest, os, time
from app import app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

u = User(username="Test123", email="test123@email.com", password_hash="test123")

webdriver_PATH = r"C:\Users\steve\OneDrive\Desktop\chromedriver_win32\chromedriver.exe"

class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=webdriver_PATH)

        if not self.driver:
            self.skipTest('Web browser not available')
        
        else:
            self.driver.get("http://127.0.0.1:5000/")

            driver = self.driver
            username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"username")))
            username.send_keys(u.username)
            password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
            password.send_keys(u.password_hash)
            submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"submit")))
            submit.click()

    def TearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()

    def test_login(self):
        driver = self.driver

        greeting = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/h1")))
        self.assertEqual(greeting.text,"Hi, "+str(u.username)+"!")

    def test_learn_page(self):
        driver = self.driver

        LearnTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[2]/a")))
        LearnTab.click()
        qg = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"meow")))
        self.assertEqual("Queens Gambit", qg.text)

    def test_results_page(self):
        driver = self.driver

        ResultsTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[4]/a")))
        ResultsTab.click()
        re_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/table/tbody/tr/th[1]")))
        self.assertEqual("Opening", re_text.text)

    
    def test_logout(self):
        driver = self.driver

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[5]/a")))
        logout.click()
        signin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/h1")))
        self.assertEqual("Sign In", signin.text)

if __name__ == '__main__':
    unittest.main(verbosity= 2)
