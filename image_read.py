import cv2
import colour_utils



img = cv2.imread(".\images\Screenshot 2022-09-22 191246.png")
img = cv2.imread(".\images\Screenshot 2022-09-22 191041.png")
h,w = img.shape[:2]
y= 400
x= 400
y_o = -100
x_o = 50
crop_img = img[int((w-y)/2)+y_o:int((w+y)/2)+y_o, int((h-x)/2)+x_o:int((h+x)/2)+x_o]
cv2.imwrite("./crop.png", crop_img)
print(colour_utils.get_colour(3, crop_img))
