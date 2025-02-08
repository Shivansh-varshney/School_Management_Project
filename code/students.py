import os
import pwinput
from core import student
   
while True:
        os.system("clear")
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)

        nme=input('\nWelcome Student,Please enter your full name: ')
        rlln=int(input('\nPlease enter your Roll Number: '))
        sec=input('\nPlease enter your section: ')
        idn=pwinput.pwinput('\nPlease enter your unique id number: ', mask="*")

        student_object = student(idn,nme,rlln,sec)
        verify = student_object.start()
        if verify==0:
                print('You have been locked out of your account. Please contact Admin for help.')
        elif verify == -1:
            print('No Student with this name exists in database.')
        elif verify == 1:
            continue
        else:
            print("Something went wrong here. Please contact Admin.")