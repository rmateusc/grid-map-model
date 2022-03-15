import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon, Point
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import random


# # 2. Create grid

# Creates a square grid according to a map
def square_grid(shapefile, n_cells=30):
    # define bounds
    xmin, ymin, xmax, ymax = shapefile.total_bounds
    
    cell_size = (xmax-xmin)/n_cells

    grid_cells = []
    for x0 in np.arange(xmin, xmax+cell_size, cell_size):
        for y0 in np.arange(ymin, ymax+cell_size, cell_size):
            # bounds
            x1 = x0-cell_size
            y1 = y0+cell_size
            grid_cells.append( shapely.geometry.box(x0, y0, x1, y1)  )
    cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'])
    return cell


# In[6]:


# Bounds square grid according to map
def bounded_grid(shapefile, cells):
    grid = cells.copy()
    # Check if grid cell inside map
    in_shape = []
    a = shapefile.geometry.values
    for i in range(len(grid)):
        b = grid.iloc[i].values
        in_shape.append(a.contains(b)[0])
        
    # Add new column with boolean
    grid['in_map'] = in_shape
    
    # Only use grid cells that are within the map
    bounded = grid[grid.in_map==True].copy()
    return bounded


# In[7]:


# Create 
def geometry_union(gdf):
    # Create a multipolygon from various polygons
    multipol = gdf.geometry.unary_union
    
    # Unify into one multipolygon
    full_polygon = gpd.GeoDataFrame(geometry=[multipol], crs=gdf.crs)
    
    return full_polygon


# # Plotting Functions

# In[8]:


# Plot grid and map
def plot_map_grid(mapa, grid, figsize=(7, 7)):
    # Plot map
    ax = mapa.plot(color='none', edgecolor='red', markersize=.1, figsize=figsize)
    # Plot grid
    grid.plot(ax=ax, facecolor="none", edgecolor='grey')
    # Show plot
    plt.show()


# In[9]:


# Plot map and points
def plot_map_points(mapa, points, figsize=(7, 7)):
    # Plot map
    ax = mapa.plot(color='none', edgecolor='black', linewidth=2, figsize=figsize)
    # Plot points
    points.plot(ax=ax, color='red', markersize=2)
    # Show plots
    plt.show()


# # Point Generator

# In[10]:


# Create random points inside bounds
def create_randpoints(shapefile, N):
    
    # Define bounds
    xmin=shapefile.geometry.bounds.minx
    ymin=shapefile.geometry.bounds.miny
    xmax=shapefile.geometry.bounds.maxx
    ymax=shapefile.geometry.bounds.maxy
    
    #Empty DataFrame
    random_points = pd.DataFrame()
    
    #Empty lists
    random_x=[]
    random_y=[]

    while len(random_x)<N:
        xrand = random.uniform(xmin, xmax)
        yrand = random.uniform(ymin, ymax)
        point = Point(xrand.values[0], yrand.values[0])
        
        # Check if point is inside shapefile
        if shapefile.geometry.contains(point).values[0]==True:
            random_x.append(xrand.values[0])
            random_y.append(yrand.values[0])

    random_points['x']=random_x
    random_points['y']=random_y
    return random_points


# In[11]:


# Join coordinates with Point geometry
def create_geom_points(random_points):
    return gpd.GeoDataFrame(random_points, geometry=gpd.points_from_xy(random_points.x, random_points.y))  
