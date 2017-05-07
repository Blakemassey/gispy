# ---------------------------------------------------------------------------
# Landcover.py
# Created on: 2015-10-25
# Description: Combines several rasters into a new raster, reprojects the new
#   raster, resamples raster to 30m cells, then clips raster to MaineOutline.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os

# Project raster

#DSLland
arcpy.ProjectRaster_management(in_raster="C:/ArcGIS/Data/LCC/DSLIand/DSLland_2010_v3.0.tif",out_raster="C:/ArcGIS/Data/LCC/Land_crop/lc_reproj",out_coor_system="PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['false_easting',500000.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-69.0],PARAMETER['scale_factor',0.9996],PARAMETER['latitude_of_origin',0.0],UNIT['Meter',1.0]]", resampling_type="NEAREST", cell_size="30", geographic_transform="", Registration_Point="335000 4750000", in_coor_system="PROJCS['NAD_1983_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-96.0],PARAMETER['standard_parallel_1',29.5],PARAMETER['standard_parallel_2',45.5],PARAMETER['latitude_of_origin',23.0],UNIT['Meter',1.0]]")

#ELU
arcpy.ProjectRaster_management(in_raster="C:/ArcGIS/Data/LCC/ELU/elu30reg1108", out_raster="C:/ArcGIS/Data/LCC/ELU_crop/elu_reproj", out_coor_system="PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="335000 4750000", in_coor_system="PROJCS['NAD_1983_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]")

#IEI
arcpy.ProjectRaster_management(in_raster="C:/ArcGIS/Data/LCC/IEI/iei-r_2010_v3.1.tif", out_raster="C:/ArcGIS/Data/LCC/IEI_crop/iei_reproj", out_coor_system="PROJCS['NAD_1983_UTM_Zone_19N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="335000 4750000", in_coor_system="PROJCS['NAD_1983_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]")