import os
import cv2
import qrcode
from PIL import Image
from datetime import date

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
qr_code_dir = os.path.join(parent_dir, "Created_QR_Codes")

class QR():
    
    # make qr code for the newly added participant
    def maker(self,convert):
        qr = qrcode.QRCode(version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_H,
                    box_size = 25, border = 4)
        
        qr.add_data(convert)
        qr.make(fit = True)

        image = qr.make_image(fill_color = "black", back_color = 'white')
        for_name = convert.split(',')
        name = for_name[0]+'-'+for_name[1]+'-'+for_name[2]+".png"
        image.save(os.path.join(qr_code_dir, name))
        
    # scanner to scan qr code for admin work
    def scanner(self,):
        print("Please wait while we open scanner to scan code.")

        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        a = None

        while True:
            
            _, img = cap.read()
            data, one, _ = detector.detectAndDecode(img)

            if data:
                a = data
                break

            cv2.imshow("Show your QR-Code to mark attendance.", img)

            if cv2.waitKey(1) == ord('q'):
                break


        try:
            cap.release(a)
        except Exception:
            cv2.destroyAllWindows()
        
        return a