from fractions import Fraction
from copy import deepcopy

def leggi_variabili(file):
    with open(file, 'r') as file:
        cont = file.read()
    variables = {}
    exec(cont, variables)
    return variables['u'], variables['m'], variables['b']

def B_generator(m):
    B = []
    for i in range(len(m)):
        row = [0 for k in range(len(m))]
        row[i] = 1
        B.append(row)
    return B
def find_base(m, tipo='b'): # tipo = 'b' per base, 'c' per non base
    x_b = [-1] * len(m)
    x_n = []

    for j in range(len(m[0])):
        col = [m[i][j] for i in range(len(m))]
        if col.count(1) == 1 and col.count(0) == len(col) - 1:
            posizione = col.index(1)
            if x_b[posizione] == -1:
                x_b[posizione] = j
            else:
                x_n.append(j)
        else:
            x_n.append(j)
    if tipo == 'c':
        return x_n
    else:
        return x_b    
   
def calcola_gamma_zero(N_T, c_B, c_N): # N_T = matrice non di base, c_B = vettore variabili di base della funzione obiettivo, c_N = vettore variabili non di base della funzione obiettivo
    vet = []
    for i in range(len(N_T)):
        sum = 0
        for j in range(len(N_T[i])):
            sum += c_B[j] * N_T[i][j] 
        vet.append(Fraction(c_N[i] - sum)) 
    return vet

def calcola_matrice_non_di_base(m, x_N): # m = matrice, x_N = vettore delle variabili non di base
    N_T = []
    for n in x_N:
        v = []
        for i in range(len(m)):
            v.append(Fraction(m[i][n]))
        N_T.append(v)
    return N_T

def test_ottimo(g):
    verificato = True
    for elem in g:
        if elem < 0:
            verificato = False
    return verificato

def test_illimitatezza(g_0, N_T): # g_0 = vettore dei costi ridotti, N_T = matrice non di base
    test_tot = False
    for k in range(len(g_0)): 
        if g_0[k] < 0:
            col_neg = True
            for i in range(len(N_T[k])): 
                if N_T[k][i] > 0:
                    col_neg = False
            if col_neg == True:
                test_tot = True

    return test_tot

def criterio_uscita(indice_entrante, N_t, b):
    elementi = []
    for j in range(len(b)):
        if N_t[indice_entrante][j] > 0:
            elementi.append(b[j] / N_t[indice_entrante][j])
        else:
            elementi.append(float('inf'))
    return elementi.index(min(elementi))

def trasposta_matrice(m):
    m_t = []
    for j in range(len(m[0])):
        v = []
        for i in range(len(m)):
            v.append(m[i][j])
        m_t.append(v)
    return m_t

def costruzione_base_canonica(M, v_entrante, k, b, voglio_vettore =None):
    N = deepcopy(M)
    a = deepcopy(v_entrante)
    for j in range(len(N[0])):
        N[k][j] = (Fraction(Fraction(N[k][j]), Fraction(v_entrante[k])))
        a[k] = Fraction(Fraction(b[k]), Fraction(v_entrante[k]))

 
    for i in range(len(N)):
        if i != k:
            for j in range(len(N[i])):
                N[i][j] = Fraction(Fraction(N[i][j])) + (Fraction(N[k][j]) * Fraction((-v_entrante[i])))
            a[i] = Fraction(b[i]) + (Fraction(a[k]) * Fraction(-v_entrante[i]))


    if voglio_vettore:
        return a
    else:
        return N

def nuova_coppia_vettori_indici(x_b, x_n, indice_variabile_entrante, indice_variabile_uscente):
    x_bc = deepcopy(x_b)
    x_nc = deepcopy(x_n)
    
    x_bc[indice_variabile_uscente] = x_n[indice_variabile_entrante]
    x_nc[indice_variabile_entrante] = x_b[indice_variabile_uscente]
    
    return [x_bc, x_nc]

def soluzione(x_b, b):
    soluzione = [0 for elem in u] #dimensione della soluzione
    for i in range(len(b)):
        if b[i].denominator > 1000 or b[i].numerator > 1000:
            soluzione[x_b[i]] = (round(float(b[i]),2))
        else:
            soluzione[x_b[i]] = b[i]
    return soluzione

def print_matrice(m):
    n = []
    for i in range(len(m)):
        r = []
        for j in range(len(m[i])):
            if isinstance(m[i][j], Fraction):
                if m[i][j].denominator == 1:
                    r.append(int(m[i][j].numerator))
                elif m[i][j].denominator > 1000 or m[i][j].numerator > 1000:
                    r.append(round(float(m[i][j]),2))
                else:
                    r.append(f"{m[i][j].numerator}/{m[i][j].denominator}")
            else:
                r.append(m[i][j])
        n.append(r)
    return n

