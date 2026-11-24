import pygame 
import math
import random

width = 960
height = 722
mapa = []

abelha_frames = []
abelha_anim_frame = 0
abelha_anim_time = 0
direcao_abelha = "direita"

tempo_cooldown = 10000
tempo_decorrido = 10000
duracao_boost = 500
tempo_boost_ativo = 0

px = 0
py = 0

vidas = 3
tempo_restante = 90000
pontos = 0
entregues = 0
estado = "jogando"
carregando_polen = False
flores_vazias = {}

sapos = []
comprimento_lingua = 3
tempo_lingua = 2000

aranhas = []
velocidade_aranha = 0.06   
alcance_aranha = 3         

invencivel = 0
tempo_invencivel = 1500

def load_map(filename):
    global mapa,px,py,sapos,aranhas
    sapos = []
    mapa = []
    aranhas = []
    with open(filename) as file:
        i = 0
        for line in file:
            line = line.strip()
            if line:
                mapa.append([])
                for j in range(len(line)):
                    mapa[i].append(line[j])
                    if line[j] == "P":
                        px = j * 48
                        py = (i * 48) + 50
                    if line[j] == "S":
                        sapos.append({"i": i, "j": j, "esticada": False,"timer": random.randint(2000, 5000), "direcao": "esquerda"})
                    if line[j] == "A":
                        aranhas.append({"i": i, "j": j, "offset": 0, "dir": 1, "max": 0})
                i+=1
    for a in aranhas:
        livres = 0
        for k in range(1, alcance_aranha + 1):
            ni = a["i"] + k
            if ni >= len(mapa) or mapa[ni][a["j"]] == "#":
                break
            livres += 1
        a["max"] = livres * 48
                 

