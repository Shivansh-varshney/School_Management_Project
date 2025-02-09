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

    def __init__(self, idn, nme): # idn is ID-NUMBER
        self.idn = idn
        self.nme = nme
    
    def add_to_table(self, table, values):
        
        try:
            if table == 'classroom':
                query="insert into classroom values({},'{}','{}','{}')".format(values[0], values[1], values[2], values[3])
                mycursor.execute(query)
                mydb.commit()
                print('Class added successfully.')
            else:
                query="insert into {} values('{}','{}','{}',{},'{}','{}')".format(table, values[0], values[1], values[2], values[3], values[4], values[5])
                mycursor.execute(query)
                mydb.commit()
                print(f'\n{table} added successfully.')
                
                idn, password = self.new_credentials()
                query = "insert into login values('{}','{}','{}');".format(values[0], hashlib.sha256(password.encode()).hexdigest(), idn)
                mycursor.execute(query)
                mydb.commit()
                dct = {'made on':str(today)}
                convert = values[0]+','+idn+','+values[1]+','+values[2]+','+str(dct)
                qr.maker(convert)
                print("\n-------------------------------------------------------------------------")
                print(f"Please note the below credentials for the newly added {table}")
                print("ID-Num | Password")
                print(f"{idn}  | {password}")
                print("-------------------------------------------------------------------------")
            return True
        
        except Exception :
            return

    def attendance(self,accnt,div,sec):
    
        if accnt=='student':
            ch=2
        
        elif accnt=='teacher':
            print('''
        What you want to do in Attendance list:
        Enter 1 to display attendance of whole class for a particular date.
        Enter 2 to display attendance of a particular student.
        Enter 3 to display attendance of a particular student for a particular date.
        Enter 4 to display full attendance of whole class.
        Enter 5 to exit.''')
            ch= int(input(':'))
        
        if ch==1:
            try:
                dte=input('Enter date(YYYY-MM-DD): ')
                query='select attendance.name, attendance.idn, attendance.division, attendance.attended, attendance.section, \
                    attendance.date from attendance,student where student.name=attendance.name and attendance.division="{}" and attendance.section="{}" and date="{}"'.format(div,sec,dte)
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Id Number','Divison','Section','Attended','Attendance Date'])
                data=mycursor.fetchall()

                
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
                    t.add_row(row)
                print(t)
                return self.attendance(accnt,div,sec)
            except Exception :
                return
        
        elif ch==2:
            try:
                if accnt=='student':
                    rlln=self.idn
                elif accnt=='teacher':
                    rlln=input('Enter idn of student:')
                query='select * from attendance where idn="{}"'.format(rlln)
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Id Number','Divison','Section','Attended','Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
                    t.add_row(row)
                print(t)
                if accnt == 'student':
                    return True
                else:
                    return self.attendance(accnt,div,sec)
            except Exception :
                return

        elif ch==3:
            try:
                dte= input('Enter date:')
                idn=input('Enter idn of student:')
                query='select * from attendance where idn="{}" and date="{}"'.format(idn,dte)
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Id Number','Divison','Section','Attended','Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
                    t.add_row(row)
                print(t)
                return self.attendance(accnt,div,sec)
            except Exception :
                return
        
        elif ch==4:
            try:
                query='select attendance.name, attendance.idn, attendance.division, attendance.section, attendance.attended,\
                    attendance.date from attendance,student where student.name=attendance.name'
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Id Number','Divison','Section','Attended','Attendance Date'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
                    t.add_row(row)
    
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
            yesterday = today-timedelta(days=1)
            query = f"select * from failed_login where idn = '{self.idn}' and date = '{today}' or '{yesterday}';" #, today, yesterday)
            mycursor.execute(query)
            row=mycursor.fetchone()

            if row is None :
                go_ahead = self.login(self.idn,self.nme)
                return go_ahead
            else:
                return False
        except Exception :
            print("The user could not be checked for past failed logins due to:")

    def display(self,accnt,div,sec):
        try:
            if accnt=='student':
                query='select * from student where roll_number={} and section="{}"'.format(self.rlln,sec)
                t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email'])
            elif accnt=='teacher':
                query='select * from student where division="{}" and section="{}"'.format(div,sec)
                t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email'])
            elif accnt=='admin':
                print('''
        What do you want to see?
        Enter 1 to see all Teachers.
        Enter 2 to see all clasrooms.
        Enter 3 to see a particular student.
        Enter 4 to see all students of a particular division and section.
        Enter 5 to exit.''')
                ch=int(input(':'))
                if ch==1:
                    query='select * from teacher'
                    t=PrettyTable(['Name', 'Division','Section', 'Salary', 'Phone Number', 'Email'])
                elif ch==2:
                        query='select * from classroom'
                        t=PrettyTable(['Room Number','Division','Teacher','Section'])
                elif ch==3:
                    div=input('Enter Id-Number of student:')
                    query='select student.name,division,section,roll_number,phone,email from student,login where student.name=login.name and login.idn="{}"'.format(div)
                    t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email'])
                elif ch==4:
                    div=input('Enter Division:')
                    sec=input('Enter section:')
                    query='select * from student where division="{}" and section = "{}"'.format(div,sec.upper())
                    t=PrettyTable(['Name','Division','Section','Roll Number','Phone Number','Email'])
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
        
        except Exception :
            return

    def login(self, idn, nme, n=1):
        while True:
            
            if idn!='admin':
                if n<=5 :
                    query='select password,name from login where idn="{}"'.format(idn)
                    mycursor.execute(query)
                    ps=mycursor.fetchone()
                    pswd=ps[0]
                    nme1=ps[1]
                    password= pwinput.pwinput('\nEnter Password: ', mask="*")
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if pswd==hashed_password and nme1==nme:
                            return True
                    
                    elif pswd!=password and nme1==nme:
                        print('Wrong password entered. Please try again')
                        n = n+1
                        return self.login(idn,nme,n) 
                
                elif n>5:
                    print("You have entered wrong password 5 times.")
                    query = "insert into failed_login values('{}','{}')".format(idn, today)
                    mycursor.execute(query)
                    mydb.commit()
                    return False
                
                else:
                    return -1
                
            elif idn=='admin':
                password=pwinput.pwinput('\nEnter Password: ', mask="*")
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                query='select password,name from login where idn="{}"'.format(idn)
                mycursor.execute(query)
                ps=mycursor.fetchone()
                pswd=ps[0]
                nme1=ps[1]
                if pswd == hashed_password:
                    return True
                else:
                    query = "insert into failed_login values('{}','{}')".format(idn, today)
                    mycursor.execute(query)
                    mydb.commit()
                    return False

    def mark_attendance(self):
        verify = self.login(self.idn, self.nme)
        if verify == True:
            
            flag = True
            while flag == True:
                
                value = qr.scanner()
                if value == None:
                    
                    verify = self.login(self.idn, self.nme)
                    if verify == True:
                        
                        print("\nMarking for the absenties...")
                        fetch_from = ['student','teacher'] #list of tables to fetch data from
                        
                        for i in fetch_from:
                            
                            query = f"select name,division,section from {i};"
                            mycursor.execute(query)
                            details_list = mycursor.fetchall() # list of tuples having name and division in the format [('name','division', 'section),('name','division', 'section'),...]
                            query = f"select idn from attendance where attended='Yes' and date='{today}';"
                            mycursor.execute(query)
                            attendies = [idn[0] for idn in mycursor.fetchall()]
                            
                            for details in details_list:
                                query = f"select idn from login where name = '{details[0]}';"
                                mycursor.execute(query)
                                idn = mycursor.fetchone()[0]
                                if idn not in attendies:
                                    query = f"insert into attendance values('{details[0]}','{idn}','{details[1]}', '{details[2]}','No', '{today}');"
                                    mycursor.execute(query)
                                    mydb.commit()

                        print("\nAll the absenties have been marked.")
                        return True
                    
                    else:
                        query = "insert into failed_login values('{}','{}')".format(self.idn, today)
                        mycursor.execute(query)
                        mydb.commit()
                        return False
                    
                else:
                    print(value)
                    values = value.split(',')
                    query = f"insert into attendance values('{values[0]}','{values[1]}','{values[2]}','{values[3]}','Yes','{today}');"
                    print(query)
                    mycursor.execute(query)
                    mydb.commit()
                    print("\nAttendance marked for",values[0])
                    
        return False
    
    def new_credentials(self):
        dict_of_items = {"symbols" : '!@#$%^&+-*/=()}]{[:";<>.,~',
        "small alphabets" : 'abcdefghijklmnopqrstuvwxyz',
        "capital alphabets" : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        "numbers" : '0123456789'}

        idn = ''
        password = ''
        for i in range(8):
            key = random.choice(["symbols", "small alphabets", "capital alphabets", "numbers"])
            item = dict_of_items[key]
            password = password + item[random.randint(0,len(item)-1)]

        for i in range(5):
            key = random.choice(["small alphabets", "numbers"])
            item = dict_of_items[key]
            idn = idn + item[random.randint(0,len(item)-1)]
        return idn, password

    def rem_from_table(self, idn, table):
        try:
            
            if table != 'classroom':
                
                try:

                    # extract name using idn 
                    query1 =f"select name from login where idn='{idn}';"
                    mycursor.execute(query1)
                    
                    tuple_of_name = mycursor.fetchone()
                    name = tuple_of_name[0]
                    
                    # to form the name of qr-code file so that can be deleted
                    query3 = f"select name,division,section from {table} where name='{name}'"
                    mycursor.execute(query3)
                    
                    # delete qr-code from the database
                    record = mycursor.fetchone()
                    file_name = record[0]+'-'+record[1]+'-'+record[2]+'.png'
                    os.remove(os.path.join(qr_code_dir, file_name))
                    
                    # finally delete particiapnt from tables.
                    query2="delete from {} where name='{}'".format(table, name)
                    query4="delete from login where idn='{}'".format(idn)
                    mycursor.execute(query4)
                
                except Exception as e:
                    print(f"Error occured while trying to remove {table} & Error is:{e}")
                
            else:
                query2="delete from classroom where room_number='{}'".format(idn)
            
            mycursor.execute(query2)
            mydb.commit()
            print(f'{table} removed successfully.')
            return True
        
        except Exception as e:
            return e
    
    def result(self,accnt,sec): 

        if accnt=='student':
            ch=2
        
        elif accnt=='teacher':
            print('''
            What you want to do with Result:
            Enter 1 to display result of whole class for a particular test.
            Enter 2 to display result of a particular student.
            Enter 3 to display result of a particular student for a particular test.
            Enter 4 to enter marks for new test.
            Enter 5 to exit.''')
            ch=int(input(':'))
        
        if ch==1:
            try:
                tst=input('Enter Name of test:')
                query='select * from result where Name_of_test="{}"'.format(tst)
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.result(accnt,sec)
            except Exception :
                return
            
        elif ch==2:
            try:
                if accnt=='student':
                    rlln=self.rlln
                elif accnt=='teacher':
                    rlln=int(input('Enter Roll Number of student:'))  
                query='select * from result where roll_no={} and section="{}"'.format(rlln,sec)
                mycursor.execute(query)
                t= PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                if accnt == 'student':
                    return True
                else:
                    return self.result(accnt,sec)
            except Exception :
                return

        elif ch==3:
            try:
                tst=input('Enter Name of Test: ')
                rlln=int(input('Enter roll number of student: '))
                query='select * from result where \
            roll_no={} and Name_of_test="{}"'.format(rlln,tst)
                mycursor.execute(query)
                t=PrettyTable(['Name of Student','Division','Section','Roll No','Maths','English','Computer','Physics','Chemistry','Total','Grade','Name Of Test'])
                data=mycursor.fetchall()
                for i in data:
                    t.add_row(i)
                print(t)
                return self.result(accnt,sec)
            except Exception :
                return
        
        elif ch==4:
            try:
                print('Enter Name of test:')
                name_of_test=input(':')
                query='select student.name,student.division,student.section,student.roll_number from \
            student where student.section="{}"'.format(sec)
                mycursor.execute(query)
                rec=mycursor.fetchall()
                for i in range(1,len(rec)+1):
                    nme1=rec[i-1][0]
                    rlln=rec[i-1][3]
                    print(f"Name: {nme}, Roll Number: {rlln}")
                    mm=int(input(f'Enter Number for Maths for roll number {i}: ')) #marks for maths
                    me=int(input(f'Enter Number for Emglish for roll number {i}: ')) #marks for English
                    mc=int(input(f'Enter Number for Computer for roll number {i}: ')) #marks for computer
                    mp=int(input(f'Enter Number for Physics for roll number {i}: ')) #marks for physics
                    mch=int(input(f'Enter Number for Chemistry for roll number {i}: ')) #marks for chemistry
                    g=input(f'Enter Grades for roll number {i}: ') #grades
                    t=mm+me+mc+mp+mch
                    query='insert into result values("{}","{}","{}",{},{},{},{},{},{},"{}","{}","{}");'.format(nme1,dvs,sec,rlln,mm,me,mc,mp,mch,t,g,name_of_test)
                    mycursor.execute(query)
                    mydb.commit()
                print('Result for ',name_of_test,' is done.')
                return self.result(accnt,sec)
            except Exception :
                return
        
        elif ch==5:
            return True
        
        else:
            print("Wrong choice entered. Please try again...")
            return self.result(accnt,sec)

