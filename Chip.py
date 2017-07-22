#Fuction for generating Cube borrowed from Jon Macey - Available from https://nccastaff.bournemouth.ac.uk/jmacey/
#!/usr/bin/python
import getpass
import time
import prman
import math
import random

ri = prman.Ri()
filename = "Chip_01.rib"
ri.Begin(filename)
ri.Option("rib", {"string asciistyle": "indented"})
ri.Display("Chip_01.tiff", "it", "rgba")
ri.Format(1280,720,1)
ri.Projection(ri.PERSPECTIVE,{ri.FOV:20})
ri.PixelVariance(0.01)
ri.Hider("raytrace", {"int incremental":1, "int maxsamples":1024})
ri.Integrator("PxrPathTracer", "integrator")
ri.DepthOfField(5.6,0.2,2.2)
ri.Exposure(1.0,2.2)
ri.ShadingRate(0.05)

#FUNCTIONS
def Cube(width, height, depth):
    w = width/2.0
    h = height/2.0
    d = depth/2.0
    face = [-w,-h,d,-w,h,d,w,-h,d,w,h,d]
    ri.Patch("bilinear",{'P':face})
    face = [-w,-h,-d,-w,h,-d,w,-h,-d,w,h,-d]
    ri.Patch("bilinear",{'P':face})
    face = [-w,-h,-d,-w,h,-d,-w,-h,d,-w,h,d]
    ri.Patch("bilinear",{'P':face})
    face = [w,-h,-d,w,h,-d,w,-h,d,w,h,d]
    ri.Patch("bilinear",{'P':face})
    face = [w,-h,d,w,-h,-d,-w,-h,d,-w,-h,-d]
    ri.Patch("bilinear",{'P':face})
    face = [w,h,d,w,h,-d,-w,h,d,-w,h,-d]
    ri.Patch("bilinear",{'P':face})

def pinMainShape():

    ri.Patch("bilinear", {"P":(0.1,0,-0.1,0.1,-0.18,-0.09,0.1,0,0.1,0.1,-0.18,0.09)}) #OUTER FACE

    ri.Patch("bilinear", {"P":(0.1,0,-0.1,0.07,0,-0.1,0.1,-0.18,-0.09,0.07,-0.18,-0.09)}) #FRONT
    ri.Patch("bilinear", {"P":(0.1,0,0.1,0.07,0,0.1,0.1,-0.18,0.09,0.07,-0.18,0.09)}) #BACK
    ri.Patch("bilinear", {"P":(0.07,0,-0.1,0.07,-0.18,-0.09,0.07,0,0.1,0.07,-0.18,0.09)}) #INNER FACE
    ri.TransformBegin()
    ri.Rotate(90,0,-1,0)
    ri.Translate(0,-0.175,-0.085)
    ri.Scale(1,0.3,1)
    ri.Cylinder(0.09,-0.015,0.015,360)
    ri.TransformEnd()
    
    ri.TransformBegin()
    ri.Rotate(90,0,-1,0)
    ri.Translate(0,-0.175,-0.085)
    ri.Scale(1,0.3,1)
    ri.Disk(0.01,0.09,360)
    ri.Translate(0,0,-0.025)
    ri.Disk(0.01,0.09,360)
    ri.TransformEnd()

def pin():
#PINS START
    ri.TransformBegin()
    ri.Rotate(90,0,1,0)
    ri.Rotate(10,0,0,1)
    ri.Scale(0.5,0.5,0.5)
    ri.Translate(0.023,0.02,0)
    ri.Cylinder(0.07,-0.1,0.1,90)
    ri.Cylinder(0.038,-0.1,0.1,90)
    ri.Translate(-0.03,0,0)
    pinMainShape()
    ri.Scale(0.8,2,0.3)
    ri.Translate(0.02,-0.06,0)
    ri.Rotate(-20,0,0,1)
    pinMainShape()
    ri.TransformEnd()


#WORLD
ri.WorldBegin()

#MAIN TRANSFORMS

'''
#TOP VIEW
ri.Translate(0,0.01,1.7)
ri.Rotate(-90,1,0,0)
ri.Rotate(0,0,-1,0)
'''


