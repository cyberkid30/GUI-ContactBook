# Inbuilt Modules
import os
import pathlib
import numpy as np

# Installed Modules
from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageDraw

file_path = pathlib.Path(__file__).parent.resolve()
print(file_path)

# Opening of logged.txt file to get name of currently logged_in user
logged = open("logged.txt", "r+")
name_logged = logged.readline()

sql = open("sqlpass.txt", "r+")
sql_pass_temp = sql.readline()
sql_pass = sql_pass_temp.replace("\n", "")

if os.environ['COMPUTERNAME'] == sql.readline():
    pass
else:
    sql_password = input("Enter password for SQL:")
    computername = os.environ['COMPUTERNAME']
    temp = open("sqlpass.txt", "w")
    temp.write(sql_password)
    temp.write("\n"+computername)
    temp.close()
    sql_pass = sql_password


print("<=If the profile does not exist then a new profile will be created=>")
name_user = input("Enter name of profile you want to use\n=")
logged = open("logged.txt", "w")
logged.write(name_user)
name_logged = name_user


path = str(file_path) + "\\Dependencies\\User Data"
list_files = os.listdir(path)

if name_logged in list_files:
    pass
else:
    os.mkdir(f"{path}\\{name_logged}")


# MainScreen ImagePath
folder_location_main = str(file_path) + "\\Dependencies\\images\\ContactMainScreen\\"

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
mycursor.execute(f"CREATE TABLE IF NOT EXISTS {str(name_logged)}Contacts (NAME VARCHAR(255), CONTACT BIGINT(12), EMAIL VARCHAR(255), DOB VARCHAR(11) DEFAULT 'NULL', CATEGORY VARCHAR(7), PROFILE_LOCATION VARCHAR(255))")


def destroy(): window.destroy()


