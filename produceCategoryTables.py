#Creative Commons Zero
#
#Author: Mikkel Baun Kjaergaard, University of Southern Denmark
#

import json
import sys

def printCSVDistribution(jsonobj,dimensionX,dimensionXentries,citeinclude=None):
    
    datamatrix = {}
    citationsmatrix = {}
    
    count = 0
    for xentry in dimensionXentries:
        for obj in jsonobj:
            if xentry.upper() in obj[dimensionX].upper():
                count = count + 1
                if xentry in datamatrix:
                    datamatrix[xentry] = datamatrix[xentry] + 1
                    citationsmatrix[xentry].append(obj["ID"])
                else:
                    datamatrix[xentry] = 1
                    citationsmatrix[xentry] = [obj["ID"]]
                    
                
            
    print str(datamatrix)
    print str(citationsmatrix)
    
    graph = []

    recount = 0
    for entry in datamatrix:
        recount = recount + datamatrix[entry]
        if citeinclude != None:
            finals = []
            for citeentry in citationsmatrix[entry]:
                if (citeentry in citeinclude) and (len(finals) < 3):
                    finals.append(citeentry)
            graph.append((datamatrix[entry] , entry + " (e.g. \cite{" + ",".join(finals) + "})"))
        else:
            graph.append((datamatrix[entry] , entry + " \cite{" + ",".join(citationsmatrix[entry]) + "}"))
    
    print str(count) + " = " + str(recount)
    
    graph = sorted(graph, key=lambda tup: tup[0])
    yticklabels = []
    coordinates = []
    i = 1
    for k,v in graph:
        coordinates.append("(" + str(k) + "," + str(i) + ")")
        yticklabels.append(v)
        i = i + 1
    
    return ("yticklabels={" + ",".join(yticklabels) + "}", "coordinates {" + " ".join(coordinates) + "};") 

def printTable(jsonobj,dimensionX,dimensionY,dimensionXentries,dimensionYentries,details=False):
    
    datamatrix = {}
    idlist = {}
    
    for xentry in dimensionXentries:
        for yentry in dimensionYentries:
            elements = []
            for obj in jsonobj:
                if xentry.upper() in obj[dimensionX].upper() and yentry.upper() in obj[dimensionY].upper(): 
                    nameID = obj["ID"]
                    idlist[nameID] = 1
                    if details:
                        detailstr = ""
                        tokens = obj["evaluation"].split("-")
                        value = tokens[len(tokens) - 1].replace(":","-").replace("%","\%").replace("?","-")
                        if obj[dimensionX].upper().startswith("BEHAVIOR") or obj[dimensionX].upper().startswith("ACTIVITIES"):
                            tokens = obj[dimensionX].split("-")
                            classes = tokens[len(tokens) - 2]
                            detailstr = " " + value + " (C: " + classes + ") \cite{" + nameID + "}"
                        else:
                            detailstr = " " + value + " \cite{" + nameID + "}"
                        elements.append(detailstr)                                                    
                    else:
                        elements.append(nameID)                     
            if not xentry in datamatrix:
                datamatrix[xentry] = {}
            datamatrix[xentry][yentry] = sorted(elements)
    
    #make data struct 
    print str(datamatrix)
    print str(idlist)
    
    #iterate objects and add ref to right cell
    
    table = """
\\begin{table*}[h]
\centering
\\begin{tabular}{%s}
 %s
\end{tabular}
\caption{YYY}
\label{tab:XXX}
\end{table*}
"""

    tableInner = []
    tableHeader = ["p{3cm}"]
    for xentry in dimensionXentries:
        tableInner.append("& \\textbf{" + xentry + "}")
        tableHeader.append("|p{3cm}")    
    tableInner.append("\\\\")
    tableInner.append("\hline ")
    for yentry in dimensionYentries:
        for xentry in dimensionXentries:        
            if xentry == dimensionXentries[0]:
                tableInner.append("\\textbf{" + yentry + "}")
            if details:
                tableInner.append("& " + ",".join(datamatrix[xentry][yentry]))
            else:
                tableInner.append( "& \cite{" + (",".join(datamatrix[xentry][yentry]) + "}"))
            if xentry == dimensionXentries[len(dimensionXentries)-1]:
                tableInner.append("\\\\ ")
                tableInner.append("\hline ")

    return table % ("".join(tableHeader),"".join(tableInner))

if __name__ == '__main__':
    
    path = 'categories.json'
    results = {}
    
    
    f=open(path, 'r')
    lines = []
    for line in f:      
        if line.startswith("#"):
            pass
        else:            
            lines.append(line)

    jsonobj = json.loads("".join(lines))
    print str(len(jsonobj["systems"]))
    
    #sensing strategy vs. people
    #gentable = printTable(jsonobj["systems"],"occupantrelation","sensingstrategy",["Anonymous","Individuals","Crowds"],["Augment the Environment","Augment Persons","Augment Objects","Repurpose Infrastructure","Occupant Interaction"])
    
    #occupancy information vs. temporal coverage
    #gentable = printTable(jsonobj["systems"],"informationtype","temporalcoverage",["Presence","Activities","Behavior"],["Past","Now","Future"])
    
    #spatialgranularity and temporalgranularity
    #gentable = printTable(jsonobj["systems"],"spatialgranularity","temporalgranularity",["Site","Building","BuildingStory","Space","Object"],["Periodic","Event-based"])
    
    #type vs. accuracy
#     gentable = printTable(jsonobj["systems"],"informationtype","evaluation",["Presence-Boolean","Presence-Count","Presence-Track","Activities","Behavior"],["Accuracy","PrecisionRecall","FMeasure","ARatio","Error","RMSE","Visual"],True)
#     gentable = gentable.replace("PrecisionRecall", "Precision and Recall")
#     gentable = gentable.replace("FMeasure", "F-measure")
#     gentable = gentable.replace("ARatio", "Accuracy Ratio")
#     gentable = gentable.replace("Visual", "Indicative Graphs")
            
    #print(gentable)
    
    includelist = ["EbadatBVWJ13","Christensen2014","MelfiRNC11","attar2011sensor","AgarwalBGLWW10","zhao2014occupant","Chang2013","Duarte2013587","HarleH08","SahaTSA14","HarleH08","Krioukov2012PBC","KoehlerZMD13","ScottBKMHHV11","patti2014event","BalajiXNGA13","Krioukov2012PBC","Christensen2014","MelfiRNC11","NguyenA12","GeorgievskiNA13","NguyenA12","GeorgievskiNA13","KoehlerZMD13","ScottBKMHHV11","ScottBKMHHV11","Beltran2013","Erickson2009","Erickson11a","dong2011building"]
    
    gendist = printCSVDistribution(jsonobj["systems"],"sensormodality",[u'Magnetic Fields-Access Cards', u'Infrared light-PIR', u'Visible Light-Light Level', u'Force-Switch', u'Occupant Data-Social Networking', u'EM Waves-Radio-based Communication', u'Air', u'HVAC Data', u'Electricity-Meter', u'Force-Pressure', u'Visible Light-Video Camera', u'Occupant Data-Calendar', u'Ultrasound-Sonar', u'Sound-Microphone', u'Magnetic Fields-REED Switch', u'Force-Device Input', u'Infrared Light-Thermal Camera', u'Water-Flow Meter'])
    
    #gendist = printCSVDistribution(jsonobj["systems"],"modelingstrategy",["Conditional Rules","Agent-based Models", "Stochastic Models", "Machine Learning", "Prediction Algorithms","Signal Analysis","Heuristics"],includelist)
    
    print(gendist[0])
    
    print(gendist[1])
    