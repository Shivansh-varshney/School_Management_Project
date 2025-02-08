import os
from core import admin
   
while True:
        os.system("clear")
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)

        print('Welcome Admin')
        admin_object = admin()
        
        verify = admin_object.start()
        if verify==0:
            print('You have been locked out of your account. Please contact backend team for help.')
        elif verify == -1:
            print('something went wrong. Please contact backend team for help.')
        else:
            continue