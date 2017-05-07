# ---------------------------------------------------------------------------
# Blank Polygon.py
# Created on: 2014-08-21
# Description: Create a blank polygon shapefile from the boundary of Maine,
#  reprojects shapefile to UTM 19N, and then create a 10km buffered version
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Local variables:
in_file ="C:\\ArcGIS\\Data\\Boundaries\\USGS_NBD_Maine\\GU_StateOrTerritory.shp"
out_file ="C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline.shp"

# Process: Project
arcpy.Project_management(in_file, out_file,"""PROJCS['NAD_1983_UTM_Zone_19N',
GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',
SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],
UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],
PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],
PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],
PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]""", "",
"""GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',
SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],
UNIT['Degree',0.0174532925199433]]""")
print "Created: " + out_file

# Local variables:
in_file = out_file
out_file = "C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline_Buffer_10km.shp"

# Process: Buffer
arcpy.Buffer_analysis(in_file, out_file, "10 Kilometers", "FULL", "ROUND",
  "NONE", "")
print "Created: " + out_file