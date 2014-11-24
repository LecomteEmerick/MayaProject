import maya.cmds as cmds
import sys

class AutorigginUI :

	def __init__(self):
		# Constants
		self.width = 300
		self.height = 700
		
		self.pointButtonWidth = 100
		self.pointButtonHeight = 50

		self.pointButtonStateWidth = 50

		self.cameraZ = 50
		# Note for "state" attrb :
		#	0 (RED): not set
		#	1 (YELLOW): pending (user have to click)
		#	2 (GREEN): set
		needColor = [0.6,0.9,0.3]
		osefColor = [0.7,0.7,0.7]
		self.pointsMap = {
			"neck" : {
				"label" : "Cou",
				"desc" : "Obligatoire",
				"color" :needColor
			},
			"wrist_left" : {
				"label" : "Poignet Gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"wrist_right" : {
				"label" : "Poignet Droit",
				"desc" : "Facultatif",
				"color" : osefColor
			},
			"elbow_left" : {
				"label" : "Coude gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"elbow_right" : {
				"label" : "Coude droit",
				"desc" : "Facultatif",
				"color" : osefColor
			},
			"shoulder_left" : {
				"label" : "Epaule Gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"shoulder_right" : {
				"label" : "Epaule Droite",
				"desc" : "Facultatif",
				"color" : osefColor
			},
			"hip" : {
				"label" : "Haches",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"leg_left" : {
				"label" : "Jambe Gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"leg_right" : {
				"label" : "Jambe Droite",
				"desc" : "Facultatif",
				"color" : osefColor
			},
			"knee_left" : {
				"label" : "Genou Gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"knee_right" : {
				"label" : "Genou Droit",
				"desc" : "Facultatif",
				"color" : osefColor
			},
			"foot_left" : {
				"label" : "Pied Gauche",
				"desc" : "Obligatoire",
				"color" : needColor
			},
			"foot_right" : {
				"label" : "Pied Droit",
				"desc" : "Facultatif",
				"color" : osefColor
			},


		}
		# Init map
		for p in self.pointsMap :
			self.pointsMap[p]["button"] = None
			self.pointsMap[p]["stateButton"] = None
			self.pointsMap[p]["isSet"] = False
			self.pointsMap[p]["clickedPoint"] = None

		# Params
		self.isActive = False
		self.currentCamera = False
		self.cameraOrigin = None

		# Click mode params
		self.currentPointKey = None

		# Getting camera
		self.currentCamera = cmds.ls("persp")
		if not self.currentCamera :
			print("Camera not found")
			return


		self.buildUI()

	def buildUI(self) :
		self.resetExternalContext()

		self.window = cmds.window("autorigging_ui", title="Auto-rigging (BB, EL, TP)", w=self.width, h=self.height)
		
		# Title
		cmds.columnLayout(w=self.width, h=self.height)
		cmds.separator(h=10)
		cmds.text(label="Autorigging", w=self.width,h=20, backgroundColor=[0.15,0.15,0.15])
		cmds.separator(h=10)

		# Mesh selector
		self.meshSelector = cmds.optionMenu(w=self.width,h=30,label="Choisissez un Mesh :")
		for m in cmds.ls(type="transform"):
			cmds.menuItem(label=str(m))

		cmds.separator(h=40)

		# Point buttons
		cmds.scrollLayout(w=self.width)
		self.definePointButtons()
		

		# Action buttons (enter mode)
		cmds.setParent("..")
		cmds.setParent("..") # Here to exit scrollLayout
		cmds.separator(h=10)
		cmds.rowLayout(numberOfColumns=3)
		self.activateButton = cmds.button("activetaBtn",
			label="Activer", 
			w=self.width/3 - 10, 
			h=self.pointButtonHeight,
			command=self.onActivateButtonClick
		)
		self.generateButton = cmds.button("generateBtn",
			label="Generer", 
			w=self.width/3 - 10, 
			h=self.pointButtonHeight,
			command=self.onGenerateButtonClick
		)
		self.autoGenerateButton = cmds.button("generateAutoRigBtn",
			label="AutoGenerer", 
			w=self.width/3 - 10, 
			h=self.pointButtonHeight,
			command=self.onAutoRigButtonClick
		)
		# Console
		
		cmds.setParent("..")
		cmds.columnLayout()
		cmds.separator(h=10)
		self.consoleText = cmds.text(label="Auto-rigging non-actif", width=self.width, height=50, backgroundColor=[0.3,0.3,0.3])

		cmds.showWindow(self.window)

		cmds.draggerContext("riggingContext", space="world", pressCommand=self.on3DSceneClick)
		
		# Registring context ?
		cmds.setToolTo("riggingContext")

	def resetExternalContext(self):
		if cmds.window("autorigging_ui", exists=True) :
			cmds.deleteUI("autorigging_ui")
		if cmds.draggerContext("riggingContext", exists=True) :
			cmds.deleteUI("riggingContext")


	def closeWindow (self):
		print("CLOSE")

	def setConsoleText(self, text, color=[0.3,0.3,0.3]):
		# 'e' flag is requested for editing
		cmds.text(self.consoleText, label=text,e=True,backgroundColor=color)

	def definePointButtons(self):
		first = True


		for config in self.pointsMap :
			if not first:
				cmds.setParent("..")

			cmds.rowLayout(numberOfColumns=5)

			cmds.canvas(h=3,w=3,backgroundColor=self.pointsMap[config]["color"])
			cmds.separator(visible=0,w=2)
			self.definePointButton(config)
			cmds.separator(visible=0,w=5)
			#cmds.canvas(h=60,w=1,backgroundColor=self.pointsMap[config]["color"])
			self.defineStateButton(config)

			first = False

	def definePointButton(self, key):
		def click (e):
			self.onPointButtonClick(key)

		bg = [0,100,100]

		try :
			bg = self.pointsMap[key]["color"]
		except :
			pass
		
		self.pointsMap[key]["button"] = cmds.button(
			label=self.pointsMap[key]["label"],
			w=self.pointButtonWidth, 
			h=self.pointButtonHeight,
			backgroundColor= bg,
			command=click
		)

	def defineStateButton(self, key):
		def click (e):
			self.onStateButtonClick(key)

		self.pointsMap[key]["stateButton"] = cmds.button(
			label="",
			backgroundColor=[255,0,0],
			w=self.pointButtonStateWidth,
			h=self.pointButtonHeight,
			command=click
		)

	#
	# Event actions
	#
	def onAutoRigButtonClick(self,e):
		meshName = cmds.optionMenu(self.meshSelector, query=1, value=1)
		self.autoRig(meshName)
	
	def onStateButtonClick(self, key):
		if self.pointsMap[key]["isSet"] is False :
			return

		cmds.delete(key+"sphere")

		stateBtn = self.pointsMap[key]["stateButton"]
		cmds.button(stateBtn, e=1, backgroundColor=[255,0,0], label="")
		self.pointsMap[key]["isSet"] = False
		self.pointsMap[key]["clickedPoint"] = None

		

	def onPointButtonClick(self, key):
		if self.currentPointKey is not None and self.currentPointKey != key and self.pointsMap[key]["isSet"] is False :
			cmds.button(self.pointsMap[key]["stateButton"], e=1, backgroundColor=[255,0,0], label="")
			
		self.currentPointKey = key
		self.setConsoleText("Placez le point '" + key + "'")

		stateBtn = self.pointsMap[key]["stateButton"]
		cmds.button(stateBtn, e=1, backgroundColor=[255,255,0], label="")

	def on3DSceneClick(self):
		if not cmds.window("autorigging_ui", exists=True) :
			self.resetExternalContext()
			return
		
		if not self.isActive :
			self.setConsoleText("Vous devez activer l'autorigging.",color=[255,0,0])
			return

		if not self.currentPointKey :
			self.setConsoleText("Choisissez un type de point a placer.")
			return


		pos = cmds.draggerContext("riggingContext", query=1, anchorPoint=1)
		strPos = "x:"+str(round(pos[0],2)) +"\ny:" + str(round(pos[1],2))

		if self.pointsMap[self.currentPointKey]["isSet"] is True :
			cmds.delete(self.currentPointKey+"sphere")
		
		
		nextObj = cmds.polySphere(name=self.currentPointKey+"sphere", radius=0.3)
		cmds.move(pos[0], pos[1], 10, nextObj)
		cmds.scale(1.0,1.0,0.0, nextObj)

		self.pointsMap[self.currentPointKey]["isSet"] = True
		self.pointsMap[self.currentPointKey]["clickedPoint"] = pos
		cmds.button(self.pointsMap[self.currentPointKey]["stateButton"], e=1, backgroundColor=[0,255,0],label=strPos)

		#print("Key == " + self.currentPointKey + " Pos == " + str(pos))
	

	def onActivateButtonClick(self,param):
		if self.isActive is True:
			self.isActive = False

			if self.cameraOrigin is not None :
				cmds.camera(self.currentCamera, edit=True, position=self.cameraOrigin["translate"], rotation=self.cameraOrigin["rotation"])
			
			self.setConsoleText("Rigging desactive.")

			for p in self.pointsMap :
				self.onStateButtonClick(p)

			return

		self.isActive = True

		self.cameraOrigin = {
			"translate" : cmds.xform(self.currentCamera, query=1, ws=1,rp=1),
			"rotation" : cmds.xform(self.currentCamera, query=1, ws=1,ro=1),
		}

		cmds.camera(self.currentCamera, edit=True, position=[0,0,self.cameraZ],rotation=[0,0,0])


		self.setConsoleText("Rigging actif, choisissez un point.", color=[0,0.4,0])
	
	def onGenerateButtonClick(self,param) :
		valid = True
		output = {}
		meshName = cmds.optionMenu(self.meshSelector, query=1, value=1)

		def getMirror(coor) :
			return (coor[0]*-1,coor[1],coor[2])

		exceptions = {
			"foot_right" : { 
				"action" : getMirror,
				"key" : "foot_left"
			},
			"knee_right" : { 
				"action" : getMirror,
				"key" : "knee_left"
			},
			"leg_right" : { 
				"action" : getMirror,
				"key" : "leg_left"
			},
			"wrist_right" : { 
				"action" : getMirror,
				"key" : "wrist_left"
			},
			"elbow_right" : { 
				"action" : getMirror,
				"key" : "elbow_left"
			},
			"shoulder_right" : { 
				"action" : getMirror,
				"key" : "shoulder_left"
			},
		}
		if not meshName :
			self.setConsoleText("Choisissez un mesh a rigger", color=[0.8,0,0])
			return

		for p in self.pointsMap :
			if not self.pointsMap[p]["isSet"] or self.pointsMap[p]["clickedPoint"] is None :
				excFound = False
				# Check if in exceptions list
				for exc in exceptions :
					if exc == p :
						point = None
						try :
							point = self.pointsMap[exceptions[exc]["key"]]["clickedPoint"]
						except:
							self.setConsoleText("Impossible de trouver la valeur mirroir du point " + str(p))
							return

						self.pointsMap[p]["clickedPoint"] = exceptions[exc]["action"](point)
						excFound = True
						break

				if not excFound :
					valid = False
					self.setConsoleText("Le point '" + p + "' n'est pas defini.", color=[0.8,0,0])
					break
			
			output[p] = {}
			output[p]["point"] = (
				self.pointsMap[p]["clickedPoint"][0],
				self.pointsMap[p]["clickedPoint"][1],
				self.getZ(self.pointsMap[p]["clickedPoint"][0],self.pointsMap[p]["clickedPoint"][1],meshName))

		if valid :
			output["mesh_name"] = meshName
			print(str(output))
			self.generate(output)
			# DO STUFF IF VALID !
			return output
		else :
			return None



	def generate(self, params):
		print("OK !! " + str(params))
		cmds.select(clear=True)
		cmds.joint(p=params["hip"]["point"],name="bassinBase")
		cmds.select("bassinBase")
		rigList = [params["neck"]["point"],params["shoulder_left"]["point"],params["elbow_left"]["point"],params["wrist_left"]["point"]]
		self.createListRig(rigList,"rigTop","bassinBase")
		cmds.select("bassinBase")
		rigList2 = [params["leg_left"]["point"],params["knee_left"]["point"],params["foot_left"]["point"]]
		self.createListRig(rigList2,"rigBot","bassinBase")
		cmds.select("rigTop1")
		cmds.mirrorJoint(mirrorYZ=True)
		cmds.select("rigBot0")
		cmds.mirrorJoint(mirrorYZ=True)
		cmds.select("bassinBase")
		cmds.select(params["mesh_name"],tgl=True)
		cmds.bindSkin()

	
	def createListRig(self, list,nameElement,ikHandleBase=None):
		for index in range(len(list)):
			tuplePoint = list[index]
			cmds.joint(p=tuplePoint,name=nameElement + str(index))
			cmds.ikHandle( sj=ikHandleBase ,ee=nameElement + "0")
			cmds.select(nameElement + str(index))
		for index in range(len(list)-1) :
			cmds.select(nameElement + str(index+1))
			cmds.ikHandle(sj=nameElement + str(index))

	def getSizeX(self,meshName):
		xOrig = cmds.xform(meshName+'.vtx[*]', q=True, ws=True, t=True)
		origPts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])
		minX = sys.maxsize
		maxX = -sys.maxsize
		for pos in origPts:
			if(pos[0]>maxX):
				maxX=pos[0]
			if(pos[0]<minX):
				minX=pos[0]
		return([(maxX-minX),(maxX-abs(minX))])

	def getSizeY(self,meshName):
		xOrig = cmds.xform(meshName+'.vtx[*]', q=True, ws=True, t=True)
		origPts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])
		minY = sys.maxsize
		maxY = -sys.maxsize
		for pos in origPts:
			if(pos[1]>maxY):
				maxY=pos[1]
			if(pos[1]<minY):
				minY=pos[1]
		return([(maxY-minY),minY])


	def getZ(self,x, y,meshName):
		size = self.getSizeY(meshName)[0]/10
		xOrig = cmds.xform( meshName + '.vtx[*]', q=True, ws=True, t=True)
		origPts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])
		nbPoints = 0
		totalZ = 0
		valZ = 0
		for pos in origPts:
			if(x-size<pos[0] and x+size>pos[0] and y-size<pos[1] and y+size>pos[1]):
				totalZ+=pos[2]
				nbPoints+=1
		if(nbPoints>0):
			valZ = totalZ/nbPoints
		return(valZ)
			
	def autoRig(self,meshName):
		height = self.getSizeY(meshName)
		minPosY = height[1]
		height = height[0]
		width = self.getSizeX(meshName)
		minPosX = width[1]
		width = width[0]
		bassinPoint = (minPosX + width * 0.0,minPosY + height * 0.48,self.getZ(minPosX + width * 0.0,minPosY + height * 0.48,meshName))
		couPoint = (minPosX + width * 0.0,minPosY + height * 0.870,self.getZ(minPosX + width * 0.0,minPosY + height * 0.870,meshName))
		epaulePoint = (minPosX + width * 0.129,minPosY + height * 0.825,self.getZ(minPosX + width * 0.129,minPosY + height * 0.825,meshName))
		coudePoint = (minPosX + width * 0.315,minPosY + height * 0.825,self.getZ(minPosX + width * 0.315,minPosY + height * 0.825,meshName))
		poignetPoint = (minPosX + width * 0.461,minPosY + height * 0.825,self.getZ(minPosX + width * 0.461,minPosY + height * 0.825,meshName))
		jambePoint = (minPosX + width * 0.0955,minPosY + height * 0.4,self.getZ(minPosX + width * 0.0955,minPosY + height * 0.4,meshName))
		genouPoint = (minPosX + width * 0.1,minPosY + height * 0.285,self.getZ(minPosX + width * 0.1,minPosY + height * 0.285,meshName))
		piedPoint = (minPosX + width * 0.12,minPosY + height * 0.039 ,self.getZ(minPosX + width * 0.12,minPosY + height * 0.039,meshName))
		
		cmds.select(clear=True)
		cmds.joint(p=bassinPoint,name="bassinBase")
		cmds.select("bassinBase")
		rigList = [couPoint,epaulePoint,coudePoint,poignetPoint]
		self.createListRig(rigList,"rigTop","bassinBase")
		cmds.select("bassinBase")
		rigList2 = [jambePoint,genouPoint,piedPoint]
		self.createListRig(rigList2,"rigBot","bassinBase")
		cmds.select("rigTop1")
		cmds.mirrorJoint(mirrorYZ=True)
		cmds.select("rigBot0")
		cmds.mirrorJoint(mirrorYZ=True)
		cmds.select("bassinBase")
		cmds.select(meshName,tgl=True)
		cmds.bindSkin()
		


