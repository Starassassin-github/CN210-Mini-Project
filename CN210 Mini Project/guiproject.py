from pathlib import Path
from tkinter import Label, Tk, Canvas, Entry, Text, Button, PhotoImage, font
from tkinter.constants import END
import time
import os
import math
try:
    import psutil
    import cpuinfo
except:
    print("Don't have psutil and cpuinfo")

#variables
totalscore = 0
resetcpu = 0
resetram = 0
resetHdd = 0
try:
    cpu = str(cpuinfo.get_cpu_info()['brand_raw'])
    listCpu = cpu.split()
    name_Cpu = listCpu[0] + " " + listCpu[1] + " " + listCpu[2]
    store_Ram = format(psutil.virtual_memory().total / (1 << 30),'.2f') + "GB"
    store_Hdd = format((psutil.disk_usage('C:\\').total + psutil.disk_usage('D:\\').total) / (1 << 30),'.2f') + "GB"
    CPUnameX = 540.0
except:
    name_Cpu = "CPU Speed"
    store_Ram = "Ram Speed"
    store_Hdd = "Disk Speed"
    CPUnameX = 640.0

#path tkinter
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#build window
window = Tk()
window.title("CN210")
window.geometry("1152x700")
window.configure(bg = "#FFFFFF")

#build canvas
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 700,
    width = 1152,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

#background
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    724.0,
    350.0,
    image=image_image_1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    112.0,
    285.0,
    image=image_image_2)

#ช่องบอกScore
scoreRam = Entry(border=4,width=10,font=("Press Start 2P", 9),justify='center')
scoreRam.place( x = 315.0, y = 421.0 )

scoreCpu = Entry(border=4,width=10,font=("Press Start 2P", 9),justify='center')
scoreCpu.place( x = 635.0, y = 421.0 )

scoreHdd_Write = Entry(border=4,width=10,font=("Press Start 2P", 9),justify='center')
scoreHdd_Write.place( x = 945.0, y = 421.0 )

scoreHdd_Read = Entry(border=4,width=10,font=("Press Start 2P", 9),justify='center')
scoreHdd_Read.place( x = 945.0, y = 484.0 )

scoreTotal = Entry(border=10,width=7,font=("Press Start 2P", 25),justify='center')
scoreTotal.place( x = 720.0, y = 570.0 )

#ชื่อ CPU และขนาด Ram,Hdd
canvas.create_text(345.0,385.0,anchor="nw",text=store_Ram,fill="#000000",font=("Press Start 2P", 10))
canvas.create_text(CPUnameX,385.0,anchor="nw",text=name_Cpu,fill="#000000",font=("Press Start 2P", 10))
canvas.create_text(977.0,385.0,anchor="nw",text=store_Hdd,fill="#000000",font=("Press Start 2P", 10))

#reset ค่าทั้งหมด
def reset():
    global totalscore
    global resetcpu
    global resetram
    global resetHdd
    scoreRam.delete(0,END)
    scoreCpu.delete(0,END)
    scoreHdd_Write.delete(0,END)
    scoreHdd_Read.delete(0,END)
    scoreTotal.delete(0,END)
    totalscore = 0
    resetcpu = 0
    resetram = 0
    resetHdd = 0    

#test Memory
def testRam():
    global totalscore
    global resetram
    totalscore -= resetram
    scoreRam.delete(0,END)
    scoreTotal.delete(0,END)

    start = time.time()
    structor()
    structor()
    structor()
    structor()
    structor()
    end = time.time()
    total = end - start
    scoreRam.insert(0, f"{total:.2f}")

    resetram = total
    totalscore += total
    scoreTotal.insert(0, f"{totalscore:.2f}")

#test CPU
def testCpu():
    global totalscore
    global resetcpu
    totalscore -= resetcpu
    scoreCpu.delete(0,END)
    scoreTotal.delete(0,END)

    start = time.time()
    defin()
    end = time.time()
    total = end - start
    scoreCpu.insert(0, f"{total:.2f}")

    resetcpu = total
    totalscore += total
    scoreTotal.insert(0, f"{totalscore:.2f}")

