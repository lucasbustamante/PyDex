# Importing Modules
import pygame
from pygame import gfxdraw
from pygame.locals import *
from threading import Thread
import time
import random
import sys
import sqlite3
import os
import math

from CButton import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text
from CUserInterface import UI

import CText

from io import StringIO

class DexCarta:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

    running = True
    reload = True
    selectionMade = False
    selectedOption = None
    serie = "#0001"

    selectedScreen = 1



    def Show():
   
#########################################################################################
#   INICIALIZAÇÃO E CONFIGURAÇÃO                                                        #
#########################################################################################

        # PyGame Inicialização
        clock = pygame.time.Clock()

        # Inicialização de janela e superfície
        displayWidth = 800
        displayHeight = 480

        idleCtr = 0

        flags = FULLSCREEN | DOUBLEBUF

        try:
            if os.uname()[1] == 'raspberrypi': 
                mainSurface = pygame.display.set_mode((0,0),flags)
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            else: 
                mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
                pygame.mouse.set_visible(True)
        except:
            mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
            pygame.mouse.set_visible(True)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

#########################################################################################
#   DEFINICOES DO MENU INICIAL                                                          #
#########################################################################################

        fadeOutCtr = 0

#espessura bordas
        borderWidth = 5
#cor linhas iniciais
        borderColor = (255,0,0)
#cor da caixa de menu
        infillColor = (20,20,20)
#fonte tela inicial
        fontColor = (255,255,255)
#fundo tela inicial
        backColor = (0,0,0)
#angulo de raio
        radius = 20
#distancia dos circulos
        sectionPadding = 12
#correcao de borda
        borderCorrection = 1
#tamanho da fonte
        fontSize = 35
#tamanho menu circular
        centerRadius = 130
 # Tempo para uso
        repressCooldown = 10

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################

        while DexCarta.running:

            DexCarta.reload = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexCarta.reload:

                # Event Processing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Keypress Processing
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q] != 0: 
                    pygame.quit()
                    sys.exit()

                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                
                #cor fundo principal
                mainSurface.fill((0,0,0))

