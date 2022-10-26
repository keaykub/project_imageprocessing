from datetime import time
from random import Random, random
from imutils import paths
import cv2
import numpy as np
import mysql.connector
from terminaltables import AsciiTable
##config window display

#connect database
mydb = mysql.connector.connect(
    host="localhost",
    username = "root",
    password="",
    database="dataeye"
    )
mycursor = mydb.cursor()

test_image_glaucoma = [] 
winrate_normal = ""
winrate_glaucoma =""
def my_function():
    imagePathTrain = list(paths.list_images(r"D:\project-Imageprocess\dataset 1\Glaucoma")) #train 80% ตาต้อ
    imagePathTrain_Normal = list(paths.list_images(r"D:\project-Imageprocess\dataset 1\Normal")) #train 80% ปรกติ 
    imagePathTest = list(paths.list_images(r"D:\project-Imageprocess\TEST_GLAUCOMA"))    #test 20 ตาต้อ 
    imagePathTest_Normal = list(paths.list_images(r"D:\project-Imageprocess\TEST_NORMAL"))  #test 20% ตาปรกติ 
    i = 0
    count = 0
    print("--------WAIT TRAIN NORMAL 80%----------")
    for imagetrain in imagePathTrain_Normal:  
        i = int(i)+1
        image = cv2.imread(imagetrain)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ##greyimage
        kernel = np.ones((5, 5), np.uint8)
        image = cv2.erode(grey, kernel)
        ist,bins = np.histogram(image.ravel(),256,[0,256]) 
        m = np.mean(ist) 
        var = ((m-ist)**2).mean() # ความแปร
        var = round(var)  #100.158665221545 100
        var = str(var)
        type = "NORMAL"
        count = count+1
        sql = "INSERT INTO datapicture_normal (name, mean_img_normal , type_normal) VALUES (%s, %s, %s)"
        val = (count, var, type)
        mycursor.execute(sql, val)
        mydb.commit()
        cv2.waitKey()
    print("--------SUCCESS TRAIN NORMAL 80%----------")
    
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
def my_function2():
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
def my_function3():   #ทดสอบรูปภาพชุดของตาต้อหิน
    mycursor.execute("SELECT mean_test FROM test_image_glaucoma")
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
        if i <=79:
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
    
    count_normal = 0
    count_glaucoma = 0
    for d,c in zip(summin_normal, summin_glaucoma):
        if d < c:
            count_normal = count_normal + 1
        elif d > c:
            count_glaucoma = count_glaucoma + 1
        else:
            print("GLAUCOMA IMAGES REPEAT")       
    global winrate_glaucoma
    winrate2 = ((count_glaucoma)/79)*100 
    winrate2 = round(winrate2, 2)
    winrate_glaucoma = str(winrate2)
    print("EYE NORMAL",count_normal)
    print("EYE GLAUCOMA",count_glaucoma)
    print("ความแม่นยำ "+" "+str(winrate2)+" %")

def my_function4():                 ##test_normal 20%
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



