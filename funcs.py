import tkinter
import customtkinter
import datetime
from tkinter import *
from datetime import date
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import mysql.connector as c
import os
import pyotp
import cv2
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

con=c.connect(host="localhost",username="root",password="myname",database="cs")
cursor=con.cursor()


class Authentication(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management Software")
        self.geometry(f"{400}x{520}")
        self.iconbitmap(r'Assets/Icons/MainWindow.ico')


        # configure grid layout
        for i in range(6):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(1, weight=1)

        global AuthFrame
        AuthFrame = customtkinter.CTkFrame(self, corner_radius=15)
        AuthFrame.grid(row=0, column=2, rowspan=2, columnspan=2, padx=(10, 10), pady=(30, 30), sticky="nsew")
        AuthFrame.grid_rowconfigure(4, weight=1)
        AuthFrame.grid_columnconfigure(2, weight=1)

        global username_verify
        global password_verify
 
        username_verify = StringVar()
        password_verify = StringVar()
 
        global username_login_entry
        global password_login_entry

        LoginLabel = customtkinter.CTkLabel(AuthFrame, text="Authenticate", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=26, weight="bold")).pack(pady=18, padx=10)
        Spacerlabel = customtkinter.CTkLabel(AuthFrame, text="").pack()

        Userlabel = customtkinter.CTkLabel(AuthFrame, text="Username * ",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).pack(pady=12, padx=10)
        username_login_entry = customtkinter.CTkEntry(AuthFrame, placeholder_text="Username", textvariable=username_verify)
        username_login_entry.pack(ipadx=20,pady=2, padx=10)
        Passlabel = customtkinter.CTkLabel(AuthFrame, text="Password * ",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).pack(pady=12, padx=10)
        password_login_entry = customtkinter.CTkEntry(AuthFrame, placeholder_text="Password", textvariable=password_verify, show= '*')
        password_login_entry.pack(ipadx=20,pady=2, padx=10)
        Spacerlabel = customtkinter.CTkLabel(AuthFrame, text="").pack()
        LoginButton = customtkinter.CTkButton(AuthFrame, text="Login", command=self.login_verify).pack(ipadx=10,ipady=2,pady=15, padx=10)
        RegisterButton = customtkinter.CTkButton(AuthFrame, text="Register", command=self.register).pack(ipadx=10,ipady=2,pady=15, padx=10)

    # Main Modules
    def register(self):
        AuthFrame = customtkinter.CTkFrame(self, corner_radius=15)
        AuthFrame.grid(row=0, column=2, rowspan=2, columnspan=2, padx=(10, 10), pady=(30, 30), sticky="nsew")
        AuthFrame.grid_rowconfigure(4, weight=1)
        AuthFrame.grid_columnconfigure(2, weight=1)
 
        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()


        global inputOTP
        global finalconfirm

        inputOTP = StringVar()       
        finalconfirm = StringVar()


        RegisterLabel = customtkinter.CTkLabel(AuthFrame, text="Enter details", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=25, weight="bold")).pack(pady=22)
        Spacerlabel = customtkinter.CTkLabel(AuthFrame, text="").pack()

        Userlabel = customtkinter.CTkLabel(AuthFrame, text="Username * ",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).pack(pady=12, padx=10)
        username_entry = customtkinter.CTkEntry(AuthFrame, placeholder_text="Username", textvariable=username)
        username_entry.pack(ipadx=20,pady=5, padx=10)
        password_lable = customtkinter.CTkLabel(AuthFrame, text="Password * ",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).pack(pady=12, padx=10)
        password_entry = customtkinter.CTkEntry(AuthFrame, textvariable=password, show='*')
        password_entry.pack(ipadx=20,pady=5, padx=10)
        totp_lable = customtkinter.CTkLabel(AuthFrame, text="Enter the OTP * ",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).pack(pady=12, padx=10)
        totp_entry = customtkinter.CTkEntry(AuthFrame, textvariable=inputOTP)
        totp_entry.pack(ipadx=20,pady=5, padx=10)

   
        Spacerlabel = customtkinter.CTkLabel(AuthFrame, text="").pack()
        RegisterButton = customtkinter.CTkButton(AuthFrame, text="Register", command=self.register_user).pack(ipadx=10,ipady=2,pady=15, padx=10)

    def login_verify(self):
        username1 = username_verify.get()
        password1 = password_verify.get()
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END)

        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                self.destroy()
                app = App()
                app.mainloop()

            else:
                self.password_not_recognised()

 
        else:
            self.user_not_found()

    def register_user(self):

        TOTPKey="ThisIsMySecretKeyForAICase"
        totp = pyotp.TOTP(TOTPKey)
        confirm = inputOTP.get()
        finalconfirm = totp.verify(confirm)


        if finalconfirm == True:
            username_info = username.get()
            password_info = password.get()

            file = open(username_info, "w+")
            file.write(username_info + "\n")
            file.write(password_info)
            file.close()
    
            username_entry.delete(0, END)
            password_entry.delete(0, END)

            global registered_user_screen
            registered_user_screen = customtkinter.CTkToplevel(AuthFrame)
            registered_user_screen.title("User Successfully Registered")
            registered_user_screen.geometry("450x150")
            frame = customtkinter.CTkFrame(master=registered_user_screen)
            frame.pack(pady=20, padx=60, fill="both", expand=True)
            label = customtkinter.CTkLabel(master=frame, text="User has been successfully registered ").pack(pady=12, padx=10)
            button = customtkinter.CTkButton(master=frame, text="OK", command=self.delete_registered_user_screen).pack(pady=12, padx=10)
        
        else:
            global registered_user_screen1
            registered_user_screen1 = customtkinter.CTkToplevel(AuthFrame)
            registered_user_screen1.title("OTP Incorrect")
            registered_user_screen1.geometry("450x150")
            frame = customtkinter.CTkFrame(master=registered_user_screen1)
            frame.pack(pady=20, padx=60, fill="both", expand=True)
            label = customtkinter.CTkLabel(master=frame, text="The OTP entered is incorrect ").pack(pady=12, padx=10)
            button = customtkinter.CTkButton(master=frame, text="OK", command=self.delete_registered_user_screen1).pack(pady=12, padx=10)
        
    # Auth error popups
    def password_not_recognised(self):
        self.iconbitmap(r'Assets/Icons/MainWindow.ico')
        global password_not_recog_screen
        password_not_recog_screen = customtkinter.CTkToplevel(AuthFrame)
        password_not_recog_screen.title("Invalid Password")
        password_not_recog_screen.geometry("450x150")
        frame = customtkinter.CTkFrame(master=password_not_recog_screen)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        label = customtkinter.CTkLabel(master=frame, text="Invalid Password ").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(master=frame, text="OK", command=self.delete_password_not_recognised).pack(pady=12, padx=10)

    def user_not_found(self):
        self.iconbitmap(r'Assets/Icons/MainWindow.ico')
        global user_not_found_screen
        user_not_found_screen = customtkinter.CTkToplevel(AuthFrame)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("450x150")
        frame = customtkinter.CTkFrame(master=user_not_found_screen)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        label = customtkinter.CTkLabel(master=frame, text="User Not Found").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(master=frame, text="OK", command=self.delete_user_not_found_screen).pack(pady=12, padx=10)
 
    # Deleting popups
    def delete_password_not_recognised(self):
        password_not_recog_screen.destroy()
    def delete_user_not_found_screen(self):
        user_not_found_screen.destroy()
    def delete_registered_user_screen(self):
        registered_user_screen.destroy()
        self.destroy()
        app = Authentication()
        app.mainloop()
    def delete_registered_user_screen1(self):
        registered_user_screen1.destroy()
        self.destroy()
        app = Authentication()
        app.mainloop()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hospital Management Software")
        self.geometry(f"{920}x{700}")
        self.iconbitmap(r'Assets/Icons/MainWindow.ico')

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3, 4, 5), weight=2)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # sidebar widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=0)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="HMS", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Patient DB",font=customtkinter.CTkFont(family="Microsoft YaHei UI", size=15), command=self.pat_start)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Billing",font=customtkinter.CTkFont(family="Microsoft YaHei UI", size=15), command=self.bill_start)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Doctor's Availability",font=customtkinter.CTkFont(family="Microsoft YaHei UI", size=14), command=self.doc_start)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        #Patient Counter
        global CurrentPatsStr
        global CounterText
        global PatCounter
        global CounterText

        queryPATCOUNTER="SELECT COUNT(pat_id) FROM pat;"
        cursor.execute(queryPATCOUNTER)
        CurrentPats = cursor.fetchone()
        CurrentPatsStr=str(CurrentPats[0])

        CounterText=("Patients  \nRegistered: ")
        PatCounter=CounterText + CurrentPatsStr
        

        self.PatsRN = customtkinter.CTkLabel(self.sidebar_frame, text=(PatCounter), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=18, weight="bold"))
        self.PatsRN.grid(row=4, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:",font=customtkinter.CTkFont(family="Microsoft YaHei UI", size=14), anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:",font=customtkinter.CTkFont(family="Microsoft YaHei UI", size=14), anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text=(date.today()), font=customtkinter.CTkFont(family="Roboto Condensed",size=20))
        self.date_label.grid(row=9, column=0, padx=20, pady=(10))


        # Initial DataFrame
        DataFrame = customtkinter.CTkFrame(self, corner_radius=15)
        DataFrame.grid(row=0, column=1, rowspan=3, columnspan=19, padx=(20, 20), pady=(20, 20), sticky="nsew")
        DataFrame.grid_rowconfigure(4, weight=1)
        DataFrame.grid_columnconfigure(2, weight=1)

    # Patient Functions
    def pat_start(self):
        global PatMainDataFrame
        global PatInfoFrame
        global pat_retrieve
        self.geometry(f"{920}x{700}")
        pat_retrieve = StringVar()

        PatMainDataFrame = customtkinter.CTkFrame(self, corner_radius=15)
        PatMainDataFrame.grid(row=0, column=1, rowspan=9, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.PatStartLabel = customtkinter.CTkLabel(PatMainDataFrame, text="Patient Database", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=25, weight="bold")).place(relx=0.02,rely=0.035)
        self.PatAddButton = customtkinter.CTkButton(PatMainDataFrame, fg_color="transparent", text="Add Patients", command=self.insert_pat, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=2, text_color=("gray10", "#DCE4EE"))
        self.PatAddButton.place(relx=0.73,rely=0.035,relwidth=0.20,anchor="ne")
        self.PatRemoveButton = customtkinter.CTkButton(PatMainDataFrame, fg_color="transparent", text="Remove Patients", command=self.delete_pat, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=2, text_color=("gray10", "#DCE4EE"))
        self.PatRemoveButton.place(relx=0.96,rely=0.035,relwidth=0.21,anchor="ne")

        # Dynamic Frame
        PatInfoFrame = customtkinter.CTkFrame(PatMainDataFrame, corner_radius=15)
        PatInfoFrame.place(relx=0.02,rely=0.14,relheight=0.73,relwidth=0.96)

        self.PatSearchLabel = customtkinter.CTkLabel(PatMainDataFrame,text="Enter Patient ID to Search", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=14, weight="bold")).place(relx=0.02,rely=0.8765)
        self.PatSearch = customtkinter.CTkEntry(PatMainDataFrame, placeholder_text="Enter Patient ID", textvariable=pat_retrieve, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16))
        self.PatSearch.place(relx=0.02,rely=0.965,relwidth=0.64, anchor="sw")
        self.PatSearchButton = customtkinter.CTkButton(PatMainDataFrame, fg_color="transparent", text="Search Patient ID", command=self.retreive_pat, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=2, text_color=("gray10", "#DCE4EE"))
        self.PatSearchButton.place(relx=0.98,rely=0.965,relwidth=0.30, anchor="se")
    
    def insert_pat(self):
        global PatInfoFrame
        global pat_id
        global pat_name
        global pat_age
        global pat_gender
        global pat_dob
        global pat_doa
        global pat_bg
        global pat_weight
        global pat_contactno
        global pat_CDoctor
        global pat_CReason

        pat_id = IntVar()       
        pat_name = StringVar()
        pat_age = IntVar()
        pat_gender = StringVar()
        pat_dob = StringVar()
        pat_doa = date.today()
        pat_bg = StringVar()
        pat_weight = IntVar()
        pat_contactno = StringVar()
        pat_CDoctor = StringVar()
        pat_CReason = StringVar()

        PatInfoFrame = customtkinter.CTkFrame(PatMainDataFrame, corner_radius=15)
        PatInfoFrame.place(relx=0.02,rely=0.14,relheight=0.73,relwidth=0.96)

        label = customtkinter.CTkLabel(PatInfoFrame, text="Insert the Patient Data below",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.05,rely=0.03)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient ID *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.08,rely=0.14)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient ID", textvariable=pat_id).place(relx=0.08,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Name *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.08,rely=0.32)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Name", textvariable=pat_name).place(relx=0.08,rely=0.40)        

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Age *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.08,rely=0.50)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Age", textvariable=pat_age).place(relx=0.08,rely=0.58)


        # CALENDARS --------------------------------
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Date Of Birth *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.08,rely=0.68)
        #pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient DOB", textvariable=pat_dob).place(relx=0.08,rely=0.76)
        #style = ttk.Style()
        #style.theme_use('clam')  # -> uncomment this line if the styling does not work
        #style.configure('my.DateEntry',fieldbackground='#565b5e',background='#7a848d',foreground='#dce4ee',arrowcolor='#dce4ee')
        pat_id_cal = DateEntry(PatInfoFrame, textvariable=pat_dob, width=20,style='my.DateEntry',background='#222222',
                    foreground='silver', headersforeground="silver",headersbackground='#2b2b2b',
                    weekendforeground='silver',weekendbackground='#5c5c5c',
                    normalbackground='#5c5c5c', normalforeground='silver',
                    othermonthforeground='silver',othermonthbackground='#777777',
                    othermonthweforeground='silver',othermonthwebackground='#444444', borderwidth=9).place(relx=0.08,rely=0.76)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Gender *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.4,rely=0.14)
        pat_gender = customtkinter.CTkComboBox(PatInfoFrame, values=["Male", "Female", "Other"])
        pat_gender.place(relx=0.4,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Blood Group *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.4,rely=0.32)
        #pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Blood Group", textvariable=pat_bg).place(relx=0.42,rely=0.40)
        pat_bg = customtkinter.CTkComboBox(PatInfoFrame, values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        pat_bg.place(relx=0.4,rely=0.40)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Weight *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.4,rely=0.50)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Weight", textvariable=pat_weight).place(relx=0.4,rely=0.58)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Contact Number *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.4,rely=0.68)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Contact Number", textvariable=pat_contactno).place(relx=0.4,rely=0.76)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Consultant Doctor *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.685,rely=0.14)
        pat_CDoctor = customtkinter.CTkComboBox(PatInfoFrame, values=["Dr. Mahmood", "Dr. Anita", "Dr. Reddy", "Dr. Ayesha"])
        pat_CDoctor.place(relx=0.685,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Consultation Reason *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.685,rely=0.32)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Consultation Reason", textvariable=pat_CReason).place(relx=0.685,rely=0.4)



        button = customtkinter.CTkButton(PatInfoFrame, text="Add Patient Record", command=self.in_pat_record).place(relx=0.38,rely=0.89, relwidth=0.25)

    def retreive_pat(self):

        PatInfoFrame = customtkinter.CTkFrame(PatMainDataFrame, corner_radius=15)
        PatInfoFrame.place(relx=0.02,rely=0.14,relheight=0.73,relwidth=0.96)

        pat_id=pat_retrieve.get()
        cursor.execute('select * from pat where pat_id={}'.format(pat_id))
        pull_up_patid=cursor.fetchone()[0]
        print(pull_up_patid)

        #Fetching
        cursor.execute('select * from pat where pat_id={}'.format(pat_id))
        pull_up_patid=cursor.fetchone()[0]
        print(pull_up_patid)

        query1=('SELECT pat_name FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query1)
        pull_up_patname=cursor.fetchone()[0]

        query2=('SELECT pat_age FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query2)
        pull_up_patage=cursor.fetchone()[0]

        query3=('SELECT pat_gender FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query1)
        pull_up_gender=cursor.fetchone()[0]

        query4=('SELECT pat_contactno FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query4)
        pull_up_patcontactno=cursor.fetchone()[0]

        query5=('SELECT pat_dob FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query5)
        pull_up_patdob=cursor.fetchone()[0]

        query6=('SELECT pat_doa FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query6)
        pull_up_patdoa=cursor.fetchone()[0]

        query7=('SELECT pat_bg FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query7)
        pull_up_patbg=cursor.fetchone()[0]

        query8=('SELECT pat_weight FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query8)
        pull_up_patweight=cursor.fetchone()[0]

        query9=('SELECT pat_CDoctor FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query9)
        pull_up_patCDoctor=cursor.fetchone()[0]

        query10=('SELECT pat_CReason FROM pat WHERE pat_id = "{}"').format(pull_up_patid)
        cursor.execute(query10)
        pull_up_patCReason=cursor.fetchone()[0]


        #Displaying the data

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient ID *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.06,rely=0.08)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patid,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.06,rely=0.14)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Name *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.06,rely=0.26)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patname,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.06,rely=0.32)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Age *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.06,rely=0.44)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patage,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.06,rely=0.50)


        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Date Of Birth *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.06,rely=0.62)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patdob,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.06,rely=0.68)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Gender *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.38,rely=0.08)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_gender,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.38,rely=0.14)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Blood Group *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.38,rely=0.26)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patbg,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.38,rely=0.32)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Weight *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.38,rely=0.44)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patweight,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.38,rely=0.50)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Contact Number *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.38,rely=0.62)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patcontactno,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.38,rely=0.68)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Consultant Doctor *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.70,rely=0.08)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patCDoctor,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.70,rely=0.14)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Consultation Reason *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.70,rely=0.26)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patCReason,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.70,rely=0.32)


        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Date of Admission *",font=customtkinter.CTkFont(family="Roboto Condensed", size=17)).place(relx=0.70,rely=0.44)
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text=pull_up_patdoa,corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.70,rely=0.50)

    def in_pat_record(self):

        print(pat_id.get()) 
        print(pat_name.get())
        print(pat_age.get())
        print(pat_gender.get())
        print(pat_dob.get())
        print(pat_doa)
        print(pat_bg.get())
        print(pat_weight.get())
        print(pat_contactno.get())
        print(pat_CDoctor.get())
        print(pat_CReason.get())
        global test
        test = pat_id.get()  

        if test > 0:
            query1="Insert into pat values ({},'{}',{},'{}','{}','{}','{}',{},'{}','{}','{}')".format(pat_id.get(),pat_name.get(),pat_age.get(),pat_gender.get(),pat_dob.get(),pat_doa,pat_bg.get(),pat_weight.get(),pat_contactno.get(),pat_CDoctor.get(),pat_CReason.get())
            cursor.execute(query1)
            con.commit()
            self.in_success()
            #Patient Counter
            queryPATCOUNTER="SELECT COUNT(pat_id) FROM pat;"
            cursor.execute(queryPATCOUNTER)
            CurrentPats = cursor.fetchone()
            CurrentPatsStr=str(CurrentPats[0])

            CounterText=("Patients  \nRegistered: ")
            PatCounter=CounterText + CurrentPatsStr
            
            self.PatsRN = customtkinter.CTkLabel(self.sidebar_frame, text=(PatCounter), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=18, weight="bold"))
            self.PatsRN.grid(row=4, column=0, padx=20, pady=(20, 10))


        else:
            self.in_unsuccess()

    def delete_pat(self):
        dialog = customtkinter.CTkInputDialog(text="Type in the Patient ID:", title="Delete Patient Data")  
        pat_id = dialog.get_input()
        if pat_id >= "0":
            self.del_success()
            print("Deleted successfully Patient ID:", pat_id)
            query="delete from pat where pat_id={}".format(pat_id)
            cursor.execute(query)
            con.commit()
        else:
            self.del_unsuccess()

    def del_unsuccess(self):
        global del_unsuccess_screen
        del_unsuccess_screen = customtkinter.CTkToplevel(self)
        del_unsuccess_screen.title("Unsuccessful")
        del_unsuccess_screen.geometry("450x150")
        del_unsuccess_screen.iconbitmap(r'Assets/Icons/info.ico')
        label = customtkinter.CTkLabel(del_unsuccess_screen, text="The record was not deleted").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(del_unsuccess_screen, text="OK", command=self.destroy_del_unsuccess).pack(pady=12, padx=10)

    def del_success(self):
        global del_success_screen
        del_success_screen = customtkinter.CTkToplevel(self)
        del_success_screen.title("Success")
        del_success_screen.geometry("450x150")
        del_success_screen.iconbitmap(r'Assets/Icons/checkmark.ico')
        label = customtkinter.CTkLabel(del_success_screen, text="Successfully deleted the Patient Record").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(del_success_screen, text="OK", command=self.destroy_del_success).pack(pady=12, padx=10)
        
    def in_unsuccess(self):
        global in_unsuccess_screen
        in_unsuccess_screen = customtkinter.CTkToplevel(self)
        in_unsuccess_screen.title("Unsuccessful")
        in_unsuccess_screen.geometry("450x150")
        in_unsuccess_screen.iconbitmap(r'Assets/Icons/info.ico')
        label = customtkinter.CTkLabel(in_unsuccess_screen, text="The record was not entered \n\nCheck the Patient ID entered").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(in_unsuccess_screen, text="OK", command=self.destroy_in_unsuccess).pack(pady=12, padx=10)

    def in_success(self):
        global in_success_screen
        in_success_screen = customtkinter.CTkToplevel()
        in_success_screen.title("Success")
        in_success_screen.geometry("450x150")
        in_success_screen.iconbitmap(r'Assets/Icons/checkmark.ico')
        label = customtkinter.CTkLabel(in_success_screen, text="Successfully inserted the Patient Record").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(in_success_screen, text="OK", command=self.destroy_in_success).pack(pady=12, padx=10)

    #Billing Functions
    def bill_start(self):
        global BillDataFrame
        global BillInfoFrame


        self.geometry(f"{920}x{700}")
        BillDataFrame = customtkinter.CTkFrame(self, corner_radius=15)
        BillDataFrame.grid(row=0, column=1, rowspan=9, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
        self.BillStartLabel = customtkinter.CTkLabel(BillDataFrame, text="Billing", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=25, weight="bold")).place(relx=0.02,rely=0.035)

        BillInfoFrame = customtkinter.CTkFrame(BillDataFrame, corner_radius=15)
        BillInfoFrame.place(relx=0.02,rely=0.12,relheight=0.8575,relwidth=0.96)


        #Billing Code Blocks
        global medicinecharge
        global BillNoCounter
        global foodcharge

        medicinecharge = IntVar()
        foodcharge = IntVar()
        BillNoCounter = IntVar()
        BillNoCounter.set(0)


        #Billing Functions
        def add_bill():
            BillNoCounter.set(BillNoCounter.get() + 1)

            bill_number_label = customtkinter.CTkLabel(BillInfoFrame, text="Bill Number *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.06)
            bill_number_textbox = customtkinter.CTkTextbox(BillInfoFrame)
            bill_number_textbox.insert("0.0",BillNoCounter.get())
            bill_number_textbox.place(relx=0.24,rely=0.06)
            bill_number_textbox.configure(width= 190,height= 24,state="disabled")
            # print([BillNoCounter.get()-1],patidmenuclicked.get(),docmenuclicked.get(),labmenuclicked.get(),roomclicked.get())


            #Fetch from DB

            docquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(docmenuclicked.get())
            cursor.execute(docquery)
            docprice=cursor.fetchone()[0]
            testquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(labmenuclicked.get())
            cursor.execute(testquery)
            testprice=cursor.fetchone()[0]
            roomquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(roomclicked.get())
            cursor.execute(roomquery)
            roomprice=cursor.fetchone()[0]


            #Adding up

            totalcharge = (docprice + testprice + roomprice + medicinecharge.get() + foodcharge.get())
            print(totalcharge)
            totalcharge_label = customtkinter.CTkLabel(BillInfoFrame, text="Final Amount is: ", corner_radius=12, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=21, weight="bold")).place(relx=0.54,rely=0.86)
            totalchargeint_label = customtkinter.CTkLabel(BillInfoFrame, text=totalcharge, corner_radius=12, text_color="black",fg_color=("black", "#dce4ee"),font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=21, weight="bold"))
            totalchargeint_label.place(relx=0.83,rely=0.86)
            generate_bill()

            # totalcharge_textbox = customtkinter.CTkTextbox(BillDataFrame)
            # totalcharge_textbox.insert("0.0", "Patient ID: ", patidmenuclicked.get())
            # # totalcharge_textbox.insert("1.0", "new text to insert")
            # # totalcharge_textbox.insert("2.0", "new text to insert")
            # # totalcharge_textbox.insert("3.0", "new text to insert")
            # # totalcharge_textbox.insert("4.0", "new text to insert")
            # totalcharge_textbox.place(relx=0.55,rely=0.56)
            # totalcharge_textbox.configure(width= 290,height= 140,state="disabled")

        #Generate Bill Image
        def generate_bill():


            #Retrieving Data

            global billnameret
            global billingname
            
            billnameret=('SELECT pat_name FROM pat WHERE pat_id = "{}"').format(patidmenuclicked.get())
            cursor.execute(billnameret)
            billingname=cursor.fetchall()
            docquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(docmenuclicked.get())
            cursor.execute(docquery)
            docprice=cursor.fetchone()[0]
            testquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(labmenuclicked.get())
            cursor.execute(testquery)
            testprice=cursor.fetchone()[0]
            roomquery=('SELECT Cost FROM prices WHERE ENTITY = "{}"').format(roomclicked.get())
            cursor.execute(roomquery)
            roomprice=cursor.fetchone()[0]
            MedPriceString = [medicinecharge.get()]
            FoodPriceString = [foodcharge.get()]
            totalbillprintcost = [docprice + testprice + roomprice + medicinecharge.get() + foodcharge.get()]

            #Converting StringVar to String

            BillNoStr = (BillNoCounter.get())
            DateStr = (now.strftime("  %d/%m/%Y %H:%M:%S"))

            DoctorChosenString = (docmenuclicked.get())
            LabTestChosenString = (labmenuclicked.get())
            RoomChosenString = (roomclicked.get())
            MedicineChargeString = "Medical Charges"
            FoodChargeString = "Food Charges"


            billingnamestr = str(billingname)
            docpricestr = str(docprice)
            testpricestr = str(testprice)
            roompricestr = str(roomprice)
            MedPriceStringStr = str(MedPriceString)
            FoodPriceStringStr = str(FoodPriceString)
            totalbillprintcoststr = str(totalbillprintcost)


            template = cv2.imread("Assets/Template/bill-template.jpg")
            # cv2.putText(template, BillNoStr, (425,720), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, DateStr, (990,715), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, billingnamestr, (410,790), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, DoctorChosenString, (400,1075), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, LabTestChosenString, (400,1150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, RoomChosenString, (400,1220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, MedicineChargeString, (410,1290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, FoodChargeString, (410,1360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, docpricestr, (870,1080), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, testpricestr, (870,1160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, roompricestr, (870,1230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, MedPriceStringStr, (870,1295), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, FoodPriceStringStr, (870,1365), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, docpricestr, (1175,1080), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, testpricestr, (1175,1160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, roompricestr, (1175,1230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, MedPriceStringStr, (1175,1295), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, FoodPriceStringStr, (1175,1365), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(template, totalbillprintcoststr, (1170,1496), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.imwrite(f'generated-bill.jpg',template)


        #Start of Billing Widgets
        bill_number_label = customtkinter.CTkLabel(BillInfoFrame, text="Bill Number *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.06)
        bill_number_textbox = customtkinter.CTkTextbox(BillInfoFrame)
        bill_number_textbox.insert("0.0",BillNoCounter.get())
        bill_number_textbox.place(relx=0.24,rely=0.06)
        bill_number_textbox.configure(width= 190,height= 24,state="disabled")


        bill_add_button = customtkinter.CTkButton(BillInfoFrame, text="TOTAL",command=add_bill).place(relx=0.24,rely=0.86,relheight=0.072,relwidth=0.285 )


        #Bill Date
        bill_date_label = customtkinter.CTkLabel(BillInfoFrame, text="Bill Date & Time *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.16)
        now = datetime.now()
        bill_date_textbox = customtkinter.CTkTextbox(BillInfoFrame)
        bill_date_textbox.insert("0.0", now.strftime("  %d/%m/%Y %H:%M:%S"))
        bill_date_textbox.place(relx=0.24,rely=0.16)
        bill_date_textbox.configure(width= 190,height= 24,state="disabled")


        #PatientID 
        query="SELECT distinct(pat_id) as pat_id FROM pat"
        cursor.execute(query)
        my_data=cursor.fetchall() # SQLAlchem engine result
        my_list = [r for r, in my_data] # create a  list 
        patidmenuclicked = StringVar()
        patidmenuclicked.set("Select Patient")
        pat_id_label = customtkinter.CTkLabel(BillInfoFrame, text="Patient ID *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.26)
        patidmenu = OptionMenu(BillInfoFrame, patidmenuclicked, *my_list)
        patidmenu.place(relx=0.24,rely=0.26)
        patidmenu.config(width=24)

        patidmenu["highlightthickness"]=1
        patidmenu["highlightbackground"]="#949a9f"
        patidmenu ["menu"] ["bg"] = "#2b2b2b"
        patidmenu ["menu"] ["fg"] = "silver"
        patidmenu ["bg"] = "#2b2b2b"
        patidmenu ["fg"] = "silver"
        patidmenu ["activeforeground"] = "silver"
        patidmenu ["activebackground"] = "#106a43"
        #-------------------------------------------

        #Doctor's Fee
        doc_list = ['None','Dr Mahmood','Dr Anita', 'Dr Reddy','Dr Ayesha']
        doctor_charge_label = customtkinter.CTkLabel(BillInfoFrame, text="Doctor's Fee *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.36)
        docmenuclicked = StringVar()
        docmenuclicked.set("Select Doctor")
        docmenu = OptionMenu(BillInfoFrame, docmenuclicked, *doc_list)
        docmenu.place(relx=0.24,rely=0.36)
        docmenu.config(width=24)

        docmenu["highlightthickness"]=1
        docmenu["highlightbackground"]="#949a9f"
        docmenu ["menu"] ["bg"] = "#2b2b2b"
        docmenu ["menu"] ["fg"] = "silver"
        docmenu ["bg"] = "#2b2b2b"
        docmenu ["fg"] = "silver"
        docmenu ["activeforeground"] = "silver"
        docmenu ["activebackground"] = "#106a43"
        #---------------------

        #Lab Test Fee
        labtest_list = ['None','Blood Tests', 'CT-Scan','Electrocardiogram (ECG)', 'MRI Scan','Eye Test','Hearing Test','X-rays']
        labtest_charge_label = customtkinter.CTkLabel(BillInfoFrame, text="Lab Test Fee *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.46)
        labmenuclicked = StringVar()
        labmenuclicked.set("Select Lab Test")
        labmenu = OptionMenu(BillInfoFrame, labmenuclicked, *labtest_list)
        labmenu.place(relx=0.24,rely=0.46)
        labmenu.config(width=24)

        labmenu["highlightthickness"]=1
        labmenu["highlightbackground"]="#949a9f"
        labmenu ["menu"] ["bg"] = "#2b2b2b"
        labmenu ["menu"] ["fg"] = "silver"
        labmenu ["bg"] = "#2b2b2b"
        labmenu ["fg"] = "silver"
        labmenu ["activeforeground"] = "silver"
        labmenu ["activebackground"] = "#106a43"
        #---------------------

        #Room Charges
        room_list = ['None','Single Room', 'Single Deluxe Room','Suite', 'Multibed Ward','Twin Sharing Room']
        room_charge_label = customtkinter.CTkLabel(BillInfoFrame, text="Room Charges *",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.56)
        roomclicked = StringVar()
        roomclicked.set("Select Room")
        roommenu = OptionMenu(BillInfoFrame, roomclicked, *room_list)
        roommenu.place(relx=0.24,rely=0.56)
        roommenu.config(width=24)

        roommenu["highlightthickness"]=1
        roommenu["highlightbackground"]="#949a9f"
        roommenu ["menu"] ["bg"] = "#2b2b2b"
        roommenu ["menu"] ["fg"] = "silver"
        roommenu ["bg"] = "#2b2b2b"
        roommenu ["fg"] = "silver"
        roommenu ["activeforeground"] = "silver"
        roommenu ["activebackground"] = "#106a43"
        #-------------------------------------

        medicine_charge_label = customtkinter.CTkLabel(BillInfoFrame, text="Medicine Charges*",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.66)
        medicine_charge_entry = customtkinter.CTkEntry(BillInfoFrame, placeholder_text="Total Medicine Charge", textvariable=medicinecharge,justify=CENTER,width=190)
        medicine_charge_entry.place(relx=0.24,rely=0.66)

        food_charge_label = customtkinter.CTkLabel(BillInfoFrame, text="Food Charges*",font=customtkinter.CTkFont(family="Roboto Condensed", size=15)).place(relx=0.04,rely=0.76)
        food_charge_entry = customtkinter.CTkEntry(BillInfoFrame, placeholder_text="Total Food Charge", textvariable=foodcharge ,justify=CENTER,width=190)
        food_charge_entry.place(relx=0.24,rely=0.76)


    # Doctor Functions
    def doc_start(self):
        global DocDataFrame
        global DAvailFrame

        self.geometry(f"{980}x{860}")
        DocDataFrame = customtkinter.CTkFrame(self, corner_radius=15)
        DocDataFrame.grid(row=0, column=1, rowspan=9, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")


        self.DocStartLabel = customtkinter.CTkLabel(DocDataFrame, text="Doctor's Availability", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=25, weight="bold")).place(relx=0.02,rely=0.035)

        self.DMahmoodButton = customtkinter.CTkButton(DocDataFrame, fg_color="transparent", text="Doctor Mahmood", command=self.DMah, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.DMahmoodButton.place(relx=0.025,rely=0.12,relwidth=0.22,height=35)
        self.DAnitaButton = customtkinter.CTkButton(DocDataFrame, fg_color="transparent", text="Doctor Anita", command=self.DAni, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.DAnitaButton.place(relx=0.2725,rely=0.12,relwidth=0.22,height=35)
        self.DReddyButton = customtkinter.CTkButton(DocDataFrame, fg_color="transparent", text="Doctor Reddy", command=self.DRedd, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.DReddyButton.place(relx=0.5225,rely=0.12,relwidth=0.22,height=35)
        self.DAyeshaButton = customtkinter.CTkButton(DocDataFrame, fg_color="transparent", text="Doctor Ayesha", command=self.DAyes, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.DAyeshaButton.place(relx=0.77,rely=0.12,relwidth=0.20,height=35)

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

    #Doc Schedules
    def DMah(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DMahmood-Jan.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DMahFeb,font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DMahFeb(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DMahmood-Feb.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DMah, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DMahMarch, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DMahMarch(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DMahmood-March.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DMahFeb, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)

    def DAni(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAnita-Jan.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DAniFeb,font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DAniFeb(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAnita-Feb.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DAni, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DAniMarch, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DAniMarch(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAnita-March.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DAniFeb, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)

    def DRedd(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DReddy-Jan.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DReddFeb,font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DReddFeb(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DReddy-Feb.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DRedd, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DReddMarch, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DReddMarch(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DReddy-March.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DReddFeb, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)

    def DAyes(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAyesha-Jan.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DAyesFeb,font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DAyesFeb(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAyesha-Feb.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DAyes, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">", command=self.DAyesMarch, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)
    def DAyesMarch(self):

        DAvailFrame = customtkinter.CTkFrame(DocDataFrame, corner_radius=15)
        DAvailFrame.place(relx=0.02,rely=0.2175,relheight=0.7575,relwidth=0.96)

        path = "Assets\DocSchedules\DAyesha-March.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(DAvailFrame, image=img)
        panel.photo = img
        panel.place(relx=0.01215,rely=0.025)

        self.PrevImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text="<", command=self.DAyesFeb, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.PrevImg.place(relx=0.775,rely=0.05,height=40,width=60)
        self.NextImg = customtkinter.CTkButton(DAvailFrame, fg_color="transparent", text=">",font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=3, text_color=("gray10", "#DCE4EE"))
        self.NextImg.place(relx=0.875,rely=0.05,height=40,width=60)

    # extra functions
    def cleanse_frame(self):
        for widgets in PatMainDataFrame.winfo_children():
            widgets.destroy()
        for widgets in DocDataFrame.winfo_children():
            widgets.destroy()

        PatMainDataFrame.grid_forget()
        DocDataFrame.grid_forget()
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # destroying window functions
    def destroy_del_unsuccess(self):
        del_unsuccess_screen.destroy()
    def destroy_del_success(self):
        del_success_screen.destroy()
        
        #Patient Counter
        queryPATCOUNTER="SELECT COUNT(pat_id) FROM pat;"
        cursor.execute(queryPATCOUNTER)
        CurrentPats = cursor.fetchone()
        CurrentPatsStr=str(CurrentPats[0])

        CounterText=("Patients \nRegistered: ")
        PatCounter=CounterText + CurrentPatsStr
        
        self.PatsRN = customtkinter.CTkLabel(self.sidebar_frame, text=(PatCounter), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=18, weight="bold"))
        self.PatsRN.grid(row=4, column=0, padx=20, pady=(20, 10))
    def destroy_in_unsuccess(self):
        in_unsuccess_screen.destroy()
    def destroy_in_success(self):
        in_success_screen.destroy()
        self.pat_start()

if __name__ == "__main__":
    app = Authentication()
    app.mainloop()