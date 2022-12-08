import pyxel
import random



# taille de la fenetre
TAILLE_FEN_HOR = 128
TAILLE_FEN_VER = 128
# taille du pad 
TAILLE_PAD_HOR = 24
TAILLE_PAD_VER = 8
#taille de la balle (multiple de 2)
TAILLE_BALLE = 6
# taille de la brique
TAILLE_BRIQUE_HOR = 8  #changer en 8 ou 16
TAILLE_BRIQUE_VER = 4   #changer en 4 ou 8
NOMBRE_RANGEES_BRIQUES = 8  #changer en 4 ou 8
NOMBRE_BRIQUES = int(TAILLE_FEN_HOR/TAILLE_BRIQUE_HOR * NOMBRE_RANGEES_BRIQUES)

# ne pas modifier
pyxel.init(TAILLE_FEN_HOR, TAILLE_FEN_VER, title="Casse brique Margot Germond")
# chargement des images
pyxel.load("briques2.pyxres")

#chargement du son
pyxel.load("platformer.pyxres",False, False, True, True)
pyxel.playm(0, loop=True)

# position initiale du pad
# (origine des positions : coin haut gauche)
pad_x = (TAILLE_FEN_HOR -TAILLE_PAD_HOR)/2
pad_y = (TAILLE_FEN_VER-TAILLE_PAD_VER)

#vitesse initiale/step=1
pad_step = 3
ball_speed_step = 1
ball_speed = [-1,-1]

#compteur pour augmenter la vitesse toutes les 30 secondes
COMPTEUR_VITESSE = 30*30
compteur = 0

# initialisation des balles
MAX_BALLES = 1
nombre_balles = 0
balles_liste = []
briques_liste = []
explosions_liste = []

init_jeu = False

#debug
stopDraw = False

def init_partie():
    # remise à 0/valeurs initiales
    global nombre_balles,balles_liste,briques_liste,explosions_liste
    global compteur,ball_speed_step,ball_speed
    nombre_balles = 0
    balles_liste = []
    briques_liste = []
    explosions_liste = []
    compteur = 0
    ball_speed_step = 1
    ball_speed = [-1,-1]


def pad_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < (TAILLE_FEN_HOR-TAILLE_PAD_HOR)) :
            x = x + pad_step
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - pad_step
#    if pyxel.btn(pyxel.KEY_DOWN):
#        if (y < 120) :
#            y = y + 1
#    if pyxel.btn(pyxel.KEY_UP):
#        if (y > 0) :
#            y = y - 1
    return x, y
        
# =========================================================
# == CREATION BALLE(s)
# =========================================================        
def balles_creation(x, y, balles_liste):
    """création d'une balle avec la barre d'espace"""
    
    global nombre_balles

    # btnr pour eviter les balles multiples
    if pyxel.btnr(pyxel.KEY_SPACE):
        if (nombre_balles < MAX_BALLES):
            balles_liste.append([x+4, y-4])
            nombre_balles += 1
    return balles_liste

# =========================================================
# == CREATION BRIQUES
# =========================================================
def briques_creation(briques_liste):
    global init_jeu
    # Liste de brique crée au départ
    if not init_jeu :
       x_brique = y_brique = 0
       couleur_brique = NOMBRE_RANGEES_BRIQUES
#       print (NOMBRE_BRIQUES)
       for i in range(NOMBRE_BRIQUES):
          briques_liste.append([x_brique, y_brique, couleur_brique])
          x_brique = x_brique + TAILLE_BRIQUE_HOR
          if(((i+1)%(NOMBRE_BRIQUES/NOMBRE_RANGEES_BRIQUES)) == 0):
               #nouvelle rangée
               x_brique = 0
               y_brique = y_brique + TAILLE_BRIQUE_VER
               couleur_brique = couleur_brique -1
       init_jeu = True # La partie peut commencer   
    return briques_liste

# =========================================================
# == DEPLACEMENT BALLE(s)
# =========================================================  
def balles_deplacement(balles_liste, briques_liste):
    """déplacement de la balle """
    global premier_contact, contact, stopDraw, nombre_balles

    for balle in balles_liste:
# A calculer suivant le vecteur vitesse
# detection des murs
        if (balle[0] + ball_speed[0] >= TAILLE_FEN_HOR - TAILLE_BALLE/2):
            # collision mur droit
            ball_speed[0] = -ball_speed[0]
            pyxel.play(3,8) 

        if (balle[0] + ball_speed[0] <= 0 + TAILLE_BALLE/2):
            # collision mur gauche
            ball_speed[0] = -ball_speed[0]
            pyxel.play(3,8)
            
        if (balle[1] + ball_speed[1] <= 0 + TAILLE_BALLE/2):
            # collision mur haut
            ball_speed[1] = -ball_speed[1]
            pyxel.play(3,8)
            
        # Balle touche PAD ?
        #if (balle[1] + ball_speed[1] + TAILLE_BALLE/2) >= pad_y :
        if (balle[1] + TAILLE_BALLE/2) >= pad_y :
            if(((balle[0] + TAILLE_BALLE/2) > pad_x) and
               ((balle[0] - TAILLE_BALLE/2) < (pad_x + TAILLE_PAD_HOR))):
               if not contact :
                   premier_contact = True
                   contact = True
               if premier_contact:
                   # contact horizontal ou lateral/vertical ?
                   if(balle[1]>= pad_y) and (balle[1] <= pad_y + TAILLE_PAD_VER):
                       # Contact lateral inversion vitesse horizontale
                       ball_speed[0] = -ball_speed[0]
