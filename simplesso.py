def find_base(m, tipo='b'): # tipo = 'b' per base, 'c' per non base
    B = [0, 0, 0]
    X_N = []

    for j in range(len(m[0])):
        v_colonna = [m[0][j], m[1][j], m[2][j]]
        
        if v_colonna == [1, 0, 0]:
            B[0] = j
        elif v_colonna == [0, 1, 0]:
            B[1] = j
        elif v_colonna == [0, 0, 1]:
            B[2] = j
        else:
            X_N.append(j)
    
    if tipo == 'c':
        return X_N
    else:
        return B
    
def calcola_gamma_zero(N_T, c_B, c_N): # N_T = matrice non di base, c_B = vettore variabili di base della funzione obiettivo, c_N = vettore variabili non di base della funzione obiettivo
    vet = []
    for i in range(len(N_T)):
        sum = 0
        for j in range(len(N_T[i])):
            sum += c_B[j] * N_T[i][j] 
        vet.append(c_N[i] - sum) 
    return vet

def calcola_matrice_non_di_base(m, x_N): # m = matrice, x_N = vettore delle variabili non di base
    N_T = []
    for n in x_N:
        v = []
        for i in range(len(m)):
            v.append(m[i][n])
        N_T.append(v)
    return N_T

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

u = [1, 2, 1, 1, 1, 1]
m = [[1, 2, 3, 1, 0, 0], [2, -1, -5, 0, 1, 0], [1, 2, -1, 0, 0, 1]]
B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

x_b = find_base(m, 'b') #vettore degli indici delle variabili di base
x_n = find_base(m, 'c') #vettore degli indici delle variabili non di base
n_t = calcola_matrice_non_di_base(m, x_b) #matrice non di base
c_b = [u[k] for k in x_b] #vettore delle variabili di base della funzione obiettivo 
c_n = [u[k] for k in x_b] #vettore delle variabili non di base della funzione obiettivo

print(f"x_b: {x_b}")
print(f"x_n: {x_n}")
print(f"c_b: {c_b}")
print(f"c_n: {c_n}")
print(f"n_t: {n_t}")

g_0 = calcola_gamma_zero(n_t, c_b, c_n)
print(f"Gamma zero: {g_0}")

print("test di illimitatezza: ", end='') 
print(test_illimitatezza(g_0, n_t)) #test di illimitatezza

variabile_entrante = 0