#FINALS
ri.Translate(0,0.15,2.5)
ri.Rotate(-20,1,0,0)
ri.Rotate(-55,0,1,0)


'''
#SIDE
ri.Translate(-0.02,0.05,1.2)
ri.Rotate(-90,0,1,0)
ri.Rotate(10,0,0,1)
'''

'''
#BACK
ri.Translate(0.3,0.12,1)
ri.Rotate(-20,1,0,0)
ri.Rotate(-225,0,1,0)
'''

'''some shadows
ri.AttributeBegin()
ri.Rotate(90,0,1,0)
ri.Rotate(20,1,0,0)
ri.Light("PxrDistantLight","theLight3",{"float exposure":[1]})
ri.AttributeEnd()


ri.AttributeBegin()
ri.Scale(0.4,0.4,0.4)
ri.Translate(-10,6,0)
ri.Light("PxrSphereLight",1,{ri.HANDLEID:"sphereLight", "float exposure":[10]})
ri.AttributeEnd()
'''

#a LIGHT
ri.AttributeBegin()
ri.Rotate(-90,1,0,0)
ri.Light("PxrDomeLight", "theLight", {"string lightColorMap":"rectLight.tx"})
ri.AttributeEnd()

#FLOOR
ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0,-0.010,1)
ri.Pattern("PxrBump","tableScratch",{"string filename" : "nanotexture2.tx","float scale": 0.02})
ri.Bxdf( "PxrDisney","bxdf", {"color baseColor":(1.9,1.9,2), "reference normal bumpNormal" : ["tableScratch:resultN"],"float metallic" : 1,})
ri.Patch("bilinear",{"P":(-2,-0.2,-2,3,-0.2,-2,-2,-0.2,2,3,-0.2,2)})
ri.AttributeEnd()
ri.TransformEnd()

#CIRCUIT BOARD
ri.TransformBegin()
ri.AttributeBegin()
ri.Rotate(-70,0,1,0)
ri.Translate(1.5,-0.2,-1.5)
ri.Pattern("circuitMap","circuit")
ri.Bxdf("PxrDisney","bxdf",{"reference color baseColor":["circuit:Cout"]})
Cube(1.5,0.01,3)
ri.AttributeEnd()
ri.TransformEnd()

