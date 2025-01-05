import cv2
import numpy as np
import face_recognition
import mysql.connector
from mysql.connector import Error
import threading
from datetime import datetime

#데이터베이스를 위한 쓰레드처리
def worker():
    try:
        raise ValueError("예외 테스트")
    except Exception as e:
        print(f"쓰레드 내부 예외 처리: {e}")
        
thread = threading.Thread(target=worker)
thread.start()
thread.join()

#데이터베이스 연결
def init_db():
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='1234',  db='face',  charset='utf8',auth_plugin="mysql_native_password")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS time (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, name char(30) NOT NULL, timestamp TIMESTAMP NOT NULL)")
    conn.commit()
    conn.close()

last_recognition = {} #최근에 인식된 얼굴 기록(전역변수)
    
#데이터베이스 저장
def log_recognition(name):
    global last_recognition #전역변수
    current_time = datetime.now()

    if name == "Unknown": #이름 없으면 저장 x
        return 

    if name in last_recognition: #최근에 인식된 시간 확인
        time_difference = (current_time - last_recognition[name]).total_seconds()
        if time_difference <10: #동일 얼굴이 10초 이내에 다시 인식되면 기록x
            return 

    try:
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='1234',  db='face', auth_plugin="mysql_native_password")
        if conn.is_connected():
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #현재시간
            query = "INSERT INTO time (name, timestamp) VALUES (%s, %s)"
            cursor.execute(query, (name, timestamp))
            conn.commit() #변경사항 저장
            print(f"로그 저장 성공:  {name} at {timestamp}")
            last_recognition[name] = current_time
    except mysql.connector.Error as e:
        print(f"데이터베이스 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

#데이터셋에 저장된 파일 읽기 
def load_encoded_faces():
    try:
        data = np.load("face_recognizer.npy", allow_pickle=True).item()
        return data["encodings"], data["names"]
    except FileNotFoundError:
        print("face_recognizer.npy 파일이 존재하지 않습니다. 얼굴 데이터를 먼저 학습하세요.")
        exit()

# 실시간 얼굴 인식
def recognize_faces():
    known_face_encodings, known_face_names = load_encoded_faces()
    cap = cv2.VideoCapture(0)
    print("실시간 얼굴 인식을 시작합니다. 'ESC'를 눌러 종료하세요.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라 접근에 실패했습니다.")
            break
        
        # 얼굴 탐지 및 인식
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # 속도 향상을 위해 크기 축소
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # 신뢰도가 가장 높은 사용자 선택
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin() if len(face_distances) > 0 else None
            
            name = "Unknown" #혹시 몰라서 초기값 설정
            confidence = None

            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if face_distances[best_match_index]<0.3:
                    name = known_face_names[best_match_index]
                    confidence = round((1 - face_distances[best_match_index])* 100,2)
                    log_recognition(name)

            # 얼굴 위치 및 이름 표시
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            label = f"{name} ({confidence:.2f}%)" if confidence else name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow("Real-Time Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == 27: #esc 아스키코드 값
            break
    
    cap.release()
    cv2.destroyAllWindows()

# 호출
if __name__ == "__main__":
    init_db()
    recognize_faces()

