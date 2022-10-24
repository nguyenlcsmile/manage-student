#Các thư viên cần thiết (Cài đặt bằng cách pip install tên_thư_viện)
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd 
import numpy as np
import mysql.connector 

#=========================================================================
#=========================================================================
class Open_File:

    def __init__(self,root):
        #Thiết lập giao diện
        self.root = root
        self.root.title("Secrets Student Management System") #Title
        self.root.geometry("1350x700+0+0") #Kích thước
        
        #Các thuộc tính của title
        title = Label(self.root, text="Secrets Student Management System",bd = 10, relief=GROOVE, font=("Arial",43,"bold"), bg="#00A1E4",fg="#FFFCF9")
        title.pack(side=TOP,fill=X)

        #Variables (các biến cần thiết)
        self.dept_id = StringVar()
        self.dept_name = StringVar()
        self.search_combo = StringVar()
    
        #DashBoard Frame (chứa các thuộc tính mình cần (Open_File, Exit, Student))
        Dash_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="#F0EDEE")
        Dash_Frame.place(x=2,y=95,width=98,height=600)

        open_btn = Button(Dash_Frame,text="Open File",bg="#00A1E4",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.open_btn).grid(row=0,column=0,padx=2,pady=2,sticky="w")   

        manage_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Student",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.student_btn).grid(row=1,column=0,padx=2,pady=0,sticky="w")

        certificate_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Certificate",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.certificate_btn).grid(row=2,column=0,padx=2,pady=0,sticky="w")

        exit_btn = Button(Dash_Frame,text="Exit",bg="#00A1E4",fg="#F0EDEE",
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.logout).grid(row=3,column=0,padx=2,pady=2,sticky="w")  


        #Detail Frame (các nút thao tác (State, Open, Save, Log Out))
        Detail_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#FFFCF9")
        Detail_Frame.place(x=350, y=95, width=860, height=595)

        lbl_state = Label(Detail_Frame,text="State:",bg="#FFFCF9",fg="#0A090C",font=("Arial",18,"bold"))
        lbl_state.grid(row=0,column=5, pady=5, padx=15, sticky="w")

        state_box = ttk.Combobox(Detail_Frame, width=10,textvariable=self.search_combo, font=("Arial",13,"bold"),state="readonly")
        state_box['values'] = ("Open", "Other")
        state_box.grid(row=0, column=10, pady=12, padx=10, ipady=4, sticky="w")

        search_btn = Button(Detail_Frame,text="Open",bg="#00A1E4",fg="#FFFCF9",
        font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command= lambda: [self.clear_file(), self.open()]).grid(row=0,column=12,padx=10,pady=10)

        show_all_btn = Button(Detail_Frame,text="Save",bg="#00A1E4",fg="#FFFCF9",
        font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command=self.save).grid(row=0,column=13,padx=10,pady=10)

        logout_btn = Button(Detail_Frame, text="Log Out",bg="#00A1E4",fg="#FFFCF9",
        font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command=self.logout).grid(row=0,column=14,padx=10,pady=10)

        #Table Frame (chứa nội dung hiển thị)
        Background = Frame(Detail_Frame, bg="#0A090C")
        Background.place(x=20, y=70, width=825, height=515)

        #Vị trí hiển thị Table Frame
        Table_Frame = Frame(Detail_Frame)
        Table_Frame.place(x=23, y=73, width=819, height=508)

        #Thêm thanh cuộn cho Table_Frame
        X_scroll = Scrollbar(Table_Frame, orient=HORIZONTAL)
        Y_scroll = Scrollbar(Table_Frame, orient=VERTICAL)
        X_scroll.pack(side=BOTTOM, fill=X)
        Y_scroll.pack(side=RIGHT, fill=Y)

        # Nơi chưa text hiển thị
        self.txtarea = Text(Table_Frame, width=100, height=100, bd=4, font=("Arial", 12, "bold"), xscrollcommand=X_scroll.set, yscrollcommand=Y_scroll.set)
        self.txtarea.pack(pady=2)
        X_scroll.config(command=self.txtarea.xview)
        Y_scroll.config(command=self.txtarea.yview)

    def clear_file(self):
        ''' Clear text khi mình mở 1 text mới'''
        self.txtarea.delete("1.0","end")

    def open(self):
        #Kiểm tra xem trạng thái có phải Open không nếu không thì báo chọn Open
        if self.search_combo.get() != 'Open':
            messagebox.showerror("Error", "Please chosse state is Open")

        else:
            #Giúp mở file từ máy tính 
            tf = filedialog.askopenfilename(initialdir="/", 
                                            title="Open Text file", 
                                            filetypes=(("Text Files", "*.txt *.json"),))
            #In tên đường dẫn file
            print(tf)
            #Mở và đọc file txt
            with open(tf, 'r', encoding='utf-8') as f:
                data = f.read()
                self.txtarea.insert(INSERT, data)


    def save(self):
        ''' Lưu file txt'''
        #Lấy nội dung cần lưu
        data = self.txtarea.get("1.0",'end-1c')
        #Kiểm tra nội dung có hay không nếu không thì báo data is empty
        if data != '':
            #Thao tác với file và lấy đường dẫn file
            filename = filedialog.asksaveasfilename(initialdir='/', title='Save File', filetypes=(('Text Files', 'txt.*'), ('All Files', '*.*')))
            print(filename)
            #Mở file
            myfile = open(filename, "w+")
            #Viết nội dung vào file
            myfile.write(data)

        else:
            messagebox.showerror("Error","Data is Empty")

    #Hàm để mở Open_File
    def open_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Open_File(st_root)
        st_root.mainloop()

    #Hàm để thoát giao diện
    def logout(self):
        return self.root.destroy()
   
    #Hàm để mở Student 
    def student_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Student(st_root)
        st_root.mainloop()
    
    #Hàm mở Certificate
    def certificate_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Certificate(st_root)
        st_root.mainloop()
    
