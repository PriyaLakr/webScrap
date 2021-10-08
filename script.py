## Adapted from tutorial: https://www.youtube.com/watch?v=s8XjEuplx_U 
# Task: Extract information from a web page and automatically send an email


## import pkgs
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


## print current time
now = datetime.datetime.now()


## email content placeholder
content = ''


## extracting Hacker news stories
def extract_news(url):
    '''extracting Hacker news stories
    '''
    info = ''
    info += ('<b>Hacker News Top Stories:</b>\n' + '<br>' + '.'*50 + '<br>')
    
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    
    for num,tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
        info += ((str(num+1) + '::' + tag.text + '\n' + '<br>') if tag.text != 'More' else '')
    return info


### url of hacker news website
url = 'https://news.ycombinator.com/'


info = extract_news(url)
content += info
content += ('<br>-----------------<br>')
content += ('<br><br>End of Message')


## setting up email details 
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '***2@gmail.com'
TO = '****@gmail.com'
password = '*******' # add you passwrd here

msg = MIMEMultipart()

msg['Subject'] = '[Automated] Hacked your account' + str(now.day) + '/' + str(now.month) + '/' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))


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
