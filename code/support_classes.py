import os
import pip
import cv2
import qrcode
import hashlib
import mysql.connector
from PIL import Image

class QR():
    
    # make qr code for the newly added participant
    def maker(self,convert):
        qr = qrcode.QRCode(version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_H,
                    box_size = 25, border = 4)
        
        qr.add_data(convert)
        qr.make(fit = True)

        image = qr.make_image(fill_color = "black", back_color = 'white')
        for_name = convert.split(',')
        name = for_name[0]+'-'+for_name[2]+'-'+for_name[3]
        image.save("Created QR-Codes\\" + name + ".png")

    # scanner to scan qr code for admin work
    def scanner(self,):
        print("Please wait while we open scanner to scan code.")

        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        a = None

        while True:
            
            _, img = cap.read()
            data, one, _ = detector.detectAndDecode(img)

            if data:
                a = data
                break

            cv2.imshow("Show your QR-Code to mark attendance.", img)

            if cv2.waitKey(1) == ord('q'):
                break


        try:
            cap.release(a)
        except Exception:
            cv2.destroyAllWindows()
        
        return a
        # print(a.split(','))

class database():

    def create(self):
        
        try:
            
            print('''We could not connect to the localhost.
This is because you are running this file for the first time on this device.
Please provide localhost user and password for that user.
we will re-create sample database for you on your localhost.\n''')
        
            user = input("Please enter user for localhost:")
            password = input("Please enter password for the user:")
            
            line = user+','+password
            with open("localhostdetails.txt",'w') as f:
                f.write(str(line))
                f.close()
            
            mydb=mysql.connector.connect(host='localhost',
                                    user= user,
                                    password= password)
            print("Creating sample database now, please wait....")
            
            queries = ['create database school;','use school;',
            '''create table teacher
            (name varchar(20) not null,
            division varchar(5) not null,
            section varchar(1) not null,
            salary int not null,
            phone_number varchar(13) not null unique,
            email varchar(200) not null unique);''',
                            
            '''insert into teacher values('Satish','12','A',45000,'9874563211','satish@school.com');''',

            '''create table student
            (name varchar(20) not null,
            division varchar(5) not null,
            section varchar(1) not null,
            roll_number int not null,
            phone_number varchar(13) not null unique,
            email varchar(200) not null unique);''',

            '''insert into student values('Shubham','12','A',1,'1123456789','shubham@student.com');''',

            '''create table classroom
            (room_number int not null unique,
            division varchar(5) not null,
            teacher varchar(20) not null,
            section varchar(1) not null);''',

            '''insert into classroom values(1,'12','Satish','A');''',
                            
            '''create table login
            (name varchar(20) not null,
            password varchar(300) not null,
            idn varchar(20) not null);''',
                            
            f"insert into login values('admin', '{hashlib.sha256("0000".encode()).hexdigest()}', 'admin');",
            f"insert into login values('Satish', '{hashlib.sha256("1234".encode()).hexdigest()}', 'sat123');",
            f"insert into login values('Shubham', '{hashlib.sha256("5678".encode()).hexdigest()}', 'shu456');",
                            
            '''create table attendance
            (name varchar(20) not null,
            idn varchar(10) not null,
            division varchar(5) not null,
            attended varchar(5) not null,
            date date not null);''',

            "insert into attendance values('Satish','sat123','12','Yes','2025-01-01');",
            "insert into attendance values('Shubham','shu456','12','Yes','2025-01-01');",

            """create table failed_login
            (idn varchar(15) not null,
            date date not null);""",

            '''create table result
            (name varchar(20) not null,
            division varchar(5) not null,
            section varchar(1) not null,
            roll_no int not null,
            Maths int not null,
            English int not null,
            Computer int not null,
            Physics int not null,
            Chemistry int not null,
            Total int not null,
            Grade varchar(3) not null,
            Name_Of_Test varchar(10) not null);'''
    ]

            mycursor=mydb.cursor()
            for query in queries:
                mycursor.execute(query)
                mydb.commit()
            
            os.system("clear")
            print("Sample database has been created successfully.")
            print("We are now closing program. Please start it again.\n")
            print("""If using windowsPlease make sure that the below path is added into your path folder of environment variables before restarting\
the application else we won't be able read the created the database.\n""")
            print("C:\Program Files\MySQL\MySQL Server 8.1\binC:\/Program Files\MySQL\MySQL Server 8.1\bin")
            exit()
        
        except Exception as e:
            # os.remove("C:\\Users\\hp\\OneDrive\\Desktop\\Python learning codes\\school management system\\Code\\localhostdetails.txt")
            print(f"\nError: {e}\n")
