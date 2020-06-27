
from selenium import webdriver
import re
from chromedriver_py import binary_path

def searchInstaUser(user):
    driver = webdriver.Chrome(executable_path=binary_path)
    driver.get('https://www.instagram.com/instagram')
    delay = 3
    driver.implicitly_wait(delay)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(user)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div').click()
    
    r = requests.get(driver.current_url).text
    followers = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)
    
    driver.quit()
    print("{} : {}".format(user, followers))
