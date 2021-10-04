# Módulos de Importação
import pygame
from pygame import gfxdraw
from pygame.locals import *
from threading import Thread
import time
import random
import sys
import sqlite3
import os

from CButton import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text
from CUserInterface import UI


class DexInfo:

#########################################################################################
#   VARIAVEIS                                                                           #
#########################################################################################

    pokeData = None
    formData = None
    megaData = None
    megaDataSingle = None
    formDataAll = None

    evoChain = None
    currentPokemon = 1
    running = True
    loadNewPokemon = False
    evoScreenActive = False
    evoSelectActive = False
    statsScreenActive = False

    formNumberSelected = None

    megaEvolutionSelected = False
    megaEvolutionNumber = 0

    alolaFormSelected = False

    galarianFormSelected = False

    genderFemaleSelected = False

    shinySelected = False


    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

#########################################################################################
#   TOGGLE FUNCTION                                                                     #
#########################################################################################
    
    def ReturnToMenu():
        DexInfo.loadNewPokemon = True
        DexInfo.running = False

    def ToggleNextForm():
        DexInfo.formNumberSelected += 1
        if DexInfo.formNumberSelected > len(DexInfo.formDataAll): DexInfo.formNumberSelected = 1 

        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def TogglePrevForm():
        DexInfo.formNumberSelected -= 1
        if DexInfo.formNumberSelected < 1: DexInfo.formNumberSelected = len(DexInfo.formDataAll) 

        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleAlolaForm():
        if DexInfo.alolaFormSelected: DexInfo.alolaFormSelected = False
        else: DexInfo.alolaFormSelected = True
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleGalarianForm():
        if DexInfo.galarianFormSelected: DexInfo.galarianFormSelected = False
        else: DexInfo.galarianFormSelected = True
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyOn():
        DexInfo.shinySelected = True
        DexInfo.oneTimeCycleLoad = True
        DexInfo.LoadSpritesheet()

    def ToggleShinyOff():
        DexInfo.shinySelected = False
        DexInfo.oneTimeCycleLoad = True
        DexInfo.LoadSpritesheet()

    def ToggleMegaEvolution1():
        if DexInfo.megaEvolutionNumber == 1 and DexInfo.megaEvolutionSelected == True: DexInfo.megaEvolutionSelected = False
        else: DexInfo.megaEvolutionSelected = True
        DexInfo.megaEvolutionNumber = 1
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleMegaEvolution2():
        if DexInfo.megaEvolutionNumber == 2 and DexInfo.megaEvolutionSelected == True: DexInfo.megaEvolutionSelected = False
        else: DexInfo.megaEvolutionSelected = True
        DexInfo.megaEvolutionNumber = 2
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleNormalMale():
        DexInfo.shinySelected = False
        DexInfo.genderFemaleSelected = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleNormalFemale():
        DexInfo.shinySelected = False
        DexInfo.genderFemaleSelected = True
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyMale():
        DexInfo.shinySelected = True
        DexInfo.genderFemaleSelected = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyFemale():
        DexInfo.shinySelected = True
        DexInfo.genderFemaleSelected = True
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleStatsScreen():
        if DexInfo.statsScreenActive: DexInfo.statsScreenActive = False
        else: DexInfo.statsScreenActive = True
        DexInfo.oneTimeCycleLoad = True
         
        DexInfo.evoScreenActive = False
        DexInfo.evoSelectActive = False
    
    def ToggleEvoSelector():
        if DexInfo.evoSelectActive: DexInfo.evoSelectActive = False
        else: DexInfo.evoSelectActive = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.evoScreenActive = False
        DexInfo.statsScreenActive = False

    def ToggleEvoChainScreen():
        if DexInfo.evoScreenActive: DexInfo.evoScreenActive = False
        else: DexInfo.evoScreenActive = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.evoSelectActive = False
        DexInfo.statsScreenActive = False

    def ToggleNextDex():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon += 1
        if DexInfo.currentPokemon >= 803: DexInfo.currentPokemon = 1

        DexInfo.LoadSpritesheet()

    def TogglePrevDex():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon -= 1
        if DexInfo.currentPokemon <=  0: DexInfo.currentPokemon = 802

        DexInfo.LoadSpritesheet()

    def ToggleNextEvo():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        if DexInfo.pokeData["nextEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["nextEvolution"]

        DexInfo.LoadSpritesheet()

    def TogglePrevEvo():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        if DexInfo.pokeData["prevEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["prevEvolution"]

        DexInfo.LoadSpritesheet()

    def ToggleDexNumber(dexNumber):
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon = dexNumber

        DexInfo.LoadSpritesheet()

    def GetPokeData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                evoNext.evoNextDex AS nextEvolution,
                evoPrev.evoDex AS prevEvolution,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND (sprites.isMegaEvolution IS NULL OR sprites.isMegaEvolution = '')
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
                LEFT JOIN regions ON pokemon.regionID = regions.id 
                LEFT JOIN evYields ON pokemon.nationalDex = evYields.nationalDex
                LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id
                LEFT JOIN growthRates ON pokemon.growthRateID = growthRates.id
                LEFT JOIN eggGroups ON pokemon.eggGroupID = eggGroups.id
                LEFT JOIN evolutions AS evoNext ON pokemon.nationalDex = evoNext.evoDex
                LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoPrev.evoNextDex
                WHERE pokemon.nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchone()

    def GetMegaData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon
                LEFT JOIN pokemonMega ON pokemon.nationalDex = pokemonMega.nationalDex
                LEFT JOIN megaStones ON pokemonMega.megaStoneID = megaStones.id
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.isMegaEvolution = 1
                LEFT JOIN types AS typeA ON pokemonMega.megaTypeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemonMega.megaTypeID2 = typeB.id 
                WHERE pokemon.nationalDex = ?
                ORDER BY megaName ASC
                """,parameters)
        # Duplicate entries because of left join
        result = DexInfo.c.fetchall()
        if len(result) > 1: return [result[0],result[3]]
        else: return result

    def GetAlolaData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.isAlolaForm = 1
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
                WHERE pokemon.nationalDex = ?
                """,parameters)
        return DexInfo.c.fetchone()

    def GetGalarianData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.isGalarianForm = 1
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id
                WHERE pokemon.nationalDex = ?
                """,parameters)
        return DexInfo.c.fetchone()


    def GetFormData(nationalDex,formNumber):
        parameters = (formNumber,formNumber,nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.formNumber = ?
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id   
                LEFT JOIN pokemonForms ON pokemon.nationalDex = pokemonForms.nationalDex
                AND pokemonForms.formNumber = ?
                WHERE pokemon.nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchone()

    def GetFormDataAll(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *
                FROM pokemonForms 
                WHERE nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchall()

    def LoadSpritesheet():

        pokeTmp = DexInfo.GetPokeData(DexInfo.currentPokemon)
        megaTmp = DexInfo.GetMegaData(DexInfo.currentPokemon)
        alolaTmp = DexInfo.GetAlolaData(DexInfo.currentPokemon)

        if pokeTmp["hasMultipleForms"] == 1 and DexInfo.formNumberSelected == None: DexInfo.formNumberSelected = pokeTmp["defaultForm"]
        formTmp = DexInfo.GetFormData(DexInfo.currentPokemon,DexInfo.formNumberSelected)

        

        if DexInfo.shinySelected:
        # SHINY
            # Spritesheets for Multiple Forms
            if pokeTmp["hasMultipleForms"] == 1:
                spriteFile = formTmp["spriteSheetHDFrontShiny"]

            # Spritesheets for Mega-Evolutions
            elif pokeTmp["hasMegaEvolution"] == 1 and DexInfo.megaEvolutionSelected:
                if len(megaTmp) > 1:
                    if DexInfo.megaEvolutionNumber == 1: spriteFile = megaTmp[0]["spriteSheetHDFrontShiny"]
                    else: spriteFile = megaTmp[1]["spriteSheetHDFrontShiny"]
                else: spriteFile = megaTmp[0]["spriteSheetHDFrontShiny"]

            # Spritesheets for Alola-Form
            elif pokeTmp["hasAlolaForm"] == 1 and DexInfo.alolaFormSelected:
                spriteFile = alolaTmp["spriteSheetHDFrontShiny"]

            # Spritesheets for Gender-Difference
            elif pokeTmp["genderDifference"] == 1:
                if DexInfo.genderFemaleSelected: spriteFile = pokeTmp["spriteSheetHDFrontFemaleShiny"]
                else: spriteFile = pokeTmp["spriteSheetHDFrontShiny"]

            # Default Spritesheet
            else:
                spriteFile = pokeTmp["spriteSheetHDFrontShiny"]
        else:
        # NORMAL
            # Spritesheets for Multiple Forms
            if pokeTmp["hasMultipleForms"] == 1:
                spriteFile = formTmp["spriteSheetHDFront"]

            # Spritesheets for Mega-Evolutions
            elif pokeTmp["hasMegaEvolution"] == 1 and DexInfo.megaEvolutionSelected:
                if len(megaTmp) > 1:
                    if DexInfo.megaEvolutionNumber == 1: spriteFile = megaTmp[0]["spriteSheetHDFront"]
                    else: spriteFile = megaTmp[1]["spriteSheetHDFront"]
                else: spriteFile = megaTmp[0]["spriteSheetHDFront"]

            # Spritesheets for Alola-Form
            elif pokeTmp["hasAlolaForm"] == 1 and DexInfo.alolaFormSelected:
                spriteFile = alolaTmp["spriteSheetHDFront"]

            # Spritesheets for Gender-Difference
            elif pokeTmp["genderDifference"] == 1:
                if DexInfo.genderFemaleSelected: spriteFile = pokeTmp["spriteSheetHDFrontFemale"]
                else: spriteFile = pokeTmp["spriteSheetHDFront"]

            # Default Spritesheet
            else:
                spriteFile = pokeTmp["spriteSheetHDFront"]

        DexInfo.thread = Thread(target = Sprite.Create, args = ("spriteSheets/" + str(spriteFile),DexInfo.currentPokemon,)) 
        DexInfo.thread.start()

    def EvoChain():
        evoChain = [DexInfo.currentPokemon]

        # get previous evolutions
        currentSelector = DexInfo.currentPokemon
        while True:
            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoNextDex = ?""",parameters)
            evoResult = DexInfo.c.fetchone()     
            if evoResult != None:
                evoChain.insert(0,evoResult["evoDex"])
                currentSelector = evoResult["evoDex"]
            else: break

        # get next evolutions
        currentSelector = DexInfo.currentPokemon
        while True:
            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
            evoResult = DexInfo.c.fetchone()     
            if evoResult != None:
                evoChain.append(evoResult["evoNextDex"])
                currentSelector = evoResult["evoNextDex"]
            else: break

        return evoChain 

    def FullChain():
        simpleChain = DexInfo.EvoChain()
        fullChain = [[simpleChain[0]]]
        fullChainSegment = []

        for sCh in simpleChain:
            currentSelector = sCh
            fullChainSegment = []

            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
            evoResults = DexInfo.c.fetchall()
            for evoResult in evoResults:
                if evoResult != None:
                    fullChainSegment.append(evoResult["evoNextDex"])
            if len(fullChainSegment) != 0:
                fullChain.append(fullChainSegment)

        return fullChain

    def NextEvolutions():
        nextEvos = []
        parameters = (DexInfo.currentPokemon,)
        DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
        evoResults = DexInfo.c.fetchall()
        for evoResult in evoResults:
            if evoResult != None:
                nextEvos.append(evoResult["evoNextDex"])
        return nextEvos

    def HasMultipleEvos():

        parameters = (DexInfo.currentPokemon,)
        DexInfo.c.execute("SELECT * FROM evolutions WHERE evoDex = ?",parameters)
        evoResults = DexInfo.c.fetchall()
        if len(evoResults) > 1: return True
        else: return False

    def GetTypeColors(dexNumber):
        parameters = (dexNumber,)
        DexInfo.c.execute("SELECT * FROM pokemon LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id WHERE pokemon.nationalDex = ?",parameters)
        pmResult = DexInfo.c.fetchone()

        colorA = (int(pmResult["typeColor"].split(',')[0]), int(pmResult["typeColor"].split(',')[1]), int(pmResult["typeColor"].split(',')[2]))
        colorB = (int(pmResult["typeColorBright"].split(',')[0]), int(pmResult["typeColorBright"].split(',')[1]), int(pmResult["typeColorBright"].split(',')[2]))

        return (colorA,colorB)

    def MegaEvolutionCount():
        parameters = (DexInfo.currentPokemon,)
        # CHANGE TO pokemonMega-Database
        DexInfo.c.execute("SELECT * FROM sprites WHERE nationalDex = ? AND isMegaEvolution = 1",parameters)
        pmResult = DexInfo.c.fetchall()

        if pmResult != None: return len(pmResult)
        else: return 0 

