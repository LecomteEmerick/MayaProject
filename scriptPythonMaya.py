import maya.cmds as cmds

def createListRig(list,nameElement,ikHandleBase=None):
    for index in range(len(list)):
        tuplePoint = list[index]
        tuplePoint = tuple([5*x for x in tuplePoint])
        cmds.joint(p=tuplePoint,name=nameElement + str(index), r=True)
    cmds.ikHandle( sj=ikHandleBase ,ee=nameElement + "0")
    for index in range(len(list)-1) :
        cmds.select(nameElement + str(index+1))
        cmds.ikHandle( sj=nameElement + str(index))
            
pointBaseHand = (0.0,0.0,0.0)
pointPouce = [(1.0,0.0,1.0),(0.75,0.0,0.75),(0.5,0.0,0.5)]
pointIndex = [(0.15,0.0,1.10),(0.125,0.0,0.875),(0.1,0.0,0.65)]
pointMajeur = [(0.0,0.0,1.25),(0.0,0.0,1.0),(0.0,0.0,0.75)]
pointAnnulaire = [(-0.15,0.0,1.10),(-0.125,0.0,0.875),(-0.1,0.0,0.65)]
pointPetit = [(-0.3,0.0,0.95),(-0.25,0.0,0.75),(-0.2,0.0,0.55)]

cmds.joint(p=pointBaseHand,name="handBase")
createListRig(pointPouce,"pouce","handBase")
cmds.select("handBase")
createListRig(pointIndex,"index","handBase")
cmds.select("handBase")
createListRig(pointMajeur,"majeur","handBase")
cmds.select("handBase")
createListRig(pointAnnulaire,"annulaire","handBase")
cmds.select("handBase")
createListRig(pointPetit,"petit","handBase")

cmds.select(clear=True)