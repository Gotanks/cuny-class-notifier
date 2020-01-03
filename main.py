from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from playsound import playsound

import time, re, os, getpass, sys, argparse


def main():
    classnum = -1
    institution = ""
    term = ""
    year = -1
    subject = ""
    cunyfirstlogin = ""
    cunyfirstpassword = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--classnum", help="class number", type=int)
    parser.add_argument("--institution",
                        help="college name in full eg. Queens College",
                        type=str)
    parser.add_argument("--term",
                        help="Spring, Summer, Fall, Winter",
                        type=str)
    parser.add_argument("--year", help="YYYY", type=int)
    parser.add_argument("--subject",
                        help="Subject name in full eg. Computer Science",
                        type=str)
    parser.add_argument("--visible",
                        help="Makes the browser visible",
                        action="store_true")
    parser.add_argument("--cunyid", help="Cuny ID", type=str)
    parser.add_argument("--password",
                        help="password for Cunyfirst username",
                        type=str)
    
    args = parser.parse_args()
    if args.classnum:
        print("Class " + str(args.classnum) + " selected")
        classnum = args.classnum
    if args.institution:
        print("Institution " + args.institution + " selected")
        institution = args.institution
    if args.term:
        print("Term " + args.term + " selected")
        term = args.term
    if args.year:
        print("Year " + str(args.year) + " selected")
        year = args.year
    if args.subject:
        print("Subject " + args.subject + " selected")
        subject = args.subject
    if args.cunyfirstlogin:
      print("Cunyfirst username " + args.cunyfirstlogin + " selected")
      cunyfirstlogin = args.cunyfirstlogin

    if args.cunyfirstpassword:
      print("Cunyfirst password " + str(cunyfirstpassword) + " selected")
      cunyfirstpassword = cunyidpassword

    if not args.institution:
        institution = institutionmenu()
        print("Institution " + institution + " selected")

    if not args.year:
        year = yearmenu()
        print("Year " + str(year) + " selected")

    if not args.term:
        term = termmenu()
        print("Term " + term + " selected")

    if not args.subject:
        subject = subjectmenu()
        print("Subject " + subject + " selected")

    if not args.classnum:
        classnum = classmenu()
        print("Class " + str(classnum) + " selected")
    
    if not args.cunyfirstlogin:
        cunyfirstlogin = cunyidmenu()
        print("Cunyfirst username " + str(cunyfirstlogin) + " selected")
    
    if not args.cunyfirstpassword:
        cunyfirstpassword = cunyidpassword
        print("Cunyfirst password " + str(cunyfirstpassword) + " selected")

    # print all vars and ask the user is this correct? if not we ask again, if yes then we run
    flag = False

    options = Options()
    #options.binary_location = "C:/Program Files (x86)/Google/Chrome Beta/Application/chrome.exe"
    if not args.visible:
        options.add_argument('headless')
    driver = webdriver.Chrome(
        chrome_options=options,
        executable_path="C:/Downloads/chromedriver_win32/chromedriver.exe",
    )
    driver.get("https://globalsearch.cuny.edu/")
    collegeID = driver.find_elements_by_xpath("//*[contains(text(), '" +
                                              institution +
                                              "')]")[0].get_attribute("for")
    driver.find_element_by_id(collegeID).click()
    selecttermyear = Select(driver.find_element_by_id('t_pd'))
    selecttermyear.select_by_visible_text(str(year) + " " + term + " Term")
    driver.find_element_by_name('next_btn').click()

    selectsubject = Select(driver.find_element_by_id('subject_ld'))
    selectsubject.select_by_visible_text(str(subject))
    selectcareer = Select(driver.find_element_by_id('courseCareerId'))
    selectcareer.select_by_visible_text('Undergraduate')
    driver.find_element_by_id(
        'open_classId').click()  #uncheck open classes only
    driver.find_element_by_id('btnGetAjax').click()
    classhtml = collegeID = driver.find_elements_by_xpath(
        "//*[contains(text(), '" + str(classnum) + "')]")[0].get_attribute("href")

    while not flag:
        driver.get(str(classhtml))
        classstatus = driver.find_element_by_id(
            'SSR_CLS_DTL_WRK_SSR_DESCRSHORT').get_attribute('innerHTML')
        if classstatus == "Open":