def add_contact(name="*Full Name", contact="*Contact", category="Work/Family/Friend/Other", email="E-mail", dob="DOB:YYYY/MM/DD", profile_path=""):
    """This is function for adding contact"""
    try:
        destroy()
    except:
        pass

    global file_path
    global label2

    get_path = profile_path

    # GUI Window Initiation and Config
    addwindow = Tk()
    addwindow.geometry('600x700')
    addwindow.maxsize(600, 700)
    addwindow.minsize(600, 700)
    addwindow.title("Add Contact")


    def del_widg(widget, *args):
        if name == "*Full Name":
            if widget == "Name":
                NameEntryBox.delete(0, END)
            elif widget == "Contact":
                ContactEntryBox.delete(0, END)
            elif widget == "Email":
                EmailEntryBox.delete(0, END)
            elif widget == "Category":
                CategoryEntryBox.delete(0, END)
            elif widget == "DOB":
                DOBEntryBox.delete(0, END)
        else:
            pass

    def cancel(*args):
        """Function for Cancel button which on click takes user back to MainWindow of Contacts"""
        addwindow.destroy()
        main()

    def submit(*args):
        """Function which is executed to save the contact on clicking SubmitButton"""
        global file_path
        try:
            name1 = NameEntryBox.get()
            contact1 = ContactEntryBox.get()
            email1 = EmailEntryBox.get()
            dob1 = DOBEntryBox.get()
            Category1 = CategoryEntryBox.get()

            path = str(file_path) + "\\Dependencies\\User Data\\" + name_logged + "\\"
            list_of_files = os.listdir(path)

            if name1 + str("_see.png") in list_of_files:
                PROFILE_LOCATION = str(file_path) + "\\Dependencies\\User Data\\" + name_logged + "\\" + str(
                    name1) + "_see.png"

            else:
                PROFILE_LOCATION = str(file_path) + "\\Dependencies\\User Data\\Default.png"

            if name1 == "" and contact1 == "" or contact1 == "" or name1 == "":
                messagebox.showerror("IMP", "Required field are missing")

            if email1 == 'E-mail' or email1 == "":
                email1 = ""

            if dob1 == 'DOB:YYYY/MM/DD' or dob1 == "":
                dob1 = "N/A"

            if Category1 == "Work/Family/Friend/Other" or Category1 == "Other":
                Category1 = "Other"

            elif Category1 != "Work" or Category1 != "Family" or Category1 != "Friend":
                Category1 = "Other"

            Formula = "INSERT INTO " + name_logged + "contacts(name, contact, email, DOB, Category, PROFILE_LOCATION) VALUES(%s, %s, %s, %s, %s, %s)"
            contact_save = (name1, contact1, email1, dob1, Category1, PROFILE_LOCATION)

            mycursor.execute(Formula, contact_save)

            mydatabase.commit()

            addwindow.destroy()
            main()

        except:
            pass

    def edit_submit():
        name1 = NameEntryBox.get()
        contact1 = ContactEntryBox.get()
        email1 = EmailEntryBox.get()
        dob1 = DOBEntryBox.get()
        Category1 = CategoryEntryBox.get()

        path = str(file_path) + "\\Dependencies\\User Data\\" + name_logged + "\\"
        list_of_files = os.listdir(path)

        file_path2 = str(file_path).replace("\\", "\\\\")

        if name + str("_see.png") in list_of_files:
            target1 = path + name + "_see.png"
            target2 = path + name + ".png"
            dest1 = path + name1 + "_see.png"
            dest2 = path + name1 + ".png"

            os.rename(target1, dest1)
            os.rename(target2, dest2)

        if name + str("_see.png") in list_of_files:
            PROFILE_LOCATION1 = str(file_path2) + "\\\\Dependencies\\\\User Data\\\\" + name_logged + "\\\\" + str(
                name1) + "_see.png"
        else:
            PROFILE_LOCATION1 = str(file_path2) + "\\\\Dependencies\\\\User Data\\\\Default.png"

        if name1 == "" and contact1 == "" or contact1 == "" or name1 == "":
            messagebox.showerror("IMP", "Required field are missing")

        if email1 == 'E-mail' or email1 == "":
            email1 = ""

        if dob1 == 'DOB:YYYY/MM/DD' or dob1 == "":
            dob1 = "N/A"

        if Category1 == "Work/Family/Friend/Other" or Category1 == "Other":
            Category1 = "Other"

        elif Category1 != "Work" or Category1 != "Family" or Category1 != "Friend":
            Category1 = "Other"
        Formula = f"UPDATE {name_logged}CONTACTS SET NAME=\'{name1}\', CONTACT={contact1},email=\'{email1}\', DOB=\'{dob1}\', " \
                  f"Category=\'{Category1}\', PROFILE_LOCATION=\'{PROFILE_LOCATION1}\' WHERE NAME=\'{name}\'"

        mycursor.execute(Formula)
        mydatabase.commit()

        addwindow.destroy()
        main()

    def change(e):
        """Function that changes tht image on hovering the cursor over the image"""
        global cam_pic

        change_path = str(file_path) + "\Dependencies\images\Add_Contact\Profile_Change.png"
        cam_pic = PhotoImage(file=change_path)
        default_pic.config(image=cam_pic)

    def undo_change(e):
        """Function that change image back to normal when cursor is not hovering"""
        global default_pic1

        path = str(file_path) + "\\Dependencies\\User Data\\" + name_logged + "\\"
        list_of_files = os.listdir(path)

        try:
            namecont = NameEntryBox.get()
        except:
            namecont = name

        if name != "*Full Name":
            temppath = get_path.replace("_see", "")
            default_pic1 = PhotoImage(file=temppath)
            default_pic.config(image=default_pic1)

        else:
            if namecont + str(".png") in list_of_files:
                cpath = str(file_path) + "\\Dependencies\\User Data\\" + name_logged + "\\" + str(namecont) + str(".png")
                default_pic1 = PhotoImage(file=cpath)
                default_pic.config(image=default_pic1)

            else:
                defprofile_path = str(file_path) + "\\Dependencies\\images\\Add_Contact\\Contact image.png"
                default_pic1 = PhotoImage(file=defprofile_path)
                default_pic.config(image=default_pic1)

    def decide():
        """The function which checks if name is entered or not before opening dialogbox for selecting image, this is done because name if
        required to set name of selected picture
        """
        namecont = NameEntryBox.get()
        if namecont == "" or namecont == "*Full Name":
            messagebox.showerror("Missing", "Please enter name first")

        else:
            messagebox.showwarning("IMP", "Select image of size 220x220px or else the image will be auto cropped")
            pic_change()

    def pic_change():
        """This function is executed when change profile pic button is clicked"""
        global get_path
        namecont = NameEntryBox.get()

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=[("Image", ".jpg")])

        try:
            x = str(file_path) + str("\\Dependencies\\User Data\\") + str(name_logged) + str("\\") + str(
                namecont) + ".png"
            y = str(file_path) + str("\\Dependencies\\User Data\\") + str(name_logged) + str("\\") + str(
                namecont) + "_see.png"
            os.remove(x)
            os.remove(y)
        except:
            pass

        try:
            pic_location = filename
            resize_path = str(file_path) + str("\\Dependencies\\User Data\\") + str(name_logged) + str("\\") + str(
                namecont) + "_resize.png"
            paste_path = str(file_path) + str("\\Dependencies\\User Data\\") + str(name_logged) + str("\\") + str(
                namecont) + ".png"
            see_save_path = str(file_path) + str("\\Dependencies\\User Data\\") + str(name_logged) + str("\\") + str(
                namecont) + "_see.png"

            imge = Image.open(pic_location)
            crop_image = imge.resize((220, 220))
            crop_image.save(resize_path)

            img = Image.open(resize_path)

            height, width = img.size
            lum_img = Image.new('L', [height, width], 0)

            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0, 0), (height, width)], 0, 360,
                          fill=255, outline="white")
            img_arr = np.array(img)
            lum_img_arr = np.array(lum_img)
            (Image.fromarray(lum_img_arr))
            final_img_arr = np.dstack((img_arr, lum_img_arr))
            (Image.fromarray(final_img_arr).save(paste_path))
            os.remove(resize_path)

            imge2 = Image.open(paste_path)
            see_contact_img = imge2.resize((100, 100))
            see_contact_img.save(see_save_path)

            if name != "*Full Name":
                get_path = paste_path

        except:
            pass

    # GUI Widgets Placements
    # Background Pic
    logo = PhotoImage(file=str(file_path) + "\\Dependencies\\images\\Add_Contact\\new_BG.png")
    label2 = Label(addwindow, image=logo, border=0)
    label2.place(x=0, y=0)

    # ProfileButton
    if name != "*Full Name":
        defprofile_path = str(file_path) + "\\Dependencies\\User Data\\" + str(name_logged) + "\\" + name + ".png"

    else:
        defprofile_path = str(file_path) + "\\Dependencies\\images\\Add_Contact\\Contact image.png"

    orange_profilepic = PhotoImage(file=defprofile_path)
    default_pic = Button(image=orange_profilepic, bg="cyan", bd="0", activebackground='cyan', command=decide)
    default_pic.place(x=185, y=90)
    default_pic.bind("<Enter>", change)
    default_pic.bind("<Leave>", undo_change)

    # Name Entry Box
    NameEntryBox = Entry(addwindow, relief=FLAT, width="40", font=("Bahnschrift SemiLight Condensed", 22))
    NameEntryBox.insert(END, name)
    NameEntryBox.place(x=60, y=364)
    NameEntryBox.bind("<Button-1>", lambda x: del_widg("Name"))

    # Contact Number
    ContactEntryBox = Entry(addwindow, relief=FLAT, width="40", font=("Bahnschrift SemiLight Condensed", 22))
    ContactEntryBox.place(x=57, y=432)
    ContactEntryBox.insert(END, contact)
    ContactEntryBox.bind("<Button-1>", lambda x: del_widg("Contact"))

    # Category
    CategoryEntryBox = Entry(addwindow, relief=FLAT, width="40", font=("Bahnschrift SemiLight Condensed", 22))
    CategoryEntryBox.place(x=60, y=500)
    CategoryEntryBox.insert(END, category)
    CategoryEntryBox.bind("<Button-1>", lambda x: del_widg("Category"))

    # Email
    EmailEntryBox = Entry(addwindow, relief=FLAT, width="40", font=("Bahnschrift SemiLight Condensed", 22))
    EmailEntryBox.place(x=60, y=570)
    EmailEntryBox.insert(END, email)
    EmailEntryBox.bind("<Button-1>", lambda x: del_widg("Email"))

    # DOB
    DOBEntryBox = Entry(addwindow, relief=FLAT, width="40", font=("Bahnschrift SemiLight Condensed", 22))
    DOBEntryBox.place(x=60, y=638)
    DOBEntryBox.insert(END, dob)
    DOBEntryBox.bind("<Button-1>", lambda x: del_widg("DOB"))

    # Submit Button
    submit_path = str(file_path) + "\Dependencies\images\Add_Contact\\save_1.png"
    Save_button = PhotoImage(file=submit_path)
    submit_button = Button(addwindow, image=Save_button, bd=0, bg="cyan", command=submit, activebackground='cyan')
    submit_button.place(x=330, y=10)

    # Cancel Button
    cancel_path = str(file_path) + "\Dependencies\images\Add_Contact\\cancel_1.png"
    cross_button = PhotoImage(file=cancel_path)
    cancel_button = Button(addwindow, image=cross_button, bd=0, bg="cyan", command=cancel, activebackground='cyan')
    cancel_button.place(x=10, y=10)


    if name != "*Full Name":
        submit_button.config(command=edit_submit)
    else:
        # Message Box [Pops up during start]
        messagebox.showinfo("IMP", "The fields marked with * should not be left empty")

    mainloop()