#########################################################################################
#########################################################################################
#   MAIN START                                                                          #
#########################################################################################
#########################################################################################

    def Show(selectedPokemon):
   
#########################################################################################
#   INITIALISATION AND SETUP                                                            #
#########################################################################################

        # PyGame Initialisation
        clock = pygame.time.Clock()

        # Window and Surface Initialisation
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
#   SURFACE DEFINITIONS                                                                 #
#########################################################################################

        spriteSurface = pygame.Surface((300,300)).convert_alpha()

        evoChainSurface = pygame.Surface((500-26,360-26)).convert_alpha()

#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################

        runtimeCtr = 0

        loadActiveCounter = 0
        spriteReloadTrigger = 10
        spriteReloaded = False

        thread = None

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################

        # Loading min and max values for stats
        statMinMaxVals = []
        statTypes = ("statHP","statAtk","statDef","statSpAtk","statSpDef","statSpd")
        for stat in statTypes:
            statSegment = []
            DexInfo.c.execute("SELECT * FROM pokemon WHERE " + stat + " NOT NULL ORDER BY " + stat + " ASC")
            statResMin = DexInfo.c.fetchone()
            statSegment.append(statResMin[stat])
            DexInfo.c.execute("SELECT * FROM pokemon ORDER BY " + stat + " DESC")
            statResMax= DexInfo.c.fetchone()
            statSegment.append(statResMax[stat])
            statMinMaxVals.append(statSegment)

        DexInfo.currentPokemon = selectedPokemon

        DexInfo.LoadSpritesheet()

        while DexInfo.running:

            # Loading data
            DexInfo.pokeData = DexInfo.GetPokeData(DexInfo.currentPokemon)

            if DexInfo.pokeData["hasMultipleForms"] == 1 and DexInfo.formNumberSelected == None: DexInfo.formNumberSelected = DexInfo.pokeData["defaultForm"]

            DexInfo.formData = DexInfo.GetFormData(DexInfo.currentPokemon,DexInfo.formNumberSelected)

            DexInfo.formDataAll = DexInfo.GetFormDataAll(DexInfo.currentPokemon)

            DexInfo.megaData = DexInfo.GetMegaData(DexInfo.currentPokemon)

            DexInfo.alolaData = DexInfo.GetAlolaData(DexInfo.currentPokemon)

            # Set default Form
            
            if DexInfo.megaEvolutionSelected:
                if len(DexInfo.megaData) > 1:
                    if DexInfo.megaEvolutionNumber == 1: DexInfo.megaDataSingle = DexInfo.megaData[0] 
                    else: DexInfo.megaDataSingle = DexInfo.megaData[1]
                else: DexInfo.megaDataSingle = DexInfo.megaData[0]

            dexTypeColor = (int(DexInfo.pokeData["typeColor"].split(',')[0]), int(DexInfo.pokeData["typeColor"].split(',')[1]), int(DexInfo.pokeData["typeColor"].split(',')[2]))
            dexTypeColorDark = (int(DexInfo.pokeData["typeColorBright"].split(',')[0]), int(DexInfo.pokeData["typeColorBright"].split(',')[1]), int(DexInfo.pokeData["typeColorBright"].split(',')[2]))

            # Configurações de Botões
            Button.idleColor = dexTypeColor
            Button.hoverColor = dexTypeColorDark 
            Button.fontColor = (255,255,255)
            Button.disabledColor = (30,30,30)
            Button.borderColor = (255,255,255)
            Button.fontFamily = "joy.otf"

            # Botões de Navegação
            btnPrevDex = Button.RoundRect(mainSurface,(320,425,110,40),15,"Anterior",18,1,DexInfo.TogglePrevDex,None,None,None,60,5)
            btnPrevEvo = Button.RoundRect(mainSurface,(440,425,110,40),15,"Pré-Evo",18,1,DexInfo.TogglePrevEvo,None,None,None,60,5)
            btnNextEvo = Button.RoundRect(mainSurface,(560,425,110,40),15,"Evolução",18,1,DexInfo.ToggleNextEvo,None,None,None,60,5)
            btnNextEvoSelect = Button.RoundRect(mainSurface,(560,425,110,40),15,"Evolução",18,1,DexInfo.ToggleEvoSelector,None,None,None,60,5)
            btnReturn = Button.RoundRect(mainSurface,(5,5,60,60),29,"Voltar",13,2,DexInfo.ReturnToMenu,None,None,None,60,5)

            btnNextDex = Button.RoundRect(mainSurface,(680,425,110,40),15,"Próximo",18,1,DexInfo.ToggleNextDex,None,None,None,60,5)

            # Gender Buttons
            btnFormNormal = Button.RoundRect(mainSurface,(520,130,126,30),10,"Normal",20,1,DexInfo.ToggleShinyOff,None,None,None,10)
            btnFormShiny = Button.RoundRect(mainSurface,(661,130,126,30),10,"Shiny",20,1,DexInfo.ToggleShinyOn,None,None,None,10)

            btnFormNormalMale = Button.RoundRect(mainSurface,(520,130,60,30),10,"Macho",15,1,DexInfo.ToggleNormalMale,None,None,None,10)
            btnFormNormalFemale = Button.RoundRect(mainSurface,(520 + 66,130,60,30),10,"Femea",15,1,DexInfo.ToggleNormalFemale,None,None,None,10)
            btnFormShinyMale = Button.RoundRect(mainSurface,(661,130,60,30),10,"MS",25,1,DexInfo.ToggleShinyMale,None,None,None,10)
            btnFormShinyFemale = Button.RoundRect(mainSurface,(661 + 66,130,60,30),10,"FS",25,1,DexInfo.ToggleShinyFemale,None,None,None,10)

            # Alola
            btnAlolaToggle = Button.RoundRect(mainSurface,(16,325,70,40),18,"Alola",18,1,DexInfo.ToggleAlolaForm,None,None,None,40,30)
            # Galarian
            """btnGalarianToggle = Button.RoundRect(mainSurface,(16,275,70,40),18,"Galarian",18,1,DexInfo.ToggleGalariamForm,None,None,None,40,30)"""

            # Form Selectors
            btnNextForm = Button.RoundRect(mainSurface,(465,160,40,80),18,">",18,1,DexInfo.ToggleNextForm,None,None,None,40,50)
            btnPrevForm = Button.RoundRect(mainSurface,(15,160,40,80),18,"<",18,1,DexInfo.TogglePrevForm,None,None,None,40,50)

            # MegaEvolution Buttons
            btnMegaEvo1 = Button.RoundRect(mainSurface,(18,280,40,40),10,"ME1",25,1,DexInfo.ToggleMegaEvolution1,None,None,None,0,30)
            btnMegaEvo2 = Button.RoundRect(mainSurface,(18,340,40,40),10,"ME2",25,1,DexInfo.ToggleMegaEvolution2,None,None,None,0,30)

            # Botão Invisivel de Evoluçoes
            btnEvoChainScreen = Button.RoundRect(mainSurface,(410,20,0,0),0,"",0,0,DexInfo.ToggleEvoChainScreen,None,None,None,100,60)
            # ScreenToggle Buttons
            btnStatsScreen = Button.RoundRect(mainSurface,(525,90,260,25),10,"Mais Status",17,1,DexInfo.ToggleStatsScreen,None,None,None,10)
        
            
            # One-Time Drawing routines
            
            mainSurface.fill((30,30,30))
        
            Draw.RoundRect(mainSurface,(40,40,40),(520,10,270,110),15,2,dexTypeColor,"Status")
            Draw.RoundRect(mainSurface,(40,40,40),(525,40,125,45),10,1,dexTypeColor,"")
            Text.Write(mainSurface,(525+55,50),"Tamanho",17,"joy.otf",(255,255,255),True)
            Text.Write(mainSurface,(525+55,73),str('{0:.2f}'.format(DexInfo.pokeData["height"]/10)) + " m",19,"joy.otf",(255,255,255),True)
            Draw.RoundRect(mainSurface,(40,40,40),(660,40,125,45),10,1,dexTypeColor,"")
            Text.Write(mainSurface,(665+55,50),"Peso",17,"joy.otf",(255,255,255),True)
            Text.Write(mainSurface,(665+55,73),str('{0:.2f}'.format(DexInfo.pokeData["weight"]/10)) + " kg",19,"joy.otf",(255,255,255),True)
            """Draw.RoundRect(mainSurface,(40,40,40),(525+115,40,146,45),10,1,dexTypeColor,"")"""
            """Text.Write(mainSurface,(525+115+73,50),"Grupo de Ovos",17,"joy.otf",(255,255,255),True)"""
            """Text.Write(mainSurface,(525+115+73,73),DexInfo.pokeData["eggGroupName"],17,"joy.otf",(255,255,255),True)"""
            Draw.RoundRect(mainSurface,(40,40,40),(520,170,270,140),15,2,dexTypeColor,"Dano Recebido")
            Draw.RoundRect(mainSurface,(40,40,40),(517,320,276,50),13,2,dexTypeColor,"Porcentagem de gênero")
            Draw.RoundRect(mainSurface,(40,40,40),(10,360,300,110),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,dexTypeColor,(10,300,400,115),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

            #Resistencias e Fraquesas  
            
            inseto = 155,181,48   
            noturno = 48,55,91
            dragao = 251,144,46
            eletrico = 255,168,0
            fada = 255,161,193
            lutador = 80,80,80
            fogo = 219,98,0
            voador = 0,175,158
            fantasma  = 90,0,175
            grama = 0,151,41
            terra = 94,65,58
            gelo  = 0,140,175
            normal = 177,161,142
            venenoso = 141,35,254
            psiquico = 165,107,152
            pedra = 144,144,144
            metal = 147,169,193
            agua = 0,108,216
            
            if DexInfo.pokeData["type2Name"] == None:
                #fada (2x 2 ½x 4)
                if "Fada" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,230,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,venenoso,(560,220,105,20),5,2,venenoso)
                    Draw.RoundRect(mainSurface,metal,(670,220,105,20),5,2,metal)
                    Text.Write(mainSurface,(610,232,352),"Venenoso",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(720,232,352),"Metal",20,"calibrilight.ttf",(255,255,255),True)
                    #½x
                    Draw.RoundRect(mainSurface,lutador,(560,265,50,20),5,2,lutador)
                    Draw.RoundRect(mainSurface,inseto,(615,265,50,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,dragao,(670,265,50,20),5,2,dragao)
                    Draw.RoundRect(mainSurface,noturno,(725,265,50,20),5,2,noturno)
                    Text.Write(mainSurface,(585,276,352),"Lutad.",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(640,276,352),"Inset.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(695,276,352),"Drag.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(750,276,352),"Notu.",20,"calibrilight.ttf",(255,255,255),True)
                #Eletrico (2x 1 ½x 3)
                elif "Eletrico" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,230,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,terra,(560,220,210,20),5,2,terra)
                    Text.Write(mainSurface,(665,232,352),"Terra",20,"calibrilight.ttf",(255,255,255),True)
                    #½x
                    Draw.RoundRect(mainSurface,voador,(560,265,66,20),5,2,voador)
                    Draw.RoundRect(mainSurface,metal,(631,265,66,20),5,2,metal)
                    Draw.RoundRect(mainSurface,eletrico,(702,265,66,20),5,2,eletrico)
                    Text.Write(mainSurface,(590,276,352),"Gelo",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,276,352),"Metal",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,276,352),"Elétrico",20,"calibrilight.ttf",(0,0,0),True)
                #Normal ( 2x 1 0x 1 )
                elif "Normal" == DexInfo.pokeData["typeName"]:
                    Text.Write(mainSurface,(540,230,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"0x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,lutador,(560,220,210,20),5,2,lutador)
                    Text.Write(mainSurface,(665,232,352),"Lutador",20,"calibrilight.ttf",(255,255,255),True)
                    #0x
                    Draw.RoundRect(mainSurface,fantasma,(560,265,210,20),5,2,fantasma)
                    Text.Write(mainSurface,(665,276,352),"Fantasma",20,"calibrilight.ttf",(255,255,255),True)
                #Lutador (2x 3 ½x 3)
                elif "Lutador" == DexInfo.pokeData["typeName"]:
                    Text.Write(mainSurface,(540,230,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,voador,(560,220,66,20),5,2,voador)
                    Draw.RoundRect(mainSurface,psiquico,(631,220,66,20),5,2,psiquico)
                    Draw.RoundRect(mainSurface,fada,(702,220,66,20),5,2,fada)
                    Text.Write(mainSurface,(590,232,352),"Voador",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,232,352),"Psíquico",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,232,352),"Fada",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,pedra,(560,265,66,20),5,2,pedra)
                    Draw.RoundRect(mainSurface,inseto,(631,265,66,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,noturno,(702,265,66,20),5,2,noturno)
                    Text.Write(mainSurface,(590,276,352),"Pedra",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,276,352),"Inseto",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(735,276,352),"Noturno",20,"calibrilight.ttf",(255,255,255),True)
                #Voador (2x 3 ½x 3 0x 1)
                elif "Voador" == DexInfo.pokeData["typeName"]:
                    Text.Write(mainSurface,(540,225,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,255,352),"½x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,285,352),"0x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,pedra,(560,215,66,20),5,2,pedra)
                    Draw.RoundRect(mainSurface,eletrico,(631,215,66,20),5,2,eletrico)
                    Draw.RoundRect(mainSurface,gelo,(702,215,66,20),5,2,gelo)
                    Text.Write(mainSurface,(590,227,352),"Pedra",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(665,227,352),"Elétrico",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(735,227,352),"Gelo",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,lutador,(560,245,66,20),5,2,lutador)
                    Draw.RoundRect(mainSurface,inseto,(631,245,66,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,grama,(702,245,66,20),5,2,grama)
                    Text.Write(mainSurface,(590,255,352),"Lutador",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(665,255,352),"Inseto",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(735,255,352),"Grama",20,"calibrilight.ttf",(0,0,0),True)
                    #0x
                    Draw.RoundRect(mainSurface,terra,(560,272,210,20),5,2,terra)
                    Text.Write(mainSurface,(665,282,352),"Terra",20,"calibrilight.ttf",(255,255,255),True)
                #Venenoso (2x 2 ½x 5)
                elif "Venenoso" == DexInfo.pokeData["typeName"]:
                    Text.Write(mainSurface,(540,220,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,terra,(560,210,105,20),5,2,terra)
                    Draw.RoundRect(mainSurface,psiquico,(670,210,105,20),5,2,psiquico)
                    Text.Write(mainSurface,(610,222,352),"Terra",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(720,222,352),"Psíquico",20,"calibrilight.ttf",(255,255,255),True)
                    #½x
                    Draw.RoundRect(mainSurface,lutador,(560,250,66,20),5,2,lutador)
                    Draw.RoundRect(mainSurface,venenoso,(631,250,66,20),5,2,venenoso)
                    Draw.RoundRect(mainSurface,inseto,(702,250,66,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,grama,(560,275,105,20),5,2,grama)
                    Draw.RoundRect(mainSurface,fada,(670,275,105,20),5,2,fada)
                    Text.Write(mainSurface,(592,260,352),"Lutador",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(665,260,352),"Venen.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(735,260,352),"Inseto",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(610,287,352),"Grama",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(720,287,352),"Fada",20,"calibrilight.ttf",(255,255,255),True)
                #Metal (2x 3 ½x 10 0x 1)
                elif "Metal" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,210,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,255,352),"½x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,295,352),"0x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,lutador,(560,200,66,20),5,2,lutador)
                    Draw.RoundRect(mainSurface,terra,(631,200,66,20),5,2,terra)
                    Draw.RoundRect(mainSurface,fogo,(702,200,66,20),5,2,fogo)
                    Text.Write(mainSurface,(590,212,352),"Lutador",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,212,352),"Terra",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,212,352),"Fogo",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,normal,(560,230,37,20),5,2,normal)
                    Draw.RoundRect(mainSurface,voador,(603,230,37,20),5,2,voador)
                    Draw.RoundRect(mainSurface,pedra,(645,230,37,20),5,2,pedra)
                    Draw.RoundRect(mainSurface,inseto,(687,230,37,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,metal,(730,230,37,20),5,2,metal)
                    Draw.RoundRect(mainSurface,grama,(560,255,37,20),5,2,grama)
                    Draw.RoundRect(mainSurface,psiquico,(603,255,37,20),5,2,psiquico)
                    Draw.RoundRect(mainSurface,gelo,(645,255,37,20),5,2,gelo)
                    Draw.RoundRect(mainSurface,dragao,(687,255,37,20),5,2,dragao)
                    Draw.RoundRect(mainSurface,fada,(730,255,37,20),5,2,fada)
                    Text.Write(mainSurface,(580,242,352),"Nor.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(623,242,352),"Voa.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,242,352),"Ped.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(707,242,352),"Ins.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(750,242,352),"Met.",20,"calibrilight.ttf",(0,0,0),True)

                    Text.Write(mainSurface,(580,265,352),"Gra.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(623,265,352),"Psí.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,265,352),"Gel.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(707,265,352),"Dra.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(750,265,352),"Fad.",20,"calibrilight.ttf",(0,0,0),True)
                    #0x                    
                    Draw.RoundRect(mainSurface,venenoso,(560,285,210,20),5,2,venenoso)
                    Text.Write(mainSurface,(665,295,352),"Venenoso",20,"calibrilight.ttf",(255,255,255),True)
                # Fogo (2x 3 ½x 6)
                elif "Fogo" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,220,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,265,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,terra,(560,210,66,20),5,2,terra)
                    Draw.RoundRect(mainSurface,pedra,(631,210,66,20),5,2,pedra)
                    Draw.RoundRect(mainSurface,agua,(702,210,66,20),5,2,agua)
                    Text.Write(mainSurface,(590,222,352),"Terra",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,222,352),"Pedra",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,222,352),"Água",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,inseto,(560,245,66,20),5,2,inseto)
                    Draw.RoundRect(mainSurface,metal,(631,245,66,20),5,2,metal)
                    Draw.RoundRect(mainSurface,fogo,(702,245,66,20),5,2,fogo)
                    Text.Write(mainSurface,(590,255,352),"Inseto",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,255,352),"Metal",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,255,352),"Fogo",20,"calibrilight.ttf",(0,0,0),True)
                    Draw.RoundRect(mainSurface,grama,(560,270,66,20),5,2,grama)
                    Draw.RoundRect(mainSurface,gelo,(631,270,66,20),5,2,gelo)
                    Draw.RoundRect(mainSurface,fada,(702,270,66,20),5,2,fada)
                    Text.Write(mainSurface,(590,280,352),"Grama",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,280,352),"Gelo",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,280,352),"Fada",20,"calibrilight.ttf",(0,0,0),True)
                # Terra
                elif "Terra" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,220,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,255,352),"½x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,290,352),"0x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,agua,(560,210,66,20),5,2,agua)
                    Draw.RoundRect(mainSurface,grama,(631,210,66,20),5,2,grama)
                    Draw.RoundRect(mainSurface,gelo,(702,210,66,20),5,2,gelo)
                    Text.Write(mainSurface,(590,222,352),"Água",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,222,352),"Grama",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(735,222,352),"Gelo",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,venenoso,(560,245,100,20),5,2,venenoso)
                    Draw.RoundRect(mainSurface,pedra,(670,245,100,20),5,2,pedra)
                    Text.Write(mainSurface,(610,257,352),"Venenoso",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(720,257,352),"Pedra",20,"calibrilight.ttf",(255,255,255),True)
                    #0x
                    Draw.RoundRect(mainSurface,eletrico,(560,278,210,20),5,2,eletrico)
                    Text.Write(mainSurface,(665,290,352),"Eletrico",20,"calibrilight.ttf",(0,0,0),True)
                # Pedra
                elif "Pedra" == DexInfo.pokeData["type1Name"]:
                    Text.Write(mainSurface,(540,220,352),"2x",20,"joy.otf",(255,255,255),True)
                    Text.Write(mainSurface,(540,275,352),"½x",20,"joy.otf",(255,255,255),True)
                    #2x
                    Draw.RoundRect(mainSurface,lutador,(560,210,68,20),5,2,lutador)
                    Draw.RoundRect(mainSurface,terra,(633,210,68,20),5,2,terra)
                    Draw.RoundRect(mainSurface,metal,(706,210,68,20),5,2,metal)
                    Text.Write(mainSurface,(590,222,352),"Lutador",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(665,222,352),"Terra",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(735,222,352),"Metal",20,"calibrilight.ttf",(0,0,0),True)
                    Draw.RoundRect(mainSurface,agua,(560,235,105,20),5,2,agua)
                    Draw.RoundRect(mainSurface,grama,(670,235,105,20),5,2,grama)
                    Text.Write(mainSurface,(610,247,352),"Água",20,"calibrilight.ttf",(255,255,255),True)
                    Text.Write(mainSurface,(720,247,352),"Grama",20,"calibrilight.ttf",(0,0,0),True)
                    #½x
                    Draw.RoundRect(mainSurface,normal,(560,265,50,20),5,2,normal)
                    Draw.RoundRect(mainSurface,voador,(615,265,50,20),5,2,voador)
                    Draw.RoundRect(mainSurface,venenoso,(670,265,50,20),5,2,venenoso)
                    Draw.RoundRect(mainSurface,fogo,(725,265,50,20),5,2,fogo)
                    Text.Write(mainSurface,(585,276,352),"Norm.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(640,276,352),"Voad.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(695,276,352),"Vene.",20,"calibrilight.ttf",(0,0,0),True)
                    Text.Write(mainSurface,(750,276,352),"Fogo",20,"calibrilight.ttf",(255,255,255),True)
                # Inseto
                # Fantasma
                # Agua
                # Grama
                # Dragao
                # Noturno
                # Psiquico
                # Gelo
                # NomalVoador
                # NormalNoturno
                # NormalFada
                # NormalPsiquico
                # NormalAgua
                # NormalLutador
                # NormalGrama
                # NormalTerra
                # NormalDragao
                # LutadorVoador
                # LutadorPsiquico
                # LutadorMetal
                # LutadorNoturno
                # LutadorGelo
                # LutadorFantasma
                # LutadorAgua
                # VoadorDragao
                # VoadorMetal
                # VoadorAgua
                # VenenosoTerra
                # VenenosoVoador
                # VenenosoPsiquico
                # VenenosoNoturno
                # VenenosoFada
                # VenenosoInseto
                # VenenosoLutador
                # VenenosoAgua
                # VenenosoFogo
                # VenenosoDragao
                # MetalTerra
                # MetalFada
                # MetalPsiquico
                # MetalDragao
                # MetalFantasma
                # FogoVoador
                # FogoDragao
                # FogoFantasma
                # FogoLutador
                # FogoMetal
                # FogoPsiquico
                # FogoNormal
                # FogoAgua
                # FogoNoturno
                # FantasmaVenenoso
                # FantasmaDragao
                # FantasmaFogo
                # FantasmaGrama
                # FantasmaVoador
                # FantasmaFada
                # FantasmaVoador
                # FantamasGelo
                # FantasmaMetal
                # FantasmaDragao
                # FantasmaFada
                # TerraMetal
                # TerraPedra
                # TerraVoador
                # TerraDragao
                # TerraPsiquico
                # TerraFogo
                # TerraNoturno
                # TerraFantasma
                # TerraEletrico
                # PedraEletrcio
                # PedraAgua
                # PedraVoador
                # PedraNoturno
                # PedraPsiquico
                # PedraGrama
                # PedraInseto
                # PedraMetal
                # PedraLutador
                # PedraDragao
                # PedraGelo
                # PedraFada
                # Pedravenenoso
                # PedraFogo  
                # InsetoVoador
                # InsetoGrama
                # InsetoMetal
                # InsetoLutador
                # InsetoAgua
                # InsetoTerra
                # InsetoFantasma
                # InsetoEletrico
                # InsetoFogo
                # InsetoFada
                # InsetoPsiquico
                # AguaPsiquico
                # AguaGelo
                # AguaNoturno
                # AguaEletrico
                # AguaFada
                # AguaDragao
                # AguaTerra
                # AguaGrama
                # AguaMetal
                # AguaPedra
                # GramaVenenoso
                # GramaPsiquico
                # GramaDragao
                # GramaVoador
                # GramaNoturno
                # GramaLutador
                # GramaTerra
                # GramaGelo
                # GramaFada
                # GramaMetal
                # FadaVoador
                # DragaoFada
                # DragaoGelo
                # DragaoLutador
                # EletricoPsiquico
                # EletricoMetal
                # EletricoVoador
                # EletricoDragao
                # EletricoFantasma
                # EletricoFogo
                # EletricoGelo
                # EletricoGrama
                # EletricoNormal
                # EletricoFada
                # EletricoVenenoso
                # EletricoNoturno
                # PsiquicoFada
                # PsiquicoVoador
                # PsiquicoFantasma
                # PsiquicoNoturno
                # PsiquicoDragao
                # PsiquicoGelo
                # GeloMetal
                # GeloFada
                # GeloVoador
                # GeloTerra
                # GeloFantasma
                # GeloFogo
                # GeloInseto
                
            # Evo Chain
            """evoImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
            evoImg = pygame.transform.scale(evoImg,(96,96))
            mainSurface.blit(evoImg,(610,218))"""

            # Porcentagem de genero
            porcmacho = str(DexInfo.pokeData["genderMale"])
            porcfemea = str(DexInfo.pokeData["genderFemale"])

            totalBarWidth = 255
            macho = DexInfo.pokeData["genderMale"]*(totalBarWidth/100)
            femea = (100-DexInfo.pokeData["genderFemale"])*(totalBarWidth/100)

            if DexInfo.pokeData["genderMale"] < 100 and DexInfo.pokeData["genderMale"] > 0:
                pygame.draw.rect(mainSurface,dexTypeColor,(655,342,5,30))
                Text.Write(mainSurface,(580,358,352),str(porcmacho) + "%",25,"joy.otf",(255,255,255),True)
                Text.Write(mainSurface,(630,358,352),"¹",25,"joy.otf",(0,120,200),True)
                Text.Write(mainSurface,(720,358,352),str(porcfemea) + "%",25,"joy.otf",(255,255,255),True)
                Text.Write(mainSurface,(765,358,352), "²",25,"joy.otf",(200,120,190),True)
                
            elif DexInfo.pokeData["genderMale"] >= 100 and DexInfo.pokeData["genderMale"] <= 200:
                Text.Write(mainSurface,(650,358,352),"100%",25,"joy.otf",(255,255,255),True)
                Text.Write(mainSurface,(690,358,352),"¹",25,"joy.otf",(0,120,200),True)

            elif DexInfo.pokeData["genderFemale"] <= 100:
                Text.Write(mainSurface,(650,358,352),"100%",25,"joy.otf",(255,255,255),True)
                Text.Write(mainSurface,(690,358,352),"²",25,"joy.otf",(200,120,190),True)
            else:
                Text.Write(mainSurface,(650,358,352),"Sem Gênero",25,"joy.otf",(255,255,255),True)
                
            Draw.RoundRect(mainSurface,(40,40,40),(20,374,110,39),10)
            Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(10,10,10))

            Text.Write(mainSurface,(28,376),"#" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])),35,"joy.otf",(255,255,255))
            
            if DexInfo.megaEvolutionSelected: Text.Write(mainSurface,(138,382),DexInfo.megaDataSingle["megaName"],25,"joy.otf",(255,255,255))
            else: Text.Write(mainSurface,(138,376),DexInfo.pokeData["name"],35,"joy.otf",(255,255,255))
        
            Text.Write(mainSurface,(20,425),"Espécie:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(20,445),"Region:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,425),DexInfo.pokeData["species"],20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,445),DexInfo.pokeData["regionName"],20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(180,445),"Generation:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(280,445),str(DexInfo.pokeData["regionID"]),20,"calibrilight.ttf",(255,255,255))

            pygame.draw.rect(mainSurface,dexTypeColor,(420,383,12,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(436,383,24,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(464,383,45,12))
            Text.Write(mainSurface,(425,396),"T  I  P  O  :",18,"joy.otf",dexTypeColor)

            if DexInfo.megaEvolutionSelected:
                if DexInfo.megaDataSingle["type2Name"] == None or DexInfo.megaDataSingle["type2Name"] == "":
                    Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.megaDataSingle["type1Name"])
                else:
                    Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.megaDataSingle["type1Name"])
                    Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.megaDataSingle["type2Name"])
            else:
                if DexInfo.pokeData["type2Name"] == None or DexInfo.pokeData["type2Name"] == "":
                    Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1Name"])
                else:
                    Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1Name"])
                    Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.pokeData["type2Name"])


            

            # Drawing Buttons before cycle (fixes visual bug)
            # Nav Buttons
            pygame.display.update(btnPrevDex.Show(False))
            pygame.display.update(btnPrevEvo.Show(False))
            pygame.display.update(btnNextEvo.Show(False))
            pygame.display.update(btnNextDex.Show(False))

            if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                pygame.display.update(btnReturn.Show(False))


                    
            # Gender & Form Buttons
            if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                pygame.display.update(btnFormNormalMale.Show(False))
                pygame.display.update(btnFormNormalFemale.Show(False))
                pygame.display.update(btnFormShinyMale.Show(False))
                pygame.display.update(btnFormShinyFemale.Show(False))
            else:
                pygame.display.update(btnFormNormal.Show(False))
                pygame.display.update(btnFormShiny.Show(False))

            # Screen Select Buttons
            pygame.display.update(btnEvoChainScreen.Show(False))
            pygame.display.update(btnStatsScreen.Show(False))


   
            DexInfo.evoChain = DexInfo.EvoChain()
            DexInfo.fullChain = DexInfo.FullChain()

            pygame.display.update()

            spriteReloaded = False
            DexInfo.loadNewPokemon = False

            DexInfo.oneTimeCycleLoad = True

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexInfo.loadNewPokemon:

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


                if DexInfo.pokeData["nextEvolution"] != None: nextEvoExists = True
                else: nextEvoExists = False

                if DexInfo.pokeData["prevEvolution"] != None: prevEvoExists = True
                else: prevEvoExists = False

