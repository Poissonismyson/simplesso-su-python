def findbase(m, tipo = 'b'): # inserisci la matrice e restituisce il vettore XB0, altrimenti X_N se inserisci 'c'
    B = [0,0,0]
    X_N = []


    for j in range(len(m[0])):
    
        v_colonna = [m[0][j],m[1][j],m[2][j]]
        
    
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
    
def calcolaGammaZero(N_T, c_B, c_N):
    vet = []
    for i in range(len(N_T)):
        sum = 0
        for j in range(len(N_T[i])):
            sum += c_B[j] * N_T[i][j] 
        vet.append(c_N[i]- sum) 
    return vet

def calcolaMatriceNonDiBase(m, x_N):
    N_T = []
    for n in x_N: # funzione per ottenere matrice non di base
        v = []
        for i in range(len(m)):
            v.append(m[i][n])
        N_T.append(v)
    return N_T

def testIllimitatezza(g_0, N_T):
    test_tot = False
    for k in range(len(g_0)): 
      if g_0[k] < 0: # stiamo prendendo le componenti negative di gamma
            col_neg = True
            for i in range(len(N_T[k])): 
              if N_T[k][i] > 0:
                  col_neg = False
            if col_neg == True:
                test_tot = True

    return test_tot



u= [1, 2, 1, 1, 1, 1] # vettore direzione di min o max

m =  [[1, 2, 3, 1, 0, 0], [2, -1, -5, 0, 1, 0], [1, 2, -1, 0, 0, 1]] # matrice di partenza
B = [[1, 0, 0],[0, 1, 0],[0, 0, 1]] #base canonica

x_B = findbase(m) # vettore indici di base

x_N = findbase(m, 'c') # vettore indici non di base

N_T = calcolaMatriceNonDiBase(m, x_N) # matrice non di base trasposta



c_B = [u[k] for k in x_B] #vettore c_b

c_N = [u[k] for k in x_N] #vettore c_n

print(f"x_B: {x_B}")
print(f"x_N: {x_N}")
print(f"c_B: {c_B}")
print(f"c_N: {c_N}")
print(f"N_T: {N_T}")



g_0 = calcolaGammaZero(N_T, c_B, c_N) #questa è la nostra gamma_0

print(f"Gamma zero: {g_0}")

print("test di illimitatezza: ", end='')

print(testIllimitatezza(g_0, N_T))




