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
    print("loading day ",day)
    
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
    
    bereken(verbruik)
    
def bereken(verbruik):
    verbruik = np.multiply(verbruik, 1000) # from kWh to Wh    
    
    dt = 1/4 # 15 minutes
    t = np.arange(0, 24, dt)
    
    dag_abs = 1
    for jaar in range(1):
        plt.figure()
        for maand in range(1,13):
            print("\nmaand "+str(maand))
            
            for dag in range(1,models.dagenInMaand(maand)):
                dag_abs = dag_abs+1
                
            dagverbruik = models.dailyConsumption(maand, verbruik[maand-1])
            dagverbruik = dagverbruik.getVerbruik()
            dagproductie = data_getDay(dag_abs)
            plt.subplot(3,4,maand)
            plt.plot(t, dagverbruik)
            plt.plot(t, dagproductie)
            plot_settings(maand)

            
    plt.show()
    return

def plot_settings(maand):
    top=0.965,
    bottom=0.06,
    left=0.04,
    right=0.995,
    hspace=0.31,
    wspace=0.285
    
    plt.xlim(0,24)
    plt.ylim(0,6500)
    
    #plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    plt.tight_layout()
    
    plt.xlabel("tijd [uren]")
    plt.ylabel("vermogen [W]")
    plt.title("laatste dag van "+models.int2Maand(maand))
    plt.legend(["verbruik", "productie"])

verbruik = [273.7, 773.92, 1122.69, 1599.74, 1887.6, 1730.16, 1740.88, 1504.93, 1131.7, 788.5, 402.4, 220.08]
verbruik = np.ones(12)*356.07
bereken(verbruik)