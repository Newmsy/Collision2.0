import CollisionBase
import random
import numpy as np
import matplotlib.pyplot as plt
import itertools
import Boundaries
import argparse

def GetArgs():
    parser = argparse.ArgumentParser(
        description='Arguments input for main program')
    parser.add_argument('--xpos',type=int,default=60)
    parser.add_argument('--capills',type=int,default=0)
    parser.add_argument('--iternum',type=int,default=50000)
    parser.add_argument('--rand',type=int,default=20)
    return parser.parse_args()


if __name__ == '__main__':
    XPos = GetArgs().xpos
    NCapill = GetArgs().capills
    NIter = GetArgs().iternum
    Randomness = GetArgs().rand
    TotalBoundaries,TotalLims = Boundaries.Boundaries(NCapill,XPos)

    with open(r'C:\Scripts\Project\CollisionDataStore\\'+('{}CapillCollX{}Random{}.txt'.format(NCapill,XPos,Randomness)),mode='a') as FileWall:
        FileWall.truncate(0)
        YHistHold=[]
        for __ in range(NIter):
            if __%int(NIter/100)==0:
                print(int(100*__/(NIter)),end='\r')
            YHold=CollisionBase.main(200,TotalBoundaries,TotalLims,XPos,Randomness)[1]
            #print(YHold)
            if abs(YHold[-1])<1e10 and len(YHold)!=200:
                YHistHold.append(YHold[-1])

                FileWall.write(str(YHold[-1])+'\n')
        plt.hist(YHistHold,200)
        plt.xlabel('Final Y-position /mm')
        StDev=np.std(YHistHold)
        print('Standard Dev:',StDev)
        #plt.text(max(YHistHold)-400,300,'Standard Deviation: '+str(round(StDev,1)))

        plt.show()
