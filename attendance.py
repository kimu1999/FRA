import tkinter as tk
from tkinter import ttk
import mysql.connector

#mysql 연결 
def fetch_data():
    try:
        #데이터베이스 연결
        conn = mysql.connector.connect(
            host='127.0.0.1', 
            user='root',
            password='1234',
            db='face', 
            charset='utf8',
            auth_plugin="mysql_native_password"
         )
        cur = conn.cursor()

        #name과 timestamp만 가져오기, 오늘 날짜만 가져오기
        query ="SELECT name, timestamp FROM time where DATE(timestamp) = CURDATE()" 
        cur.execute(query)
        rows = cur.fetchall()

        #treeview에 데이터 추가
        for row in rows:
            tree.insert("", tk.END, values=row)

        cur.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# GUI창을 생성하고 라벨을 설정한다.
root = tk.Tk()
root.title("오늘 출결 현황")
root.geometry("440x300+10+10")

#treeview 위젯 생성
tree = ttk.Treeview(root, columns=("name", "timestamp"), show="headings")
#tree.heading("id", text="id")
tree.heading("name", text="이름")
tree.heading("timestamp", text="날짜 및 시간")

# 열 너비 설정
#tree.column("id", width=1)
tree.column("name", width=30)
tree.column("timestamp", width=100)

# Treeview 스크롤바 추가
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.pack(fill=tk.BOTH, expand=True)

# 데이터 로드
fetch_data()

# 이벤트 루프 실행
root.mainloop()
