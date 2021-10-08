
from os import EX_TEMPFAIL
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

videos = {}

USERNAME = None #put on line 1  of login_info.txt
PASSWORD = None #put on line 2  of login_info.txt

PATH = "./chromedriver"
driver = webdriver.Chrome(PATH)

##################get password from file##################
passfile = open("login_info.txt", "r")
login_info_lines = passfile.read().split('\n')
USERNAME = login_info_lines[0]
PASSWORD = login_info_lines[1]

##################login##################
driver.get("https://decobubbles.com/login")
current_url = driver.current_url

inputs = driver.find_elements_by_tag_name("input")
email = inputs[0]
password = inputs[1]
email.send_keys(USERNAME)
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN)

#####get account info#####

try:
    WebDriverWait(driver, 10).until(
        (EC.url_changes(current_url))
    )
    current_url = driver.current_url
    admin_button = driver.find_elements_by_class_name("mat-button")
    admin_button = admin_button[3]
    admin_button.click()
    
    WebDriverWait(driver, 10).until(
        (EC.url_changes(current_url))
    )
    time.sleep(1)

    #switch to completed videos
    dropdown = driver.find_elements_by_tag_name("mat-form-field")
    dropdown[0].click()

    WebDriverWait(driver, 0.2)
    time.sleep(.2)
    complete = driver.find_elements_by_tag_name("mat-option")
    complete = complete[1]
    complete.click()

    #Get names of each of the videos
    more_videos = True
    while(more_videos):
        #check if last page
        page_label = driver.find_element_by_class_name("mat-paginator-range-label")
        page_label = page_label.text.split(' ')
        current = page_label[2]
        end = page_label[-1]
        print (current, end)
        if (current >= end):
            more_videos = False

        #get all videos on page.

        table_body = driver.find_element_by_tag_name("tbody")
        WebDriverWait(driver, .5)
        time.sleep(.5)
        rows = table_body.find_elements_by_tag_name("tr")

        for video in rows:
            columns = video.find_elements_by_tag_name("td")
            video_name = columns[1].text
            print (video_name) #save
            try:
                columns[4].click()
            except Exception as e:
                print(e)

            WebDriverWait(driver, .2)
            time.sleep(.2)
            video_options = driver.find_element_by_class_name("cdk-overlay-pane")
            actions = ActionChains(driver)
            expand_button = video_options.find_element_by_tag_name("button")
            actions.move_to_element(expand_button)
            actions.click()
            actions.perform()
            WebDriverWait(driver, .2)
            time.sleep(.2)
            dialog = driver.find_element_by_tag_name("mat-dialog-container")
            user_ratings = []
            user_table = dialog.find_element_by_tag_name("tbody")
            user_rows = user_table.find_elements_by_tag_name("tr")
            for row in user_rows:
                cols = row.find_elements_by_tag_name("td")
                user = cols[0].text
                rating = cols[1].text
                user_ratings.append((user, rating))
            videos[video_name] = user_ratings
            quit_dialog = dialog.find_element_by_tag_name('button')
            quit_dialog.click()
        
        #navigate to next page

        next_page = driver.find_element_by_class_name("mat-paginator-navigation-next")
        next_page.click()
        time.sleep(.2)
        WebDriverWait(driver, .2)
        print(more_videos)
    driver.quit()


except Exception as e:
    print(e)

    driver.quit()


print (videos)
f = open("video_info.txt", "w")
for video in videos.keys():
    line = video 
    for rating in videos[video]:
        line += "," + rating[0] + ' ' + rating[1] 
    line += '\n'
    f.write(line)
#driver.save_screenshot("./sc1.png")
