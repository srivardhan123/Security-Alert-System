import RPi.GPIO as gpio
import time
from cv2 import *

# make sure to have the drivers folder on the same parent folder as this python file
import drivers

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

# Set the GPIO pins ids
led=5
buzzer=6
pir=4

HIGH=1
LOW=0
#for disabeling warnings 
gpio.setwarnings(False)
#It tells the library which pin nunbering system you are going to use
gpio.setmode(gpio.BCM)

# Output GPIO pins 
gpio.setup(led, gpio.OUT)            
gpio.setup(buzzer, gpio.OUT)         

# Input GPIO pins 
gpio.setup(pir, gpio.IN)        
data=""

# Setup LED and buzzer
gpio.output(led, LOW)
gpio.output(buzzer, LOW)

# Configure the to and from email address 
from_email =  "raspberrycream47@gmail.com"
from_email_pwd = "mtewqifakahwgqvd" 

to_email = "prateekrajesh000@gmail.com"
 
mail = MIMEMultipart()

mail['From'] = from_email
mail['To'] = to_email
mail['Subject'] = "Someone is at Your Doorstep! "
body = "motion detected"

# Setup camera


# Setup LCD display from the driver package
display = drivers.Lcd()

# Function to send the mail to the owner with images attached

def sendMail(data):

    # Create mail object with image attachment and text
    #mail.attach(MIMEText(body, 'plain'))
    print('hy')
    dat='hy.jpg'%data
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)

    # Estabilish connection and send the mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_email_pwd)
    text = mail.as_string()
    server.sendmail(from_email, to_email, text)

    # Notify that mail has been sent in LCD and console
    print('Mail Sent')
    display.lcd_clear()
    display.lcd_display_string("Mail Sent", 1)

    server.quit()
    
def capture_image():
    # Capture the image and save the name as the time
    #data = time.strftime("%d_%b_%Y|%H:%M:%S")
    #camera.start_preview()
    #time.sleep(3)
    #camera.capture('%s.jpg'%data)
    #camera.stop_preview()
    # program to capture single image from webcam in python

# importing OpenCV library


# initialize the camera
# If you have multiple camera connected with
# current device, assign a value in cam_port
# variable according to that
  cam_port = 0
  cam = VideoCapture(cam_port)

# reading the input using the camera
  result, image = cam.read()

# If image will detected without any error,
# show result
  if result:
	  imshow("img", image)
	  imwrite("img.jpg", image)
	  waitKey(0)
	  destroyWindow("img")
  else:
	  print("No image detected. Please! try again")

    # Send the mail
  sendMail(image)

# Run a forever loop
while 1:
    # PIR sensor detects any motion
    if gpio.input(pir)==1:
        # Trigger the led and buzzer
        gpio.output(led, HIGH)
        gpio.output(buzzer, HIGH)

        # Display that intrusion has been detected in the LCD and console
        print('Intrusion Detected')
        display.lcd_clear()
        display.lcd_display_string("motion", 1)
        display.lcd_display_string("Detected", 2)

        # Capture the image and send the mail
        capture_image()
        #gpio.setup(pir,False)
        # Wait for the PIR sensor to not detect any motion
        while(gpio.input(pir)==1):
            time.sleep(1)
        #gpio.setup(pir,False)
    # PIR sensor doesn't detect any motion
    else:
        # Turn off LED and buzzer and clear the LCD display
        time.sleep(5)
        gpio.output(led, LOW)
        gpio.output(buzzer, LOW)
        display.lcd_clear()
        