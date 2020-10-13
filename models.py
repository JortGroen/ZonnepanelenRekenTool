#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:40:17 2020

@author: djoghurt
"""

import numpy as np

dt = 1/4
t = np.arange(0, 24, dt)

def dagenInMaand(maand):
    lookupTable = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return lookupTable[maand-1]

def int2Maand(maand):
    lookupTable = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]
    return lookupTable[maand-1]

def daglichtRange(maand):
    zonsopgang = [8.75, 8, 7, 6.75, 5.75, 5.33, 5.66, 6.33, 7.25, 8.1, 8, 8.75]
    zonsondergang = [17, 17.8, 18.75, 20.66, 21.5, 22, 22, 21, 20, 18.75, 16.75, 16.5]
    #print("daglicht van ", zonsopgang[maand-1], " tot ", zonsondergang[maand-1])
    return (zonsondergang[maand-1] - zonsopgang[maand-1]), (zonsondergang[maand-1]+zonsopgang[maand-1])/2

def kansOpWolkjes(maand):
    kansen = [0.83, 0.83, 0.7, 0.6, 0.4, 0.3, 0.2, 0.3, 0.5, 0.7, 0.8, 0.83]
    return kansen[maand-1]

def verdeelOverMaand(maand, maandverbruik):
    inhomogeniteit = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    scale = inhomogeniteit[maand-1]
    maandverbruikPerDag = np.random.normal(loc=100, scale=scale, size=dagenInMaand(maand))
    maandverbruikPerDag = maandverbruikPerDag/np.sum(maandverbruikPerDag)
    maandverbruikPerDag = maandverbruikPerDag*maandverbruik
    print("maandverbruik totaal = "+str(maandverbruik), " check: ", str(round(np.sum(maandverbruikPerDag),2)))
    return maandverbruikPerDag

def plot(x,y, maand, dag):
    import matplotlib.pyplot as plt

    plt.xlim(1,24)
    plt.ylim(0,np.max(y)*1.1)
    plt.xlabel("tijd [uren]")
    plt.ylabel("vermogen [kW]")
    plt.title(str("maand "+str(maand)+", dag "+str(dag)))
    
    plt.plot(x,y)
    plt.show()
    
class dailyConsumption():
   
    def __init__(self, maand, maandverbruik):
        dagverbruik = maandverbruik/dagenInMaand(maand)  
        
        piek = 3000
        peak1 = self.getPeak(t, 7.5, 2/3*piek, 1) # ochtend piek om half 8
        peak2 = self.getPeak(t, 12, 2/3*piek, 1) # middag piek om 12 uur
        peak3 = self.getPeak(t, 16, 1/3*piek, 3/4) # middag piek om 16 uur
        peak4 = self.getPeak(t, 18, 9/10*piek, 1.5) # avond piek om 6 uur
        peak5 = self.getPeak(t, 18.75, 2/3*piek, 1.5)
        
        y = peak1 + peak2 + peak3 + peak4 + peak5
        
        backgroundNoise = np.random.rand(len(t))*100
        y = y + backgroundNoise
        
        y_int = np.sum(y*dt)
        baseline = np.ones(len(t))*(dagverbruik-y_int)/len(t)/dt
        print("baseline: ", (dagverbruik-y_int)/len(t)/dt)
        
        y = y + baseline

        self.verbruik = y
        self.maand = maand
        
        
    def getPeak(self, t, tijdstip, peak, tijdsduur):
        std = tijdsduur/4
        y = peak*np.exp( -0.5/(std*std)*(np.power((t-tijdstip),2)) )
        return y
    
    def getVerbruik(self):
        return self.verbruik
       
    def plot(self, dag):
        plot(t, self.verbruik, self.maand, dag)
        return

class dailyProduction():
    
    def __init__(self, maand, maandproductie):
        self.maand = maand
        
        dagproductie = maandproductie/dagenInMaand(maand)  
        dagRange, tijdstip = daglichtRange(maand)
        std = dagRange/6
        y = dagproductie/(std*np.sqrt(2*3.1415)) * np.exp( -0.5/(std*std)*(np.power((t-tijdstip),2)) )
        
        kansOpWolkje = kansOpWolkjes(maand)
        wolkjesDichtheid = 3
        #wolkjes = np.random.random_sample(len(t)) < kansOpWolkje
        
        wolkjes = np.random.random_sample(len(t))
        wolkjes = wolkjes * np.ones(len(t))*(wolkjes<kansOpWolkje)
        wolkjes = np.ones(len(t))-wolkjes*wolkjesDichtheid
        wolkjes[wolkjes<0] = 0
               
        y = y*wolkjes
        #y = y*~wolkjes
        
        # now lets compensate for the wolkjes such that we still have total output as predicted
        stepSize = 0.5
        i = 0
        multiplier = 1
        direction = True # we moeten eerst altijd omhoog
        y_old = y
        y_inter = np.sum(y*dt)
        while abs(dagproductie - y_inter) > 0.01:
            if dagproductie - y_inter > 0:    # we need more production
                if direction == False:
                    stepSize = stepSize/10
                    #print("switch omhoog")
                direction = True
                multiplier = multiplier+stepSize
                y = y_old*multiplier
            else:                               # we need less production
                if direction == True:
                    stepSize = stepSize/10
                    #print("switch naar beneden")
                direction = False
                multiplier = multiplier-stepSize
                y = y_old*multiplier
            y_inter = np.sum(y*dt)
            i = i+1
            if i>100:
                print("error, we kunnen de input niet goed krijgen")
                break
            #print("iteration "+str(i))
        #print(str(i)+" iterations")
        self.productie = y        
        
    def plot(self, dag):
        plot(t, self.productie, self.maand, dag)
        return

        
def test_dagproductie(maand, maandproductie):
    dagproductie = dailyProduction(maand,maandproductie)
    dagproductie.plot(1)
    print("totaal dagproductie: ", round(np.sum(dagproductie.productie*dt),2), " check: ", round(maandproductie/dagenInMaand(maand),2))
    return
    
def test_maandproductie():
    import matplotlib.pyplot as plt
    
    maandproductie = 3.38
    maand = 1
    
    #plt.figure()
    for dag in range(1,9,1):
        dagproductie = dailyProduction(maand, maandproductie)
        plt.subplot(2,4,dag)
        dagproductie.plot(dag)
    return
    
def test_dagverbruik(maand, maandverbruik):    
    dagverbruik = dailyConsumption(1,maandverbruik)
    dagverbruik.plot(1)
    print("totaal dagverbruik: ", round(np.sum(dagverbruik.verbruik*dt),2), " check: ", round(maandverbruik/dagenInMaand(maand),2))
    return

#test_dagverbruik()
#test_dagproductie()
#test_maandproductie()