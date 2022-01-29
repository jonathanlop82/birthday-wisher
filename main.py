##################### Extra Hard Starting Project ######################

import datetime as dt
import csv
from csv import writer
import random
import shutil
import smtplib
import credentials

name_birthday = ''
email_birthday = ''
new_letter = ''

# 1. Update the birthdays.csv
def input_data():
    day = int(input("Give me your birthday day: "))
    month = int(input("Give me your birthday month: "))
    year = int(input("Give me your year birthday: "))
    name = input("Give me your name: ")
    email = input("Give me your email: ")

    new_birthday = [name,email,year,month,day]

    return new_birthday


# 2. Check if today matches a birthday in the birthdays.csv

def check_birthday():
    today = dt.datetime.now()
    global name_birthday
    global email_birthday


    with open("birthdays.csv", newline='') as csvfile:
        birthday_data = csv.reader(csvfile, delimiter=',')
        next(birthday_data)
        for row in birthday_data:
            if int(row[3]) == today.month and int(row[4]) == today.day:
                #print(f"Feliz Cumpleaños {row[0]}")
                name_birthday = row[0]
                email_birthday = row[1]
                return True

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

def select_a_letter():

    global name_birthday, new_letter

    num_letter = random.randint(1,3)
    select_letter = f"letter_templates/letter_{num_letter}.txt"
    new_letter = f"letter_{num_letter}.txt"

    original = select_letter
    target = new_letter

    shutil.copyfile(original, target)

    with open(new_letter, "r") as file:
        letter = file.read()
        letter = letter.replace("[NAME]",name_birthday)

    with open(new_letter, "w") as file:
        file.write(letter)

# 4. Send the letter generated in step 3 to that person's email address.

def send_email():
    global name_birthday, email_birthday, new_letter

    my_email = credentials.my_email
    password = credentials.password

    with open(new_letter) as file:
        letter = file.read()

    with smtplib.SMTP("smtp.gmail.com") as conection:
        conection.starttls()
        conection.login(user=my_email, password=password)
        conection.sendmail(from_addr=my_email, to_addrs=email_birthday,
                           msg=f"Subject:Happy Birthday!!!\n\n{letter}")


add_birthday = input("Can you add new birthday day (yes/no)?: ")

if add_birthday == 'yes':

    with open("birthdays.csv", 'a', newline='') as csvfile:
        #birthday_data= csv.reader(csvfile, delimiter=',')
        birthday_data = writer(csvfile)
        new_birthday = input_data()
        birthday_data.writerow(new_birthday)
        csvfile.close()


if check_birthday():
    select_a_letter()
    send_email()