############### RENDER ACTIVE BUTTONS ##################################################################
                if not DexInfo.thread.isAlive():
                    # Nav Buttons
                    pygame.display.update(btnPrevDex.Show())
                    pygame.display.update(btnPrevEvo.Show(disabled = not prevEvoExists))
                    if DexInfo.HasMultipleEvos(): pygame.display.update(btnNextEvoSelect.Show(disabled = not nextEvoExists))
                    else: pygame.display.update(btnNextEvo.Show(disabled = not nextEvoExists))
                    pygame.display.update(btnNextDex.Show())
                    
                    if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                        pygame.display.update(btnReturn.Show())


                    # Gender & Form Buttons
                    if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                        pygame.display.update(btnFormNormalMale.Show())
                        pygame.display.update(btnFormNormalFemale.Show())
                        pygame.display.update(btnFormShinyMale.Show())
                        pygame.display.update(btnFormShinyFemale.Show())
                    else:
                        pygame.display.update(btnFormNormal.Show())
                        pygame.display.update(btnFormShiny.Show())

                    # Screen Select Buttons
                    pygame.display.update(btnEvoChainScreen.Show())
                    pygame.display.update(btnStatsScreen.Show())

############### RENDER DUMMY BUTTONS ###################################################################
                else:
                    # Nav Buttons
                    pygame.display.update(btnPrevDex.Show(False))
                    pygame.display.update(btnPrevEvo.Show(False,not prevEvoExists))
                    pygame.display.update(btnNextEvo.Show(False,not nextEvoExists))
                    pygame.display.update(btnNextDex.Show(False))
                    
                    if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                        pygame.display.update(btnReturn.Show(False))
    
                    # Gender & Form Buttons
                    if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                        pygame.display.update(btnFormNormalMale.Show(False))
                        pygame.display.update(btnFormNormalFemale.Show(False))
                        pygame.display.update(btnFormShinyMale.Show(False))
                        pygame.display.update(btnFormShinyFemale.Show(False))
                    else:
                        pygame.display.update(btnFormNormal.Show(False))
                        pygame.display.update(btnFormShiny.Show(False))

                    # Screen Select Buttons
                    pygame.display.update(btnEvoChainScreen.Show(False))
                    pygame.display.update(btnStatsScreen.Show(False))

                # Animation-Cycle for the Sprite and Stat-Screens
