import os
import pwinput
from core import teacher
   
os.system("clear")
while True:
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)
        print("Welcome Teacher")
        email=input('\nPlease enter your email: ')

        teacher_object = teacher(email)
        verify = teacher_object.start()
        if not verify:
            print('You have been locked out of your account. Please contact Admin for help.')
        elif verify == -1:
            print('No Teacher with this name exists in database.')
        else:
            print("Something went wrong here. Please contact Admin.")
            break