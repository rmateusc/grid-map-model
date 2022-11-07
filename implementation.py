import geopandas as gpd

from utils import (
    unbounded_grid,
    bounded_grid,
    geometry_union,
    plot_map_grid,
    plot_map_points,
    create_randpoints,
    create_geom_points
)

# Load data
# Complete Bello map
bello_map = gpd.read_file('maps/BELLO_MAPA/bello_map.shp')
# Bello map divided by neighborhoods
veredas = gpd.read_file('maps/BELLO_VEREDAS/bello_veredas.shp')

# Create an unbounded grid according to the map
bello_unbnd_grid = unbounded_grid(bello_map, n_cells=100)
# Plot the previously unbounded grid
plot_map_grid(bello_map, bello_unbnd_grid)

# Bound the grid according to the map
grid_bounded = bounded_grid(bello_map, bello_unbnd_grid)
# Plot the bounded grid
plot_map_grid(bello_map, grid_bounded)
