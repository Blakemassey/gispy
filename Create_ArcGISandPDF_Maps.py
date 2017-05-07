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

# ################################## Create Overview Map  ####################################################################

print "Making overview map."

#Create final compiled GPS Location Map
current_date = strftime("%Y.%m.%d")

#Make primary map document
mxd = arcpy.mapping.MapDocument("C:\\Work\\Python\\Maps\\BAEA_Basemap.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Telemetry")[0]    
All_Units = "C:\\Work\\Python\\Data\\Layers\\All_Units.lyr"
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
legend.autoAdd = False

fldName = 'serial'
fcName = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Points"
baea_points = "C:\\Work\\Python\\Data\\BAEA.gdb\\BAEA_Points"
baea_gdb = "C:\\Work\\Python\\Data\\BAEA.gdb"

myList = set([row.getValue(fldName) for row in arcpy.SearchCursor(fcName)])
myString = ', '.join(map(str, myList))

for i in myList:
    # Local variables:  
    layer_point = "C:\\Work\\Python\\Data\\Layers\\"+str(i)+".lyr"
    layer_path = "C:\\Work\\Python\\Data\\Layers\\"+str(i)+"_Path.lyr"

    #Add layer into primary map document
    addLayer = arcpy.mapping.Layer(layer_path)
    arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
    addLayer2 = arcpy.mapping.Layer(layer_point)
    arcpy.mapping.AddLayer(df, addLayer2, "AUTO_ARRANGE")
    layer3 = arcpy.mapping.ListLayers(mxd, "")[0] 
    if layer3.supports("LABELCLASSES"):
        for lblclass in layer3.labelClasses:
            lblclass.showClassLabels = True
    lblclass.expression = "[datetime_converted]"
    layer3.showLabels = True

lyr1 = arcpy.mapping.Layer(All_Units)
newextent = lyr1.getExtent()
desc = arcpy.Describe(lyr1)
newextent.XMin = desc.extent.XMin - .025
newextent.XMax = desc.extent.XMax + .025
newextent.YMin = desc.extent.YMin - .025
newextent.YMax = desc.extent.YMax + .025
df.extent = newextent

#Change title

new_title = "GPS Units: " + myString
elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Title")[0]
elm.text = new_title
del elm

#Change date range
recs = arcpy.SearchCursor(All_Units)
ary = []
for rec in recs:
   val = rec.getValue('datetime_converted')
   ary.append(val)
max_date = max(ary)
min_date = min(ary)
elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Date Range")[0]
elm.text = "Date Range: " + str(min_date) + " to " + str(max_date)
del elm

#Change made map date

current_time= strftime("%Y-%m-%d %H:%M")
elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Made Date")[0]
elm.text = "Created: " + str(current_time)

arcpy.env.workspace = "c:/Work/Python/Maps"
arcpy.env.overwriteOutput = True

tmpPdf = r"C:/Work/Python/Maps/PDF/BAEA Overview Map.pdf"
arcpy.mapping.ExportToPDF(mxd, tmpPdf)

del current_date, mxd, df, All_Units, legend, fldName, fcName, baea_points, baea_gdb, myList, row, \
    lyr1, desc, newextent, recs, ary, rec, val, max_date, min_date, elm, tmpPdf 

print "Made overview map!"

# ################################## Create Maps for Each Eagle  ####################################################

print "Making map for each unit."

#set workspace
arcpy.env.workspace = 'C:/Work/Python/Maps'
arcpy.env.overwriteOutput = True

#Create final compiled GPS Location Map
current_date = strftime("%Y.%m.%d")
final_pdf_location = "C:/Work/Python/Maps/PDF/GPS Location Map - "+ current_date +".pdf"
finalPdf = arcpy.mapping.PDFDocumentCreate(final_pdf_location)
overview_pdf = r"C:/Work/Python/Maps/PDF/BAEA Overview Map.pdf"
finalPdf.appendPages(overview_pdf)

#set creates a unique value iterator from the value field
fldName = 'serial'
fcName = "C:/Work/Python/Data/BAEA.gdb/BAEA_Points"
BAEA_Points = "C:/Work/Python/Data/BAEA.gdb/BAEA_Points"
BAEA_gdb = "C:/Work/Python/Data/BAEA.gdb"
myList = set([row.getValue(fldName) for row in arcpy.SearchCursor(fcName)])

