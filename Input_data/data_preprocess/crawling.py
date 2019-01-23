
import time
import pyautogui

# 크롤링

# web brouser : Chrome, screen size : 67%
# screen size : 1920x1080 기준
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

### 이동 단위(web brouser : Chrome, screen size : 67% 기준)
mx=112
my=132

### 현재 마우스 커서 위치 확인
currentMouseX, currentMouseY = pyautogui.position()
print(currentMouseX, currentMouseY)

### Setting
x_ = 652 # 시작 위치의 x좌표, #기본 652
y_ = 321 # 시작 위치의 y좌표, #기본 321
a = 6 # 한 화면 안에 들어오는 rows 수 #기본 6
b = 7 # 한 화면 안에 들어오는 columns 수 #기본 7
k = 1 # 다운받으려는 음악들이 한 페이지를 넘어갈 때 사용. 넘어가지 않을 땐 1. 넘어간다면, k=1로 한 페이지 실행 후, k=2, 3, ...으로 계속 실행. #기본 1
# x_, y_, a, b, k를 조정해준 뒤, 제일 아래에 있는 start()함수를 실행시켜주시면 됩니다.
# (실행한 뒤, 4초 후에 함수가 실행됩니다.)
#######################################################

def macro(mxcount, mycount):
    pyautogui.moveTo(x_+mx*mxcount, y_+my*mycount) #n번째 파일의 화면 상 위치로 마우스 이동, 클릭
    pyautogui.click()
    time.sleep(3)

    pyautogui.moveTo(620, 240) # copy버튼 클릭
    pyautogui.click()
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(4)

    pyautogui.moveTo(860, 245) # key 설정 버튼 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(843, 640) # 장단조 선택 버튼 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(843, 380) # Major 선택 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(860, 380) # C key 선택 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(940, 245) # Tempo 조절 버튼 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(896, 393) # Tempo 110 선택 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(1850, 260) # Export 버튼 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(1686, 416) # MIDI 저장 버튼 클릭
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(90, 80) # 뒤로
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)

    pyautogui.moveTo(90, 80) # 뒤로
    pyautogui.click()
    pyautogui.press('enter')
    time.sleep(3)
#######################################################
def start(c):
    time.sleep(4)
    for j in range(20*(c-1)):
        pyautogui.press('down')
    for y in range(a):
        for x in range(b):
            macro(x, y)
#######################################################

start(k)
