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

import CText

from DexMenu import DexMenu
from DexCarta import DexCarta

#########################################################################################
# Variaveis de Traducao                                                                 #
#########################################################################################

botaocentral = "Pokédex"
botao1 = "Itens"
botao2 = "--"
botao3 = "--"
botao4 = "Mais >"
botao5 = "< Voltar"
botao6 = "--"
botao7 = "Cartão"
botao7_2 = "de"
botao7_3 = "Treinador"
botao8 = "--"
botao9 = "Atualizar"
botao10 = "Sobre"


class DexHome:

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

    selectedScreen = 1

#########################################################################################
#   FUNCTIONS                                                                           #
#########################################################################################


#########################################################################################
#   TOGGLE FUNCTIONS                                                                    #
#########################################################################################



#########################################################################################
#########################################################################################
#   MAIN START                                                                          #
#########################################################################################
#########################################################################################

    def Show():
   
#########################################################################################
#   INICIALIZAÇÃO E CONFIGURAÇÃO                                                          #
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
#   TEMA ENTRADA                                                                        #
#########################################################################################         
        run = True

        pygame.draw.rect(mainSurface,(20,20,20),(0,0,800,480))
        #amplitude da tela
        logoSurface = pygame.Surface((1500,1000)).convert_alpha()
        logoImg = pygame.image.load("logo.png").convert_alpha()

        runtimeCtr = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            click = pygame.mouse.get_pressed()
            #opção de toque para liberar 0 == 1
            if click[0] == 0:
                run = False

            logoSurface.fill((20,20,20))
            logoSurface.set_colorkey((0,0,0))
            if runtimeCtr % 2 == 0: logoSurface.blit(logoImg,(0,0))
            else: logoSurface.blit(logoImg,(-600,0))
            #alinhamento da imagem
            mainSurface.blit(logoSurface,(0,150))
            Text.Write(mainSurface,(670,330),"V1.0.0",11,"calibrilight.ttf",(200,200,200),True)
            pygame.display.update()
            #time automatico
            time.sleep(3)
                
            #ativador de gif
            runtimeCtr += 1
            if runtimeCtr > 0: runtimeCtr = 0
            #velocidade
            clock.tick(20)



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

        while DexHome.running:

            DexHome.reload = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexHome.reload:

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
#   Tela 1                                                                              #
#########################################################################################               
                
                if DexHome.selectedScreen == 1:

                    boxOffset1 = 300
                    boxOffset2 = 360
                    boxOffset3 = 420
                    boxOffset4 = -420
                    boxOffset5 = -360
                    boxOffset6 = -300

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


                    if repressCooldown <= 0 and not DexHome.selectionMade:

                        # Button functionality
                        if 400-centerRadius < mouse[0] < 400+centerRadius and 240-centerRadius < mouse[1] < 240+centerRadius: 
                            btnColorCenter = (30,30,30)
                            btnFontCenter = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 1
                
                        if (0 < mouse[0] < 400 and 0 < mouse[1] < 240-centerRadius) or (0 < mouse[0] < 400-centerRadius and 0 < mouse[1] < 240): 
                            btnColorTopLeft = (30,30,30)
                            btnFontTopLeft = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 2

                        if (400 < mouse[0] < 800 and 0 < mouse[1] < 240-centerRadius) or (400+centerRadius < mouse[0] < 800 and 0 < mouse[1] < 240): 
                            btnColorTopRight = (30,30,30)
                            btnFontTopRight = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 3

                        if (0 < mouse[0] < 400 and 240+centerRadius < mouse[1] < 480) or (0 < mouse[0] < 400-centerRadius and 240 < mouse[1] < 480): 
                            btnColorBottomLeft = (30,30,30)
                            btnFontBottomLeft = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 4

                        if (400 < mouse[0] < 800 and 240+centerRadius < mouse[1] < 480) or (400+centerRadius < mouse[0] < 800 and 240 < mouse[1] < 480): 
                            btnColorBottomRight = (30,30,30)
                            btnFontBottomRight = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 5





                    # Top Left Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,sectionPadding+radius,radius,btnColorTopLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,400-sectionPadding-radius,sectionPadding+radius,radius,btnColorTopLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,240-sectionPadding-radius,radius,btnColorTopLeft,borderColor,borderWidth)

                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,sectionPadding+borderCorrection),(400-sectionPadding-radius,sectionPadding+borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+borderCorrection,sectionPadding+radius),(sectionPadding+borderCorrection,240-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,240-sectionPadding-borderCorrection),(800-sectionPadding-radius,240-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(400-sectionPadding-borderCorrection,sectionPadding+radius+borderCorrection),(400-sectionPadding-borderCorrection,480-sectionPadding-radius),borderWidth)
                
                    # Infills
                    pygame.draw.rect(mainSurface,btnColorTopLeft,(sectionPadding+borderWidth,sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorTopLeft,(sectionPadding+radius,sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Top Right Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,400+sectionPadding+radius,sectionPadding+radius,radius,btnColorTopRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,sectionPadding+radius,radius,btnColorTopRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,240-sectionPadding-radius,radius,btnColorTopRight,borderColor,borderWidth)
                
                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+radius,sectionPadding+borderCorrection),(800-sectionPadding-radius,sectionPadding+borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+borderCorrection,240+sectionPadding+radius),(sectionPadding+borderCorrection,480-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+borderCorrection,sectionPadding+radius+borderCorrection),(400+sectionPadding+borderCorrection,480-sectionPadding-radius),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorTopRight,(400+sectionPadding+borderWidth,sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorTopRight,(400+sectionPadding+radius,sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))


                    # Bottom Left Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,240+sectionPadding+radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,400-sectionPadding-radius,480-sectionPadding-radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,480-sectionPadding-radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                
                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,480-sectionPadding-borderCorrection),(400-sectionPadding-radius,480-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(800-sectionPadding-borderCorrection,sectionPadding+radius),(800-sectionPadding-borderCorrection,240-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,240+sectionPadding+borderCorrection),(800-sectionPadding-radius,240+sectionPadding+borderCorrection),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorBottomLeft,(sectionPadding+borderWidth,240+sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorBottomLeft,(sectionPadding+radius,240+sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Bottom Right Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,400+sectionPadding+radius,480-sectionPadding-radius,radius,btnColorBottomRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,480-sectionPadding-radius,radius,btnColorBottomRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,240+sectionPadding+radius,radius,btnColorBottomRight,borderColor,borderWidth)

                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+radius,480-sectionPadding-borderCorrection),(800-sectionPadding-radius,480-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(800-sectionPadding-borderCorrection,240+sectionPadding+radius),(800-sectionPadding-borderCorrection,480-sectionPadding-radius),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorBottomRight,(400+sectionPadding+borderWidth,240+sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorBottomRight,(400+sectionPadding+radius,240+sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Outer Segments Large Radius
                    Draw.AAFilledCircle(mainSurface,400,240,centerRadius+2*sectionPadding,backColor,borderColor,borderWidth)
                    pygame.draw.rect(mainSurface,backColor,(400-sectionPadding+borderCorrection,0,2*sectionPadding-borderCorrection,480))
                    pygame.draw.rect(mainSurface,backColor,(0,240-sectionPadding+borderCorrection,800,2*sectionPadding-borderCorrection))

                    # Center segment
                    Draw.AAFilledCircle(mainSurface,400,240,centerRadius,btnColorCenter,borderColor,borderWidth)


                    ##################################################################################
                    # Topicos do menu                                                                #
                    ##################################################################################
                    Text.Write(mainSurface,(400,240),botaocentral,fontSize,"joy.otf",btnFontCenter,True)

                    Text.Write(mainSurface,(170,120),botao1,fontSize,"joy.otf",btnFontTopLeft,True)

                    Text.Write(mainSurface,(645,120),botao2,fontSize,"joy.otf",btnFontTopRight,True)


                    Text.Write(mainSurface,(170,370),botao3,fontSize,"joy.otf",btnFontBottomLeft,True)

                    Text.Write(mainSurface,(645,370),botao4,fontSize,"joy.otf",btnFontBottomRight,True)

                    # fade entre telas
                    if DexHome.selectionMade:
                        if fadeOutCtr <= 1:
                            sectionPadding -= 1
                            centerRadius += 1
                        if fadeOutCtr > 1:
                            sectionPadding += 1
                            if centerRadius >= 2: centerRadius -= 3
                            if fontSize > 0: fontSize -= 1
                        if fadeOutCtr > 100:
                            fadeOutColor = (0,0,0)
                            Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 11:

                            sectionPadding = 10
                            fontSize = 35
                            centerRadius = 130
                            fadeOutCtr = 0
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 1: DexMenu.Show()
                            if DexHome.selectedOption == 2: pass
                            if DexHome.selectedOption == 3: pass
                            if DexHome.selectedOption == 4: pass
                            if DexHome.selectedOption == 5: DexHome.selectedScreen = 2

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   Mais >   Tela 2                                                                              #
#########################################################################################

                

                if DexHome.selectedScreen == 2:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)

                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 266 and 0 < mouse[1] < 240: 
                            btnColorMore1 = (30,30,30)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 266 < mouse[0] < 533 and 0 < mouse[1] < 240: 
                            btnColorMore2 = (30,30,30)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7

                        elif 533 < mouse[0] < 800 and 0 < mouse[1] < 240: 
                            btnColorMore3 = (30,30,30)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 266 and 240 < mouse[1] < 480: 
                            btnColorMore4 = (30,30,30)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 266 < mouse[0] < 533 and 240 < mouse[1] < 480:
                            btnColorMore5 = (30,30,30)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                        elif 533 < mouse[0] < 800 and 240 < mouse[1] < 480:
                            btnColorMore6 = (30,30,30)
                            btnFontMore6 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 11


                    Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)

                    Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)

                    Text.Write(mainSurface,(1*10+0*boxWidth+boxWidth/2,10+boxHeight/2),botao5,fontSize,"joy.otf",btnFontMore1,True)

                    Text.Write(mainSurface,(3*10+1*boxWidth+boxWidth/2,10+boxHeight/2),botao6,fontSize,"joy.otf",btnFontMore2,True)

                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,10+boxHeight/2-40),botao7,fontSize,"joy.otf",btnFontMore3,True)
                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,10+boxHeight/2),botao7_2,fontSize,"joy.otf",btnFontMore3,True)
                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,10+boxHeight/2+40),botao7_3,fontSize,"joy.otf",btnFontMore3,True)

                    Text.Write(mainSurface,(1*10+0*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2),botao8,fontSize,"joy.otf",btnFontMore4,True)
                    Text.Write(mainSurface,(3*10+1*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2),botao9,fontSize,"joy.otf",btnFontMore5,True)

                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2),botao10,fontSize,"joy.otf",btnFontMore6,True)


                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=5
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 2
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 1
                            if DexHome.selectedOption == 7: pass
                            if DexHome.selectedOption == 8: DexHome.selectedScreen = 20
                            if DexHome.selectedOption == 9: pass
                            if DexHome.selectedOption == 10: pass
                            if DexHome.selectedOption == 11: DexHome.selectedScreen = 11

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1
                    
