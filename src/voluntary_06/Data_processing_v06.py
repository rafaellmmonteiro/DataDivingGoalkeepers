#Importando bibliotecas
import numpy as np
import pandas as pd
import math
import scipy as sp
import statistics
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

#contador de saltos
conts=contrne=contrae=contrad=contrnd= 0        #zerando contadores
while (conts <18):                                                           #ler os arquivos dos diferentes saltos
    if (conts==0):
        dat = pd.read_csv('trial (1).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (1).csv",sep= ',', skiprows=5)
    if (conts==1):
        dat = pd.read_csv('trial (2).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (2).csv",sep= ',', skiprows=5)
    if (conts==2):
        dat = pd.read_csv('trial (3).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (3).csv",sep= ',', skiprows=5)
    if (conts==3):
        dat = pd.read_csv('trial (4).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (4).csv",sep= ',', skiprows=5)
    if (conts==4):
        dat = pd.read_csv('trial (5).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (5).csv",sep= ',', skiprows=5)
    if (conts==5):
        dat = pd.read_csv('trial (6).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (6).csv",sep= ',', skiprows=5)
    if (conts==6):
        dat = pd.read_csv('trial (7).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (7).csv",sep= ',', skiprows=5)
    if (conts==7):
        dat = pd.read_csv('trial (8).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (8).csv",sep= ',', skiprows=5)
    if (conts==8):
        dat = pd.read_csv('trial (9).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (9).csv",sep= ',', skiprows=5)
    if (conts==9):
        dat = pd.read_csv('trial (10).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (10).csv",sep= ',', skiprows=5)
    if (conts==10):
        dat = pd.read_csv('trial (11).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (11).csv",sep= ',', skiprows=5)
    if (conts==11):
        dat = pd.read_csv('trial (12).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (12).csv",sep= ',', skiprows=5)
    if (conts==12):
        dat = pd.read_csv('trial (13).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (13).csv",sep= ',', skiprows=5)
    if (conts==13):
        dat = pd.read_csv('trial (14).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (14).csv",sep= ',', skiprows=5)
    if (conts==14):
        dat = pd.read_csv('trial (15).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (15).csv",sep= ',', skiprows=5)
    if (conts==15):
        dat = pd.read_csv('trial (17).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (17).csv",sep= ',', skiprows=5)
    if (conts==16):
        dat = pd.read_csv('trial (19).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (19).csv",sep= ',', skiprows=5)
    if (conts==17):
        dat = pd.read_csv('trial (20).csv', sep=',', header=None, skiprows=5)
        dp = pd.read_csv("ptrial (20).csv",sep= ',', skiprows=5)
    conts += 1
    
    #zerando variáveis
    cont=maior=menor=lmaior=lmenor=DV=DH=DT=DAP=VM=VP=VMM=DVM=DHM=DAPM=Li=Vmenor=Vucsv=FPT=Lvucsv=a=LFPV=LMVAP=LFPV=LMVAPR=RdpDfn=RdpD=RdpEfn=RdpE=0
    
    #lendo arquivo vicon
    datm1 = dat.to_numpy()         #convertendo para numpy
    datm = datm1[:,2:5] / 1000     #convertendo para metros e selecionando eixos x,y,z +1 para calcular escrever o deslocamento tridimensional
    
    #filtrando dados
    datmf = filtro(datm, fc=10, fs=400, filtorder=4, typefilt='low')  #frequencia de corte de 10, ordem 4 e frequencia de aquisição 400
    
    
    #Plataforma 1 é a do salto a esquerda e a 2 é a do salto a direita
    #lendo arquivo com coordenadas que serão usadas
    dp1 = dp.to_numpy()
    dpE = dp1[:,2:6]    #selecionando eixos x,y,z +1 para calcular escrever o deslocamento tridimensional
    dpD = dp1[:,11:15]   #selecionando eixos x,y,z +1 para calcular escrever o deslocamento tridimensional
    
    #filtrando os dados da plataforma de força
    dpEf = filtro(dpE, fc=100, fs=2000, filtorder=4, typefilt='low')  #frequencia de corte estão altas devido ao mokka 2000/400 hz
    dpDf = filtro(dpD, fc=100, fs=2000, filtorder=4, typefilt='low') 
    
    
    #determinando eixo x da plataforma
    t1 = np.linspace(0,len(dpEf[:,0])*(1/400),len(dpEf[:,0]), False)
        
    #processamento dos dados da vicon
    #Encontrando maior e menor valor no eixo Z (ponto mais baixo e mais alto do salto)
    menor= datmf[:,2].min()                         #Menor valor de Z
    lmenor= datmf[:,2].argmin()                     #localização do menor eixo z dentro do arquivo
    maior= datmf[lmenor:,2].max()                   #Maior valor de Z
    lmaior= datmf[lmenor:,2].argmax() + lmenor      #localização do maior eixo z dentro do arquivo
            
    #Calculando os deslocamentos em cada eixo
    DV=abs(float(maior)-float(menor))                              #vertical
    DH=abs(float(datmf[lmaior,0])-float(datmf[lmenor,0]))          #horizontal
    DAP=abs(float(datmf[lmaior,1])-float(datmf[lmenor,1]))         #antero-posterior
    
    #Calculando deslocamento tridimensional
    DT=(float(DH**2)+float(DV**2)+float(DAP**2))**0.5         #Raiza da soma dos quadrados de cada deslocamento
    
    #Calculando velocidade média do salto
    VM=(float(DT))/((lmaior-lmenor)*0.0025)      #0.0025 representa o valor de segundos para cada quadro a 400HZ 
 
    #inicio do cálculo das forças da plataforma para finalizar os da vicon
    #calculando força peso.
    massa=81.5 
    peso= massa*9.8   #utilizando gravidade como 9.8
    dpDfn= dpDf/peso  #salto a esquerda normalizado
    dpEfn= dpEf/peso  #salto a direita normalizado         
    
    if ((datmf[0,0]-datmf[len(datmf[:,0])-1,0]) > 0):   #processamento caso o salto seja a esquerda(ve se o deslocamento do eixo x foi positivo(E) ou  negativo(D))

        #achando o útimo momento de contato com o solo
        lmaiorp= dpEf[:,2].argmax()              #maior ponto do eixo Z 
        ucs=lmaiorp-1+dpE[lmaiorp:,2].argmin()  #ultimo ponto de contato com o solo
        ucsv=dp1[ucs,0]-dp1[0,0]                #loc do ultimo ponto de contato com o solo na vicon  
        
        #Calculando força pico do salto a esquerda 
        FPH= abs(dpEfn[:,1].max())         #devido ao posicionamento da plataforma de força de lado o eixo x é o deslocamento antero-posterior e o y horizontal
        FPAP= abs(dpEfn[:,0].min())        
        FPV= abs(dpEfn[:,2].max())
        
        #calculando força pico tridimensional
        cont=0
        t2= len(dpEfn[:,0])-1  #valor final para o contador                                                 
        while (cont <= t2):
            FTM=(float(dpEfn[cont,0]**2)+float(dpEfn[cont,1]**2)+float(dpEfn[cont,2]**2))**0.5  #Força tridimensional do momento
            dpEfn[cont,3]=FTM            #escrevendo os valores da força tridimensional
            cont += 1
            if (float(FTM)>float(FPT)):
                FPT= FTM                  #Valor da força pico tridimensional
        
        #Calculando impulso            #Está sendo feito pela área do gráfico de Força(N)xTempo(s)
        if (dpD[0,2] > 1):           #identificando regra antiga (tem que ser feito isso pois o sujeito está na plataforma antes do salto e retira um pé para saltar)
            RdpEfn=dpEfn[::-1]         #salto a esquerda espelhado
            LFPV= RdpEfn[:,2].argmax()  #encontrando loc da força pico vertical com ele espelhado
            RdpE=dpE[::-1]              #espelhando o salto a esquerda sem estar filtrado
            LMVAPR= RdpE[LFPV:,2].argmin() #localização do maior valor antes do pico (seria o menor antes do pico, porém o Z é para baixo) 
            LMVAP= len(dpE[:,2])-LMVAPR-LFPV  #valor exato de onde começou o salto (menor valor antes do pico)
            t2 = np.linspace(0,len(dpEf[LMVAP:,0])*(1/400),len(dpEf[LMVAP:,0]), False) #criando o eixo x para calcular o impulso
            IV= abs(np.trapz(dpEfn[LMVAP:,2], t2))    #impulso vertical (integral trapezoidal)
            IH= abs(np.trapz(dpEfn[LMVAP:,1], t2))     #impulso horizontal
            IAP= abs(np.trapz(dpEfn[LMVAP:,0], t2))    #impulso antero-posterior
            IT= abs(np.trapz(dpEfn[LMVAP:,3], t2))    #impulso tridimensional
        else:    
            IV= abs(np.trapz(dpEfn[:,2], t1))    #impulso vertical
            IH= abs(np.trapz(dpEfn[:,1], t1))     #impulso horizontal
            IAP= abs(np.trapz(dpEfn[:,0], t1))    #impulso antero-posterior
            IT= abs(np.trapz(dpEfn[:,3], t1))    #impulso tridimensional
    
        #processamento caso salto seja a direita
    else:
        #achando o útimo momento de contato com o solo
        lmaiorp= dpDf[:,2].argmax()              #maior ponto do eixo Z 
        ucs=lmaiorp-1+dpD[lmaiorp:,2].argmin()  #ultimo ponto de contato com o solo
        ucsv=dp1[ucs,0]-dp1[0,0]                #loc do ultimo ponto de contato com o solo na vicon  
        
        #Calculando força pico do salto a direita
        FPAP= abs(dpDfn[:,0].min())
        FPH= abs(dpDfn[:,1].min())
        FPV= abs(dpDfn[:,2].max())
        
        #calculando força pico tridimensional
        cont=0                         
        t2= len(dpDfn[:,0])-2  #valor final para o contador                                                 
        while (cont <= t2):
            cont += 1
            FTM=(float(dpDfn[cont,0]**2)+float(dpDfn[cont,1]**2)+float(dpDfn[cont,2]**2))**0.5  #Força tridimensional do momento
            dpDfn[cont,3]=FTM
            if (float(FTM)>float(FPT)):
                FPT= FTM                  #Valor da força pico tridimensional
        
        #Calculando impulso            #Está sendo feito pela área do gráfico de Força(N)xTempo(s)
        if (dpD[0,2] > 1):           #identificando regra antiga
            RdpDfn=dpDfn[::-1]
            LFPV= RdpDfn[:,2].argmax()  #encontrando loc da força pico vertical
            RdpD=dpD[::-1]
            LMVAPR= RdpD[LFPV:,2].argmin() #localização do maior valor antes do pico (momento em que ele tira o pé para impulsionar e saltar)
            LMVAP= len(dpD[:,2])-LMVAPR-LFPV
            t2 = np.linspace(0,len(dpDf[LMVAP:,0])*(1/400),len(dpDf[LMVAP:,0]), False) #criando o eixo x para calcular o impulso
            IV= abs(np.trapz(dpDfn[LMVAP:,2], t2))    #impulso vertical
            IH= abs(np.trapz(dpDfn[LMVAP:,1], t2))     #impulso horizontal
            IAP= abs(np.trapz(dpDfn[LMVAP:,0], t2))    #impulso antero-posterior
            IT= abs(np.trapz(dpDfn[LMVAP:,3], t2))    #impulso tridimensional
        else:    
            IV= abs(np.trapz(dpDfn[:,2], t1))    #impulso vertical
            IH= abs(np.trapz(dpDfn[:,1], t1))     #impulso horizontal
            IAP= abs(np.trapz(dpDfn[:,0], t1))    #impulso antero-posterior
            IT= abs(np.trapz(dpDfn[:,3], t1))    #impulso tridimensional
        
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
    a=abs((Vucsv-Vmenor)/(Lvucsv*0.0025))
        
    #Escrevendo arquivos 
    #Regra antiga a esquerda
    if ((datmf[0,0]-datmf[len(datmf[:,0])-1,0]) > 0) and (dpD[0,2] > 1):    #identifica se o seujeito está em cima da plataforma e o deslocamento do eixo x da vicon para saber o lado
        if (contrae==0):
            Colunas = ['Deslocamento Vertical','Deslocamento Horizontal','Deslocamento Antero-Posterior','Deslocamento Tridimensional', 'velocidade média do salto',
                       'velocidade pico do salto', 'aceleração', 'força pico vertical normalizada', 'força pico horizontal normalizada', 'força pico antero-posterior normalizada',
                       'força pico tridimensional normalizada', 'impulso vertical normalizado', 'impulso horizontal normalizado', 'impulso antero-posterior normalizado', 'impulso tridimensional normalizado']
            Linhas = ['rae1','2','3','4','5', 'média', 'desvio-padrão']
            rae = pd.DataFrame(index=Linhas, columns=Colunas)
        rae.iloc[contrae,0] = DV
        rae.iloc[contrae,1] = DH
        rae.iloc[contrae,2] = DAP
        rae.iloc[contrae,3] = DT
        rae.iloc[contrae,4] = VM
        rae.iloc[contrae,5] = VP
        rae.iloc[contrae,6] = a
        rae.iloc[contrae,7] = FPV
        rae.iloc[contrae,8] = FPH
        rae.iloc[contrae,9] = FPAP
        rae.iloc[contrae,10] = FPT
        rae.iloc[contrae,11] = IV
        rae.iloc[contrae,12] = IH
        rae.iloc[contrae,13] = IAP
        rae.iloc[contrae,14] = IT
        contrae += 1
        contm=0           #contador media
        while (contm<15):        
            rae.iloc[5,contm]= np.mean([rae.iloc[0:contrae,contm]])
            rae.iloc[6,contm]= np.std([rae.iloc[0:contrae,contm]])
            contm += 1
    
    #Regra nova a esquerda
    if ((datmf[0,0]-datmf[len(datmf[:,0])-1,0]) > 0) and (dpD[0,2] < 1):   #verifica se o sujeto não está na plataforma e o deslocamento no eixo x da vicon
        if (contrne==0):
            Colunas = ['Deslocamento Vertical','Deslocamento Horizontal','Deslocamento Antero-Posterior','Deslocamento Tridimensional', 'velocidade média do salto',
                       'velocidade pico do salto', 'aceleração', 'força pico vertical normalizada', 'força pico horizontal normalizada', 'força pico antero-posterior normalizada',
                       'força pico tridimensional normalizada', 'impulso vertical normalizado', 'impulso horizontal normalizado', 'impulso antero-posterior normalizado', 'impulso tridimensional normalizado']
            Linhas = ['rne1','2','3','4','5', 'média', 'desvio-padrão']
            rne = pd.DataFrame(index=Linhas, columns=Colunas)
        rne.iloc[contrne,0] = DV
        rne.iloc[contrne,1] = DH
        rne.iloc[contrne,2] = DAP
        rne.iloc[contrne,3] = DT
        rne.iloc[contrne,4] = VM
        rne.iloc[contrne,5] = VP
        rne.iloc[contrne,6] = a
        rne.iloc[contrne,7] = FPV
        rne.iloc[contrne,8] = FPH
        rne.iloc[contrne,9] = FPAP
        rne.iloc[contrne,10] = FPT
        rne.iloc[contrne,11] = IV
        rne.iloc[contrne,12] = IH
        rne.iloc[contrne,13] = IAP
        rne.iloc[contrne,14] = IT
        contrne += 1
        contm=0           #contador media
        while (contm<15):        
            rne.iloc[5,contm]= np.mean([rne.iloc[0:5,contm]]) #calcula méia
            rne.iloc[6,contm]= np.std([rne.iloc[0:5,contm]]) #cálcula desvio padrão
            contm += 1

    #Regra antiga a direita
    if ((datmf[0,0]-datmf[len(datmf[:,0])-1,0]) < 0) and (dpD[0,2] > 1):
        if (contrad==0):
            Colunas = ['Deslocamento Vertical','Deslocamento Horizontal','Deslocamento Antero-Posterior','Deslocamento Tridimensional', 'velocidade média do salto',
                       'velocidade pico do salto', 'aceleração', 'força pico vertical normalizada', 'força pico horizontal normalizada', 'força pico antero-posterior normalizada',
                       'força pico tridimensional normalizada', 'impulso vertical normalizado', 'impulso horizontal normalizado', 'impulso antero-posterior normalizado', 'impulso tridimensional normalizado']
            Linhas = ['rad1','2','3','4','5', 'média', 'desvio-padrão']
            rad = pd.DataFrame(index=Linhas, columns=Colunas)
        rad.iloc[contrad,0] = DV
        rad.iloc[contrad,1] = DH
        rad.iloc[contrad,2] = DAP
        rad.iloc[contrad,3] = DT
        rad.iloc[contrad,4] = VM
        rad.iloc[contrad,5] = VP
        rad.iloc[contrad,6] = a
        rad.iloc[contrad,7] = FPV
        rad.iloc[contrad,8] = FPH
        rad.iloc[contrad,9] = FPAP
        rad.iloc[contrad,10] = FPT
        rad.iloc[contrad,11] = IV
        rad.iloc[contrad,12] = IH
        rad.iloc[contrad,13] = IAP
        rad.iloc[contrad,14] = IT
        contrad += 1
        contm=0           #contador media
        while (contm<15):        
            rad.iloc[5,contm]= np.mean([rad.iloc[0:contrad,contm]])
            rad.iloc[6,contm]= np.std([rad.iloc[0:contrad,contm]])
            contm += 1
        
    #Regra nova a direita
    if ((datmf[0,0]-datmf[len(datmf[:,0])-1,0]) < 0) and (dpD[0,2] < 1):
        if (contrnd==0):
            Colunas = ['Deslocamento Vertical','Deslocamento Horizontal','Deslocamento Antero-Posterior','Deslocamento Tridimensional', 'velocidade média do salto',
                       'velocidade pico do salto', 'aceleração', 'força pico vertical normalizada', 'força pico horizontal normalizada', 'força pico antero-posterior normalizada',
                       'força pico tridimensional normalizada', 'impulso vertical normalizado', 'impulso horizontal normalizado', 'impulso antero-posterior normalizado', 'impulso tridimensional normalizado']
            Linhas = ['rnd1','2','3','4','5', 'média', 'desvio-padrão']
            rnd = pd.DataFrame(index=Linhas, columns=Colunas)
        rnd.iloc[contrnd,0] = DV
        rnd.iloc[contrnd,1] = DH
        rnd.iloc[contrnd,2] = DAP
        rnd.iloc[contrnd,3] = DT
        rnd.iloc[contrnd,4] = VM
        rnd.iloc[contrnd,5] = VP
        rnd.iloc[contrnd,6] = a
        rnd.iloc[contrnd,7] = FPV
        rnd.iloc[contrnd,8] = FPH
        rnd.iloc[contrnd,9] = FPAP
        rnd.iloc[contrnd,10] = FPT
        rnd.iloc[contrnd,11] = IV
        rnd.iloc[contrnd,12] = IH
        rnd.iloc[contrnd,13] = IAP
        rnd.iloc[contrnd,14] = IT
        contrnd += 1
        contm=0           #contador media
        while (contm<15):        
            rnd.iloc[5,contm]= np.mean([rnd.iloc[0:5,contm]])
            rnd.iloc[6,contm]= np.std([rnd.iloc[0:5,contm]])
            contm += 1
saída=pd.concat([rae,rne,rad,rnd])         #juntando todos arquivos em um só        
saída.to_csv("ouput_voluntary_06.csv")                  #criando um arquivo de saída csv
#para finalizar adicioar o rnd no arquivo de saída, não da ainda pq não foi utilizado então não foi criado
#soltar a aceleração quando os saltos permitirem
#usar a leitura de dados do processamento_final
#utilizar a técnica para achar ultimo contato com o solo (ucsv) do processamento_final
#tirar o interpolate()