#             
#           This code will be used once a class has been found open and log into cunyfirst
#           using the cunyfirst login credentials
#           
# 
#             
            # flag = True
            # for x in range(10):
            #     playsound('sound.mp3')
            #     time.sleep(1)
        # print(classstatus)
          break #temporary break
def SignUp(driver, term, classnum):
    email = cunyidmenu()
    password = cunyidpassword()
    driver.get("https://cunyfirst.cuny.edu")
    Usernameinput = driver.find_element_by_id("CUNYfirstUsernameH")
    Usernameinput.clear()
    Usernameinput.send_keys(email)
    PasswordInput = driver.find_element_by_id("CUNYfirstPassword")
    PasswordInput.send_keys(password)
    driver.find_element_by_id("submit").click()
    time.sleep(3)
    ElementList = driver.find_elements_by_tag_name("tr")
    print(len(ElementList))
    SCElement = driver.find_element_by_id("crefli_HC_SSS_STUDENT_CENTER")
    SCElement.find_element_by_tag_name("a").click()
    time.sleep(3)
    frame = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(frame)
    EnrElement = driver.find_element_by_xpath("//*[contains(text(),'Enroll')]").click()
    #get the element id which contains Semester
    time.sleep(3)
    ID = driver.find_element_by_xpath("//*[contains(text(),'" + term + "')]").get_attribute("id")[-1]
    print(ID)
    #combine the id with the expected Radio Button id
    RadioID = "SSR_DUMMY_RECV1$sels$" + ID + "$$0"
    #search for element with RadioID
    driver.find_element_by_id(RadioID).click()
    driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
    time.sleep(3)
    classbox = driver.find_element_by_id("DERIVED_REGFRM1_CLASS_NBR")
    classbox.send_keys(classnumber)
    driver.find_element_by_id("DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$").click()
    time.sleep(1)
    driver.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB$280$").click()

def yearmenu():
    return input("Enter a year: ")


def classmenu():
    return input("Enter a 5 digit class number: ")

def termmenu():
    choice = '0'
    while choice == '0':
        print("Choose a term")
        print("Choose 1 for Spring")
        print("Choose 2 for Summer")
        print("Choose 3 for Fall")
        print("Choose 4 for Winter")

        choice = input("Please make a choice: ")

        if choice == "4":
            return "Winter"
        elif choice == "3":
            return "Fall"
        elif choice == "2":
            return "Summer"
        elif choice == "1":
            return "Spring"
        else:
            print("I don't understand your choice.")


def subjectmenu():
    choice = '0'
    while choice == '0':
        print("Choose a subject")
        print("Choose 1 for Computer Science")
        print("Choose 2 for Mathematics")
        print("Choose 3 for Other")

        choice = input("Please make a choice: ")

        if choice == "1":
            return "Computer Science"
        elif choice == "2":
            return "Mathematics"
        elif choice == "3":
            return input("Enter FULL subject name: ")
        else:
            print("I don't understand your choice.")


def institutionmenu():
    choice = '0'
    while choice == '0':
        print("Choose a college")
        print("Choose 1 for Queens College")
        print("Choose 2 for Other")

        choice = input("Please make a choice: ")

        if choice == "1":
            return "Queens College"
        elif choice == "2":
            return input("Enter FULL institution name: ")
        else:
            print("I don't understand your choice.")


def cunyidmenu():
  return input("Please enter your Cunyfirst username ")


def cunyidpassword():
  return input("Please enter your Cunyfirst password ")

main()
