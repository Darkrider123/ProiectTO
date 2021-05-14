import numpy as np
import matplotlib.pyplot as plt
import random

######## FUNCTII PT GENERARE DI ##########

def exponentiala(lamb):
    u = random.random()
    
    return - 1/lamb * np.log(u)


def norm(miu, sigma):

    while True:
        y = exponentiala(1)

        u1 = random.random()
        u2 = random.random()

        if u1 <= np.exp(- ((y-1)**2)/2 ): 
            x = y
            if u2 <= 1/2:
                x = -np.abs(x)
                return miu + sigma*x
            else:
                x = np.abs(x)
                return miu + sigma* x



def verificare_vector_di(di):

    for elem in di:
        if elem < 0:
            return False
    
    return True

def generare_di(x, ai):

    r = norm(0, 10)

    di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
    di = np.array(di)

    while verificare_vector_di(di) == False or r < 0:
        
        r = norm(0, 20)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di

def generare_di_ce_reurneaza_si_r(x, ai):

    r = norm(0, 10)

    di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
    di = np.array(di)

    while verificare_vector_di(di) == False or r < 0:
        
        r = norm(0, 10)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di, r



######### FUNCTII PT GPS_LS si CF_LS ##########


def r(x, ai, di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = vec - di

    rez = 1/m * sum(vec)
    

    rez = np.abs(rez)
    rez = np.floor(rez)

    return rez


def T(x, ai, di):
    
    m = len(ai)

    vec = [np.linalg.norm(x - a) for a in ai]

    vec = [ix / a for ix,a in zip(x-ai, vec)]

    factor_stang = r(x,ai,di) + di

    vec = [a * b for a,b in zip(factor_stang,vec)]

    return 1/m * sum(ai) + 1/m * sum(vec)



def generare_A_caciula(a):

    A_caciula = list()

    for elem in a:    
        linie = [2* np.transpose( elem ) , -1]
        linie = np.array(linie, dtype=object)
        A_caciula.append(linie)

    A_caciula = np.array(A_caciula, dtype=object)
    return A_caciula



def verificare_asumption_matrice(a):

    A_caciula = generare_A_caciula(a)

    for linie in A_caciula:
        if sum(linie[0]) == 0:
            return False
    
    return True




############ FUNCTII PT GPS_SLS #############



def generare_B(a, d):
    m = len(a)
    B = list()

    for i in range(m):
        aux = [2* np.transpose(a[i]) , -1 , 2* d[i]]
        B.append(aux)
    
    B= np.array(B, dtype=object)

    return B


def generare_b(a, d):
    
    m = len(a)
    b = list()

    b = [np.linalg.norm(ai)**2 - di**2 for ai, di in zip(a,d)]
    b = np.array(b)

    return b



def generare_In(n):

    In = generare_On(n)

    for i in range(n):
        for j in range(n):
            if i == j:
                In[i][j] = 1

    return In

def generare_On(n):
    
    return np.array([ np.array([0 for i in range(n)]) for i in range(n)])


def generare_D(n):
    
    D = list()

    linie = [generare_In(n), generare_On(n), generare_On(n)]
    linie = np.array(linie, dtype=object)
    D.append(linie)

    linie = [np.transpose(generare_On(n))   ,  0    ,    0]
    linie = np.array(linie, dtype=object)
    D.append(linie)

    linie = [np.transpose(generare_On(n)),     0        ,   -1]
    linie = np.array(linie, dtype=object)
    D.append(linie)

    return D

def generare_g(n):
    linie = [generare_On(n) , 1, 0]
    linie = np.array(linie, dtype=object)
    
    rez = list()
    for elem in linie:
        rez.append( elem * 1/2)

    
    return rez





def generare_E(n):

    E = list()

    linie = [generare_In(n), generare_On(n)]
    linie = np.array(linie, dtype=object)

    E.append(linie)


    linie = [np.transpose(generare_On(n)) , 0]
    linie = np.array(linie, dtype=object)

    E.append(linie)

    return E


def generare_beta(n, a):
    E = generare_E(n)
    A_caciula = generare_A_caciula(a)

    rez = E@( np.transpose(A_caciula) @ A_caciula)      # Cine naiba s-a gandit ca poate inmulti matrici de genul?


def cautare_lambda_caciula(B, D):

    lambda_caciula = None

    while True:
        G = np.transpose(B)@B + lambda_caciula * D

        flag = True
        for elem in np.eigvalues(G):
            if elem == False:
                flag = False
        
        if flag == True:
            return lambda_caciula
        
        lambda_caciula = lambda_caciula / 2







############### FUNCTII PT x0 OPTIM PENTRU GPS_LS FOLOSIND GPS_SLS ##################

"""alg pag 22 +  lema 5.1 pagina 21 
Find x0 satisfying : f(x0) < min {f(a1), ..f(an), fliminf }
f_liminf = np.
"""

def h(x,ai,di,j):
    m = len(ai) -1
    copy_ai = ai
    copy_ai= np.delete(ai,j)
    vec = [np.linalg.norm(x - a) for a in copy_ai]
    vec = sum(vec)
    vec = vec/m
    return m

def g(x,ai,di,j):
    m = len(ai) -1
    copy_ai = ai
    copy_ai= np.delete(ai,j)
    copy_di = di
    copy_di = np.delete(di,j)
    vec = [np.linalg.norm(x-a) for a in copy_ai]
    vec = vec - copy_di
    vec =  vec^2
    vec = sum(vec)
    return vec

def f(x,ai,di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = (vec - di)
    vec = np.square(vec)
    vec = sum(vec)

    vec = vec - m * r(x,ai,di)**2
   
    return vec


"""Gaseste x0 optim pentru GSP LS : """

def find_x0(ai,di):
    m = len(ai)
    f_liminf = np.zeros_like(ai[0])  ## gresit!!! nu stiu cum 
    vec = [f(a,ai,di) for a in ai]
    minn = min(vec)
    if np.less(f_liminf,minn).all():
        x0 = f_liminf  ### gresit !!!!  x0 = x_sls  => nu stiu cine e 
        return x0
    
    p = vec.index(minn)
    a_p = vec[p]
    if r(ai[p]) > 0 :
        z1 =  - np.gradient(g(a_p,ai,di,p)) + 2 * m * r(a_p) * np.gradiend(h(a_p,ai,di,p))
        if z1 != 0:
            v = z1/np.linalg.norm(z1)
        else:
            v = np.random.randn(*z1.shape)
            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
    else:
        z = np.gradient(g(a_p,ai,di,p))
        if z != 0 :
            v= - z/np.linalg.norm(z)
        else:
            v = np.random.randn(*z.shape)
            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
    
    s = 1 
    while f(a_p + s*v) >= f(a_p):
        s = s/2
    
    xo = a_p + s*v
    return x0