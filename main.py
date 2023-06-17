import threading

import cv2 ### Opencv
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Defenimos um objeto do tipo câmera

# Dimensões
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0 # Vamos querer ter uma variável para controlar os frames em que vamos testar, não vamos querer estar a testar constantemente 

face_match = False # Booleana

reference_img = cv2.imread("reference.jpg") # Imagem que irá servir de referência

def check_face(frame): # Função que analisa e avalia se a fotografia e o frame têm a mesma cara neles
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']: # Aqui é feita a análise da Foto com o frame retirado na web cam
            face_match = True
        else :
            face_match = False
    except ValueError:
        face_match = False 

# ret -> Return value
while True :
    ret, frame = cap.read() # Dá return de dois itens
    

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face(frame), args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match: # Caso haja match
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3) 
        else: # Caso não haja match
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            
        cv2.imshow("video",frame) # Mostra o resultado depois de add o Text


    key = cv2.waitKey(1) # Para que seja capaz de processar User Input
    if key == ord("q"): # Se pressionar "q" saímos do loop
        break
    
cv2.destroyAllWindows()
      
