import sys, pygame
from random import randint as rng
from math import sqrt,exp,radians,sin,cos
import os.path
from repelers import repelers

def sigmoid(x):return 1/(1+exp(-x))

def vecLen(vec):return sqrt(vec[0]**2+vec[1]**2)
def vec3Len(vec):return sqrt(vec[0]**2+vec[1]**2+vec[2]**2)
def vecDif(vecA,vecB):return [vecA[0]-vecB[0],vecA[1]-vecB[1]]
def vec3MulSc(vec,sc):return [vec[0]*sc,vec[1]*sc,vec[2]*sc]
def vecUnit(vec):
	vl=vecLen(vec)
	return [vec[0]/vl,vec[1]/vl]
def vec3Unit(vec):
	vl=vec3Len(vec)
	return [vec[0]/vl,vec[1]/vl,vec[2]/vl]
def rngClr(mx,alpha):
	clr=[rng(0, 255), rng(0, 255), rng(0, 255)]
	clr=vec3Unit(clr)
	clr=vec3MulSc(clr,mx)
	return clr+[alpha]
szx=4720;szy=1600;nAgents=10000;nReps=1000;
#szx=800;szy=600;nAgents=1000;nReps=20;
pygame.init()

size = width, height = szx,szy
rect=(0,0,width,height)
white=(255,255,255)
black=(0,0,0)
red=(255,0,0,10)
win=pygame.display.set_mode(size)
win.fill(white)
fname='image.png'
if os.path.isfile(fname):
	image=pygame.image.load(fname)
	win.blit(image, (0, 0))
agents=[[rng(0,width),rng(0,height)]for i in range(nAgents)]
agentsClr=[rngClr(200,10) for i in range(nAgents)]
agentsAge=[0 for i in range(nAgents)]
if len(repelers)==0:
	repelers=[[rng(0,width),rng(0,height),rng(10,200)]for i in range(nReps)]
'''
repelers=[]
for j in range(10):
	sz=rng(10,100)
	x=rng(20,width-20)
	y = rng(20, height-20)
	for i in range(20):
		repelers.append([sin(radians(i*36))*sz+x,cos(radians(i*sz))*sz+y,sz])'''
repeler=[width//2,height//2]
run=True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:run=False
	shape_surf=pygame.Surface(pygame.Rect(rect).size,pygame.SRCALPHA)
	for i in range(len(agents)):
		repeler=[(agents[i][0]-width/2)/width,(agents[i][1]-height/2)/height]
		vl=vecLen(repeler)*1.5
		repeler=[repeler[0]/vl,repeler[1]/vl]
		vel=[0,0]
		vel[0]=rng(-1,1)/10+repeler[0]
		vel[1]=rng(-1,1)/10+repeler[1]
		for j in range(len(repelers)):
			if abs(agents[i][0]-repelers[j][0])<repelers[j][2] and abs(agents[i][1]-repelers[j][1])<repelers[j][2]:
				dist=vecLen(vecDif(agents[i],repelers[j]))
				if dist<repelers[j][2]:
					rep=[agents[i][0] - repelers[j][0], agents[i][1] - repelers[j][1] ]
					vlr=vecLen(rep)
					if vlr == 0: vlr = 0.0001
					inrem=sigmoid(repelers[j][2]/5-vlr)+(repelers[j][2]-vlr)/200
					if inrem==0:inrem=0.0001
					rep = [rep[0] / vlr*inrem, rep[1] / vlr*inrem]
					vel[0] +=rep[0]
					vel[1] +=rep[1]
		vel=vecUnit(vel)
		agents[i][0]+=vel[0]
		agents[i][1]+=vel[1]
		if agents[i][0]<0 or agents[i][0]>width or agents[i][1]<0 or agents[i][1]>height or agentsAge[i]>szx:
			agents[i]=[rng(0,width),rng(0,height)]
			agentsAge[i]=0
		else:agentsAge[i]+=1
		pygame.draw.circle(shape_surf,agentsClr[i],agents[i], 1)
	win.blit(shape_surf,rect)
	pygame.display.flip()

pygame.image.save(win, "image.png")
with open("repelers.py",'w') as file:
	file.write('repelers='+str(repelers))
sys.exit()