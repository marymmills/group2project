import numpy as np
import pandas as pd

#raw data files can be downloaded from https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-8473/E-MTAB-8473.raw.1.zip
#the files should be extracted and placed into the working directory
#Please note that due to the amount of data, this script will take a few minutes to run

#Save file names as variables for easy typing
#draftraw = 'smallraw.txt'
#draftraw2 = 'smallraw2.txt'
raw1='US10133796_252665223678_S01_GE1_107_Sep09_1_1.txt'
raw2='US10133796_252665223678_S01_GE1_107_Sep09_1_2.txt'
raw3='US10133796_252665223678_S01_GE1_107_Sep09_1_3.txt'
raw4='US10133796_252665223678_S01_GE1_107_Sep09_1_4.txt'
raw5='US10133796_252665223679_S01_GE1_107_Sep09_1_1.txt'
raw6='US10133796_252665223679_S01_GE1_107_Sep09_1_2.txt'
raw7='US10133796_252665223679_S01_GE1_107_Sep09_1_3.txt'
raw8='US10133796_252665223679_S01_GE1_107_Sep09_1_4.txt'
raw9='US10133796_252665223680_S01_GE1_107_Sep09_1_1.txt'
raw10='US10133796_252665223680_S01_GE1_107_Sep09_1_2.txt'
raw11='US10133796_252665223680_S01_GE1_107_Sep09_1_3.txt'
raw12='US10133796_252665223680_S01_GE1_107_Sep09_1_4.txt'

filelist = (raw1,raw2,raw3,raw4,raw5,raw6,raw7,raw8,raw9,raw10,raw11,raw12)
#filelist = (draftraw, draftraw2, raw1)

#Create new files to write results to
proberesultsfile = open('proberesults.txt', 'w+')
probelistfile = open('probelist.txt', 'w+')
probesystemlistfile = open('probesystemlist.txt', 'w+')

#Create new lists for significant ProbeNames and SystematicName
probenames = []
systemnames = []


for f in filelist:
    #import file and create 1D arrays with Numpy
    rawnp = np.genfromtxt(f, skip_header=10, unpack=True, dtype=('U20', int, int, int, int, int, 'U20', 'U20', float, float, float,float,
                                                                float,float,float,int,int,int,int,int,int,float,int, int, float, float))

    #Morph 1D entries into a 2D dataframe with pandas
    rawpandas = pd.DataFrame(rawnp)

    #Name columns in dataframe
    rawpandas.columns = ['Features', 'FeatureNum', 'Row', 'Column', 'SubTypeMask', 'ControlType', 'ProbeName', 'SystematicName',
          'PositionX', 'PositionY', 'gProcessedSignal', 'gProcessedSigError', 'gMedianSignal', 'gBGMedianSignal',
          'gBGPixSDev', 'gIsSaturated', 'gIsFeatNonUnifOL', 'gIsBGNonUnifOL','gIsFeatPopnOL', 'gIsBGPopnOL', 'IsManualFlag', 'gBGSubSignal',
          'gIsPosAndSignif', 'gIsWellAboveBG', 'SpotExtentX', 'gBGMeanSignal']

    #Drop first column in dataframe as it is not needed
    rawpandas = rawpandas.drop(columns=['Features'])

    #Create search to identify the probes that had the desired outputs
    correctprobes=(rawpandas.loc[(rawpandas['ControlType'] == 0) & (rawpandas['gIsWellAboveBG'] == 1) &
                            (rawpandas['gBGSubSignal'] > 0) & (rawpandas['gIsPosAndSignif'] == 1) &
                            (rawpandas['gIsFeatPopnOL'] == 0) & (rawpandas['gIsSaturated'] == 0) &
                            (rawpandas['gIsBGPopnOL'] == 0)])

    #Fill list with significant probe names
    listofnames = correctprobes['ProbeName'].to_list()
    for i in listofnames:
        if i not in probenames:
            probenames.append(i)
    probenames.sort()

    #Fill list with significant systematic names
    listofsystemnames = correctprobes['SystematicName'].to_list()
    for i in listofsystemnames:
        if i not in systemnames:
            systemnames.append(i)
    systemnames.sort()
        
#Write significant probe data to file
correctprobes.to_csv(proberesultsfile, mode='a', header=True, index=False)

#Write significant probe names to file
with open('probelist.txt', 'a') as file:
    file.write('The following is a list of significant probes by probe name \n')
    for i in probenames:
        file.write((i) + ', ')

#Write significant systematic names to file
with open('probesystemlist.txt', 'a') as file:
    file.write('The following is a list of significant probes by systematic name \n')
    for i in systemnames:
        file.write((i) + ', ')

#Close all files
proberesultsfile.close()
probelistfile.close()
probesystemlistfile.close()

#Print general results
print('done!')
print('There were ' + str(len(probenames)) + ' significant probes found')



#Create new dataframe with counts of how many times each probe was significant 
#probecounts = pd.DataFrame(correctprobes.SystematicName.value_counts().reset_index().values, columns=['Name', 'AggregateCounts'])
#probecounts_index = probecounts.sort_index(axis = 0, ascending = True)
#print(probecounts_index)