def print_vettore(v):
    u = []
    for el in v:
        if isinstance(el, Fraction):
            if el.denominator == 1:
                u.append(int(el.numerator))
            elif el.denominator > 1000 or el.numerator > 1000:
                u.append(round(float(el),2))
            else:
                u.append(f"{el.numerator}/{el.denominator}")        
        else:
            u.append(el)
    return u

u, m, b = leggi_variabili('dati.txt')

B = B_generator(m) #matrice base
x_b = find_base(m, 'b') #vettore degli indici delle variabili di base
x_n = find_base(m, 'c') #vettore degli indici delle variabili non di base
N_t = calcola_matrice_non_di_base(m, x_n) #matrice non di base


def simplesso(x_b, x_n, N_t, b, u, iterazione =0):

    print(f"\n** Iterazione: {iterazione} **\n")
    if iterazione == 5:
        return
    
    c_b = [u[k] for k in x_b] #vettore delle variabili di base della funzione obiettivo
    c_n = [u[k] for k in x_n] #vettore delle variabili non di base della funzione obiettivo
    
    print("\nForma canonica:\n")
    print(f"x_b: {x_b}")
    print(f"x_n: {x_n}")
    print(f"c_b: {c_b}")
    print(f"c_n: {c_n}")
    print(f"N_t: {print_matrice(N_t)}")
    print(f"b: {print_vettore(b)}\n")

    print("\nCalcolo dei costi ridotti: ")
    g_0 = calcola_gamma_zero(N_t, c_b, c_n)
    print(f"Gamma zero: {print_vettore(g_0)}")

    print("\nTest di ottimalità: ", test_ottimo(g_0))


    if test_ottimo(g_0):
        return soluzione(x_b, b)

    print("\nTest di illimitatezza: ", end='') 
    print(test_illimitatezza(g_0, N_t)) #test di illimitatezza
    if test_illimitatezza(g_0,N_t):
        return -1

    print("\n\nCostruzione nuova base ammissibile:\n")

    indice_variabile_entrante = g_0.index(min(g_0))
    vettore_entrante = N_t[indice_variabile_entrante]
    print(f"Indice variabile entrante: {indice_variabile_entrante}")
    print(f"Vettore entrante: {print_vettore(vettore_entrante)}")

    indice_variabile_uscente = criterio_uscita(indice_variabile_entrante, N_t, b)
    vettore_uscente = B[indice_variabile_uscente]
    print(f"Indice variabile uscente: {indice_variabile_uscente}")
    print(f"Vettore uscente: {print_vettore(vettore_uscente)}")

    N_1_t = [] #nuova matrice non di base trasposta

    for i in range(len(N_t)):
        if i == indice_variabile_entrante:
            N_1_t.append(vettore_uscente)
        else:
            N_1_t.append(N_t[i])

    N_1 = trasposta_matrice(N_1_t)
    print(f"Nuova matrice N: {print_matrice(N_1)}\n")

    print("\nCostruzione nuova forma canonica:\n")

    N_c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b)
    b_c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b, 1)

    print(f"nuova matrice fuori base: {print_matrice(N_c)}")
    print(f"nuovo vettore soluzione: {print_vettore(b_c)}")

    N_c_t = trasposta_matrice(N_c)
    print(f"trasposta matrice fuori base: {print_matrice(N_c_t)}\n\n")

    coppia = nuova_coppia_vettori_indici(x_b, x_n, indice_variabile_entrante, indice_variabile_uscente)
    x_bc = coppia[0]
    x_nc = coppia[1]

    print('Nuova forma canonica:\n')
    print(f"x_b: {x_bc}")
    print(f"x_n: {x_nc}")
    print(f"c_b: {c_b}")
    print(f"c_n: {c_n}")
    print(f"N_t: {print_matrice(N_c_t)}")
    print(f"b: {print_vettore(b_c)}\n")

    return simplesso(x_bc, x_nc, N_c_t, b_c, u, iterazione + 1)


soluz = simplesso(x_b, x_n, N_t, b, u)

if soluz == -1:
    print("\nIl problema non ha soluzione")
else:
    print(f"\nSoluzione: {print_vettore(soluz)}")

'''
u = [3, 2, 1, 1] #vettore dei costi
m = [[1, 0, -1, 2], [0, 1, 2, -1]] #matrice di partenza
b = [5, 3] #vettore dei termini noti
'''