# ---------------------------------------------------------------------------
# Elevation.py
# Created on: 2015-10-25
# Description: Merges all rasters within a single folder into a new raster,
#   reprojects raster, resamples raster to 30m, clips raster, creates
#   hillshade, and then clips hillshade.
# ---------------------------------------------------------------------------

# Import Modules
import os
import arcpy
from arcpy import env

arcpy.env.workspace = "C:\\ArcGIS\\Data\\Elevation\\Elevation"
arcpy.env.overwriteOutput = 'True'

# Local variables
in_folder = "C:\\ArcGIS\\Data\\Elevation\\NED 1_3 Arc Second"
out_folder = arcpy.env.workspace
out_file = "elev_TEMP.tif"
folder_list = os.walk(os.path.join(in_folder,'.')).next()[1]

# Process: Create Directories and Files (using a for loop)
if not os.path.exists(out_folder): os.makedirs(out_folder)
folder_list = os.walk(os.path.join(in_folder,'.')).next()[1]
in_files=""
for i in folder_list:
 grd_i = 'grd' + i + '_13'
 in_files+= "'" + os.path.join(in_folder,i, grd_i) + "';"
 # single quotes and semicolon needed for "input_rasters" parameter

# Process: Mosaic To New Raster
arcpy.MosaicToNewRaster_management(in_files, out_folder, out_file, "",
  "16_BIT_UNSIGNED", "", "1", "BLEND", "FIRST")
file_count = len(folder_list)
out_path = os.path.join(out_folder, out_file)
print  "Finished moasaicking " + str(file_count) + " files into: " + "'" + \
  out_path + "'"

# Local variables
in_file = os.path.join(out_folder, out_file)
out_file = os.path.join(out_folder,'elev_5m.tif')

# Process: Project Raster
arcpy.ProjectRaster_management(in_file, out_file,
"""PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',
DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],
PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],
PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],
PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],
PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],
UNIT['Meter',1.0]]""", "BILINEAR", "5", "", "335000 4750000",
"""GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',
SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],
UNIT['Degree',0.0174532925199433]],VERTCS['Unknown VCS',VDATUM['Unknown'],
PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],
UNIT['Meter',1.0]]""")
# The fourth parameter down (e.g. "5") is where the cell size is determined
os.remove(in_file) # removes non-projected file
print "Created: " + out_file

# Local variables:
in_file = out_file
out_file = os.path.join(out_folder, "elev_30m.tif")
cell_size = "30"

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Set Geoprocessing environments
arcpy.env.snapRaster = "C:\\ArcGIS\\Data\\BlankRaster\\maine_30m.tif"

# Process: Resample
arcpy.Resample_management(in_file, out_file, cell_size, "NEAREST")
print "Created: " + out_file

# Local variables:
in_file = out_file
clip_geometry = "C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline.shp"
out_file = os.path.join(out_folder, "elev_30mc.tif")

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000", out_file,
  clip_geometry, "-999", "ClippingGeometry")
print "Created: " + out_file

# Local variables:
in_file = os.path.join(out_folder, "elev_30m.tif")
out_file = os.path.join(out_folder, "hillsh_30m")

# Process: Hillshade
arcpy.gp.HillShade_sa(in_file, out_file, "315", "45", "NO_SHADOWS", "1")
print "Created: " + out_file

# Local variables:
in_file = os.path.join(out_folder, "elev_30mc.tif")
out_file = os.path.join(out_folder, "hillsh_30mc")

# Process: Hillshade
arcpy.gp.HillShade_sa(in_file, out_file, "315", "45", "NO_SHADOWS", "1")
print "Created: " + out_file