# class for administration works
class admin(base):

    def __init__(self,nme = '', idn = 'admin'):
        super().__init__(idn, nme)
        
    def start(self):
        
        verify = self.check()
        if verify == True:
            return self.ask()
        else:
            return verify
        
    def ask(self):
        print('-'*90)
        accnt='admin'
        print('''
        Welcome Admin,What would you like to do...
        To Add a teacher please enter 1.
        To Remove a teacher enter 2.
        To Add a student please enter 3.
        To Remove a student enter 4.
        To Add a Class enter 5.
        To Remove a Class enter 6.
        To start attendance for today enter 7.
        Enter 8 to see saved information.
        To exit enter 9.
        ''')
        
        ch=int(input('Enter:'))
        if ch==1:
            nme=input('Enter name of teacher:') #nme is for name
            div=input('Enter division of teacher:')
            sec=input('Enter section of teacher:')
            sal=int(input('Enter Salary:')) #sal is for salary
            phn=input('Enter Phone Number of teacher:')
            email=input('Enter Email of teacher:')
            
            rv=self.add_to_table(table='teacher', values=[nme,div,sec,sal,phn,email])
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
                    
        elif ch==2:
            idn=input('Enter idn of teacher:')
            rv=self.rem_from_table(idn, table = "teacher")
            if not rv:
                print('Something went wrong...', rv)
                print('Please Try Again')
            return self.ask()

        elif ch==3:
            
            nme1=input('Enter name of Student: ') #nme is for name
            div=input('Enter division of Student: ') #nme is for name
            sec=input('Enter section of Student: ') #nme is for name
            rlln=input('Enter Roll Number: ') #rlln is for roll number 
            PNo=input('Enter Phone Number: ') #PNo is for Phone Number
            email=input('Enter email of student: ')
            
            rv=self.add_to_table(table='student', values=[nme1,div,sec,rlln,PNo,email])
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==4:
            idn = input("Enter idn of student:")
            rv=self.rem_from_table(idn,table = 'student')
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()

        elif ch==5:
            rno=int(input('Enter room number:'))#rno is for room number
            div=input('Enter division:')#div is for division
            tchr=input('Enter teacher:') #tchr is for teacher
            sec = input('Enter section:')
            
            rv=self.add_to_table(table='classroom', values=[rno,div,tchr,sec])
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
                   
        elif ch==6:
            rno=input('Enter Room number:')
            rv=self.rem_from_table(idn = rno, table = 'classroom')
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==7:
            rv = self.mark_attendance()
            if rv == True:
                return self.ask()
            else:
                return rv

        elif ch==8:
            rv=self.display(accnt,div='',sec='')
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
                    
        elif ch==9:
            os.system("clear")
            exit()
        
        else:
            print('Wrong choice entered:')
            return self.ask()