#########################################################################################
#   Cartao                                                                              #
#########################################################################################

                
                serie = "0001"
                if DexHome.selectedScreen == 20:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 20 < mouse[0] < 110 and 40 < mouse[1] < 70: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 1

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                                           

                    #topico
                    Draw.RoundRect(mainSurface,(20,20,20),(20,27,760,5),2,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(40,40,40),(250,10,300,40),5,2,(255,0,0))
                    Text.Write(mainSurface,(400,30),"Cartão de Treinador",fontSize-10,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,(20,20,20),(250,100,530,250),5,2,(255,0,0))
                    
                    
                    #Draw.Pokeball(mainSurface,(40,50),(255,0,0),(10,10,10))
                    #Voltar
                    #Draw.RoundRect(mainSurface,(40,40,40),(20,40,105,35),5,2,(255,0,0))
                    #Text.Write(mainSurface,(72,58),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #foto
                    Draw.RoundRect(mainSurface,(40,40,40),(35,90,160,160),5,4,(255,0,0))                                  
                    #Carimbo
                    """logoSurface = pygame.Surface((1500,1000)).convert_alpha()
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
                    #editar
                    Draw.RoundRect(mainSurface,(40,40,40),(668,433,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(720,450),"Editar",fontSize-10,"joy.otf",btnFontMore3,True)"""
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

                    
                    Draw.RoundRect(mainSurface,(20,20,20),(270,145,tamanho+(50),30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,125,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,140),"Nome",fontSize-10,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(distancia,160),nome,fontSize-10,"joy.otf",(255,255,255),True)

                    #idade
                    
                    from datetime import date
                    ano_anos = "anos"
                    india = 23
                    inmes = 7
                    inano = 1994
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
                                   
                    Draw.RoundRect(mainSurface,(20,20,20),(270,210,200,30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,190,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,205),"Idade",fontSize-10,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(370,225),str(data) + " " + ano_anos,fontSize-10,"joy.otf",(255,255,255),True)

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

                    
                    Draw.RoundRect(mainSurface,(20,20,20),(270,280,tamanho2+(50),30),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(20,20,20),(210,260,80,30),5,2,(255,0,0))
                    Text.Write(mainSurface,(250,275),"Região",fontSize-14,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(distancia2,295),regiao,fontSize-10,"joy.otf",(255,255,255),True)

                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                                        
                    #Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))
                  
                    

                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 
                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False
                            if DexHome.selectedOption == 1: DexHome.selectedScreen = 2
                            if DexHome.selectedOption == 2: pass
                            if DexHome.selectedOption == 3: pass
                            if DexHome.selectedOption == 4: pass
                            if DexHome.selectedOption == 5: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   Pydex                                                                               #
