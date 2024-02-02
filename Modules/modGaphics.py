from matplotlib.collections import PatchCollection
from typing import List, Union

import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

def create_hex_grid(nx: int = 4,
					ny: int = 5,
					min_diam: float = 1,
					n: int = 0,
					align_to_origin: bool = True,
					face_color: Union[List[float], str] = None,
					edge_color: Union[List[float], str] = None,
					plotting_gap: float = 0.,
					crop_circ: float = 0.,
					do_plot: bool = False,
					rotate_deg: float = 0.,
					keep_x_sym: bool = True,
					h_ax: plt.Axes = None,
					line_width: float = 0.2,
					background_color: Union[List[float], str] = None) -> (np.ndarray, plt.Axes):
	"""
	Creates and prints hexagonal lattices.
	:param nx: Number of horizontal hexagons in rectangular grid, [nx * ny]
	:param ny: Number of vertical hexagons in rectangular grid, [nx * ny]
	:param min_diam: Minimal diameter of each hexagon.
	:param n: Alternative way to create rectangular grid. The final grid might have less hexagons
	:param align_to_origin: Shift the grid s.t. the central tile will center at the origin
	:param face_color: Provide RGB triplet, valid abbreviation (e.g. 'k') or RGB+alpha
	:param edge_color: Provide RGB triplet, valid abbreviation (e.g. 'k') or RGB+alpha
	:param plotting_gap: Gap between the edges of adjacent tiles, in fraction of min_diam
	:param crop_circ: Disabled if 0. If >0 a circle of central tiles will be kept, with radius r=crop_circ
	:param do_plot: Add the hexagon to an axes. If h_ax not provided a new figure will be opened.
	:param rotate_deg: Rotate the grid around the center of the central tile, by rotate_deg degrees
	:param keep_x_sym: NOT YET IMPLEMENTED
	:param h_ax: Handle to axes. If provided the grid will be added to it, if not a new figure will be opened.
	:param line_width: The width of the hexagon lines
	:param background_color: The color of the axis background
	:return:
	"""
	
	coord_x, coord_y = make_grid(nx, ny, min_diam, n, crop_circ, rotate_deg, align_to_origin)

	return np.hstack([coord_x, coord_y]), h_ax

def make_grid(nx, ny, min_diam, n, crop_circ, rotate_deg, align_to_origin) -> (np.ndarray, np.ndarray):
	"""
	Computes the coordinates of the hexagon centers, given the size rotation and layout specifications
	:return:
	"""
	ratio = np.sqrt(3) / 2
	if n > 0:  # n variable overwrites (nx, ny) in case all three were provided
		ny = int(np.sqrt(n / ratio))
		nx = n // ny

	coord_x, coord_y = np.meshgrid(np.arange(nx), np.arange(ny), sparse=False, indexing='xy')
	coord_y = coord_y * ratio
	coord_x = coord_x.astype('float')
	coord_x[1::2, :] += 0.5
	coord_x = coord_x.reshape(-1, 1)
	coord_y = coord_y.reshape(-1, 1)

	coord_x *= min_diam  # Scale to requested size
	coord_y = coord_y.astype('float') * min_diam

	mid_x = (np.ceil(nx / 2) - 1) + 0.5 * (np.ceil(ny/2) % 2 == 0)  # Pick center of some hexagon as origin for rotation or crop...
	mid_y = (np.ceil(ny / 2) - 1) * ratio  # np.median() averages center 2 values for even arrays :\
	mid_x *= min_diam
	mid_y *= min_diam

	if crop_circ > 0:
		rad = ((coord_x - mid_x)*2 + (coord_y - mid_y)*2)*0.5
		coord_x = coord_x[rad.flatten() <= crop_circ, :]
		coord_y = coord_y[rad.flatten() <= crop_circ, :]

	if not np.isclose(rotate_deg, 0):  # Check if rotation is not 0, with tolerance due to float format
		# Clockwise, 2D rotation matrix
		RotMatrix = np.array([[np.cos(np.deg2rad(rotate_deg)), np.sin(np.deg2rad(rotate_deg))],
							[-np.sin(np.deg2rad(rotate_deg)), np.cos(np.deg2rad(rotate_deg))]])
		rot_locs = np.hstack((coord_x - mid_x, coord_y - mid_y)) @ RotMatrix.T
		# rot_locs = np.hstack((coord_x - mid_x, coord_y - mid_y))
		coord_x, coord_y = np.hsplit(rot_locs + np.array([mid_x, mid_y]), 2)

	if align_to_origin:
		coord_x -= mid_x
		coord_y -= mid_y

	return coord_x, coord_y



if __name__ == "__main__":

	# Parameters
	x_dim = 10
	y_dim = 10
	diam = 1
	frames = 100
		
	figure, axs = plt.subplots()

	# Compute hexagon centers
	centers, _ = create_hex_grid(nx = x_dim, ny = y_dim, min_diam = diam)
	
	# Create hexagons
	polygons = [mpatches.RegularPolygon((x, y), numVertices = 6, radius = diam / np.sqrt(3)) for x, y in zip(centers[:, 0], centers[:, 1])]
	collection = PatchCollection(polygons)
	axs.add_collection(collection)
	
	# Set axis properties (diam size)
	axs.set_aspect('equal')
	axs.axis([
		centers[:, 0].min() - 2 * diam,
		centers[:, 0].max() + 2 * diam,
		centers[:, 1].min() - 2 * diam,
        centers[:, 1].max() + 2 * diam,
	])
	
	# Animate
	ani = animation.FuncAnimation(figure, func = update, frames = frames)
	plt.show()