#########################################################################################
#   Pydex                                                                               #
#########################################################################################            
                
                if DexCarta.selectedScreen == 1:

                    boxOffset1 = 0
                    boxOffset2 = 0
                    boxOffset3 = 0
                    boxOffset4 = 0
                    boxOffset5 = 0
                    
                    boxWidth = int(266.66 - 2*10)
                    boxHeight = 240-2  *10

                    btnColorCenter = infillColor
                    btnColorTopLeft = infillColor
                    btnColorTopRight = infillColor
                    btnColorBottomLeft = infillColor
                    btnColorBottomRight = infillColor

                    btnFontCenter = fontColor
                    btnFontTopLeft = fontColor
                    btnFontTopRight = fontColor
                    btnFontBottomLeft = fontColor
                    btnFontBottomRight = fontColor
                                
                if DexCarta.selectedScreen == 1:
                    
                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    

                    
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        
                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 160 and 0 < mouse[1] < 55: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexCarta.selectionMade = True
                                DexCarta.selectedOption = 1

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexCarta.selectionMade = True
                                DexCarta.selectedOption = 2
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexCarta.selectionMade = True
                                DexCarta.selectedOption = 3

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexCarta.selectionMade = True
                                DexCarta.selectedOption = 4

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexCarta.selectionMade = True
                                DexCarta.selectedOption = 5

                                      
                    
                    #topico
                    Draw.RoundRect(mainSurface,(20,20,20),(20,27,760,5),2,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(40,40,40),(250,10,300,40),5,2,(255,0,0))
                    Text.Write(mainSurface,(400,30),"Cartão de Treinador",fontSize-10,"joy.otf",btnFontMore2,True)
                    #logo
                    #Draw.Pokeball(mainSurface,(40,50),(255,0,0),(10,10,10))
                    #Voltar
                    Draw.RoundRect(mainSurface,(40,40,40),(20,40,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(72,58),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #foto
                    Draw.RoundRect(mainSurface,(40,40,40),(25,100,160,160),5,4,(255,0,0))
                                                            
                    #Carimbo
                    logoSurface = pygame.Surface((1500,1000)).convert_alpha()
                    logoImg = pygame.image.load("carimbopt2.png").convert_alpha()
                    runtimeCtr = 0
                    click = pygame.mouse.get_pressed()
                    if click[0] == 0:
                        run = False
                    logoSurface.fill((0,0,0))
                    logoSurface.set_colorkey((0,0,0))
                    if runtimeCtr % 2 == 0: logoSurface.blit(logoImg,(0,0))
                    else: logoSurface.blit(logoImg,(-600,0))
                    mainSurface.blit(logoSurface,(110,200))
                    
                    #nome
                    nome = "Lucas da Costa Bustamante"
                    if (nome.count('') -1) ==1:
                        d = 310
                    elif (nome.count('') -1) ==2:
                        d = 160
                    elif (nome.count('') -1) ==3:
                        d = 110
                    elif (nome.count('') -1) ==4:
                        d = 83
                    elif (nome.count('') -1) ==5:
                        d = 68
                    elif (nome.count('') -1) ==6:
                        d = 58
                    elif (nome.count('') -1) ==7:
                        d = 52
                    elif (nome.count('') -1) ==8:
                        d =  46
                    elif (nome.count('') -1) ==9:
                        d = 42
                    elif (nome.count('') -1) ==10:
                        d = 39
                    elif (nome.count('') -1) ==11:
                        d = 36
                    elif (nome.count('') -1) ==12:
                        d = 34
                    elif (nome.count('') -1) ==13:
                        d = 32
                    elif (nome.count('') -1) ==14:
                        d = 30
                    elif (nome.count('') -1) ==15:
                        d = 28.5
                    elif (nome.count('') -1) ==16:
                        d = 27.5
                    elif (nome.count('') -1) ==17:
                        d = 26
                    elif (nome.count('') -1) ==18:
                        d = 25
                    elif (nome.count('') -1) ==19:
                        d = 24.3
                    elif (nome.count('') -1) ==20:
                        d = 23.5
                    elif (nome.count('') -1) ==21:
                        d = 23
                    elif (nome.count('') -1) ==22:
                        d = 22.2
                    elif (nome.count('') -1) ==23:
                        d = 21.2
                    elif (nome.count('') -1) ==24:
                        d = 21
                    elif (nome.count('') -1) ==25:
                        d = 20.6
                    elif (nome.count('') -1) ==26:
                        d = 20.2
                    elif (nome.count('') -1) ==27:
                        d = 19.8
           
                   
                    tamanho = 17 * (nome.count('') -1)
                    distancia = d * (nome.count('') -1)

                    
                    Draw.RoundRect(mainSurface,(20,20,20),(270,105,tamanho+(50),30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,85,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,100),"Nome",fontSize-10,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(distancia,120),nome,fontSize-10,"joy.otf",(255,255,255),True)

                    #idade
                    
                    from datetime import date
                    ano_anos = "anos"
                    india = 1
                    inmes = 5
                    inano = 1900
                    data = date.today()
                    mes = int('{}'.format(data.month))
                    dia = int('{}'.format(data.day))
                    ano = int('{}'.format(data.year))
                    
                    if ano - inano <= 1:
                        ano_anos = "ano"
                    if mes < inmes:
                        data = ano - inano - 1
                    elif mes == inmes and dia < india:
                        data = ano - inano - 1
                    elif inmes <= mes:
                        data = ano - inano
                                   
                    Draw.RoundRect(mainSurface,(20,20,20),(270,170,200,30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,150,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,165),"Idade",fontSize-10,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(370,185),str(data) + " " + ano_anos,fontSize-10,"joy.otf",(255,255,255),True)

                    #regiao
                    regiao = "São Paulo"
                    if (regiao.count('') -1) ==1:
                        d2 = 310
                    elif (regiao.count('') -1) ==2:
                        d2 = 160
                    elif (regiao.count('') -1) ==3:
                        d2 = 110
                    elif (regiao.count('') -1) ==4:
                        d2 = 83
                    elif (regiao.count('') -1) ==5:
                        d2 = 68
                    elif (regiao.count('') -1) ==6:
                        d2 = 58
                    elif (regiao.count('') -1) ==7:
                        d2 = 52
                    elif (regiao.count('') -1) ==8:
                        d2 =  46
                    elif (regiao.count('') -1) ==9:
                        d2 = 42
                    elif (regiao.count('') -1) ==10:
                        d2 = 39
                    elif (regiao.count('') -1) ==11:
                        d2 = 36
                    elif (regiao.count('') -1) ==12:
                        d2 = 34
                    elif (regiao.count('') -1) ==13:
                        d2 = 32
                    elif (regiao.count('') -1) ==14:
                        d2 = 30
                    elif (regiao.count('') -1) ==15:
                        d2 = 28.5
                    elif (regiao.count('') -1) ==16:
                        d2 = 27.5
                    elif (regiao.count('') -1) ==17:
                        d2 = 26
                    elif (regiao.count('') -1) ==18:
                        d2 = 25
                    elif (regiao.count('') -1) ==19:
                        d2 = 24.3
                    elif (regiao.count('') -1) ==20:
                        d2 = 23.5
                    elif (regiao.count('') -1) ==21:
                        d2 = 23
                    elif (regiao.count('') -1) ==22:
                        d2 = 22.2
                    elif (regiao.count('') -1) ==23:
                        d2 = 21.2
                    elif (regiao.count('') -1) ==24:
                        d2 = 21
                    elif (regiao.count('') -1) ==25:
                        d2 = 20.6
                    elif (regiao.count('') -1) ==26:
                        d2 = 20.2
                    elif (regiao.count('') -1) ==27:
                        d2 = 19.8
           
                   
                    tamanho2 = 17 * (regiao.count('') -1)
                    distancia2 = d2 * (regiao.count('') -1)

                    
                    Draw.RoundRect(mainSurface,(20,20,20),(270,240,tamanho2+(50),30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,220,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,235),"Região",fontSize-14,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(distancia2,255),regiao,fontSize-10,"joy.otf",(255,255,255),True)

                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                                        
                    #Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))
                  
                    

                    if DexCarta.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexCarta.selectionMade=False
                            from DexHome import DexHome
                            if DexCarta.selectedOption == 1: pass
                            if DexCarta.selectedOption == 2: pass
                            if DexCarta.selectedOption == 3: pass
                            if DexCarta.selectedOption == 4: pass
                            if DexCarta.selectedOption == 5: pass
                            

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

                # Update Screen
                pygame.display.update()
                clock.tick(60)

        DexCarta.running = True
        return