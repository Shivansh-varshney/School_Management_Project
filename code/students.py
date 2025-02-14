import os
import pwinput
from core import student
   
os.system("clear")
while True:
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)

        email= input('\nPlease enter your email: ')

        student_object = student(email)
        verify = student_object.start()
        if verify==0:
                print('You have been locked out of your account. Please contact Admin for help.')
        elif verify == -1:
            print('No Student with this name exists in database.')
        elif verify == 1:
            continue
        else:
            print("Something went wrong here. Please contact Admin.")