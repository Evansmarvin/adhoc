import json
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys

global chrome

def send_requests(url="https://www.quora.com/partners", max_wait=10, total_requests=25):

    """Function for sending requests to the writers for each question"""

    #for reading the email and password from credentials.json file and storing it in credentials variable
    cred_file = open("./quora_credentials.json", "r")
    credentials = cred_file.read()
    credentials = json.loads(credentials)
    cred_file.close()

    #for maximizing the browser's window
    options = Options()
    options.add_argument("--start-maximized")
    #options.headless = True

    #browser = webdriver.Chrome('./chromedriver', options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options) 

    browser.get(url)

    #for login to the user's account
    email = browser.find_element_by_id("email")
    email.send_keys(credentials["email"])
    pwd = browser.find_element_by_id("password")
    pwd.send_keys(credentials["password"])
    pwd.send_keys(Keys.ENTER)

    #fetching all the questions on the page before sending any request for the older questions
    try:
        all_questions = WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.ID, "questions")))
    except TimeoutException:
        exit("Invalid Email or Password")
    all_questions = all_questions.find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.QuestionListItem")
    no_class = browser.find_element_by_xpath("//div[@class='question_title']")
    no_of_questions = no_class.find_element_by_xpath('.//span[@class = "u-padding-left--xs u-text--gray-light"]')
    print(no_of_questions.text) #prints the number of questions asked
    
    length = len(all_questions)
    each_question = -1

    while each_question < length:

        each_question += 1

        #for scrolling the browser's window vertically by 42
        browser.execute_script("window.scrollTo(0, 42)")

        #when the question will be last then it will fetch the older questions after waiting 5 seconds
        if each_question == (len(all_questions)-1):
            sleep(5)
            all_questions = browser.find_element_by_id("questions").find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.QuestionListItem")
            #all_questions = browser.find_element_by_id("questions").find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.QuestionListItem MinimalQuestionListItem")
            length = len(all_questions)

        
        #when the question is not merged with other question then there will be a request answer button else it will skip that question
        try:
            request_ans_btn = all_questions[each_question].find_element_by_css_selector("div.a2a_section").find_element_by_css_selector("span")
            request_ans_btn.click()
        except:
            continue

        #for requesting the answers from the writers
        try:
            sleep(4)
            print("comes here")
            #topics =       //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[1]
            #writers =      //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]
            #writers =      //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div
            #list_writers = //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]    --list
            #               //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]
            #writer_1 =     //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]
            #writer_2 =     //*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[3]
            #writers = WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/')))
            
            #all_writers = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]')
            #all_writers = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]')
            #print(all_writers)
            #all_writers = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]')
            #all_writers = browser.find_element_by_css_selector("div.q-box").find_elements_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div/div') #works for one writer
            #all_writers = browser.find_element_by_css_selector("div.q-box").find_elements_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]')  #works for one writer
            #all_writers = browser.find_element_by_css_selector("div.q-box").find_elements_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div')  #works for one writer
            all_writers = browser.find_element_by_css_selector("div.q-box").find_elements_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]')
                                                                                                    
            #all_writers = browser.find_element_by_css_selector("div.q-box").find_elements_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]')
            print(all_writers)
                                                                                                   #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]
            #all_writers = browser.find_element_by_css_selector("div.q-box")
            #all_writers = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]')
            #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1] - list of writers now
            #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div/div - previous
            for each_writer in range(total_requests):
                sleep(0.8)
                print(each_writer)
                #print(all_writers[each_writer])
                #send_request = all_writers[each_writer].find_element_by_css_selector("div.ui_layout_text").find_element_by_css_selector("div.button_wrapper:not(.pop_in)")
                send_request = all_writers[each_writer].find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[{}]/div/div/div/div[3]/div'.format(each_writer+2)) #request button WORKING FOR ONE
                #send_request = all_writers[each_writer].find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[{}]/div/div/div/div[3]/div'.format(each_writer+2))
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div/div/div/div[3]/div/div/div/span/span/svg/g/circle
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/span/span/svg/g/circle
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[4]/div/div/div/div[3]/div/div/div/span/span/svg/g/circle
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[12]
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[10]
                #//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div/div/div/div[3]/div    request button
                send_request.click()
                browser.execute_script("window.scrollTo(0, 5)")
        except:
            print("Answer limit reached or Question is a sensitive question, and for that you have to manually request for answers")
            pass

        sleep(0.9)
        try:
            #done_btn = browser.find_element_by_css_selector("div.modal_overlay:not(.hidden)").find_element_by_css_selector("div.modal_wrapper.normal:not(.hidden)").find_element_by_css_selector("div.modal_actions").find_element_by_css_selector("a.ui_button--PillStyle--bright_blue")
            #done_btn = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/button').click()
            #done_btn = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/button/div/div/div')
            #done_btn = browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/button")
            continue
        except:
            #done_btn = browser.find_element_by_xpath('//*[@id="react_loadable"]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/button/div/div/div')
            print("done")
        
        #done_btn.click()
        sleep(0.5)

    return browser.quit()

send_requests(max_wait=10)