# class for teacher accounts
class teacher(base):
    
    def __init__(self, idn, nme):
        super().__init__(idn, nme)
        
    def start(self):
        
        verify = self.check()
        if verify == True:
            return self.ask()
        else:
            return verify
    
    def ask(self):
        
        accnt='teacher'
        print('-'*90)
        query='select division,section from teacher where name="{}"'.format(self.nme) 
        mycursor.execute(query)
        record=mycursor.fetchone()
        div=record[0]
        sec=record[1]
        print('Your class is',div,'-',sec,'What would you Like to do..')
        print('''
        For Attendance related work enter 1.
        For Result related work enter 2.
        To display all the students of class enter 3.
        To exit enter 4.
        ''')
        ch=int(input('Enter: '))
        print('-'*90)
        
        if ch==1:
            rv=self.attendance(accnt,div,sec)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
                
        elif ch==2:
            rv=self.result(accnt,sec)
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
                print('Something went wrong...')
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
    
    def __init__(self, idn, nme, rlln, sec):
        super().__init__(idn, nme)
        self.rlln = rlln
        self.sec = sec
    
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
        Enter 1 to see  result.
        Enter 2 to see Attendance.
        Enter 3 to see your information.
        Enter 4 to exit.
        ''')
        
        ch=int(input(':'))
        if ch==1:
            
            rv=self.result(accnt,self.sec)
            if rv==True:
                return self.ask()
            
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==2:
            query='select division from student where name="{}"'.format(self.nme)
            mycursor.execute(query)
            rec=mycursor.fetchone()
            div=rec[0]
            rv=self.attendance(accnt,div,self.sec)
            if rv==True:
                return self.ask()
            else:
                print('Something went wrong...')
                print('Please Try Again')
                return self.ask()
        
        elif ch==3:
            rv=self.display(accnt,div='',sec=self.sec)
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
