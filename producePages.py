import json
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

if __name__ == '__main__':
    
    path = 'categories.json'
    results = {}
    
    prettyprint = {"occupantrelation":"Occupant Relation",
                    "informationtype":"Information Type",
                    "spatialgranularity":"Spatial Granularity",
                    "temporalgranularity":"Temporal Granularity",
                    "spatialcoverage":"Spatial Coverage",
                    "temporalcoverage":"Temporal Coverage",
                    "sensormodality":"Sensor Modality",
                    "sensingstrategy":"Sensing Strategy",
                    "modelingstrategy":"Modeling Strategy"}
    
    f=open(path, 'r')
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
        results = {}
        for obj in jsonobj["systems"]:
            for val in obj[key].split(","):                
                valkey = val.split("-")[0]
                if not valkey in results:
                    results[valkey] = []
                results[valkey].append(obj["ID"])
        
        graphdata = {}
        for subkey in results:
            graphdata[subkey] = len(results[subkey])
            print " * ***%s (%i)*** [%s]" % (subkey,len(results[subkey]),",".join(results[subkey]))
                    
        graphkeys = graphdata.keys()
        graphvalues = graphdata.values()
        y_pos = np.arange(len(graphkeys))
        plt.barh(y_pos, graphvalues, align='center')
        plt.yticks(y_pos, graphkeys)
        plt.xlabel('Number of Examples')
        plt.title('Classification of ' + prettyprint[key])
        plt.savefig(key + '.png', format='png', bbox_inches='tight')
        plt.close()
    
    