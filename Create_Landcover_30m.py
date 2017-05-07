# ---------------------------------------------------------------------------
# Landcover.py
# Created on: 2015-10-25
# Description: Combines several rasters into a new raster, reprojects the new
#   raster, resamples raster to 30m cells, then clips raster to MaineOutline.
# ---------------------------------------------------------------------------

# Import Modules
import arcpy
import os

# Local variables:
N42W066 = "C:/ArcGIS/Data/Landcover/NLCD2011_LC_N42W066/NLCD2011_LC_N42W066.tif"
N42W069 = "C:/ArcGIS/Data/Landcover/NLCD2011_LC_N42W069/NLCD2011_LC_N42W069.tif"
N45W066 = "C:/ArcGIS/Data/Landcover/NLCD2011_LC_N45W066/NLCD2011_LC_N45W066.tif"
N45W069 = "C:/ArcGIS/Data/Landcover/NLCD2011_LC_N45W069/NLCD2011_LC_N45W069.tif"
in_files = "'" + N42W066 + "';'" + N42W069 + "';'" + N45W066 + "';'" + \
  N45W069 + "'"
out_folder = "C:\\ArcGIS\\Data\\Landcover\\Landcover"
out_file = "lc_TEMP.tif"

# Process: Mosaic To New Raster
if not os.path.exists(out_folder): os.makedirs(out_folder)
arcpy.MosaicToNewRaster_management(in_files, out_folder, out_file, "",
  "8_BIT_UNSIGNED", "", "1", "LAST", "MATCH")

# Local variables:
in_file = os.path.join(out_folder, out_file)
out_file = os.path.join(out_folder, "lc30m.tif")

# Process: Project Raster
arcpy.ProjectRaster_management(in_file, out_file,
"""PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',
DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],
PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],
PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],
PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],
PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],
UNIT['Meter',1.0]]""", "NEAREST", "30", "", "335000 4750000", \
"""PROJCS['Albers_Conical_Equal_Area',GEOGCS['GCS_North_American_1983',
DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],
PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],
PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],
PARAMETER['central_meridian',-96.0],PARAMETER['standard_parallel_1',29.5],
PARAMETER['standard_parallel_2',45.5],PARAMETER['latitude_of_origin',23.0],
UNIT['Meter',1.0]]""")
os.remove(in_file) # removes non-projected file
print "Created: " + out_file

# Local variables:
in_file = out_file
out_file = os.path.join(out_folder, "lc_30m.tif")
cell_size = "30"

# Set Geoprocessing environments
arcpy.env.snapRaster = "C:\\ArcGIS\\Data\\BlankRaster\\maine_30m.tif"

# Process: Resample
arcpy.Resample_management(in_file, out_file, cell_size, "NEAREST")
print "Created: " + out_file

# Local variables:
in_file = out_file
clip_geometry = "C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline.shp"
out_file = os.path.join(out_folder, "lc_30mc.tif")

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000", out_file,
  clip_geometry, "", "ClippingGeometry")
print "Created: " + out_file