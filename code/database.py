import os
import hashlib
import pwinput
import mysql.connector
from datetime import date
from colorama import Fore, Style
from rich.progress import Progress

class database():

    def create(self):
        
        try:        
            user = input("Please enter user for localhost: ")
            password = pwinput.pwinput("Please enter password for the user: ", mask='*')
            
            with open(".env",'w') as f:
                f.write(f"MYSQL_USER = '{user}'\n")
                f.write(f"MYSQL_PASSWORD = '{password}'")
                f.close()
            
            mydb=mysql.connector.connect(host='localhost',
                                    user= user,
                                    password= password)

            queries = [
            '''
            create database school;
            ''',
            
            '''
            use school;
            ''',

            '''
            create table user(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name varchar(50) not null,
            division varchar(4) null,
            section varchar(2) null,
            phone varchar(10) not null unique,
            email varchar(100) not null unique);
            ''',

            '''
            create table student(
            id INT AUTO_INCREMENT PRIMARY KEY,
            rollno int not null,
            parent_phone varchar(10) not null,
            parent_email varchar(100) not null,
            user_id int not null unique,
            foreign key (user_id) references user(id) on delete cascade);
            ''',

            '''
            create table teacher(
            id INT AUTO_INCREMENT PRIMARY KEY,
            salary int not null,
            user_id int not null unique,
            foreign key (user_id) references user(id) on delete cascade);
            ''',

            '''
            create table subject(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE);
            ''',
            
            '''
            CREATE TABLE teacher_subject (
            id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_id INT NOT NULL,
            subject_id INT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE,
            UNIQUE (teacher_id, subject_id));
            ''',

            '''
            CREATE TABLE classroom (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_number INT NOT NULL UNIQUE,
            division VARCHAR(5) not NULL,
            section VARCHAR(1) not NULL,
            teacher varchar(50) not null
            );
            ''',

            '''
            CREATE TABLE login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id int not null,
            password VARCHAR(300) NOT NULL,
            FOREIGN KEY (user_id) references user(id) ON DELETE CASCADE);
            ''',

            '''
            CREATE TABLE attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            attended varchar(4) NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (user_id) references user(id) ON DELETE CASCADE);
            ''',

            '''
            CREATE TABLE failed_login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (user_id) references user(id) ON DELETE CASCADE);
            ''',

            '''
            CREATE TABLE result (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            Maths INT NOT NULL,
            English INT NOT NULL,
            Computer INT NOT NULL,
            Physics INT NOT NULL,
            Chemistry INT NOT NULL,
            Total INT NOT NULL,
            Grade VARCHAR(3) NOT NULL,
            Name_Of_Test VARCHAR(10) NOT NULL,
            FOREIGN KEY (user_id) references user(id) ON DELETE CASCADE);
            ''',

            # admin user
            "INSERT INTO user (name, phone, email) VALUES ('shivansh', '7302232878', 'shivansh.admin@school.com');",

            "SET @admin_id = LAST_INSERT_ID();",

            f"INSERT INTO login (user_id, password) VALUES (@admin_id, '{hashlib.sha256("0000".encode()).hexdigest()}');",

            # teacher user
            "INSERT INTO user (name, division, section, phone, email) VALUES ('Satish', '12', 'A', '9874563211', 'satish.teacher@school.com');",

            "SET @teacher_id = LAST_INSERT_ID();",

            "INSERT INTO teacher (user_id, salary) VALUES (@teacher_id, 45000);",

            # login credentials for teacher
            f"INSERT INTO login (user_id, password) VALUES (@teacher_id, '{hashlib.sha256("1234".encode()).hexdigest()}');",

            # classroom for the teacher
            "INSERT INTO classroom (teacher, room_number, division, section) VALUES ('Satish', 1, '12', 'A');",

            # attendance for teacher
            "INSERT INTO attendance (user_id, attended, date) VALUES (@teacher_id, 'Yes', CURDATE());",

            # subjects for teacher
            "INSERT INTO subject (name) VALUES ('Social Science'), ('English');",
            "INSERT INTO teacher_subject (teacher_id, subject_id) VALUES (1, 1), (1, 2);",

            # student user
            "INSERT INTO user (name, division, section, phone, email) VALUES ('Shubham', '12', 'A', '1123456789', 'shubham.student@school.com');",

            "SET @student_id = LAST_INSERT_ID();",

            "INSERT INTO student (user_id, rollno, parent_phone, parent_email) VALUES (@student_id, 1, '9876157245', 'parent.shubham@school.com');",

            # login credentials for student
            f"INSERT INTO login (user_id, password) VALUES (@student_id, '{hashlib.sha256("5678".encode()).hexdigest()}');",

            # attendance for student
            "INSERT INTO attendance (user_id, attended, date) VALUES (@student_id, 'Yes', CURDATE());",

            # result for student
            "INSERT INTO result (user_id, Maths, English, Computer, Physics, Chemistry, Total, Grade, Name_Of_Test) VALUES (@student_id, 85, 78, 92, 80, 76, (85+78+92+80+76), 'A', 'MidTerm');"
        ]
            os.system('cls' if os.name == 'nt' else 'clear')
            mycursor=mydb.cursor()
            with Progress() as progress:
                task = progress.add_task("[green]Creating database...", total=len(queries))
                
                for query in queries:
                    mycursor.execute(query)
                    mydb.commit()
                    progress.update(task, advance=1)
            
            print(Fore.GREEN + "\nSample database has been created successfully." + Style.RESET_ALL)
            print("""\nIf using windows, Please make sure that the below path is added into your path folder of environment variables before running 
        the application else we won't be able read the created the database.\n""")
            print(Fore.YELLOW+"C:\\Program Files\\MySQL\\MySQL Server 8.1\\binC:\\Program Files\\MySQL\\MySQL Server 8.1\\bin\n"+Style.RESET_ALL)
            exit()
        
        except Exception:
            print(Fore.RED+str(e)+Style.RESET_ALL)

if __name__ == "__main__":
    db = database()
    db.create()