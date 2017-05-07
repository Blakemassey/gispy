###-------------------------------------------------------------------------------
### Name:        Update_Nests_Study_Intact_Last
### Purpose:     Creates nest geodatabases from
###                 R/Data/BAEA/Nests/Nests_Study_Intact_Last.csv file
### Author:      Blake Massey
### Created:     2015/11/12
###-------------------------------------------------------------------------------

# import system modules
import arcpy
from arcpy import env

# Environmental Variables
arcpy.env.workspace = "C:\\ArcGIS\\Data\\BAEA\\Nests\\Nests.gdb"
arcpy.env.overwriteOutput = 'True'

# ####################### Study_Intact_Active ##################################

csv = "C:\\Work\\R\\Data\\BAEA\\Nests\\Nests_Study_Intact_Active.csv"
x_coords = "long"
y_coords = "lat"
points = "C:\\ArcGIS\\Data\\BAEA\\Nests\\Nests.gdb\\Study_Intact_Last_Active"

# Set the spatial reference
spRef = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',\
  SPHEROID['WGS_1984',6378137.0,298.257223563]],\
  PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];\
  -400 -400 1000000000;-100000 10000;-100000 10000;\
  8.98315284119522E-09;0.001;0.001;IsHighPrecision"

# Process: Make the XY event layer
arcpy.MakeXYEventLayer_management(csv, x_coords, y_coords,
  "nest_points_XY_lyr",spRef)

# Process: Feature To Point
arcpy.FeatureToPoint_management("nest_points_XY_lyr", points, "CENTROID")

del csv, x_coords, y_coords, points

print "Made Study_Intact_Active feature class!"