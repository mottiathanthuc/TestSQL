import csv
import json
import requests
import random
import unicodedata
def get_gender(no_accent_name,api_key=""):
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/genderFullGeoBatch"

    payload = {
    "personalNames": [
        {
        "id": "3a2d203a-a6a4-42f9-acd1-1b5c56c7d39f",
        "name": no_accent_name,
        "countryIso2": "VN"
        }
    ]
    }
    headers = {
        "X-API-KEY": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json().get('personalNames',[])[0].get('likelyGender') 


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFD', input_str)
    no_accent_str = []
    for c in nfkd_form:
        if c == 'Đ':
            no_accent_str.append('D')
        elif c == 'đ':
            no_accent_str.append('d')
        elif not unicodedata.combining(c):
            no_accent_str.append(c)
    return ''.join(no_accent_str)



def get_random_district(district_list=['Ba Đình', 'Cầu Giấy', 'Hoàn Kiếm', 'Hai Bà Trưng', 'Hoàng Mai', 'Đống Đa', 'Tây Hồ', 'Thanh Xuân', 'Bắc Từ Liêm', "Hà Đông"]):
   
    values = [item for item in district_list]
    probabilities = [0.1 for _ in district_list]
    chosen_item = random.choices(values, probabilities)[0]
    return chosen_item


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 ==0)
    
def random_date(year):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year):
        days_in_month[2-1] = 29
        
    month = random.randint(1, 12)
    
    day = random.randint(1,days_in_month[month-1])
    
    return str(year) + '-' + f"{month:02d}" + "-" + f"{day:02d}"


def da_nghi_hoc(MSV):
    return 0

def password(MSV):
    return ''

def create_SQL(students):
    temp = [x[6] for x in students]
    lop = set(temp)
    SQL = "-- can them cac lop" + str(lop) + "\n" + "INSERT INTO [dbo].[SINHVIEN] ([MASV], [HO], [TEN], [PHAI], [DIACHI], [NGAYSINH], [MALOP], [DANGHIHOC], [PASSWORD]) VALUES \n"
    for student in students:
        temp = '('
        for att in student:
            if isinstance(att, str):
               temp = temp + "N'" + att +"', "
            else:
                temp = temp + str(att) +"', "
        temp = temp + "),\n"
        SQL = SQL + temp
    return SQL

def edit_txt(input_filename, output_filename, birth_year,comment_char = '#',remove_B_in_classid=True,using_api_for_genders = False,api_key = ''):
    with open(input_filename, newline='', encoding='utf-8-sig') as input_file, open(output_filename, 'w', encoding='utf-8') as output:        
        input = csv.reader(input_file)
        students=[]
        for row in input:
            if row[0][0] != comment_char or len(row>0):
                line_list = [x for x in row if x!='']
                student = [line_list[x] for x in range(1,5)]
                if using_api_for_genders:
                    no_accent_name = remove_accents(line_list[2])+' '+remove_accents(line_list[3])
                    student = student + [get_gender(no_accent_name)]
                else:
                    student = student + [0]
                student = student+[get_random_district()]+[random_date(birth_year)]+[da_nghi_hoc(MSV=student[0])] + [password(MSV=student[0])]\

                for x in range (3,6):
                    student[x],student[x+1] = student[x+1], student[x]

                if remove_B_in_classid:
                    student[6] = student[6][:-2]


                students.append(student)

        output.write(create_SQL(students)+"\n------------------END---------------------")
                
    return students

if __name__ == '__main__':
    print(edit_txt('D2021_CNTT.csv','DS_CNTT2021.sql',2003,remove_B_in_classid=True,using_api_for_genders=False,api_key=''))