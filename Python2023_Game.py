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
    
# 잡몹이 총알에 충돌시 나타나는 피격효과
class hitEffect(imageManager):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.put_img("hit_effect.png")  # 피격 효과 이미지 로드
        self.change_size(70, 70)  # 피격 효과 이미지 크기 조절
        self.duration = 0.1 * 1000  # 효과 지속 시간 (0.3초)
        self.start_time = pygame.time.get_ticks()  # 효과 시작 시간

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time >= self.duration



# 충돌 함수 정의
def crash(a, b):
    if (a.x + 25 - b.sx <= b.x) and (b.x <= a.x - 25 + a.sx):
        if (a.y + 25 - b.sy <= b.y) and (b.y <= a.y - 25 + a.sy):
            return True
        else:
            return False
    else: 
        return False
        
# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [500, 1000]
screen = pygame.display.set_mode(size)
rockimg = ['rock1.png', 'rock2.png']
rock_list = []  # 운석 리스트 추가
hit_effects = []  # 피격 효과 객체를 저장할 리스트 생성
title = "미사일 게임"
background1 = pygame.image.load("배경화면.png").convert_alpha()
background1 = pygame.transform.scale(background1, (500, 1000))
 
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock() # FPS를 위한 변수

ss = imageManager()
ss.put_img("비행선.png")
ss.change_size(31.5, 54.3)
ss.x = round(size[0]/2) - ss.sx / 2
ss.y = size[1] - ss.sy - 15
ss.move = 10

gun_sound = pygame.mixer.Sound("gun.mp3")

black = (0,0,0)

left_go = False
right_go = False
space_go = False
up_go = False  
down_go = False

# 4. 메인 이벤트
SB = 0
count = 0
item_count = 0 # 아이템 사용 시간
power = 15 # 총알 속도

kill = 0
loss = 0

a_list = [] # 잡몹1
a2_list = [] # 잡몹2
m_list = [] # 총알
item_list = [] # 아이템
boss_list = [] # 보스

