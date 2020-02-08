"""
A automation script used to keep track of price drops of products sold on www.amazon.co.uk

Code written by Michael Zhou
"""

# Imported libraries used to:
# Make HTTP requests
import requests
# Extract data out of HTML and XML files
from bs4 import BeautifulSoup   
# Simple Mail Transfer Protocol library
import smtplib 
# Hides user input
import getpass
# Timer functionality
import time


# Prompts user to input an URL link into the program
URL = input("Copy and paste a URL link here: ")

# Every time your web browser makes a request to a website, it sends a HTTP Request Header called the "User Agent". 
# The "User Agent" string contains information about your web browser name, operating system, device type etc
# You may need to change this depending on your configuration by googling "My User Agent"
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}


# Function to check for changes in price from the URL link 
def check_price():
    # Returns all the data from the website link 
    page = requests.get(URL, headers=headers)

    # Parses the information from the link to retrieve metadata from it
    soup = BeautifulSoup(page.content, "html.parser")

    # Retrieves the title of the product
    title = soup.find(id="productTitle").get_text()

    # Retrieves the existing price of the product 
    price = soup.find(id="priceblock_ourprice").get_text()

    # Converts the existing price from a string to a float 
    converted_price = float(price[1:])

    # Prompts user to enter their desired target price drop
    desired_price = input("We'll send you an email when the price drops below: £")

    # Converts the desired price entered from a string to a float
    converted_desired_price = float(desired_price)

    # Conditional statement to send an email if a price drop occurs
    if(converted_price < converted_desired_price):
        # Prompt user to enter their user login details
        email_address = input('Email Address: ')
        password = getpass.getpass()
        # Invokes the send_mail function
        send_mail(email_address, password)

    # Outputs name of the product, current price and desired price
    print("Product Title: " + title.strip())
    print("Current Price: " + price)
    print("Desired Price: " + desired_price)


# Function to send an email to the user if there has been a price drop
def send_mail(email_address, password):
    # Establishes a server connection
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Server issues a command sent by an email server to identify itself when connecting to another email server 
    server.ehlo()

    # Encrypts the connection between the two servers
    server.starttls()

    # Server issues another command to identify itself 
    server.ehlo()

    # Authenticates user log in to the server via email and password
    server.login(email_address, password)

    # Default email subject and body text
    subject = 'Price Drop Alert!'
    body = 'Check out the following amazon link: ' + URL

    # Formats the message 
    msg = f"Subject: {subject}\n\n{body}"

    # Performs sending mail transaction
    server.sendmail(
        replace_with_your_email_address,   # Sender
        replace_with_your_email_address,   # Recipient
        msg                                # Message Content
    )

    # Confirmation that an email has been sent
    print('Email has been sent!')

    # Terminates the server connection once email has been sent
    server.quit()


# Invokes the check_price function once on a daily basis
while(True):
    check_price()
    time.sleep(86400)
