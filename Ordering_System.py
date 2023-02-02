from psycopg2 import connect
from os import system
from time import localtime
import time
from random import randint

def update_log(conn,query,Trade_ID,ID,Transaction_Amount_Money,Transaction_Amount_Point):
    times=localtime()
    date=str(times.tm_year)+'/'+str(times.tm_mon)+'/'+str(times.tm_mday)
    query.execute('insert into "Log" values(%s,%s,%s,%s,%s)',(Trade_ID,date,ID,Transaction_Amount_Money,Transaction_Amount_Point))
    conn.commit()
    
def store(conn,query,ID):
    system('cls')
    num=int(input("How much do you want to store?\n"))
    query.execute('select "Balance" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    row=query.fetchone() 
    Trade_ID=str(randint(0,100000))
    savings=int(row[0])+num
    query.execute('update "VIP_Card" set "Balance"=%s where "Card_ID"=%s',(savings,ID))
    conn.commit()
    
    update_log(conn,query,Trade_ID,ID,num,0)
    
    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'_'+str(times.tm_mon)+'_'+str(times.tm_mday)
            path=date+'_Store_'+str(ID)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("Your Receipt.\n")
            file.write("==============================\n")
            query.execute('select * from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
            row=query.fetchone()
            lines=["ID:\t",str(row[1]),"\t\tCard_ID:\t",str(row[0]),"\nDate:\t",date,"\nTime:\t",timing,"\nBalance:\t",str(row[2]),"\nPoint:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tStore\nMoney:\t+",str(num)]
            file.writelines(lines)
            file.write("\n==============================\nYEEhoO")
            break
        elif receipt==2:
            break
    return

def exchange(conn,query,Card_ID):
    system('cls')

    query.execute('select "Meal_ID","Meal_Name","Price","Point","Remaining_Amount" from "Menu"')
    rows=query.fetchall()
        
    flag_ID=False
    print("Meal_ID\tMeal_Name\tPrice\tPoint\tRemaining_Amount\n")
    for row in rows:        
        print(row[0],"\t",row[1],"\t",row[2],"\t",row[3],"\t",row[4],"\n")
    
    query.execute('select "Balance","Point" from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':Card_ID})
    row=query.fetchone()
    print("You have...\nCash: ",row[0],"\nPoint: ",row[1],"\n")
    meal_id=input("Which meal do you want to buy?\n")
    query.execute('select "Meal_ID" from "Menu"')
    check_menu = query.fetchall()
    check = False
    for meal in check_menu:
        if meal_id==meal[0]:
            check = True
            break
    if check==False:
        print("We do not offer meal", meal_id, ".\nPlease choose a real meal.\n")
        return

    query.execute('select "Remaining_Amount" from "Menu" where "Meal_ID"=%(ID)s',{'ID':meal_id})
    row=query.fetchone()
    if int(row[0])<=0:
        print("87YEEhoO")
        return
    
    op=input("Which method do you want to pay?\n1 Cash\n2 Point\n")
    if op=='1':
        query.execute('select "Balance" from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':Card_ID})
        row1=query.fetchone()
        query.execute('select "Price" from "Menu" where "Meal_ID"=%(Meal_ID)s',{'Meal_ID':meal_id})
        row2=query.fetchone()
        if(int(row1[0])<int(row2[0])):
            print("You don't have enough money.\n87YEEhoO")
            return
        query.execute('select "Point" from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':Card_ID})
        row4=query.fetchone()
        query.execute('update "VIP_Card" set "Balance"=%s where "Card_ID"=%s',(str(int(row1[0])-int(row2[0])),(Card_ID)))
        query.execute('update "VIP_Card" set "Point"=%s where "Card_ID"=%s',(str(round(float(row4[0])+float(row2[0])*0.1,1)),(Card_ID)))
        query.execute('select "Meal_Name" from "Menu" where "Meal_ID"=%(Meal_ID)s',{'Meal_ID':meal_id})
        row3=query.fetchone()
        print("You get a ",row3[0], ", yeehoo!\n")
        conn.commit()
        Trade_ID=str(randint(0,100000))
        update_log(conn,query,Trade_ID,Card_ID,str(-int(row2[0])),str(int(row2[0])*0.1))
    elif op=='2':
        query.execute('select "Point" from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':Card_ID})
        row1=query.fetchone()
        query.execute('select "Point" from "Menu" where "Meal_ID"=%(Meal_ID)s',{'Meal_ID':meal_id})
        row2=query.fetchone()
        if(float(row1[0])<float(row2[0])):
            print("You don't have enough point.\n87YEEhoO\n")
            return
        query.execute('update "VIP_Card" set "Point"=%s where "Card_ID"=%s',(str(round(float(row1[0])-float(row2[0]),1)),(Card_ID)))
        query.execute('select "Meal_Name" from "Menu" where "Meal_ID"=%(Meal_ID)s',{'Meal_ID':meal_id})
        row3=query.fetchone()
        print("You get a ", row3[0], ", yeehoo!\n")
        conn.commit()
        Trade_ID=str(randint(0,100000))
        update_log(conn,query,Trade_ID,Card_ID,str(0),str(-int(row2[0])))
    else:
        print("Error: Please pay with cash or point!")
        return
    
    query.execute('select "Balance","Point" from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':Card_ID})
    remain=query.fetchone()
    print("Remaining...\nCash: ",remain[0],"\nPoint: ",remain[1],"\n")

    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'_'+str(times.tm_mon)+'_'+str(times.tm_mday)
            path=date+'_Exchange_'+str(Card_ID)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("Your Receipt.\n")
            file.write("==============================\n")
            query.execute('select * from "VIP_Card" where "Card_ID"=%(Card_ID)s',{'Card_ID':Card_ID})
            row=query.fetchone()
            query.execute('select "Meal_Name" from "Menu" where "Meal_ID"=%(Meal_ID)s',{'Meal_ID':meal_id})
            row3=query.fetchone()
            lines=["ID:\t",str(row[1]),"\t\tCard_ID:\t",str(row[0]),"\nDate:\t",date,"\nTime:\t",timing,"\n品項:\t",row3[0],"\nRemaining_Balance:",str(row[2]),"\nRemaining_Point:",str(row[3])]
            file.writelines(lines)
            file.write("\n==============================\nThanks for Using.")
            break
        elif receipt==2:
            break
    return   

