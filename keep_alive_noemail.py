from flask import Flask
from threading import Thread
from app import run_app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
import json
from flask import Markup
from flask import Flask
from flask import render_template, flash, redirect
import os
from flask_mail import Mail, Message
from forms import LoginForm

app = Flask('')






@app.route('/', methods=["GET", "POST"])
def home():
    with open("data_file.json") as f:
        appointments = json.load(f)

    appointments_string2 = ""

    with open("last_check.json") as f:
        time_json = json.load(f)

    time_check = time_json["last_check"]

    for x in appointments["appointments"]:
        if x["available"] == True:
            appointments_string2 += "---------------------------------------------<br>"
            appointments_string2 += x["date"] + "<br><br>"
            appointments_string2 += x["location"] + "<br>"

       
    appt_html2 = Markup(appointments_string2)
            
    form = LoginForm()

    if form.validate_on_submit():
        
        flash('E-mail address %s will be updated when appointments are available!' % form.Email.data)
        with open("emaillist.json") as f:
            emaillist = json.load(f)
        emaillist["e-mail"].append(form.Email.data)
        with open("emaillist.json", "w") as write_file:
            json.dump(emaillist, write_file)
        return redirect('/')
        

    return render_template('home.html', appt2=appt_html2, time=time_check, form=form)

@app.route('/go')
def go():
    t = Thread(target=run_app())
    return "Updating Appointment info..."


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