############### STATUS SCREENS #########################################################################
                if DexInfo.statsScreenActive:
                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        Text.Write(evoChainSurface,(52,0),"Status",25,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(132,20),"Pokémon",25,"joy.otf",(255,255,255))

                        Draw.RoundRect(evoChainSurface,(40,40,40),(5,50,250,282),15,2,dexTypeColor,"Status Base")
                        UI.ProgressBar(evoChainSurface,(25,110),180,15,dexTypeColor,"PS",statMinMaxVals[0][0],statMinMaxVals[0][1],DexInfo.pokeData["statHP"])
                        UI.ProgressBar(evoChainSurface,(25,150),180,15,dexTypeColorDark,"Ataque",statMinMaxVals[1][0],statMinMaxVals[1][1],DexInfo.pokeData["statAtk"])
                        UI.ProgressBar(evoChainSurface,(25,190),180,15,dexTypeColor,"Defesa",statMinMaxVals[2][0],statMinMaxVals[2][1],DexInfo.pokeData["statDef"])
                        UI.ProgressBar(evoChainSurface,(25,230),180,15,dexTypeColorDark,"Ataque Especial",statMinMaxVals[3][0],statMinMaxVals[3][1],DexInfo.pokeData["statSpAtk"])
                        UI.ProgressBar(evoChainSurface,(25,270),180,15,dexTypeColor,"Defesa Especial",statMinMaxVals[4][0],statMinMaxVals[4][1],DexInfo.pokeData["statSpDef"])
                        UI.ProgressBar(evoChainSurface,(25,310),180,15,dexTypeColorDark,"Velocidade",statMinMaxVals[5][0],statMinMaxVals[5][1],DexInfo.pokeData["statSpd"])

                        Draw.RoundRect(evoChainSurface,(40,40,40),(265,2,205,150),15,2,dexTypeColor,"Training")
                        
                        Text.Write(evoChainSurface,(275,30),"Taxa de Captura:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(425,30),str(DexInfo.pokeData["catchRate"]) + "%",15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,50),"Amizade Base:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(400,50),str(DexInfo.pokeData["baseFriendship"]),15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,70),"Experiência Base:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(430,70),str(DexInfo.pokeData["baseExp"]),15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,90),"Cresc.:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(340,90),str(DexInfo.pokeData["growthRate"]),15,"joy.otf",(255,255,255))

                        Text.Write(evoChainSurface,(275,110),"EV-Yield:",15,"joy.otf",(180,180,180))
                        # Fetch EV-Yield data
                        parameters = (DexInfo.currentPokemon,)
                        DexInfo.c.execute("SELECT * FROM evYields LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id WHERE evYields.nationalDex = ?",parameters)
                        pmResult = DexInfo.c.fetchall()
                        evYieldTextOffset = 0
                        for evYield in pmResult:
                            Text.Write(evoChainSurface,(360,110 + evYieldTextOffset),str(evYield["evYieldPoints"]) + " " + evYield["evYieldType"],15,"joy.otf",(255,255,255))
                            evYieldTextOffset += 20


                        Draw.RoundRect(evoChainSurface,(40,40,40),(265,162,205,170),15,2,dexTypeColor,"Descrição")

                        Text.WriteMultiline(evoChainSurface,str(DexInfo.pokeData["dexInfo"]),(275,190),pygame.font.Font("calibrilight.ttf",18),(255,255,255))

                        mainSurface.blit(evoChainSurface,(23,23))
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(10,10,10))
                    pygame.display.update(0,0,526,366)


