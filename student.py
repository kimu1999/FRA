import tkinter as tk
from tkinter import messagebox, Label, Entry
import subprocess #다른 파일 실행
import mysql.connector
import threading

def worker():
    try:
        raise ValueError("예외 테스트")
    except Exception as e:
        print(f"쓰레드 내부 예외 처리: {e}")
        
thread = threading.Thread(target=worker)
thread.start()
thread.join()

def init_db():
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='1234',  db='face',  charset='utf8',auth_plugin="mysql_native_password")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS student (userName char(15), birthYear INT, phoneNumber char(20))")
    conn.commit()
    conn.close()

def save_to_db(user_name, birth_year, phone_number):
    try:
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='1234',  db='face',  charset='utf8',auth_plugin="mysql_native_password")
        cur = conn.cursor()
        cur.execute("INSERT INTO student (userName, birthYear, phoneNumber) VALUES (%s, %s, %s)", (user_name, birth_year, phone_number))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def save_button_clicked():
    """저장 버튼 클릭 시 실행"""
    user_name = entry1.get()
    birth_year = entry2.get()
    phone_number = entry3.get()

    if user_name.strip() and birth_year.strip() and phone_number.strip():
        try:
            birth_year = int(birth_year)  # 생년월일은 숫자로 변환
            success = save_to_db(user_name, birth_year, phone_number)
            if success:
                messagebox.showinfo("성공", "값이 성공적으로 저장되었습니다!")
                entry1.delete(0, tk.END)
                entry2.delete(0, tk.END)
                entry3.delete(0, tk.END)
            else:
                messagebox.showerror("오류", "값을 저장하는 중 오류가 발생했습니다.")
        except ValueError:
            messagebox.showerror("오류", "생년월일은 숫자로 입력해야 합니다.")
    else:
        messagebox.showwarning("경고", "모든 값을 입력하세요!")


# 새로운 Tkinter 창 생성
window = tk.Tk()
window.title("New Window")
window.geometry("250x100")

# 라벨 추가
#label = tk.Label(window, text="학생 등록", font=("Arial", 14))
#label.grid(row=2, column = 1)

#pack이랑 grid 혼합사용이 안됨
label1 = Label(window, text = "이름 : ").grid(row=0, column=0)
entry1 = Entry(window, width=20)
entry1.grid(row=0, column=1)

label2 = Label(window, text = "생년월일 : ").grid(row=1, column=0)
entry2 = Entry(window, width=20)
entry2.grid(row=1, column=1)

label3 = Label(window, text = "전화번호 : ").grid(row=2, column=0)
entry3 = Entry(window, width=20)
entry3.grid(row=2, column=1)

save_button = tk.Button(window, text="저장", command=save_button_clicked)
save_button.grid(row=3,column=2,pady=10)

init_db()

# 이벤트 루프 실행
window.mainloop()
