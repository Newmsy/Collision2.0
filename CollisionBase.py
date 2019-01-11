import random
import numpy as np
import matplotlib.pyplot as plt
import itertools

def CollisionFinder(MCLine,MCDir,LinePosition,MCBoundary,BoundaryLimits):
    '''
    COLLISION FINDER
    Function which calculates the collision POSITION given: the line gradient (M) and constant (C), the line\'s previous position
    The line\'s direction (To differentiate between the two direction-based solutions), then the boundary gradient and constant
    and the limits of the boundary.

    MCLine: a tuple of two integer values (gradient,constant), defining the line of motion of the particle
    MCDir: the x-direction of the line, takes one of two values: +1 for increasing x, -1 for decreasing x
    LinePosition: (x,y) tuple of the previous position of the particle (i.e usually the last wall position of the collision)
    MCboundary: a tuple of two integer values (gradient,constant), defining the line of the boundary
    BoundaryLimits: two lists nested within a list, each containing a set of [xmin,xmax],[ymin,ymax] values for the boundary conditions

    Return Values:
    Ideal output: an (x,y) tuple of the new collision position
    Else: returns a string stating why no collision was made

    To use this function in a closed system iterate over all boundaries
    '''
    if MCLine[0]==MCBoundary[0]:
        #print('No Collision - Same Grad')
        return 'No Collision - Same Grad'

    XSolution = (MCBoundary[1]-MCLine[1])/(MCLine[0]-MCBoundary[0])
    YSolution = XSolution*MCLine[0]+MCLine[1]
    if BoundaryLimits==None:
        return [XSolution,YSolution,'Special']
    if (LinePosition[0]<min(BoundaryLimits[0]) and MCDir==-1) or (LinePosition[0]>max(BoundaryLimits[0]) and MCDir==1):
        #print('No Collision - Wrong Direction')
        return 'No Collision - Wrong Direction'
    if XSolution>max(BoundaryLimits[0]) or XSolution<min(BoundaryLimits[0]) or YSolution>max(BoundaryLimits[1]) or YSolution<min(BoundaryLimits[1]):
        #print('No Collision - Out of Boundary Limits')
        return 'No Collision - Out of Boundary Limits'
    if (XSolution>LinePosition[0] and MCDir==-1) or (XSolution<LinePosition[0] and MCDir==1):
        #print('No Collision - Wrong Direction 2')
        return 'Non Collision - Wrong Direction 2'
    return [XSolution,YSolution]

def Reflector(ParticleAngle,WallAngle,Randomness=0):

    '''
    Function that returns the reflected angle of an incoming line and a wall.
    We define 0 degrees as the positive x direction, increasing anticlockwise. All angles are between 0 and 359.999...

    ParticleAngle: The incoming angle of the particle in degrees
    WallAngle: The angle of the wall, since this does not have a direction the wall angle can be either direction along its line
               e.g the 45 degree wall, given by y=x line, will return the same reflection as a 225 degree wall
    Randomness: Optional arg which randomises the return angle. This will be limited by the wall angle so that particle doesn't ever go through
                the wall.

    Return Values:
    Only output: single integer of the new reflected outgoing angle.
    '''

    WallAngle = (WallAngle+360)%180
    OutAngle = ((2*WallAngle - ParticleAngle)+360)%360
    LimitAngle = min(abs(WallAngle-OutAngle),abs(180+WallAngle-OutAngle),abs(360+WallAngle-OutAngle))
    Randomness = min(abs(Randomness),round(LimitAngle/1.5))
    #print('ParticleAngle: '+str(ParticleAngle)+ '   WallAngle: '+str(WallAngle)+ '    OutAngle:'+str(OutAngle))
    ReturnedAngle = (OutAngle + random.randint(-Randomness,Randomness))%360
    while ReturnedAngle%90==0:
        ReturnedAngle = (OutAngle + random.randint(-Randomness,Randomness))%360
    return ReturnedAngle

def ConvertDegToMC(Degrees):

    '''
    Function that takes a degree value and tranforms it into line gradient information and a XDir to differentiate between two possible directions

    Degrees: integer input between 0 and 360

    Return values:
    Only return: A combination of (gradient,xdirection)
    Note: No constant returned for line information
    '''

    XDir = -1 if (Degrees <= 270 and Degrees >90) else  1
    return np.tan(Degrees*np.pi/180),XDir

def ConvertMCToDeg(MLine,XDir):

    '''
    Function that takes a line gradient and direction and transforms it into an angle in degrees

    MLine: Gradient information about the line
    XDir: XDirection, takes +1 if increasing x, else -1

    Return values:
    Only return: A integer value of degrees
    '''
    Additional = 180 if (XDir == -1) else 0
    Additional = 360 if (not Additional and np.sign(MLine)==-1) else Additional
    return ((np.arctan(MLine)*180/np.pi) + Additional)%360

