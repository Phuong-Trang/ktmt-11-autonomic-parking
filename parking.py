import cv2
import imutils
import numpy as np
import time
import easyocr
from PIL import Image, ImageDraw , ImageFont
from datetime import datetime
from dis import dis

def Read_Image(path_image):
    try:
        img = cv2.imread(path_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #loc va tim canh
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection
        # bao vien doi tuong
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        count_number_word = len(result)
        if count_number_word != 1:
            final_result = str(result[0][1])+" - "+str(result[1][1])
        else:
            final_result = str(result[0][1])
    except:
        final_result = "ERROR"
    final_result  = final_result.replace("\'","")
    return final_result




#thuc hien chup lai bien so xe de xu li
#sua lai ham nay########################################
# def capture():
#     cam  = cv2.VideoCapture(0)
#     result, image = cam.read()
#     cv2.imwrite(luu_anh+"biensoxe.jpg", image)
    # cv2.imshow("Anh chup camera",image)           
    # cv2.waitKey()
    # cv2.destroyWindow("Anh chup camera")

#trong truong hop qua size xe thi khong cho xe vao nua
#kiem tra xe di vao va di ra co trung bien so hay khong
#tinh thoi gian do xe, thu phi
arr=[] #[[bienso1,ngayguixe1,gioguixe1],[bienso2,ngayguixe2,gioguixe2],...]
def quanlixe(path):
    while True:
        #kiem tra xe di vao tram (neu co xe thi chup anh) an PHIM I va ENTER
            # capture()
        bienso = Read_Image(path)
        if bienso == "ERROR":
            print("Chua xac nhan duoc bien so xe, chup lai!")
            break
        else:
            print(bienso)
            break
        
#kiem tra bien so xe co nam trong co so du lieu khong
#neu co thi la xe di ra, tinh phi, tra ve True
#neu khong thi tra ve False
def kiemtra(bienso):
    for i in range(len(arr)):
        #xe di ra
        if arr[i][0] == bienso:
            #kiem tra thoi gian, tinh phi theo khung thoi gian 7h-19h la 5000, 19h-7h la 10000
            #hien thi ra man hinh glcd
            #neu thoi gian gui xe trong ngay thi tinh phi nhu tren
            #neu thoi gian gui xe qua 1 ngay thi phat 20000/ngay
            print("Xe di ra:",bienso)
            ngayhientai= (datetime.now().strftime("%d/%m/%Y")).split("/")
            ngayguixe=arr[i][1].split("/")
            giohientai = (datetime.now().strftime("%H:%M:%S")).split(":")
            gioguixe=arr[i][2].split(":")
            phi = 0
            if (ngayhientai[0] == ngayguixe[0] and ngayhientai[1] == ngayguixe[1] and ngayhientai[2] == ngayguixe[2]):
                if int(giohientai[0]) > 7 and int(giohientai[0]) < 19:
                    phi = 5000
                else:
                    phi = 10000
            else:
                phi = 20000*(abs(int(ngayguixe[0]) - int(ngayhientai[0])) + 30*abs(int(ngayguixe[1]) - int(ngayhientai[1])) + 365*abs(int(ngayguixe[2]) - int(ngayhientai[2])))
            print("Ban phai nop phi gui xe:",phi)
            #loai bo khoi hang doi
            arr.pop(i)
            return True
    #xe di vao
    return False



# try:
#     # path="C:\\Users\\ADMIN\\eclipse-workspace\\KTMT\\QUANLIDOXE\\"
#     # name_image='bien1.jpg'
#     # lay_bien_so(path+name_image)
#     quanlixe("C:\\0_HUS\\402_KTMT\\YOLO_train\\1.jpg")
# except KeyboardInterrupt:
#     print("chuong trinh da thoat!")