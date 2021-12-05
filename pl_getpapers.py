# retrieve all papers of an author from NCBI Pubmed

# importing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
### import this error so as that we can handle it by raising an exception 
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


url = "https://pubmed.ncbi.nlm.nih.gov/"
author = input(str(f"which author you want to search?:"))


# service step is added as executable_path is deprecated 
ser = Service("/Users/priyalakra/Desktop/webscrapping_know/webdrivers/chromedriver")
driver = webdriver.Chrome(service=ser)

driver.get(url)

search_bar = driver.find_element(by="xpath", value="//div[@class='form-field ']/span[@class='twitter-typeahead ncbi-autocomplete']/input")

search_bar.click()

search_bar.send_keys(author)

button = driver.find_element(by="xpath", value="//div[@class='form-field ']/button[@class='search-btn']")
button.click()

author_list = []
papers_list = []


authors = driver.find_elements(by="xpath", value="//div[@class='docsum-citation full-citation']/span[@class='docsum-authors full-authors']")
author_list += [author.text for author in authors]
papers = driver.find_elements(by="xpath", value="//div[@class='docsum-content']/a[@class='docsum-title']")
papers_list += [paper.text for paper in papers]    
    
while True:
    
    showmore = driver.find_element(by="xpath", value="//div[@class='search-results']/div[@class='bottom-pagination']/button[@class='button-wrapper next-page-btn']/label")
    try:
        showmore.click()
        authors = driver.find_elements(by="xpath", value="//div[@class='docsum-citation full-citation']/span[@class='docsum-authors full-authors']")
        author_list += [author.text for author in authors]
        papers = driver.find_elements(by="xpath", value="//div[@class='docsum-content']/a[@class='docsum-title']")
        papers_list += [paper.text for paper in papers]    
    except ElementClickInterceptedException:
        print('no more pages')
        break
        
driver.close()

# write to a file
with open(f"{author}_papers.text", 'w') as f:
    for i in range(len(author_list)):
        f.write(f"{author_list[i]} {papers_list[i]}\n\n")

print(f"{author}_papers.text file stored in {os.getcwd()} directory")


# automated mail the text file 
## print current time
now = datetime.datetime.now()

## setting up email details 
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = input(str(f"send mail from id?:"))
TO = input(str(f"send mail to id?:"))
password = input(str(f"add you passwrd here:"))

msg = MIMEMultipart()

msg['Subject'] = '[Automated] Papers' + str(now.day) + '/' + str(now.month) + '/' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

file = f"{author}_papers.text"
msg.attach(MIMEText("List of papers is attached as a separate text file with this mail!"))

with open(file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    
encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    "attachment", filename=file)
msg.attach(part)

## initializing server
server = smtplib.SMTP(SERVER, PORT)

### if you want to see any debug (error) msg then type 1 else 0
server.set_debuglevel(1)

server.ehlo()
server.starttls()
server.login(FROM, password)
server.sendmail(FROM, TO, msg.as_string())

print('email sent....')

server.quit()
