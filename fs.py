import json
import csv

## Segments I Need
#   "Snoring"
#   "Wheeze

dataSet={'e':'data/eval_segments.csv','b':'data/balanced_train_segments.csv','u':'data/unbalanced_train_segments.csv'}

##  Load dic
with open('log.json','r') as f:
    rowNum=json.load(f)

##  Get tag code
def getCode(name):
    with open('data/ontology.json','r') as f:
        data=json.load(f)
    for d in data:
        if d['name']==name:
            item=d
    return item['id']

##  Get Selected Segments
def getSeg(ds,name,l=100,nolog=False):
    tag=getCode(name)
    seg=[]
    with open(dataSet[ds]) as f:
        f_csv=csv.reader(f, delimiter=' ')
        for i,row in enumerate(f_csv):
            if row[0]== "#":
                continue
            if l>0:
                if len(seg)>=l:
                    rowNum[ds][name]=i
                    break
            if i>=rowNum[ds][name]:
                if tag in row[3]:
                    seg.append(row)
        else:
            rowNum[ds][name]=0
    if not nolog:
        with open('log.json','w') as f:
            json.dump(rowNum,f)

    print('Got {} segments from the {} dataset'.format(len(seg),ds))
    return seg


##  test code
if __name__=='__main__':
    seg=getSeg('e','Snoring',20,nolog=True)
    for s in seg:
        print(s)
