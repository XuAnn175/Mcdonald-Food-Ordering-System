import staff
import yeehoo
from os import system

if __name__=='__main__':
    while True:
        system("cls")
        print("Welcome to our YEEhoO system!")
        option=int(input("Which system will want to use?\n1:Customer\n2:Staff system\n3:Quit\n"))
        system("cls")
        if option==1 or option==2:
            if option==1:
                yeehoo.yeehoo_system()
            else:
                staff.staff_system()
        else:
            break
    print("Thanks for using YEEhoO!!!")