############### EVO SELECTION SCREEN ###################################################################
                elif DexInfo.evoSelectActive:
                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        if DexInfo.currentPokemon == 133: Text.Write(evoChainSurface,(250,30),"Select next eeveelution",25,"joy.otf",(255,255,255),True)
                        else: Text.Write(evoChainSurface,(250,30),"Select next evolution",25,"joy.otf",(255,255,255),True)
                        mainSurface.blit(evoChainSurface,(23,23))

                    horizontalOffset = 10
                    verticalOffset = 120

                    nextEvos = DexInfo.NextEvolutions()

                    if len(nextEvos) == 2: horizontalOffset = 140
                    elif len(nextEvos) == 3: horizontalOffset = 80
                    else: horizontalOffset = 10

                    if len(nextEvos) > 4: verticalOffset = 70

                    evoCount = 0

                    for evo in nextEvos:

                        typeColors = DexInfo.GetTypeColors(evo)

                        if horizontalOffset+23-2 < mouse[0] < horizontalOffset+110+23+2 and verticalOffset+23-2 < mouse[1] < verticalOffset+96+23+2:
                            Draw.RoundRect(evoChainSurface,(40,40,40),(horizontalOffset,verticalOffset,96,110),15,2,typeColors[1],"#" + str('{0:03d}'.format(evo)))
                            if click[0] == 1: DexInfo.ToggleDexNumber(evo)

                        else: 
                            Draw.RoundRect(evoChainSurface,(40,40,40),(horizontalOffset,verticalOffset,96,110),15,2,typeColors[0],"#" + str('{0:03d}'.format(evo)))

                        nextEvoImg = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(evo)) +"/sprite-small-FN-" + str('{0:03d}'.format(evo)) + ".png"),(96,96))
                        evoChainSurface.blit(nextEvoImg,(horizontalOffset,verticalOffset+20))
                        horizontalOffset += 120
                        evoCount += 1
                        if evoCount >= 4:
                            horizontalOffset = 10
                            verticalOffset += 120
                            evoCount = 0
                    
                    
                    mainSurface.blit(evoChainSurface,(23,23))
                    Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(10,10,10))
                    pygame.display.update(0,0,526,366)