#########################################################################################

                

                if DexHome.selectedScreen == 11:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 160 and 0 < mouse[1] < 55: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                                      

                    Draw.RoundRect(mainSurface,(0,0,0),(45,90,90,50),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(0,0,0),(11,120,160,250),5,2,(255,0,0))
                    #Topico
                    Text.Write(mainSurface,(90,105),"Sobre",fontSize-10,"joy.otf",(255,0,0),True)
                    #Voltar
                    Draw.RoundRect(mainSurface,(40,40,40),(13,22,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(65,40),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #Sobre
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"PyDex",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,btnColorMore2,(170,15,620,445),radius,borderWidth,borderColor)
                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                    #Pydex
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"PyDex",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,(40,40,40),(20,130,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,155),"Pydex",fontSize,"joy.otf",btnFontMore2,True)
                    ##Criadores
                    Draw.RoundRect(mainSurface,(40,40,40),(20,190,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,215),"Criadores",fontSize-12,"joy.otf",btnFontMore3,True)
                    #Parceiros
                    Draw.RoundRect(mainSurface,(40,40,40),(20,250,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,275),"Parceiros",fontSize-12,"joy.otf",btnFontMore4,True)
                    #Botao4
                    Draw.RoundRect(mainSurface,(40,40,40),(20,310,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,335),"Livre",fontSize,"joy.otf",btnFontMore5,True)
                    
                    Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))
                  
                    

                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            #Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 2
                            if DexHome.selectedOption == 7: DexHome.selectedScreen = 11
                            if DexHome.selectedOption == 8: DexHome.selectedScreen = 8
                            if DexHome.selectedOption == 9: DexHome.selectedScreen = 9
                            if DexHome.selectedOption == 10: DexHome.selectedScreen = 10
                            if DexHome.selectedOption == 11: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   Criadores                                                                             #
