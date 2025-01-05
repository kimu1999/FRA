import cv2
import os
import numpy as np
import face_recognition
import tkinter as tk 
from tkinter import simpledialog

# 1. 얼굴 데이터 저장 경로 설정
DATASET_PATH = "dataset"
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

# 2. 얼굴 탐지 모델 로그
def collect_face_data(user_name):
    user_path = os.path.join(DATASET_PATH, user_name)
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    
    cap = cv2.VideoCapture(0)
    print("얼굴 데이터를 수집 중입니다. 'ESC'를 눌러 종료하세요.")
    
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        for (top, right, bottom, left) in face_locations:
            count += 1
            face_image = frame[top:bottom, left:right]
            face_resized = cv2.resize(face_image, (150, 150))  # 얼굴 크기를 고정
            face_path = os.path.join(user_path, f"{count}.jpg")
            cv2.imwrite(face_path, face_resized)
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        
        cv2.imshow("Face Data Collection", frame)
        if cv2.waitKey(1) & 0xFF == 27 or count >= 200:  # 200장 저장 후 종료
            break
    
    cap.release()
    cv2.destroyAllWindows()

def train_model():
    known_face_encodings = []
    known_face_names = []
    
    # 데이터셋에서 얼굴 데이터 읽기
    user_dirs = os.listdir(DATASET_PATH)
    for user_name in user_dirs:
        user_path = os.path.join(DATASET_PATH, user_name)
        if os.path.isdir(user_path): #디렉토리 확인
            for image_name in os.listdir(user_path):
                image_path = os.path.join(user_path, image_name)
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encoding = face_recognition.face_encodings(image)[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(user_name)
                except IndexError:
                    print(f"얼굴 인코딩 실패: {image_path}")

    #얼굴 인코딩과 이름을 저장                
    if known_face_encodings and known_face_names:
        if os.path.exists("face_recognizer.npy"):
            existing_data = np.load("face_recognizer.npy", allow_pickle=True).item()
            known_face_encodings.extend(existing_data["encodings"])
            known_face_names.extend(existing_data["names"])

        data = {"encodings": known_face_encodings, "names": known_face_names}
        np.save("face_recognizer.npy", data)
        print("모델이 성공적으로 학습되고 저장되었습니다!")
    else:
        print("학습할 데이터가 없습니다.")

#사용자 입력을 윈도우 창으로 받기
def get_user_name():
    root = tk.Tk()
    root.withdraw()
    user_name = simpledialog.askstring("이름 입력", "이름을 입력하세요: ")
    return user_name

# 사용자 입력 받아 얼굴 데이터 수집 및 학습 실행
if __name__ == "__main__":
    user_name = get_user_name()
    if user_name:
        collect_face_data(user_name)
        train_model()
    else:
        print("이름을 입력하지 않았습니다.")
