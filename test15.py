from datetime import time    ##import วันที่ เวลา เผื่อไว้ใช้งาน
from random import Random, random #import random เพื่อใช้งานในการ random
from imutils import paths #import imutils (paths - ใช้ในการดึงที่อย๋ไฟล์)
import cv2      #import cv2 = opencv มีฟังก์ชันสำหรับการทำงานที่เกี่ยวกับรูปภาพมากมาย
import numpy as np  #import numpy เรียกใช้โดย np (แล้วแต่ว่าจะใช้ทำอะไร)
import mysql.connector #เชื่อมดาต้าเบส
from terminaltables import AsciiTable    #ทำตารางให้ดูดี

#connect database
mydb = mysql.connector.connect(     #10-16 = ไว้สำหรับเชื่อม database 
    host="localhost",
    username = "root",
    password="",
    database="dataeye"
    )
mycursor = mydb.cursor()

test_image_glaucoma = []      #กำหนดเป็นarray ที่มีค่าว่าง เพื่อนำไปใช้งาน
winrate_normal = ""     #19-20 กำหนดตัวแปรเป็นรูปแบบ string เพื่อไว้ใช้งาน
winrate_glaucoma =""
def my_function():
    imagePathTrain = list(paths.list_images(r"D:\project-Imageprocess\dataset 1\Glaucoma")) #train 80% ตาต้อ
    imagePathTrain_Normal = list(paths.list_images(r"D:\project-Imageprocess\dataset 1\Normal")) #train 80% ปรกติ 
    imagePathTest = list(paths.list_images(r"D:\project-Imageprocess\TEST_GLAUCOMA"))    #test 20 ตาต้อ 
    imagePathTest_Normal = list(paths.list_images(r"D:\project-Imageprocess\TEST_NORMAL"))  #test 20% ตาปรกติ 
    i = 0
    count = 0
    print("--------WAIT TRAIN NORMAL 80%----------")
    for imagetrain in imagePathTrain_Normal:  #กำหนดตัวแปร imagetrain ให้วนลูปรับค่าจาก imagePathTrain_Normal
        i = int(i)+1                          #กำหนดให้ตัวแปร i + 1 ในทุกๆครั้งที่รับค่าจากรูปภาพ จุดประสงค์คือไว้ใช้บันทึกลง database                        
        image = cv2.imread(imagetrain)        #รับค่า path ที่อยู่มาแล้วทำการรันและเก็บค่าไว้ในตัวแปร image
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #แปลงรูปภาพปรกติให้เป็นสีเทา
        kernel = np.ones((5, 5), np.uint8)          #ค่าเริ่มต้นสำหรับ kernel ใช้ในการแปลงรูปภาพ errosion
        image = cv2.erode(grey, kernel)       #แปลงรูปภาพสีเทาโดยใช้การ errosion
        ist,bins = np.histogram(image.ravel(),256,[0,256])  #นำค่ารูปภาพที่แปลงแล้วมาหาค่า histrogram ทั้งหมด 256 ช่อง [0,256]
        m = np.mean(ist)     #หาค่าเฉลี่ยของแต่ละช่อง ["1,2,3", "2,5,8"] => ["2","5"]
        var = ((m-ist)**2).mean() #นำข้อมูลไปหาความแปรปรวนรวมของทุกช่อง ใน 1รูปภาพ
        var = round(var)  #แปลงเลขทศนิยมเป็นเลขจำนวนเต็ม
        var = str(var)  #แปลงจากเลขจำนวนเต็มเป็น string เพื่อบันทึกลง database
        type = "NORMAL"            #40-45 => เป็นการบันทึกข้อมูลลง database
        count = count+1
        sql = "INSERT INTO datapicture_normal (name, mean_img_normal , type_normal) VALUES (%s, %s, %s)"
        val = (count, var, type)
        mycursor.execute(sql, val)
        mydb.commit()
        cv2.waitKey()
    print("--------SUCCESS TRAIN NORMAL 80%----------")     #47-112 เป็นการทำซ้ำข้อมูลอีก 3 ชุดที่เหลือ

    i = 0
    count = 0
    print("--------WAIT TEST GLAUCOMA 20%----------")
    for imagetest in imagePathTest:
        i = int(i)+1
        image = cv2.imread(imagetest)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ##greyimage
        kernel = np.ones((5, 5), np.uint8)
        image = cv2.erode(grey, kernel)
        ist,bins = np.histogram(image.ravel(),256,[0,256]) 
        m = np.mean(ist) 
        var = ((m-ist)**2).mean()
        var = round(var)
        var = str(var)
        count = count+1
        sql = "INSERT INTO test_image_glaucoma (name, mean_test) VALUES (%s, %s)"
        val = (count, var)
        mycursor.execute(sql, val)
        mydb.commit()
        cv2.waitKey()
    print("--------SUCCESS TEST GLAUCOMA 20%----------")
    i = 0
    count = 0
    print("--------WAIT TEST NORMAL 20%----------")
    for imagetest_normal in imagePathTest_Normal:      ##TEST 20% ตาปรกติ
        i = int(i)+1
        image = cv2.imread(imagetest_normal)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ##greyimage
        kernel = np.ones((5, 5), np.uint8)
        image = cv2.erode(grey, kernel)
        ist,bins = np.histogram(image.ravel(),256,[0,256]) 
        m = np.mean(ist) 
        var = ((m-ist)**2).mean()
        var = round(var)
        var = str(var)
        count = count+1
        sql = "INSERT INTO test_img_nomal (name, mean_test_normal) VALUES (%s, %s)"
        val = (count, var)
        mycursor.execute(sql, val)
        mydb.commit()
        cv2.waitKey()
    print("--------SUCCESS TEST NORMAL 20%----------")
    i = 0
    count = 0
    print("--------WAIT TRAIN GLOUCOMA 80%----------")
    for imagetrainglaucoma in imagePathTrain: 
        i = int(i)+1
        image = cv2.imread(imagetrainglaucoma)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ##greyimage [0,0]
        kernel = np.ones((5, 5), np.uint8)
        image = cv2.erode(grey, kernel)
        ist,bins = np.histogram(image.ravel(),256,[0,256]) 
        m = np.mean(ist) 
        var = ((m-ist)**2).mean()  
        var = round(var)   
        var = str(var)
        type = "GLAUCOMA"
        count = count+1
        sql = "INSERT INTO datapicture (name, mean_images, type) VALUES (%s, %s, %s)"
        val = (count, var, type)
        mycursor.execute(sql, val)
        mydb.commit()
        cv2.waitKey()
    print("--------SUCCESS TRAIN GLOUCOMA 80%----------")