def load():
    global clock, arbusto, grama, abelha_1, abelha_2, abelha_com_polen, aranha_1, aranha_2, colmeia, coracao, fio, flor, flor_vazia
    global lingua_meio, lingua_ponta, sapo_1, sapo_2, px, py, fonte, coracao_pequeno, fonte_grande, som_vitoria, som_derrota, som_dano
    clock = pygame.time.Clock()
    load_map("mapa.txt")
    
    arbusto = pygame.image.load("Imagens/arbusto.png")
    grama = pygame.image.load("Imagens/grama.png")
    
    abelha_frames.append(pygame.image.load("Imagens/abelha_1.png"))
    abelha_frames.append(pygame.image.load("Imagens/abelha_2.png"))
    
    abelha_com_polen = pygame.image.load("Imagens/abelha_com_polen.png")
    aranha_1 = pygame.image.load("Imagens/aranha_1.png")
    aranha_2 = pygame.image.load("Imagens/aranha_2.png")
    colmeia = pygame.image.load("Imagens/colmeia.png")
    coracao = pygame.image.load("Imagens/coracao.png")
    fio = pygame.image.load("Imagens/fio.png")
    flor = pygame.image.load("Imagens/flor.png")
    flor_vazia = pygame.image.load("Imagens/flor_vazia.png")
    lingua_meio = pygame.image.load("Imagens/lingua_meio.png")
    lingua_ponta = pygame.image.load("Imagens/lingua_ponta.png")
    sapo_1 = pygame.image.load("Imagens/sapo_1.png")
    sapo_2 = pygame.image.load("Imagens/sapo_2.png")    
    
    coracao_pequeno = pygame.transform.scale(coracao, (32, 32))
    fonte = pygame.font.SysFont("arial", 24, bold=True)
    fonte_grande = pygame.font.SysFont("arial", 110, bold=True)
    
    pygame.mixer.music.load("Sons/Musica_fundo.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    som_vitoria = pygame.mixer.Sound("Sons/vitoria.mp3")
    som_vitoria.set_volume(0.8)
    
    som_derrota = pygame.mixer.Sound("Sons/derrota.mp3")
    som_derrota.set_volume(0.8)
    
    som_dano = pygame.mixer.Sound("Sons/dano.mp3")
    som_dano.set_volume(0.8)
def check_box_collision(x1, y1, w1, h1, x2, y2, w2, h2):
   return (x1 < x2 + w2) and (x2 < x1 + w1) and (y1 < y2 + h2) and (y2 < y1 + h1)    

def draw_hud(screen):
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, width, 50))
    
    for i in range(vidas):
        screen.blit(coracao_pequeno, (10 + i * 40, 9))
    
    segundos = math.ceil(tempo_restante/1000)
    if segundos <= 10:
       cor = (255, 80, 80)
    else:
        cor = (255, 255, 255)
    
    txt_tempo = fonte.render(f"Tempo: {segundos}s", True, cor)
    screen.blit(txt_tempo, (width//2 - txt_tempo.get_width() // 2, 12))
    
    txt_pontos = fonte.render(f"Pontos: {pontos} Pólens: {entregues}/10", True, (255, 255, 255))
    screen.blit(txt_pontos, (width - txt_pontos.get_width() - 10, 12))

def reiniciar():
    global vidas, tempo_restante, pontos, entregues, estado, tempo_decorrido, tempo_boost_ativo, direcao_abelha,carregando_polen,invencivel
    vidas = 3
    tempo_restante = 90000
    pontos = 0
    entregues = 0
    estado = "jogando"
    tempo_decorrido = tempo_cooldown
    tempo_boost_ativo = 0
    direcao_abelha = "direita"
    load_map("mapa.txt")
    carregando_polen = False
    flores_vazias.clear()
    invencivel = 0
    
    som_derrota.stop()
    som_vitoria.stop()
    pygame.mixer.music.play(-1)

def draw_game_over(screen):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))
    
    txt = fonte_grande.render("GAME OVER", True, (255,60,60))
    screen.blit(txt, (width // 2 - txt.get_width() // 2, height // 2 - txt.get_height() // 2 - 30))
    
    txt_reiniciar = fonte.render("Aperte R para reiniciar", True, (255, 255, 255))
    screen.blit(txt_reiniciar, (width // 2 - txt_reiniciar.get_width() // 2,  height // 2 + 60))
    

def coletar_e_entregar():
    global carregando_polen, pontos, entregues, estado
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            carac = mapa[i][j]
            if carac == "F" and not carregando_polen:
                if check_box_collision(px + 8, py + 8, 32, 32, j * 48, (i*48) + 50, 48, 48):
                    mapa[i][j] = "."
                    carregando_polen = True
                    nova = achar_posicao_livre()
                    if nova:
                        ni, nj = nova
                        mapa[ni][nj] = "f"
                        flores_vazias[(ni, nj)] = random.randint(5000, 15000)
                    return
            elif carac == "H" and carregando_polen:
                if check_box_collision(px + 8, py + 8, 32, 32, j * 48, (i*48) + 50, 48, 48):
                    carregando_polen = False
                    pontos += 100
                    entregues += 1
                    if entregues >= 10:
                       estado = "vitoria"
                       pygame.mixer.music.stop()
                       som_vitoria.play()
                    return
               
def draw_polen(screen):
    if carregando_polen:
        centro = (int(px + 24), int(py + 38))
        pygame.draw.circle(screen, (255, 215, 0), centro, 8)
        pygame.draw.circle(screen, (180, 140, 0), centro, 8, 2)

def achar_posicao_livre():
    livres = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] not in ("#", "F", "f", "H", "A", "S", "P"):
                livres.append((i, j))
    if livres:
        return random.choice(livres)
    return None

def atualizar_flores(dt):
   global flores_vazias
   ainda_vazias = {}
   for pos, tempo in flores_vazias.items():
       tempo -= dt
       if tempo <= 0:
           i, j = pos
           mapa[i][j] = "F"
       else:
           ainda_vazias[pos] = tempo
   flores_vazias = ainda_vazias

def posicoes_lingua(s):
    direcoes = {"direita": (0, 1), "esquerda": (0, -1), "cima": (-1, 0), "baixo": (1, 0)}
    di, dj = direcoes[s["direcao"]]
    posicoes = []
    for k in range(1, comprimento_lingua + 1):
        ni = s["i"] + di * k
        nj = s["j"] + dj * k
        if ni < 0 or ni >= len(mapa) or nj < 0 or nj >= len(mapa[ni]):
            break
        if mapa[ni][nj] == "#":
            break   
        posicoes.append((nj * 48, ni * 48 + 50))
    return posicoes

def atualizar_sapos(dt):
    for s in sapos:
        s["timer"] -= dt
        if s["timer"] <= 0:
            if s["esticada"]:
                s["esticada"] = False
                s["timer"] = random.randint(2000, 5000)
            else:
                s["esticada"] = True
                s["direcao"] = random.choice(["esquerda", "direita", "cima", "baixo"])
                s["timer"] = tempo_lingua

def draw_sapos(screen):
    angulos = {"direita": 0, "cima": 90, "esquerda": 180, "baixo": 270}
    for s in sapos:
        x = s["j"] * 48
        y = s["i"] * 48 + 50
        if s["esticada"]:
            screen.blit(sapo_2, (x, y))
            posicoes = posicoes_lingua(s)
            for n, (lx, ly) in enumerate(posicoes):
                if n == len(posicoes) - 1:
                    img = lingua_ponta
                else:
                    img = lingua_meio
                img = pygame.transform.rotate(img, angulos[s["direcao"]])
                screen.blit(img, (lx, ly))
        else:
            screen.blit(sapo_1, (x, y))

def atualizar_aranhas(dt):
    for a in aranhas:
        a["offset"] += a["dir"] * velocidade_aranha * dt
        if a["offset"] >= a["max"]:
            a["offset"] = a["max"]
            a["dir"] = -1
        elif a["offset"] <= 0:
            a["offset"] = 0
            a["dir"] = 1

def draw_aranhas(screen):
    frame = (pygame.time.get_ticks() // 300) % 2
    if frame == 0:
        img = aranha_1
    else:
        img = aranha_2

    for a in aranhas:
        x = a["j"] * 48
        topo = a["i"] * 48 + 50
        y = topo + a["offset"]

        yy = topo
        while yy < y:
            screen.blit(fio, (x, yy))
            yy += 48

        screen.blit(img, (x, y))

def levar_dano():
    global vidas, carregando_polen, invencivel, estado
    if invencivel > 0:
        return
    vidas -= 1
    carregando_polen = False     
    invencivel = tempo_invencivel
    if vidas <= 0:
        vidas = 0
        estado = "derrota"
        som_derrota.play()
        pygame.mixer.music.stop()
    else:
        som_dano.play()
    
def checar_dano():
    abelha = (px + 8, py + 8, 32, 32)

    for s in sapos:
        if check_box_collision(*abelha, s["j"] * 48 + 6, s["i"] * 48 + 50 + 6, 36, 36):
            levar_dano()
            return
        if s["esticada"]:
            for lx, ly in posicoes_lingua(s):
                if check_box_collision(*abelha, lx + 12, ly + 12, 24, 24):
                    levar_dano()
                    return

    for a in aranhas:
        x = a["j"] * 48
        topo = a["i"] * 48 + 50
        y = topo + a["offset"]
        if check_box_collision(*abelha, x + 6, y + 6, 36, 36):
            levar_dano()
            return
        if check_box_collision(*abelha, x + 22, topo, 4, a["offset"]):
            levar_dano()
            return

def draw_vitoria(screen):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    txt = fonte_grande.render("VOCÊ VENCEU!", True, (255, 215, 0))
    screen.blit(txt, (width // 2 - txt.get_width() // 2,
                      height // 2 - txt.get_height() // 2 - 50))

    info = fonte.render(f"Pontuação final: {pontos}", True, (255, 255, 255))
    screen.blit(info, (width // 2 - info.get_width() // 2, height // 2 + 30))

    sub = fonte.render("Aperte R para reiniciar", True, (255, 255, 255))
    screen.blit(sub, (width // 2 - sub.get_width() // 2, height // 2 + 75))

def update(dt):
    global px,py,abelha_anim_frame,abelha_anim_time,direcao_abelha,tempo_decorrido, tempo_boost_ativo, tempo_restante,estado,carregando_polen,pontos,entregues, invencivel
    
    if estado != "jogando":
        if pygame.key.get_pressed()[pygame.K_r]:
            reiniciar()
        return
    
    if invencivel > 0:
        invencivel -= dt
    
    keys = pygame.key.get_pressed()
    movendo = False
    velocidade = 0.1
    
    if tempo_restante > 0:
        tempo_restante -= dt
        if tempo_restante <= 0:
            tempo_restante = 0
            if entregues < 10:
                estado = "derrota"
                som_derrota.play()
                pygame.mixer.music.stop()
                return
    
    if tempo_decorrido < tempo_cooldown:
        tempo_decorrido += dt
    
    if tempo_boost_ativo > 0:
        tempo_boost_ativo += dt
        if tempo_boost_ativo > duracao_boost:
            tempo_boost_ativo = 0
    
    if keys[pygame.K_SPACE]:
        if tempo_decorrido >= tempo_cooldown:
            tempo_decorrido = 0
            tempo_boost_ativo = 0.1
    
    if tempo_boost_ativo > 0:
        velocidade = 0.25
    
    novo_x = px
    novo_y = py
    
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        novo_x += velocidade * dt
        direcao_abelha = "direita"
        movendo = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        novo_x -= velocidade * dt
        direcao_abelha = "esquerda"
        movendo = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        novo_y -= velocidade * dt
        movendo = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        novo_y += velocidade * dt
        movendo = True
    
    
    colidiu_x = False
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "#":
                if check_box_collision(novo_x + 8, py + 8, 32, 32, j * 48, (i*48) + 50, 48, 48):
                    colidiu_x = True
                    break
        if colidiu_x:
            break
    if not colidiu_x:
        px = novo_x
        
    colidiu_y = False
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "#":
                if check_box_collision(px + 8, novo_y + 8, 32, 32, j * 48, (i*48) + 50, 48, 48):
                    colidiu_y = True
                    break
        if colidiu_y:
            break
    if not colidiu_y:
        py = novo_y
    
    coletar_e_entregar()
    atualizar_flores(dt)
    atualizar_sapos(dt)
    atualizar_aranhas(dt)
    checar_dano()
    
    if movendo:
        abelha_anim_time += dt
        if abelha_anim_time >= 150:
            abelha_anim_frame += 1
            if abelha_anim_frame >= 2:
                abelha_anim_frame = 0
            abelha_anim_time = 0
    else:
        abelha_anim_frame = 0
        abelha_anim_time = 0
            
def draw_screen(screen):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "#":
                screen.blit(arbusto, ((j * 48), (i * 48) + 50))
            else:
                screen.blit(grama, ((j * 48), (i * 48)+ 50))
                if mapa[i][j] == "F":
                    screen.blit(flor, ((j * 48), (i * 48)+ 50))
                elif mapa[i][j] == "f":
                    screen.blit(flor_vazia, ((j * 48), (i * 48)+ 50))
                elif mapa[i][j] == "H":
                    screen.blit(colmeia, ((j * 48), (i * 48)+ 50))
    
    draw_sapos(screen)
    draw_aranhas(screen)
    imagem_atual = abelha_frames[abelha_anim_frame]
    
    if direcao_abelha == "esquerda":
        imagem_atual = pygame.transform.flip(imagem_atual, True, False)
    
    if invencivel > 0 and (invencivel // 100) % 2 == 0:
        piscando = True
    else:
        piscando = False
    
    if not piscando:
        screen.blit(imagem_atual, (px, py))
        draw_polen(screen)
    
    draw_hud(screen)
    
    if estado == "derrota":
        draw_game_over(screen)
    elif estado == "vitoria":
        draw_vitoria(screen)
    
def main_loop(screen):  
    global clock
    running = True
    while running:
        for e in pygame.event.get(): 
            if e.type == pygame.QUIT:
                running = False
                break

        clock.tick(60)        
        dt = clock.get_time()
        draw_screen(screen)
        update(dt)
        pygame.display.update() 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Abelha Coletora")
load()
main_loop(screen)
pygame.quit()    
    
    