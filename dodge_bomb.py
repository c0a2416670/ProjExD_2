import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  #練習１
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_RIGHT:(5,0),
    pg.K_LEFT:(-5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:  # 練習３
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate



def gameover(screen: pg.Surface) -> None:  # 演習１
    fonto = pg.font.Font(None, 80)

    haikei = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(haikei, (0, 0, 0), pg.Rect(0,0,WIDTH,HEIGHT))
    haikei.set_alpha(100)
    screen.blit(haikei,[0,0])

    txt = fonto.render("GAME OVER", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(txt,txt_rct)

    koukaton = pg.image.load("./fig/8.png")
    koukaton_rct = koukaton.get_rect()
    koukaton_rct.center = WIDTH/4,HEIGHT/2
    koukaton2_rct = koukaton.get_rect()
    koukaton2_rct.center = WIDTH/1.35,HEIGHT/2
    screen.blit(koukaton,koukaton_rct)
    screen.blit(koukaton,koukaton2_rct)
    pg.display.update()
    time.sleep(5)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾初期化
    bb_img = pg.Surface((20, 20))  # 練習２
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0,HEIGHT)
    bb_img.set_colorkey((0,0,0))
    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0

    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 


        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectが重なっていたら
            gameover(screen)  # 練習４
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():  # 練習１
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右
                sum_mv[1] += mv[1]  # 上下

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):  # 画面外なら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])  # 画面内に戻す

        bb_rct.move_ip(vx,vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1 
        # bb_imgs, bb_accs = init_bb_imgs()
        # avx = vx*bb_accs[min(tmr//500, 9)]
        # bb_img = bb_imgs[min(tmr//500, 9)]

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        tmr += 1
        pg.display.update()
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
