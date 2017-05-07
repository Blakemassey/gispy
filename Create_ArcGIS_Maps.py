# -# ---------------------------------------------------------------------------
# BAEA_Create_Maps.py
# Created on: 2013-12-11 
# Author: Blake Massey
# Usage: BAEA_Create_Maps (Days_Back OR Start_Date/End_Date needs to be set)
# Description: Used to make feature classes, KMZs, and maps for each GPS unit
#              The code is divided into 'sections' because Python was crashing
#              and the breaks are needed to remove locks on data that were
#              causing the problems.
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy, os, string
from time import gmtime, strftime

# Script arguments
Days_Back = 1000
Start_Date = '2013-12-25'
End_Date = '2013-12-30'

# Environmental Variables
arcpy.env.workspace = "C:\\Work\\Python\\Data\\BAEA.gdb"
arcpy.env.overwriteOutput = 'True'

current_time = strftime("%Y-%m-%d %H:%M:%S")
print "Started \"BAEA_Create_Maps\" script at " + current_time + "."
print "Making BAEA_Points feature class."

# ################################## Make BAEA_Points Feature Class  ####################################################

# Local variables:
baea_csv = "C:\\Work\\Python\\Data\\CSV\\BAEA.csv"
expression = "\"date\" >= CURRENT_DATE - "+ str(Days_Back)
expression2 = ' "date" >= date ' + '\'' + str(Start_Date) + '\' ' + 'And "date" <= date ' + '\'' + str(End_Date) + '\' '
baea_select = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Select"
baea_points = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Points"
baea_points_lyr = "C:\\Work\\Python\\Data\\Layers\\All_Units.lyr"
baea_points_lyr_temp = "C:\\Work\\Python\\Data\\Layers\\All_Units_TEMP.lyr"

# Process: Table Select
arcpy.TableSelect_analysis(baea_csv, baea_select, expression)

# Process: Convert Time Field
arcpy.ConvertTimeField_management(baea_select, "datetime", "'Not Used'", "datetime_converted", "TEXT", "yyyy-MM-dd HH:mm")

# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(baea_select, "long", "lat", "baea_points_XY_lyr",
                                  "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                                  PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;\
                                  8.98315284119522E-09;0.001;0.001;IsHighPrecision","alt")

# Process: Feature To Point
arcpy.FeatureToPoint_management("baea_points_XY_lyr", baea_points, "CENTROID")

#Process: Make Feature Layer (Points)
arcpy.MakeFeatureLayer_management(baea_points, baea_points_lyr_temp, "", "")

#Process: Save To Layer File (Point)
arcpy.SaveToLayerFile_management(baea_points_lyr_temp, baea_points_lyr, "ABSOLUTE")

del baea_csv, baea_select, baea_points, baea_points_lyr #deleting everything to remove locks

print "Made BAEA_Points feature class!"

# ################################## Make Feature Class for Each Unit  ####################################################

fldName = 'serial'
fcName = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Points"
baea_points = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Points"
baea_gdb = "C:\\Work\\Python\\Data\\BAEA.gdb"

myList = set([row.getValue(fldName) for row in arcpy.SearchCursor(fcName)])
myString = ', '.join(map(str, myList))

print "Making feature class and layers for units " + myString + "."

for i in myList: 
   expression = "\"serial\" = "+ str(i)
   fcname = "Unit_"+str(i)
   #Process: Feature Class to Feature Class
   arcpy.FeatureClassToFeatureClass_conversion(baea_points, baea_gdb, fcname, expression, "")

#arcpy.env.scratchWorkspace = "C:\\Work\\Python\\Data\\Work.gdb"

for i in myList:

   #Local variables for points:
   
   points = "C:\\Work\\Python\\Data\\BAEA.gdb\\Unit_" + str(i)
   points_layer = "C:\\Work\\Python\\Data\\Layers\\" + str(i) + ".lyr"
   points_feature_layer_temp = "Unit " + str(i)
   points_sym_lyr = "C:\\Work\\Python\\Data\\Symbology\\Points.lyr"
   points_kmz = "C:\\Work\\Python\\Data\\KMZ\\" + str(i) + ".kmz"
   points_kmz_sym_lyr = "C:\\Work\\Python\\Data\\Symbology\\Points_KMZ.lyr"

   #Local variables for lines:
   
   path = "C:\\Work\\Python\\Data\\BAEA.gdb\\Unit_" + str(i) + "_Path"
   path_layer = "C:\\Work\\Python\\Data\\Layers\\" + str(i) + "_Path.lyr"
   path_feature_layer_temp = "Path"
   path_layer_temp = "C:\\Work\\Python\\Data\\Work.gdb\\Unit_" + str(i) + "_Path_temp"
   path_layer_temp2 = "C:\\Work\\Python\\Data\\Work.gdb\\Unit_" + str(i) + "_Path_temp2"
   path_sym_lyr = "C:\\Work\\Python\\Data\\Symbology\\Paths.lyr"
   path_kmz = "C:\\Work\\Python\\Data\\KMZ\\" + str(i) + "_Path.kmz"
   path_kmz_sym_lyr = "C:\\Work\\Python\\Data\\Symbology\\Paths_KMZ.lyr"

   #Process: Make Feature Layer (Points)
   arcpy.MakeFeatureLayer_management(points, points_feature_layer_temp, "", "",)
   
   # Process: Apply Symbology From Layer (Points)
   arcpy.ApplySymbologyFromLayer_management(points_feature_layer_temp, points_sym_lyr)
   #Process: Save To Layer File (Points)
   arcpy.SaveToLayerFile_management(points_feature_layer_temp, points_layer, "", "CURRENT")
   # Process: Apply Symbology From Layer (Points)
   arcpy.ApplySymbologyFromLayer_management(points_feature_layer_temp, points_kmz_sym_lyr)
   # Process: Layer To KML (Points)
   arcpy.LayerToKML_conversion(points_feature_layer_temp, points_kmz, "1", "false", points_layer, "1024", "200", "ABSOLUTE")
   # Process: Points To Line (Paths)
   arcpy.PointsToLine_management(points, path_layer_temp, "", "", "NO_CLOSE")
   # Process: Split Line At Vertices (Paths)
   arcpy.SplitLine_management(path_layer_temp, path)
   # Process: Make Feature Layer (Paths)
   arcpy.MakeFeatureLayer_management(path, path_feature_layer_temp, "", "", "")
   # Process: Apply Symbology From Layer (Paths)
   arcpy.ApplySymbologyFromLayer_management(path_feature_layer_temp, path_sym_lyr)
   # Process: Save To Layer File (Paths)
   arcpy.SaveToLayerFile_management(path_feature_layer_temp, path_layer, "", "CURRENT")
   # Process: Apply Symbology From Layer
   arcpy.ApplySymbologyFromLayer_management(path_feature_layer_temp, path_kmz_sym_lyr)
   # Process: Layer To KML
   arcpy.LayerToKML_conversion(path_feature_layer_temp, path_kmz, "1", "false", path_layer, "1024", "96", "ABSOLUTE")   

#del fldName, fcName, baea_points, baea_gdb, myList, myString, expression, fcname, \
#    points, points_layer, points_feature_layer_temp, points_sym_lyr, points_kmz, points_kmz_sym_lyr, \
#    path, path_layer, path_feature_layer_temp, path_layer_temp, path_layer_temp2, path_sym_lyr, path_kmz, path_kmz_sym_lyr

print "Made feature class and layer for each unit!" 
