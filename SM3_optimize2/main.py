# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import binascii
import time


IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
T = [0x79cc4519, 0x7a879d8a]
V=[]
V.append(IV)  #B是512bit
def bin1(text):
    result = bin(text)[2:]
    if len(result)%4 !=0:
        result = (4-len(result)%4)*'0'+result
    return result
def BIN(text):
    result=bin(text)[2:]
    if len(result)<32:
        result = (32-len(result))*'0'+result
    return result
def convert(plain_text):
    plain_text=binascii.b2a_hex(plain_text).decode('ascii')
    result = bin1(int(plain_text,16))
    k = 512-(len(result)+65)%512
    length = (64-len(bin(len(result))[2:]))*'0'+bin(len(result))[2:]
    result = result +'1'+k*'0'+length
    return result

def shift(text,n):
    n = n%32
    text = text[n:]+text[:n]
    return text
def P0(text):
    text = BIN(int(text, 2) ^ int(shift(text, 9), 2) ^ int(shift(text, 17), 2))
    return text
def P1(text):
    text = BIN(int(text,2)^int(shift(text,15),2)^int(shift(text,23),2))
    return text

def xor(a,b,c):
    r = BIN(int(a,2)^int(b,2)^int(c,2))
    return r

# def expand(result):
#     W = []
#     for i in range(16):
#         W.append(result[i*32:(i+1)*32])
#     for i in range(16,68):
#         W.append(xor(P1(xor( W[i-16],W[i-9],(shift(W[i-3],15)))),shift(W[i-13],7),W[i-6] ))
#     W1 = []
#     for j in range(64):
#         W1.append(BIN(int(W[j],2)^int(W[j+4],2)))
#     return W,W1
def expand(result):
    W = []
    for i in range(4):
        W.append(result[i*32:(i+1)*32])
    # for i in range(16,68):
    #     W.append(xor(P1(xor( W[i-16],W[i-9],(shift(W[i-3],15)))),shift(W[i-13],7),W[i-6] ))
    W1 = []
    # for j in range(64):
    #     W1.append(BIN(int(W[j],2)^int(W[j+4],2)))
    return W,W1

def FF(X,Y,Z,j):
    if j<16:
        result = BIN(int(X,2)^int(Y,2)^int(Z,2))
    if j>15:
        result=BIN((int(X,2)&int(Y,2))|(int(X,2)&int(Z,2))|(int(Y,2)&int(Z,2)))
    return result
def GG(X,Y,Z,j):
    if j<16:
        result=BIN(int(X,2)^int(Y,2)^int(Z,2))
    if j>15:
        result=BIN((int(X,2)&int(Y,2))|(~(int(X,2))&int(Z,2)))
    return result
def T(j):
    if j<16:
        result = "01111001110011000100010100011001"           #79cc4519
    if j>15:
        result = "01111010100001111001110110001010"           #7a879d8a
    return result
def T_new(j):
    if j<16:
        return shift("01111001110011000100010100011001",j%32)
    if j>15:
        return shift("01111010100001111001110110001010",j%32)
def HEX(text):
    if len(text)<10:
        text = '0x'+'0'*(10-len(text))+text[2:]
    return text
def CF(V,P,i):
    A1,B1,C1,D1,E1,F1,G1,H1 = V[i]
    A=BIN(A1)
    B=BIN(B1)
    C = BIN(C1)
    D = BIN(D1)
    E = BIN(E1)
    F = BIN(F1)
    G = BIN(G1)
    H = BIN(H1)
    A1,B1,C1,D1,E1,F1,G1,H1 = A,B,C,D,E,F,G,H
    for j in range(64):
        if j<12:
            W.append(P[(j+4)*32:(j+5)*32])
        else:
            W.append(xor(P1(xor( W[j-12],W[j-5],(shift(W[j+1],15)))),shift(W[j-9],7),W[j-2] ))
        W1.append(BIN(int(W[j],2)^int(W[j+4],2)))
        SS1=shift(BIN((int(shift(A,12),2)+int(E,2)+int(T_new_array[j],2))%(2**32)),7)
        SS2=BIN(int(SS1,2)^int(shift(A,12),2))
        TT1=BIN((int(FF(A,B,C,j),2)+int(D,2)+int(SS2,2)+int(W1[j],2))%(2**32))
        TT2=BIN((int(GG(E,F,G,j),2)+int(H,2)+int(SS1,2)+int(W[j],2))%(2**32))
        D=C
        C=shift(B,9)
        B=A
        A=TT1
        H=G
        G=shift(F,19)
        F=E
        E=P0(TT2)
    #print("result:",A,B,C,D,E,F,G,H)
    #print(len(A+B+C+D+E+F+G+H))
    # end = int((A+B+C+D+E+F+G+H),2)^int((A1+B1+C1+D1+E1+F1+G1+H1),2)
    end=[[],[],[],[],[],[],[],[]]
    end[0].append(BIN(int(A,2)^int(A1,2)))
    end[1].append(BIN(int(B, 2) ^ int(B1, 2)))
    end[2].append(BIN(int(C, 2) ^ int(C1, 2)))
    end[3].append(BIN(int(D, 2) ^ int(D1, 2)))
    end[4].append(BIN(int(E, 2) ^ int(E1, 2)))
    end[5].append(BIN(int(F, 2) ^ int(F1, 2)))
    end[6].append(BIN(int(G, 2) ^ int(G1, 2)))
    end[7].append(BIN(int(H, 2) ^ int(H1, 2)))
    end_end = []
    for k in range(8):
        end_end.append(int(end[k][0],2))
    V.append(end_end)
    return end_end
start_time = time.time()
T_new_array = []
for i in range(64):
    T_new_array.append(T_new(i))
plain_text = b'abc'   #明文

result=convert(plain_text)
end_result=[]
print("convert:",result)   #数据填充之后
i = len(result)//512
print("num:",i)            #分组数量
result_divide=[]
for j in range(i):
    result_divide.append(result[512*j:512*(j+1)])
for j in range(i):
    W, W1 = expand(result_divide[j])
    CF(V,result_divide[j],j)
    if j == i-1:
        for k in range(8):
            end_result.append(HEX(hex(V[j+1][k])))
        print("result:",end_result)
end_time = time.time()
print("time:",end_time-start_time,"s")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/