for i in myList:

   # Local variables:
   layer_point = "C:/Work/Python/Data/Layers/"+str(i)+".lyr"
   layer_path = "C:/Work/Python/Data/Layers/"+str(i)+"_Path.lyr"
   SC = arcpy.SearchCursor(layer_point)
   field_name = 'deploy_location'
   SavedCopy = "C:/Work/Python/Maps/"+str(i)+".mxd"
   point_lyr = "C:/Work/Python/Data/Layers/" + str(i) + ".lyr"
   point_sym_lyr = "C:/Work/Python/Data/Symbology/Points.lyr"
   path_lyr = "C:/Work/Python/Data/Layers/" + str(i) + "_Path.lyr"
   path_sym_lyr = "C:/Work/Python/Data/Symbology/Paths.lyr"

   # Add layer into primary map document
   mxd = arcpy.mapping.MapDocument("C:/Work/Python/Maps/BAEA_Basemap.mxd")   
   legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
   legend.autoAdd = False
   df = arcpy.mapping.ListDataFrames(mxd, "Telemetry")[0] 
   addLayer = arcpy.mapping.Layer(layer_path)
   arcpy.mapping.AddLayer(df, addLayer, "TOP")
   addLayer2 = arcpy.mapping.Layer(layer_point)
   arcpy.mapping.AddLayer(df, addLayer2, "AUTO_ARRANGE")
   layer3 = arcpy.mapping.ListLayers(mxd, "")[0] 
   if layer3.supports("LABELCLASSES"):
        for lblclass in layer3.labelClasses:
            lblclass.showClassLabels = True
   lblclass.expression = "[Datetime_converted]"
   layer3.showLabels = True

   df2 = arcpy.mapping.ListDataFrames(mxd)[0]
   lyr1 = arcpy.mapping.Layer(layer_path)
   newextent = lyr1.getExtent()
   desc = arcpy.Describe(layer_point)
   newextent.XMin = desc.extent.XMin - .025
   newextent.XMax = desc.extent.XMax + .025
   newextent.YMin = desc.extent.YMin - .025
   newextent.YMax = desc.extent.YMax + .025
   df2.extent = newextent

   #Change title
   for row in SC:
       location = row.getValue(field_name)
       # using break allows you to stop the search cursor
       break

   new_title = "GPS Unit " + str(i) + ": " + location 
   elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Title")[0]
   elm.text = new_title
   del elm

   #Change date range
   recs = arcpy.SearchCursor(layer_point)
   ary = []
   for rec in recs:
       val = rec.getValue('datetime_converted')
       ary.append(val)
   max_date = max(ary)
   min_date = min(ary)
   elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Date Range")[0]
   elm.text = "Date Range: " + str(min_date) + " to " + str(max_date)

   #Change made map date
   from time import gmtime, strftime
   current_time= strftime("%Y-%m-%d %H:%M")
   elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Made Date")[0]
   elm.text = "Created: " + str(current_time)

   SavedCopyPFD = "C:/Work/Python/Maps/PDF/"+str(i)+" - " + location + ".pdf"
   arcpy.mapping.ExportToPDF(mxd, SavedCopyPFD, image_quality=2)
   current_time2= strftime("%Y-%m-%d %H:%M:%S")

   #Export map page and append to final PDF file
   tmpPdf = r"C:/Windows/TEMP/BAEA_Individual_Maps.pdf"
   arcpy.mapping.ExportToPDF(mxd, tmpPdf)
   finalPdf.appendPages(tmpPdf)
   print "Made a map for unit "+ str(i) +"-"+ location + " at " + current_time2 +"!"

   del layer_point, layer_path, SC, field_name, SavedCopy, point_lyr, point_sym_lyr, path_lyr, path_sym_lyr, \
       mxd, legend, df, addLayer, addLayer2, layer3, df2, lyr1, newextent, row, location, new_title, elm, \
       recs, ary, rec, val, max_date, min_date, current_time, SavedCopyPFD, current_time2, tmpPdf

del overview_pdf, fldName, fcName, BAEA_Points, BAEA_gdb, myList

finalPdf.updateDocProperties(pdf_open_view="USE_THUMBS", pdf_layout="SINGLE_PAGE")
del finalPdf

current_time3= strftime("%Y-%m-%d %H:%M:%S")
print "Successfully finished at " + current_time3 + "!"