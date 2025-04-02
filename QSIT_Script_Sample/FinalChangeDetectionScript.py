import arcpy
import json
import csv
from sys import argv
from arcpy import env
from arcpy.sa import *
from arcpy.ia import *



Constant_reference_image="Dec2016"
Update_new_Image="Nov2019"
Ownership_Layer="AwkafPacel"
Workspace=r"C:\Users\esrinea\Documents\ArcGIS\Projects\MyProject3"
#####Parameter############
reference_image =arcpy.GetParameterAsText(0)
Update_image =arcpy.GetParameterAsText(1)
Awkaf_Layer =arcpy.GetParameterAsText(2)
#sourceWorkspace=arcpy.GetParameterAsText(3)
#arcpy.env.scratchWorkspace = 'c:/data/scratchoutput.gdb'

workspaceOutput= arcpy.env.scratchGDB
FolderSpace = arcpy.env.scratchFolder
#FolderSpace = r"C:\Users\esrinea\Documents\ArcGIS\Projects\MyProject3"


##reference_imagePath = sourceWorkspace +"Dec2016"
##Update_new_ImagePath = sourceWorkspace +"Dec2016"
##Awkaf_LayerPath =sourceWorkspace +"AwkafPacel"



    # To allow overwriting outputs change overwriteOutput option to True.
arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
arcpy.CheckOutExtension("ImageAnalyst")
arcpy.CheckOutExtension("spatial")


Input_raster_or_constant_value_2 = "2"



##TableSelectResult = workspaceOutput+"\SelectTable"
##RasterOutput =workspaceOutput+"\Minus"

    # Process: Minus (Minus)

#####################################################################################################################
arcpy.MakeRasterLayer_management(reference_image, r"memory\reference_image1", "#", "", "1")
reference_image1= r"memory\reference_image1"

arcpy.MakeRasterLayer_management(Update_image, r"memory\Update_image1", "#", "", "1")
Update_image1=r"memory\Update_image1"


outMinus = Minus(reference_image1,Update_image1)
outMinus.save(r"memory\Changesimage.tif")
Changes_image = r"memory\Changesimage.tif"



##############################################################################################################################################


arcpy.MakeRasterLayer_management(Changes_image, r"memory\Changes_image1", "#", "", "1")
Changes_image1= r"memory\Changes_image1"


Mean1 = arcpy.GetRasterProperties_management(in_raster=Changes_image1, property_type="MEAN", band_index="Band_1")[0]
extent="3540872.61569534 3686934.67114642 3542189.14012413 3687678.78172461"

cell_size=Changes_image1

outConstRaster = CreateConstantRaster(Mean1, "INTEGER", cell_size, extent)
outConstRaster.save(r"memory\MeanConstant.tif")
Mean_Raster = r"memory\MeanConstant.tif"

STD = arcpy.GetRasterProperties_management(in_raster=Changes_image1, property_type="STD", band_index="Band_1")[0]

outConstRaster = CreateConstantRaster(STD, "INTEGER", cell_size, extent)
outConstRaster.save(r"memory\STDConstant.tif")
STD_Raster =r"memory\STDConstant.tif"
########################################################################################################################################################

    # Process: Times (Times)

arcpy.MakeRasterLayer_management(STD_Raster, r"memory\STD_Raster1", "#", "", "1")
STD_Raster1= r"memory\STD_Raster1"

outTimes = Times(STD_Raster1, 2)
outTimes.save(r"memory\TimesConstant.tif")
TimeRaster = r"memory\TimesConstant.tif"
#########################################################################################################################################################33

    # Process: Plus (Plus)

arcpy.MakeRasterLayer_management(Mean_Raster, r"memory\Mean_Raster1", "#", "", "1")
Mean_Raster1= r"memory\Mean_Raster1"

arcpy.MakeRasterLayer_management(TimeRaster, r"memory\TimeRaster1", "#", "", "1")
TimeRaster1=r"memory\TimeRaster1"

outPlus = Plus(Mean_Raster1, TimeRaster1 )
outPlus.save(r"memory\PlusConstant.tif")
PlusRaster =r"memory\PlusConstant.tif"
###########################################################################################################################################################
    # Process: Greater Than (Greater Than)
##
##arcpy.MakeRasterLayer_management(Changes_image, r"memory\Changes_image1", "#", "", "1")
##Changes_image1= r"memory\Changes_image1"

arcpy.MakeRasterLayer_management(PlusRaster, r"memory\PlusRaster1", "#", "", "1")
PlusRaster1=r"memory\PlusRaster1"

