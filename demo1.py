import pyxel

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 55
        self.vaisseau_y = 120

        pyxel.run(self.update, self.draw)


    def vaisseau_deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x<120:
            self.vaisseau_x += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x>0:
            self.vaisseau_x += -1


    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.vaisseau_deplacement()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)

        # vaisseau (carre 8x8)
        pyxel.rect(self.vaisseau_x, 8, 8, 1)

Jeu()






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

# ne pas modifier
pyxel.init(TAILLE_FEN_HOR, TAILLE_FEN_VER, title="Casse brique Margot Germond")

# position initiale du pad
# (origine des positions : coin haut gauche)
pad_x = (TAILLE_FEN_HOR -TAILLE_PAD_HOR)/2
pad_y = (TAILLE_FEN_VER-TAILLE_PAD_VER)

#vitesse initiale/step=1
pad_step = 1
ball_speed_step = 1
ball_speed = [-1,-1]

#compteur pour augmenter la vitesse toutes les 30 secondes
COMPTEUR_VITESSE = 30*30
compteur = 0

# initialisation des balles
MAX_BALLES = 1
nombre_balles = 0
balles_liste = []
premier_contact = False
contact = False

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
# == DEPLACEMENT BALLE(s)
# =========================================================  
def balles_deplacement(balles_liste):
    """déplacement de la balle """
    global premier_contact, contact

    for balle in balles_liste:
# A calculer suivant le vecteur vitesse
# detection des murs
        if (balle[0] + ball_speed[0] >= TAILLE_FEN_HOR - TAILLE_BALLE/2):
            # collision mur droit
            ball_speed[0] = -ball_speed[0]
        
        if (balle[0] + ball_speed[0] <= 0 + TAILLE_BALLE/2):
            # collision mur gauche
            ball_speed[0] = -ball_speed[0]
            
        if (balle[1] + ball_speed[1] <= 0 + TAILLE_BALLE/2):
            # collision mur haut
            ball_speed[1] = -ball_speed[1]
            
        # Balle touche PAD ?
        #if (balle[1] + ball_speed[1] + TAILLE_BALLE/2) >= pad_y :
        if (balle[1] + TAILLE_BALLE/2) >= pad_y :
            if(((balle[0] + TAILLE_BALLE/2) >= pad_x) and
               ((balle[0] - TAILLE_BALLE/2) <= pad_x + TAILLE_PAD_HOR)):
               if not contact :
                   premier_contact = True
                   contact = True
               if premier_contact:
                   ball_speed[1] = -ball_speed[1]
                   premier_contact = False
                   
        else:
            contact = False
            premier_contact = False
       
        #if (balle[1] + ball_speed[1] >= TAILLE_FEN_VER - TAILLE_BALLE/2):
            # collision mur bas  = balle perdue
            # ball_speed[1] = -ball_speed[1]
    
        balle[0] += ball_speed[0]
        balle[1] += ball_speed[1]
        
        if  balle[1]>TAILLE_FEN_VER - TAILLE_BALLE/2:
            balles_liste.remove(balle)

    return balles_liste


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global pad_x, pad_y, compteur, balles_liste, ball_speed, ball_speed_step
    pyxel.text(50,64, 'GAME OVER', 7)

    # mise à jour de la position du pad
    pad_x, pad_y = pad_deplacement(pad_x, pad_y)
    
    # creation des balles en fonction de la position du pad
    balles_liste = balles_creation(pad_x, pad_y, balles_liste)

    # mise a jour des positions des balles
    balles_liste = balles_deplacement(balles_liste)
     
    # test si il reste une/des balles en jeu
    if balles_liste == False:
        pyxel.text(50,64, 'GAME OVER', 7)
    
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

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # pad (rectangle 8x8)
    pyxel.rect(pad_x, pad_y, TAILLE_PAD_HOR, TAILLE_PAD_VER, 1)
    
    # balles
    for balle in balles_liste:
#        pyxel.rect(balle[0], balle[1], 1, 4, 10
        pyxel.circb(balle[0], balle[1],TAILLE_BALLE/2,random.randint(1,10))
    
    
    


pyxel.run(update, draw)