def chip():

    #-----------------------------------------------MAINBODY-------------------------------------------------
    ri.TransformBegin() #LEFT, TOP, BACK
    ri.Scale(1.03,0.07,0.3)
    ri.Translate(0,0.5,0)

    ri.AttributeBegin()
    ri.Attribute("displacementbound", {"sphere":0.5, "coordinatesystem":"shader"})
    ri.Pattern("topDisp","topDispTx") #DISPLACEMENT
    ri.Displace("PxrDisplace", "topDisplacement", {"float dispAmount":0.095, "reference float dispScalar":"topDispTx:resultF"})
    ri.Pattern("map","decal") #MAP
    ri.Bxdf("PxrDisney","bxdf",{"reference color baseColor":["decal:Cout"], "float roughness":[0.5]})
    #ri.ShadingRate(10)
    ri.Patch("bilinear", {"P":(0.48,0.457,0.285,0.48,0.457,-0.48,-0.48,0.457,0.285,-0.48,0.457,-0.48)}) #TOP
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheChip", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Patch("bilinear", {"P":(-0.5,-0.4,-0.51,-0.485,0.4,-0.483,-0.5,-0.4,0.31,-0.485,0.4,0.28)}) #LEFT
    ri.Patch("bilinear", {"P":(-0.495,-0.4,0.325,-0.481,0.41,0.298,0.5,-0.4,0.325,0.481,0.41,0.298)}) #BACK
    ri.AttributeEnd()

    ri.TransformEnd()

    #EDGES & CORNERS BEGIN
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheEdges", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Translate(0.003,0,-0.0033) #MAIN TRANSFORM FOR EDGES BEGIN

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,0.088)#L,H,W
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,0,1,0)
    ri.Translate(0.40959,0,0.12)
    ri.Scale(1,1,4.35)
    ri.Translate(-0.4976,0.0621,-0.028)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.099,0.099,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Scale(1,0.25,1)
    ri.Translate(-0.01095,0.075,0.0308)
    ri.Rotate(3.95,0,0,-1)
    ri.Rotate(88,1,0,0)
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.141)
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,1,0,0)
    ri.Translate(-0.5059,-0.1457,-0.032)
    ri.Rotate(15.4,0,-1,0)
    ri.Rotate(8.7,1,0,0)
    ri.Cylinder(0.005,-0.032,0.032,360)
    ri.TransformEnd()

    ri.AttributeEnd()
    ri.TransformEnd()
    #EDGES & CORNERS END

    ri.TransformBegin()
    ri.Rotate (180,0,1,0)
    ri.Translate(-0.001,0,0.0597)
    ri.TransformBegin() #LEFT, TOP, BACK
    ri.Scale(1.03,0.07,0.3)
    ri.Translate(0,0.5,0)
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheChip", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})

    ri.Patch("bilinear", {"P":(-0.5,-0.4,0.005,-0.485,0.4,0.006,-0.5,-0.4,0.31,-0.485,0.4,0.28)}) #RIGHT
    ri.Patch("bilinear", {"P":(-0.5,-0.4,-0.51,-0.485,0.4,-0.483,-0.5,-0.4,-0.21,-0.485,0.4,-0.21)}) #RIGHT

    #INWARD PIECES
    ri.Patch("bilinear", {"P":(-0.5,-0.4,0.005,-0.485,0.4,0.006,0,-0.4,0.005,0,0.4,0.006)})
    ri.TransformBegin()
    ri.Translate(0,0,-0.218)
    ri.Patch("bilinear", {"P":(-0.5,-0.4,0.009,-0.485,0.4,0.008,0,-0.4,0.009,0,0.4,0.008)})
    ri.TransformEnd()

    ri.Patch("bilinear", {"P":(-0.495,-0.4,0.325,-0.481,0.41,0.298,0.496,-0.4,0.328,0.481,0.41,0.298)}) #FRONT                                                           
    ri.AttributeEnd()
    ri.TransformEnd()

    #EDGES & CORNERS BEGIN

    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheEdges", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Translate(0.003,0,-0.0033) #MAIN TRANSFORM FOR EDGES BEGIN

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)

    ri.Cylinder(0.0025,0.0277,0.1,360)
    ri.Cylinder(0.0025,-0.0994,-0.0283,360)

    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,0.088)
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,0,1,0)
    ri.Translate(0.40959,0,0.12)
    ri.Scale(1,1,4.35)
    ri.Translate(-0.4976,0.0621,-0.028)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.099,0.099,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Scale(1,0.25,1)
    ri.Translate(-0.01095,0.075,0.0308)
    ri.Rotate(3.95,0,0,-1)
    ri.Rotate(88,1,0,0)
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.141)
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,1,0,0)
    ri.Translate(-0.5059,-0.1457,-0.032)
    ri.Rotate(15.4,0,-1,0)
    ri.Rotate(8.7,1,0,0)
    ri.Cylinder(0.005,-0.032,0.032,360)
    ri.TransformEnd()

    ri.AttributeEnd()
    ri.TransformEnd()
    #EDGES & CORNERS END

    ri.TransformEnd()
    #--------------------------------------------------UNDERSIDE-----------------------------------------------

    ri.TransformBegin()
    ri.Rotate(180,1,0,0)
    ri.Translate(0,0,0.06)

    ri.TransformBegin() #LEFT, TOP, BACK
    ri.Scale(1.03,0.07,0.3)
    ri.Translate(0,0.5,0)

    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheChip", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    
    ri.AttributeBegin()
    ri.Attribute("displacementbound", {"sphere":0.5, "coordinatesystem":"shader"})
    ri.Pattern("bottomDisp","bottomDispTx") #DISPLACEMENT
    ri.Displace("PxrDisplace", "bottomDisplacement", {"float dispAmount":0.095, "reference float dispScalar":"bottomDispTx:resultF"})
    ri.Patch("bilinear", {"P":(0.48,0.457,0.285,0.48,0.457,-0.48,-0.48,0.457,0.285,-0.48,0.457,-0.48)}) #TOP
    ri.AttributeEnd()

    ri.Patch("bilinear", {"P":(-0.5,-0.4,-0.51,-0.485,0.4,-0.483,-0.5,-0.4,0.31,-0.485,0.4,0.28)}) #LEFT
    ri.Patch("bilinear", {"P":(-0.495,-0.4,0.325,-0.481,0.41,0.298,0.5,-0.4,0.325,0.481,0.41,0.298)}) #BACK
    ri.AttributeEnd()

    ri.TransformEnd()

    #EDGES & CORNERS BEGIN
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheEdges", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Translate(0.003,0,-0.0033) #MAIN TRANSFORM FOR EDGES BEGIN

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,0.088)#L,H,W
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,0,1,0)
    ri.Translate(0.40959,0,0.12)
    ri.Scale(1,1,4.35)
    ri.Translate(-0.4976,0.0621,-0.028)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.099,0.099,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Scale(1,0.25,1)
    ri.Translate(-0.01095,0.075,0.0308)
    ri.Rotate(3.95,0,0,-1)
    ri.Rotate(88,1,0,0)
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.141)
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,1,0,0)
    ri.Translate(-0.5059,-0.1457,-0.032)
    ri.Rotate(15.4,0,-1,0)
    ri.Rotate(8.7,1,0,0)
    ri.Cylinder(0.005,-0.032,0.032,360)
    ri.TransformEnd()

    ri.AttributeEnd()
    ri.TransformEnd()
    #EDGES & CORNERS END

    ri.TransformBegin()
    ri.Rotate (180,0,1,0)
    ri.Translate(-0.001,0,0.0597)
    ri.TransformBegin() #LEFT, TOP, BACK
    ri.Scale(1.03,0.07,0.3)
    ri.Translate(0,0.5,0)
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheChip", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Patch("bilinear", {"P":(-0.5,-0.4,-0.51,-0.485,0.4,-0.483,-0.5,-0.4,0.31,-0.485,0.4,0.28)}) #RIGHT
    ri.Patch("bilinear", {"P":(-0.495,-0.4,0.325,-0.481,0.41,0.298,0.496,-0.4,0.328,0.481,0.41,0.298)}) #FRONT                                                           
    ri.AttributeEnd()
    ri.TransformEnd()

    #EDGES & CORNERS BEGIN

    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheEdges", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})
    ri.Translate(0.003,0,-0.0033) #MAIN TRANSFORM FOR EDGES BEGIN

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,0.088)#L,H,W
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,0,1,0)
    ri.Translate(0.40959,0,0.12)
    ri.Scale(1,1,4.35)
    ri.Translate(-0.4976,0.0621,-0.028)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.099,0.099,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Scale(1,0.25,1)
    ri.Translate(-0.01095,0.075,0.0308)
    ri.Rotate(3.95,0,0,-1)
    ri.Rotate(88,1,0,0)
    ri.Translate(-0.4976,0.0621,-0.027)
    ri.Scale(2,2,1.15)
    ri.Cylinder(0.0025,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-0.4976,0.0621,-0.141)
    ri.Sphere(0.005,-0.1,0.1,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(90,1,0,0)
    ri.Translate(-0.5059,-0.1457,-0.032)
    ri.Rotate(15.4,0,-1,0)
    ri.Rotate(8.7,1,0,0)
    ri.Cylinder(0.005,-0.032,0.032,360)
    ri.TransformEnd()

    ri.AttributeEnd()
    ri.TransformEnd()
    #EDGES & CORNERS END

    ri.TransformEnd()

    ri.TransformEnd()

    #---------------------------------------------MIDDLE PROTRUSIONS-------------------------------------------
    ri.TransformBegin()
    ri.Scale(1.01,0.7,0.75) #MAIN SCALE
    ri.Translate(0.005,0,0)
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheEdges", {"color baseColor":(0,0,0),  "float metallic":1, "float roughness":0.5})

    #LENGTH - EDGE
    ri.TransformBegin()
    ri.Scale(1,0.02,0.02)
    ri.Translate(0,0,6.6)
    Cube(1,1,1)
    ri.Translate(0,0,-17)
    Cube(1,1,1)
    ri.TransformEnd()

    #WIDTH - EDGE
    ri.TransformBegin()
    ri.Scale(0.03,0.02,0.23)
    ri.Translate(-16.85,0,0.065)
    Cube(1,1,1) #FRONT WIDTH
    ri.Scale(1,1,0.4)
    ri.Translate(0.2,0,-1.7)
    Cube(1,1,1)
    ri.Translate(32.73,0,1.15)
    ri.Scale(2.2,1,3.5)
    Cube(1,1,1)
    ri.TransformEnd()

    #ROUNDED CORNERS
    for i in range(0,4):
        ri.TransformBegin()
        ri.Scale(1,2,1)
        if (i == 0): 
            ri.Translate(0.495,0,0.122)
        elif (i == 1):
            ri.Translate(0.495,0,-0.198)
        elif (i == 2):
            ri.Translate(-0.5,0,0.122)
        elif (i == 3):
            ri.Translate(-0.5,0,-0.198)
        ri.Rotate(90,1,0,0)
        ri.Cylinder(0.02,-0.005,0.005,360)
        ri.Translate(0,0,-0.095)
        ri.Disk(0.1,0.02,360)
        ri.Translate(0,0,-0.01)
        ri.Disk(0.1,0.02,360)
        ri.TransformEnd()

    ri.AttributeEnd()
    ri.TransformEnd()
    #-------------------------------------------SHINY DISCS ON TOP--------------------------------------------------
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheDiscs", {"color baseColor":(0.0,0.0,0.0),  "float metallic":1, "float roughness":0})
    ri.Translate(-0.345,0.165,-0.03)
    ri.Rotate(90,1,0,0)
    ri.Disk(0.1,0.05,360)
    ri.Translate(0.693,0,-0.1)
    ri.Disk(0.2,0.05,360)
    ri.AttributeEnd()
    ri.TransformEnd()

    ri.TransformBegin()

    ri.Translate(0,-0.13,0)

    ri.AttributeBegin()
    ri.Bxdf("PxrDisney", "forTheDiscs", {"color baseColor":(0.0,0.0,0.0),  "float metallic":1, "float roughness":0})
    ri.Translate(-0.345,0.165,-0.03)
    ri.Rotate(90,1,0,0)
    ri.Disk(0.1,0.05,360)
    ri.Translate(0.693,0,-0.1)
    ri.Disk(0.2,0.05,360)
    ri.AttributeEnd()
    ri.TransformEnd()
    #-------------------------------------------------PINS-----------------------------------------------------------
    
    
    ri.TransformBegin()
    ri.Translate(-0.16,0.005,-0.026)
    ri.Scale(0.7,0.7,0.9)

    for i in range(0,9):
        ri.TransformBegin()
        ri.Scale(0.8,1,0.8)
        ri.Translate(-0.55,-0.04,-0.166)
        ri.AttributeBegin()
        ri.Pattern("PxrBump","pinNoise1",{"string filename" : "pinNoise1.tx","float scale": random.uniform(0.0, 0.1),"int invertT":i%2})
        ri.Bxdf("PxrDisney", "forThePins", {"color baseColor":(0.6,0.6,0.5), "reference normal bumpNormal" : ["pinNoise1:resultN"], "float metallic":1, "float roughness":0.2})
        pin()
        ri.AttributeEnd()
        ri.TransformEnd()
        ri.Translate(0.165,0,0)
        
    ri.Rotate(180,0,1,0)
    ri.Translate(1.09,0,0.005)

    for i in range(0,9):
        ri.TransformBegin()
        ri.Scale(0.8,1,0.8)
        ri.Translate(-0.55,-0.04,-0.165)
        ri.AttributeBegin()
        ri.Pattern("PxrBump","pinNoise1",{"string filename" : "pinNoise1.tx","float scale": random.uniform(0.0, 0.1),"int invertT":i%2})
        ri.Bxdf("PxrDisney", "forThePins", {"color baseColor":(0.6,0.6,0.5), "reference normal bumpNormal" : ["pinNoise1:resultN"], "float metallic":1, "float roughness":0.2})
        pin()
        ri.AttributeEnd()
        ri.TransformEnd()
        ri.Translate(0.16,0,0)

    ri.TransformEnd()

    ri.Bxdf("PxrDisney", "forThePins", {"color baseColor":(0.6,0.6,0.5),"float metallic":1, "float roughness":0.2})

    for i in range(0,9):
        ri.TransformBegin()
        ri.Rotate(90,0,1,0)
        ri.Translate(0.15,-0.015,-0.4955)
        ri.Scale(0.3,0.3,0.3)
        ri.Patch("bicubic",{"P":(0,0.045,0,0,0.075,0,0,0.085,0,0,0.081,0,
                            0.033,0.042,0,0.04,0.0693,0,0.045,0.0779,0,0.055,0.082,0,
                            0.052,0.0322,0,0.0693,0.04,0,0.0779,0.045,0,0.0866,0.05,0,
                            0.052,0,0,0.063,0,0,0.076,0,0,0.09,0,0)})
        ri.TransformEnd()
        ri.Translate(0.1155,0,0)

    for i in range(0,9):
        ri.TransformBegin()
        ri.Rotate(90,0,1,0)
        ri.Translate(0.15,-0.015,-1.48)
        ri.Scale(0.3,0.3,0.3)
        ri.Patch("bicubic",{"P":(0,0.045,0,0,0.075,0,0,0.085,0,0,0.081,0,
                            0.033,0.042,0,0.04,0.0693,0,0.045,0.0779,0,0.055,0.082,0,
                            0.052,0.0322,0,0.0693,0.04,0,0.0779,0.045,0,0.0866,0.05,0,
                            0.052,0,0,0.063,0,0,0.076,0,0,0.09,0,0)})
        ri.TransformEnd()
        ri.Translate(0.1155,0,0)

    ri.Transform

    for i in range(0,9):
        ri.TransformBegin()
        ri.Rotate(90,0,1,0)
        ri.Translate(0.15,-0.015,-0.4955)
        ri.Scale(0.3,0.3,0.3)
        ri.Patch("bicubic",{"P":(0,0.045,0,0,0.075,0,0,0.085,0,0,0.081,0,
                            0.033,0.042,0,0.04,0.0693,0,0.045,0.0779,0,0.055,0.082,0,
                            0.052,0.0322,0,0.0693,0.04,0,0.0779,0.045,0,0.0866,0.05,0,
                            0.052,0,0,0.063,0,0,0.076,0,0,0.09,0,0)})
        ri.TransformEnd()
        ri.Translate(0.1155,0,0)

    for i in range(0,9):
        ri.TransformBegin()
        ri.Rotate(90,0,1,0)
        ri.Translate(0.15,-0.015,-1.48)
        ri.Scale(0.3,0.3,0.3)
        ri.Patch("bicubic",{"P":(0,0.045,0,0,0.075,0,0,0.085,0,0,0.081,0,
                            0.033,0.042,0,0.04,0.0693,0,0.045,0.0779,0,0.055,0.082,0,
                            0.052,0.0322,0,0.0693,0.04,0,0.0779,0.045,0,0.0866,0.05,0,
                            0.052,0,0,0.063,0,0,0.076,0,0,0.09,0,0)})
        ri.TransformEnd()
        ri.Translate(0.1155,0,0)
#----------------------------------------------------------------------------------------------------------------
if (filename == "Chip_01.rib"):
    chip()
elif (filename == "Chip_02.rib"):
    ri.Translate(0.1,0,-0.1)#main transform
    ri.TransformBegin()
    ri.Translate(-0.2,0,0.25)
    ri.Rotate(-225,0,1,0)
    chip() #upright
    ri.TransformEnd()
    ri.TransformBegin()
    ri.Rotate(180,0,0,1)
    ri.Rotate(20,0,1,0)
    ri.Translate(0.1,0.14,-0.17)
    chip() #upsidedown
    ri.TransformEnd()

ri.WorldEnd()
ri.End()