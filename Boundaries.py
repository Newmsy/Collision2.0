def MakeCapillaries(Number,XPos):
    #Makes the capillary arrays for how ever many capills we want, woooooo
    FunctCapillaries=[]
    FunctCapillaryBounds=[]
    if Number==0:
        return FunctCapillaries,FunctCapillaryBounds
    Step = 6/Number
    for i in range(1,Number):
        Boundary = [0,i*Step-3]
        BoundaryLim = [[XPos,XPos+20],[i*Step-2.999999,i*Step-3.0000001]]
        FunctCapillaries.append(Boundary)
        FunctCapillaryBounds.append(BoundaryLim)
    print('{} boundaries made! At y={}'.format(Number-1,list(i*Step-3 for i in range(1,Number))))
    return FunctCapillaries,FunctCapillaryBounds


def Boundaries(NCapills,XPos):
    X1,X2=XPos,XPos+40
    Y1,Y2=-3,3
    ### CONDITIONS ###
    ### MAIN BOUNDARIES ###
    Boundary1 = [1e10,-X2*1e10]
    BoundaryLims1 = [[X2-0.000001,X2+0.000001],[Y1-0.000001,Y2+0.0000001]]

    Boundary2 = [0,Y2]
    BoundaryLims2 = [[X1,X2+0.00001],[Y2-0.0000001,Y2+0.000001]]

    Boundary3 = [0,Y1]
    BoundaryLims3 = [[X1,X2+0.00001],[Y1-0.0000001,Y2+1.000001]]


    BoundaryEnd = [1e10,0]
    BoundaryLimsEnd = None
    ###For A Funnel on the end###
    # BoundaryF1 = [1e10,-60e10]
    # BoundaryLimsF1 = [[59.99999,60.00001],[1,3.0001]]
    #
    # BoundaryF2 = [1e10,-60e10]
    # BoundaryLimsF2 = [[59.99999,60.00001],[-1,-3.0001]]

    #For Capillaries
    FunctCapBounds,FunctCapLims=MakeCapillaries(NCapills,XPos)
    TotalBoundaries=[Boundary1,Boundary2,Boundary3,BoundaryEnd] + FunctCapBounds # + BoundaryCapillaries + BoundaryFineCapillaries
    TotalLims = [BoundaryLims1,BoundaryLims2,BoundaryLims3,BoundaryLimsEnd] + FunctCapLims # + BoundaryLimsCapillaries + BoundaryLimsFineCapillaries
    return TotalBoundaries,TotalLims
