#Importing all the necessary packages

from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.keys import Keys
from email.mime.base import MIMEBase
from email import encoders
import time
import re
import pandas as pd

def main():
    #Critical fields for authorization of the app.
    hp = "foo_bar loves some foo" #Your Virginia Tech email Password
    he = "foo" #Your Virginia Tech PID 
    email_user = 'foo_bar@gmail.com' #The email you want to send from
    email_password = 'foo_baratbarfoo' #The password for the email you want to send from
    email_send = 'bar_foo@gmail.com' #the email you want to send to

    #Logging in to canvas
    br = webdriver.Chrome(executable_path=r"C:/Users/qasim/Downloads/chromedriver_win32/chromedriver.exe")
    br.get('http://canvas.vt.edu')
    time.sleep(3)
    username = br.find_element_by_id("username")
    username.send_keys(he)
    password = br.find_element_by_id("password")
    password.send_keys(hp)
    time.sleep(1)
    button = br.find_element_by_name("_eventId_proceed")
    button.click()
    time.sleep(15)

    #Scrolling through the feed to tackle pagination
    x = ".View__ehkxkl-root.Button__dUxGkD-root.Button__dUxGkD-link.Button__dUxGkD-medium.Button__dUxGkD-width--auto.Button__dUxGkD-borderRadius--rounded"
    y = ".ToggleDetails__ettLPz-toggle"


    loadMore = br.find_elements_by_css_selector(x)

    links = []

    allCompletedAssignments = []

    whenAssignment = []
    "Function to load all events"
    def duo(times):
        for c in range(0,times+1):
            time.sleep(1)

            load_more_button = br.find_elements_by_css_selector(".czbXA_bGBk.bavIU_bGBk.bavIU_brAJ.bavIU_ycrn.bavIU_bNlk.bavIU_cuTS")[-1]
            if(load_more_button.text == 'Load more'):
                load_more_button.click()
        br.find_element_by_css_selector("#planner-today-btn").click()
    "End of Function"    


    duo(2)


    zzz = ".czbXA_bGBk.czbXA_UeJS.cIcZl_bGBk.cIcZl_bOQC"
    allAss = br.find_elements_by_css_selector(zzz)
    for x in range(len(allAss)):
        allCompletedAssignments.append(allAss[x].text)
    xxx = ".ELpHc_bGBk.ELpHc_dfBC.ELpHc_eQnG.ELpHc_bLsb"
    abc = br.find_elements_by_css_selector(xxx)
    for t in range(len(abc)):
        if(t%2 == 0):
            whenAssignment.append(abc[t].text)

    #Data analysis and storing different types of data into different lists
    links = allAss
    nameOfAssignment = []
    monthRegex = []
    dateAndRest = []
    dateNum = []
    brevity = []
    error = ".CloseButton__fPgxVp-root.CloseButton__fPgxVp-placement--end.CloseButton__fPgxVp-offset--x-small"
    for x in range(len(links)):
        nameOfAssignment.append(links[x].text)
    for y in range(len(nameOfAssignment)):
        nameOfAssignment[y] = nameOfAssignment[y].split("\n")
        brevity.append(nameOfAssignment[y][1])
        monthRegex.append(re.findall(r'.January|February|March|April|May|June|July|August|September|October|November|December',nameOfAssignment[y][0]))
        dateAndRest.append(nameOfAssignment[y][0].partition(monthRegex[y][0])[2].partition("2019")[0:3])
        dateNum.append(monthRegex[y][0] + "," + dateAndRest[y][0].split(",")[0] + " " + dateAndRest[y][1] + dateAndRest[y][2])

    #making a unified list from all lists
    details = list(zip(brevity,whenAssignment,dateNum))
    #creating a dataframe
    df = pd.DataFrame(data=details,columns=['Assignment Name','Class Name','Due Date'])
    #creating a .csv file and exporting dataframe object to it
    df.to_csv('homeworkCanvasHack.csv',index=False,encoding='utf-8')

    #email connection and sending the email with an attachment to the desired address
    subject = 'Homework Hack using Python'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Here\'s a list of homework assigned to you. More soul-crunching and meaningless work for corrupt organizations...'
    msg.attach(MIMEText(body,'plain'))

    filename = 'homeworkCanvasHack.csv'
    attachment  = open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()

if __name__ == "main":
    main() #Running main()
