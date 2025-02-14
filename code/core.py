import os
import random
import hashlib
import pwinput
from datetime import date
from decouple import config
from datetime import timedelta
from qr_code import QR, qr_code_dir     # custom module
import mysql.connector as connector
from prettytable import PrettyTable

today = date.today()
qr = QR()

mydb= connector.connect(host='localhost',
                            user=config("MYSQL_USER"),
                            password=config("MYSQL_PASSWORD"),
                            database = 'school')

mycursor = mydb.cursor()

# base class with all the required functions
class base():

    def __init__(self, email): # id is ID-NUMBER
        self.id = ''
        self.email = email
    
    def add_to_table(self, context):
        
        try:
            if context['table'] == 'classroom':
                query=f"""
                insert into classroom (room_number, division, section, teacher) value ('{context['room_number']}','{context['division']}','{context['section']}','{context['teacher']}')
                """
                mycursor.execute(query)
                mydb.commit()
                print('Class added successfully.')
            else:
                query=f"""
                insert into user (name,division,section,phone,email) value('{context['name']}', '{context['division']}', '{context['section']}', '{context['phone']}', '{context['email']}');
                """
                mycursor.execute(query)
                mydb.commit()

                user_id = mycursor.lastrowid
                
                if context['table'] == 'teacher':
                    query=f"""
                    insert into teacher (salary, user_id) values('{context['salary']}', '{user_id}')
                    """
                else:
                    query=f"""
                    insert into student (rollno, parent_phone, parent_email, user_id) values('{context['rollno']}', '{context['parent_phone']}', '{context['parent_email']}', '{user_id}')
                    """
                mycursor.execute(query)
                mydb.commit()

                print(f'\n{context['table']} added successfully.')
                
                password = self.new_user_password()
                query=f"""
                insert into login (user_id, password) values('{user_id}','{hashlib.sha256(password.encode()).hexdigest()}');
                """
                mycursor.execute(query)
                mydb.commit()
                dct = {'made on':str(today)}
                convert = context['name']+','+context['division']+','+context['section']+','+str(dct)
                qr.maker(convert)
                print("\n-------------------------------------------------------------------------")
                print(f"Please note login credentials for the newly added {context['table']}")
                print("Email                | Password")
                print(f"{context['email']}  | {password}")
                print("-------------------------------------------------------------------------")
            return True
        
        except Exception:
            return

    def attendance(self,accnt, div='', sec=''):
    
        if accnt=='student':
            query=f'select user.name, user.division, user.section, attendance.attended, attendance.date from user, attendance where user.id="{self.id}" and attendance.user_id="{self.id}"'
            mycursor.execute(query)
            t=PrettyTable(['Name', 'Divison', 'Section', 'Attended', 'Attendance Date'])
            data=mycursor.fetchall()
            for i in data:
                row = [i[0],i[1],i[2],i[3],i[4]]
                t.add_row(row)
            print(t)
            return True
        
        elif accnt=='teacher':
            ch = int(input('''
            What you want to do in Attendance list:
            Enter 1 to display attendance of whole class for a particular date.
            Enter 2 to display attendance of a particular student.
            Enter 3 to display attendance of a particular student for a particular date.
            Enter 4 to display full attendance of whole class.
            Enter 5 to exit: '''))
        
        if ch==1:
            try:
                dte=input('Enter date(YYYY-MM-DD): ')
                query=f"""
                select user.name, user.division, user.section, student.rollno, attendance.attended, attendance.date 
                from user
                join student on student.user_id = user.id
                join attendance on attendance.user_id = user.id
                where user.division='{div}' and user.section='{sec}' and attendance.date='{dte}';
                """
                mycursor.execute(query)
                data=mycursor.fetchall()
                t=PrettyTable(['Name of Student','Divison','Section', 'Roll Number', 'Attended','Attendance Date'])

                for i in data:
                    t.add_row(i)

                print(t)
                return self.attendance(accnt,div,sec)
            except Exception:
                return
        
        elif ch==2:
            try:
                rlln=input('Enter student roll number: ')
                query=f"select user.name, user.division, user.section, student.rollno, attendance.attended, attendance.date from user, attendance, student where user.id=student.user_id and attendance.user_id=student.user_id and student.rollno='{rlln};'"
                mycursor.execute(query)
                t=PrettyTable(['Name', 'Divison', 'Section', 'Roll Number', 'Attended', 'Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
                    t.add_row(row)
                print(t)
                return self.attendance(accnt,div,sec)
            except Exception :
                return

        elif ch==3:
            try:
                dte= input('Enter date: ')
                rlln=input('Enter roll number of student: ')
                query=f"""
                select user.name, user.division, user.section, student.rollno, attendance.attended, attendance.date
                from user
                join student on user.id=student.user_id
                join attendance on user.id=attendance.user_id
                where student.rollno='{rlln}' and attendance.date='{dte}';
                """
                mycursor.execute(query)
                t=PrettyTable(['Name of Student', 'Divison','Section','Roll Number','Attended','Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.attendance(accnt,div,sec)
            except Exception:
                return
        
        elif ch==4:
            try:
                query=query=f"""
                select user.name, user.division, user.section, student.rollno, attendance.attended, attendance.date 
                from user
                join student on student.user_id = user.id
                join attendance on attendance.user_id = user.id
                where user.division='{div}' and user.section='{sec}';
                """
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Divison','Section','Roll Number','Attended','Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
    
                print(t)
                return self.attendance(accnt,div,sec)
            except Exception :
                return

        elif ch==5:
            return True
        
        else:
            print("Wrong choice entered. Please try again...")
            return self.attendance(accnt,div,sec)
        
    def check(self):
        try:

            query = f"select id from user where email='{self.email}';"
            mycursor.execute(query)
            self.id = mycursor.fetchone()[0]

            if not self.id:
                print("No user with given email.")
                return False

            yesterday = today-timedelta(days=1)
            query = f"select * from failed_login where user_id = '{self.id}' and date = '{today}' or '{yesterday}';" #, today, yesterday)
            mycursor.execute(query)
            row=mycursor.fetchone()

            if row is None :
                go_ahead = self.login()
                return go_ahead
            else:
                return False
        except Exception:
            print("The user could not be checked for past failed logins due to: ", e)

    def display(self,accnt,div='',sec=''):
        try:
            if accnt=='student':
                query=f'select user.name, user.division, user.section, student.rollno, user.phone, user.email, student.parent_phone, student.parent_email from user,student where user.id="{self.id}" and student.user_id="{self.id}"'
                t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email', 'Parent Phone', 'Parent Email'])
            elif accnt=='teacher':
                query=f"""
                select user.name, user.division, user.section, student.rollno, user.phone, user.email, student.parent_phone, student.parent_email
                from user
                join student on student.user_id = user.id
                where user.division='{div}' and user.section='{sec}';
                """
                t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email', 'Parent Phone', 'Parent Email'])
            elif accnt=='admin':
                ch = int(input('''
        What do you want to see?
        Enter 1 to see all Teachers.
        Enter 2 to see all clasrooms.
        Enter 3 to see a particular student.
        Enter 4 to see all students of a particular division and section.
        Enter 5 to exit: '''))
                if ch==1:
                    query=f"""
                    select user.name, user.division, user.section, user.phone, user.email, teacher.salary
                    from user
                    join teacher on teacher.user_id = user.id
                    """
                    t=PrettyTable(['Name', 'Division','Section', 'Phone Number', 'Email', 'Salary'])
                elif ch==2:
                        query=f"""
                        select classroom.room_number, classroom.teacher, classroom.division, classroom.section from classroom;
                        """
                        t=PrettyTable(['Room Number','Teacher','Division','Section'])
                elif ch==3:
                    email=input('Enter email of student:')
                    query=f"""
                    select user.name, user.division, user.section, student.rollno, user.phone, user.email, student.parent_phone, student.parent_email
                    from user
                    join student on student.user_id = user.id
                    where user.email='{email}';
                    """
                    t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email', 'Parent Phone', 'Parent Email'])
                elif ch==4:
                    div=input('Enter Division: ')
                    sec=input('Enter section: ')
                    query=f"""
                    select user.name, user.division, user.section, student.rollno, user.phone, user.email, student.parent_phone, student.parent_email
                    from user
                    join student on student.user_id = user.id
                    where user.division='{div}' and user.section='{sec}';
                    """
                    t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email', 'Parent Phone', 'Parent Email'])
                elif ch==5:
                    return True
                else:
                    print("Wrong choice entered. Please try again...")
                    return self.display(accnt,div,sec)
 
            mycursor.execute(query)
            record=mycursor.fetchall()
            for i in record:
                t.add_row(i)
            print(t)

            if accnt == 'admin':
                return self.display(accnt,div,sec)
            
            return True
        
        except Exception:
            return

    def login(self, n=1):
        while True:
            
            if n<=5 :
                query=f'select password from login where user_id="{self.id}"'
                mycursor.execute(query)
                ps=mycursor.fetchone()
                pswd=ps[0]
                password= pwinput.pwinput('\nEnter Password: ', mask="*")
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if pswd==hashed_password:
                        return True
                
                elif pswd!=password:
                    print('Wrong password entered. Please try again')
                    n = n+1
                    return self.login(n) 
            
            elif n>5:
                print("You have entered wrong password 5 times.")
                query = "insert into failed_login values('{}','{}')".format(id, today)
                mycursor.execute(query)
                mydb.commit()
                return False
            
            else:
                return -1

    def mark_attendance(self):
        verify = self.login()
        if verify == True:
            
            flag = True
            while flag == True:
                
                value = qr.scanner()
                if value == None:
                    
                    verify = self.login()
                    if verify == True:
                        
                        print("\nMarking for the absenties...")
                        
                        query = f"select id from user;"
                        mycursor.execute(query)
                        details_list = mycursor.fetchall() # list of tuples having user_ids in the format [('user_id',),('user_id',),...]
                        query = f"select user_id from attendance where attended='Yes' and date='{today}';"
                        mycursor.execute(query)
                        attendies = [id[0] for id in mycursor.fetchall()]
                        
                        for details in details_list:
                            user_id = details[0]
                            if user_id not in attendies:
                                query = f"insert into attendance(user_id, attended, date) values('{user_id}','No', '{today}');"
                                mycursor.execute(query)
                                mydb.commit()

                        print("\nAll the absenties have been marked.")
                        return True
                    
                    else:
                        query = "insert into failed_login values('{}','{}')".format(self.id, today)
                        mycursor.execute(query)
                        mydb.commit()
                        return False
                    
                else:
                    values = value.split(',')
                    query=f"""
                    select id from user where name='{values[0]}' and division='{values[1]}' and section='{values[2]}';
                    """
                    mycursor.execute(query)
                    user_id = mycursor.fetchone()[0]
                    query = f"insert into attendance (user_id, attended, date) values('{user_id}','Yes','{today}');"
                    mycursor.execute(query)
                    mydb.commit()
                    print("\nAttendance marked for",values[0])
                    
        return False
    
    def new_user_password(self):
        dict_of_items = {"symbols" : '!@#$%^&+-*/=()}]{[:";<>.,~',
        "small alphabets" : 'abcdefghijklmnopqrstuvwxyz',
        "capital alphabets" : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        "numbers" : '0123456789'}

        password = ''
        for i in range(8):
            key = random.choice(["symbols", "small alphabets", "capital alphabets", "numbers"])
            item = dict_of_items[key]
            password = password + item[random.randint(0,len(item)-1)]
            
        return password

    def rem_from_table(self, context):
        try:
            
            if context['table'] != 'classroom':
                
                try:
                    # to form the name of qr-code file so that can be deleted
                    query = f"select name,division,section,phone,email from user where email='{context['email']}'"
                    mycursor.execute(query)
                    record = mycursor.fetchall()

                    t=PrettyTable(['Name','Division','Section','Phone Number','Email'])

                    for i in record:
                        t.add_row(i)
                    print(t)
                    
                    ch = input(f"You want to delete above {context['table']}? (y/n): ")
                    if ch.lower() != 'y':
                        print('No record deleted.')
                        return True

                    # delete qr-code from the database
                    mycursor.execute(query)
                    record = mycursor.fetchone()
                    file_name = record[0]+'-'+record[1]+'-'+record[2]+'.png'
                    os.remove(os.path.join(qr_code_dir, file_name))

                    query = f"""
                    delete from user where email='{context['email']}';
                    """
                                                        
                except Exception:
                    print(f"Error occured while trying to remove {context['table']} & Error is:{e}")
                
            else:
                query=f"""
                delete from classroom where room_number='{context['room_number']}';
                """
            
            mycursor.execute(query)
            mydb.commit()
            print(f'{context['table']} removed successfully.')
            return True
        
        except Exception:
            return
    
    def result(self,accnt, div='', sec=''): 

        if accnt=='student':
            query=f"""
            select user.name, user.division, user.section, student.rollno,
            result.Maths, result.English, result.Computer, result.Physics, result.Chemistry, result.Total, result.Grade, result.Name_Of_Test
            from user, student, result where user.id='{self.id}' and student.user_id='{self.id}' and result.user_id='{self.id}';
            """
            mycursor.execute(query)
            t= PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
            data=mycursor.fetchall()
            for i in data:
                t.add_row(i)
            print(t)
            return True
        
        elif accnt=='teacher':
            ch = int(input('''
            What you want to do with Result:
            Enter 1 to display result of whole class for a particular test.
            Enter 2 to display result of a particular student.
            Enter 3 to display result of a particular student for a particular test.
            Enter 4 to enter marks for new test.
            Enter 5 to exit: '''))
        
        if ch==1:
            try:
                tst=input('Enter Name of test: ')
                query=f"""
                select 
                user.name, user.division, user.section, student.rollno,
                result.Maths, result.English, result.Computer, result.Physics, result.Chemistry, result.Total, result.Grade, result.Name_Of_Test
                from user
                join student on student.user_id = user.id
                join result on result.user_id = user.id
                where Name_of_test='{tst}'
                """
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.result(accnt)
            except Exception:
                return
            
        elif ch==2:
            try:
                rlln=int(input('Enter Roll Number of student: '))  
                
                query=f"""
                select user.name, user.division, user.section, student.rollno,
                result.Maths, result.English, result.Computer, result.Physics, result.Chemistry, result.Total, result.Grade, result.Name_Of_Test
                from user, student, result where user.id=student.user_id and user.id=result.user_id and student.rollno='{rlln}';
                """
                
                mycursor.execute(query)
                t= PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.result(accnt)
            except Exception:
                return

        elif ch==3:
            try:
                tst=input('Enter Name of Test: ')
                rlln=int(input('Enter roll number of student: '))
                query=f"""
                select 
                user.name, user.division, user.section, student.rollno,
                result.Maths, result.English, result.Computer, result.Physics, result.Chemistry, result.Total, result.Grade, result.Name_Of_Test
                from user
                join student on student.user_id = user.id
                join result on result.user_id = user.id
                where student.rollno='{rlln}' and Name_of_test='{tst}'
                """
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.result(accnt)
            except Exception :
                return
        
        elif ch==4:
            try:
                name_of_test=input('Enter Name of test: ')
                query=f"""
                select user.id, user.name, student.rollno
                from user
                join student on student.user_id = user.id
                where user.division='{div}' and user.section='{sec}';
                """
                mycursor.execute(query)
                rec=mycursor.fetchall()
                for i in range(1,len(rec)+1):
                    user_id=rec[i-1][0]
                    nme=rec[i-1][1]
                    rlln=rec[i-1][2]
                    print(f"\nName: {nme}, Roll Number: {rlln}\n")
                    maths= int(input(f'Enter Number for Maths for roll number {i}: ')) #marks for maths
                    english=int(input(f'Enter Number for English for roll number {i}: ')) #marks for English
                    computer=int(input(f'Enter Number for Computer for roll number {i}: ')) #marks for computer
                    physics=int(input(f'Enter Number for Physics for roll number {i}: ')) #marks for physics
                    chemistry=int(input(f'Enter Number for Chemistry for roll number {i}: ')) #marks for chemistry
                    grades=input(f'Enter Grades for roll number {i}: ') #grades
                    total=maths+english+computer+physics+chemistry
                    query=f"insert into result (user_id, Maths, English, Computer, Physics, Chemistry, Total, Grade, Name_Of_Test) values('{user_id}','{maths}','{english}','{computer}','{physics}','{chemistry}','{total}','{grades}','{name_of_test}');"
                    mycursor.execute(query)
                    mydb.commit()
                print('Result for ',name_of_test,' is done.')
                return self.result(accnt)
            except Exception:
                return
        
        elif ch==5:
            return True
        
        else:
            print("Wrong choice entered. Please try again...")
            return self.result(accnt,sec)

    def update_in_table(self, context):

        try:
            change_context = {
                'salary': 'teacher',
                'rollno' : 'student', 
                'parent_phone' : 'student', 
                'parent_email' : 'student',
            }

            if context['column'] in change_context.keys():
                query = f"""
                select id from user where {context['identify_column']}='{context['identify_value']}';
                """
                mycursor.execute(query)
                user_id = mycursor.fetchone()[0]
                context['identify_column'] = 'user_id' # change the column
                context['identify_value'] = user_id # change the value
                
                context['table'] = change_context[context['column']] # change table to suitable table
            
            query = f"""
            update {context['table']} set {context['column']}='{context['value']}' where {context['identify_column']}='{context['identify_value']}';
            """
            mycursor.execute(query)
            mydb.commit()                

            print(f"\n{context['table']} updated successfully!!")

            return True

        except Exception:
            return
            

# class for administration works
class admin(base):

    def __init__(self, email):
        super().__init__(email)
        
    def start(self):
        
        verify = self.check()
        if verify == True:
            return self.ask()
        else:
            return verify 
            
    def ask(self):
        print('-'*90)
        accnt='admin'
        ch = int(input('''
        Welcome Admin,What would you like to do...
        To Add a teacher please enter 1.
        To update a teacher enter 2.
        To Remove a teacher enter 3.
        To Add a student please enter 4.
        To update a student enter 5.
        To Remove a student enter 6.
        To Add a Class enter 7.
        To update a Class enter 8.
        To Remove a Class enter 9.
        To start attendance for today enter 10.
        To see saved information enter 11.
        To exit enter 12: '''))
        
        if ch==1:
            nme=input('Enter name of teacher: ') #nme is for name
            div=input('Enter division of teacher: ')
            sec=input('Enter section of teacher: ')
            sal=int(input('Enter Salary: ')) #sal is for salary
            phn=input('Enter Phone Number of teacher: ')
            email=input('Enter Email of teacher: ')

            context = {
                'table': 'teacher',
                'name': nme,
                'division': div,
                'section': sec,
                'phone': phn,
                'email': email,
                'salary': sal
            }
            
            rv=self.add_to_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()

        elif ch==2:
            email=input('Enter email of teacher: ')
            print("Name | Division | Section | Phone | Email | Salary")
            column = input("What would you like to change: ").lower()
            value = input(f"Enter value for {column}: ")

            context = {
                'table': 'user',
                'identify_column': 'email',
                'identify_value': email,
                'column': column,
                'value': value
            }

            rv=self.update_in_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()

        elif ch==3:
            email=input('Enter email of teacher: ')

            context = {
                'table': 'teacher',
                'email': email
            }
            rv=self.rem_from_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()

        elif ch==4:
            
            name=input('Enter name of Student: ') #nme is for name
            div=input('Enter division of Student: ') #nme is for name
            sec=input('Enter section of Student: ') #nme is for name
            rlln=input('Enter Roll Number: ') #rlln is for roll number 
            phone=input('Enter Phone Number: ') #PNo is for Phone Number
            email=input('Enter Email of student: ')
            parent_phone=input('Enter Parent Phone Number: ') #PNo is for Phone Number
            parent_email=input('Enter Parent Email of student: ')

            context = {
                'table': 'student',
                'name': name,
                'division': div,
                'section': sec,
                'rollno': rlln,
                'phone': phone,
                'email': email,
                'parent_phone': parent_phone,
                'parent_email': parent_email,
            }
            
            rv=self.add_to_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()

        elif ch==5:
            email=input('Enter email of student: ')
            print("| Name | Division | Section | Roll Number | Phone | Email | Parent Phone | Parent Email |")
            column = input("What would you like to change: ").lower()
            value = input(f"Enter value for {column}: ")

            context = {
                'table': 'user',
                'identify_column': 'email',
                'identify_value': email,
                'column': column,
                'value': value
            }

            rv=self.update_in_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()

        elif ch==6:
            email = input("Enter email of student: ")
            context = {
                'table': 'student',
                'email': email
            }
            rv=self.rem_from_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==7:
            rno=int(input('Enter room number: '))
            div=input('Enter division: ')
            sec = input('Enter section: ')
            teacher=input('Enter teacher name: ')

            context = {
                'table': 'classroom',
                'room_number': rno,
                'division': div,
                'section': sec,
                'teacher': teacher
            }
            
            rv=self.add_to_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==8:
            room_number = int(input("Enter Room number you want to change: "))
            print("Room Number | Division | Section | Teacher")
            column = input("What would you like to change: ").lower()
            value = input(f"Enter value for {column}: ")

            context = {
                'table': 'classroom',
                'identify_column': 'room_number',
                'identify_value': room_number,
                'column': column,
                'value': value
            }

            rv=self.update_in_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==9:
            room=input('Enter Room number: ')
            context = {
                'table': 'classroom',
                'room_number': room
            }
            rv=self.rem_from_table(context)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==10:
            rv = self.mark_attendance()
            if rv == True:
                return self.ask()
            else:
                return rv

        elif ch==11:
            rv=self.display(accnt)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()
                    
        elif ch==12:
            os.system("clear")
            exit()
        
        else:
            print('Wrong choice entered:')
            return self.ask()

# class for teacher accounts
class teacher(base):
    
    def __init__(self, email):
        super().__init__(email)
        
    def start(self):
        
        verify = self.check('1234')
        if verify == True:
            return self.ask()
        else:
            return verify
    
    def ask(self):
        
        accnt='teacher'
        print('-'*90)
        query=f'select division,section from user where id="{self.id}"'
        mycursor.execute(query)
        record=mycursor.fetchone()
        div=record[0]
        sec=record[1]
        print('Your class is',div,'-',sec,'What would you Like to do..')
        ch = int(input('''
        For Attendance related work enter 1.
        For Result related work enter 2.
        To display all the students of class enter 3.
        To exit enter 4: '''))
        print('-'*90)
        
        if ch==1:
            rv=self.attendance(accnt, div, sec)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()
                
        elif ch==2:
            rv=self.result(accnt, div, sec)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==3:
            
            rv=self.display(accnt,div,sec)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...', )
                print('Please Try Again')
                return self.ask()
                
        elif ch==4:
            os.system("clear")
            exit()

        else:
            print('Wrong choice entered:')
            return self.ask()

# class for student accounts
class student(base):
    
    def __init__(self, email):
        super().__init__(email)
    
    def start(self):
        
        verify = self.check()
        if verify == True:
            return self.ask()
        else:
            return verify
    
    def ask(self):
        accnt='student'
        print('-'*90)
        print('''
        What you want to do...
        Enter 1 to see your result.
        Enter 2 to see your Attendance.
        Enter 3 to see your information.
        Enter 4 to exit.
        ''')
        
        ch=int(input(':'))
        if ch==1:
            
            rv=self.result(accnt)
            if rv==True:
                return self.ask()
            
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==2:
            rv=self.attendance(accnt)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==3:
            rv=self.display(accnt)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==4:
            os.system("clear")
            exit()
        
        else:
            print("Wrong choice entered. Please try again...")
            return self.ask()
