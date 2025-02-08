import os
import pwinput
from core import teacher
   
while True:
        os.system("clear")
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)

        nme=input('\nWelcome Teacher,Please enter your full name: ')

        idn=pwinput.pwinput('\nPlease enter your unique id number: ', mask='*')

        teacher_object = teacher(idn, nme)
        verify = teacher_object.start()
        if verify==0:
            print('You have been locked out of your account. Please contact Admin for help.')
        elif verify == -1:
            print('No Teacher with this name exists in database.')
        else:
            print("Something went wrong here. Please contact Admin.")