############### EVO CHAIN SCREEN #######################################################################
                elif DexInfo.evoScreenActive:

                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        Text.Write(evoChainSurface,(240,25),"Grade de Evolução",25,"joy.otf",(255,255,255),True)
                        Text.Write(evoChainSurface,(420,60),"< Voltar",15,"joy.otf",(255,255,255),True)
                        Text.Write(evoChainSurface,(250,320),str(len(DexInfo.fullChain)) + " estagio de evolução",20,"joy.otf",(255,255,255),True)
                        

                        verticalOffset = 0
                        scaleFactor = 2
                        scaleOffsetCorrection = 48
                        scaleHorizontalCorrection = 48

                        if len(DexInfo.fullChain) == 1: horizontalOffset = 205
                        elif len(DexInfo.fullChain) == 2: horizontalOffset = 205 - 48 - 40
                        elif len(DexInfo.fullChain) == 3: horizontalOffset = 205 - 96 - 60
                        elif len(DexInfo.fullChain) == 4: horizontalOffset = 205 - 144 - 75

                        if len(DexInfo.fullChain) > 2: 
                            scaleFactor = 1
                            scaleOffsetCorrection = 0
                            scaleHorizontalCorrection = 0

                        for evoGroups in DexInfo.fullChain:
                            if len(evoGroups) > 1: 
                                scaleFactor = 1
                                scaleOffsetCorrection = 0
                                scaleHorizontalCorrection = 0

                        if len(DexInfo.fullChain) == 2 and scaleFactor == 2: horizontalOffset -= 20

                        for evoGroups in DexInfo.fullChain:

                            if len(evoGroups) == 1: verticalOffset = 131
                            elif len(evoGroups) == 2:verticalOffset = 83
                            else: verticalOffset = 35

                            evoItemCount = 0
                            for evoItem in evoGroups:
                                evoItemImg = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(evoItem)) +"/sprite-small-FN-" + str('{0:03d}'.format(evoItem)) + ".png"),(96*scaleFactor,96*scaleFactor))
                                evoChainSurface.blit(evoItemImg,(horizontalOffset-scaleOffsetCorrection,verticalOffset-scaleOffsetCorrection))
                                verticalOffset += 96
                                evoItemCount += 1
                                if evoItemCount >= 3: 
                                    horizontalOffset += 60
                                    verticalOffset = 35
                                    evoItemCount = 0
                            horizontalOffset += 150 + scaleHorizontalCorrection

                        mainSurface.blit(evoChainSurface,(23,23))
                        
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(10,10,10))
                        pygame.display.update(0,0,526,366)

