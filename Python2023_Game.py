import pygame
import random
import time
from datetime import datetime

# 이미지 관리 클래스 정의
class imageManager:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        if address[-3:] == "png":
            self.image = pygame.image.load(address).convert_alpha()
        else:
            self.image = pygame.image.load(address)
        self.sx, self.sy = self.image.get_size() 
    def change_size(self, sx, sy):
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.sx, self.sy = self.image.get_size()
    def show(self):
        screen.blit(self.image, (self.x, self.y))

# 충돌 함수 정의
def crash(a,b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else: 
        return False
        
# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "미사일 게임"

pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock() # FPS를 위한 변수

ss = imageManager()
ss.put_img("비행선.png")
ss.change_size(80, 80)
ss.x = round(size[0]/2) - ss.sx / 2
ss.y = size[1] - ss.sy - 15
ss.move = 10

black = (0,0,0)

left_go = False
right_go = False
space_go = False
up_go = False
down_go = False

# 4. 메인 이벤트
SB = 0
k = 0

kill = 0
loss = 0

a_list = []
 #b_list = [] 잡몹더만들다실패
m_list = []

start_time = datetime.now()

while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60) # 1초에 60번 while문 반복
    
    # 4-2. 각종 입력 감지 
    for event in pygame.event.get():# 키보드나 마우스의 동작을 받아옴
        if event.type == pygame.QUIT: # 게임 종료
            SB = 1
        if event.type == pygame.KEYDOWN: # 키가 눌렸을 때
            if event.key == pygame.K_LEFT: # 키가 왼쪽키이면 
                left_go = True
            if event.key == pygame.K_RIGHT:
                right_go = True
            if event.key == pygame.K_SPACE:
                space_go = True
                k = 0
            if event.key == pygame.K_UP:
                up_go = True
            if event.key == pygame.K_DOWN:
                down_go = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            if event.key == pygame.K_RIGHT:
                right_go = False  
            if event.key == pygame.K_SPACE:
                space_go = False
            if event.key == pygame.K_UP:
                up_go = False
            if event.key == pygame.K_DOWN:
                down_go = False
        
    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())
    
    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0
    elif right_go == True:
        ss.x += ss.move
        if ss.x >= size[0] - ss.sx:
            ss.x = size[0] - ss.sx
    elif up_go == True:
        ss.y -= ss.move
        if ss.y <= 0:
            ss.y = 0
    elif down_go == True:
        ss.y += ss.move
        if ss.y >= size[1] - ss.sy:
            ss.y = size[1] - ss.sy

    
    # 미사일 생성하기 

    if space_go == True and k % 30 == 0:
        mm = imageManager()
        mm.put_img("총알.png")
        mm.change_size(20, 40)
        mm.x = round(ss.x + ss.sx/2 - mm.sx/2) 
        mm.y = ss.y - mm.sy - 10  # 총알의 크기만큼 위로 올라가야함
        mm.move = 15
        m_list.append(mm)

    k += 1 
    
    # 화면에서 나간 미사일 지우기 
    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y < -m.sy:
            d_list.append(i)
    
    for d in d_list:
        del m_list[d]
    
    # 외계인 등장
    if random.random() > 0.98:
        aa = imageManager()
        aa.put_img("잡몹1.png")
        aa.change_size(50, 50)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx/2)) # 외계인의 크기만큼 빼줌
        aa.y = 10
        aa.move = 2
        a_list.append(aa)
        
        # bb = imageManager()       -- 잡몹더만들다실패 --
        # bb.put_img("잡몹2.png")
        # bb.change_size(50, 50)
        # bb.x = random.randrange(0, size[0] - bb.sx - round(ss.sx/2)) # 외계인의 크기만큼 빼줌
        # bb.y = 10
        # bb.move = 1
        # b_list.append(bb)           ---------------------
        
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
            loss += 1 # 외계인이 지나가면 loss + 1
            
    # for i in range(len( b_list)):  -- 잡몹더만들다실패 --
    #     b = b_list[i]
    #     b.y += b.move
    #     if  b.y >= size[1]:
    #         d_list.append(i)
    #         loss += 1 # 외계인이 지나가면 loss + 1 ---------------
            
    
    dd_list = []
    for d in dd_list:
        del a_list[d]
    
    # 외계인 vs 미사일 충돌하는 경우 제거
    dm_list = []
    da_list = []
    
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m,a) == True:
                dm_list.append(i)
                da_list.append(j)
                
    dm_list = list(set(dm_list)) # 중복제거
    da_list = list(set(da_list)) # 중복제거
    
    for d in dm_list:
        del m_list[d]
    
    for a in da_list:
        del a_list[a]
        kill += 1 # 외계인이 사라지면 kill + 1
    
    
    # 비행기 vs 외계인 충돌하면 죽음
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1
    
    # 4-4. 그리기
    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    
    for a in a_list:
        a.show()
    
    # 텍스트 그리기
    # font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf")
    font = pygame.font.Font("GulimChe-02.ttf", 20)
    text_kill = font.render("kill : {} loss : {}". format(kill, loss), True, (255, 255, 0))  
    screen.blit(text_kill, (10, 5))
    
    text_time = font.render("time : {}". format(delta_time), True, (255, 255, 255))
    screen.blit(text_time, (size[0]-100, 5))
    
    # 4-5. 업데이트
    pygame.display.flip()
    
# 5. 게임 종료 
pygame.quit()