#                   else:
                       # Contact vertical (au dessous/en dessous)
                   ball_speed[1] = -ball_speed[1] # dans tous les cas, on remonte la balle
                   premier_contact = False
#                   stopDraw = True
                   pyxel.play(3,10) 
        else:
            contact = False
            premier_contact = False
       

        # Balle touche brique ?
        for brique in briques_liste: 
        # balle x compatible avec contact ?
            if(((balle[0] + TAILLE_BALLE/2) >= brique[0]) and
               ((balle[0] - TAILLE_BALLE/2) <= brique [0] + TAILLE_BRIQUE_HOR)):
             # balle y compatible avec contact ?
                 if(((balle[1] + TAILLE_BALLE/2) >= brique[1]) and
                    ((balle[1] - TAILLE_BALLE/2) <= brique[1] + TAILLE_BRIQUE_VER)):
                # Contact
                     pyxel.play(3,9) 

                     if(balle[1]>= brique[1]) and (balle[1] <= brique[1] + TAILLE_BRIQUE_VER):
                         # Contact lateral
                         ball_speed[0] = -ball_speed[0]
                     else:
                         # Contact vertical (au dessous/en dessous)
                         ball_speed[1] = -ball_speed[1]
                     explosions_creation(brique[0] + TAILLE_BRIQUE_HOR/2, brique[1] + TAILLE_BRIQUE_VER/2)
                # comptabilise le nombre de contacts de la brique
                     brique[2] = brique[2] -1
                     if brique[2] == 0 : briques_liste.remove(brique)

        balle[0] += ball_speed[0]
        balle[1] += ball_speed[1]
 
        if  balle[1]>TAILLE_FEN_VER - TAILLE_BALLE/2:
            balles_liste.remove(balle)
            nombre_balles = nombre_balles-1
            pyxel.play(3,11)

    return balles_liste

def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])


def explosions_animation():
    """animation des explosions"""
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)
            
# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global pad_x, pad_y, compteur, balles_liste, ball_speed, ball_speed_step
    global nombre_balles, init_jeu
    # Nouvelle partie ?
    if not init_jeu : init_partie()
    
    # mise à jour de la position du pad
    pad_x, pad_y = pad_deplacement(pad_x, pad_y)
    
    briques_listes = briques_creation(briques_liste)
    
    # creation des balles en fonction de la position du pad
    balles_liste = balles_creation(pad_x, pad_y, balles_liste)

    # mise a jour des positions des balles
    balles_liste = balles_deplacement(balles_liste, briques_liste)
    
    # evolution de l'animation des explosions
    explosions_animation()    
       
    # mise à jour de la vitesse de la balle
    if (compteur == COMPTEUR_VITESSE):
        compteur = 0
        if ball_speed[0] > 0 :
            ball_speed[0] += ball_speed_step
        else:
            ball_speed[0] -= ball_speed_step
        if ball_speed[1] > 0 :
            ball_speed[1] += ball_speed_step
        else:
            ball_speed[1] -= ball_speed_step
    else:
        compteur += 1
    
    # mise à jour de l'état du jeu
    if nombre_balles == 0: init_jeu = False #Perdu
    elif briques_liste == []: init_jeu = False #Gagne

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""
    # Debug
    global stopDraw, nombre_balles
    if not stopDraw:

    # vide la fenetre
       pyxel.cls(0)
    
    # pad (rectangle 8x8)
       #pyxel.rect(pad_x, pad_y, TAILLE_PAD_HOR, TAILLE_PAD_VER, 1)
       pyxel.blt(pad_x, pad_y, 0, 32, 40,TAILLE_PAD_HOR, TAILLE_PAD_VER)
        
    # explosions (cercles de plus en plus grands)
       for explosion in explosions_liste:
          pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)   

# test si il reste une/des balles en jeu
       if nombre_balles == 0:
          pyxel.text(11,64, 'GAME OVER - SPACE TO START', 8)
       else:
    # test si il reste une/des briques en jeu
          if briques_liste == []:
            pyxel.text(30,64, 'CONGRATS : YOU WON', 7)
          else:
               for balle in balles_liste:
#        pyxel.rect(balle[0], balle[1], 1, 4, 10
                   pyxel.circb(balle[0], balle[1],TAILLE_BALLE/2,random.randint(1,10))
               for brique in briques_liste:
              # Dessin différent en fonction du niveau
                  #pyxel.rect(brique[0], brique[1], TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER, brique[2])
                  if (brique[2] == 1):
                      pyxel.blt(brique[0], brique[1], 0, 0, 46,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 2):
                      pyxel.blt(brique[0], brique[1], 0, 0, 32,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 3):
                      pyxel.blt(brique[0], brique[1], 0, 0, 39,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 4):
                      pyxel.blt(brique[0], brique[1], 0, 0, 53,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 5):
                      pyxel.blt(brique[0], brique[1], 0, 0, 60,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 6):
                      pyxel.blt(brique[0], brique[1], 0, 0, 67,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 7):
                      pyxel.blt(brique[0], brique[1], 0, 0, 76,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)
                  elif (brique[2] == 8):
                      pyxel.blt(brique[0], brique[1], 0, 0, 83,TAILLE_BRIQUE_HOR, TAILLE_BRIQUE_VER)


pyxel.run(update, draw)
