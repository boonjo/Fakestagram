from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, strftime
from random import randint
import pandas as pd
import getpass

HASHTAGS = ['yashicac', 'filmphotography', 'filmisnotdead']
COMMENTS = ['This is great', 'keep up the good work!', 'I love your photos!', 'This is so cool']

# Opening Chrome
print('⏳ Opening Browser... ⌛️\n')
chromedriver_path = '/Users/joonbo/Documents/Personal/Playground/Fakestagram/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)


USER = 'wnsqh' #input("Enter your Instagram username: ")
PASSWORD = 'Bigpenguinshim113()' #getpass.getpass("Enter your Password: ")

password_length = len(PASSWORD)
password_hide = ('*' * password_length)

if (USER==None or PASSWORD ==None):
    print ('===> Make sure to type in both your username and password')
    print('===> Exiting...')
    exit()

username = driver.find_element_by_name('username')
username.send_keys(USER)
password = driver.find_element_by_name('password')
password.send_keys(PASSWORD)


# Logging in
print('===> Logging into Instagram\n')
button_login = driver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button')
button_login.click()
sleep(3)

# Bypassing the "Save Login Info" pop up
notnow = driver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
notnow.click()
sleep(1)

# Bypassing the "Turn Notifications On" pop up
plznotnow = driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
plznotnow.click()
sleep(1)

#prev_user_list = [] #- if it's the first time you run it, use this line and comment the two below
# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])
new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0
#total_posts = 5 # per hashtag
comment_percentage = 100

for hashtag in HASHTAGS:
    print('===> Looking through #' + hashtag + '\n')
    tag += 1
    driver.get('https://www.instagram.com/explore/tags/'+ HASHTAGS[tag] + '/')
    sleep(randint(2,4))
    
    print("===> Clicking first post of #" + hashtag + '\n')
    first_thumbnail = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')    
    first_thumbnail.click()
    sleep(randint(1,2))
    
    try:        
        for x in range(1,200):
            print('#' + hashtag, 'Post: ' + str(x) + '\n')
            # If we already like, then do nothing with the post, go to next post
            alreadyLike = driver.find_elements_by_xpath( "//section/span/button/div/span[*[local-name()='svg']/@aria-label='Like']")
            
            if len(alreadyLike) == 1:
                print('===> Following the user if we have follow button\n')
                
                action = ActionChains(driver)
                action.move_to_element(driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd > div:nth-child(1) > div > span > a')).perform()                            
                sleep(2)
                
                print("===> Following user now in few seconds\n")
                button_follow = driver.find_element_by_xpath('//button[normalize-space()="Follow"]')                
                button_follow.click()
                followed += 1

                # Liking the picture
                print('===> Liking the picture\n')
                sleep(1)
                button_like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                button_like.click()
                likes += 1

                # Comments and tracker
                comm_prob = randint(1,10)
                print('===> Trying to comment if probability is found to be more than', str(comment_percentage) + '\n')
                print('===> Probability found to be: ', str(comm_prob*10) + '\n')
                if comm_prob > comment_percentage/10:
                    print('===> Commenting\n')
                    sleep(3)                                                    
                    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()
                    sleep(3)
                    comment_box = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                    commentIndex = randint(0,len(COMMENTS)-1)
                    print('===> Printing comment number {0}, which is {1}'.format(commentIndex+1, COMMENTS[commentIndex]) + '\n')
                    comment_box.send_keys(COMMENTS[commentIndex])
                    sleep(1)
                    
                    # Enter to post comment
                    comment_box.send_keys(Keys.ENTER)
                    comments += 1
                    print('===> Commented! now waiting few seconds\n')
                    sleep(randint(3,6))
                else:
                    print('===> Skipping commenting, since probability is low\n')
            else:
                print('===> Post already liked, so skipping the post\n')

            # Next picture
            print('===> Moving next\n') 
            if x == 1:
                driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
            else:
                driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[' + str(x) + ']').click()
            sleep(randint(2,5))
                        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        continue


print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