outGreaterThan = Raster(Changes_image1) > Raster(PlusRaster1)
outGreaterThan.save(r"memory\GreaterThanConstant.tif")
GreaterThanRaster =r"memory\GreaterThanConstant.tif"
##############################################################################################################################################################33

    # Process: Minus (2) (Minus)


outMinus2 = Minus(Mean_Raster1, TimeRaster1 )
outMinus2.save(r"memory\Minus2.tif")
Minus2Raster =r"memory\Minus2.tif"

#########################################################################################################################################################33
    # Process: Less Than (Less Than)



arcpy.MakeRasterLayer_management(Changes_image, r"memory\Changes_image1", "#", "", "1")
Changes_image1= r"memory\Changes_image1"

arcpy.MakeRasterLayer_management(Minus2Raster, r"memory\Minus2Raster1", "#", "", "1")
Minus2Raster1=r"memory\PlusRaster1"

outLessThan = LessThan(Changes_image1, Minus2Raster1)
outLessThan.save(r"memory\LessThanRaster.tif")
LessThanRaster =r"memory\LessThanRaster.tif"

#############################################################################################################################################################


arcpy.MakeRasterLayer_management(LessThanRaster, r"memory\LessThanRaster1", "#", "", "1")
LessThanRaster1= r"memory\LessThanRaster1"

arcpy.MakeRasterLayer_management(GreaterThanRaster, r"memory\GreaterThanRaster1", "#", "", "1")
GreaterThanRaster1= r"memory\LessThanRaster1"

outPlus2 = Plus(GreaterThanRaster1,LessThanRaster1)
outPlus2.save(r"memory\PlusConstant2.tif")
PlusRaster2 = r"memory\PlusConstant2.tif"


#########################################################################################################################################################



outSetNull = SetNull(PlusRaster2,PlusRaster2, "VALUE = 0")
outSetNull.save(r"memory\SetNullRaster.tif")
SetNullRaster = r"memory\SetNullRaster.tif"

Ownership_Layer = Awkaf_Layer


#################################################################################################################################################################

outPolygons = r"memory\outputpolygon"
RastertoPolygon = arcpy.RasterToPolygon_conversion(SetNullRaster,outPolygons, simplify="SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)


inFeatures = [outPolygons,Ownership_Layer ]


intersectOutput =r"memory\Intersect_crossings"

arcpy.Intersect_analysis(inFeatures ,intersectOutput,"","", "INPUT")

StatField =[['TawliaNo','FIRST']]

disolveResuilt = arcpy.management.Dissolve(intersectOutput , r"memory\Intersect_Dissolve1","Eain_NO", StatField, "MULTI_PART", "DISSOLVE_LINES")

ChangeDetectionArea=r"memory\Intersect_Dissolve1"
outputfc = arcpy.SetParameterAsText(3, ChangeDetectionArea)

###############################################################################################################################
#arcpy.management.AlterField(workspaceOutput +"\\Intersect_Dissolve1", "FIRST_TawliaNo", "TawliaNo", "TawliaNo", "Text", 50, "NULLABLE", "DO_NOT_CLEAR")

FinalTable = arcpy.conversion.TableToTable(disolveResuilt, r"memory" , "FinalTable")
arcpy.management.DeleteField(FinalTable, "FID_outPolygons;gridcode;FID_AwkafPacel;parcel_no;???????;???_???????;???_?????;Shape_Length;Shape_Area;???????;???_???????;???_?????")

arcpy.conversion.TableToTable(FinalTable,FolderSpace, "FinalTable.csv" )

#Json = json.dumps(listTin)
#print Json


    # Open a csv reader called DictReader
def make_json(csvFilePath, jsonFilePath):

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(FolderSpace+"\FinalTable.csv", encoding="utf8") as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Eain_NO']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(FolderSpace+"\jsonFilePath", 'w',encoding="utf8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    ##with open(r"C:\Users\esrinea\Desktop\jsonFilePath", 'w',encoding="utf8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


csvFilePath = r'Names.csv'
jsonFilePath = r'Names.json'

# Call the make_json function
make_json(FolderSpace +"\FinalTable.csv",Workspace +"\jsonFilePath" )
#Json =Workspace +"\jsonFilePath"


output = json.dumps(Workspace +"\jsonFilePathtest")

output=arcpy.SetParameterAsText(4,output)


#output=arcpy.SetParameterAsText(1,Json.json )
#make_json(r"C:\Users\esrinea\Desktop\FinalTable.csv", r"C:\Users\esrinea\Desktop\jsonFilePath")
