
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch



""""
equipment_type = {
            "T" : 'Touch Workstation',
            "NT" : 'Touch Workstation',
            "AIO" : 'All in One Workstation',
            "DT" : 'Desktop Workstation',
            "MON" : 'Monintor',
            "WKBM" : 'Wireless Keyboard Mouse Combo',
            "KB" : "Keyboard USB",
            "MS" : "Mouse USB",
            "DOC": "Docking Station"
        }
barcode_action = {
            '0000' : 'Inventory',
            '0001' : "Deployed",
            '0002' : "Return",
            '0003' : "Warranty",
            '0004' : "Broken",
            '0005' : "Recycle"
        }
"""""

def connect_to_database():
    conn_str = 'DRIVER={SQL Server};SERVER={ESMHCANDBP3};DATABASE={AnalyticsSource};Trusted_Connection=yes'
    try:
         conn = pyodbc.connect(conn_str)
         return conn
        
    except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None
#def clearInputs():

class BarcodeApp:
    def __init__(self, root):
        self.root= root
        self.root.title("Inventory log")

        self.main_ui()
        self.loginScreen()
        
    def loginScreen(self):
        self.title = ttk.Label(root,text="MIS Inventory log", font="Arial 20 bold",foreground="#004B8D")
        self.title.place(x=600, y=20)
       
        self.image_frame = ttk.Frame(root)
        ttk.Label(self.image_frame,image=self.jh_image,justify="right").grid(column=0,row=0)
        self.image_frame.place(x=1350, y= 0)

        self.login_title = ttk.Label(self.main_frame,text="Please Login Using your JHED Credentials", font = 'Arial 18 bold',foreground="#004B8D")
        self.login_title.grid(column=2,row=0)

        self.user_label_frame = ttk.LabelFrame(self.main_frame, text="User Credentials", width=300, height=300)
        self.user_label_frame.grid(column=2, row =2, sticky="nsew")

        ttk.Label(self.user_label_frame, text="Scan or enter your Card Number", font=10, padding=10).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(self.user_label_frame, text="Enter first name", font=10, padding=10).grid(column=0, row=1, padx=5, pady=5)
        ttk.Label(self.user_label_frame, text="Enter last name", font=10, padding=10).grid(column=0, row=2, padx=5, pady=5)

        self.user_jhedID = ttk.Entry(self.user_label_frame, width=50)
        self.user_jhedID.bind("<Return>", lambda e: self.get_user(e,self.user_fName,self.user_jhedID,self.user_fName,self.user_lName))
        self.user_jhedID.grid(column=1, row=0, padx=10, pady=5)

        self.user_fName = ttk.Entry(self.user_label_frame, width=50)
        self.user_fName.bind("<Return>", lambda e: self.focus_next_widget(e,self.user_lName))
        self.user_fName.grid(column=1, row=1, padx=10, pady=5)

        self.user_lName = ttk.Entry(self.user_label_frame, width=50)
        self.user_lName.grid(column=1, row=2, padx=10, pady=5)
        self.user_fName.bind("<Return>", lambda e: self.submit_login(e))


    def main_ui(self):
        """Main Frame""" 
        self.main_frame = ttk.Frame(root,width=800,height=800)
        self.main_frame.pack(expand=True)
        self.main_frame.propagate(True)
        self.switch_buttons_frame = tk.Frame(root,width=700,height=50)
        self.switch_buttons_frame.place(x=390,y=700)

        """Title"""
        self.title = ttk.Label(root,text="MIS Inventory log", font="Arial 20 bold",foreground="#004B8D")
        self.title.place(x=600, y=20)

        '''Images'''
        self.image = Image.open("JH_logo.png")
        self.reduced_jh_iamge = self.image.resize((150,100))
        self.jh_image = ImageTk.PhotoImage(self.reduced_jh_iamge)

        '''Variables'''
        self.save_var = tk.IntVar()
        self.batch_var = tk.IntVar()
        self.save_owner_creds =  tk.IntVar()
        self.field2_var = tk.IntVar()
        self.field3_var = tk.IntVar()
        self.time = datetime.now()
        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.search_options = ("-----------" , "Scanned_Badge_ID", "Equip_Serial", "Equip_Barcode", "Return_Fname", "Return_Lname", "Owner_JHED")
        self.field1.set("-----------")
        self.field2.set("-----------")
        self.field3.set("-----------")

   
    """Home/Inserst page"""
    def device_return_page(self):
        
        
        self.insert_frame = ttk.Frame(self.main_frame)

        self.navbar =ttk.LabelFrame(self.insert_frame, text="Switch Pages", width=200,  relief=tk.RAISED, borderwidth=2)
        
        #self.navbar.grid(column=4,row=10)

        """Title"""
      
        
        #self.return_label = ttk.Label(root,text="Regular Insert", font = 'Arial 18 bold',foreground="#004B8D")
        self.navbar.grid(column=4,row=10) 

        self.entry_frame = ttk.Frame(self.insert_frame)
        single_item_entry_frame = ttk.LabelFrame(self.entry_frame, text="Device", width=500, height=500)
        single_item_entry_frame.grid(column=0, row=0, ipadx=5, ipady=5)
        self.entry_frame.grid(column=4,row=7)

        ttk.Label(single_item_entry_frame, text="Scan Equipment barcode", font= 30,padding=10).grid(column=0,row=0)
        ttk.Label(single_item_entry_frame, text="Scan/ Enter the barcode of the device", font= 30,padding=10).grid(column=0,row=2)
        ttk.Label(self.main_frame, text="Device Return Page", font= 'Arial 18 bold', foreground="#004B8D" ).place(x=200,y=0)

        self.barcodeEquipment = ttk.Entry(single_item_entry_frame, width=50)
        self.barcodeEquipment.grid(column=0, row=1, padx=5, pady=5)
        self.barcodeEquipment.focus()
        self.barcodeEquipment.bind("<Return>", lambda e: self.focus_next_widget(e,self.deviceBarcode))

        self.deviceBarcode = ttk.Entry(single_item_entry_frame, width=50)
        self.deviceBarcode.grid(column=0, row=3, padx=5, pady=5)

        self.deviceBarcode.bind("<Return>", lambda e: self.focus_next_widget(e, self.return_jhedID))

        """Logo"""
        self.image_frame = ttk.Frame(root)
        ttk.Label(self.image_frame,image=self.jh_image,justify="right").grid(column=0,row=0)
        self.image_frame.place(x=1350, y= 0)


        """Owner Information"""
        self.owner_creds_frame = ttk.Frame(self.insert_frame,width=300,height=300)
        self.owner_creds_frame.grid(column=5,row=7)  
        owner_label_frame = ttk.LabelFrame(self.owner_creds_frame, text="Owner Creds here",width=300,height=300)
        owner_label_frame.grid(column=0,row=0)

        ttk.Label(owner_label_frame, text="Scan or enter owner JHED ID", font= 10,padding=10).grid(column=0,row=0)
        ttk.Label(owner_label_frame, text="Enter the owner's first name", font= 10,padding=10).grid(column=0,row=2)
        ttk.Label(owner_label_frame, text="Enter the owner's last Name", font= 10,padding=10).grid(column=0,row=4)
        ttk.Label(owner_label_frame,text="Comments", font= 10,padding=10).grid(column=0,row=6)

        self.return_fName = ttk.Entry(owner_label_frame, width=50)
        self.return_fName.grid(column=0, row=3, padx=5, pady=5)
        self.return_fName.bind("<Return>", lambda e: self.focus_next_widget(e,self.return_lName))

        self.return_lName = ttk.Entry(owner_label_frame, width=50)
        self.return_lName.grid(column=0, row=5, padx=5, pady=5)

        self.return_jhedID = ttk.Entry(owner_label_frame, width=50)
        self.return_jhedID.grid(column=0, row=1, padx=5, pady=5)
        self.return_jhedID.bind("<Return>", lambda e: self.get_Name(e,self.return_commments,self.return_jhedID,self.return_fName,self.return_lName,self.return_commments))

        self.return_commments = ttk.Entry(owner_label_frame,width=50)
        self.return_commments.grid(column=0,row=7)
        self.return_commments.bind("<Return>" , lambda e: self.check_return_validation(e,self.barcodeEquipment,self.deviceBarcode,self.return_jhedID,self.return_fName,self.return_lName,self.return_commments))

        self.search_button_page = ttk.Button(self.navbar, text="Search Page", command=lambda: self.switch_pages(self.search_page),width=25)
        self.insertion_button = ttk.Button(self.navbar, text="Insert Page", command= lambda: self.switch_pages(self.insertion_page),width=25)
        self.back_to_login = ttk.Button(self.navbar, text="Logout", command=self.check_logout,width=25)
        self.save_return_device = ttk.Checkbutton(owner_label_frame, text="Save Owner Credentials", variable=self.save_var, command=self.save_entries).grid(column=0,row=8)

        
        self.insert_frame.grid(column=0,row=0)

        
        self.search_button_page.grid(column=0,row=0)
        self.insertion_button.grid(column=1,row=0)
        self.back_to_login.grid(column=2,row=0)

    
    """Search Page"""
    def search_page(self):
        
        self.search_frame = ttk.Frame(self.main_frame)
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_filtered_frame = ttk.Frame(self.main_frame)
        self.navbar_search = ttk.LabelFrame(self.search_frame, text="Switch Pages", width=200,  relief=tk.RAISED, borderwidth=2)
        self.navbar_search.grid(column=5,row=1)
        ttk.Label(self.main_frame,text="Search Page", font = 'Arial 18 bold').place(x=0,y=0)

        self.search_by_frame = ttk.LabelFrame(self.search_frame,text= "Search", width=300, height=80)
        self.search_by_frame.grid(column=5,row=2)

        ttk.Label(self.search_by_frame, text="Field (Required)", font= 5).grid(column=1,row=0)
        ttk.Label(self.search_by_frame, text="Field 2 (Optional): ", font= 5).grid(column=1,row=2)
        ttk.Label(self.search_by_frame, text="Field 3 (Optional): ", font= 5).grid(column=1,row=4)
        ttk.Label(self.search_by_frame, text=" Value: ", font=5).grid(column= 3,row=0)
        ttk.Label(self.search_by_frame, text=" Value 2: ", font=5).grid(column= 3,row=2)
        ttk.Label(self.search_by_frame, text=" Value 3: ", font=5).grid(column= 3,row=4)
        
        
        self.search_value1 = ttk.Entry(self.search_by_frame, width=50)
        self.search_value1.grid(column=4,row=0)

        self.search_value2 = ttk.Entry(self.search_by_frame, width=50)
        self.search_value2.grid(column=4,row=2)
        self.search_value2.configure(state="disabled")

        self.search_value3 = ttk.Entry(self.search_by_frame, width=50)
        self.search_value3.grid(column=4,row=4)
        self.search_value3.configure(state="disabled")

        self.filter_search = ttk.Button(self.search_by_frame, text= "Filtered Search", command=self.filtered_show).grid(column= 6, row=2,padx=5,pady=5)
        self.show_results = ttk.Button(self.search_by_frame, text= "View All", command=self.Show_All).grid(column=6,row=0,padx=5,pady=5)
        self.clear_Table = ttk.Button(self.search_by_frame, text= "Clear", command=self.clear_tree).grid(column=6,row= 4,padx=5,pady=5)
        self.show_graph = ttk.Button(self.search_by_frame, text= "Show graph", command=self.show_plot).grid(column=6,row= 5,padx=5,pady=5)

        self.toReturn_search = ttk.Button(self.navbar_search,text="Device Return Page", command=lambda:self.switch_pages(self.device_return_page),width=25)
        self.toInsert_search = ttk.Button(self.navbar_search, text="Insert Page", command=lambda:self.switch_pages(self.insertion_page),width=25)
        self.toLogin_search = ttk.Button(self.navbar_search,text="Logout", command=self.check_logout,width=25)


        self.check_field2 = ttk.Checkbutton(self.search_by_frame, command=self.field_handling, variable=self.field2_var).grid(column=0, row= 2)
        self.check_field3 = ttk.Checkbutton(self.search_by_frame, command=self.field_handling, variable=self.field3_var).grid(column=0, row= 4)
       
        self.field1_dropdown = ttk.OptionMenu(self.search_by_frame, self.field1, *self.search_options)
        self.field1_dropdown.grid(column= 2, row=0)

        self.field2_dropdown = ttk.OptionMenu(self.search_by_frame, self.field2, *self.search_options)
        self.field2_dropdown.grid(column= 2, row=2)

        self.field2_dropdown.configure(state="disabled")
        self.field3_dropdown = ttk.OptionMenu(self.search_by_frame, self.field3, *self.search_options)

        self.field3_dropdown.configure(state="disabled")
        self.field3_dropdown.grid(column= 2, row=4)
        
        
        
        self.search_frame.grid(column=0,row=1)
        self.results_frame.grid(column=0,row=3)
        self.results_filtered_frame.grid(column=0,row=4)

        self.toReturn_search.grid(column=0,row=0)
        self.toInsert_search.grid(column=1,row=0)
        self.toLogin_search.grid(column=2,row=0)
      
    
    def insertion_page(self):
        
        self.batch_insert_frame = ttk.LabelFrame(self.main_frame, text=" Insert Frame", width=300, height=300)
        self.batch_insert_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.navbar_batch = ttk.Labelframe(self.main_frame,text="Switch Pages",width=200,  relief=tk.RAISED, borderwidth=2)

        ttk.Label(self.batch_insert_frame, text="Scan Equipment barcode", font= 30,padding=10).grid(column=0,row=0)
        ttk.Label(self.batch_insert_frame, text="Scan/ Enter the barcode of the device", font= 30,padding=10).grid(column=0,row=2)
        ttk.Label(self.batch_insert_frame, text="Issued to", font= 30,padding=10).grid(column=0,row=4)
        ttk.Label(self.batch_insert_frame, text="Comments", font= 30,padding=10).grid(column=0,row=6)
       
        


        self.batch_barcodeEquipment = ttk.Entry(self.batch_insert_frame, width=50)
        self.batch_barcodeEquipment.grid(column=0, row=1, padx=5, pady=5)
        self.batch_barcodeEquipment.focus()
        self.batch_barcodeEquipment.bind("<Return>", lambda e: self.focus_next_widget(e,self.batch_deviceBarcode))

        self.batch_deviceBarcode = ttk.Entry(self.batch_insert_frame, width=50)
        self.batch_deviceBarcode.grid(column=0, row=3, padx=5, pady=5)
        self.batch_deviceBarcode.bind("<Return>", lambda e: self.focus_next_widget(e,self.insert_issued_to))

        self.insert_issued_to = ttk.Entry(self.batch_insert_frame, width=50)
        self.insert_issued_to.grid(column=0, row=5, padx=5, pady=5)
        self.insert_issued_to.bind("<Return>", lambda e: self.focus_next_widget(e,self.insert_comments) )

        self.insert_comments = ttk.Entry(self.batch_insert_frame, width=50)
        self.insert_comments.grid(column=0, row=7, padx=5, pady=5)
        self.insert_comments.bind("<Return>", lambda e: self.check_validation(e,self.batch_deviceBarcode,self.batch_barcodeEquipment, self.insert_issued_to, self.insert_comments))
       
        self.batch_checkbox = ttk.Checkbutton(self.batch_insert_frame, text="batch insert?",command=self.batch_lock,variable=self.batch_var)
        self.batch_checkbox.grid(column=0,row=8)

        self.toInsert_search = ttk.Button(self.navbar_batch,text="Device Return Page", command=lambda:self.switch_pages(self.device_return_page),width=25)
        self.toBatch_search = ttk.Button(self.navbar_batch, text="Search Page", command=lambda:self.switch_pages(self.search_page),width=25)
        self.toLogin_search = ttk.Button(self.navbar_batch, text="Logout", command=self.check_logout,width=25)

        self.toInsert_search.grid(column=0,row=0)
        self.toBatch_search.grid(column=1,row=0)
        self.toLogin_search.grid(column=2,row=0)

        self.navbar_batch.grid(column=0,row=1)

        
    
    def check_logout(self):
        logout_answer =  messagebox.askyesno("Log out",f"You are about to Log out are you sure? \n")

        if logout_answer:
            self.switch_pages(self.loginScreen)
            self.current_user.destroy()
        else:
            return

    def check_validation(self,event,device,equipment,issued_to,comments):
        #action = barcode_action.get(self.batch_barcodeEquipment.get().split('-')[-1])
        #code = equipment.get().split('-')[-1]
        #item = equipment.get().split('-')[1]
        equipment_code = equipment.get()
        conn = connect_to_database()
        cursor = conn.cursor()


       

        if equipment_code.endswith('0010'):
            messagebox.showerror("WRONG PAGE", f"The code you entered: {equipment_code} \n Is a device return code. \n For codes ending in 0010 please refer to the device return page \n" )
            equipment.delete(0,tk.END)
            equipment.focus()
        else:
            cursor.execute("{CALL [inv].[app_select_equip_action] (?)} ",equipment_code)

            self.val_res = cursor.fetchone()

            answer = messagebox.askyesno("Insert Check",f"You are about to insert device: {device.get()} \n as {self.val_res} \n Issued to: {issued_to.get()} \n With comments: {comments.get()} \n")


            if answer:
                self.insertIntoDB(equipment,device,comments,issued_to)
            else:
                device.delete(0,tk.END)
                equipment.configure(state="normal")
                self.batch_var.set(0)
                equipment.delete(0,tk.END)
                equipment.focus()
        
    def check_return_validation(self,event,equip_code,device,return_JHED,fname,lname,comments):
        
        equipment_code= equip_code.get()
        conn = connect_to_database()
        cursor = conn.cursor()

        if not equipment_code.endswith("0010"):
            messagebox.showerror("WRONG PAGE", f"The code you entered: {equipment_code} \n Is not a device return code \n, for codes not ending in 0010 please refer to the insert page \n" )
            equip_code.delete(0,tk.END)
            equip_code.focus()
        else:  
            cursor.execute("{CALL [inv].[app_select_equip_action] (?)} ",equipment_code)

            self.val_res = cursor.fetchone()


        #cursor.execute(f"SELECT Action, Item FROM [AnalyticsAdhoc].[dbo].[inventory_actions],[AnalyticsAdhoc].[dbo].[inventory_items]  WHERE Barcode = {code}")
            answer = messagebox.askyesno("Insert Check",f"You are about to insert device: {device.get()} \n as {self.val_res} \n from: {fname.get()} {lname.get()} \n Comments: {comments.get()} ")


            if answer:
                self.insert_Device_Return(fname,lname,comments,equip_code,device,return_JHED)
            else:
                device.delete(0,tk.END)
                equip_code.configure(state="normal")
                equip_code.delete(0,tk.END)
                equip_code.focus()


    def batch_lock(self):
        if self.batch_var.get() == 1:
            self.batch_barcodeEquipment.configure(state="disabled")
        else:
            self.batch_barcodeEquipment.configure(state="normal")


    def switch_pages(self,page):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
            root.update()

        page()

    def save_entries(self):
        if self.save_var.get() == 1 :
            for entries in [self.return_jhedID, self.return_fName, self.return_lName]:
                entries.configure(state="disabled")
        else:
               for entries in [self.return_jhedID, self.return_fName, self.return_lName]:
                entries.configure(state="normal")
    
    def focus_next_widget(self,event,next_widget):
        next_widget.focus()
        return 'break'
    
    def field_handling(self):
        if self.field2_var.get() == 1:
            self.field2_dropdown.configure(state="normal")
            self.search_value2.configure(state="normal")
        else:
            self.field2_dropdown.configure(state="disabled")
            self.search_value2.configure(state="disabled")

        if self.field3_var.get() == 1:
            self.field3_dropdown.configure(state="normal")
            self.search_value3.configure(state="normal")
        else:
            self.field3_dropdown.configure(state="disabled")
            self.search_value3.configure(state="disabled")
            

    def insertIntoDB(self,barcode,device,comments,issued_to):
        cardNo = self.user[0]
        eq_barcode = barcode.get()
        device = device.get()
        comments = comments.get()
        issued_to = issued_to.get()
        
        try:
            conn = connect_to_database()
            cursor= conn.cursor()
            cursor.execute("{CALL [inv].[app_Insert_Records] (?,?,?,?,?,?)}", cardNo,eq_barcode,device,issued_to,comments,self.time)
            cursor.commit()
        
        except Exception as e:
            messagebox.showerror("Database Error", f"Error inserting into to database: {e}")
            print("Database Error", f"Error inserting into to database: {e}")
            return None
        
        self.show_entry(device)
        self.clear_insert_entries()
        

    def insert_Device_Return(self,fname,lname,comments,equip_code,device,return_JHED):

        cardNo = self.user[0]
        fname = fname.get()
        lname = lname.get()
        equip_code = equip_code.get()
        device = device.get()
        return_JHED = return_JHED.get()
        comments = comments.get()


        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("{CALL [inv].[app_insert_record_return] (?,?,?,?,?,?,?,?)}" , equip_code,device, return_JHED, fname, lname, comments, cardNo, self.time)
            cursor.commit()

        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Error inserting into to database: {e}")
            print("Database Error", f"Error inserting into to database: {e}")
            return None
        
        self.show_entry(device)
        self.clear_return_entries()
        
    def show_entry (self,device):
        
        str = (f"JHEID: {self.user[0]}\n" 
        f"Time: {self.time}\n"
        f"Successfully imported device {device} into the database! \n as {self.val_res}")
        messagebox.showinfo("Sucessful Insertion", str)

    def clear_tree(self):
        for widgets in self.results_frame.winfo_children():
            widgets.destroy()
        for widgets in self.results_filtered_frame.winfo_children():
            widgets.destroy()

        for entries in [self.search_value1, self.search_value2, self.search_value3]:
            entries.delete(0,tk.END)
        self.field1.set("-----------")
        self.field2.set("-----------")
        self.field3.set("-----------")

    def submit_login(self,event):

        if self.user_jhedID.get() and  self.user_fName.get() and self.user_lName.get():
            messagebox.showinfo("SUCCESSFULL LOGIN ", "LOGIN SUCCESS, WELCOME TO THE MIS INVENTORY SYSTEM")
            self.user = [self.user_jhedID.get(),self.user_fName.get(),self.user_lName.get()]
            self.switch_pages(self.insertion_page)
            self.current_user = ttk.Label(root,text=f"Current User: {self.user[1], self.user[2]}", font="Arial 20 bold",foreground="#004B8D",)
            self.current_user.place(x=20, y=20)

        else:
            messagebox.showerror("LOGIN FAILURE","Must Log in with correct credentials")
            self.user_jhedID.focus()
            
    def clear_return_entries(self):
        entries = [self.return_jhedID, self.return_fName, self.return_lName, self.barcodeEquipment, self.deviceBarcode,self.return_commments]
        if self.save_var.get() == 1:
            self.barcodeEquipment.delete(0,tk.END) 
            self.deviceBarcode.delete(0,tk.END)
            self.return_commments.delete(0,tk.END)
        else:
            for entry in entries:
                entry.delete(0,tk.END)
        self.barcodeEquipment.focus()
        
    def clear_insert_entries(self):
        if self.batch_var.get() == 1:
            self.batch_deviceBarcode.delete(0,tk.END)
            self.insert_issued_to.delete(0,tk.END)
            self.insert_comments.delete(0,tk.END)
            self.batch_deviceBarcode.focus()
        else:
            self.batch_deviceBarcode.delete(0,tk.END)
            self.batch_barcodeEquipment.delete(0,tk.END)
            self.insert_issued_to.delete(0,tk.END)
            self.insert_comments.delete(0,tk.END)
            self.batch_barcodeEquipment.focus()
    def readAll(self):
        conn = connect_to_database()
        cursor= conn.cursor()
        cursor.execute('{CALL [inv].[app_select_records]}')
        self.res = cursor.fetchall()


    def filtered_read(self):
        field1_drop_val = self.field1.get()
        field2_drop_val = self.field2.get()
        field3_drop_val = self.field3.get()
        stmnt = "SELECT [Scanned_Badge_ID], [Return_Fname], [Return_Lname], [Owner_JHED], [Equip_Barcode], [Equip_Serial], CONVERT(varchar, [Scanned_InsertDateTime], 101) AS insert_date, CONVERT(varchar, [Scanned_InsertDateTime], 108) AS insert_time FROM [inv].[Equipment_Register_vw] WHERE"

        conn = connect_to_database()
        cursor= conn.cursor()
        

        if field1_drop_val == "-----------":
            messagebox.showerror("Field 1 must be completed", "Must choose at least one search value,\n Please fill choose a value to search for\n")


        if field1_drop_val in self.filtered_columns and field2_drop_val and field3_drop_val not in self.filtered_columns:
            cursor.execute(f"{stmnt} {field1_drop_val} = '{self.search_value1.get()}'")
            self.res = cursor.fetchall()

        if field1_drop_val and field2_drop_val in self.filtered_columns and field3_drop_val not in self.filtered_columns:
            cursor.execute(f"{stmnt} {field1_drop_val} = '{self.search_value1.get()}' AND {field2_drop_val} = '{self.search_value2.get()}'")
            self.res = cursor.fetchall()

        if field1_drop_val and field2_drop_val and field3_drop_val in self.filtered_columns:
            cursor.execute(f" {stmnt} {field1_drop_val} = '{self.search_value1.get()}' AND {field2_drop_val} = '{self.search_value2.get()}' AND {field3_drop_val} = '{self.search_value3.get()}'")
            self.res = cursor.fetchall()

        if not self.res :
            messagebox.showerror("NO RESULTS FOUND", "No results of the above query have been found, Please Try Again")
    
        '''''
        if  field1_drop_val in self.filtered_columns and self.search_value1.get() in self.filtered_values and  field2_drop_val and field3_drop_val not in self.filtered_columns:
            cursor.execute(f"SELECT {field1_drop_val} FROM inventory WHERE {field1_drop_val} LIKE '%{self.search_value1.get()}%'")
            self.res = cursor.fetchall()
            print(self.search_value1.get())
        '''''

    """Table Results"""
    def Show_All(self):
        self.readAll()

        columns = ('cardNo', 'EQ BARCODE', 'Device', 'Return/Swap JHED', 'Date')
        self.inventory = ttk.Treeview(self.results_filtered_frame, columns=columns,show='headings')
        for col in columns:
            self.inventory.heading(col, text=col)

        for value in self.res:
            self.inventory.insert("", tk.END, values=value)

        self.inventory.grid(column=0,row=8)

    def filtered_show(self):

        columns = ('cardNo', 'return_fName', 'return_lName', 'return/swap JHED', 'EQ Barcode', 'Device Barcode', 'Date')
        self.filtered_columns = []
        filters = [self.field1.get()]

        if self.field2_var.get() == 1:
            filters.append(self.field2.get())

        if self.field3_var.get() == 1:
            filters.append(self.field3.get())

        elif self.field2_var.get() == 0 and self.field2.get() in filters:
            filters.remove(self.field2.get())

        elif self.field3_var.get() == 0 and self.field3.get() in filters:
            filters.remove(self.field3.get())

        for filter in filters:
            self.filtered_columns.append(filter)
        
        self.filtered_inventory = ttk.Treeview(self.results_frame, columns=columns,show="headings")
        for col in columns:
            self.filtered_inventory.heading(col, text=col)

        self.filtered_read()
        for value in self.res:
            self.filtered_inventory.insert("", tk.END, values=value)


        self.filtered_inventory.grid(column=5,row=8)

    def get_user(self,event,next_widget,ID,fname,lname):

        conn = connect_to_database()
        curr = conn.cursor()
        cardNo = ID.get()

        curr.execute('{CALL [inv].[app_getuser] (?)}',cardNo)

        self.res = curr.fetchall()

        if not self.res :
            messagebox.showerror("User Not Found", "This user does not exist please try other credentials")

        for row in self.res:
            fname.insert(tk.END, row[0])
            lname.insert(tk.END, row[1])

            next_widget.focus()
        return 'break'

    def get_Name(self,event,next_widget,ID,fname,lname,comments):
        conn_HR = connect_to_database()
        curr_HR = conn_HR.cursor()
        JHED = ID.get()
    
        curr_HR.execute(f"SELECT EmployeeFirstName, EmployeeLastName FROM [derived].[EmployeeList] WHERE EmployeeJHED = '{JHED}'")
        self.res = curr_HR.fetchall()

        if not self.res:
            answer = messagebox.askyesnocancel("User Not Found", "This user does not exist. Do you wish to continue")
            if answer:
                comments.focus()
            else:
                return
        else:
             if not fname.get():
                    for row in self.res:
                        fname.insert(tk.END, row[0])
                        lname.insert(tk.END, row[1])
        
                    next_widget.focus()
             else:
                    comments.focus()

    def show_plot(self):
        equip_code_desc = []
        equip_code_action = []
        count = []

        conn_str = 'DRIVER={SQL Server};SERVER=ESMHCANDBP3;DATABASE=AnalyticsSource;Trusted_Connection=yes'
        try:
            conn = pyodbc.connect(conn_str)
        except Exception as e:
            print("Database Error", f"Error connecting to database: {e}")

        # Create a cursor object
        cursor = conn.cursor()

        # Execute SQL query
        cursor.execute("SELECT * FROM [inv].[Equip_Item_count_vw]")

        # Fetch and store data
        for rows in cursor.fetchall():
            equip_code_desc.append(rows[0])
            equip_code_action.append(rows[1])
            count.append(rows[2])

        # Create a DataFrame
        df = pd.DataFrame({
            'Equip_Code_Desc': equip_code_desc,
            'Equip_Code_Action': equip_code_action,
            'Count': count
        })

        # Plotting
        df_grouped = df.groupby(['Equip_Code_Desc', 'Equip_Code_Action']).sum().unstack()
        ax = df_grouped.plot(kind='bar', stacked=True, title='Equipment Actions Tracker')

        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')


        for container in ax.containers:
            # Iterate over each container (representing a set of stacked bars)
            for patch in container:
                height = patch.get_height()
                if height > 0:  # Only annotate non-zero bars
                    # Find the bottom of the current patch
                    bottom = patch.get_y() + (patch.get_height() - height)
                    # Add the annotation
                    ax.annotate(f'{int(height)}', xy=(patch.get_x() + patch.get_width() / 2, bottom + height / 2),
                                xytext=(0, 3), textcoords='offset points',
                                ha='center', va='center', fontsize='large', color='black')
                    
        ax.legend(title= 'Equipment Actions')
        # Add labels and show plot
        plt.xlabel('Equip Code Description')
        plt.ylabel('Count')
        plt.show()


if __name__ == "__main__":
    root=tk.Tk()
    app = BarcodeApp(root)
    root.mainloop()

    

