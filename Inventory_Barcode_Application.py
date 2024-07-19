from barcode import Code39
from barcode.writer import ImageWriter 
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from datetime import datetime
from PIL import Image, ImageTk


''''
        equipment_type = {
            "T" : 'Touch Workstation',
            "NT" : 'Touch Workstation',
            "AIO" : 'All in One Workstation',
            "DT" : 'Desktop Workstation',
            "MON" : 'Monintor',
            "WKBM" : 'Wireless Keyboard Mouse Combo',
            "KB" : "Keyboard USB",
            "MS" : "Mouse USB",
        }
        barcode_action = {
            '0000' : 'Inventory',
            '0001' : "Deployed",
            '0002' : "Return",
            '0003' : "Warranty",
            '0004' : "Broken",
            '0005' : "Recycle"
        }
'''

def connect_to_database():
    conn_str = 'DRIVER={SQL Server};SERVER={ESMHCANDBP3};DATABASE={AnalyticsAdhoc};Trusted_Connection=yes'
    try:
         conn = pyodbc.connect(conn_str)
         return conn
        
    except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None
    
def connect_to_hr_database():
    conn_str = 'DRIVER={SQL Server};SERVER={ESMHCANDBP3};DATABASE={AnalyticsSource};Trusted_Connection=yes'
    try:
        conn_HR = pyodbc.connect(conn_str)
        return conn_HR
            
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
        self.image_frame = ttk.Frame(root)
        ttk.Label(self.image_frame,image=self.jh_image,justify="right").grid(column=0,row=0)
        self.image_frame.place(x=1350, y= 0)

        self.login_title = ttk.Label(self.main_frame,text="Please Login Using your JHED Credentials", font = 'Arial 18 bold',foreground="#004B8D")
        self.login_title.grid(column=2,row=0)

        self.user_label_frame = ttk.LabelFrame(self.main_frame, text="User Credentials", width=300, height=300)
        self.user_label_frame.grid(column=2, row =2, sticky="nsew")

        ttk.Label(self.user_label_frame, text="Scan or enter your JHED ID", font=10, padding=10).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(self.user_label_frame, text="Enter first name", font=10, padding=10).grid(column=0, row=1, padx=5, pady=5)
        ttk.Label(self.user_label_frame, text="Enter last name", font=10, padding=10).grid(column=0, row=2, padx=5, pady=5)

        self.user_jhedID = ttk.Entry(self.user_label_frame, width=50)
        self.user_jhedID.bind("<Return>", lambda e: self.get_Name(e,self.user_fName))
        self.user_jhedID.grid(column=1, row=0, padx=10, pady=5)

        self.user_fName = ttk.Entry(self.user_label_frame, width=50)
        self.user_fName.bind("<Return>", lambda e: self.focus_next_widget(e,self.user_lName))
        self.user_fName.grid(column=1, row=1, padx=10, pady=5)

        self.user_lName = ttk.Entry(self.user_label_frame, width=50)
        self.user_lName.grid(column=1, row=2, padx=10, pady=5)
        self.user_fName.bind("<Return>", lambda e: self.submit_login(e))



        #Enter should check if they exist if not prompt them to try again
        ttk.Button(self.user_label_frame, text="Submit",command= self.submit_login).grid(column=0, row=4, columnspan=2, pady=10)


    def main_ui(self):
        """Main Frame""" 
        self.main_frame = ttk.Frame(root,width=800,height=800)
        self.main_frame.pack(expand=True)
        self.main_frame.propagate(True)
        self.switch_buttons_frame = tk.Frame(root,width=700,height=50)
        self.switch_buttons_frame.place(x=390,y=700)

        """Title"""
        self.title = ttk.Label(root,text="MIS Inventory log", font="Arial 20")
        self.title.place(x=600, y=0)
      
        '''Images'''
        self.image = Image.open("JH_logo.png")
        self.reduced_jh_iamge = self.image.resize((150,100))
        self.jh_image = ImageTk.PhotoImage(self.reduced_jh_iamge)

        '''Variables'''
        self.save_var = tk.IntVar()
        self.save_equipment = tk.IntVar()
        self.field2_var = tk.IntVar()
        self.field3_var = tk.IntVar()
        self.time = datetime.now()
        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.search_options = ("-----------" , "JHEID", "Device_Barcode", "EQ_Barcode", "fName", "lName", "Date", "Time")
        self.field1.set("-----------")
        self.field2.set("-----------")
        self.field3.set("-----------")

   
    """Home/Inserst page"""
    def insertion_page(self):
        self.insert_frame = ttk.Frame(self.main_frame)

        """Title"""
        self.title_frame = ttk.Frame(self.insert_frame)
        ttk.Label(self.title_frame,text="Regular Insert", font = 'Arial 18 bold',foreground="#004B8D").grid(column=0,row=0)
        self.title_frame.grid(column=3,row=0)

        self.entry_frame = ttk.Frame(self.insert_frame)
        single_item_entry_frame = ttk.LabelFrame(self.entry_frame, text="Single Item Entry", width=500, height=500)
        single_item_entry_frame.grid(column=0, row=0, ipadx=5, ipady=5)
        self.entry_frame.grid(column=3,row=6)

        ttk.Label(single_item_entry_frame, text="Scan Equipment barcode", font= 30,padding=10).grid(column=0,row=0)
        ttk.Label(single_item_entry_frame, text="Scan/ Enter the barcode of the device", font= 30,padding=10).grid(column=0,row=2)

        self.barcodeEquipment = ttk.Entry(single_item_entry_frame, width=50)
        self.barcodeEquipment.grid(column=0, row=1, padx=5, pady=5)
        self.barcodeEquipment.focus()
        self.barcodeEquipment.bind("<Return>", lambda e: self.focus_next_widget(e,self.deviceBarcode))

        self.deviceBarcode = ttk.Entry(single_item_entry_frame, width=50)
        self.deviceBarcode.grid(column=0, row=3, padx=5, pady=5)
        self.deviceBarcode.bind("<Return>", lambda e: self.focus_next_widget(e,self.return_jhedID))

        self.save_equip = ttk.Checkbutton(single_item_entry_frame, text="Save Equip barcode?",command=self.save_equip, variable=self.save_equipment).grid(column=0, row=5)

        """Logo"""
        self.image_frame = ttk.Frame(root)
        ttk.Label(self.image_frame,image=self.jh_image,justify="right").grid(column=0,row=0)
        self.image_frame.place(x=1350, y= 0)

        """Buttons"""
        self.buttons_frame = ttk.Frame(self.insert_frame)
        self.enter_button = ttk.Button(self.buttons_frame, text= "Enter", command=self.insertIntoDB).grid(column=0,row=0,padx=5,pady=5)
        self.clear = ttk.Button(self.buttons_frame, text= "Clear Entries", command=self.clear_entries).grid(column=0,row=2,padx=5,pady=5)
        self.buttons_frame.grid(column=8,row =6)

        """Owner Information"""
        self.owner_creds_frame = ttk.Frame(self.insert_frame,width=300,height=300)
        self.owner_creds_frame.grid(column=4,row=6)  
        owner_label_frame = ttk.LabelFrame(self.owner_creds_frame, text="Owner Creds here",width=300,height=300)
        owner_label_frame.grid(column=0,row=0)

        ttk.Label(owner_label_frame, text="Scan or enter owner JHED ID", font= 10,padding=10).grid(column=0,row=0)
        ttk.Label(owner_label_frame, text="Enter the owner's first name", font= 10,padding=10).grid(column=0,row=2)
        ttk.Label(owner_label_frame, text="Enter the owner's last Name", font= 10,padding=10).grid(column=0,row=4)

        self.return_fName = ttk.Entry(owner_label_frame, width=50)
        self.return_fName.grid(column=0, row=3, padx=5, pady=5)
        self.return_fName.configure(state="disabled")
        self.return_fName.bind("<Return>", lambda e: self.focus_next_widget(e,self.return_lName))

        self.return_lName = ttk.Entry(owner_label_frame, width=50)
        #self.return_lName.bind("<Return>", lambda e: self.insertIntoDB(e))
        self.return_lName.configure(state="disabled")
        self.return_lName.grid(column=0, row=5, padx=5, pady=5)

        self.return_jhedID = ttk.Entry(owner_label_frame, width=50)
        self.return_jhedID.grid(column=0, row=1, padx=5, pady=5)
        self.return_jhedID.configure(state="disabled")
        self.return_jhedID.bind("<Return>", lambda e: self.get_Name(e,self.return_fName))

        self.save_Creds = ttk.Checkbutton(owner_label_frame, text= "Device Return?", command=self.save_entries, variable=self.save_var).grid(column=0, row= 7)

        self.search_button_page = ttk.Button(self.switch_buttons_frame, text="Search", command=lambda: self.switch_pages(page=self.search_page))
        self.batch_insertion_button = ttk.Button(self.switch_buttons_frame, text="Batch Insert", command= lambda: self.switch_pages(self.batch_insertion))
        
        self.search_button_page.grid(column=0,row=0)
        self.batch_insertion_button.grid(column=1,row=0)

        
        self.insert_frame.grid(column=0,row=0)

    
    """Search Page"""
    def search_page(self):
        
        self.search_frame = ttk.Frame(self.main_frame)
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_filtered_frame = ttk.Frame(self.main_frame)

        self.search_by_frame = ttk.LabelFrame(self.search_frame,text= "Search", width=300, height=80)
        self.search_by_frame.grid(column=5,row=0)

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
        
        self.back_to_inserstion = ttk.Button(self.switch_buttons_frame, text="Insert", command=lambda:self.switch_pages(page=self.insertion_page)).grid(column=4,row=0,padx=5,pady=5)

    
        self.search_frame.grid(column=0,row=0)
        self.results_frame.grid(column=0,row=2)
        self.results_filtered_frame.grid(column=0,row=3)
    
    def batch_insertion(self):
        
        self.batch_insert_frame = ttk.LabelFrame(self.main_frame, text="Batch Insert Frame", width=300, height=300)
        self.batch_insert_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.batch_insert_frame, text="Scan Equipment barcode", font= 30,padding=10).grid(column=0,row=0)
        ttk.Label(self.batch_insert_frame, text="Scan/ Enter the barcode of the device", font= 30,padding=10).grid(column=0,row=2)

        self.batch_barcodeEquipment = ttk.Entry(self.batch_insert_frame, width=50)
        self.batch_barcodeEquipment.grid(column=0, row=1, padx=5, pady=5)
        self.batch_barcodeEquipment.focus()
        self.batch_barcodeEquipment.bind("<Return>", lambda e: self.batch_lock(e))

        self.batch_deviceBarcode = ttk.Entry(self.batch_insert_frame, width=50)
        self.batch_deviceBarcode.grid(column=0, row=3, padx=5, pady=5)
        self.batch_deviceBarcode.bind("<Return>", lambda e: self.batch_insertIntoDB(e))

        #ttk.Button(self.batch_insert_frame, text="Submit", command=self.batch_insertIntoDB).grid(column=0, row=4, columnspan=2, pady=10)

    def batch_lock(self,event):
        self.batch_barcodeEquipment.configure(state="disabled")
        self.batch_deviceBarcode.focus()
        self.batch_deviceBarcode.delete(0,tk.END)

    def switch_pages(self,page):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
            root.update()

        page()

    def save_entries(self):
        if self.save_var.get() == 1 :
            for entries in [self.return_jhedID, self.return_fName, self.return_lName]:
                entries.configure(state="normal")
        else:
            for entries in [self.return_jhedID, self.return_fName, self.return_lName]:
                entries.configure(state="disabled")

    def save_equip(self):
        if self.save_equipment.get() == 1 :
            self.barcodeEquipment.configure(state="disabled")
        else:
            self.barcodeEquipment.configure(state="normal")
    
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
            

    def insertIntoDB(self,event):
        jhedID = self.user[0]
        fName = self.user[1]
        lName = self.user[2]
        eq_barcode = self.barcodeEquipment.get()
        device = self.deviceBarcode.get()
        
        try:
            conn = connect_to_database()
            cursor= conn.cursor()
            cursor.execute("{CALL insert_into_DB (?,?,?,?,?,?)}", jhedID,fName,lName,eq_barcode,device,self.time)
            cursor.commit()
            self.show_entry()
            self.clear_entries()

        
        except Exception as e:
            messagebox.showerror("Database Error", f"Error inserting into to database: {e}")
            print("Database Error", f"Error inserting into to database: {e}")
            return None
        
    def batch_insertIntoDB(self,event):
        jhedID = self.user[0]
        fName = self.user[1]
        lName = self.user[2]
        eq_barcode = self.batch_barcodeEquipment.get()
        device = self.batch_deviceBarcode.get()
        
        #try:
        conn = connect_to_database()
        cursor= conn.cursor()
        cursor.execute("{CALL insert_into_DB (?,?,?,?,?,?)}", jhedID,fName,lName,eq_barcode,device,self.time)
        cursor.commit()
        self.show_batch_entry()
        self.batch_deviceBarcode.delete(0,tk.END)
        self.batch_deviceBarcode.focus()

        
        #except Exception as e:
            #messagebox.showerror("Database Error", f"Error inserting into to database: {e}")
            #print("Database Error", f"Error inserting into to database: {e}")
            #return None
            
            
    def show_entry (self):
        
        str = (f"JHEID: {self.user[0]}\n" 
        f"Time: {self.time}\n"
        f"Successfully imported device {self.deviceBarcode.get()} into the database! \n")
        messagebox.showinfo("Sucessful Insertion", str)
    
    def show_batch_entry (self):
        
        str = (f"JHEID: {self.user[0]}\n" 
        f"Time: {self.time}\n"
        f"Successfully imported device {self.batch_deviceBarcode.get()} into the database! \n")
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
        else:
            messagebox.showerror("LOGIN FAILURE","Must Log in with correct credentials")
            self.user_jhedID.focus()
            
    def clear_entries(self):
        entries = [self.return_jhedID, self.return_fName, self.return_lName, self.barcodeEquipment, self.deviceBarcode]
        if self.save_var.get() == 1:
            entries.remove(self.return_jhedID)
            entries.remove(self.return_fName)
            entries.remove(self.return_lName)
            self.barcodeEquipment.focus()
        elif self.save_equipment.get() == 1:
            entries.remove(self.barcodeEquipment)
        for entry in entries :
            entry.delete(0,tk.END)
        self.barcodeEquipment.focus()
        


    def readAll(self):
        conn = connect_to_database()
        cursor= conn.cursor()
        cursor.execute('{CALL read_all}')
        self.res = cursor.fetchall()


    def filtered_read(self):
        field1_drop_val = self.field1.get()
        field2_drop_val = self.field2.get()
        field3_drop_val = self.field3.get()
        stmnt = "SELECT JHEID, fName, lName, EQ_Barcode, Device_Barcode, CONVERT(varchar, Insert_Date_Time, 101) AS insert_date, CONVERT(varchar, Insert_Date_Time, 108) AS insert_time FROM inventory WHERE"

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

        columns = ('JHEID', 'fName', 'lName', 'EQ Barcode', 'Device Barcode', 'Date','Time')
        self.inventory = ttk.Treeview(self.results_filtered_frame, columns=columns,show='headings')
        for col in columns:
            self.inventory.heading(col, text=col)

        for value in self.res:
            self.inventory.insert("", tk.END, values=value)

        self.inventory.grid(column=0,row=8)

    def filtered_show(self):

        columns = ('JHEID', 'fName', 'lName', 'EQ Barcode', 'Device Barcode', 'Date','Time')
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

    def get_Name(self,event,next_widget):
        conn_HR = connect_to_hr_database()
        curr_HR = conn_HR.cursor()
        JHED = self.user_jhedID.get()
    
        curr_HR.execute(f"SELECT EmployeeFirstName, EmployeeLastName FROM [derived].[EmployeeList] WHERE EmployeeJHED = '{JHED}'")
        self.res = curr_HR.fetchall()

        if not self.res :
            messagebox.showerror("User Not Found", "This user does not exist please try other credentials")

        for row in self.res:
            self.user_fName.insert(tk.END, row[0])
            self.user_lName.insert(tk.END, row[1])

            next_widget.focus()
        return 'break'
    

if __name__ == "__main__":
    root=tk.Tk()
    app = BarcodeApp(root)
    root.mainloop()

    

