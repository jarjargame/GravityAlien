import pygame
import sys
import random
import time
from pygame.locals import *

#Widthは偶数にする
WIDTH = 10

BLACK = (0,0,0)
GRAY = (50,50,50)
WHITE = (255,255,255)
BLUE = (0,90,255)
dBLUE = (0,18,51)
ORANGE =(246,170,0)
dORANGE = (45,34,0)
RED = (255,75,0)
dRED = (51,15,0)
GREEN = (3,175,122)
dGREEN = (1,35,24)

#落ちる方向を決めるときに使う。以降基本的に0,1,2,3,4をそれぞれ下、上、右、左、移動なしを示すものとする
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


def create_ob(gra):
    global obx, oby, cc
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
    if gra < 2:
        for i in range(WIDTH):
            if matrix[oby][i] != 4:
                GAMEOVER = True
    else :
        for i in range(WIDTH):
            if matrix[i][obx] != 4:
                GAMEOVER = True
    #ランダムにオブジェクトを生成
    if GAMEOVER == False:
        #1周目
        if cc == 0:
            random.shuffle(obinf)
            matrix[oby][obx] = obinf[0]
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = obinf[1]
            cc =cc + 1
        #2周目
        else:
            matrix[oby][obx] = obinf[2]
            matrix[oby+vector_x[gra]][obx+vector_y[gra]] = obinf[3]
            cc = 0
    else:
        print("game_over")
        pygame.quit()
        sys.exit()


 #オブジェクトを左右に動かす       
def move(gra, vkey):
    global obx, oby, timer
    #キーと重力が一致する時即座にdrop1に移行
    if gra == vkey :
        timer = 10
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
    global obx, oby
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
    return flg

#全体を落とす
def drop2(gra):
    flg = False
    #重力が下か上だったら
    if gra < 2:
        for y in range((WIDTH-2)*(1-gra)+gra,(-1+gra)+WIDTH*gra,-1+2*gra) : #重力に逆らうような順でmatrixを更新する
            for x in range(WIDTH):
                if matrix[y][x] != 4 and matrix[y+vector_y[gra]][x+vector_x[gra]] == 4:
                    matrix[y+vector_y[gra]][x+vector_x[gra]] = matrix[y][x]
                    matrix[y][x] = 4
                    flg = True
    else:
        for x in range((WIDTH-2)*(3-gra)+(gra-2), (gra-3)+WIDTH*(gra-2),-5+2*gra): #重力に逆らうような順でmatrixを更新する
            for y in range(WIDTH):
                if matrix[y][x] != 4 and matrix[y+vector_y[gra]][x+vector_x[gra]] == 4:
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
    
    if gra <2:
        for y in range(WIDTH):
            for x in range(1,WIDTH-1):
                if check[y][x] < 4:
                    if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                        gflag[check[y][x]] = 1
                        flag = True
                        matrix[y][x-1] = 5
                        matrix[y][x] = 5
                        matrix[y][x+1] = 5
    
    else:
        for y in range(1,WIDTH-1):
            for x in range(WIDTH):
                if check[y][x] < 4:
                    if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                        gflag[check[y][x]] = 1
                        flag = True
                        matrix[y-1][x] = 5
                        matrix[y][x] = 5
                        matrix[y+1][x] = 5
    
    return flag

#揃って黒くなったマスを消して、消した数をreturnする
def sweep():
    global timer
    delta = 0
    for y in range(WIDTH):
        for x in range(WIDTH):
            if matrix[y][x] == 5:
                delta = delta + 1
                matrix[y][x] = 4
    return delta




#マスと文字を描画
def draw(bg, fnt, gra_f):
    global point
    bg.fill((0,0,0))
    for y in range(WIDTH):
        for x in range(WIDTH):
            if matrix [y][x] == 4:
                pygame.draw.rect(bg, WHITE, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif matrix[y][x] == 5:
                pygame.draw.rect(bg, BLACK, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif matrix[y][x] == 0:
                pygame.draw.rect(bg, BLUE, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif matrix[y][x] == 1:
                pygame.draw.rect(bg, ORANGE, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif matrix[y][x] == 2:
                pygame.draw.rect(bg, RED, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
            elif matrix[y][x] == 3:
                pygame.draw.rect(bg, GREEN, [x*int(600/WIDTH), y*int(600/WIDTH),int(600/WIDTH)-1,int(600/WIDTH)-1],width=0)
    
    sur1 = fnt.render("nextgravity is ", True, WHITE)
    
    if gra_f == 0:
        sur2 = fnt.render(" Down ", True, BLUE)
    elif gra_f == 1:
        sur2 = fnt.render(" Up ", True, ORANGE)  
    elif gra_f == 2:
        sur2 = fnt.render(" Right ", True, RED)
    elif gra_f == 3:
        sur2 = fnt.render(" Left ", True, GREEN)

    if gflag[0] == 0:
        bg.blit(fnt.render("D", True, dBLUE), [650,90])
    else:
        bg.blit(fnt.render("D", True, BLUE), [650,90])

    if gflag[1] == 0:
        bg.blit(fnt.render("U", True, dORANGE), [680,90])
    else:
        bg.blit(fnt.render("U", True, ORANGE), [680,90])

    if gflag[2] == 0:
        bg.blit(fnt.render("R", True, dRED), [710,90])
    else:
        bg.blit(fnt.render("R", True, RED), [710,90])

    if gflag[3] == 0:
        bg.blit(fnt.render("L", True, dGREEN), [740,90])
    else:
        bg.blit(fnt.render("L", True, GREEN), [740,90])



    
    sur4 = fnt.render("Score: " + str(point), True, WHITE)
    bg.blit(sur1, [650,30])
    bg.blit(sur2, [670,60])
    bg.blit(sur4, [670,120])
    pygame.display.update()
            
    

index = 0
timer = 0
count = 0
point = 0

def main():
    global index, timer, count, point
    #pygame初期化
    pygame.init()
    #ウインドウサイズを決定
    pygame.display.set_caption("試作３")
    screen = pygame.display.set_mode((800, 680))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 30)
    screen.fill((0,0,0))
    for y in range(14):
        for x in range(14):
                pygame.draw.rect(screen, WHITE, [x*45, y*45,44,44],width=0)
    pygame.display.update()
    key_flg = 4

    #重力と重力フラグ
    g = 0
    g_inter = 0
    
    while True:
        #ウィンドウを閉じる処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #落下物生成
        if index == 0:
            create_ob(g)
            index = 1
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
                g_inter = 0
            elif key[K_w] == 1:
                g_inter = 1
            elif key[K_d] == 1:
                g_inter = 2
            elif key[K_a] == 1:
                g_inter = 3
            move(g, key_flg)
            if timer < 9:
                timer = timer + 1
            #timer = 10の時オブジェクトを下に落下.難易度調整でここが短くなる予定
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
            #揃っていたら２周後に削除しポイント加算。
            elif timer == 2:
                dp = sweep()
                point = point + dp
                timer = 0
                index = 2
            else:
                timer = timer + 1
  
        #重力変化
        if index == 4:
            if timer < 3:
                timer = timer +1
            else:
                #現在と異なる重力を選んでかつそのストックを持っていたら    
                if g != g_inter and gflag[g_inter] == 1:
                    gflag[g_inter] = 0
                    g = g_inter
                index = 2
                timer = 0
        
        draw(screen, font, g_inter) 
        clock.tick(10)
        
        

if __name__ =='__main__':
    main()