#=========================================================================
#=========================================================================
#=========================================================================
#=========================================================================

class Student:

    def __init__(self,root):
        self.root = root
        self.root.call('encoding', 'system', 'utf-8')
        self.root.title("Secrets Student Management System")
        self.root.geometry("1350x700+0+0")


        title = Label(self.root, text="Secrets Student Management System", bd = 10,relief=GROOVE,font=("Arial",43,"bold"),bg="#00A1E4",fg="#FFFCF9")

        title.pack(side=TOP,fill=X)

        #Variables
        self.sbd = StringVar()
        self.name = StringVar()
        self.date = StringVar()
        self.gender = StringVar()
        self.score_toan = StringVar()
        self.score_van = StringVar()
        self.school = StringVar()
        self.search_combo = StringVar()
        self.search_field = StringVar()

        
        #DashBoard Frame
        Dash_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#F0EDEE")
        Dash_Frame.place(x=2, y=95, width=98, height=600)


        open_btn = Button(Dash_Frame,text="Open File",bg="#00A1E4",fg="#F0EDEE", font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.open_btn).grid(row=0,column=0,padx=2,pady=2,sticky="w")   
        manage_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Student",fg="#F0EDEE", font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.student_btn).grid(row=1,column=0,padx=2,pady=0,sticky="w")
        certificate_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Certificate",fg="#F0EDEE", font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.certificate_btn).grid(row=2,column=0,padx=2,pady=0,sticky="w")
        exit_btn = Button(Dash_Frame,text="Exit",bg="#00A1E4",fg="#F0EDEE", font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.logout).grid(row=3,column=0,padx=2,pady=2,sticky="w")  

                           
        #Manage Frame

        Manage_Frame = Frame(self.root, bd=4,relief=RIDGE,bg="#F0EDEE")
        Manage_Frame.place(x=100,y=95,width=450,height=600)
        m_title = Label(Manage_Frame,text="Manage Student",bg="#F0EDEE",fg="#0A090C", font=("Arial",30,"bold","italic"))
        m_title.grid(row = 0,columnspan=2,pady=20)

        
        #Nơi điến số báo danh và các thuộc tính
        lbl_roll = Label(Manage_Frame,text="SBD.",bg="#F0EDEE",fg="black", font=("Arial",15,"bold"))
        lbl_roll.grid(row = 1,column=0,pady=10,padx=20,sticky="w")
        self.txt_Roll = Entry(Manage_Frame,textvariable=self.sbd,font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_Roll.grid(row = 1,column=1,pady=10,padx=20,sticky="w")

        #Nơi điền Họ và Tên và các thuộc tính
        lbl_name = Label(Manage_Frame,text="Họ và Tên.",bg="#F0EDEE",fg="black",font=("Arial",15,"bold"))
        lbl_name.grid(row = 2,column=0,pady=10,padx=20,sticky="w")
        self.txt_name = Entry(Manage_Frame,textvariable=self.name,font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_name.grid(row = 2,column=1,pady=10,padx=20,sticky="w")

        #Nơi điển Ngày sinh và các thuộc tính
        lbl_date = Label(Manage_Frame,text="Ngày sinh.",bg="#F0EDEE",fg="black",font=("Arial",15,"bold"))
        lbl_date.grid(row = 3,column=0,pady=10,padx=20,sticky="w")
        self.txt_date = Entry(Manage_Frame,textvariable=self.date,font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_date.grid(row = 3,column=1,pady=10,padx=20,sticky="w")

        #Nơi điền giới tính và các thuộc tính
        lbl_gender = Label(Manage_Frame,text="Gender",bg="#F0EDEE",fg="black",font=("Arial",15,"bold"))
        lbl_gender.grid(row = 4,column=0,pady=10,padx=20,sticky="w")
        self.gender_box = ttk.Combobox(Manage_Frame,textvariable=self.gender, font=("Arial",13,"bold"),state="readonly")
        self.gender_box['values'] = ("Nam","Nữ","Other")
        self.gender_box.grid(row=4,column=1,pady=10,padx=20,sticky="w")

        
        #Nơi điền điểm
        lbl_toan = Label(Manage_Frame,text="Điểm Toán.",bg="#F0EDEE",fg="black", font=("Arial",15,"bold"))
        lbl_toan.grid(row = 5,column=0,pady=10,padx=20,sticky="w")
        self.txt_toan = Entry(Manage_Frame,textvariable=self.score_toan, font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_toan.grid(row = 5,column=1,pady=10,padx=20,sticky="w")

        lbl_van = Label(Manage_Frame,text="Điểm Văn.",bg="#F0EDEE",fg="black", font=("Arial",15,"bold"))
        lbl_van.grid(row = 6,column=0,pady=10,padx=20,sticky="w")
        self.txt_van = Entry(Manage_Frame,textvariable=self.score_van,font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_van.grid(row = 6,column=1,pady=10,padx=20,sticky="w")

        #Nơi điền trường và các thuộc tính
        lbl_school = Label(Manage_Frame,text="Trường.",bg="#F0EDEE",fg="black", font=("Arial",15,"bold"))
        lbl_school.grid(row = 7,column=0,pady=10,padx=20,sticky="w")
        self.txt_school = Entry(Manage_Frame,textvariable=self.school, font=("Arial",15,"bold"),bd=5,relief=GROOVE)
        self.txt_school.grid(row = 7,column=1,pady=10,padx=20,sticky="w")

        #Các button Add Studetn và Delete Student theo số báo danh
        #Button Frame
        btn_frame = Frame(Manage_Frame,bg="#F0EDEE")
        btn_frame.place(x=100, y=520,width=410) 

        add_btn = Button(btn_frame,text="Add", width=10,bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),command= lambda: [self.add_student(), self.clear()]).grid(row=0,column=2,padx=10,pady=10)
        delete_btn = Button(btn_frame,text="Delete", width=10, bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),command=self.delete).grid(row=0,column=3,padx=10,pady=10)

        #Frăm hiển thị các thông tin
        #Detail Frame
        Detail_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="#FFFCF9")
        Detail_Frame.place(x=550,y=95,width=800,height=600)

        #Button Search 
        lbl_search = Label(Detail_Frame,text="Search:",bg="#FFFCF9",fg="#0A090C",font=("Arial",18,"bold"))
        lbl_search.grid(row = 0,column=0,pady=10,padx=15,sticky="w")

        #Các yêu cầu cần search
        search_box = ttk.Combobox(Detail_Frame,width=25,textvariable= self.search_combo, font=("Arial",13,"bold"),state="readonly")
        search_box['values'] = ("Show local", "Student cùng trường", "Học sinh kém", "Điển Toán lớn hơn Văn", "Thủ Khoa", "ADD Student", "Show database", "ADD Student database", "Delete database", "Other")
        search_box.grid(row=0,column=1,pady=10,padx=10,ipady=4,sticky="w")

        #Các nút thao tác thoe yêu cầu
        search_btn = Button(Detail_Frame,text="Search",bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command=self.search_data).grid(row=0,column=5,padx=10,pady=10)
        show_all_btn = Button(Detail_Frame,text="Show All",bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command=self.show_data).grid(row=0,column=6,padx=10,pady=10)
        logout_btn = Button(Detail_Frame,text="Log Out",bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),relief=GROOVE,width=10,pady=5,command=self.logout).grid(row=0,column=7,padx=10,pady=10)

        # Bảng chứa các thông tin sau search
        #Table Frame
        Table_Frame = Frame(Detail_Frame,bg="#0A090C")
        Table_Frame.place(x=10,y=60,width=760,height=505)

        
        X_scroll = Scrollbar(Table_Frame,orient=HORIZONTAL)
        Y_scroll = Scrollbar(Table_Frame,orient=VERTICAL)
        self.Table = ttk.Treeview(Table_Frame, columns=("SBD","Họ và Tên", "Ngày sinh", "Giới tính", "Trường", "Toán", "Văn", "Tổng điểm", "DTN", "Xếp loại"), xscrollcommand=X_scroll.set, yscrollcommand=Y_scroll.set)

        X_scroll.pack(side=BOTTOM,fill=X)
        Y_scroll.pack(side=RIGHT,fill=Y)
        X_scroll.config(command=self.Table.xview)
        Y_scroll.config(command=self.Table.yview)

        #Tạo cột cho table_frame
        self.Table.heading("SBD",text="SBD")
        self.Table.heading("Họ và Tên",text="Họ và Tên")
        self.Table.heading("Ngày sinh",text="Ngày sinh")
        self.Table.heading("Giới tính",text="Giới tính")
        self.Table.heading("Trường",text="Trường")
        self.Table.heading("Toán",text="Toán")
        self.Table.heading("Văn",text="Văn")
        self.Table.heading("Tổng điểm",text="Tổng điểm")
        self.Table.heading("DTN",text="DTN")
        self.Table.heading("Xếp loại",text="Xếp loại")

        #Kích thước của các cột
        self.Table['show']="headings"
        self.Table.column("SBD",width=100)
        self.Table.column("Họ và Tên",width=100)
        self.Table.column("Ngày sinh",width=100)
        self.Table.column("Giới tính",width=100)
        self.Table.column("Trường",width=100)
        self.Table.column("Toán",width=100)
        self.Table.column("Văn",width=100)
        self.Table.column("Tổng điểm",width=100)
        self.Table.column("DTN",width=100)
        self.Table.column("Xếp loại",width=150)
        self.Table.pack(fill=BOTH,expand=1)
        self.Table.bind('<ButtonRelease 1>',self.get_fields)
        self.txt_date.bind("<FocusIn>", self.foc_in)
        self.txt_date.bind("<FocusOut>", self.foc_out)

        #Nội dung hiển thị được lưu dưới dạng csv
        self.data_frame = pd.DataFrame()
        self.put_placeholder()
        # self.show_data()

    #Xóa các thông tin trong ô sbd, tên, trường,... khi điền vào 
    def clear(self):
        self.txt_toan.delete(0, END)
        self.txt_van.delete(0, END)
        self.txt_school.delete(0, END)
        self.txt_date.delete(0, END)
        self.txt_name.delete(0, END)
        self.txt_Roll.delete(0, END)
        self.gender_box.delete(0, END)
        
    def add_student(self):
        ''' Thêm student theo yêu cầu'''

        #Kiểm tra xem đã chọn là "ADD Student" hay chưa? và dữ liệu đã hiển thị trong bản hay chưa 
        if self.search_combo.get() == "ADD Student" and self.data_frame is not None:
            #Kiểm tra các ố sbd, trường, tên,... đã nhập hay chưa
            if self.sbd.get() == "" or self.name.get() == "" or self.date.get() == ""or self.gender.get()== "" or self.score_toan.get()== ""or self.score_van.get() == ""or self.txt_school.get() == "":
                messagebox.showerror("Error","All Fields are Required")

            else:
                #Lấy nội dung trong các ô sbd, tên, trường,...
                sbd = self.sbd.get()
                name = self.name.get()
                date = self.date.get()
                gender = self.gender.get()
                score_toan = self.score_toan.get()
                score_van = self.score_van.get()
                school = self.txt_school.get()
                total_score = float(score_van) + float(score_toan)

                #Tính toán để xem student có điểm toán hay văn thấp hơn
                if float(score_toan) > float(score_van):
                    dnt = float(score_van)
                else:
                    dnt = float(score_toan)

                #Xem student thêm vào thuộc xếp loại nào 
                if  total_score>= 16.0 and (float(score_toan) >= 7.0 or float(score_van) >= 7.0):
                    xep_loai = 'Giỏi'
                elif total_score >= 14 and (float(score_toan) >= 6.0 or float(score_van) >= 6.0):
                    xep_loai = 'Khá'
                elif total_score >= 10.0 and (float(score_toan) >= 4.0 or float(score_van) >= 4.0):
                    xep_loai = 'Trung Bình'
                else:
                    xep_loai = 'Yếu'
                
                #Tạo dữ liệu được lưu dưới dạng csv(excel)
                # print(sbd, name, date, gender, score_van, score_toan, school)
                data_add = np.array([sbd, name, date, gender, school, score_toan, score_van, total_score, dnt, xep_loai]).reshape(1, 10)
                frame_add = pd.DataFrame(data_add, columns=self.data_frame.columns)
                data_add = pd.concat([frame_add, self.data_frame])

                #Kiểm tra dữ liệu đã được tạo chưa và chèn dữ liệu và table_frame
                if len(data_add) != 0:
                    self.Table.delete(*self.Table.get_children())
                    for row in range(len(data_add)):
                        values = [i for i in data_add.iloc[row].values]
                        self.Table.insert('', END, values=values)

                #Thông báo đã chèn 
                messagebox.showinfo("Succes","Record Successfully Added")
        
        #Thêm student lên database 
        elif self.search_combo.get() == "ADD Student database" and self.data_frame is not None:
            if self.sbd.get() == "" or self.name.get() == "" or self.date.get() == ""or self.gender.get()== "" or self.score_toan.get()== ""or self.score_van.get() == ""or self.txt_school.get() == "":
                messagebox.showerror("Error","All Fields are Required")
            
            else:
                sbd = self.sbd.get()
                name = self.name.get()
                date = self.date.get()
                gender = self.gender.get()
                score_toan = self.score_toan.get()
                score_van = self.score_van.get()
                school = self.txt_school.get()
                total_score = float(score_van) + float(score_toan)

                if float(score_toan) > float(score_van):
                    dnt = float(score_van)
                else:
                    dnt = float(score_toan)

                if  total_score>= 16.0 and (float(score_toan) >= 7.0 or float(score_van) >= 7.0):
                    xep_loai = 'Giỏi'
                elif total_score >= 14 and (float(score_toan) >= 6.0 or float(score_van) >= 6.0):
                    xep_loai = 'Khá'
                elif total_score >= 10.0 and (float(score_toan) >= 4.0 or float(score_van) >= 4.0):
                    xep_loai = 'Trung Bình'
                else:
                    xep_loai = 'Yếu'
                # print(sbd, name, date, gender, score_van, score_toan, school)
                
                #Vì bảng mình tạo với các biến là char nên phải ép kiểu trước khi đưa vào database
                data_add_sql = tuple([str(sbd), str(name), str(date), str(gender), str(school), str(score_toan), str(score_van), str(total_score), str(dnt), str(xep_loai)])
                
                #Kết nối với database
                mydb_stu = mysql.connector.connect(
                    host="localhost",
                    user = "root",
                    passwd = "", 
                    database='students')

                # print(mydb_stu)

                #Thêm dữ liệu vào database
                mycurror = mydb_stu.cursor()
                sql = 'insert into stu_table(SBD, Họ_và_Tên, Ngày_sinh, Giới_tính, Trường, Điểm_Toán, Điểm_Văn, Tổng_điểm, DTN, Xếp_loại) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                mycurror.execute(sql, data_add_sql)
                mydb_stu.commit()

                #Cập nhật lại dữ liệu sau khi thêm vào databse để hiển thị ở Table Frame
                data_add = np.array([sbd, name, date, gender, school, score_toan, score_van, total_score, dnt, xep_loai]).reshape(1, 10)
                frame_add = pd.DataFrame(data_add, columns=self.data_frame.columns)
                data_add = pd.concat([frame_add, self.data_frame])

                if len(data_add) != 0:
                    self.Table.delete(*self.Table.get_children())
                    for row in range(len(data_add)):
                        values = [i for i in data_add.iloc[row].values]
                        self.Table.insert('', END, values=values)
                
                messagebox.showinfo("Succes","Record Successfully Added")

        else:
            messagebox.showerror("Error","Data is empty")

    def show_data(self):
        ''' Hiển thị dữ liệu'''
        #Kiểm tra xem đã chọn "Show all" ... không sử dụng database để đưa dữ liệu lên
        #Chọn file dữ liệu sau khi mình sử lí xong 
        #Dữ liệu sau khi xử lí xong bào gồm SBD, TÊN, TRƯỜNG, GIỚI TÍNH, ĐIỂM TOÁN, ĐIỂM VĂN, NGÀY SINH thiếu TỔNG ĐIỂN, DTN, XẾP LOẠI

        if self.search_combo.get() == "Show local":
            tf = filedialog.askopenfilename(initialdir="/", 
                                            title="Open Text file", 
                                            filetypes=(("Text Files", "*.txt *.json"),))
            print(tf)

            data_arr = []
            with open(tf, 'r', encoding='utf-8') as f:
                data = f.read()
                data = data.split('\n')
                
                for i in data:
                    a = np.array([i.split(',')]).reshape(1, 7)
                    data_arr.append(a)

            data_arr = np.array(data_arr)
            self.data_frame = pd.DataFrame(data_arr.reshape(len(data), 7), columns=['SBD', 'Họ_và_Tên', 'Ngày_sinh', 'Giới_tính', 'Trường', 'Điểm_Toán', 'Điểm_Văn'])
            
            #Ép dữ liệu điểm_toán và điểm_văn sang float để tiện cho việc tính toán
            self.data_frame['Điểm_Toán'] = self.data_frame['Điểm_Toán'].astype('float32')
            self.data_frame['Điểm_Văn'] = self.data_frame['Điểm_Văn'].astype('float32')
            #Tính tổng điểm
            total_score = self.data_frame['Điểm_Toán'] + self.data_frame['Điểm_Văn']
            self.data_frame['Tổng_điểm'] = total_score

            #Lấy điểm thấp nhất của điểm toán và văn của 1 học sinh
            dnt = []
            for i in range(len(self.data_frame)):
                if self.data_frame['Điểm_Văn'][i] > self.data_frame['Điểm_Toán'][i]:
                        dnt.append(self.data_frame['Điểm_Toán'][i])
                else:
                        dnt.append(self.data_frame['Điểm_Văn'][i])
            self.data_frame['DTN'] = dnt
            
            #Xếp loại học sinh
            xep_loai = []
            for i in range(len(self.data_frame)):
                if self.data_frame['Tổng_điểm'][i] >= 16.0 and (self.data_frame['Điểm_Toán'][i] >= 7.0 or self.data_frame['Điểm_Văn'][i] >= 7.0):
                    xep_loai.append('Giỏi')
                elif self.data_frame['Tổng_điểm'][i] >= 14 and (self.data_frame['Điểm_Toán'][i] >= 6.0 or self.data_frame['Điểm_Văn'][i] >= 6.0):
                    xep_loai.append('Khá')
                elif self.data_frame['Tổng_điểm'][i] >= 10.0 and (self.data_frame['Điểm_Toán'][i] >= 4.0 or self.data_frame['Điểm_Văn'][i] >= 4.0):
                    xep_loai.append('Trung Bình')
                else:
                    xep_loai.append('Yếu')
            self.data_frame['Xếp_Loại'] = xep_loai

            #Hiển thị dữ liệu và table frame
            if len(self.data_frame) != 0:
                # print(self.data_frame.head())
                self.data_frame = self.data_frame.sort_values(by=['Trường', 'Họ_và_Tên'], ascending=(True, True))
                
                self.Table.delete(*self.Table.get_children())
                for row in range(len(self.data_frame)):
                    values = [i for i in self.data_frame.iloc[row].values]
                    self.Table.insert('', END, values=values)
            # print(len(data_frame))


        #Hiển thị dữ liệu vào Table Frame bằng cách lấy dữ liệu tử database
        elif self.search_combo.get() == "Show database":

            #Kết nối database
            mydb_stu = mysql.connector.connect(
                host="localhost",
                user = "root",
                passwd = "", 
                database='students')

            # print(mydb_stu)
            #Lấy tất cả các dữ liệu từ database
            mycurror = mydb_stu.cursor()
            mycurror.execute("SELECT * from stu_table ORDER BY Trường")
            rows = mycurror.fetchall()

            #Tạo dữ liệu được lưu bằng file csv(excel) để hiển thị
            data_arr = []
            for i in range(len(rows)):
                data_arr.append(rows[i])
            data_arr = np.array(data_arr)

            self.data_frame = pd.DataFrame(data_arr.reshape(len(rows), 10), columns=['SBD', 'Họ_và_Tên', 'Ngày_sinh', 'Giới_tính', 'Trường', 'Điểm_Toán', 'Điểm_Văn', 'Tổng_điểm', 'DTN', 'Xếp_Loại'])
            # print(self.data_frame)

            #Đưa dữ liệu lên bảng
            if(len(rows)!=0):
                self.Table.delete(*self.Table.get_children())
                for row in rows:
                    self.Table.insert('', END, values=row)

                mydb_stu.commit()
            mydb_stu.close()

        else:
            messagebox.showerror("Error", "Please chosse show all in Search")
            

    def get_fields(self, event):
        ''' Dùng để hiển thị các đặc điểm của sinh viên khi chọn 1 sinh viên bất kì'''
        cursor_row = self.Table.focus()
        content = self.Table.item(cursor_row)
        row = content['values']
        self.sbd.set(row[0])
        self.name.set(row[1])
        self.date.set(row[2])
        self.gender.set(row[3])
        self.score_toan.set(row[5])
        self.score_van.set(row[6])
        self.school.set(row[4])


    def delete(self):
        ''' Xóa sinh viên khỏi database bằng số báo danh (Bonus thêm không cần thiết)'''
        if self.sbd.get() != "" and self.data_frame is not None and self.search_combo.get() == "Delete database":
            sbd = self.sbd.get()
            self.txt_Roll.delete(0, END)
            # print(sbd)
            mydb_stu = mysql.connector.connect(
                    host="localhost",
                    user = "root",
                    passwd = "", 
                    database='students')

            # print(mydb_stu)
            mycurror = mydb_stu.cursor()
            sql = "DELETE FROM stu_table WHERE SBD = '{}'".format(sbd)
            mycurror.execute(sql)
            mydb_stu.commit()
            mydb_stu.close()

            messagebox.showinfo("Succes","Delete Successfully")
        else:
            messagebox.showerror("Error","Fields are Empty")

    def search_data(self):
        ''' Tìm các sinh viên theo yêu cầu'''
        # Tìm cái sinh viên cùng trường
        if self.search_combo.get() == "Student cùng trường" and self.data_frame is not None:
            #Lấy tất cả các tên trường trong dữ liệu
            name_school = self.data_frame['Trường'].values
            # print(name_school)
            #Kiểm tra xem đã nhập tên trường cần tìm hay chưa
            if self.txt_school.get() != "":
                #Lây tên trường
                school = self.txt_school.get()
                self.txt_school.delete(0, END)
                #Kiểm tra xem trường cần tìm có tồn tại hay không
                if school in name_school:
                    #Lấy tất cả các dữ liệu liên quan đến trường cần tìm
                    data = self.data_frame[self.data_frame['Trường'] == school]
                    # print(data)
                    if len(data) != 0:
                        #Sắp xếp các trường theo thứ tự tông điểm
                        data = data.sort_values(by=['Tổng_điểm'], ascending=False)
                        #Tính xem có bào nhiêu học sinh giỏi, khá, trung bình, kém
                        count = data['Xếp_Loại'].value_counts()
                        #Tạo dữ liệu để hiển thị vào bản
                        data_count = np.array(['', 'Giỏi: {}'.format(count['Giỏi']), 'Khá: {}'.format(count['Khá']), 'Trung Bình: {}'.format(count['Trung Bình']), 'Yếu: {}'.format(count['Yếu']), '', '', '', '', '']).reshape(1, 10)
                        frame_count = pd.DataFrame(data_count, columns=self.data_frame.columns)
                        # print(frame_count)
                        data = pd.concat([data, frame_count])
                        self.Table.delete(*self.Table.get_children())
                        for row in range(len(data)):
                            values = [i for i in data.iloc[row].values]
                            self.Table.insert('', END, values=values)
                else:
                    messagebox.showerror("Error","Name school not exist")
        
        #Tương tự tìm theo trường
        elif self.search_combo.get() == "Điển Toán lớn hơn Văn" and self.data_frame is not None:
            # print(self.data_frame)
            data = self.data_frame[self.data_frame['Điểm_Toán'] > self.data_frame['Điểm_Văn']]
            # print(data)
            if len(data) != 0:
                self.Table.delete(*self.Table.get_children())
                for row in range(len(data)):
                    values = [i for i in data.iloc[row].values]
                    self.Table.insert('', END, values=values)

        #Tương tự tìm theo trường
        elif self.search_combo.get() == "Học sinh kém" and self.data_frame is not None:
            # print(self.data_frame)
            data = self.data_frame[self.data_frame['Xếp_Loại'] == "Yếu"]
            data = data.sort_values(by=['Trường', 'Tổng_điểm'], ascending=(True, False))
            # print(data)
            
            if len(data) != 0:
                self.Table.delete(*self.Table.get_children())
                for row in range(len(data)):
                    values = [i for i in data.iloc[row].values]
                    self.Table.insert('', END, values=values)

        #Tương tự tìm theo trường
        elif self.search_combo.get() == "Thủ Khoa" and self.data_frame is not None:
            school = self.data_frame['Trường'].values
            index = []

            for i in set(school):
                frame_school = self.data_frame[self.data_frame['Trường'] == str(i)]
                frame_school['Tổng_điểm'] = frame_school['Tổng_điểm'].astype('float32')
                diem_thu_khoa = frame_school['Tổng_điểm'].max()
                index_thu_khoa = frame_school.loc[frame_school['Tổng_điểm'] == diem_thu_khoa].index
                for j in index_thu_khoa.values:
                    index.append(int(j))
            # print(index)
        
            data = self.data_frame.loc[index]
            # print(data)
            if len(data) != 0:
                data = data.sort_values(by=['Tổng_điểm'], ascending=False)
                self.Table.delete(*self.Table.get_children())
                for row in range(len(data)):
                    values = [i for i in data.iloc[row].values]
                    self.Table.insert('', END, values=values)
            
        else:   
            messagebox.showerror("Error","Data is Empty")

    #Hàm thêm để hiển thị ngày sinh cho đẹp (không cần thiết)
    def put_placeholder(self):
        self.txt_date.insert(0,"DD-MM-YYYY")
        self.txt_date['fg'] = "grey"
    #Hàm thêm để ô ngày sinh hiển thị đẹp (không cần thiết)
    def foc_in(self, event):
        if self.txt_date['fg'] == "grey":
            self.txt_date.delete('0', 'end')
            self['fg'] = "grey"
    #Hàm thêm để ô ngày sinh hiển thị đẹp (không cần thiết)
    def foc_out(self, event):
        if not self.get():
            self.txt_date.put_placeholder()

    #Hàm thoát giao diện
    def logout(self):
        return self.root.destroy()
        
    #Hàm mở Open_File
    def open_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Open_File(st_root)
        st_root.mainloop()

    #Hàm mở Student
    def student_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Student(st_root)
        st_root.mainloop()
    
    #Hàm mở Certificate
    def certificate_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Certificate(st_root)
        st_root.mainloop()

class Certificate:
    def __init__(self,root):
        #Thiết lập giao diện
        self.root = root
        self.root.title("Secrets Student Management System") #Title
        self.root.geometry("1350x700+0+0") #Kích thước
        
        #Các thuộc tính của title
        title = Label(self.root, text="Secrets Student Management System",bd = 10, relief=GROOVE, font=("Arial",43,"bold"), bg="#00A1E4",fg="#FFFCF9")
        title.pack(side=TOP,fill=X)

        #Variables (các biến cần thiết)
        self.dept_id = StringVar()
        self.dept_name = StringVar()
        self.search_combo = StringVar()
    
        #DashBoard Frame (chứa các thuộc tính mình cần (Open_File, Exit, Student))
        Dash_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="#F0EDEE")
        Dash_Frame.place(x=2,y=95,width=98,height=600)

        open_btn = Button(Dash_Frame,text="Open File",bg="#00A1E4",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.open_btn).grid(row=0,column=0,padx=2,pady=2,sticky="w")   

        manage_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Student",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.student_btn).grid(row=1,column=0,padx=2,pady=0,sticky="w")

        certificate_student_btn = Button(Dash_Frame,bg="#00A1E4",text="Certificate",fg="#F0EDEE", 
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.certificate_btn).grid(row=2,column=0,padx=2,pady=0,sticky="w")

        exit_btn = Button(Dash_Frame,text="Exit",bg="#00A1E4",fg="#F0EDEE",
        font=("Arial",9,"bold"),relief=GROOVE,width=11,pady=20,command=self.logout).grid(row=3,column=0,padx=2,pady=2,sticky="w")   

        Search_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="#F0EDEE")
        Search_Frame.place(x=680,y=600,width=97,height=35)
        certificate_btn = Button(Search_Frame, text="Search", width=10,bg="#00A1E4",fg="#FFFCF9",font=("Arial",10,"bold"),command=self.search_student).grid(row=0,column=0,padx=0,pady=0)

        # Bảng chứa các thông tin sau search
        #Text chứa bằng cấp
        Table_Frame_1 = Frame(self.root,bg="#0A090C")
        Table_Frame_1.place(x=195,y=200,width=320,height=300)
        self.txt_1 = Text(Table_Frame_1, width=310, height=290, bd=4, font=("Arial", 12, "bold"))
        self.txt_1.pack(pady=2)

        #Text chứa bằng cấp
        Table_Frame_2 = Frame(self.root,bg="#0A090C")
        Table_Frame_2.place(x=570,y=200,width=320,height=300)
        self.txt_2 = Text(Table_Frame_2, width=310, height=290, bd=4, font=("Arial", 12, "bold"))
        self.txt_2.pack(pady=2)
        
        #Text chứa bằng cấp
        Table_Frame_3 = Frame(self.root,bg="#0A090C")
        Table_Frame_3.place(x=940,y=200,width=320,height=300)
        self.txt_3 = Text(Table_Frame_3, width=310, height=290, bd=4, font=("Arial", 12, "bold"))
        self.txt_3.pack(pady=2)

    def search_student(self):
        #Kiểm tra xem có text 1,2,3 chứa dữ liệu hay chưa nếu chứa thì xóa
        self.txt_1.delete("1.0","end")
        self.txt_2.delete("1.0","end")
        self.txt_3.delete("1.0","end")

        #Kết nối database
        mydb_stu = mysql.connector.connect(
            host="localhost",
            user = "root",
            passwd = "", 
            database='students')

        # print(mydb_stu)
        #Lấy tất cả các dữ liệu từ database
        mycurror = mydb_stu.cursor()
        mycurror.execute("SELECT * from stu_table ORDER BY Trường")
        rows = mycurror.fetchall()

        #Tạo dữ liệu được lưu bằng file csv(excel) để hiển thị
        data_arr = []
        for i in range(len(rows)):
            data_arr.append(rows[i])
        data_arr = np.array(data_arr)

        self.data_frame = pd.DataFrame(data_arr.reshape(len(rows), 10), columns=['SBD', 'Họ_và_Tên', 'Ngày_sinh', 'Giới_tính', 'Trường', 'Điểm_Toán', 'Điểm_Văn', 'Tổng_điểm', 'DTN', 'Xếp_Loại'])
        # print(self.data_frame)

        #Random 3 bằng số bất kì để lấy bằng cấp
        index = np.random.randint(len(self.data_frame), size=(3,))
        # print(index)
        #Lấy tên các cột
        column = self.data_frame.columns.values
        # print(column)

        #List chứa bằng cấp
        certificate = []
        
        #Tạo bằng cấp
        for i in index:
            data = ''
            for j in range(len(self.data_frame.loc[int(i)].values)):
                if data == '':
                    data += 'GIAY BAO DIEM'
                else:
                    data += '\n' + str(column[j]) + ':' + '\t' + str(self.data_frame.loc[int(i)].values[j])
            certificate.append(data)

        #Ghi bằng cấp vào các text 1,2,3
        self.txt_1.insert(INSERT, certificate[0])
        self.txt_2.insert(INSERT, certificate[1])
        self.txt_3.insert(INSERT, certificate[2])

        mydb_stu.commit()
        mydb_stu.close()

    #Hàm thoát giao diện
    def logout(self):
        return self.root.destroy()
        
    #Hàm mở Open_File
    def open_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Open_File(st_root)
        st_root.mainloop()

    #Hàm mở Student
    def student_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Student(st_root)
        st_root.mainloop()
    
    #Hàm mở Certificate
    def certificate_btn(self):
        self.root.destroy() 
        st_root = Tk()
        st = Certificate(st_root)
        st_root.mainloop()
    
root = Tk()
st = Open_File(root)
root.mainloop()

