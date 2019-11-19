from LSBSteg import *
import cv2


for x in range(1, 1501):
    gmbrasl = "C:\\Users\\user pc\\Desktop\\dataset\\learn dataset\\"+str(x)+".bmp"
    steg = LSBSteg(cv2.imread(gmbrasl))
    img_encoded = steg.encode_text("password")
    statement = "C:\\Users\\user pc\\Desktop\\stega\\new learn dataset stega\\"+str(x)+".bmp"
    cv2.imwrite(statement, img_encoded)