############### ANIMATED SPRITE CYCLE ##################################################################
                else:

                    # Form Buttons
                    if DexInfo.pokeData["hasMultipleForms"] == 1:
                        
                        pygame.display.update(btnNextForm.Show())
                        pygame.display.update(btnPrevForm.Show())

                    # Alola Form Button
                    if DexInfo.pokeData["hasAlolaForm"] == 1:
                        pygame.display.update(btnAlolaToggle.Show())

                    # Mega Evolution Buttons
                    if DexInfo.pokeData["hasMegaEvolution"] != None:
                        megaStoneImg = pygame.transform.scale(pygame.image.load("megaStones/" + DexInfo.megaData[0]["megaStoneImage"]),(80,80))
                        mainSurface.blit(megaStoneImg,(10,290))
                        if 10 < mouse[0] < 90 and 290 < mouse[1] < 370:
                            Text.Write(mainSurface,(50,330),"Mega",18,"joy.otf",dexTypeColor,True)
                            if not DexInfo.sleepThread.isAlive() and click[0] == 1: 
                                DexInfo.ToggleMegaEvolution1()
                                DexInfo.sleepThread = Thread(target = time.sleep, args = (0.3,)) 
                                DexInfo.sleepThread.start()    
                        else: Text.Write(mainSurface,(50,330),"Mega",18,"joy.otf",(0,0,0),True)
                        pygame.display.update((14,274,92,92))

                        if len(DexInfo.megaData) > 1: 
                            megaStoneImg = pygame.transform.scale(pygame.image.load("megaStones/" + DexInfo.megaData[1]["megaStoneImage"]),(80,80))
                            mainSurface.blit(megaStoneImg,(10,220))
                            if 10 < mouse[0] < 90 and 220 < mouse[1] < 300:
                                Text.Write(mainSurface,(50,260),"Mega",18,"joy.otf",dexTypeColor,True)
                                if not DexInfo.sleepThread.isAlive() and click[0] == 1: 
                                    DexInfo.ToggleMegaEvolution2()
                                    DexInfo.sleepThread = Thread(target = time.sleep, args = (0.3,)) 
                                    DexInfo.sleepThread.start()    
                            else: Text.Write(mainSurface,(50,260),"Mega",18,"joy.otf",(0,0,0),True)
                            pygame.display.update((14,204,92,92))

                        
                        # Caixa de Sprite
                    if DexInfo.oneTimeCycleLoad: 
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(10,10,10))
                        Draw.RoundRect(mainSurface,(10,10,10),(412,18,90,90),21,2,dexTypeColor)
                        spriteImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
                        spriteImg = pygame.transform.scale(spriteImg,(96,96))
                        mainSurface.blit(spriteImg,(412-3,18-3))
                        Text.Write(mainSurface,(456,118),"Evoluções",12,"joy.otf",(255,255,255),True)

                        if DexInfo.pokeData["hasMultipleForms"] == 1: Text.Write(mainSurface,(250,25),"Form: " + DexInfo.formData["formName"],20,"joy.otf",(255,255,255),True)
                        if DexInfo.shinySelected: Text.Write(mainSurface,(260,350),"Shiny",20,"joy.otf",(255,255,255),True)
                        pygame.display.update(0,0,526,386)

                    if not DexInfo.thread.isAlive() and Sprite.loadedSpriteNr == DexInfo.currentPokemon:

                        if runtimeCtr % 1 == 0: 
                            Sprite.Cycle(Sprite.frameIndex,Sprite.tilesAmount,Sprite.frames)    
                            spriteSurface.fill((40,40,40))
                            spriteSurface.set_colorkey((0,0,0))
                            spriteSurface.blit(Sprite.current,Sprite.sprite)
                            mainSurface.blit(spriteSurface,(100,30))
                            pygame.display.update(100,30,300,300)
                    else:
                        spriteSurface.fill((40,40,40))
                        spriteSurface.set_colorkey((0,0,0))
                        if runtimeCtr % 2 == 0:
                            pygame.gfxdraw.aacircle(spriteSurface,120,150,8,dexTypeColor)
                            pygame.gfxdraw.aacircle(spriteSurface,150,150,8,dexTypeColorDark)
                            pygame.gfxdraw.aacircle(spriteSurface,180,150,8,dexTypeColor)
                            pygame.gfxdraw.filled_circle(spriteSurface,120,150,8,dexTypeColor)
                            pygame.gfxdraw.filled_circle(spriteSurface,150,150,8,dexTypeColorDark)
                            pygame.gfxdraw.filled_circle(spriteSurface,180,150,8,dexTypeColor)
                        else:
                            pygame.gfxdraw.aacircle(spriteSurface,120,150,8,dexTypeColorDark)
                            pygame.gfxdraw.aacircle(spriteSurface,150,150,8,dexTypeColor)
                            pygame.gfxdraw.aacircle(spriteSurface,180,150,8,dexTypeColorDark)
                            pygame.gfxdraw.filled_circle(spriteSurface,120,150,8,dexTypeColorDark)
                            pygame.gfxdraw.filled_circle(spriteSurface,150,150,8,dexTypeColor)
                            pygame.gfxdraw.filled_circle(spriteSurface,180,150,8,dexTypeColorDark)
                        pygame.draw.rect(mainSurface,(40,40,40),(22,330,476,36))
                        mainSurface.blit(spriteSurface,(100,30))


                        pygame.display.update(100,30,300,300)

                clock.tick(60)

                runtimeCtr += 1
                if runtimeCtr > 10000: runtimeCtr = 1

                DexInfo.oneTimeCycleLoad = False

                # Re-Triggers sprite-loading if thread failed
                if Sprite.loadedSpriteNr != DexInfo.currentPokemon: loadActiveCounter += 1
                else: loadActiveCounter = 0

                if not spriteReloaded and loadActiveCounter >= spriteReloadTrigger: 
                    DexInfo.LoadSpritesheet()  
                    spriteReloaded = True

                idleCtr += 1
                if click[0] == 1: idleCtr = 0
                if idleCtr > 1000:
                    idleCtr = 0
                    DexInfo.SleepState()
                    DexInfo.oneTimeCycleLoad = True
                    DexInfo.loadNewPokemon = True
        
        DexInfo.running = True
        return  DexInfo.currentPokemon

    def SleepState():
        # PyGame Initialisation
        clock = pygame.time.Clock()

        # Window and Surface Initialisation
        displayWidth = 800
        displayHeight = 480

        try:
            if os.uname()[1] == 'raspberrypi': 
                mainSurface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            else: 
                mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
                pygame.mouse.set_visible(True)
        except:
            mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
            pygame.mouse.set_visible(True)

        run = True

        """pygame.draw.rect(mainSurface,(20,20,20),(0,0,800,480))
        sleepSurface = pygame.Surface((600,300)).convert_alpha()
        sleepImg = pygame.image.load("sleeping.png").convert_alpha()

        runtimeCtr = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                run = False

            sleepSurface.fill((20,20,20))
            sleepSurface.set_colorkey((0,0,0))
            if runtimeCtr % 2 == 0: sleepSurface.blit(sleepImg,(0,0))
            else: sleepSurface.blit(sleepImg,(-600,0))
            mainSurface.blit(sleepSurface,(100,180))
            Text.Write(mainSurface,(400,140),"Sleeping...",30,"joy.otf",(200,200,200),True)
            pygame.display.update()
                
            runtimeCtr += 1
            if runtimeCtr > 100: runtimeCtr = 0

            clock.tick(2)
        return"""