def balance(query,ID):
    system('cls')
    times=localtime()
    print("Your Balance.")
    print("=============================")
    query.execute('select * from "VIP_Card" where "Card_ID"=%(ID)s',{'ID':ID})
    row=query.fetchone()
    date=str(times.tm_year)+'_'+str(times.tm_mon)+'_'+str(times.tm_mday)
    timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
    print('ID:\t',row[1])
    print('Card_ID:',row[0])
    print('Balance:',row[2])
    print('Point:\t',row[3])
    print('Date:\t',date)
    print('Time:\t',timing)
    print('-----------------------------')
    print("Operation:\tCheck Balance")
    print("=============================")
    return


def yeehoo_system():
    system('cls')
    print("You're in yeehoo system!")
    time.sleep(0.5)
    print("~Yeehoo~ ")
    time.sleep(0.5)
    print("~~Yeehoo~~ ")
    time.sleep(0.5)
    print("~~~Yeehoo~~~ ")
    time.sleep(1)

    conet=connect(database='postgres',user='yeehoo',password='yeehooyeehoo',host='yeehoo.cdcziiki5cxt.us-east-1.rds.amazonaws.com',port='5432')
    query=conet.cursor()

    id=""   # customer_id
    ID=""   # card_id
    flag=False
    while True:
        system('cls')
        id=input("Please enter your ID:")
        query.execute('select "Card_ID" from "VIP_Card" where "ID"=%(id)s order by "Card_ID"',{'id':id})
        rows=query.fetchall()
        if(len(rows)==0):
            print("Wrong ID yeehoo~\nPlease enter valid ID!")
            time.sleep(2)
            continue
        for row in rows:
            print("Card_ID: ",row[0])
        ID=input("Please input your Card ID number:")
        flag1=False
        for row in rows:
            if(ID==row[0]):
                flag1=True
                break
        if(flag1==False):
            print("Wrong card id yeehoo~\n")
            time.sleep(2)
            continue
        query.execute('select "Card_ID" from "VIP_Card"')
        rows=query.fetchall()
        
        flag_ID=False
        for row in rows:
            if ID==row[0]:
                flag_ID=True
                flag=True
                break
        if flag_ID==False:
            print("There is no ID:'",ID,"'.",sep="")
            time.sleep(2)
            return
        
        if flag:
            break
    
    system('cls')
    print("Successfully login.")
    while True:
        operate=int(input("What do you want to do?\n1:Store\n2:Exchange\n3:Check Balance\n4:Quit\n"))
        flag_flag=True
        if operate==1:
            store(conet,query,ID)
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==2:
            exchange(conet,query,ID) #card id
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==3:
            balance(query,ID)
            while True:
                next_op=int(input("\nContinue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==4:
            system('cls')
            break
        else:
            system('cls')
            print("Error!")
        
        if flag_flag:
            system('cls')
        else:
            system('cls')
            break
    conet.close()
    
if __name__=='__main__':
    yeehoo_system()