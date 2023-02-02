from time import localtime
import time
from psycopg2 import connect
from os import system
from random import randint

def logfile(query,ID):
    query.execute('select "Permission" from "Staff" where "ID"=%(ID)s',{'ID':ID})
    row=query.fetchone()
    if int(row[0])!=1:
        system('cls')
        print("Permission Denied.")
        return
    times=localtime()
    date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
    query.execute('select * from "Log"')
    rows=query.fetchall()
    for row in rows:
        print("Trade_ID: ",row[0]," \tTime: ",row[1],"\tUser_ID: ",row[2],"\tTransaction_Amount_Money: ",row[3],"\t\tTransaction_Amount_Point: ",row[4])
    return 

def update_log(conn,query,Trade_ID,ID,Transaction_Amount_Money,Transaction_Amount_Point):
    times=localtime()
    date=str(times.tm_year)+'/'+str(times.tm_mon)+'/'+str(times.tm_mday)
    query.execute('insert into "Log" values(%s,%s,%s,%s,%s)',(Trade_ID,date,ID,Transaction_Amount_Money,Transaction_Amount_Point))
    conn.commit()

def gift(conn,query,ID):
    system('cls')
    num=int(input("How much do you want to give a gift?\n"))
    query.execute('select "Balance" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    row=query.fetchone() 
    Trade_ID=str(randint(0,100000))
    savings=int(row[0])+num
    query.execute('update "VIP_Card" set "Balance"=%s where "Card_ID"=%s',(savings,ID))
    conn.commit()
    
    update_log(conn,query,Trade_ID,ID,num,0)
    
    query.execute('select "Balance","Point" from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':ID})
    remain=query.fetchone()
    print("Card ID: ", ID,"\nCash: ",remain[0],"\nPoint: ",remain[1],"\n")

    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'_'+str(times.tm_mon)+'_'+str(times.tm_mday)
            path=date+'_Gift_'+str(ID)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("HAPPY YEEHoO DAY.\nYEEHoO~~~~~~~~\n")
            file.write("==============================\n")
            query.execute('select * from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
            row=query.fetchone()
            lines=["ID:\t",str(row[1]),"\t\tCard_ID:\t",str(row[0]),"\nDate:\t",date,"\nTime:\t",timing,"\nBalance:\t",str(row[2]),"\nPoint:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tGift\nMoney:\t+",str(num)]
            file.writelines(lines)
            file.write("\n==============================\nYEEhoO")
            break
        elif receipt==2:
            break
    return

def oh_shit(conn,query,ID,surprise,msg):
    system('cls')
    query.execute('select "Balance" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    row=query.fetchone() 
    Trade_ID=str(randint(0,100000))
    savings=int(row[0])+surprise
    query.execute('update "VIP_Card" set "Balance"=%s where "Card_ID"=%s',(savings,ID))
    conn.commit()
    update_log(conn,query,Trade_ID,ID,surprise,0)
    print("Sending Surprise: Card ID: ", ID)
    times=localtime()
    date=str(times.tm_year)+'_'+str(times.tm_mon)+'_'+str(times.tm_mday)
    path=date+'_Surprise_'+str(ID)+'.txt'
    timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
    file=open(path,'w')
    file.write(msg)
    file.write("\nYEEHoO~~~~~~~~\n")
    file.write("==============================\n")
    query.execute('select * from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    row=query.fetchone()
    lines=["ID:\t",str(row[1]),"\t\tCard_ID:\t",str(row[0]),"\nDate:\t",date,"\nTime:\t",timing,"\nBalance:\t",str(row[2]),"\nPoint:\t",str(row[3])]
    file.writelines(lines)
    file.write("\n------------------------------\n")
    lines=["Operation:\tGift\nMoney:\t+",str(surprise)]
    file.writelines(lines)
    file.write("\n==============================\nYEEhoO")

def check_card(conn,query,ID):
    query.execute('select "ID" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    owner=query.fetchone()
    query.execute('select "Balance" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    bal=query.fetchone()
    query.execute('select "Point" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    poi=query.fetchone()
    print(ID, "\t", owner[0], "\t\t", bal[0], "\t", poi[0])

def staff_system():
    system('cls')
    print("You're in staff system!")
    
    conet=connect(database='postgres',user='yeehoo',password='yeehooyeehoo',host='yeehoo.cdcziiki5cxt.us-east-1.rds.amazonaws.com',port='5432')
    query=conet.cursor()
    
    ID=''
    flag=False
    
    while True:
        ID=input("Please input your staff ID number:")
        query.execute('select "ID" from "Staff"')
        rows=query.fetchall()
        
        flag_ID=False
        for row in rows:
            #print(row[0])
            if int(ID)==int(row[0]):
                flag_ID=True
                flag=True
                break
        if flag_ID==False:
            print("There is no staff ID:'",ID,"'.",sep="")
            time.sleep(2)
            return

        if flag:
            break

    query.execute('select "Name" from "Staff" where "ID"=%(ID)s',{'ID':ID})
    row=query.fetchone()
    
    system('cls')
    print("Welcome! ",row[0],".",sep="")
    while True:
        operate=int(input('What do you want to do?\n1:Check Daily Log\n2:Gift(Don\'t press me)\n3:Surprise~~~~~\n4:Check Card\n5:Quit\n'))
        flag_flag=True
        if operate==1:
            logfile(query,ID)
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==2:
            system('cls')
            query.execute('select "Card_ID", "Balance" from "VIP_Card" order by "Card_ID"')
            rows=query.fetchall()
            for row in rows:
                print("Card_ID: ",row[0], "\tCash: ", row[1])
            id=input("Which id do you want to give a gift to?\n")
            fl_ID=False
            for row in rows:
                if id == row[0]:
                    fl_ID=True
                    break
            if fl_ID==False:
                print("Wrong Card ID!\n")
                time.sleep(1)
                system('cls')
                continue
            gift(conet,query,id)
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break

        elif operate==3:
            system('cls')
            query.execute('select "Card_ID" from "VIP_Card" order by "Card_ID"')
            rows=query.fetchall()
            surprise=int(input("How much do you want to give a surprise?\n"))
            msg=input("What surprising message do you want to send?\n")
            for id1 in rows:
                oh_shit(conet, query, id1[0], surprise, msg)
            system('cls')
            print("Sending Successfully!\n")
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break

        elif operate==4:
            system('cls')
            query.execute('select "Card_ID" from "VIP_Card" order by "Card_ID"')
            rows=query.fetchall()
            print("Card_ID\t Owner_ID\tBalance\tPoint")
            for row in rows:
                check_card(conet, query, row[0])
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break

        elif operate==5:
            system('cls')
            break
        else:
            system('cls')
            print('Error!')
        
        if flag_flag:
            system('cls')
        else:
            system('cls')
            break
    conet.close()
    
if __name__=='__main__':
    staff_system()