def my_function2():                                         #113-132 เป็นการรับข้อมูลจาก database มาแสดงผล
    mycursor.execute("SELECT * FROM test_img_nomal")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    print("-----------------------------------------------")
    mycursor.execute("SELECT * FROM test_image_glaucoma")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    print("-----------------------------------------------")
    mycursor.execute("SELECT * FROM datapicture")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    print("-----------------------------------------------")
    mycursor.execute("SELECT * FROM datapicture_normal")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def my_function3():                 # ทดสอบรูปภาพของชุด test ตาต้อหินจำนวน 79 รูป
    mycursor.execute("SELECT mean_test FROM test_image_glaucoma")  #134-140 รับข้อมูลจาก database แล้วมาเก็บค่าไว้ในตัวแปร data_test[]
    result_test = mycursor.fetchall()
    data_test = []
    for a in result_test: 
        datatest = a[0]
        cvt_test = int(datatest)
        data_test.append(cvt_test)
        
    mycursor.execute("SELECT mean_images FROM datapicture")  #142-143เป็นการรับข้อมูลชุด train ตาต้อหิน 317 รูปมาเก็บค่าไว้ใน result
    myresult = mycursor.fetchall()
    i = 0                          #144-145 กำหนดให้ค่า i , j =0 เพื่อนำไปใช้งานใน loop
    j = 0
    data = []               #ใช้ในการเก็บค่าความแปรปรวนของรูปภาพ train ตาต้อหิน 
    data_train = []         #ใช้ในการเก็บค่าความแปรปวรของทุกรูปภาพใน train ตาต้อหิน 317 รูป
    sumtest = []            #ใช้ในการเก็บค่ารูปภาพแต่ละรูปของ test ตาต้อหิน - train ตาต้อหิน 317 รูป
    summin_glaucoma = []    #ใช้ในการเก็บค่าที่น้อยที่สุดของแต่ละรูปภาพที่ได้ทำการลบกัน
    for x in myresult:      #   x วนลูปรับข้อมูลจาก myresult -> train ตาต้อหิน ทีละรูป
        data = x[0]         # เก็บค่า x[0] ไว้ใน data
        cvt = int(data)     # แปลงค่าเป็น int แล้วเก็บไว้ใน cvt
        data_train.append(cvt)     #นำข้อมูลบันทึกลงในตัวแปร data_train
    for x in data_test:     #x วนลูปรับข้อมูลจาก myresult -> test ตาต้อหิน ทีละรูป
        if i <=79:          #ถ้าค่า i ยังน้อยกว่าหรือเท่ากับ 79 ให้ทำใน if ต่อไป (เพราะรูปภาพทดสอบตาต้อหินมี 79 รูป)
            if j <=317:     #ถ้าค่า j น้อยกว่าหรือเท่ากับ 317 ให้ทำใน if ต่อไป (เพราะรูปภาพ train ตาต้อหินมี 317 รูป)
                for z in myresult:     # z รับค่าความแปรปรวนของ train ตาต้อหิน ทีละรูปจนครบ 317 รูป
                    sum = abs(data_test[i]-data_train[j])  #นำความแปรปรวนของรูปภาพแรกของ test ตาต้อหิน - train ตาต้อหินทั้ง 317 รูปตามลำดับ
                    sumtest.append(sum)  #เก็บค่าที่ลบกันได้ไว้ใน sumtest[] สรุปคือรูปที่ 1 - ทั้งหมด317 รูป จะมีค่าที่ลบแล้ว 317 ชุด['100','150',...]
                    j = j+1   #ให้ค่า j +1 เพื่อที่จะได้ทำให้ครบทั้งหมด 317 รูป 
            summin = min(sumtest) #นำชุดข้อมูลของ test ตาต้อหิน ที่ลบกันแล้วกับ train ตาต้อหิน มาหาค่าที่น้อยที่สุด ['100','150','250']--> 100
            summin_glaucoma.append(summin) #ทำการเก็บค่าที่น้อยที่สุดของแต่ละรูปไว้ในตัวแปร (ตอนนี้จะเหลือข้อมูล 79 ชุด)
            sumtest = []
            i = i+1
            j = 0
        else:
            print("no data")

    mycursor.execute("SELECT mean_img_normal FROM datapicture_normal") #169-196 ทำเหมือนกันแต่เปลี่ยนชุดข้อมูลจาก train ตาต้อหิน เป็น train ตาปรกติ
    myresult_tain_normal = mycursor.fetchall()
    i = 0
    j = 0
    data = []
    data_train = []
    sumtest = []
    summin_normal = []
    for x in myresult_tain_normal:
        data = x[0]
        cvt = int(data)
        data_train.append(cvt)
    for x in data_test:
        if i <=79:
            if j <=247:
                for z in myresult_tain_normal:
                    sum = abs(data_test[i]-data_train[j])
                    sumtest.append(sum)
                    j = j+1
            
            summin = min(sumtest)
            summin_normal.append(summin)
            sumtest = []
            i = i+1
            j = 0
        else:
            print("no data")
    
    count_normal = 0        #กำหนดค่าไว้สำหรับนับจำนวน
    count_glaucoma = 0      #กำหนดค่าไว้สำหรับนับจำนวน
    for d,c in zip(summin_normal, summin_glaucoma): #d = ค่าที่น้อยที่สุดของทุกรูปของชุดข้อมูลที่ลบกับตาปรกติและตาต้อหิน(จะมี 79+79 ค่า)
        if d < c:  #ถ้า d น้อยกว่า c แสดงว่าค่าความแปรปรวนมีความใกล้เคียงกับรูปภาพธรรมดามากกว่า(ex ตาธรรมดาที่ลบได้ 100 : ตาต้อหินที่ลบได้ 120 --> ภาพนี้เป็นตาปรกติเพราะข้อมูลอยู่ใกล้ข้อมูลตาปรกติมากกว่า)
            count_normal = count_normal + 1  #นับจำนวนครั้งไว้
        elif d > c: #เหมือนกับข้างบนแต่ ถ้า d มากกว่า c รูปภาพมีความแปรปวรนห่างจากรูปภาพตาปรกติมากกว่า => แสดงว่าเป็นรูปภาพตาต้อหิน
            count_glaucoma = count_glaucoma + 1   #นับจำนวนครั้งไว้
        else:
            print("GLAUCOMA IMAGES REPEAT")       #ถ้าเกิดข้อมูลผิดผลาดหรือซ้ำกัน
    global winrate_glaucoma
    winrate2 = ((count_glaucoma)/79)*100 #test ตาต้อหินมี 79 รูปเลยใช้ 79
    winrate2 = round(winrate2, 2)              #208-212 เป็นการแสดงผลลัพธ์
    winrate_glaucoma = str(winrate2)
    print("EYE NORMAL",count_normal)
    print("EYE GLAUCOMA",count_glaucoma)
    print("ความแม่นยำ "+" "+str(winrate2)+" %")

