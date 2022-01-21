#Importando bibliotecas
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Explicando variáveis:
#cont=contador   maior=maior ponto do salto (eixo z)   menor=menor ponto do salto (eixo z)
#lmaior=localização do maior ponto do salto no arquivo   lmenor=localização do menor ponto do salto no arquivo
#DV= deslocamento vertical(Z)   DH=deslocamento horizontal(H)    DAP=deslocamento antero-posterior(Y)
#VM=velociade média   VP=velocidade pico   VMM=velocidade média momentânea
#DVM deslocamento vertical momentâneo   DH=deslocamento horizontal momentâneo   DAPM=deslocamento antero-posterior momentâneo
#Li=linha inicial (utilizado para aachar velocidade pico)   dat= base de dados a ser processada
#datm1= base de dados convertida para numpy    datm= selecionando colunas que serão utilizadas e convertendo para metros 
#datmf= data filtrada e pronta para o processamento  t= váriavel criada para ser o tempo do eixo x na vicon
#dp e dp1= dados da plataforma  #dpE= dados da plataforma esquerda  #dpD= dados da plataforma direita
#dpEf e dpDf= dados das plataformas filtrados  Vmenor= velocidade no menor ponto do eixo z  Vucsv= velocidade no ultimo ponto de contato do pé com o solo
#t1=  váriavel criada para ser o tempo do eixo x na plataforma de força
#massa= masssa do sujeito  Peso= peso do sujeito   dpEfn= dados da plataforma esquerda filtrados

#Zerando variáveis
cont=maior=menor=lmaior=lmenor=DV=DH=DT=DAP=VM=VP=VMM=DVM=DHM=DAPM=Li=Vmenor=Vucsv=FPT=0

def filtro(dat, fc=59, fs=1000, filtorder=4, typefilt='low'):
    import numpy as np
    from scipy import signal
    
    nl, nc = dat.shape
    # fc=59  # Cut-off frequency of the filter
    w = fc/(fs/2)  # Normalize the frequency
    b, a = signal.butter(filtorder, w, typefilt)
    
    datf = np.zeros([nl, nc], dtype=float)
    for i in range(nc):
        datf[:,i] = signal.filtfilt(b, a, dat[:,i])
   
    return datf

#lendo arquivo vicon
dat = pd.read_csv('trial (10).csv', sep=',', header=None, skiprows=5) 
datm1 = dat.to_numpy()         #convertendo para numpy
datm = datm1[:,2:5] / 1000     #convertendo para metros

#filtrando dados
datmf = filtro(datm, fc=10, fs=400, filtorder=4, typefilt='low')  #frequencia de corte de 10, ordem 4 e frequencia de aquisição 400

#plotando gráfico 3d
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(datm[:,0], datm[:,1], datm[:,2], marker='o', color='red')
ax.plot3D(datmf[:,0], datmf[:,1], datmf[:,2])
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

#plotando cada um dos eixos com o valor filtrado e não filtrado
t = np.linspace(0,len(datmf[:,2])*(1/400),len(datmf[:,2]), False)
fig1, f1_axes = plt.subplots(ncols=2, nrows=2)
f1_axes[0,0].plot(t,datm[:,0])
f1_axes[0,0].plot(t,datmf[:,0])
f1_axes[0,1].plot(t,datm[:,1])
f1_axes[0,1].plot(t,datmf[:,1])
f1_axes[1,0].plot(t,datm[:,2])
f1_axes[1,0].plot(t,datmf[:,2])

#lendo e filtrando dados da plataforma
#Plataforma 1 é a do salto a esquerda e a 2 é a do salto a direita
#lendo arquivo com coordenadas que serão usadas
dp = pd.read_csv("ptrial (10).csv",sep= ',', skiprows=5)
dp1 = dp.to_numpy()
dpE = dp1[:,2:6]
dpD = dp1[:,11:15]

