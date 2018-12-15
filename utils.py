"""
General utilities
"""

import numpy as np


def rotX(theta, mode = 'radians'):
	"""Generate a rotation matrix that rotates a point by an angle theta about the X-axis.

	By default, assumes that the angle is passed in ``radians``.

	Args:
		theta (float): angle of rotation (by default, in ``radians``)
		mode (:obj:`str`, optional): one of ``radians`` or ``degrees``

	Returns:
		R (:obj:`np.matrix`): 3 x 3 rotation matrix about the X-axis

	Examples:
		>>> R = rotX(np.pi/2)
		>>> R = rotX(90, mode = 'degrees')
	"""

	if mode != 'radians' and mode != 'degrees':
		raise ValueError('Mode should either be ``radians`` or ``degrees``.')
	if mode == 'degrees':
		theta = np.deg2rad(theta)
	return np.matrix([[1., 0., 0.], [0, np.cos(theta), -np.sin(theta)], \
		[0, np.sin(theta), np.cos(theta)]])


def rotY(theta, mode = 'radians'):
	"""Generate a rotation matrix that rotates a point by an angle theta about the Y-axis.

	By default, assumes that the angle is passed in ``radians``.

	Args:
		theta (float): angle of rotation (by default, in ``radians``)
		mode (:obj:`str`, optional): one of ``radians`` or ``degrees``

	Returns:
		R (:obj:`np.matrix`): 3 x 3 rotation matrix about the Y-axis

	Examples:
		>>> R = rotY(np.pi/2)
		>>> R = rotY(90, mode = 'degrees')
	"""

	if mode != 'radians' and mode != 'degrees':
		raise ValueError('Mode should either be ``radians`` or ``degrees``.')
	if mode == 'degrees':
		theta = np.deg2rad(theta)
	return np.matrix([[np.cos(theta), 0., np.sin(theta)], [0, 1, 0], \
		[-np.sin(theta), 0, np.cos(theta)]])


def rotZ(theta, mode = 'radians'):
	"""Generate a rotation matrix that rotates a point by an angle theta about the Z-axis.

	By default, assumes that the angle is passed in ``radians``.

	Args:
		theta (float): angle of rotation (by default, in ``radians``)
		mode (:obj:`str`, optional): one of ``radians`` or ``degrees``

	Returns:
		R (:obj:`np.matrix`): 3 x 3 rotation matrix about the Z-axis

	Examples:
		>>> R = rotZ(np.pi/2)
		>>> R = rotZ(90, mode = 'degrees')
	"""

	if mode != 'radians' and mode != 'degrees':
		raise ValueError('Mode should either be ``radians`` or ``degrees``.')
	if mode == 'degrees':
		theta = np.deg2rad(theta)
	return np.matrix([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], \
		[0., 0., 1.]])



def getDistinguishableColors(numColors, bgColors = [(1, 1, 1)]):
	"""Pick a set of `numColors` colors that are maximally perceptually distinct.

	When plotting a set of lines/curves/points, you might want to distinguish them 
	by color. This module generates a set of colors that are ``maximally perceptually 
	distinguishable`` in the RGB colorspace. Given an initial seed list of candidate colors, 
	it iteratively picks the color from the list that is the farthest (in the RGB colorspace) 
	from all previously chosen entries. This is a ``greedy`` method and does not yield 
	a global maximum.

	Inspired by the MATLAB implementation from Timothy E. Holy.

	Args: 
		numColors (int): number of distinguishable colors to generate
		bgColors (:obj:`list`, optional): list of background colors	

	Returns:
		colors (:obj:`list`): list of `numColors` distinguishable colors

	Examples:
		>>> colors = getDistinguishableColors(25)
	"""

	# Start out by generating a sizeable number of RGB triples. This represents our space 
	# of possible choices. By starting out in the RGB space, we ensure that all of the colors 
	# can be generated by the monitor.

	# Number of grid divisions along each axis in RGB space
	numGrid = 30
	x = np.linspace(0, 1, numGrid)
	[R, G, B] = np.meshgrid(x, x, x)
	rgb = np.concatenate((R.T.reshape((numGrid*numGrid*numGrid, 1)), \
		G.T.reshape((numGrid*numGrid*numGrid, 1)), \
		B.T.reshape((numGrid*numGrid*numGrid, 1))), axis = 1)
	if numColors > rgb.shape[0] / 3:
		raise ValueError('You cannot really distinguish that many colors! At most 9000 colors')

	# If the user specified multiple bgColors, compute distance from the candidate colors
	# to the background colors.
	mindist = np.full(rgb.shape[0], np.inf)
	for c in bgColors:
		col = np.full(rgb.shape, 1)
		col[:,0] = c[0]
		col[:,1] = c[1]
		col[:,2] = c[2]
		dx = np.sum(np.abs(rgb - col), axis = 1)
		mindist = np.minimum(mindist, dx)

	# Initialize a list of colors
	colors = []
	lastColor = bgColors[-1]
	for i in range(numColors):
		col = np.full(rgb.shape, 1)
		col[:,0] = lastColor[0]
		col[:,1] = lastColor[1]
		col[:,2] = lastColor[2]
		dx = np.sum(np.abs(rgb - lastColor), axis = 1)
		mindist = np.minimum(mindist, dx)
		index = np.argmax(mindist)
		chosenColor = (rgb[index,0], rgb[index,1], rgb[index,2])
		colors.append(chosenColor)
		lastColor = chosenColor

	return colors