def my_function4():                 #214-294 ทำเหมือนกับก่อนหน้าแต่เปลี่ยนจาก test ตาต้อหิน 79 รูป เป็น-> test ตาปรกติ 62 รูป
    mycursor.execute("SELECT mean_test_normal FROM test_img_nomal")
    result_test = mycursor.fetchall()
    data_test = []
    for a in result_test:
        datatest = a[0]
        cvt_test = int(datatest)
        data_test.append(cvt_test)
        
    mycursor.execute("SELECT mean_images FROM datapicture")
    myresult = mycursor.fetchall()
    i = 0
    j = 0
    data = []
    data_train = []
    sumtest = []
    summin_glaucoma = []
    for x in myresult:
        data = x[0]
        cvt = int(data)
        data_train.append(cvt)
    for x in data_test:
        if i <=62:
            if j <=317:
                for z in myresult:
                    sum = abs(data_test[i]-data_train[j])
                    sumtest.append(sum)
                    j = j+1
            summin = min(sumtest)
            summin_glaucoma.append(summin)
            sumtest = []
            i = i+1
            j = 0
        else:
            print("no data")

    mycursor.execute("SELECT mean_img_normal FROM datapicture_normal")
    myresult_tain_normal = mycursor.fetchall()
    summary_normal = []
    i = 0
    j = 0
    datatest_sumtest = []
    data = []
    data_train = []
    sumtest = []
    summin_normal = []
    for x in myresult_tain_normal:
        data = x[0]
        cvt = int(data)
        data_train.append(cvt)
    for x in data_test:
        if i <=62:
            if j <=247:
                for z in myresult_tain_normal:
                    sum = abs(data_test[i]-data_train[j])
                    sumtest.append(sum)
                    j = j+1
            summin = min(sumtest)
            summin_normal.append(summin)
            sumtest = []
            i = i+1
            j = 0
        else:
            print("no data")
    count_normal = 0
    count_glaucoma = 0
    for d,c in zip(summin_normal, summin_glaucoma):
        if d < c:
            count_normal = count_normal + 1
        elif d > c:
            count_glaucoma = count_glaucoma + 1 
        else:
            print("NODATA")

    global winrate_normal
    winrate1 =  (count_normal/62)*100
    winrate1 = round(winrate1, 2)
    winrate_normal = str(winrate1)
    print("EYE NORMAL",count_normal)
    print("EYE GLAUCOMA",count_glaucoma)
    print("ความแม่นยำ"+" "+str(winrate1)+" %") 
    