def see_contact():
    """This is function for seeing contacts"""
    destroy()
    seewindow = Tk()
    seewindow.title("See Contacts")
    seewindow.maxsize(1200, 800)
    seewindow.minsize(1200, 800)
    seewindow.geometry("1200x800")
    seewindow.config(bg="#D5EAE8")

    # ImagePaths
    folder_location = str(file_path) + "\\Dependencies\\images\\SeeContact\\"
    DeleteButton = PhotoImage(file=folder_location + "Delete_button.png")

    # ImageLoading
    BG = PhotoImage(file=folder_location + "Aqua.png")
    FamilyButton = PhotoImage(file=folder_location + "family_button.png")
    WorkButton = PhotoImage(file=folder_location + "Work_button.png")
    FriendButton = PhotoImage(file=folder_location + "Friend_button.png")
    OthersButton = PhotoImage(file=folder_location + "Others_button.png")
    AllButton = PhotoImage(file=folder_location + "All_button.png")
    AddContactButton = PhotoImage(file=folder_location + "Add_button.png")
    HomeButton = PhotoImage(file=folder_location + "Home_button.png")
    DeleteButton = PhotoImage(file=folder_location + "Delete_button.png")
    EditButton = PhotoImage(file=folder_location + "Edit_button.png")

    MAIN_BG = Label(seewindow, image=BG, border=0)
    MAIN_BG.place(x=0, y=0)

    # Folder Creation
    file_path1 = str(file_path) + "\\Dependencies\\User Data\\"
    try:
        path = os.path.join(file_path1, name_logged)
        os.makedirs(path)
    except:
        pass

    def delete(name):
        command = f"DELETE FROM {name_logged}contacts WHERE NAME='{name}';"
        mycursor.execute(command)
        mydatabase.commit()
        mainscreen()

    def mainscreen(cat="None"):
        global LBG

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="#65EBDC", darkcolor="#59E8D7", lightcolor="#59E8D7",
                        troughcolor="#59E8D7", bordercolor="#59E8D7", arrowcolor="Black", arrowsize=15)

        wrapper1 = LabelFrame(seewindow, width="1600", height="100", background="gray6", bd=0)
        mycanvas = Canvas(wrapper1, background="#D5EAE8", borderwidth=0, highlightthickness=0, width=1145, height=558)
        mycanvas.pack(side=LEFT, expand=False, padx=0)

        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
        yscrollbar.pack(side=RIGHT, fill="y", expand=False)

        mycanvas.configure(yscrollcommand=yscrollbar.set)

        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))
        myframe = Frame(mycanvas)
        myframe.config(bg="#D5EAE8")
        mycanvas.create_window((0, 0), window=myframe, anchor="n")

        wrapper1.place(x=20, y=218)

        def OnMouseWheel(event):
            mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

        mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

        if cat == "None":
            see = f"SELECT * from {name_logged}contacts ORDER BY NAME"
        else:
            see = f"SELECT * from {name_logged}contacts WHERE CATEGORY=\'{str(cat)}\'"
        mycursor.execute(see)

        show_result = mycursor.fetchall()

        name_list, contact_list, email_list, dob_list, category_list, profile_location = [], [], [], [], [], []

        for row in show_result:
            name_list.append(row[0])
            contact_list.append(row[1])
            email_list.append(row[2])
            dob_list.append(row[3])
            category_list.append(row[4])
            profile_location.append(row[5])

        name_length = len(name_list)

        row_1, column1 = 0, 0

        LBG_path = str(file_path) + "\\Dependencies\\images\\SeeContact\\LabelBG.png"
        LBG = PhotoImage(file=LBG_path)


        def edit(name, contact, category, email, dob, profile):
            seewindow.destroy()
            add_contact(name, contact, category, email, dob, profile)

        for i in range(0, name_length):
            name = name_list[i]
            contact = contact_list[i]
            email = email_list[i]
            dob = dob_list[i]
            category = category_list[i]
            profile = profile_location[i]

            label2 = Label(myframe, image=LBG, border=0)
            label2.grid(row=row_1, column=column1)

            NameLabel = Label(myframe, text=name, background="LightCyan", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="DeepSkyBlue3")
            NameLabel.grid(row=row_1, column=column1, pady=(0, 100), padx=(70, 0))

            ContactLabel = Label(myframe, text=contact, background="LightCyan",
                                 font=("Bahnschrift SemiLight Condensed", 16), foreground="DeepSkyBlue3")
            ContactLabel.grid(row=row_1, column=column1, pady=(0, 40), padx=(103, 0))

            CategoryLabel = Label(myframe, text=category, background="LightCyan",
                                  font=("Bahnschrift SemiLight Condensed", 14), foreground="DeepSkyBlue3")
            CategoryLabel.grid(row=row_1, column=column1, pady=(45, 0), padx=(40, 0))

            DOBLabel = Label(myframe, text=dob, background="LightCyan",
                             font=("Bahnschrift SemiLight Condensed", 14), foreground="DeepSkyBlue3")
            DOBLabel.grid(row=row_1, column=column1, pady=(5, 0), padx=(55, 0))

            EmailLabel = Label(myframe, text=email, background="LightCyan",
                               font=("Bahnschrift SemiLight Condensed", 15, 'italic'), foreground="DeepSkyBlue3")
            EmailLabel.grid(row=row_1, column=column1, pady=(110, 0), padx=(20, 0), sticky=W)

            DelButton = Button(myframe, bd=0, image=DeleteButton, background="LightCyan", activebackground="LightCyan",
                               command=lambda name1=name: delete(name1))
            DelButton.grid(row=row_1, column=column1, pady=(85, 0), padx=(0, 6), sticky=E)

            edit_button = Button(myframe, image=EditButton, bd=0, background="LightCyan", activebackground="LightCyan", command=lambda currentname=name, currentcontact=contact,
                                currentcategory=category, currentdob=dob, currentemail=email, currentprofile=profile:
                                edit(currentname, currentcontact, currentcategory, currentemail, currentdob, currentprofile))
            edit_button.grid(row=row_1, column=column1, pady=(0, 90), padx=(0, 6), sticky=E)

            img_tst = PhotoImage(file=profile)
            test = Label(myframe, image=img_tst, background="LightCyan")
            test.grid(row=row_1, column=column1, pady=(0, 20), padx=(0, 135))
            test.image = img_tst

            column1 += 1

            if column1 == 4:
                column1 = 0
                row_1 += 1

    def back():
        seewindow.destroy()
        main()

    def add():
        seewindow.destroy()
        add_contact()

    def allcont(cat="None"):
        mainscreen("None")

        if cat == "Work":
            Work_bt1.config(image=WorkButton, command=work)
        elif cat == "Friend":
            Friend_bt1.config(image=FriendButton, command=friend)
        elif cat == "Family":
            Family_bt1.config(image=FamilyButton, command=family)
        elif cat == "Other":
            Others_bt1.config(image=OthersButton, command=other)
        else:
            Family_bt1.config(image=FamilyButton, command=family)
            Friend_bt1.config(image=FriendButton, command=friend)
            Work_bt1.config(image=WorkButton, command=work)
            Others_bt1.config(image=OthersButton, command=other)

    def work():
        mainscreen("Work")
        Family_bt1.config(image=FamilyButton, command=family)
        Friend_bt1.config(image=FriendButton, command=friend)
        Others_bt1.config(image=OthersButton, command=other)

        Work_bt1.config(image=AllButton, command=lambda: allcont("Work"))

    def friend():
        mainscreen("Friend")
        Family_bt1.config(image=FamilyButton, command=family)
        Work_bt1.config(image=WorkButton, command=work)
        Others_bt1.config(image=OthersButton, command=other)

        Friend_bt1.config(image=AllButton, command=lambda: allcont("Friend"))

    def family():
        mainscreen("Family")
        Friend_bt1.config(image=FriendButton, command=friend)
        Work_bt1.config(image=WorkButton, command=work)
        Others_bt1.config(image=OthersButton, command=other)

        Family_bt1.config(image=AllButton, command=lambda: allcont("Family"))

    def other():
        mainscreen("Other")
        Friend_bt1.config(image=FriendButton, command=friend)
        Family_bt1.config(image=FamilyButton, command=family)
        Work_bt1.config(image=WorkButton, command=work)

        Others_bt1.config(image=AllButton, command=lambda: allcont("Other"))

    Friend_bt1 = Button(seewindow, image=FriendButton, border=0, bg="#D5EAE8", activebackground="#D5EAE8",
                        command=friend)
    Friend_bt1.place(x=227, y=140)

    Work_bt1 = Button(seewindow, image=WorkButton, border=0, bg="#D5EAE8", activebackground="#D5EAE8", command=work)
    Work_bt1.place(x=434, y=140)

    Family_bt1 = Button(seewindow, image=FamilyButton, border=0, bg="#D5EAE8", activebackground="#D5EAE8",
                        command=family)
    Family_bt1.place(x=20, y=140)

    Others_bt1 = Button(seewindow, image=OthersButton, border=0, bg="#D5EAE8", activebackground="#D5EAE8",
                        command=other)
    Others_bt1.place(x=641, y=140)

    Home_btn = Button(seewindow, image=HomeButton, border=0, bg="#59E8D7", activebackground="#59E8D7", command=back)
    Home_btn.place(x=1100, y=124)

    AddContact_btn = Button(seewindow, image=AddContactButton, border=0, bg="#59E8D7", activebackground="#59E8D7",
                            command=add)
    AddContact_btn.place(x=1010, y=124)

    logged.close()
    mainscreen()
    mainloop()


