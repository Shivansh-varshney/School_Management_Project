import os
import hashlib
import pwinput
import mysql.connector
from datetime import date

class database():

    def create(self):
        
        try:        
            user = pwinput.pwinput("Please enter user for localhost: ", mask='*')
            password = pwinput.pwinput("Please enter password for the user: ", mask='*')
            
            with open(".env",'w') as f:
                f.write(f"MYSQL_USER = '{user}'\n")
                f.write(f"MYSQL_PASSWORD = '{password}'")
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
            rollno int not null,
            phone varchar(13) not null unique,
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
            section varchar(5) not null,
            attended varchar(5) not null,
            date date not null);''',

            f"insert into attendance values('Satish', 'sat123', '12', 'A', 'Yes', '{date.today()}');",
            f"insert into attendance values('Shubham', 'shu456', '12', 'A', 'Yes', '{date.today()}');",

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
            print("""\nIf using windows, Please make sure that the below path is added into your path folder of environment variables before running 
the application else we won't be able read the created the database.\n""")
            print("C:\\Program Files\\MySQL\\MySQL Server 8.1\\binC:\\Program Files\\MySQL\\MySQL Server 8.1\\bin\n")
            exit()
        
        except Exception:
            return

if __name__ == "__main__":
    db = database()
    db.create()