def my_function5():
    heading = "DATA_GLAUCOMA"
    heading2 = "DATA_NORMAL"
    table_data = [
    ["Number", heading, heading2, "Type_test", "ACCURENCY"],
    ['0','317(images)', '247(images)', 'GLAUCOMA(79images)', winrate_glaucoma+" %"],
    ['1','317(images)', '247(images)', 'NORMAL(62images)',winrate_normal+" %"]
    ]
    table = AsciiTable(table_data)
    print(table.table)
    
def my_function6():
    print("----------CLEAR DATABASE----------")
    sql = "DELETE FROM test_image_glaucoma WHERE name"
    sql2 = "DELETE FROM datapicture_normal WHERE name"
    sql3 = "DELETE FROM datapicture WHERE name"
    sql4 = "DELETE FROM test_img_nomal WHERE name"
    mycursor.execute(sql)
    mycursor.execute(sql2)
    mycursor.execute(sql3)
    mycursor.execute(sql4)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")

number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
while number != "0":
    try:
        if number == "1":
            my_function()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
        elif number == "2":
            my_function2()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
        elif number == "3":
            my_function3()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
        elif number == "4":
            my_function4()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
        elif number == "5":
            my_function5()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
        elif number == "6":
            my_function6()
            number = input("CHOOSE 1(SAVE DATA) OR 2(SHOW DATA) OR 3(CHECKTYPE_TESTGLOUCOMA) OR 4(CHECKTYPE_TESTNORMAL) OR 5(SHOW WINRATE) OR 6(CLEAR DATABASE): ")
    except:
        number="0"

cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1)
