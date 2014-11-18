import maya.cmds as cmds

def createListRig(list,nameElement):
    for index in range(len(list)):
        tuplePoint = list[index]
        tuplePoint = tuple([5*x for x in tuplePoint])
        cmds.joint(p=tuplePoint,name=nameElement + str(index), r=True)


pointBaseHand = (0.0,0.0,0.0)
pointPouce = [(1.0,0.0,1.0),(0.75,0.0,0.75),(0.5,0.0,0.5)]
pointIndex = [(0.15,0.0,1.10),(0.125,0.0,0.875),(0.1,0.0,0.65)]
pointMajeur = [(0.0,0.0,1.25),(0.0,0.0,1.0),(0.0,0.0,0.75)]
pointAnnulaire = [(-0.15,0.0,1.10),(-0.125,0.0,0.875),(-0.1,0.0,0.65)]
pointPetit = [(-0.3,0.0,0.95),(-0.25,0.0,0.75),(-0.2,0.0,0.55)]

cmds.joint(p=pointBaseHand,name="handBase")
createListRig(pointPouce,"pouce")
cmds.select("handBase")
createListRig(pointIndex,"index")
cmds.select("handBase")
createListRig(pointMajeur,"majeur")
cmds.select("handBase")
createListRig(pointAnnulaire,"annulaire")
cmds.select("handBase")
createListRig(pointPetit,"petit")

cmds.select(clear=True)