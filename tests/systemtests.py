import unittest2, time
from app import app, db
from app.models import User

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
from selenium.webdriver.common.action_chains import ActionChains

u = User(username="Test123", email="test123@email.com", password_hash="test123")
admin = User(username='admin', password_hash='123')
webdriver_PATH = "chromedriver.exe"

class SystemTest(unittest2.TestCase):
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

    def test_1_register(self):
        driver = self.driver

        num = randint(0,1000000)
        u1 = User(username="Test"+str(num), email="test"+str(num)+"@email.com", password_hash="test"+str(num))
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[6]/a")))
        logout.click()
        register = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/p/a/span")))
        register.click()
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"username")))
        username.send_keys(u1.username)
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"email")))
        email.send_keys(u1.email)
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
        password.send_keys(u1.password_hash)
        password2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password2")))
        password2.send_keys(u1.password_hash)
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"submit")))
        submit.click()
        signin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/h1")))
        self.assertEqual("Sign In", signin.text)

    def test_2_login(self):
        driver = self.driver

        greeting = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/h1")))
        self.assertEqual(greeting.text,"Hi, "+str(u.username)+"!")

    def test_3_learn_page(self):
        driver = self.driver

        LearnTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[2]/a")))
        LearnTab.click()
        qg = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"Queens Gambit")))
        self.assertEqual("Queens Gambit", qg.text)

    def test_4_results_page(self):
        driver = self.driver

        ResultsTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[4]/a")))
        ResultsTab.click()
        ResultsQG = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="listleft"]/li[1]/a')))
        ResultsQG.click()
        re_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header"]/th[2]')))
        self.assertEqual("Result", re_text.text)
    
    def test_5_logout(self):
        driver = self.driver

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[6]/a")))
        logout.click()
        signin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/h1")))
        self.assertEqual("Sign In", signin.text)

    def test_6_addOpening(self):
        driver = self.driver
        action = ActionChains(driver)
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[6]/a")))
        logout.click()
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"username")))
        username.send_keys(admin.username)
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
        password.send_keys(admin.password_hash)
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"submit")))
        submit.click()
        time.sleep(3)
        openings = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="admin-navbar-collapse"]/ul[1]/li[2]')))
        openings.click()
        time.sleep(3)
        create = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/ul/li[2]')))
        create.click()
        time.sleep(3)
        name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'name')))
        name.send_keys('TestOpening')
        fen = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'FEN')))
        fen.send_keys('rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR')
        time.sleep(3)
        save = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/form/div[3]/div/input[1]')))
        save.click()

        listOpenings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'col-name')))
        self.assertEqual('TestOpening',listOpenings[-1].text)

    def test_7_learnOpening(self):
        driver = self.driver
        driver.maximize_window()
        action = ActionChains(driver)
        LearnTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[2]/a")))
        LearnTab.click()
        toTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[id='TestOpening']")))
        toTab.click()
        toLearn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"openingname")))
        toLearn.click()
        time.sleep(3)
        move1s = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-square='a2']")))
        move1e = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-square='a4']")))
        action.drag_and_drop(move1s[-1],move1e[-1]).perform()

        complete = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="complete"]')))
        self.assertEqual("Complete!", complete.text)
        self.assertNotEqual("NotComplete!", complete.text)

    def test_8_testOpening(self):
        driver = self.driver
        driver.maximize_window()
        action = ActionChains(driver)
        TestTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[3]/a")))
        TestTab.click()
        toTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[id='TestOpening']")))
        toTab.click()
        toLearn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"openingname")))
        toLearn.click()
        time.sleep(3)
        move1s = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-square='a2']")))
        move1e = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-square='a4']")))
        action.drag_and_drop(move1s[-1],move1e[-1]).perform()

        complete = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="complete"]')))
        self.assertEqual("Complete!", complete.text)
        self.assertNotEqual("NotComplete!", complete.text)

    def test_9_remove_opening(self):
        driver = self.driver
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[6]/a")))
        logout.click()
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"username")))
        username.send_keys(admin.username)
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
        password.send_keys(admin.password_hash)
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"submit")))
        submit.click()
        time.sleep(2)
        openings = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="admin-navbar-collapse"]/ul[1]/li[2]')))
        openings.click()
        listOpenings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'col-name')))
        if listOpenings[-1].text == "TestOpening":
            time.sleep(3)
            selectOpening = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'action-checkbox')))
            selectOpening[-1].click()
            time.sleep(3)
            selectDropDown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/ul/li[3]/a')))
            selectDropDown.click()
            time.sleep(3)
            deleteOpening = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/ul/li[3]/ul')))
            deleteOpening.click()
            time.sleep(3)
            driver.switch_to_alert().accept()
            time.sleep(3)
            listOpenings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'col-name')))
            self.assertNotEqual(listOpenings[-1],"TestOpening")

    def test_10_feedback(self):
        driver = self.driver
        FeedbackTab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/nav/ul/li[5]/a")))
        FeedbackTab.click()
        FeedbackQG = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="listleft"]/li[1]/a')))
        FeedbackQG.click()
        Feedbacktext = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="selecttest"]')))
        self.assertEqual("Select test with errors",Feedbacktext.text)

    def test_11_progress(self):
        driver = self.driver
        progress = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]')))
        self.assertIn('%',progress.text)

if __name__ == '__main__':
    unittest2.main(verbosity= 2)
