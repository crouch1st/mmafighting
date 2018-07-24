import os
import cv2

image = os.path.join(os.getcwd(), "pngs", "logo.png")
new_img = os.path.join(os.getcwd(), "pngs", "small_logo.png")

img = cv2.imread(image)
cv2.imshow("ORIGINAL", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

res = cv2.resize(img,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
cv2.imshow("RESCALED", res)
cv2.imwrite(new_img, res)
cv2.waitKey(0)
cv2.destroyAllWindows()
