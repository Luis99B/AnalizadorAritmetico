# Luis Bodart   A01635000

from collections import deque
from re import *
from tkinter import *

# tamaño y pos de la ventana
def window(frame, width=500, height=520):
    frame.title("Analizador Aritmetico")
    frame.minsize(width, height)
    frame.maxsize(width, height)
    frame.resizable(False, False)
    screenW = frame.winfo_screenwidth()
    screenH = frame.winfo_screenheight()
    x = (screenW/2) - (width/2)
    y = (screenH/2.15) - (height/2)
    frame.geometry("%dx%d+%d+%d" % (width, height, x, y))

# aplicacion
class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.widgets()

    # widgets principales
    def widgets(self):
        self.label = Label(self, text="Expresion Aritmetica", width=60)
        self.label.grid(row=1, column=1, columnspan=3, sticky=W+E)

        self.expresion = Entry(self, width=50)
        self.expresion.grid(row=2, column=1, columnspan=2, sticky=W+E)

        self.validar = Button(self, text="Validar expresion", command=self.validaExpr)
        self.validar.grid(row=2, column=3, sticky=N+S+W+E)

        self.expresionValida = Label(self, text="\n\n")
        self.expresionValida.grid(row=4, column=1, columnspan=3, sticky=W+E)

        self.canvas = Canvas(self, width=400, height=400, bg='#fff')
        self.canvas.grid(row=7, column=1, columnspan=3, sticky=N+S+W+E)

    # valida que la expresion sea valida y checar si los parentesis estan balanceados '[0-9][+-*()]'
    def validaExpr(self):
        expr = self.expresion.get()
        self.expresionValida.config(text="\n\n")
        self.canvas.delete('all')
        self.w = self.canvas.winfo_reqwidth() + 10
        self.h = self.canvas.winfo_reqheight() - 20
        # print("%d, %d" % (w, h))
        if len(expr) == 0 or expr.isspace():
            self.canvas.create_text(
                self.w / 2, self.h / 2, text="Expresion\nInvalida", font='bold 32', justify='center')
            return

        expr = sub('\s+', "", expr)

        # checar que la expresion solo contenga 0-9+-*()
        carac = len(findall('[\d(+\-*)]', expr))
        if len(expr) != carac:
            invalidos = findall('[^\d(+\-*)]', expr)
            caracInvalidos = ""
            for i in range(len(invalidos) - 1):
                caracInvalidos += invalidos[i] + ","
                if i != 0 and i % 9 == 0:
                    caracInvalidos += "\n"
            caracInvalidos += invalidos[len(invalidos) - 1]
            # print(len(caracInvalidos))
            self.canvas.create_text(self.w / 2, self.h / 2, text="Incluye\n" + caracInvalidos + "\nque son\ncaracteres invalidos", font='bold 32', justify='center')
            return
        """
        print("letras", len(findall('[A-Za-z]', expr)))
        print("digitos", len(findall('\d', expr)))
        print("+", len(findall('[+]', expr)))
        print("-", len(findall('[-]', expr)))
        print("*", len(findall('[*]', expr)))
        print("()", len(findall('[()]', expr)))
        print("(+-*)", len(findall('[(+\-*)]', expr)))
        print("validos", len(findall('[\d(+\-*)]', expr)))
        """
        self.expresionValida.config(text=expr)

        # checar que los parentesis esten balanceados
        tokens = list(expr)
        stack = deque()
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if len(stack) > 0:
                    stack.pop()
                else:
                    self.canvas.create_text(self.w / 2, self.h / 2, text="Hay error\nen los\nparentesis", font='bold 32', justify='center')
                    return
        if len(stack) != 0:
            self.canvas.create_text(self.w / 2, self.h / 2, text="Faltan %d" % len(stack)+"\nparentesis\nde cierre", font='bold 32', justify='center')
        else:
            # checar que los operadores sean validos por su orden
            for i in range(len(tokens)):
                token = tokens[i]
                if i == 0:
                    if token == '*':
                        self.canvas.create_text(self.w / 2, self.h / 2, text="Expresion\nInvalida", font='bold 32', justify='center')
                        return
                elif i == len(tokens) - 1:
                    if token == '+' or token == '-' or token == '*':
                        self.canvas.create_text(self.w / 2, self.h / 2, text="Expresion\nInvalida", font='bold 32', justify='center')
                        return
                elif token == '+' or token == '-':
                    if tokens[i - 1] == '+' or tokens[i - 1] == '-':
                        self.canvas.create_text(self.w / 2, self.h / 2, text="Expresion\nInvalida", font='bold 32', justify='center')
                        return
                elif token == '*':
                    if tokens[i - 1] == '+' or tokens[i - 1] == '-' or tokens[i - 1] == '*':
                        self.canvas.create_text(self.w / 2, self.h / 2, text="Expresion\nInvalida", font='bold 32', justify='center')
                        return

            self.convertirPostfija(expr)

    # convertir la expresion infija a postfija
    def convertirPostfija(self, infija):
        postfija = deque()
        tokens = list()
        lista = list(infija)
        num = ""
        # mantener los numeros que son mas de un digito
        for i in range(len(lista)):
            token = lista[i]
            if token.isdigit():
                num += token
                if i == len(lista) - 1:
                    tokens.append(num)
            else:
                if token == '(' or num == "":
                    tokens.append(token)
                else:
                    tokens.append(num)
                    tokens.append(token)
                    num = ""
        # print(tokens)

        # convertir a postfija usando la jeraquia de operadores
        entrada = deque()
        operadores = deque()
        for i in range(len(tokens), 0, -1):
            entrada.append(tokens[i - 1])
        while entrada:
            token = entrada[len(entrada) - 1]
            prioridad = self.prioridad(token)
            if prioridad == 1:
                operadores.append(entrada.pop())
            elif prioridad == 2:
                if operadores:
                    while operadores[len(operadores) - 1] != '(':
                        postfija.append(operadores.pop())
                    operadores.pop()
                    entrada.pop()
            elif prioridad == 3 or prioridad == 4:
                if operadores:
                    operadorPrioridad = self.prioridad(
                        operadores[len(operadores) - 1])
                    while operadores and operadorPrioridad >= prioridad:
                        if len(postfija) > 1 and operadorPrioridad >= prioridad:
                            postfija.append(operadores.pop())
                            if operadores:
                                operadorPrioridad = self.prioridad(
                                    operadores[len(operadores) - 1])
                        else:
                            postfija.append(entrada.pop())
                            if entrada:
                                prioridad = self.prioridad(
                                    entrada[len(entrada) - 1])
                operadores.append(entrada.pop())
            else:
                postfija.append(entrada.pop())
        while operadores:
            postfija.append(operadores.pop())

        self.evaluarPostfija(postfija)

    # checar la jeraquia de operadores
    def prioridad(self, token):
        if token == '*':
            return 4
        elif token == '+' or token == '-':
            return 3
        elif token == ')':
            return 2
        elif token == '(':
            return 1
        else:
            return 9

    # evaluar la expresion postija
    def evaluarPostfija(self, postfija):
        tokens = list(postfija)
        stack = deque()
        resultado = float()
        # print(tokens)
        n1 = float()
        n2 = float()
        res = float()
        pos = 0
        #print("tokens Evaluar", tokens)
        for token in tokens:
            if token.isdigit():
                stack.append(float(token))
            else:
                if token == '+':
                    if len(stack) > 1:
                        n2 = float(stack.pop())
                        n1 = float(stack.pop())
                        res = n1 + n2
                    else:
                        n1 = float(stack.pop())
                        res = + n1
                elif token == '-':
                    if len(stack) > 1:
                        n2 = float(stack.pop())
                        n1 = float(stack.pop())
                        res = n1 - n2
                    else:
                        n1 = float(stack.pop())
                        res = - n1
                elif token == '*':
                    if len(stack) > 1:
                        n1 = float(stack.pop())
                        n2 = float(stack.pop())
                        res = n2 * n1
                    else:
                        t = tokens.pop(pos + 1)
                        if tokens[pos + 1] == '+':
                            n1 = float(t)
                            res = + n1
                        elif tokens[pos + 1] == '-':
                            n1 = float(t)
                            res = - n1
                        tokens.insert(pos, "-%s" % t)
                        pos -= 1
                stack.append(float(res))
            pos += 1
        # print(stack)
        resultado = stack.pop()
        #print("resultado %d" % resultado)
        self.arbolDerivacion(tokens, resultado)

    # muestra el arbol de derivacion de la expresion
    def arbolDerivacion(self, tokens, resultado):
        postfija = ""
        for i in range(len(tokens) - 1):
            postfija += tokens[i] + " "
        postfija += tokens[len(tokens) - 1]
        self.expresionValida.config(text=self.expresionValida.cget('text') + "\n" + postfija + "\n{0:.2f}".format(resultado))
        arbol = Arbol(tokens)
        nodo = arbol.root
        maxNivel = arbol.maxNivel()
        if maxNivel == 1:
            nodo.x = self.w / 2
            nodo.y = self.h / 2
            self.canvas.create_text(nodo.x, nodo.y, text=nodo.valor, font='bold 24', justify='center')
        elif maxNivel == 2:
            nodo.x = self.w / 2
            nodo.y = self.h / 3.5
            self.canvas.create_text(nodo.x, nodo.y, text=nodo.valor, font='bold 24', justify='center')
            if nodo.izq:
                nodo.izq.x = self.w / 2.75
                nodo.izq.y = self.h / 1.75
                self.canvas.create_text(nodo.izq.x, nodo.izq.y, text=nodo.izq.valor, font='bold 20', justify='center')
                self.canvas.create_line(
                    nodo.x, nodo.y + 10, nodo.izq.x, nodo.izq.y - 20)
            if nodo.der:
                nodo.der.x = self.w / 1.5
                nodo.der.y = self.h / 1.75
                self.canvas.create_text(nodo.der.x, nodo.der.y, text=nodo.der.valor, font='bold 20', justify='center')
                self.canvas.create_line(nodo.x, nodo.y + 10, nodo.der.x, nodo.der.y - 20)
        elif maxNivel > 6:
            self.canvas.create_text(self.w / 2, self.h / 2, text="Arbol de derivacion\nmuy grande\npara dibujarlo", font='bold 32', justify='center')
        else:
            # print(maxNivel)
            nodo.x = self.w / maxNivel + (self.w * .2)
            nodo.y = self.h / (maxNivel + 1.5) - (self.h * .05)
            self.espacio = (self.h / (maxNivel + 1.5) + (self.h * .05))
            self.dibujarArbol(nodo, maxNivel)

    # dibuja cada nodo del arbol dentro del canvas
    def dibujarArbol(self, nodo, nivel):
        if nodo is None:
            return
        #print("\nnivel:", nivel)
        if nodo.izq and nodo.der:
            if nodo.dibujar:
                #print("nodo %s, (X, Y) (%d, %d)" % (nodo.valor, nodo.x, nodo.y))
                self.canvas.create_text(nodo.x, nodo.y, text=nodo.valor, font='bold 24', justify='center')
                nodo.dibujar = False
        if nodo.izq:
            if nodo.izq.dibujar:
                nodo.izq.x = nodo.x + (self.w * .05) - self.espacio * (nivel / 8)
                nodo.izq.y = nodo.y + self.espacio
                if not (nodo.izq.izq and nodo.izq.der):
                    #print("izq %s, (X, Y) (%d, %d)" % (nodo.izq.valor, nodo.izq.x, nodo.izq.y))
                    self.canvas.create_text(nodo.izq.x, nodo.izq.y, text=nodo.izq.valor, font='bold 20', justify='center')
                    self.canvas.create_line(nodo.x, nodo.y + 10, nodo.izq.x, nodo.izq.y - 15)
                    nodo.izq.dibujar = False
                else:
                    #print("nodo izq es padre")
                    self.canvas.create_line(nodo.x, nodo.y + 10, nodo.izq.x, nodo.izq.y - 15)
        if nodo.der:
            if nodo.der.dibujar:
                nodo.der.x = nodo.x + (self.w * .05) + (self.espacio * 1.5) * (nivel / 8)
                nodo.der.y = nodo.y + self.espacio
                if not (nodo.der.izq and nodo.der.der):
                    #print("der %s, (X, Y) (%d, %d)" % (nodo.der.valor, nodo.der.x, nodo.der.y))
                    self.canvas.create_text(nodo.der.x, nodo.der.y, text=nodo.der.valor, font='bold 20', justify='center')
                    self.canvas.create_line(nodo.x, nodo.y + 10, nodo.der.x, nodo.der.y - 15)
                    nodo.der.dibujar = False
                else:
                    #print("nodo der es padre")
                    self.canvas.create_line(nodo.x, nodo.y + 10, nodo.der.x, nodo.der.y - 15)
        self.dibujarArbol(nodo.izq, nivel - 1)
        self.dibujarArbol(nodo.der, nivel - 1)

# clase Nodo
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.dibujar = True
        self.x = 0
        self.y = 0

# clase Arbol
class Arbol:
    def __init__(self, tokens):
        self.root = self.crearArbol(tokens)

    def crearArbol(self, tokens):
        stack = deque()
        for token in tokens:
            if token.isdigit():
                nodo = Nodo(token)
                stack.append(nodo)
            else:
                nodo = Nodo(token)
                nodo.der = stack.pop()
                if stack:
                    nodo.izq = stack.pop()
                stack.append(nodo)
        return stack.pop()

    def lista(self):
        lista = list()
        return self.avanzarArbol(lista, self.root)

    def avanzarArbol(self, lista, nodo):
        if nodo is None:
            return lista
        lista.append(nodo)
        self.avanzarArbol(lista, nodo.izq)
        self.avanzarArbol(lista, nodo.der)
        return lista

    def maxNivel(self):
        return self.nivel(self.root)

    def nivel(self, nodo):
        if nodo is None:
            return 0
        return max(self.nivel(nodo.izq), self.nivel(nodo.der)) + 1


tk = Tk()
window(tk)
app = App(tk)
app.mainloop()
