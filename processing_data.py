import re 

#Vì dữ liệu này đặc thù theo form nên áp dụng code này khi file txt đúng form này

#Lấy dữ liệu file DanhSach.txt
with open('DanhSach.txt', 'r', encoding='utf-8') as file:
    diem = file.readlines()

#Sau khi đọc file dữ liệu thì dữ liệu có dấu xuống dòng '\n' gây khó khăn cho việc xử lí nên mình loại bỏ nó
data_danh_sach = []
for i in diem: 
    data_danh_sach.append(i.replace('\n', ''))

#Lấy các trường Ngày sinh, Tên, Trường, số báo danh
data_ds_total = []
for data in data_danh_sach:
    #Kiểm tra xem dữ liệu có dạng ngày sinh hay không (ví dụ dạng 22/06/1999)
    regexr_time = re.search(r'\b((?:\d\d[-/\.:])+\d\d(\d\d)?)[\s-]?((?:\d\d[\.:])+\d\d)?\b', data)
    #Lấy thời gian
    time = regexr_time.group(0), regexr_time.start(0), regexr_time.end(0)
    date = time[0].strip()
    #Lấy giới tính
    gender = ['Nam' if data[time[1]-2] == '0' else 'Nữ']
    #Lấy trướng
    school = data[time[2]:-1].strip()
    #Lấy họ và tên
    name = data[4:time[1]-3].strip()
    name = " ".join([i for i in name.split(" ") if i != ''])
    #Lấy số báo danh
    sbd = data[:4]
    data_ds_total.append([sbd, name, date, gender[0], school])

print(data_ds_total)

#=================================================
#=================================================

#Lấy điểm toán văn
with open('Diem.txt', 'r', encoding='utf-8') as file:
    diem = file.readlines()

data_diem = []
for i in diem:
    data_diem.append(i.replace('\n', ''))

data_diem_total = []
for data in data_diem:
    data_diem_total.append([i for i in data.split(" ") if i != ""])

print(data_diem_total)

#=================================================
#=================================================

#Lưu các dữ liệu Điểm và Danh Sách vào cùng 1 file
data_total = data_ds_total.copy()
for i in range(len(data_ds_total)):
    for j in range(len(data_diem_total)):
        if data_diem_total[j][0] in data_ds_total[i] and data_diem_total[j][1] == 'Toan':
            data_total[i].append(data_diem_total[j][2])

        elif data_diem_total[j][0] in data_ds_total[i] and data_diem_total[j][1] == 'Van':
            data_total[i].append(data_diem_total[j][2])
        else:
            continue

string = ""
for i in range(len(data_total)):
    if string == "":
        string += ','.join([i for i in data_total[i]])
    else:
        string += '\n' + ','.join([i for i in data_total[i]])

print(string)
with open("data_processing.txt", 'w', encoding='utf-8') as file:
    file.write(string)

