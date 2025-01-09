FRA (Face-Recognition-Attendance)
얼굴 인식 출결 시스템 

프로젝트 개요
1. 배경
 - 기존 국비 수업의 출결 시스템이 어플을 설치하여 QR, 비콘, WIFI 3가지로 구성
 - 본 학원은 QR코드 출석 체크 시스템, 입실 및 퇴실 QR을 안찍으면 담당자가 출결을 등록해야되는 불편함이 존재
 - QR은 해당 학원 위치에서 반경 1KM내에 있으면 언제든지 출석체크가 된다는 에러가 발생
 - 따라서 대리 출석 또한 안되고 카메라가 설치되어 있다면 정해진 시간 내 자동 출결이 되는 시스템을 구현하고자 함
 - 파이썬과 OpenCV를 활용하여 출결시스템을 진행

2. H/W
 - 노트북 OR 컴퓨터
 - 웹 카메라

3. S/W 
 - OS : Window 10 or 11
 - IDE : Visual Studio Code
 - Language : Python
 - Library : OpenCV & Face_recognition
 - DataBase : Mysql
 - PaltForm : Tkinter

주요 기능 
1. Main.py Process & GUI 
   - 메인 페이지 

2. student.py Process & GUI 
   - 학생 정보 등록 및 관리 

3. face_test.py Process & GUI 
   - 얼굴 인식 테스트 하며, 인식하면 attendance.py로 정보 제공

4. face_registration.py Process & GUI
   - 학생들의 얼굴을 등록

5. attendance.py Process & GUI 
   - 얼굴이 인식된 학생의 이름과 시간을 제공


아쉬운 점 
 - 학원 건물이 공공기관이라 네트워크 환경이 폐쇄적인 점
 - 라즈베리파이에 포트포워딩을 이용하여 팀원들 각자 집에서 접근해 프로젝트를 진행할려고 했지만 못한 점
 - 학생등록 DB와 출결관리 DB가 서로 연동을 못 시킨 점(*학생등록은 DB에 저장, 얼굴등록은 .npy파일에 dataset에 폴더명으로 저장)


 

