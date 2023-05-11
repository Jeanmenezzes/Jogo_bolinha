from tkinter import *
import pdb, functools

#CLASSE PRINCIPAL DO JOGO
class joguinho(object):
    def __init__(self):
        #DEFININDO OS ATRIBUTOS PRINCIPAIS DO PROGRAMA
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Jogo Simples")
        self.root.wm_iconbitmap('icone jogo.ico')
        self.frame_Geral = Frame(self.root)
        self.frame_Geral.pack()

        self.fonte_Um = ('Arial', '32', 'bold')
        self.label_Um = Label(self.frame_Geral, text = '\n\nBem Vindo!\n', font = self.fonte_Um)
        self.label_Um.pack()

        self.botao_Um = Button(self.frame_Geral, text = 'Clique aqui para iniciar o jogo', command = self.criaJogo, bg = 'lightgray')
        self.botao_Um.pack()
        self.botao_Um.focus_force()
        self.botao_Um.bind('<Return>', self.criaJogo)

    def criaJogo(self, event = False):
        self.label_Um.destroy()
        self.botao_Um.destroy()

        self.frame_FE_Um = Frame(self.frame_Geral, height = 50)
        self.frame_FE_Um.pack()
        
        self.canvas_Um = Canvas(self.frame_Geral, width = 700, height = 500, bg = "black")
        self.canvas_Um.pack()

        #ANIMAÇÃO DE FUNDO
        #self.framesFundo = [PhotoImage(file = 'psico_bg/psico_%.2i.gif'%x).zoom(2) for x in range(1,91)]
        #self.fundo = self.canvas_Um.create_image(350, 250, image = self.framesFundo[0])

        coord_Um = [6, 20]
        coord_Dois = [116, 40]
        self.retangulos = []

        for i in range(6):
            for j in range(6):
                self.retangulo = self.canvas_Um.create_rectangle(coord_Um, coord_Dois, fill = 'blue', tag = 'rec%i%i'%(i,j))
                self.retangulo_esq = self.canvas_Um.create_rectangle(coord_Um, [coord_Um[0]+2,coord_Dois[1]-1], fill = 'blue', tag = 'rec%i%i'%(i,j))
                self.retangulo_drt = self.canvas_Um.create_rectangle([coord_Dois[0]-2,coord_Um[1]], [coord_Dois[0], coord_Dois[1]-1], fill = 'blue', tag = 'rec%i%i'%(i,j))
                self.retangulo_front = self.canvas_Um.create_rectangle([coord_Um[0],coord_Dois[1]-2], coord_Dois, fill = 'blue', tag = 'rec%i%i'%(i,j))
                
                self.retangulos.append(self.retangulo)
                coord_Um[0] = coord_Dois[0] + 6
                coord_Dois[0] = coord_Um[0] + 110
                
            coord_Um[1] = coord_Dois[1] + 5
            coord_Dois[1] = coord_Um[1] + 20
            coord_Um[0] = 6
            coord_Dois[0] = 116

        self.player_vx = 0
        self.player_posx = 275
        self.player_posy = 450
        self.player = self.canvas_Um.create_rectangle([self.player_posx, self.player_posy],[self.player_posx + 150, self.player_posy + 25], fill = "red", tag = "player")
        self.player_dir = self.canvas_Um.create_rectangle([self.player_posx, self.player_posy],[self.player_posx+2, self.player_posy +25], fill= 'red', tag = 'player')
        self.player_esq = self.canvas_Um.create_rectangle([self.player_posx +148, self.player_posy],[self.player_posx+150, self.player_posy +25], fill= 'red', tag = 'player')
        self.player_front = self.canvas_Um.create_rectangle([self.player_posx, self.player_posy],[self.player_posx+150, self.player_posy +2], fill= 'red', tag = 'player') 

        self.posx_bola = 335
        self.posy_bola = 350
        self.bola = self.canvas_Um.create_oval([self.posx_bola, self.posy_bola],[self.posx_bola+30, self.posy_bola+30], fill = "yellow", tag = "bola")
        self.vx_bola = 10
        self.vy_bola = 10

        self.botao_Dois = Button(self.frame_Geral, text = 'Iniciar Jogo', command = functools.partial(self.start,None))
        self.botao_Dois.focus_force()
        self.botao_Dois.pack()
        self.botao_Dois.bind("<Return>", self.start)

    def modificaVX(self, event):
        self.player_vx = 0

    def movePlayer(self,event):
        if event.keysym == 'Left':
            self.player_vx = -20

        elif event.keysym == 'Right':
            self.player_vx = 20

        else:
            self.player_vx = 0

    def start(self, event):
        self.canvas_Um.focus_force()
        self.iniciar()    

    def iniciar(self):
        self.canvas_Um.bind('<Any-KeyPress>', self.movePlayer)
        self.canvas_Um.move('player', self.player_vx, 0)
        self.canvas_Um.bind('<Any-KeyRelease>', self.modificaVX)
        
        #self.botao_Dois['command'] = None
        self.box_bola = self.canvas_Um.bbox("bola")
        self.colisoes = list(self.canvas_Um.find_overlapping(self.box_bola[0], self.box_bola[1], self.box_bola[2], self.box_bola[3]))

        #ANIMAÇÃO DE FUNDO
        #self.colisoes.remove(self.fundo)
        #self.fundo = self.canvas_Um.create_image(350, 250, image = self.framesFundo[50])
        #self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)

        self.posx_bola += self.vx_bola
        self.posy_bola += self.vy_bola 
        
        if self.posx_bola >= 700 or self.posx_bola <= 0:
            if len(self.colisoes) > 1:
                self.vy_bola = 10
                self.vx_bola = -1 * self.vx_bola
                self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)
            else:
                self.vx_bola = -1 * self.vx_bola
                self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)
            
        elif self.posy_bola >= 500 or self.posy_bola <= 0:
            self.vy_bola = -1 * self.vy_bola
            self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)

        elif len(self.colisoes) > 1:
            if self.player in self.colisoes:
                if self.player_dir in self.colisoes:
                    self.vx_bola = -10
                elif self.player_esq in self.colisoes:
                    self.vx_bola = 10
                if self.player_front in self.colisoes:
                    self.vy_bola = -10
                self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)
            else:
                for i in self.colisoes:
                    if i % 4 == 0:
                        self.front = i
                        self.drt = i -1
                        self.esq = i -2
                        self.rec = i -3
                if self.drt in self.colisoes:
                    self.vx_bola = 10
                elif self.esq in self.colisoes:
                    self.vx_bola = - 10
                if self.front in self.colisoes:
                    self.vy_bola = 10
                self.tag = self.canvas_Um.itemcget(self.rec, 'tag')
                self.canvas_Um.delete(self.tag)
                self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)
        else:
            self.canvas_Um.move('bola', self.vx_bola, self.vy_bola)

        self.root.after('33', func = self.iniciar)

if __name__ == '__main__':
    master = joguinho()
#PRÓXIMA ETAPA
#GARANTIR QUE CASO ALGUMA VELOCIDADE SE TORNE 0 NA PRÓXIMA COLISÃO COM AS LATERAIS OU AS VERTICAIS DO CANVAS IRÁ MUDAR ESSA VELOCIDADE
#DEFINIR A DERROTA E VITÓRIA DO PLAYER
#REORGANIZAR TODO O APLICATIVO EM MÓDULOS E PASTAS DISTINTOS E ADICIONAR A DESCRIÇÃO DAS LINHAS DO CÓDIGO

