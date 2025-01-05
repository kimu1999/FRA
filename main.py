import tkinter as tk
import subprocess
from datetime import datetime, time
from tkinter import messagebox

# 전역 변수
time_limits = {
    "출석 체크 (입실)": None,
    "출석 체크 (퇴실)": None,
    "지각/조퇴/외출": None,
}

# 창 생성
window = tk.Tk()
window.title("Face Recognition Attendance System")  # 창 제목
window.geometry("450x500")  # 창 크기 (너비 x 높이)

# 라벨 추가
label = tk.Label(window, text="FRA System", font=("Arial", 16))
label.pack(pady=10)

# 버튼 클릭 시 다른 파일 실행
def run_other1_script():
    subprocess.run(["python", "face_test.py"])

def run_other2_script():
    subprocess.run(["python", "face_test.py"])

def run_other3_script():
    subprocess.run(["python", "student.py"])

def run_other4_script():
    subprocess.run(["python", "face_registration.py"])

def run_other5_script():
    subprocess.run(["python", "attendance.py"])


# 시간 설정 함수
def set_time_window(label):
    def save_time():
        try:
            if label == "지각/조퇴/외출":
                # 지각/조퇴/외출 시간 설정
                start_time = datetime.strptime(start_time_entry.get(), "%H:%M").time()
                end_time = datetime.strptime(end_time_entry.get(), "%H:%M").time()
                time_limits[label] = (start_time, end_time)
                messagebox.showinfo("설정 완료", f"{label} 시간: {start_time} - {end_time}")
            else:
                # 입실 시간 설정
                start_entry = datetime.strptime(start_time_entry.get(), "%H:%M").time()
                end_entry = datetime.strptime(end_time_entry.get(), "%H:%M").time()
                # 퇴실 시간 설정
                start_exit = datetime.strptime(start_exit_time_entry.get(), "%H:%M").time()
                end_exit = datetime.strptime(end_exit_time_entry.get(), "%H:%M").time()
                time_limits[f"{label} (입실)"] = (start_entry, end_entry)
                time_limits[f"{label} (퇴실)"] = (start_exit, end_exit)
                messagebox.showinfo("설정 완료", f"{label} 입실 시간: {start_entry} - {end_entry}\n퇴실: {start_exit} - {end_exit}")
            
            time_window.destroy()
        except ValueError:
            messagebox.showerror("입력 오류", "시간 형식은 HH:MM이어야 합니다.")

    time_window = tk.Toplevel()
    time_window.title(f"{label} 시간 설정")

    if label == "지각/조퇴/외출":
        # 지각/조퇴/외출 시간 설정
        tk.Label(time_window, text="시작 시간 (HH:MM):").pack(pady=5)
        start_time_entry = tk.Entry(time_window)
        start_time_entry.pack(pady=5)

        tk.Label(time_window, text="종료 시간 (HH:MM):").pack(pady=5)
        end_time_entry = tk.Entry(time_window)
        end_time_entry.pack(pady=5)
    else:
        # 입실 시간 설정
        tk.Label(time_window, text="입실 시작 시간 (HH:MM):").pack(pady=5)
        start_time_entry = tk.Entry(time_window)
        start_time_entry.pack(pady=5)

        tk.Label(time_window, text="입실 종료 시간 (HH:MM):").pack(pady=5)
        end_time_entry = tk.Entry(time_window)
        end_time_entry.pack(pady=5)

        # 퇴실 시간 설정
        tk.Label(time_window, text="퇴실 시작 시간 (HH:MM):").pack(pady=5)
        start_exit_time_entry = tk.Entry(time_window)
        start_exit_time_entry.pack(pady=5)

        tk.Label(time_window, text="퇴실 종료 시간 (HH:MM):").pack(pady=5)
        end_exit_time_entry = tk.Entry(time_window)
        end_exit_time_entry.pack(pady=5)

    tk.Button(time_window, text="저장", command=save_time).pack(pady=10)


# 버튼 활성화 상태 업데이트 함수
def update_button_states():
    current_time = datetime.now().time()
    for label, time_limit in time_limits.items():
        if time_limit:
            start, end = time_limit
            if start <= current_time <= end:
                buttons[label].config(state=tk.NORMAL)
            else:
                buttons[label].config(state=tk.DISABLED)
        else:
            buttons[label].config(state=tk.DISABLED)
    window.after(1000, update_button_states)  # 1초마다 업데이트

# 메뉴 생성 함수
def create_menu():
    menubar = tk.Menu(window)

    # 학생 관리 메뉴
    student_menu = tk.Menu(menubar, tearoff=0)
    student_menu.add_command(label="학생 등록", command=run_other3_script)
    student_menu.add_command(label="얼굴 등록", command=run_other4_script)
    menubar.add_cascade(label="학생 관리", menu=student_menu)

    # 시간 등록 메뉴
    time_menu = tk.Menu(menubar, tearoff=0)
    time_menu.add_command(label="출석 체크 시간 설정", command=lambda: set_time_window("출석 체크"))
    time_menu.add_command(label="지각/조퇴/외출 시간 설정", command=lambda: set_time_window("지각/조퇴/외출"))
    menubar.add_cascade(label="시간 설정", menu=time_menu)

    # 창 메뉴 설정
    window.config(menu=menubar)

# 메뉴바 생성
create_menu()

# 버튼 추가
buttons = {
    "출석 체크 (입실)": tk.Button(window, text="출석 체크 : 입실", command=run_other1_script, width=50, height=5),
    "출석 체크 (퇴실)": tk.Button(window, text="출석 체크 : 퇴실", command=run_other1_script, width=50, height=5),
    "지각/조퇴/외출": tk.Button(window, text="지각/조퇴/외출", command=run_other2_script, width=50, height=5),
    "출석 관리": tk.Button(window, text="출석 관리", command=run_other5_script, width=50, height=5)
}

# 버튼 배치
for btn in buttons.values():
    btn.pack(pady=10)

# 초기 상태 업데이트
update_button_states()

# 이벤트 루프 실행
window.mainloop()
