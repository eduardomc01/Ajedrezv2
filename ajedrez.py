#false = blancas
#true = negras

import chess
import time


board = chess.Board()
start_time = time.time()

aux = []
aux4 = []
aux5 = []
tiroCPU = []


class arbol():

    def __init__(self, coordenada, peso, heuristica, tipo):
        self.coordenada = coordenada
        self.peso = peso
        self.tipo = tipo
        self.heuristica = heuristica
        self.hijos = []


    def AgregarNivelesDefault(self, nodo, peso, tipo):
            nodo.hijos.append(arbol(None, peso, None, tipo)) # ingresando apartir de raiz -> en hijos


    def AgregarSubNivel(self, nodo):
        for i in range(len(aux4)):
            if aux4[i][0:1] == "K":
                n = self.funcionBusquedaNodo(nodo,"k")
                n.hijos.append(arbol(aux4[i],None, 6 + (100 * chess.square_distance(i,board.king(False))) - (10 * i),   "k"))
                #print("Rey")

            elif aux4[i][0:1] == "Q":
                n = self.funcionBusquedaNodo(nodo,"q")
                n.hijos.append(arbol(aux4[i],None,  5 + (100 * chess.square_distance(i,board.king(False))) - (10 * i), "q"))
                #print("Reyna")

            elif aux4[i][0:1] == "R":
                n = self.funcionBusquedaNodo(nodo,"r")
                n.hijos.append(arbol(aux4[i],None, 4 + (100 * chess.square_distance(i,board.king(False))) - (10 * i), "r"))
                #print("Torre")

            elif aux4[i][0:1] == "B":
                n = self.funcionBusquedaNodo(nodo,"b")
                n.hijos.append(arbol(aux4[i],None, 3 + (100 * chess.square_distance(i,board.king(False))) - (10 * i), "b"))
                #print("Alfil")

            elif aux4[i][0:1] == "N":
                n = self.funcionBusquedaNodo(nodo,"n")
                n.hijos.append(arbol(aux4[i],None, 2 + (100 * chess.square_distance(i,board.king(False))) - (10 * i), "n"))
                #print("Caballo")

            else:
                n = self.funcionBusquedaNodo(nodo,"p")
                n.hijos.append(arbol(aux4[i],None, 1 + (100 * chess.square_distance(i,board.king(False))) - (10 * i), "p"))
                #print("Peon")


    def funcionBusquedaNodo(self, nodo, nodo_buscar):
        if(nodo.tipo == nodo_buscar):
            return nodo
        else:
            for x in nodo.hijos:
                e = self.funcionBusquedaNodo(x, nodo_buscar)
                if(e != None):
                    return e



    def funcionTipoDeFichas(self, nodo, color=False):
        for x in range(1,7):
            a = chess.Piece(x,color)
            self.AgregarNivelesDefault(nodo,x,a.symbol())


    def funcionEncontrarValorDondeTiro(self):
        self.funcionObtenerNegrasyBlancasExistentes()


    def funcionTiro(self, t):
        cord = chess.Move.from_uci(str(t))
        board.push(cord)


    def funcionMovimientosPosibles(self):
        aux.append(str(board.legal_moves))
        a = aux[0][39:].split(", ")

        for x in range(len(a)):
            if len(a[x]) == 4:
                e = a.pop()
                a.append(e[0:2])

        for x in range(len(a)):
            aux4.append(a[x])


    def limpiarListas(self):
        for i in range(len(aux)):
            aux.pop()

        for i in range(len(aux4)):
            aux4.pop()

        for i in range(len(aux5)):
            aux5.pop()

        for i in range(len(tiroCPU)):
            tiroCPU.pop()


    def limpiarArbol(self, nodo):
        for i in nodo.hijos:
            nodo.hijos.pop()
            return self.limpiarArbol(nodo)


    def imprimirArbol(self,nodo,nivel):
    	print(nivel,nodo.coordenada, nodo.peso, nodo.heuristica, nodo.tipo)
    	for n in nodo.hijos:
    		self.imprimirArbol(n,nivel+"-")


    def busquedaHeuristicaMenor(self,nodo):
        aux5.append(nodo.heuristica)
        for n in nodo.hijos:
            self.busquedaHeuristicaMenor(n)


    def componerLista(self):
        listaHeuristicaMenor=[]

        for i in range(len(aux5)):
            if(aux5[i] != None):
                listaHeuristicaMenor.append(aux5[i])

        return min(listaHeuristicaMenor)

    def busquedaTiroXHeuristicaMenor(self, nodo, busqueda_h):
        if(nodo.heuristica == busqueda_h):
            return tiroCPU.append(nodo.coordenada)

        for n in nodo.hijos:
            self.busquedaTiroXHeuristicaMenor(n, busqueda_h)



    def FuncionTiroMaquina(self, nodo):
        self.busquedaHeuristicaMenor(nodo)
        self.busquedaTiroXHeuristicaMenor(nodo, self.componerLista())
        n.funcionTiro(board.parse_san(tiroCPU[0]))

        print("Tiempo de ejecución --> ", time.time() - start_time)

        self.ChecarJaqueyJaqueMate()


    def ChecarJaqueyJaqueMate(self):
        if board.is_check():
            print('Jaque')
        else:
            pass

        if board.is_checkmate():
            print('Jaque Mate')
            board.is_game_over()
        else:
            pass


n = arbol("raiz",None,None,None)

print("Examen - Ajedrez")

while(True):

    print("\n----------------")
    print(board.unicode())
    print("----------------")

    tiro = input("\nDonde tirar ?:")
    n.funcionTiro(tiro)

    n.ChecarJaqueyJaqueMate()

    n.funcionTipoDeFichas(n)
    n.funcionMovimientosPosibles()
    n.AgregarSubNivel(n)
    #n.imprimirArbol(n,"-")

    n.FuncionTiroMaquina(n)

    n.limpiarArbol(n)
    n.limpiarListas()

    print("-----------------------------")
