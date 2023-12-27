"""
exe化手順
ターミナルでC:\forPython\GRAVITY_ALIENforDev>に入り
①仮想環境にする
.venv\Scripts\Activate.ps1
②pyinstllerを起動
pyinstaller --onefile --icon=.\data\icon.ico --noconsole Gravity_Alien.py
"""

import pygame
import sys
import random
import time
from pygame.locals import *

#Widthは偶数にする
pygame.init()
WIDTH = 10

BLACK = (0,0,0)
GRAY = (50,50,50)
WHITE = (255,255,255)
BLUE = (0,90,255)
dBLUE= (0,18,51)
ORANGE =(246,170,0)
dORANGE = (49,34,0)
RED = (255,10,0)
dRED =(51,2,0)
GREEN = (3,175,122)
dGREEN= (0,35,24)



global bg_img
bg_img = pygame.image.load("./data/image/space2.jpg")

global egg_img
global exp_img
global monster
monster = []*4






#落ちる方向を決めるときに使う。以降基本的に0,1,2,3,4をそれぞれ下、上、右、左、移動なし(もしくは空白)を示すものとする
vector_x = (0, 0, 1, -1, 0)
vector_y = (1, -1, 0, 0, 0)

matrix = []
check = []
for i in range(WIDTH):
    matrix.append([4]*WIDTH)
    check.append([4]*WIDTH)

#落下物のx,y主座標。重力方向に対して水平方向に隣り合う座標にも落下物は存在する
obx = 0
oby = 0
cc = 0
obinf = [0,1,2,3]
cn = 0
gra_o = 0


def create_ob(gra):
    global obx, oby, cc, cn, gra_o
    flg = False
    #オブジェクトの位置を初期化
    if gra == 0:
        obx = int(WIDTH/2)-1
        oby = 0
    elif gra == 1:
        obx = int(WIDTH/2)
        oby = WIDTH-1
    elif gra == 2:
        obx = 0
        oby = int(WIDTH/2)-1
    elif gra == 3:
        obx = WIDTH-1
        oby = int(WIDTH/2)
    
    GAMEOVER =False
    if matrix[oby][obx] != 4 or matrix[oby+vector_x[gra]][obx+vector_y[gra]] != 4:
        GAMEOVER = True
    #ランダムにオブジェクトを生成
    if GAMEOVER == False:
        #1周目
        if cc == 0:
            for i in range(4):
                obinf[i]=i
        if cc%2 == 0:
            random.shuffle(obinf)
            if cc == 6:
                for i in range(4):
                    if obinf[i] == gra:
                        obinf[i] = 6
                        cn = i
                        gra_o = gra

            matrix[oby][obx] = obinf[0]
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = obinf[1]
            cc =cc + 1
        #2周目
        else:
            matrix[oby][obx] = obinf[2]
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = obinf[3]
            cc = cc + 1
            if cc > 7:
                cc = 0
    return GAMEOVER


 #オブジェクトを左右に動かす       
def move(gra, vkey, t_max):
    global obx, oby, timer
    #キーと重力が一致する時即座にdrop1に移行
    if gra == vkey :
        timer = t_max
    elif (gra, vkey) == (0,1) or (gra, vkey) == (1,0) or (gra, vkey) == (2,3) or (gra, vkey) == (3,2):
        vkey = 4
    #キー方向には動けるなら
    elif -1< obx+vector_x[vkey] and obx+vector_x[vkey] < WIDTH and -1 < oby+vector_y[vkey] and oby+vector_y[vkey] < WIDTH and -1 < (obx+vector_y[gra])+vector_x[vkey] and (obx+vector_y[gra])+vector_x[vkey] < WIDTH and -1 < (oby+vector_x[gra])+vector_y[vkey] and (oby+vector_x[gra])+vector_y[vkey] < WIDTH:
        if matrix[oby+vector_y[vkey]][obx+vector_x[vkey]] == 4 or matrix[(oby+vector_x[gra])+vector_y[vkey]][(obx+vector_y[gra])+vector_x[vkey]] == 4:
            one = matrix[oby][obx]
            two = matrix[oby+vector_x[gra]][obx+vector_y[gra]]
            matrix[oby][obx] = 4
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = 4
            matrix[oby+vector_y[vkey]][obx+vector_x[vkey]] = one
            matrix[(oby+vector_x[gra])+vector_y[vkey]][(obx+vector_y[gra])+vector_x[vkey]] = two
            obx = obx+vector_x[vkey]
            oby = oby+vector_y[vkey]
            