#########################################################################################

                

                if DexHome.selectedScreen == 8:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 160 and 0 < mouse[1] < 55: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                      
                    Draw.RoundRect(mainSurface,(0,0,0),(45,90,90,50),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(0,0,0),(11,120,160,250),5,2,(255,0,0))
                    #Topico
                    Text.Write(mainSurface,(90,105),"Sobre",fontSize-10,"joy.otf",(255,0,0),True)
                    #Voltar
                    Draw.RoundRect(mainSurface,(40,40,40),(13,22,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(65,40),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #Sobre
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"PyDex",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,btnColorMore2,(170,15,620,445),radius,borderWidth,borderColor)
                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                    #Pydex
                    Draw.RoundRect(mainSurface,(40,40,40),(20,130,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,155),"Pydex",fontSize,"joy.otf",btnFontMore2,True)
                    #Criadores
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"Criadores",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,(40,40,40),(20,190,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,215),"Criadores",fontSize-12,"joy.otf",btnFontMore3,True)
                    #Botao3
                    Draw.RoundRect(mainSurface,(40,40,40),(20,250,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,275),"Parceiros",fontSize-12,"joy.otf",btnFontMore4,True)
                    #Botao4
                    Draw.RoundRect(mainSurface,(40,40,40),(20,310,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,335),"Livre",fontSize,"joy.otf",btnFontMore5,True)
                    
                    Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))
                                   
                 
                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            #Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 2
                            if DexHome.selectedOption == 7: DexHome.selectedScreen = 11
                            if DexHome.selectedOption == 8: DexHome.selectedScreen = 8
                            if DexHome.selectedOption == 9: DexHome.selectedScreen = 9
                            if DexHome.selectedOption == 10: DexHome.selectedScreen = 10
                            if DexHome.selectedOption == 11: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   Parceiros                                                                            #
