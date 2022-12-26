import tkinter
import customtkinter
import datetime
from tkinter import *
from datetime import date
from tkcalendar import Calendar, DateEntry
import mysql.connector as c
import os
import pyotp
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
        self.iconbitmap(r'C:\Users\imsaa\Pictures\test.ico')


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
        global password_not_recog_screen
        password_not_recog_screen = customtkinter.CTkToplevel(AuthFrame)
        password_not_recog_screen.title("Invalid Password")
        password_not_recog_screen.geometry("450x150")
        frame = customtkinter.CTkFrame(master=password_not_recog_screen)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        label = customtkinter.CTkLabel(master=frame, text="Invalid Password ").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(master=frame, text="OK", command=self.delete_password_not_recognised).pack(pady=12, padx=10)

    def user_not_found(self):
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
        self.iconbitmap(r'C:\Users\imsaa\Pictures\test.ico')

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

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Patient DB", command=self.pat_start)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Billing")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Doctor's Availibility", command=self.doc_start)
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

        CounterText=("Patients Currently \nRegistered:  ")
        PatCounter=CounterText + CurrentPatsStr
        

        self.PatsRN = customtkinter.CTkLabel(self.sidebar_frame, text=(PatCounter), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=18, weight="bold"))
        self.PatsRN.grid(row=4, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text=(date.today()), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light",size=20))
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

        self.PatSearch = customtkinter.CTkEntry(PatMainDataFrame, placeholder_text="Enter Patient ID", textvariable=pat_retrieve, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16))
        self.PatSearch.place(relx=0.02,rely=0.965,relwidth=0.64, anchor="sw")
        self.PatSearchButton = customtkinter.CTkButton(PatMainDataFrame, fg_color="transparent", text="Search Patient", command=self.retreive_pat, font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=16), border_width=2, text_color=("gray10", "#DCE4EE"))
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

        label = customtkinter.CTkLabel(PatInfoFrame, text="Insert the Patient Data below").place(relx=0.05,rely=0.03)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient ID *").place(relx=0.08,rely=0.14)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient ID", textvariable=pat_id).place(relx=0.08,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Name *").place(relx=0.08,rely=0.32)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Name", textvariable=pat_name).place(relx=0.08,rely=0.40)        

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Age *").place(relx=0.08,rely=0.50)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Age", textvariable=pat_age).place(relx=0.08,rely=0.58)


        # CALENDARS --------------------------------
        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Date Of Birth *").place(relx=0.08,rely=0.68)
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

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Gender *").place(relx=0.4,rely=0.14)
        pat_gender = customtkinter.CTkComboBox(PatInfoFrame, values=["Male", "Female", "Other"])
        pat_gender.place(relx=0.4,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Blood Group *").place(relx=0.4,rely=0.32)
        #pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Blood Group", textvariable=pat_bg).place(relx=0.42,rely=0.40)
        pat_bg = customtkinter.CTkComboBox(PatInfoFrame, values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        pat_bg.place(relx=0.4,rely=0.40)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Weight *").place(relx=0.4,rely=0.50)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Weight", textvariable=pat_weight).place(relx=0.4,rely=0.58)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Contact Number *").place(relx=0.4,rely=0.68)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Patient Contact Number", textvariable=pat_contactno).place(relx=0.4,rely=0.76)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Patient Consultant Doctor *").place(relx=0.72,rely=0.14)
        pat_CDoctor = customtkinter.CTkComboBox(PatInfoFrame, values=["Dr. Mahmood", "Dr. Anita", "Dr. Reddy", "Dr. Ayesha"])
        pat_CDoctor.place(relx=0.72,rely=0.22)

        pat_id_label = customtkinter.CTkLabel(PatInfoFrame, text="Consultation Reason *").place(relx=0.72,rely=0.32)
        pat_id_entry = customtkinter.CTkEntry(PatInfoFrame, placeholder_text="Consultation Reason", textvariable=pat_CReason).place(relx=0.72,rely=0.4)



        button = customtkinter.CTkButton(PatInfoFrame, text="Add Patient Record", command=self.in_pat_record).place(relx=0.38,rely=0.89, relwidth=0.25)

    def retreive_pat(self):

        PatInfoFrame = customtkinter.CTkFrame(PatMainDataFrame, corner_radius=15)
        PatInfoFrame.place(relx=0.02,rely=0.14,relheight=0.73,relwidth=0.96)

        pat_id=pat_retrieve.get()
        cursor.execute('select * from pat where pat_id={}'.format(pat_id))
        print(cursor.fetchone())

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

            CounterText=("Patients Currently \nRegistered:  ")
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
        label = customtkinter.CTkLabel(del_unsuccess_screen, text="The record was not deleted").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(del_unsuccess_screen, text="OK", command=self.destroy_del_unsuccess).pack(pady=12, padx=10)

    def del_success(self):
        global del_success_screen
        del_success_screen = customtkinter.CTkToplevel(self)
        del_success_screen.title("Success")
        del_success_screen.geometry("450x150")
        label = customtkinter.CTkLabel(del_success_screen, text="Successfully deleted the Patient Record").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(del_success_screen, text="OK", command=self.destroy_del_success).pack(pady=12, padx=10)
        


    def in_unsuccess(self):
        global in_unsuccess_screen
        in_unsuccess_screen = customtkinter.CTkToplevel(self)
        in_unsuccess_screen.title("Unsuccessful")
        in_unsuccess_screen.geometry("450x150")
        label = customtkinter.CTkLabel(in_unsuccess_screen, text="The record was not entered \n\nCheck the Patient ID entered").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(in_unsuccess_screen, text="OK", command=self.destroy_in_unsuccess).pack(pady=12, padx=10)

    def in_success(self):
        global in_success_screen
        in_success_screen = customtkinter.CTkToplevel()
        in_success_screen.title("Success")
        in_success_screen.geometry("450x150")
        label = customtkinter.CTkLabel(in_success_screen, text="Successfully inserted the Patient Record").pack(pady=12, padx=10)
        button = customtkinter.CTkButton(in_success_screen, text="OK", command=self.destroy_in_success).pack(pady=12, padx=10)


    # Doctor Functions
    def doc_start(self):
        global DocDataFrame
        self.geometry(f"{980}x{860}")


        DocDataFrame = customtkinter.CTkFrame(self, corner_radius=15)
        DocDataFrame.grid(row=0, column=1, rowspan=9, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")


        self.DocStartLabel = customtkinter.CTkLabel(DocDataFrame, text="Doctor's Availibility", font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=25, weight="bold")).place(relx=0.02,rely=0.035)

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

        path = "DMahmood-Jan.png"
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

        path = "DMahmood-Feb.png"
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

        path = "DMahmood-March.png"
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

        path = "DAnita-Jan.png"
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

        path = "DAnita-Feb.png"
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

        path = "DAnita-March.png"
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

        path = "DReddy-Jan.png"
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

        path = "DReddy-Feb.png"
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

        path = "DReddy-March.png"
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

        path = "DAyesha-Jan.png"
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

        path = "DAyesha-Feb.png"
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

        path = "DAyesha-March.png"
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

        CounterText=("Patients Currently \nRegistered:  ")
        PatCounter=CounterText + CurrentPatsStr
        
        self.PatsRN = customtkinter.CTkLabel(self.sidebar_frame, text=(PatCounter), font=customtkinter.CTkFont(family="Microsoft YaHei UI Light", size=18, weight="bold"))
        self.PatsRN.grid(row=4, column=0, padx=20, pady=(20, 10))

    def destroy_in_unsuccess(self):
        in_unsuccess_screen.destroy()
    def destroy_in_success(self):
        in_success_screen.destroy()
        self.pat_start()




if __name__ == "__main__":
    app = App()
    app.mainloop()