start_time = datetime.now()

 
while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60) # 1초에 60번 while문 반복
    count += 1
    # 4-2. 각종 입력 감지 
    for event in pygame.event.get():# 키보드나 마우스의 동작을 받아옴
        if event.type == pygame.QUIT: # 게임 종료
            SB = 1
            
    # 키 입력 확인
    keys = pygame.key.get_pressed()

    # 비행선 위치 이동
    ss.x += ss.move * (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    ss.y += ss.move * (keys[pygame.K_DOWN] - keys[pygame.K_UP])

    # 밖으로 못 나가게
    ss.x = max(min(ss.x, size[0] - ss.sx), 0)
    ss.y = max(min(ss.y, size[1] - ss.sy), 0)
            
    # 총알 나가기
    if keys[pygame.K_SPACE]:
        space_go = True
    
    # 피격 효과 제거 이벤트 처리
    if event.type == pygame.USEREVENT + 2:
        if len(hit_effects) > 0:
            hit_effects.pop(0)

        
    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())
    
    # 피격 효과 제거
    hit_effects = [effect for effect in hit_effects if not effect.is_expired()]

    # 미사일 생성하기 

    if space_go == True and count % power == 0:
        mm = imageManager()
        mm.put_img("총알.png")
        mm.change_size(50, 100)
        gun_sound.play()
        mm.x = round(ss.x + ss.sx/2 - mm.sx/2) 
        mm.y = ss.y - mm.sy - 10  # 총알의 크기만큼 위로 올라가야함
        mm.move = 10
        m_list.append(mm)
    
    # 화면에서 나간 미사일 지우기 
    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y < -m.sy:
            d_list.append(i)
    
    for d in d_list:
        if d < len(m_list) :
            del m_list[d]
    
    # 잡몹1
    if random.random() > 0.98 :
        aa = imageManager()
        aa.put_img("잡몹1.png")
        aa.change_size(80, 100)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx/2)) # 외계인의 크기만큼 빼줌
        aa.y = 10
        aa.move = 3
        aa.hp = 2  # 체력을 2으로 설정
        a_list.append(aa)
    # 잡몹2
    if random.random() > 0.99 :
        aa2 = imageManager()
        aa2.put_img("잡몹2.png")
        aa2.change_size(100, 100)
        aa2.x = random.randrange(0, size[0] - aa2.sx - round(ss.sx/2)) # 외계인의 크기만큼 빼줌
        aa2.y = 10
        aa2.move = 2
        aa2.hp = 3  # 체력을 3으로 설정
        a_list.append(aa2)
    # 아이템1
    if count % 1000 == 0 :
        item1 = imageManager()
        item1.put_img("부스트아이템.png")
        item1.change_size(100, 100)
        item1.x = random.randrange(0, size[0] - item1.sx - round(ss.sx/2)) # 외계인의 크기만큼 빼줌
        item1.y = 10
        item1.move = 5
        item_list.append(item1)
    # 보스1
    if count == 10 :
        boss1 = imageManager() 
        boss1.put_img("보스1.png")
        boss1.change_size(200, 200)
        boss1.x = 0
        boss1.y = 15
        boss1.move = 0
        boss1.hp = 100
        boss_list.append(boss1)

    # 운석 생성하기
    if delta_time % 10 == 0 and not any(rock.y > 0 and rock.y < size[1] for rock in rock_list):
        rock = imageManager()
        rock.put_img(random.choice(rockimg))  # rockimg 배열에서 무작위 이미지 선택
        rock.change_size(100, 100)
        rock.x = random.randrange(-rock.sx, size[0])
        rock.y = 10
        rock.move = 5
        rock_list.append(rock)

     # 운석 이동하기
    for rock in rock_list:
        rock.y += rock.move
        if rock.y > size[1]:
            rock_list.remove(rock)

    # 비행기와 운석 충돌 처리
    for rock in rock_list:
        if crash(rock, ss) == True:
            SB = 1  # 게임 종료

    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
    
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
            if crash(m, a) == True :
                dm_list.append(i)
                a.hp -= 1  # 외계인 체력 감소
                if a.hp <= 0:  # 체력이 0 이하가 되면 외계인을 제거 리스트에 추가
                    da_list.append(j)
                # 피격 효과 객체 생성
                effect = hitEffect(a.x, a.y)
                hit_effects.append(effect)
                # 피격 효과를 일정 시간 후에 사라지게 하기 위한 타이머 이벤트 추가
                pygame.time.set_timer(pygame.USEREVENT + 2, 200, True)

    dboss_list = []

    for i in range(len(boss_list)) :
        b = boss_list[i]
        b.x = ss.x - 100

    for i in range(len(m_list)) :
        for j in range(len(boss_list)) :
            m = m_list[i]
            b = boss_list[j]
            if crash(m, b) == True :
                dm_list.append(i)
                b.hp -= 1
                if b.hp <= 0 :
                    dboss_list.append(j)
                effect = hitEffect(a.x, a.y)
                hit_effects.append(effect)
                pygame.time.set_timer(pygame.USEREVENT + 2, 200, True)
        

    for i in range(len(m_list)) :
        m = m_list[i]
        if crash(m, rock) :
            m = m_list[i]
            dm_list.append(i)

    dm_list = list(set(dm_list))  # 중복 제거
    da_list = list(set(da_list))  # 중복 제거

    for d in dm_list:
        if d < len(m_list) :
            del m_list[d]
    
    for a in da_list:
        if a >= 0 :
            kill += 1 # 외계인이 사라지면 kill + 
            del a_list[a]

    for b in dboss_list :
        if b >= 0 :
            del boss_list[b]

    
    # 비행기 vs 외계인 충돌하면 죽음
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1

    # 비행기 아이템 파밍
    ditem_list = []

    for i in range(len(item_list)) :
        item = item_list[i]
        item.y += item.move
        if crash(item, ss) == True :
            power = 10
            ditem_list.append(i)

    for i in ditem_list :
        del item_list[i]

    # 아이템 파워가 10일 때 아이템 카운트 증가     
    if power == 10 :
        item_count += 1
    # 아이템 카운트가 100이 됐을 때 원래대로 파워가 돌아감
    if item_count >= 100 :
        power = 15
        item_count = 0

    # 4-4. 그리기
    screen.fill(black)
    screen.blit(background1, (0, 0))
    ss.show()
    for m in m_list:
        m.show()
    
    for a in a_list:
        a.show()
    
    for rock in rock_list:
        rock.show()

    for effect in hit_effects: 
        effect.show()

    for item in item_list :
        item.show()

    for boss in boss_list :
        boss.show()

    # 텍스트 그리기  
    # font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf")
    font = pygame.font.Font("GulimChe-02.ttf", 20)
    text_kill = font.render("kill : {} ". format(kill), True, (255, 255, 0))  
    screen.blit(text_kill, (10, 5))
    
    text_time = font.render("time : {}". format(delta_time), True, (255, 255, 255))
    screen.blit(text_time, (size[0]-100, 5))
    
    # 4-5. 업데이트
    pygame.display.flip()
    
# 5. 게임 종료 
pygame.quit()