#test Disk
def testHdd():
    global totalscore
    global resetHdd
    totalscore -= resetHdd
    scoreHdd_Write.delete(0,END)
    scoreHdd_Read.delete(0,END)
    scoreTotal.delete(0,END)

    t0 = time.time()
    #write file
    with open("xyz.txt", "w") as f:
        for r in range(180000000):
            f.write(f"{r}\n")
        f.close

    t1 = time.time()
    #read file
    with open("xyz.txt") as name:
        x = name.read()
        name.close

    t2 = time.time()
    writetime = t1 - t0
    readtime = t2 - t1
    total = t2 - t0
    os.remove("xyz.txt")
    scoreHdd_Write.insert(0, f"W:{writetime:.2f}")
    scoreHdd_Read.insert(0, f"R:{readtime:.2f}")

    resetHdd = t2 - t0
    totalscore += total
    scoreTotal.insert(0, f"{totalscore:.2f}")

#ทำเลขฐาน2
def toBinaryNumber(n):
    BinaryNumber = ""
    t = 1
    num = 0
    while(t<=n):
        num = 2**t
        if(num>n):
            num = 2**(t-1)
            break
        t+=1

    for i in range(t-1,-1,-1):
        check = 2**i
        if(n>=(check)):
            BinaryNumber = BinaryNumber+"1"
            n -= check
        elif(n<check):
            BinaryNumber = BinaryNumber+"0"
    return BinaryNumber

#เปลี่ยน String เลข3หลัก เป็น Integer
def toInteger(s):
    list3 = []
    num = 0
    for j in s:
        list3.append(j)
    if(len(list3)==3):
        if(list3[0]=="1"):
            num += 100
        if(list3[1]=="1"):
            num += 10
        if(list3[2]=="1"):
            num+=1
    if(len(list3)==2):
        if(list3[0]=="1"):
            num += 10
        if(list3[1]=="1"):
            num += 1
    if(len(list3)==1):
        if(list3[0]=="1"):
            num+=1
    return num

#เปลี่ยนเป็นเลขฐาน10
def toNumTen(x):
    num =0
    two =1
    while(x>0):
        num += (x%10)*two
        two*=2
        x = math.floor(x/10)
    return num

#เปลี่ยนเลขเป็น String
def numToString(num):
    if(num==1):
        return "1"
    elif(num==2):
        return "2"
    elif(num==3):
        return "3"
    elif(num==4):
        return "4"
    elif(num==5):
        return "5"
    elif(num==6):
        return "6"
    elif(num==7):
        return "7"
    elif(num==0):
        return "0"

#เปลี่ยนเลขฐาน10 เป็นฐาน8
def defin():
    list1 = []
    for i in range(5000000,10000000):
        RandNUm = i
        result = toBinaryNumber(RandNUm)
        list1.append(result)

    eightNum = ""
    listEightNum = []
    for i in list1:
        list2 = []
        for z in i:
            list2.append(z)
        while(len(list2)>0):
            if(len(list2) >= 3):
                numThree = list2[len(list2)-3]+list2[len(list2)-2]+list2[len(list2)-1]
                list2.pop(len(list2)-1)
                list2.pop(len(list2)-1)
                list2.pop(len(list2)-1)
                num1 = toInteger(numThree)
                num2 = toNumTen(num1)
                eightNum = numToString(num2) + eightNum
            elif(len(list2)==2):
                numThree = list2[len(list2)-2]+list2[len(list2)-1]
                list2.pop(len(list2)-1)
                list2.pop(len(list2)-1)
                num1 = toInteger(numThree)
                num2 = toNumTen(num1)
                eightNum = numToString(num2) + eightNum
            else:
                numThree = list2[0]
                list2.remove(list2[0])
                num1 = toInteger(numThree)
                num2 = toNumTen(num1)
                eightNum = numToString(num2) + eightNum
        listEightNum.append(eightNum)
        eightNum = ""
    return listEightNum

#เปลี่ยนค่าใน list
def setter(list):
    for j in range(len(list)):
        list[j] = 5

def setter2(list):
    for j in range(len(list)):
        list[j] = 0

#สร้าง list และกำหนดเลข
def structor():
    list = []
    for i in range(100000000):
        list.append(i)
    setter(list)
    setter2(list)
    
    list2 = []
    for z in range(100000000):
        list2.append(z)
    setter(list2)
    setter2(list2)


#button reset
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=reset)
button_1.place(
    x=21.0,
    y=597.0,
    width=206.0,
    height=87.0)

#button test Memory
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=testRam)
button_2.place(
    x=260.0,
    y=157.0,
    width=262.0,
    height=205.0)

#button test CPU
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=testCpu)
button_3.place(
    x=602.0,
    y=157.0,
    width=226.0,
    height=223.0)

#button test Disk
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=testHdd)
button_4.place(
    x=949.0,
    y=170.0,
    width=175.0,
    height=192.0)


window.mainloop()