#オブジェクトのみ落とす
def drop1(gra):
    global obx, oby, land_se
    flg = False
    #重力方向には動けるなら
    if -1< obx+vector_x[gra] and obx+vector_x[gra] < WIDTH and -1 < oby+vector_y[gra] and oby+vector_y[gra] < WIDTH and -1 < (obx+vector_y[gra])+vector_x[gra] and (obx+vector_y[gra])+vector_x[gra] < WIDTH and -1 < (oby+vector_x[gra])+vector_y[gra] and (oby+vector_x[gra])+vector_y[gra] < WIDTH:
        if matrix[oby+vector_y[gra]][obx+vector_x[gra]] == 4 and matrix[(oby+vector_x[gra])+vector_y[gra]][(obx+vector_y[gra])+vector_x[gra]] == 4:
            matrix[oby+vector_y[gra]][obx+vector_x[gra]] = matrix[oby][obx]
            matrix[(oby+vector_x[gra])+vector_y[gra]][(obx+vector_y[gra])+vector_x[gra]] = matrix[oby+vector_x[gra]][obx+vector_y[gra]]
            matrix[oby][obx] = 4
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = 4
            obx = obx+vector_x[gra]
            oby = oby+vector_y[gra]
            flg = True
    if not flg :
        land_se.play()
    return flg

#全体を落とす
def drop2(gra):
    flg = False
    #重力が下か上だったら
    if gra < 2:
        for y in range((WIDTH-2)*(1-gra)+gra,(-1+gra)+WIDTH*gra,-1+2*gra) : #重力に逆らうような順でmatrixを更新する
            for x in range(WIDTH):
                if matrix[y][x] != 4 and matrix[y][x] != 6 and matrix[y+vector_y[gra]][x+vector_x[gra]] == 4:
                    matrix[y+vector_y[gra]][x+vector_x[gra]] = matrix[y][x]
                    matrix[y][x] = 4
                    flg = True
    else:
        for x in range((WIDTH-2)*(3-gra)+(gra-2), (gra-3)+WIDTH*(gra-2),-5+2*gra): #重力に逆らうような順でmatrixを更新する
            for y in range(WIDTH):
                if matrix[y][x] != 4 and matrix[y][x] != 6 and matrix[y+vector_y[gra]][x+vector_x[gra]] == 4:
                    matrix[y+vector_y[gra]][x+vector_x[gra]] = matrix[y][x]
                    matrix[y][x] = 4
                    flg = True    
    return flg
    
gflag =[0,0,0,0]
#水平方向に揃ったらマスの属性を変化.変化させたらtrueを返す 
def checkmat(gra):
    flag = False
    for y in range(WIDTH):
        for x in range(WIDTH):
            check[y][x] = matrix[y][x]
    #重力方向とオブジェクトの方向が揃ったら垂直方向でも変化させる
    if gra <2:             
        for y in range(WIDTH):
            for x in range(WIDTH):
                if check[y][x] < 4:
                    if x>0 and x<WIDTH-1 and check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                        gflag[check[y][x]] = 1
                        flag = True
                        matrix[y][x-1] = 5
                        matrix[y][x] = 5
                        matrix[y][x+1] = 5
                    if y>0 and y<WIDTH-1 and check[y][x] == gra:
                        if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                            gflag[check[y][x]] = 1
                            flag = True
                            matrix[y-1][x] = 5
                            matrix[y][x] = 5
                            matrix[y+1][x] = 5

    
    else:
        for y in range(WIDTH):
            for x in range(WIDTH):
                if check[y][x] < 4:
                    if y>0 and y<WIDTH-1 and check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                        gflag[check[y][x]] = 1
                        flag = True
                        matrix[y-1][x] = 5
                        matrix[y][x] = 5
                        matrix[y+1][x] = 5
                    elif x>0 and x<WIDTH-1 and check[y][x] == gra:
                        if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                            gflag[check[y][x]] = 1
                            flag = True
                            matrix[y][x-1] = 5
                            matrix[y][x] = 5
                            matrix[y][x+1] = 5

    
    return flag