#filtrando os dados da plataforma de força
dpEf = filtro(dpE, fc=100, fs=2000, filtorder=4, typefilt='low') 
dpDf = filtro(dpD, fc=100, fs=2000, filtorder=4, typefilt='low') 

#determinando eixo x para plotar os gráficos
t1 = np.linspace(0,len(dpEf[:,0])*(1/2000),len(dpEf[:,0]), False)

#plotando dados plataforma 1 (salto à esquerda)
fig1, f1_axes = plt.subplots(ncols=2, nrows=2)
f1_axes[0,0].plot(t1, dpE[:,0])
f1_axes[0,0].plot(t1, dpEf[:,0])
f1_axes[0,1].plot(t1, dpE[:,1])
f1_axes[0,1].plot(t1, dpEf[:,1])
f1_axes[1,0].plot(t1, dpE[:,2])
f1_axes[1,0].plot(t1, dpEf[:,2])

#plotando dados plataforma 2 (salto à direita)
fig2, f2_axes = plt.subplots(ncols=2, nrows=2)
f2_axes[0,0].plot(t1, dpD[:,0])
f2_axes[0,0].plot(t1, dpDf[:,0])
f2_axes[0,1].plot(t1, dpD[:,1])
f2_axes[0,1].plot(t1, dpDf[:,1])
f2_axes[1,0].plot(t1, dpD[:,2])
f2_axes[1,0].plot(t1, dpDf[:,2])

#processamento dos dados da vicon
#Encontrando maior e menor valor no eixo Z (ponto mais baixo e mais alto do salto)
menor= datmf[:,2].min()                         #Menor valor de Z
lmenor= datmf[:,2].argmin()                     #localização do menor eixo z dentro do arquivo
maior= datmf[lmenor:,2].max()                   #Maior valor de Z
lmaior= datmf[lmenor:,2].argmax() + lmenor      #localização do maior eixo z dentro do arquivo
        
#Calculando os deslocamentos em cada eixo
DV=float(maior)-float(menor)                              #vertical
DH=float(datmf[lmenor,0])-float(datmf[lmaior,0])          #horizontal
DAP=float(datmf[lmaior,1])-float(datmf[lmenor,1])         #antero-posterior

#Calculando deslocamento tridimensional
DT=(float(DH**2)+float(DV**2)+float(DAP**2))**0.5         #Raiza da soma dos quadrados de cada deslocamento

#Calculando velocidade média do salto
VM=(float(DT))/((lmaior-lmenor)*0.0025)      #0.0025 representa o valor de segundos para cada quadro a 400HZ                
                
#Calculando aceleração (será preciso achar o útimo momento de contato com o solo)
lmaiorp= dpEf[:,2].argmax()              #maior ponto do eixo Z 
ucs=lmaiorp-1+dpE[lmaiorp:,2].argmin()  #ultimo ponto de contato com o solo
ucsv=dp1[ucs,0]-dp1[0,0]                #loc do ultimo ponto de contato com o solo na vicon                                  

#Calculando Velocidade Pico
cont=0 
li=lmenor                                                #atribui o valor de lmenor ao linicial                                                 
while (cont <= (lmaior-lmenor-1)):
    cont += 1
    DVM=float(datmf[lmenor+cont,2])-float(datmf[li,2])  #Deslocamento vertical do momento
    DHM=float(datmf[lmenor+cont,0])-float(datmf[li,0])  #Deslocamento horizontal do momento
    DAPM=float(datmf[lmenor+cont,1])-float(datmf[li,1]) #Deslocamento antero-posterior do momento
    DTM=(float(DHM**2)+float(DVM**2)+float(DAPM**2))**0.5      #Deslocamento tridimensional do momento
    VMM=(DTM)/0.0025                                           #Velocidade momentânea
    li +=1
    if (float(VMM)>float(VP)):
        VP=VMM                  #Valor da velocidade pico
    if (cont == 1):
        Vmenor=VMM              #valor da velocidade no menor ponto do eixo z
    if ((cont+lmenor) == ucsv):
        Vucsv=VMM               #valor da velocidade no ultimo contato com o solo
        Lvucsv=cont             # localização da Vucsv, para calculo da aceleração

