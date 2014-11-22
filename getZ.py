def getZ(x, y):
    xOrig = cmds.xform('baseMesh.vtx[*]', q=True, ws=True, t=True)
    origPts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])
    nbPoints = 0
    totalZ = 0
    valZ = 0
    for pos in origPts:
        if(x-20<pos[0] and x+20>pos[0] and y-20<pos[1] and y+20>pos[1]):
            totalZ+=pos[2]
            nbPoints+=1
    if(nbPoints>0):
        valZ = totalZ/nbPoints
    return(valZ)
    
print(getZ(10,20))