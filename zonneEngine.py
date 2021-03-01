#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:09:29 2020

@author: djoghurt
"""
import matplotlib.pyplot as plt
import numpy as np
import models

def str2Float(string):
    try:
        return float(string)
    except:
        print("Error, ",string," is not a float")
        return 0
    
def strArray2FloatArray(stringArray):
    floatArray = []
    for element in stringArray:
        floatArray.append(str2Float(element)) 
    return floatArray

def data_getDay(day):
    import csv
    #print("loading day ",day)
    
    path = "data/2019/"
    filename = "dag_"+str(day)+".csv"
    
    data = []
    
    with open(path+filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row[1])
            
    data = data[1:len(data)]
    data = strArray2FloatArray(data)
    return data

def bereken_uit_UI(ui):
    print("ik bereken met:")
    print(ui.lineEdit_verbruikJan.text())
    
    paneelRichting = ui.comboBox_orientatie.currentText()
    if paneelRichting == "Zuid":
        orientatieRendement = 1
    elif paneelRichting == "Noord":
        orientatieRendement = 0.5
    elif paneelRichting == "Oost":
        orientatieRendement = 0.8
    elif paneelRichting == "West":
        orientatieRendement = 0.8
    elif paneelRichting == "Vlak":
        orientatieRendement = 0.9
    
    totRendement = str2Float(ui.lineEdit_omvormerRendement.text())/100 * orientatieRendement
    
    verbruik = [ui.lineEdit_verbruikJan.text(),
                ui.lineEdit_verbruikFeb.text(),
                ui.lineEdit_verbruikMaart.text(),
                ui.lineEdit_verbruikApr.text(),
                ui.lineEdit_verbruikMei.text(),
                ui.lineEdit_verbruikJun.text(),
                ui.lineEdit_verbruikJul.text(),
                ui.lineEdit_verbruikAug.text(),
                ui.lineEdit_verbruikSep.text(),
                ui.lineEdit_verbruikOkt.text(),
                ui.lineEdit_verbruikNov.text(),
                ui.lineEdit_verbruikDec.text(),
        ]
    verbruik = strArray2FloatArray(verbruik)

    verbruikDag = [ ui.lineEdit_verbruikDagJan.text(),
                    ui.lineEdit_verbruikDagFeb.text(),
                    ui.lineEdit_verbruikDagMaart.text(),
                    ui.lineEdit_verbruikDagApr.text(),
                    ui.lineEdit_verbruikDagMei.text(),
                    ui.lineEdit_verbruikDagJun.text(),
                    ui.lineEdit_verbruikDagJul.text(),
                    ui.lineEdit_verbruikDagAug.text(),
                    ui.lineEdit_verbruikDagSep.text(),
                    ui.lineEdit_verbruikDagOkt.text(),
                    ui.lineEdit_verbruikDagNov.text(),
                    ui.lineEdit_verbruikDagDec.text(),
        ] 
    deelVerbruikDag = strArray2FloatArray(verbruikDag)
        
    
    opbrengsten = [ui.lineEdit_opbrengstJan.text(),
                   ui.lineEdit_opbrengstFeb.text(),
                   ui.lineEdit_opbrengstMaart.text(),
                   ui.lineEdit_opbrengstApr.text(),
                   ui.lineEdit_opbrengstMei.text(),
                   ui.lineEdit_opbrengstJun.text(),
                   ui.lineEdit_opbrengstJul.text(),
                   ui.lineEdit_opbrengstAug.text(),
                   ui.lineEdit_opbrengstSep.text(),
                   ui.lineEdit_opbrengstOkt.text(),
                   ui.lineEdit_opbrengstNov.text(),
                   ui.lineEdit_opbrengstDec.text(),
    ]
    opbrengsten = strArray2FloatArray(opbrengsten)
    
    startdatum = ui.lineEdit_startdatum.text()
    einddatum = ui.lineEdit_einddatum.text()
    batterijCap = float(ui.lineEdit_batterijCap.text())
    
    
    plots = (ui.checkBox_verbruikVSproductie_1.isChecked(),
             ui.checkBox_verbruikVSproductie_2.isChecked(),
             ui.comboBox_verbruikVSproductie_2.currentText(),
             ui.checkBox_verbruikVSproductie_3.isChecked(),
             ui.checkBox_aankoopVSteruglevering_1.isChecked(),
             ui.checkBox_aankoopVSteruglevering_2.isChecked(),
             ui.comboBox_aankoopVSteruglevering_2.currentText(),
             ui.checkBox_aankoopVSteruglevering_3.isChecked(),
             ui.checkBox_batterij_lvl_mean.isChecked(),
             ui.checkBox_batterij_lvl_exact.isChecked()
             )
    
    totaal_aangekocht, totaal_teruggeleverd = bereken(verbruik, batterijCap, plots)
    geld_aangekocht = round(totaal_aangekocht*float(ui.lineEdit_ePrijsHeen.text()),2)
    geld_teruggeleverd = round(totaal_teruggeleverd*float(ui.lineEdit_ePrijsTerug.text()),2)
    result = round(totaal_aangekocht-totaal_teruggeleverd,2)
    geld_result = round(geld_aangekocht-geld_teruggeleverd,2)
    
    ui.label_result1.setText("totaal aangekocht: "+str(totaal_aangekocht)+" kWh")
    ui.label_result2.setText("totaal teruggeleverd: "+str(totaal_teruggeleverd)+" kWh")    
    ui.label_result3.setText("totaal: "+str(result)+" kWh")
    ui.label_result1b.setText("€ "+str(geld_aangekocht))
    ui.label_result2b.setText("€ "+str(geld_teruggeleverd))
    ui.label_result3b.setText("€ "+str(geld_result))
    if geld_result >= 0:
        ui.label_result3c.setText("(u moet betalen)")
    else:
        ui.label_result3c.setText("(u krijgt geld)")
    
def bereken(verbruik_m, batterijCap, plots):
    plt.close('all')
    dt = 1/4 # 15 minutes
    tijd = np.arange(0, 24, dt)
    
    batterijCap = batterijCap*1000 # maximale cappaciteit van de batterij [Wh], tesla heeft 6.4 en 13.5 kWh
    batterijCap = batterijCap/dt # cappaciteit in Wkwartier
    batterij = 0 # start met lege batterij 
    
    verbruik = np.zeros((365, len(tijd)))
    productie = np.zeros((365, len(tijd)))
    teruglever = np.zeros((365, len(tijd)))
    aankoop = np.zeros((365, len(tijd)))
    batterij_t = np.zeros((365, len(tijd)))
    
    verbruik_m = np.multiply(verbruik_m, 1000) # from kWh to Wh    
    
    dag_abs = 1
    for jaar in range(1):
        for maand in range(1,13):
            #print("\nmaand "+str(maand))
            
            for dag in range(1,models.dagenInMaand(maand)+1):
                #print(dag)
                dagverbruik = models.dailyConsumption(maand, verbruik_m[maand-1])
                dagverbruik = dagverbruik.getVerbruik()
                dagproductie = data_getDay(dag_abs)                
                restant = dagproductie-dagverbruik
                
                verbruik[dag_abs-1,:] = dagverbruik
                productie[dag_abs-1,:] = dagproductie
                
                # verwerk met batterij
                for t, _ in enumerate(tijd):                    
                    batterij = batterij + restant[t]
                    if batterij<0: # batterij is leeg
                        aankoop[dag_abs-1, t] = abs(batterij)
                        batterij = 0
                    elif batterij>batterijCap: # batterij is vol
                        teruglever[dag_abs-1, t] = batterij-batterijCap
                        batterij = batterijCap    
                    batterij_t[dag_abs-1,t] = batterij
                    
                dag_abs = dag_abs+1 # nieuwe dag hierna
                
            if(plots[0]):
                #print("plotting dag", dag_abs-2)
                plt.figure(num=1)
                plt.subplot(3,4,maand)
                plt.plot(tijd, dagverbruik)
                plt.plot(tijd, dagproductie)
                plot_settings(maand, batterijCap*dt)
                plt.legend(["verbruik", "productie"], loc='upper left')
            
            if(plots[4]):
                plt.figure(num=4)
                plt.subplot(3,4,maand)
                plt.plot(tijd, aankoop[dag_abs-2,:])
                plt.plot(tijd, teruglever[dag_abs-2,:])
                plt.plot(tijd, batterij_t[dag_abs-2,:]*dt)
                plot_settings(maand, batterijCap*dt)
                plt.legend(["aankoop", "teruggeleverd", "batterij"], loc='upper left')
    
    if(plots[0]): # figure 1
        plt.figure(num=1)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()    
        
    if(plots[1]): # figure 2
        plt.figure(num=2)
        plot_maand(plots[2], tijd, verbruik, productie, batterij_t*dt, batterijCap, ["aankoop", "teruggeleverd", "batterij"])        
        
    if(plots[3]): # figure 3
        plt.figure(num=3)
        dagen = np.arange(1,366)
        verbruik_d = np.sum(verbruik,1)
        plt.plot(dagen, verbruik_d)
        plt.title("verbruik elektricitieit")
        plt.xlabel("tijd [dagen]")
        plt.ylabel("Watt")
        plt.ylim(0,max(verbruik_d)*1.1)
        
    if(plots[4]): # figure 4
        plt.figure(num=4)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()   
        
    if(plots[5]): # figure 5
        plt.figure(num=5)
        plot_maand(plots[6], tijd, aankoop, teruglever, batterij_t*dt, batterijCap, ["aankoop", "teruggeleverd", "batterij"])
        
    if(plots[7]): # figure 6
        plt.figure(num=6)
        dagen = np.arange(1,366)
        aankoop_d = np.sum(aankoop,1)
        plt.plot(dagen, aankoop_d)
        plt.title("aankoop elektricitieit")
        plt.xlabel("tijd [dagen]")
        plt.ylabel("Watt")
        
    if(plots[8]): # figure 7
        plt.figure(7)
        dagen = np.arange(1,366)
        batterij_d = np.mean(batterij_t,1)*dt
        plt.plot(dagen, batterij_d)
        plt.plot(dagen, np.ones(len(dagen))*batterijCap*dt)
        plt.title("batterij level (gemiddelde over dag)")
        plt.xlabel("tijd [dagen]")
        plt.ylabel("cappaciteit [kWh]")
    
    if(plots[9]): # figure 8
        plt.figure(8)
        dagen = np.arange(1,366,1/24/4)
        batterij_td = np.reshape(batterij_t, -1, order='C')*dt
        plt.plot(dagen, batterij_td)
        plt.plot(dagen, np.ones(len(dagen))*batterijCap*dt)
        plt.title("batterij level (exact)")
        plt.xlabel("tijd [dagen]")
        plt.ylabel("cappaciteit [kWh]")
                           
    #plt.close('all')
    
    plt.show()
    
    totaal_aangekocht = round(np.sum(np.sum(aankoop*dt))/1000,2)
    totaal_teruggeleverd = round(np.sum(np.sum(teruglever*dt))/1000,2)
    
    print("totaal aangekocht = ",totaal_aangekocht, "kWh")
    print("totaal teruggeleverd = ", totaal_teruggeleverd, "kWh")
    
    return totaal_aangekocht, totaal_teruggeleverd

def plot_maand(maand, tijd, y, y2, batterij_t, batterijCap, legend):
    
    if isinstance(maand, str):
        maand = models.maand2Int(maand)
    
    if maand == 1:
        startdag = 1
    else:
        startdag = 0
        for m in range(1,maand):
            startdag = startdag+models.dagenInMaand(m) 
    
    laatstedag = startdag + models.dagenInMaand(maand)    
    y = y[startdag:laatstedag,:]
    y2 = y2[startdag:laatstedag,:]
    batterij_t = batterij_t[startdag:laatstedag,:]
    
    for dag in range(0,y.shape[0]):
        plt.subplot(8,4,dag+1)
        plt.plot(tijd, y[dag,:])
        plt.plot(tijd, y2[dag,:])
        plt.plot(tijd, batterij_t[dag,:])
        plt.legend(legend, loc='upper left', fontsize='xx-small')
        batterijText = ", batterij "+str(batterijCap/1000)+"kWh"
        plt.title(str(dag+1)+" "+models.int2Maand(maand)+batterijText, fontsize='xx-small')
        #plt.text(23, 6000, "batterij "+str(batterijCap/1000)+"kWh", verticalalignment='bottom', horizontalalignment='right')
    

def plot_settings(maand, batterijCap):
    plt.xlim(0,24)
    plt.ylim(0,6500)   
    plt.xlabel("tijd [uren]")
    plt.ylabel("vermogen [W]")
    plt.title("laatste dag van "+models.int2Maand(maand))
    plt.text(23, 6000, "batterij "+str(batterijCap/1000)+"kWh", verticalalignment='bottom', horizontalalignment='right')

# verbruik = [273.7, 773.92, 1122.69, 1599.74, 1887.6, 1730.16, 1740.88, 1504.93, 1131.7, 788.5, 402.4, 220.08]
# verbruik = np.ones(12)*356.07
# aankoop, teruglever, batterij_t = bereken(verbruik)