#Calculando aceleração 
a=(Vucsv-Vmenor)/(Lvucsv*0.0025)

#calculando força peso
massa= 73.4
peso= massa*9.8
dpEfn= dpEf/peso               #valores do salto normalizados pelo peso

#Calculando força pico do salto a esquerda
FPH= abs(dpEfn[:,0].min())
FPAP= abs(dpEfn[:,1].max())
FPV= abs(dpEfn[:,2].max())

#Calculando força pico tridimensional
cont=0
t2= len(dpEfn[:,0])-2  #valor final para o contador                                                 
while (cont <= t2):
    cont += 1
    FTM=(float(dpEfn[cont,0]**2)+float(dpEfn[cont,1]**2)+float(dpEfn[cont,2]**2))**0.5  #Força tridimensional do momento
    dpEfn[cont,3]=FTM
    if (float(FTM)>float(FPT)):
        FPT= FTM                  #Valor da força pico tridimensional

#Calculando impulso            #Está sendo feito pela área do gráfico de Força(N)xTempo(s)
IV= abs(np.trapz(dpEfn[:,2], t1))    #impulso vertical
IH= abs(np.trapz(dpEfn[:,0], t1))     #impulso horizontal
IAP= abs(np.trapz(dpEfn[:,1], t1))    #impulso antero-posterior
IT= abs(np.trapz(dpEfn[:,3], t1))    #impulso tridimensional

#Resultados apresentados
print ('o deslocamento Vertical é:',DV,'m')
print ('o deslocamento Horizontal é:',DH,'m')
print ('o deslocamento Antero-posterior é:',DAP,'m')
print ('o deslocamento Tridimensional é:',DT,'m')
print ('A velocidade média do salto foi de:', VM,'m/s')
print ('A velocidade pico do salto foi de:', VP,'m/s' )
print ('A aceleração é de:', a,'m/s²')
print('A força pico vertical normalizada é:', FPV,'N')
print('A força pico horizontal normalizada é:', FPH,'N')
print('A força pico antero-posterior normalizada é:', FPAP,'N')
print('A força pico tridimensional normalizada é:', FPT,'N')
print('O impulso vertical normalizado é:', IV,'N/s')
print('O impulso horizontal normalizado é:', IH,'N/s')
print('O impulso antero-posterior normalizado é:', IAP,'N/s')
print('O impulso tridimensional normalizado é:', IT,'N/s')

#escrevendo arquivos no excel
Colunas = ['Deslocamento Vertical','Deslocamento Horizontal','Deslocamento Antero-Posterior','Deslocamento Tridimensional', 'velocidade média do salto',
          'velocidade pico do salto', 'aceleração', 'força pico vertical normalizada', 'força pico horizontal normalizada', 'força pico antero-posterior normalizada',
          'força pico tridimensional normalizada', 'impulso vertical normalizado', 'impulso horizontal normalizado', 'impulso antero-posterior normalizado', 'impulso tridimensional normalizado']
Linhas = ['1','2','3','4','5', 'média', 'desvio-padrão']
rne = pd.DataFrame(index=Linhas, columns=Colunas)
rne.iloc[0,0] = DV
rne.iloc[0,1] = DH
rne.iloc[0,2] = DAP
rne.iloc[0,3] = DT
rne.iloc[0,4] = VM
rne.iloc[0,5] = VP
rne.iloc[0,6] = a
rne.iloc[0,7] = FPV
rne.iloc[0,8] = FPH
rne.iloc[0,9] = FPAP
rne.iloc[0,10] = FPT
rne.iloc[0,11] = IV
rne.iloc[0,12] = IH
rne.iloc[0,13] = IAP
rne.iloc[0,14] = IT