def search_():
    """This is function for seeing contacts through category"""
    global LBG
    global BG2
    global SearchIcon
    global HomeIcon
    global DelButton1
    global edit_button1
    destroy()


    def show_result_():
        global LBG
        global name_list
        global contact_list
        global email_list
        global dob_list
        global category_list
        global profile_location

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="Cyan", darkcolor="gray6", lightcolor="LightGreen",
                        troughcolor="Turquoise4", bordercolor="gray6", arrowcolor="gray6", arrowsize=15)

        wrapper1 = LabelFrame(search_window, width="1600", height="100", background="#D5EAE8", bd=0)
        mycanvas = Canvas(wrapper1, background="#D5EAE8", borderwidth=0, highlightthickness=0, width=1160, height=572)
        mycanvas.pack(side=LEFT, expand=False, padx=0)

        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
        yscrollbar.pack(side=RIGHT, fill="y", expand=False)

        mycanvas.configure(yscrollcommand=yscrollbar.set)

        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

        myframe = Frame(mycanvas)
        myframe.config(bg="#D5EAE8")
        mycanvas.create_window((0, 0), window=myframe, anchor="n")

        def OnMouseWheel(event):
            mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

        mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

        wrapper1.place(x=15, y=195)

        LBG = PhotoImage(file=folder_location_main + "LabelBG.png")

        name_list, contact_list, email_list, dob_list, category_list, profile_location = else_name_list, else_contact_list, else_email_list, else_dob_list, else_category_list, else_profile_location

        name_length = len(name_list)

        row_1, column1 = 0, 0

        for i in range(0, name_length):
            name = name_list[i]
            contact = contact_list[i]
            email = email_list[i]
            dob = dob_list[i]
            category = category_list[i]
            profile = profile_location[i]

            label2 = Label(myframe, image=LBG, border=0)
            label2.grid(row=row_1, column=column1)

            NameLabel = Label(myframe, text=name, background="LightCyan", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="DeepSkyBlue3")
            NameLabel.grid(row=row_1, column=column1, pady=(0, 100), padx=(70, 0))

            ContactLabel = Label(myframe, text=contact, background="LightCyan",
                                 font=("Bahnschrift SemiLight Condensed", 16), foreground="DeepSkyBlue3")
            ContactLabel.grid(row=row_1, column=column1, pady=(0, 40), padx=(103, 0))

            CategoryLabel = Label(myframe, text=category, background="LightCyan",
                                  font=("Bahnschrift SemiLight Condensed", 14), foreground="DeepSkyBlue3")
            CategoryLabel.grid(row=row_1, column=column1, pady=(45, 0), padx=(40, 0))

            DOBLabel = Label(myframe, text=dob, background="LightCyan",
                             font=("Bahnschrift SemiLight Condensed", 14), foreground="DeepSkyBlue3")
            DOBLabel.grid(row=row_1, column=column1, pady=(5, 0), padx=(55, 0))

            EmailLabel = Label(myframe, text=email, background="LightCyan",
                               font=("Bahnschrift SemiLight Condensed", 15, 'italic'), foreground="DeepSkyBlue3")
            EmailLabel.grid(row=row_1, column=column1, pady=(110, 0), padx=(20, 0), sticky=W)

            DelButton = Button(myframe, bd=0, image=DeleteButton, background="LightCyan", activebackground="LightCyan",
                               command=lambda name1=name: delete(name1))
            DelButton.grid(row=row_1, column=column1, pady=(85, 0), padx=(0, 6), sticky=E)

            edit_button = Button(myframe, image=EditButton, bd=0, background="LightCyan",
                                 command=lambda currentname=name, currentcontact=contact,
                                                currentcategory=category, currentdob=dob, currentemail=email,
                                                currentprofile=profile:edit(currentname, currentcontact, currentcategory, currentemail, currentdob,currentprofile))
            edit_button.grid(row=row_1, column=column1, pady=(0, 90), padx=(0, 6), sticky=E)

            img_tst = PhotoImage(file=profile)
            test = Label(myframe, image=img_tst, background="LightCyan")
            test.grid(row=row_1, column=column1, pady=(0, 20), padx=(0, 135))
            test.image = img_tst

            column1 += 1

            if column1 == 4:
                column1 = 0
                row_1 += 1

    def search_command(*args):
        global else_name_list
        global else_contact_list
        global else_email_list
        global else_dob_list
        global else_category_list
        global else_profile_location

        else_name_list, else_contact_list, else_email_list, else_dob_list, else_category_list, else_profile_location = [], [], [], [], [], []

        search = SearchEntry.get()

        see = f"SELECT * FROM {name_logged}CONTACTS WHERE NAME LIKE \'%{search}%\'"

        mycursor.execute(see)

        show_result = mycursor.fetchall()

        for row in show_result:
            else_name_list.append(row[0])
            else_contact_list.append(str(row[1]))
            else_email_list.append(row[2])
            else_dob_list.append(row[3])
            else_category_list.append(row[4])
            else_profile_location.append(row[5])

        show_result_()

    search_window = Tk()
    search_window.geometry('1200x800')
    search_window.title("Search")

    def home():
        search_window.destroy()
        main()

    def delete(name):
        global name_list
        global contact_list
        global email_list
        global dob_list
        global category_list
        global profile_location

        command = f"DELETE FROM {name_logged}contacts WHERE NAME='{name}';"
        mycursor.execute(command)
        mydatabase.commit()
        index = name_list.index(name)
        name_list.remove(name)
        contact_list.pop(index)
        email_list.pop(index)
        dob_list.pop(index)
        category_list.pop(index)
        profile_location.pop(index)
        show_result_()

    def edit(name, contact, category, email, dob, profile):
        search_window.destroy()
        add_contact(name, contact, category, email, dob, profile)

    folder_location = str(file_path) + "\\Dependencies\\images\\SeeContact\\"
    DeleteButton = PhotoImage(file=folder_location + "Delete_button.png")

    DeleteButton = PhotoImage(file=folder_location + "Delete_button.png")
    EditButton = PhotoImage(file=folder_location + "Edit_button.png")

    BG2 = PhotoImage(file=folder_location_main + "Search_BG.png")
    BG2_Label = Label(search_window, image=BG2)
    BG2_Label.place(x=0, y=0)

    SearchEntry = Entry(search_window, relief=FLAT, bg="#68DBCF", width="37",
                        font=("Bahnschrift SemiLight Condensed", 25), foreground="#3D2257")
    SearchEntry.place(x=514, y=40)

    SearchIcon = PhotoImage(file=folder_location_main + "Search1.png")
    SearchButton = Button(search_window, image=SearchIcon, border=0, activebackground="#D5EAE8", background="#D5EAE8",
                          command=search_command)
    SearchButton.place(x=1055, y=39)
    search_window.bind("<Return>", search_command)

    HomeIcon = PhotoImage(file=folder_location_main + "HomeButton.png")
    HomeButton = Button(search_window, image=HomeIcon, border=0, activebackground="#D5EAE8", background="#D5EAE8",
                        command=home)
    HomeButton.place(x=1126, y=39)


def main():
    global Logo
    global add_button
    global see_button
    global search_button
    global window

    # Window Configuration
    window = Tk()
    window.geometry('410x710')
    window.maxsize(410, 710)
    window.minsize(410, 710)
    window.title("ContactBook")
    window.configure(background='white')

    Logo = PhotoImage(file=folder_location_main + "logo.png")
    add_button = PhotoImage(file=folder_location_main + "add_button.png")
    see_button = PhotoImage(file=folder_location_main + "See_button.png")
    search_button = PhotoImage(file=folder_location_main + "SearchContact_Button.png")

    # LOGO_Label
    LogoLabel = Label(window, image=Logo, border=0, bg="white")
    LogoLabel.place(x=0, y=-10)

    # Add Contact Button
    add_bt = Button(window, image=add_button, border=0, height="70", bg="white", command=add_contact)
    add_bt.place(x=96, y=340)

    # See Contact Button
    see_bt = Button(window, image=see_button, border=0, height="70", bg="white", command=see_contact)
    see_bt.place(x=96, y=430)

    # Category
    search_bt = Button(window, image=search_button, border=0, height="70", bg="white", command=search_)
    search_bt.place(x=96, y=520)

    logged.close()

# LoopCommand
main()
mainloop()