{'hip': {'point': (0.8902097988472102, 81.00909169509568, 0)}, 
'leg_right': {'point': (10.979254185782196, 74.48088650354948, 0)}, 
'leg_left': {'point': (-10.979254185782196, 74.48088650354948, 0)}, 
'neck': {'point': (0.29673659961572985, 140.94988481747416, 0)}, 
'mesh_name': u'highFBXASC045polyMeshShape', 
'shoulder_right': {'point': (19.881352174254243, 128.48694763361328, 0)}, 
'wrist_left': {'point': (-44.80722654197598, 101.18718046896566, 0)}, 
'shoulder_left': {'point': (-19.881352174254243, 128.48694763361328, 0)}, 
'wrist_right': {'point': (44.80722654197598, 101.18718046896566, 0)}, 
'knee_right': {'point': (13.353146982708074, 48.961538936596284, 0)}, 
'elbow_right': {'point': (31.15734295965217, 113.65011765282652, 0)}, 
'elbow_left': {'point': (-31.15734295965217, 113.65011765282652, 0)}, 
'foot_right': {'point': (18.694405775791296, 6.824941791161921, 0)}, 
'knee_left': {'point': (-13.353146982708074, 48.961538936596284, 0)}, 
'foot_left': {'point': (-18.694405775791296, 6.824941791161921, 0)}}