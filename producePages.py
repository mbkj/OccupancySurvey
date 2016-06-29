import json
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

if __name__ == '__main__':
    
    results = {}
    reflines = {}
    
    prettyprint = {"occupantrelation":"Occupant Relation",
                    "informationtype":"Information Type",
                    "spatialgranularity":"Spatial Granularity",
                    "temporalgranularity":"Temporal Granularity",
                    "spatialcoverage":"Spatial Coverage",
                    "temporalcoverage":"Temporal Coverage",
                    "sensormodality":"Sensor Modality",
                    "sensingstrategy":"Sensing Strategy",
                    "modelingstrategy":"Modeling Strategy"}
    
    
    f=open('occupancysurvey.bib', 'r')
    i = 1
    for line in f:      
        if line.startswith("#"):
            pass
        else:            
            if line.startswith("@"):
                pubname = line[line.find("{")+1:(len(line)-2)]
                reflines[pubname] = i
        i = i + 1       
    
    
    f=open('categories.json', 'r')
    lines = []
    for line in f:      
        if line.startswith("#"):
            pass
        else:            
            lines.append(line)

    jsonobj = json.loads("".join(lines))
    
    #Print main page
    
    for val in prettyprint.values():
        print " * [[%s|%s]]" % (val,val)
        
    # Print each subpage
    
    for key in prettyprint:
        print "Producing: " + prettyprint[key]
        results = {}
        for obj in jsonobj["systems"]:
            for val in obj[key].split(","):                
                valkey = val.split("-")[0]
                if not valkey in results:
                    results[valkey] = []
                for objkey in obj["ID"].split(","):
                    results[valkey].append(objkey)
        
        graphdata = {}
        for subkey in results:
            graphdata[subkey] = len(results[subkey])
            refentries = []
            for refentry in results[subkey]:
                refentries.append("[[%s|https://github.com/mbkj/OccupancySurvey/blob/master/occupancysurvey.bib#L%i]]" % (refentry,reflines[refentry]))
            print " * ***%s (%i)*** %s" % (subkey,len(results[subkey]),",".join(refentries))
                    
        graphkeys = graphdata.keys()
        graphvalues = graphdata.values()
        y_pos = np.arange(len(graphkeys))
        plt.barh(y_pos, graphvalues, align='center')
        plt.yticks(y_pos, graphkeys)
        plt.xlabel('Number of Examples')
        plt.title('Classification of ' + prettyprint[key])
        plt.savefig(key + '.png', format='png', bbox_inches='tight')
        plt.close()
    
    