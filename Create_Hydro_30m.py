# ---------------------------------------------------------------------------
# Create_Hydro_30m.py
# Created on: 2015-10-25
# Description: Merges NHDArea and NHDWaterbody into a new polygon shapefile,
#   reprojects shapefile, convert shapefile to a raster, resamples raster to
#   30m, and clips raster to MaineOutline
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os

# Local variables:
Area = "C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea"
Waterbody ="C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody"
in_files = "'" + Area + "';'" + Waterbody + "'"
out_folder = "C:\\ArcGIS\\Data\\Hydrology\\NHD_shapefiles\\"
out_file = os.path.join(out_folder,"Hydro_Merge_TEMP.shp")

### Process: Merge
##if not os.path.exists(out_folder): os.makedirs(out_folder)
##arcpy.Merge_management(in_files, out_file, """Permanent_ \"Permanent_\" true
## false false 40 Text 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,
## Permanent_Identifier,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,
## Permanent_Identifier,-1,-1;FDate \"FDate\" true false false 8 Date 0 0 ,First,
## #,C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,FDate,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,FDate,-1,
## -1;Resolution \"Resolution\" true false false 4 Long 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,Resolution,-1,
## -1,C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,
## Resolution,-1,-1;GNIS_ID \"GNIS_ID\" true true false 10 Text 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,GNIS_ID,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,GNIS_ID,-1,
## -1;GNIS_Name \"GNIS_Name\" true true false 65 Text 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,GNIS_Name,-1,
## -1,C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,
## GNIS_Name,-1,-1;AreaSqKm \"AreaSqKm\" true true false 8 Double 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,AreaSqKm,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,AreaSqKm,
## -1,-1;Elevation \"Elevation\" true true false 8 Double 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,Elevation,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,Elevation,
## -1,-1;FType \"FType\" true false false 4 Long 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,FType,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,FType,-1,
## -1;FCode \"FCode\" true true false 4 Long 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,FCode,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,FCode,-1,
## -1;Shape_Leng \"Shape_Length\" false true true 8 Double 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,Shape_Length,
## -1,-1,C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,
## Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0 ,
## First,#,C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDArea,
## Shape_Area,-1,-1,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,Shape_Area,
## -1,-1;ReachCode \"ReachCode\" true true false 14 Text 0 0 ,First,#,
## C:\\ArcGIS\\Data\\Hydrology\\NHDH_ME.gdb\\Hydrography\\NHDWaterbody,
## ReachCode,-1,-1""")

### Local variables:
##in_file = out_file
##out_file = os.path.join(out_folder,"Hydro_Merge.shp")
##
### Process: Project -- is projected here so cell size can be set in the next process
##arcpy.Project_management(in_file, out_file,
##"""PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',
##DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],
##PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],
##PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],
##PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],
##PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],
##UNIT['Meter',1.0]]""", "",
##"""GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',
##SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],
##UNIT['Degree',0.0174532925199433]]""")
##
##os.remove(in_file) # removes non-projected file
##print "Created: " + out_file

# Local variables:
from arcpy import env
arcpy.env.workspace = "C:\\ArcGIS\\Data\\Hydrology\\NHD_rasters\\"
arcpy.env.overwriteOutput = 'True'

in_file = out_file
out_folder = arcpy.env.workspace
out_file = os.path.join(out_folder,"hydro5m.tif")
##
### Process: Polygon to Raster
##if not os.path.exists(out_folder): os.makedirs(out_folder)
##arcpy.PolygonToRaster_conversion(in_file, "FCode", out_file,
##  "MAXIMUM_COMBINED_AREA", "FCODE", "5")
##print "Created: " + out_file
### Cell size is set by last parameter (e.g., "5")

# Local Variables
in_file = out_file
out_file = os.path.join(out_folder,"hydro_30m.tif")

# Set Geoprocessing environments
arcpy.env.snapRaster = "C:\\ArcGIS\\Data\\BlankRaster\\maine_30m.tif"

### Process: Resample
##arcpy.Resample_management(in_file, out_file, "30 30", "MAJORITY")
##print "Created: " + out_file

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables:
in_file = out_file
out_file_dist = os.path.join(out_folder, "hydro_dist_30m.tif")
out_file_direction = os.path.join(out_folder, "hydro_dir_30m.tif")

# Process: Euclidean Distance
arcpy.gp.EucDistance_sa(in_file, out_file_dist, "", "30", out_file_direction)

# Local variables:
in_file = os.path.join(out_folder, "hydro_30m.tif")
clip_geometry = "C:\\ArcGIS\\Data\\BlankPolygon\\MaineOutline.shp"
out_file = os.path.join(out_folder, "hydro_30mc.tif")

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000",
  out_file, clip_geometry, "", "ClippingGeometry")

# Local variables:
in_file = os.path.join(out_folder, "hydro_dist_30m.tif")
clip_geometry = clip_geometry
out_file = os.path.join(out_folder, "hydro_dist_30mc.tif")

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000",
  out_file, clip_geometry, "", "ClippingGeometry")

# Local variables:
in_file = os.path.join(out_folder, "hydro_dir_30m.tif")
clip_geometry = clip_geometry
out_file = os.path.join(out_folder, "hydro_dir_30mc.tif")

# Process: Clip
arcpy.Clip_management(in_file, "335000 4750000 668000 5257000",
  out_file, clip_geometry, "", "ClippingGeometry")