def DistanceChooser(StartPosition,HitPositions,HitNumbers):

    '''
    Given all of the collision points, this function will return the closest one to the origin, this helps create a more
    realistic situation to avoid a particle travelling through a wall and colliding with the one behind it instead

    StartPosition: a tuple of (x,y) values for the previous position of the particle
    HitPositions: a list of all (x,y) collisions found
    HitNumbers: a list of integers of the collisional walls\'s indeces within the total boundary limits, this helps determine which
                wall should be ignored over the next iteration of collisions after colliding with a wall

    Return values:
    Ideal output: the position (x,y) of the nearest collision and the index of the wall in the total boundaries list
    Else: if the HitPositions is an empty list then no collisions have been found and an error is raised
    '''

    if len(HitPositions)==0:
        print('SOMETHING WRONG NOTHING HIT')
        k=input()

    if len(HitPositions)==1:
        if len(HitPositions[0])==3:
            return HitPositions[0][:2],'Break'
        return HitPositions[0],HitNumbers[0]
    func = lambda x:((x[0]-StartPosition[0])**2 + (x[1]-StartPosition[1])**2)**0.5
    MinDistance= min(HitPositions,key=func)
    #print('HN'+str(HitNumbers))
    #print(HitNumbers[HitPositions.index(MinDistance)])
    return MinDistance,HitNumbers[HitPositions.index(MinDistance)]

def MToMC(M, Position):
    '''
    Converts a gradient and a position into (gradient,constant) line information

    M: the gradient of the line
    Position: the current (x,y) position of the particle

    Return values:
    Only output: (gradient,constant) integers
    '''
    Constant = Position[1]-M*Position[0]
    return [M,Constant]

def main(IterationNumber,TotalBoundaries,TotalLims,XPos,Randomness):
    '''
    Main Iterator, does shit, not sure how
    '''
    #CONDITIONS
    RandomAngle = Randomness
    Start = [XPos+30,0]
    StartAng = random.randint(0,359)
    StartM,StartDir = ConvertDegToMC(StartAng)
    StartMC = MToMC(StartM,Start)

    #print(TotalBoundaries)

    ###   Initiating data stores   ####
    XYPlotHold=[[],[]]
    XYPlotHold[0].append(Start[0])
    XYPlotHold[1].append(Start[1])
    CurrentPosition=Start
    CurrentMC = StartMC
    CurrentDir = StartDir
    CurrentAng = ConvertMCToDeg(CurrentMC[0],CurrentDir)
    IgnoreWall=-1

    ###   Iterations    ###
    for _ in range(IterationNumber):
        PossibleHits=[]
        HitNumber=[]
        for NIndex,(Bound,BLims) in enumerate(zip(TotalBoundaries,TotalLims)):
            #print('Iteration: '+ str(_) + '    NIndex: '+str(NIndex))
            if NIndex==IgnoreWall:
                continue
            #Iterates over all possible hits, must choose nearest
            Coll = CollisionFinder(CurrentMC,CurrentDir,CurrentPosition,Bound,BLims)
            if type(Coll)!=str:
                if len(Coll)==2:
                    PossibleHits.append(Coll)
                    HitNumber.append(NIndex)
                if len(Coll)==3:
                    PossibleHits.append(Coll)
                    HitNumber.append(NIndex)
        CurrentPosition,IgnoreWall=DistanceChooser(CurrentPosition,PossibleHits,HitNumber)
        if IgnoreWall=='Break':
            XYPlotHold[0].append(CurrentPosition[0])
            XYPlotHold[1].append(CurrentPosition[1])
            break
        CurrentAng=Reflector(CurrentAng,ConvertMCToDeg(TotalBoundaries[IgnoreWall][0],1),RandomAngle) #Randomness for set above
        CurrentM,CurrentDir=ConvertDegToMC(CurrentAng)
        CurrentMC=MToMC(CurrentM,CurrentPosition)
        XYPlotHold[0].append(CurrentPosition[0])
        XYPlotHold[1].append(CurrentPosition[1])

        #print('POS:'+str(CurrentPosition)+'   ANG:'+str(CurrentAng)+'    MC:' + str(CurrentMC) + '    DIR: '+str(CurrentDir))

    # if abs(XYPlotHold[1][-1])<2000 and _!=(IterationNumber-1):
    #     plt.plot(XYPlotHold[0],XYPlotHold[1])
    return XYPlotHold
