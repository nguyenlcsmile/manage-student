import mysql.connector
import pandas as pd 
import numpy as np 

#Kết nối database
mydb = mysql.connector.connect( 
    host="localhost",
    user = "root",
    passwd = ""
) 
print(mydb)

#Tạo database students
mycurror = mydb.cursor()
mycurror.execute("CREATE DATABASE students")

#Kết nối vào database student
mydb_stu = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "", 
    database='students'
)
print(mydb_stu)

mycurror = mydb_stu.cursor()

#Ghi dữ liệu vào database
mycurror.execute("create table stu_table(SBD varchar(50), Họ_và_Tên varchar(50), Ngày_sinh varchar(50), Giới_tính varchar(50), Trường varchar(50), Điểm_Toán varchar(50), Điểm_Văn varchar(50), Tổng_điểm varchar(50), DTN varchar(50), Xếp_loại varchar(50))")
sql = 'insert into stu_table(SBD, Họ_và_Tên, Ngày_sinh, Giới_tính, Trường, Điểm_Toán, Điểm_Văn, Tổng_điểm, DTN, Xếp_loại) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

#Mở file dữ liệu đã được xử lí
data_arr = []
with open('data_processing.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()
    for i in data:
        a = np.array([i.split(',')]).reshape(1, 7)
        data_arr.append(a)

#Kiểm tra xem đã chọn "Show all" ... không sử dụng database để đưa dữ liệu lên
#Chọn file dữ liệu sau khi mình sử lí xong 
#Dữ liệu sau khi xử lí xong bào gồm SBD, TÊN, TRƯỜNG, GIỚI TÍNH, ĐIỂM TOÁN, ĐIỂM VĂN, NGÀY SINH thiếu TỔNG ĐIỂN, DTN, XẾP LOẠI
data_arr = np.array(data_arr)
data_frame = pd.DataFrame(data_arr.reshape(len(data), 7), columns=['SBD', 'Họ và Tên', 'Ngày sinh', 'Giới tính', 'Trường', 'Điểm Toán', 'Điểm Văn'])
data_frame['Điểm Toán'] = data_frame['Điểm Toán'].astype('float32')
data_frame['Điểm Văn'] = data_frame['Điểm Văn'].astype('float32')
total_score = data_frame['Điểm Toán'] + data_frame['Điểm Văn']
data_frame['Tổng điểm'] = total_score

#Tạo côt điểm thấp nhất
dnt = []
for i in range(len(data_frame)):
    if data_frame['Điểm Văn'][i] > data_frame['Điểm Toán'][i]:
            dnt.append(data_frame['Điểm Toán'][i])
    else:
            dnt.append(data_frame['Điểm Văn'][i])
data_frame['DTN'] = dnt

#Tạo cột xếp loại
xep_loai = []
for i in range(len(data_frame)):
    if data_frame['Tổng điểm'][i] >= 16.0 and (data_frame['Điểm Toán'][i] >= 7.0 or data_frame['Điểm Văn'][i] >= 7.0):
        xep_loai.append('Giỏi')
    elif data_frame['Tổng điểm'][i] >= 14 and (data_frame['Điểm Toán'][i] >= 6.0 or data_frame['Điểm Văn'][i] >= 6.0):
        xep_loai.append('Khá')
    elif data_frame['Tổng điểm'][i] >= 10.0 and (data_frame['Điểm Toán'][i] >= 4.0 or data_frame['Điểm Văn'][i] >= 4.0):
        xep_loai.append('Trung Bình')
    else:
        xep_loai.append('Yếu')
data_frame['Xếp Loại'] = xep_loai

#Đưa dữ liệu lên database
for i in range(len(data_frame)):
    val = []
    val.append([str(i) for i in data_frame.loc[i].values])
    print(val)
    mycurror.execute(sql, tuple(val[0]))
    mydb_stu.commit()

