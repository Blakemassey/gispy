# ---------------------------------------------------------------------------
# Blank Raster.py
# Created on: 2014-08-22
# Description: Creates a random raster, defines projection, and clips raster.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os

# Local variables:
out_folder = "C:\\ArcGIS\\Data\\BlankRaster"
out_name = "maine_30m.tif"

# Process: Create Random Raster
arcpy.CreateRandomRaster_management(out_folder, out_name, "INTEGER 1 10",
  "335000 4750000 668000 5257000", "30")
# THE EXTENT HERE IS CRITICAL

# Local variables:
in_file = os.path.join(out_folder, out_name)

# Process: Define Projection
arcpy.DefineProjection_management(in_file, """PROJCS['NAD_1983_UTM_Zone_19N',
GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',
SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],
UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],
PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],
PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],
PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]""")
print "Created: " + out_name + "and projection set to NAD 83 UTM Zone 19N."

# Local variables:
in_file = in_file
out_file = os.path.join(out_folder, "maine_30mc.tif")
clip_geometry = "C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline.shp"
print "Created: " + out_file

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000", out_file,
  clip_geometry, "255", "ClippingGeometry")
# MUST have a NoData Value (second to last parameter) in order to clip out
# polygon shape
print "Created: " + out_file