#揃って黒くなったマスを消して、消した数をreturnする
def sweep():
    delta = 0
    for y in range(WIDTH):
        for x in range(WIDTH):
            if matrix[y][x] == 5:
                delta = delta + 1
                matrix[y][x] = 4
    return delta

#卵を重力の向きに沿って孵化させる
def change(gra):
    for y in range(WIDTH):
        for x in range(WIDTH):
            check[y][x] = matrix[y][x]
    #上下左右に卵と変化後の重力のエイリアンしかいないかチェック
    for y in range(WIDTH):
            for x in range(WIDTH):
                if check[y][x] == 6:
                    if y == 0:
                        if x == 0:
                            if ((check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra
                        elif x == WIDTH-1:
                            if ((check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra)):
                                matrix[y][x] = gra  
                        else:
                            if ((check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra
                    elif y == WIDTH-1:
                        if x == 0:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra
                        elif x == WIDTH-1:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra)):
                                matrix[y][x] = gra  
                        else:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra
                    else:
                        if x == 0:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and
                                (check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra
                        elif x == WIDTH-1:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and 
                                (check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra)):
                                matrix[y][x] = gra  
                        else:
                            if ((check[y-1][x] > 3 or check[y-1][x] == gra) and 
                                (check[y+1][x] > 3 or check[y+1][x] == gra) and 
                                (check[y][x-1] > 3 or check[y][x-1] == gra) and 
                                (check[y][x+1] > 3 or check[y][x+1] == gra)):
                                matrix[y][x] = gra







#マスと文字を描画
def draw(bg, fnt, gra_f):
    global point
    global bg_img, egg_img, exp_img

    bg.blit(bg_img,[0,0])
    pygame.draw.rect(bg,WHITE,[0,0,600,600])



    for y in range(WIDTH):
        for x in range(WIDTH):
            pygame.draw.rect(bg, GRAY, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            
            if matrix [y][x] == 4:
                pygame.draw.rect(bg, BLACK, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0) 

            if ((y,x)==(int(WIDTH/2)-1,0) or (y,x)==(int(WIDTH/2),0)):
                pygame.draw.rect(bg, dRED, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif ((y,x)==(int(WIDTH/2)-1,WIDTH-1) or (y,x)==(int(WIDTH/2),WIDTH-1)):
                pygame.draw.rect(bg, dGREEN, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            if ((x,y)==(int(WIDTH/2)-1,0) or (x,y)==(int(WIDTH/2),0)):
                pygame.draw.rect(bg, dBLUE, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif ((x,y)==(int(WIDTH/2)-1,WIDTH-1) or (x,y)==(int(WIDTH/2),WIDTH-1)):
                pygame.draw.rect(bg, dORANGE, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)

            if matrix [y][x] == 5:
                bg.blit(exp_img,[x*int(600/WIDTH), y*int(600/WIDTH)])
            elif matrix [y][x] == 6:
                bg.blit(egg_img,[x*int(600/WIDTH), y*int(600/WIDTH)])
            elif matrix[y][x] == 0:
                bg.blit(monster[0],[x*int(600/WIDTH), y*int(600/WIDTH)])
            elif matrix[y][x] == 1:
                bg.blit(monster[1],[x*int(600/WIDTH), y*int(600/WIDTH)])
            elif matrix[y][x] == 2:
                bg.blit(monster[2],[x*int(600/WIDTH), y*int(600/WIDTH)])
            elif matrix[y][x] == 3:
                bg.blit(monster[3],[x*int(600/WIDTH), y*int(600/WIDTH)])
    
    
    
    #４方向を指す矢印を描画、重力を変えたい方向だけ白色に描画する
    bw =[BLACK]*4
    bw[gra_f]= WHITE

    pygame.draw.polygon(bg,bw[0],[(750,465),(710,415),(790,415)])
    pygame.draw.rect(bg,bw[0],[730,365,40,50])

    pygame.draw.polygon(bg,bw[1],[(750,215),(710,265),(790,265)])
    pygame.draw.rect(bg,bw[1],[730,265,40,50])

    pygame.draw.polygon(bg,bw[2],[(875,340),(825,380),(825,300)])
    pygame.draw.rect(bg,bw[2],[775,320,50,40])

    pygame.draw.polygon(bg,bw[3],[(625,340),(675,380),(675,300)])
    pygame.draw.rect(bg,bw[3],[675,320,50,40])

    

    #動かせる重力は色を付ける
    if gflag[0] == 1:
        pygame.draw.polygon(bg,BLUE,[(750,440),(730,415),(770,415)])
        pygame.draw.rect(bg,BLUE,[730,365,40,50])
    if gflag[1] == 1:
        pygame.draw.polygon(bg,ORANGE,[(750,240),(730,265),(770,265)])
        pygame.draw.rect(bg,ORANGE,[730,265,40,50])
    if gflag[2] == 1:
        pygame.draw.polygon(bg,RED,[(850,340),(825,360),(825,320)])
        pygame.draw.rect(bg,RED,[775,320,50,40])
    if gflag[3] == 1:
        pygame.draw.polygon(bg,GREEN,[(650,340),(675,360),(675,320)])
        pygame.draw.rect(bg,GREEN,[675,320,50,40])
        
    #スコア表示
    Sc_l = fnt.render("Score: " + str(point), True, WHITE)
    pygame.draw.rect(bg,BLACK,[750-Sc_l.get_width()/2,120-Sc_l.get_height()/2,Sc_l.get_width(),Sc_l.get_height()])
    bg.blit(Sc_l, [750-Sc_l.get_width()/2,120-Sc_l.get_height()/2])

    #メニュー表示
    mn_l = fnt.render("[M]enu", True, WHITE)
    pygame.draw.rect(bg,BLACK,[750-mn_l.get_width()/2,600-mn_l.get_height()/2,mn_l.get_width(),mn_l.get_height()])
    bg.blit(mn_l, [750-mn_l.get_width()/2,600-mn_l.get_height()/2])



    pygame.display.update()
            
    

index = 0
timer = 0
count = 0
point = 0

"""
-------------------------------------------------------------------------------------------------

"""

def main():
    global index, timer, count, point, monster, egg_img, exp_img, cc
    pygame.init()
    screen = pygame.display.set_mode((900, 680))
    clock = pygame.time.Clock()
    font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 30)

    t_font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 60)
    h_font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 30)
    c_font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 20)
    m_font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 80)
    big_font = pygame.font.Font("./data/x12y16pxMaruMonica.ttf", 100)
    

    logo_img = pygame.image.load("./data/image/title_logo.jpg").convert_alpha()
    logo_img = pygame.transform.rotozoom(logo_img, 0, 0.5)
    pygame.display.set_caption("Gravity Alien")
    pygame.display.set_icon(logo_img)
    #モンスターの画像を管理する配列
    for i in range(4):
        img = pygame.image.load("./data/image/monster_img"+str(i)+".png").convert_alpha()
        monster.append(pygame.transform.rotozoom(img, 0, 59/500))
    
    egg_img = pygame.image.load("./data/image/egg.png").convert_alpha()
    egg_img = pygame.transform.rotozoom(egg_img, 0, 59/500)

    exp_img = pygame.image.load("./data/image/explosion.png").convert_alpha()
    exp_img = pygame.transform.rotozoom(exp_img, 0, 59/500)

    title_se =pygame.mixer.Sound("./data/sound/nc315489.wav")
    title_se.set_volume(0.15)
    
    pygame.mixer.music.load("./data/sound/nc105042.wav")
    pygame.mixer.music.set_volume(0.1)

    move_se =pygame.mixer.Sound("./data/sound/nc257692.wav")
    move_se.set_volume(0.7)

    global land_se
    land_se =pygame.mixer.Sound("./data/sound/nc173781.mp3")
    land_se.set_volume(0.15)
    scene = 0

    exp_se = pygame.mixer.Sound("./data/sound/nc278397.wav")
    exp_se.set_volume(0.7)

    gmov_se = pygame.mixer.Sound("./data/sound/nc99707.wav")
    gmov_se.set_volume(0.7)


    scene = 0
    index = 0

    while True:
        #タイトル
        if scene == 0:
            index = 0
            while scene == 0:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                #タイトル描画
                if index == 0:
                    screen.fill((0,0,12))
                    screen.blit(logo_img,[0,340-logo_img.get_height()/2])

                    play_l = t_font.render(" [P]lay Game ", True, WHITE)
                    screen.blit(play_l,[logo_img.get_width(),280])

                    how_l = t_font.render(" [H]ow to play ", True, WHITE)
                    screen.blit(how_l,[logo_img.get_width(),340])

                    credit_l = t_font.render(" [C]redits", True, WHITE)
                    screen.blit(credit_l,[logo_img.get_width(),400])
                    index = 1
                #タイトル待機
                if index == 1:
                    key = pygame.event.pump()
                    key = pygame.key.get_pressed()
                    if key[K_p] == 1:
                        title_se.play()
                        scene = 1 
                        time.sleep(0.4)
                    elif key[K_h] == 1:
                        title_se.play()
                        index = 2
                        first = True
                    elif key[K_c] == 1:
                        title_se.play()
                        title_se.play()
                        index = 3
                        first = True
                
                #遊び方
                if index == 2:
                    if first:
                        first =False
                        overlay = pygame.Surface((900, 680), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 240))
                        screen.blit(overlay,[0,0])

                        f = open("./data/text/howtoplay.txt", 'r', encoding='UTF-8')
                        text =f.read().splitlines()
                        f.close()
                        for i in range(len(text)):
                            howtoplay = h_font.render(text[i], True, WHITE)
                            screen.blit(howtoplay,[10,10+40*i])
                        #エイリアンの図                    
                        for i in range(len(monster)):
                            screen.blit(monster[i],[80 + 70*i, 500])
                        alien_l = h_font.render("エイリアン", True, WHITE)
                        screen.blit(alien_l,[220-alien_l.get_width()/2,580])
                        #卵の図
                        screen.blit(egg_img,[450,500])
                        egg_l = h_font.render("卵", True, WHITE)
                        screen.blit(egg_l,[481-egg_l.get_width()/2,580])

                        back_l = t_font.render("[B]ack", True, WHITE)
                        screen.blit(back_l,[850-back_l.get_width(),630-back_l.get_height()])
                    key = pygame.event.pump()
                    key = pygame.key.get_pressed()
                    if key[K_b] == 1:
                        title_se.play()
                        index = 0
                #クレジット
                if index == 3:
                    if first:
                        first =False
                        overlay = pygame.Surface((900, 680), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 240))
                        screen.blit(overlay,[0,0])

                        f = open("./data/text/credit.txt", 'r', encoding='UTF-8')
                        text =f.read().splitlines()
                        f.close()
                        for i in range(len(text)):
                            letter = c_font.render(text[i], True, WHITE)
                            screen.blit(letter,[10,10+30*i])
                        back_l = t_font.render("[B]ack", True, WHITE)
                        screen.blit(back_l,[850-back_l.get_width(),630-back_l.get_height()])
                    key = pygame.event.pump()
                    key = pygame.key.get_pressed()
                    if key[K_b] == 1:
                        title_se.play()
                        index = 0
                
                    


                pygame.display.update()
        
        #プレイ
        if scene == 1:
            #初期化
            for y in range(WIDTH):
                for x in range(WIDTH):
                    matrix[y][x] = 4
                    check[y][x] = 4
            for i in range(4):
                gflag[i] =0
            pygame.mixer.music.play(-1)
            key_flg = 4
            #重力は下
            g = 0
            #矢印は下
            g_inter = 0
            index = 0
            #エイリアンの生成周期の初期化
            cc=0
            #スコアの初期化
            point = 0
            #落ちるスピードの初期化
            time_m=10
            tt=20

            while scene == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    key = pygame.event.pump()
                    key = pygame.key.get_pressed()
                    #メニュー画面
                    if key[K_m] == 1:
                        title_se.play()
                        #画面を暗くする
                        overlay = pygame.Surface((900, 680), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 240))
                        screen.blit(overlay,[0,0])
                        #文字を描画
                        menu =["MENU","[C]ontinue","[R]etry","[T]itle"]
                        for i in range(len(menu)):
                            letter = m_font.render(menu[i], True, WHITE)
                            screen.blit(letter,[450-letter.get_width()/2,100+100*i])

                        letter = h_font.render("Move Aliens: direction key", True, WHITE)
                        screen.blit(letter,[450-letter.get_width()/2,550])
                        letter = h_font.render("Change Gravity: WASD key", True, WHITE)
                        screen.blit(letter,[450-letter.get_width()/2,600])
                        
                        pygame.display.update()

                        exit_flg = False
                        #一時停止
                        while exit_flg == False:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                            key = pygame.event.pump()
                            key = pygame.key.get_pressed()
                            if key[K_c]==1:
                                title_se.play()
                                exit_flg = True
                            #リトライ
                            if key[K_r]==1:
                                title_se.play()
                                exit_flg= True
                                #初期化
                                for y in range(WIDTH):
                                    for x in range(WIDTH):
                                        matrix[y][x] = 4
                                        check[y][x] = 4
                                        for i in range(4):
                                            gflag[i] =0
                                        key_flg = 4
                                        g = 0
                                        g_inter = 0
                                        index = 0
                                        cc = 0
                                        point = 0
                                        time_m = 10
                                        tt=20
                                        pygame.display.update()
                            #タイトルへ
                            if key[K_t]==1:
                                title_se.play()
                                exit_flg = True
                                index = -1
                                scene = 0
                                pygame.mixer_music.stop()                           
                    
                #落下物生成
                if index == 0:
                    if create_ob(g) ==False:
                        index = 1
                    #ゲームオーバー
                    else:
                        pygame.mixer.music.stop()
                        gmov_se.play()
                        scene = 2

                #落下１
                if index == 1:
                    key_flg = 4
                    key = pygame.event.pump()
                    key = pygame.key.get_pressed()

                    #キー入力を検知
                    if key[K_DOWN] == 1:
                        key_flg = 0
                    elif key[K_UP] == 1:
                        key_flg = 1
                    elif key[K_RIGHT] == 1:
                        key_flg = 2
                    elif key[K_LEFT] == 1:
                        key_flg = 3
                
                    if key[K_s]== 1:
                        if g_inter != 0:
                            title_se.play()
                        g_inter = 0
                    elif key[K_w] == 1:
                        if g_inter != 1:
                            title_se.play()
                        g_inter = 1
                    elif key[K_d] == 1:
                        if g_inter != 2:
                            title_se.play()
                        g_inter = 2
                    elif key[K_a] == 1:
                        if g_inter != 3:
                            title_se.play()
                        g_inter = 3
                    move(g, key_flg,time_m)
                    if timer < time_m-1:
                        timer = timer + 1
                    #timer = time_mの時オブジェクトを下に落下.難易度調整でここが短くなる予定
                    else:
                        if drop1(g) == False:
                            index = 2
                        timer = 0
                #落下２(全体)
                if index == 2:
                    #落とす。もし落とすものがないなら
                    if drop2(g) == False:
                        index = 3
                     
            #消去
                if index == 3:
                    if timer == 0:                                    
                        #揃ったマスがないならフェイズ変更
                        if checkmat(g) == False:
                        #重力変化前なら重力変化フェイズに
                            if count == 0:
                                count = count + 1
                                index = 4
                        #重力変化後ならオブジェクト作成フェイズに
                            else:
                                count = 0
                                index = 0
                        else:
                            timer =timer + 1
                            exp_se.play() 
                    #揃っていたら２周後に削除しポイント加算。
                    elif timer == 2:
                        dp = sweep()
                        point = point + dp
                        timer = 0
                        index = 2
                        #20ポイントごとに加速
                        if point>tt and time_m>2:
                            #初期が10で20pointごとに1減る
                            time_m=10-point//20
                            tt = tt+20
                            print(tt)
                            print(time_m)
                            #2より短くならない
                            if time_m<2:
                                time_m=2
                            letter = big_font.render("SPEED UP", True, WHITE)
                            screen.blit(letter,[300-letter.get_width()/2,300-letter.get_height()/2])
                            pygame.display.update()
                            time.sleep(1)

                            
                    else:
                        timer = timer + 1

                


                #重力変化
                if index == 4:
                    if timer < 3:
                        timer = timer +1
                    else:
                        #現在と異なる重力を選んでかつそのストックを持っていたら    
                        if g != g_inter and gflag[g_inter] == 1:
                            move_se.play()
                            gflag[g_inter] = 0
                            g = g_inter
                            change(g)
                        index = 2
                        timer = 0
            
                draw(screen, t_font, g_inter) 
                clock.tick(10)
        #ゲームオーバーとベストスコア更新
        if scene == 2:
            #画面を暗くする
            overlay = pygame.Surface((900, 680), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 240))
            screen.blit(overlay,[0,0])

            #記録の読み取り
            f = open('./data/text/bestrecord.txt','r',encoding='UTF-8')
            bests =f.read().splitlines()
            f.close()
            #例外処理の初期化
            if len(bests) != 3:
                bests=[str(0)]*3
            
            #ベストスコアの更新
            score = point
            first = True
            newrecord = 4
            for i in range(len(bests)):
                if score >= int(bests[i]):
                    if first:
                        first=False
                        newrecord = i
                    a=bests[i]
                    bests[i]=str(score)
                    score = int(a)
    
            #文字を描画
            rank =["1st ","2nd ","3rd "]
            for i in range(len(rank)):
                letter = m_font.render(rank[i], True, WHITE)
                screen.blit(letter,[300,100-letter.get_height()/2+100*i])
            for i in range(len(rank)):
                #記録を更新したら演出
                if i == newrecord:
                    letter = big_font.render(bests[i], True, WHITE)
                    screen.blit(letter,[420,100-letter.get_height()/2+100*i])
                    w =letter.get_width()
                    letter = h_font.render("New Record", True, WHITE)
                    screen.blit(letter,[440+w,100-letter.get_height()/2+100*i])
                else :
                    letter = m_font.render(bests[i], True, WHITE)
                    screen.blit(letter,[420,100-letter.get_height()/2+100*i])
            
            #今回のスコアを表示
            letter = big_font.render("Score: " + str(point), True, WHITE)
            screen.blit(letter,[450-letter.get_width()/2,400])
            #UIを表示
            letter = m_font.render("[R]etry", True, WHITE)
            screen.blit(letter,[425-letter.get_width(),500])
            letter = m_font.render("[T]itle", True, WHITE)
            screen.blit(letter,[475,500])

            
            
            #セーブのために形式を整える
            for i in range(len(bests)):
                bests[i]=bests[i]+"\n"
            #セーブ
            f = open('./data/text/bestrecord.txt','w',encoding='UTF-8')
            f.writelines(bests)
            f.close()
            pygame.display.update()

            #一時停止
            while scene==2:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                key = pygame.event.pump()
                key = pygame.key.get_pressed()
                #リトライ
                if key[K_r]==1:
                    title_se.play()
                    scene = 1
                if key[K_t]==1:
                    title_se.play()
                    scene = 0


                pygame.display.update()
        
        

if __name__ =='__main__':
    main()