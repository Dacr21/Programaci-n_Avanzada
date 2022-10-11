#%%
import cv2

img1 = cv2.imread('img\\img3.jpg', cv2.IMREAD_COLOR)
print("Size img1: ", img1.shape)

img2 = cv2.imread('img\\img4.jpg', cv2.IMREAD_COLOR)
img2 = cv2.resize(img2,(img1.shape[1], img1.shape[0]))
print("Size img2: ", img2.shape)

img_photo = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
cv2.imshow("Imagen", img_photo)

cv2.waitKey(0)
cv2.destroyAllWindows()
#%%
import cv2
import numpy as np

def foo(event):

  pass

img = cv2.imread("img\\people_green_bg.jpg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, foo)   # 49
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, foo)  # 64
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, foo)   # 36
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, foo)  # 255
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, foo)   # 92
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, foo)  # 255

while True:
  h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
  h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
  s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
  s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
  v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
  v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
  lower_bound = np.array([h_min, s_min, v_min])
  upper_bound = np.array([h_max, s_max, v_max])
  mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
  img_result = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))
  cv2.imshow("Image", img)

  #cv2.imshow("Image HSV", img_hsv)

  #cv2.imshow("Mask", mask)

  cv2.imshow("Image Result", img_result)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cv2.destroyAllWindows()
#%%
#Detector de colores
import cv2
import numpy as np

kernel_open = np.ones((5,5))
kernel_close = np.ones((80,80))
cap = cv2.VideoCapture(0)

while True:
  ret, frame = cap.read()
  img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  mask1 = cv2.inRange(img_hsv,(0,50,20),(5,255,255))
  mask2 = cv2.inRange(img_hsv,(175,50,20),(180,255,255))
  mask = cv2.bitwise_or(mask1,mask2)
  #Eliminar ruido
  mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
  #Elimina manchas negras
  mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)
  mask_final = mask_close

  conts,h = cv2.findContours(mask_final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
  #cv2.drawContours(frame, conts, -1, (255,0,0), 2)
  for i in range(len(conts)):
      x,y,w,h = cv2.boundingRect(conts[i])
      cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
      cv2.putText(frame,"Polo", (x,y-12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

  #cv2.imshow("Mask", mask_final)
  cv2.imshow("Frame", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

#%%
#DETECCION DE ROSTRO
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # patron de escala, cantidad de pixeles adyasentes dentro del patron
  faces = face_cascade.detectMultiScale(gray, 1.2, 5)

  for x,y,w,h in faces:
      cv2.rectangle(frame, (x,y), (w+x,h+y), (255,0,0),2)

  cv2.imshow("Cam",frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

#%%
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv2.imread("img\\img8.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.2, 5)

for x,y,w,h in faces:
  cv2.rectangle(img, (x,y), (w+x,h+y), (255,0,0), 2)

cv2.imshow("Image",img)

cv2.waitKey(0)
cv2.destroyAllWindows()