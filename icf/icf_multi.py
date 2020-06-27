
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from tqdm import tqdm


def searchMultipleInstaUser(userList):

    listUser = []
    listFollower = []
    a=0
    
    while a in tqdm(range(0, int(np.ceil((len(userList))/2)))):
#        print("a = {}".format(a))
        driver = webdriver.Chrome(executable_path=binary_path)
        driver.get('https://www.instagram.com/instagram')
        delay = 3
        driver.implicitly_wait(delay)

        n = 0
        while n < 2:
            
            try:
                userNum = 2*a + n
#                print("userNum: {}+{}={}".format(a,n,userNum))
                user = userList[userNum]
                
                driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(user)
                toNext = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')))
                toNext.click()
#                driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div').click()

                r = requests.get(driver.current_url).text
                followers = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)    
            
                if (r.find('"is_verified":true')!=-1):
#                    print('{} : {}'.format(user, followers))
                    listUser.append(user)
                    listFollower.append(followers)
                else:
#                    print('{} : user not verified'.format(user))
                    listUser.append(user)
                    listFollower.append('user not verified')
            
                n += 1
                continue
                
            except Exception:
                driver.refresh()
                listUser.append(user)
                listFollower.append('Error')
                break
                
            except IndexError:
                driver.quit()
                print("End of List: Terminating Instagram Crawler")
                return
                    
        driver.quit()
        a += 1
    return pd.DataFrame(list(zip(listUser, listFollower)), columns=["Users", "Followers"])
