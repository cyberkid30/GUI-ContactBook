import mysql.connector
import random
import pathlib
import os
import shutil

file_path = pathlib.Path(__file__).parent.resolve()

print("<=If the profile does not exist new profile will be created and contacts will be imported to the new created profile=>")
name = input("Enter name of profile you want to import contacts:")
logged_file = open("logged.txt", "w")
logged_file.write(name)
logged_file.close()
cont_numb = random.randint(8, 15)

path = str(file_path) + "\\Dependencies\\User Data"
list_files = os.listdir(path)

sql = open("sqlpass.txt", "r+")
sql_pass_temp = sql.readline()
sql_pass = sql_pass_temp.replace("\n", "")

if sql.readline() == "":
    sql_password = input("Enter password for SQL:")
    computername = os.environ['COMPUTERNAME']
    temp = open("sqlpass.txt", "w")
    temp.write(sql_password)
    temp.write("\n"+computername)
    temp.close()
    sql_pass = sql_password
else:
    pass
    

if name in list_files:
    pass
else:
    os.mkdir(f"{path}\\{name}")

# Database Initiation
try:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sql_pass,
        database="ContactBook"
    )

except:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sql_pass
    )

# Cursor Initiation
mycursor = mydatabase.cursor()

# Database Creation
mycursor.execute("CREATE DATABASE IF NOT EXISTS ContactBook")
mycursor.execute("USE ContactBook")

# Table Creation
mycursor.execute(
    f"CREATE TABLE IF NOT EXISTS {str(name)}Contacts (NAME VARCHAR(255), CONTACT BIGINT(12), EMAIL VARCHAR(255), DOB VARCHAR(11) DEFAULT 'NULL', CATEGORY VARCHAR(7), PROFILE_LOCATION VARCHAR(255))")

name_contact, contact_contact, email_contact, category_contact, dob_contact = [], [], [], [], []

name_contact_choices = ["Shinichi", "Shino", "Mello", "Mitshua", "Eren", "Lelouch", "Miko", "Shiro", "Ishigami", "Ryuk",
                        "Levi", "Kirito", "Asuna", "Komi", "Light"]

contact_contact_choices = ["9876453215", "9060193063", "9909876126", "9874562345", "8563456234", "9867434567",
                           "6743215467", "9087123780", "9123456870", "6789017765", "9362140586", "7412365891",
                           "9856321456", "8546217002", "9966332145"]
email_contact_choices = ["", "", "", "", "", "", "", "s19@yahoo.com", "mhs@gmail.com", "m3044@gmail.com", "h3304@gmail.com",
                         "s1904@gmail.com", "m30@hotmail.com", "h03@yahoo.com", "smh@yahoo.com"]
dob_choice = ["2004/04/30", "2004/06/16", "2004/03/03", "2004/03/19", "2000/08/24", "1990/05/19", "1999/08/09", "2001/12/25",
              "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
category_contact_choices = ["Family", "Friend", "Work", "Other", "Other"]

for i in range(0, cont_numb):
    name_cont = random.choice(name_contact_choices)
    contact_cont = random.choice(contact_contact_choices)
    email_cont = random.choice(email_contact_choices)
    dob_cont = random.choice(dob_choice)
    category_cont = random.choice(category_contact_choices)

    name_contact_choices.remove(name_cont)
    contact_contact_choices.remove(contact_cont)
    email_contact_choices.remove(email_cont)
    dob_choice.remove(dob_cont)

    name_contact.append(name_cont)
    contact_contact.append(contact_cont)
    email_contact.append(email_cont)
    dob_contact.append(dob_cont)
    category_contact.append(category_cont)

name_contact_length = len(name_contact)

for i in range(0, name_contact_length):
    name_store = name_contact[i]
    contact_store = contact_contact[i]
    email_store = email_contact[i]
    dob_store = dob_contact[i]
    category_store = category_contact[i]

    path = str(file_path) + "\\Dependencies\\User Data\\Test\\"
    list_of_files = os.listdir(path)

    PROFILE_LOCATION = str(file_path) + "\\Dependencies\\User Data\\Test\\" + name_store + "_see.png"
    temp_PROFILE = str(file_path) + "\\Dependencies\\User Data\\Test\\" + name_store + ".png"

    dest = str(file_path) + "\\Dependencies\\User Data\\" + name + "\\"
    shutil.copy(PROFILE_LOCATION, dest)
    shutil.copy(temp_PROFILE, dest)

    Formula = "INSERT INTO " + name + "contacts(name, contact, email, DOB, Category, PROFILE_LOCATION) VALUES(%s, %s, %s, %s, %s, %s)"
    contact_save = (name_store, contact_store, email_store, dob_store, category_store, PROFILE_LOCATION)
    mycursor.execute(Formula, contact_save)
    mydatabase.commit()

print("\nAccount is generated with", cont_numb, " Contacts.")

input("\nPress ANY KEY to redirect to MainScreen...")
os.system("ContactBOok.py")
quit()
