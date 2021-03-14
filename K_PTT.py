from itertools import combinations 
Q=["A","B","C","D","E","G"]
F=[[["A","B"],["C"]], [["A","C"],["D"]], [["D"],["E","G"]], [["G"],["B"]], [["A"],["D"]], [["C","G"],["A"]]]

def check_exists(A,B):
    if A is None or B is None:
        return False
    if(len(A)>len(B)):
        A,B = B,A
    tmp_bool=True
    for a in A:
        if a in B:
            tmp_bool = (tmp_bool and True)
        else:
            tmp_bool = (tmp_bool and False)
    return tmp_bool


def equal(A,B):
    if A is None or B is None:
        return False
    if len(A) != len(B):
        return False
    return check_exists(A, B)

def qplus(Q,F):
    Q = Q.copy()
    Qnew=list()
    while(True):
        Qnew=list(Q.copy())
        # print(Qnew)
        for f in F:
            tmp_bool=True
            for iVT in f[0]:
                if iVT in Q:
                    tmp_bool=(tmp_bool and True)
                else:
                    tmp_bool=(tmp_bool and False)
            if tmp_bool:
                if Qnew is not None:
                    Qnew.extend(f[1])
                    Qnew = list(set(Qnew))              
        # print(Qnew)
        # print("Q"+str(Q))
        if(equal(Q,Qnew)):
            break
        else:
            Q = Qnew.copy()
    return Qnew


def getK(Q,F):
    keys=list()
    TN=list()
    TTG=list()
    for q in Q:
        VT = False
        VP = False
        for f in F:
            if q in f[0]:
                VT=True
            if q in f[1]:
                VP=True
        if VT and VP:
            TTG.append(q)
        elif VT:
            TN.append(q)
    tmp = qplus(TN,F)
    # print(TN)
    # print(TTG)
    # print(tmp)
    # print(equal(tmp, Q))
    if equal(tmp, Q):
        return TN
    else:
        for r in range(len(TTG)):
            for i_cTTG in combinations(TTG, r):
                tmp_TN=TN.copy()
                # print(i_cTTG)
                tmp_TN.extend(list(i_cTTG))
                tmp_TN = list(set(tmp_TN))
                # print(tmp_TN)
                if equal(qplus(tmp_TN,F),Q):
                    # print(tmp_TN)
                    isSuperKey=True
                    for key in keys:
                        if check_exists(tmp_TN,key):
                            isSuperKey=isSuperKey and False
                    if isSuperKey:
                        keys.append(tmp_TN)
            # if len(keys)>0:
            #     break
        return keys


print(getK(Q,F))


def getPTT(Q,F):
    G = list()
    
    # Step 1
    for f in F:
        if len(f[1])>1:
            f_tmp = f.copy()
            for i_f in f[1]:
                # print(i_f)
                f_tmp[1] = [i_f]
                G.append(f_tmp.copy())
                # print(G)
        else:
            G.append(f.copy())
    # print(G)

    # Step 2
    while(True):
        isChanged=False
        for f in G:
            if len(f[0])>1:
                for i_cTTG in combinations(f[0], 1):
                    G_tmp = G.copy()
                    f0_tmp=f[0].copy()
                    f0_tmp.remove(i_cTTG[0])
                    G_tmp.remove(f)
                    qplus_res = qplus(f0_tmp, G_tmp)
                    if check_exists(i_cTTG, qplus_res):
                        G_tmp.append([f0_tmp.copy(), f[1].copy()])
                        G=G_tmp.copy()
                        isChanged=True
            if(isChanged):
                break
        if not isChanged:
            break

    #Step 3
    while(True):
        isChanged=False
        for f in G:
            G_tmp = G.copy()
            f0_tmp, f1_tmp=f[0].copy(),f[1].copy()
            G_tmp.remove(f)
            qplus_res = qplus(f0_tmp, G_tmp)
            if check_exists(f1_tmp, qplus_res):
                G=G_tmp.copy()
                isChanged=True
            if(isChanged):
                break
        if not isChanged:
            break
    return G


print(getPTT(Q,F))
