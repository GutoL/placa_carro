import cv2
import numpy as np

def opencv(nome):
	img = cv2.imread(nome)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


	edges = cv2.Canny(gray,100,200,apertureSize = 3)
	#cv2.imshow('edges',edges)
	#cv2.waitKey(0)

	minLineLength = 50
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges,1,np.pi/2,50,minLineLength,maxLineGap)
	#print lines.shape
	
	lines = lines[0]
	

	coefficients, indices_out = findEquationLine(lines,img) #lines, img


	'''print 'numero linhas:%i'%len(lines)
	print 'numero indices: %i'%len(indices_out)
	print 'sub: %i'%(len(lines) - len(indices_out))'''

	lines = remove_lines(lines,indices_out)

	#print 'linhas: %i coe: %i'%(len(lines),len(coefficients))

	#print "numero linhas: %i "%len(lines)

	parallels = findParalell(coefficients)

	perpendicular = findPerpendicular(coefficients,parallels)
	print len(perpendicular)
	'''for x in xrange(len(parallels)):
		#print coefficients[parallels[x][0]]
		#print coefficients[parallels[x][1]]
		print lines[(parallels[x][0])]
		print lines[(parallels[x][1])]
		print "--"'''
	
	for x in xrange(len(parallels)):
		v1 = lines[(parallels[x][0])]
		v2 = lines[(parallels[x][1])]
		#print 'p1: %i p2: %i'%((parallels[x][0]),(parallels[x][1]))
		cv2.line(img,(v1[0],v1[1]),(v1[2],v1[3]),(255,0,0),3)
		cv2.line(img,(v2[0],v2[1]),(v2[2],v2[3]),(0,255,0),3)

	cv2.imshow('hough2',img)
	cv2.waitKey(0)
	
	#retangulo = lines[parallels[0][0]]
	#print retangulo[0]
	#roi = img[retangulo[1]:retangulo[3]+20,retangulo[0]:retangulo[2]]
	#print roi
	#roi = img[10:400,0:200]
	#cv2.imshow('roi',roi)
	#cv2.waitKey(0)

def findPerpendicular(coefficients,parallels):
	perpendicular = []
	

	for x in xrange(len(coefficients)):
		for y in parallels:
			#print coefficients[y[0]]
			if coefficients[x] != 0 and coefficients[y[0]] == (1.0/coefficients[x]):
				temp = []
				temp.append(y)
				temp.append(x)
				perpendicular.append(temp)
	return perpendicular


def remove_lines(lines,indices_out):

	i = 0
	for x in indices_out:
		lines = np.delete(lines,x-i,axis=0)
		i = i + 1
	return lines

def findParalell(coefficients):

	parallel = []
	
	for x in xrange(len(coefficients)):
		for i in xrange(len(coefficients)):
			if x != i:
				if coefficients[x] == coefficients[i]:
					temp = []
					temp.append(x)
					temp.append(i)
					parallel.append(temp)
		
	#print len(parallel)
	parallel = removeEquals(parallel)
	#print len(parallel)
	return parallel

def removeEquals(parallels):
	new = parallels
	for x in parallels:
		temp = invert(x)
		if temp in new:
			new.remove(temp)
	return new

def invert(lista):
	new = []
	for x in reversed(lista):
		new.append(x)
	return new

def findEquationLine(lines,img):#lines,img
	
	m = []
	i = 0
	indice = []


	for x1,y1,x2,y2 in lines:
		#cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
		if (float(x2)-float(x1)) != 0:
			#print float((float(y2) - float(y1))/(float(x2)-float(x1)))
			#print "y2: %f y1: %f x1: %f x2: %f"%(y2,y1,x2,x1)
			m.append(float((float(y2) - float(y1))/(float(x2)-float(x1))))
		else:
			indice.append(i)
		i = i+1

	#cv2.imshow('hough1',img)
	#cv2.waitKey(0)
	return m, indice


def main():

	opencv('images/placa8.jpg')
	'''arr = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
	print arr
	arr = np.delete(arr, 1, 0)
	print '--'
	print arr'''

if __name__ == '__main__':
	main()