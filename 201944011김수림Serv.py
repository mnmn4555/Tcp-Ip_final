from socket import *
import sys
import random as rd
from threading import *
import time

clients = []
BUFF = 1024
HOST ='192.168.0.41'
port = 2500
answer = False
error = ""

if len(sys.argv) > 1:
    port = int(eval(sys.argv[1])) #입력한 port가 있을 때, port는 입력한 port로 사용
else:
    port = port # 입력한 port가 없는 경우 default값으로 설정

def handler(conn):
    global clients, answer #전역변수인 clients, answer을 지역변수로 사용하기 위해 global을 사용
    while True:
        if answer == True: # answer이 True일 때, 게임이 종료된다.
            break
        number = str(rd.randint(1, 999)).zfill(3) # 1~999까지 숫자가
        print('임의의 3자리 숫자 :', number)

        num = "0123456789" # 숫자 이외 다른 것을 입력할 때, 이를 구분하기 위해 사용하는 num변수
        cnt = 1 # 숫자를 입력하는 횟수를 구하는 변수 -> 정답을 맞출 때까지 숫자를 입력 할 때마다 cnt변수가 1씩 증가함

        while True:
            guess = conn.recv(BUFF) # Client에서 입력한 문자열을 받는다. (데이터 수신)
            print('data: ' + repr(guess)) # 수신받은 데이터를 Server 창에 띄워준다
            if not guess: # guess에 아무런 내용이 없을때, 해당 파일 디스크립트(conn)를 삭제한다
                clients.remove(conn)
                break
            guess = guess.decode() # 수신반은 guess를 화면에 뿌려주는 역할

            strike = 0
            ball = 0
            try:
                if len(guess) != 3: # 수신받은 데이터의 길이가 3이 아닐경우 발생하는 오류
                    error = "0~999 사이의 숫자를 입력해주세요~!"
                    conn.send(error.encode()) # 오류 내용을 Client 결과 창에 출력하기 위해 전송한다
                    raise Exception("0~999 사이의 숫자를 입력해주세요")

                for i in guess:
                    if i not in num: # guess에 있는 문자가 num에 없는 경우 발생하는 오류
                        error = "숫자만 입력하세요~!"
                        conn.send(error.encode()) # 오류 내용을 Client 결과 창에 출력하기 위해 전송한다
                        raise Exception("숫자만 입력하세요")

            except Exception as e: # 오류 내용을 출력한다
                print('error :', e)
            else:
                if guess == number: # 수신받은 데이터(guess)와 임의의 숫자(number)가 일치하면 정답으로 처리되어 게임이 종료된다
                    data = "정답 ! {0}번 시도".format(cnt)
                    conn.send(data.encode()) #
                    time.sleep(3) # sleep(3)을 하지 않으면 client에 "정답"이라는 문구가 보여지지 않고 게임이 종료된다.
                    answer = True # 정답일 때, answer을 True로 바꾼다
                    break

                number2 = list(number) # number를 리스트로 변환하여 index를 이용하여 각 자리 숫자
                for i in range(3):
                    if guess[i] == number2[i]: # 숫자의 종류와 위치가 일치할 경우 strike변수는 1증가
                        strike += 1
                        number2[i] = 's'

                for i in range(3):
                    if guess[i] in number2: # 숫자가 number2에 있을 경우 ball변수는 1증가
                        ball += 1
                        number2[number2.index(guess[i])] = 'b'

                data = str(strike) + 's', str(ball) + 'b' # 입력한 숫자에 대한 strike와 ball 정보,
                rdata = data[0] + data[1] # tuple형태로는 encode가 되지 않으므로 string으로 변환한다
                conn.send(rdata.encode()) # rdata를 Client로 전송한다
                cnt += 1 # cnt 1증가
    conn.close()

ADDR = (HOST,port)
servsock = socket(AF_INET, SOCK_STREAM)
servsock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
servsock.bind(ADDR)
servsock.listen(3)
print("Waiting for connection from client")

while True:
    conn, (remotehost, remoteport) = servsock.accept()
    if conn not in clients:
        clients.append(conn)
    print(HOST, ':', str(port), '가 연결되었습니다')
    t = Thread(target=handler, args=(conn, ))
    t.daemon = True
    t.start()


