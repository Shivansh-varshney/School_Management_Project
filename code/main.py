import main_classes as all
   
while True:
        print('*'*89)
        print('*\t\t\t\tSchool Management System\t\t\t\t*')
        print('*'*89)
        print("""
    Welcome,Please tell us your designation.
    For Admin enter 'A'.
    For Teacher enter 'T'.
    For Student enter 'S'.
    To End the Program enter 'E'.
    """)
        dsg=input(':') #dsg refers to designation

        if dsg=='A' or dsg=='a':
            print('Welcome Admin')
            admin_object = all.admin()
            
            verify = admin_object.start()
            if verify==0:
                print('You have been locked out of your account. Please contact backend team for help.')
            elif verify == -1:
                print('something went wrong. Please contact backend team for help.')
            else:
                continue

        elif dsg=='T' or dsg=='t':
            print('Welcome Teacher,Please enter your full name below,')
            nme=input(':')

            print('Please enter your unique id number')
            idn=input(':')

            teacher_object = all.teacher(idn,nme)
            verify = teacher_object.start()
            if verify==0:
                    print('You have been locked out of your account. Please contact Admin for help.')
            elif verify == -1:
                print('No Teacher with this name exists in database.')
            else:
                print("Something went wrong here. Please contact Admin.")

        elif dsg=='S' or dsg=='s':
            print('Welcome Student,Please enter your full name below,')
            nme=input(':')

            print('Please enter your Roll Number.')
            rlln=int(input(':'))

            print('Please enter your section.')
            sec=input(':')

            print('Please enter your unique id number.')
            idn=input(':')

            student_object = all.student(idn,nme,rlln,sec)
            verify = student_object.start()
            if verify==0:
                    print('You have been locked out of your account. Please contact Admin for help.')
            elif verify == -1:
                print('No Student with this name exists in database.')
            elif verify == 1:
                continue
            else:
                print("Something went wrong here. Please contact Admin.")

        elif dsg=='E' or dsg=='e':
            break

        else:
            print("Wrong choice entered.")
            continue