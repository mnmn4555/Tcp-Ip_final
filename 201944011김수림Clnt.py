from tkinter import *
from socket import *
import threading


def baseball(): # 입력한 숫자를 Server에 전송
    num = en_num.get() # 입력한 숫자를 읽는다
    sock.send(num.encode()) # Server에 num을 전송

def handler(sock): #스레드
    while True:
        try:
            r_msg = sock.recv(1024) # 메세지 수신
        except:
            pass # 수신된 데이터가 없으면 pass
        else:
            num = en_num.get() # 입력한 숫자를 읽는다
            en_recv.delete(0, END) # 결과 창을 초기화
            en_recv.insert(0, r_msg.decode()) # 입력한 숫자에 대한 결과값을 입력하여 화면에 보여준다
            en_num.delete(0, END) # btn_input버튼을 누르면 입력란에 쓰인 text 삭제
            text_result.insert(END, num + '\t') # 입력한 숫자를 누적해서 보여준다
            text_result.insert(END, r_msg.decode()+'\n') # 입력한 숫자에 해당하는 결과값을 누적하여 보여준다

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("192.168.0.41", 2500))

w = Tk()
w.title("숫자 야구게임")
w.geometry('700x550')

explain = Label(text="***** 숫자야구게임 *****\n"
              "3자리의 임의의 숫자와 숫자의 위치를 맞추는 게임 !!!\n"\
              "숫자는 맞지만 숫자의 위치가 맞지 않는 경우 -> ball\n"\
              "숫자와 숫자의 위치 모두 맞는 경우 -> strike\n"\
              "3strike가 되면 정답처리되어 게임이 종료됩니다!!\n"\
              "ex) 답 : 359 \n"\
              "입력 : 392 -> 1s 1b \n"\
              "입력 : 463 -> 0s 1b \n" , font=('Verdana', 16)) # 숫자야구게임 설명
lbl_num = Label(text='숫자입력', font=('Verdana', 16))
en_num = Entry(text="중복 허용 3자리 숫자",font=('Verdana', 16), width=15)
lbl_recv = Label(text='결과', font=('Verdana', 16))
en_recv = Entry(font=('Verdana', 16), width=15)
btn_input = Button(text='입력', font=('Verdana', 12), command=baseball)
text_result = Text(w, width = 50, height = 15)

explain.grid(row=0,column=1)
lbl_num.grid(row=1, column=0)
en_num.grid(row=1, column=1)
btn_input.grid(row=1, column=2)
lbl_recv.grid(row=2, column=0)
en_recv.grid(row=2, column=1)
text_result.grid(row=3, column=1)

t = threading.Thread(target=handler, args=(sock,)) # 스레드 발생
t.deamon = True
t.start()

w.mainloop()