#########################################################################################

                

                if DexHome.selectedScreen == 9:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 160 and 0 < mouse[1] < 55: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10
                                       

                    Draw.RoundRect(mainSurface,(0,0,0),(45,90,90,50),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(0,0,0),(11,120,160,250),5,2,(255,0,0))
                    #Topico
                    Text.Write(mainSurface,(90,105),"Sobre",fontSize-10,"joy.otf",(255,0,0),True)
                    #Voltar
                    Draw.RoundRect(mainSurface,(40,40,40),(13,22,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(65,40),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #Sobre
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"PyDex",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,btnColorMore2,(170,15,620,445),radius,borderWidth,borderColor)
                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                    #Pydex
                    Draw.RoundRect(mainSurface,(40,40,40),(20,130,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,155),"Pydex",fontSize,"joy.otf",btnFontMore2,True)
                    ##Criadores
                    Draw.RoundRect(mainSurface,(40,40,40),(20,190,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,215),"Criadores",fontSize-12,"joy.otf",btnFontMore3,True)
                    #Parceiros
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"Parceiros",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,(40,40,40),(20,250,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,275),"Parceiros",fontSize-12,"joy.otf",btnFontMore4,True)
                    #Botao4
                    Draw.RoundRect(mainSurface,(40,40,40),(20,310,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,335),"Livre",fontSize,"joy.otf",btnFontMore5,True)
                    
                    Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))

                                        
                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            #Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 2
                            if DexHome.selectedOption == 7: DexHome.selectedScreen = 11
                            if DexHome.selectedOption == 8: DexHome.selectedScreen = 8
                            if DexHome.selectedOption == 9: DexHome.selectedScreen = 9
                            if DexHome.selectedOption == 10: DexHome.selectedScreen = 10
                            if DexHome.selectedOption == 11: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   Livre                                                                         #
#########################################################################################

                

                if DexHome.selectedScreen == 10:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((0,0,0))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)
                    
                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 160 and 0 < mouse[1] < 55: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 190: 
                            btnColorMore2 = (20,20,20)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7
                                                           

                        elif  0 < mouse[0] < 150 and 120 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 300: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 0 < mouse[0] < 150 and 120 < mouse[1] < 360:
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                                           

                    Draw.RoundRect(mainSurface,(0,0,0),(45,90,90,50),5,2,(255,0,0))
                    Draw.RoundRect(mainSurface,(0,0,0),(11,120,160,250),5,2,(255,0,0))
                    #Topico
                    Text.Write(mainSurface,(90,105),"Sobre",fontSize-10,"joy.otf",(255,0,0),True)
                    #Voltar
                    Draw.RoundRect(mainSurface,(40,40,40),(13,22,105,35),5,2,(255,0,0))
                    Text.Write(mainSurface,(65,40),"Voltar",fontSize-10,"joy.otf",btnFontMore1,True)
                    #Sobre
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"PyDex",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,btnColorMore2,(170,15,620,445),radius,borderWidth,borderColor)
                    #Logo
                    Text.Write(mainSurface,(85,410),"PyDex",fontSize+5,"joy.otf",(255,0,0),True)
                    Text.Write(mainSurface,(115,435),"Pokédex",fontSize-15,"calibrilight.ttf",(255,255,255),True)
                    #Pydex
                    Draw.RoundRect(mainSurface,(40,40,40),(20,130,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,155),"Pydex",fontSize,"joy.otf",btnFontMore2,True)
                    ##Criadores
                    Draw.RoundRect(mainSurface,(40,40,40),(20,190,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,215),"Criadores",fontSize-12,"joy.otf",btnFontMore3,True)
                    #Parceiros
                    Draw.RoundRect(mainSurface,(40,40,40),(20,250,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,275),"Parceiros",fontSize-12,"joy.otf",btnFontMore4,True)
                    #Botao4
                    Text.Write(mainSurface,(3*37+1*boxWidth+boxWidth/2,0+boxHeight/5),"Livre",fontSize,"joy.otf",(255,255,255),True)
                    Draw.RoundRect(mainSurface,(40,40,40),(20,310,145,50),5,2,(255,0,0))
                    Text.Write(mainSurface,(90,335),"Livre",fontSize,"joy.otf",btnFontMore5,True)
                    
                    Draw.Pokeball(mainSurface,(180,35),(255,0,0),(10,10,10))
                                        

                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=50
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 0
                        if fadeOutCtr > 10:
                            fadeOutColor = (0,0,0)
                            #Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 2
                            if DexHome.selectedOption == 7: DexHome.selectedScreen = 11
                            if DexHome.selectedOption == 8: DexHome.selectedScreen = 8
                            if DexHome.selectedOption == 9: DexHome.selectedScreen = 9
                            if DexHome.selectedOption == 10: pass
                            if DexHome.selectedOption == 11: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

                # Update Screen
                pygame.display.update()
                clock.tick(60)

        DexHome.running = True
        return