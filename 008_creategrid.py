import qgis.core
import processing
import os
from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface

studyareas = ['0057','0150','0175','0183','0186','0207','0226','0237','0276','0295',
                '0324','0330','0421','0443','0466','0467','0480','0517','0547','0556',
                '0606','0633','0670','0717','0995','1009','1079','1132','1135','1332',
                '1373','1539','1552','1781','1861','2015','2589','2874']

for i in studyareas:
    path = ".../cityblock2/walk_effi_2nd/" + i + "/000_studyarea.shp"
    ly = QgsVectorLayer(path, "study areas", "ogr")
    typee=1
    crs="EPSG:5179"
    xmin = ly.extent().xMinimum()-100
    xmax = ly.extent().xMaximum()+100
    ymin = ly.extent().yMinimum()-100
    ymax = ly.extent().yMaximum()+100
    extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
    gridsize = [50,75,100]
    vspacing = 45
    for j in gridsize:
        grid_out = ".../cityblock2/walk_effi_2nd/" + i + "/002_grid_" + str(j) + "_45_line.shp"
        #if os.path.isfile(grid_out):
        #    os.remove(grid_out)
        a10 = processing.runalg('qgis:creategrid', typee, extent, j, vspacing, crs, None)
        a11 = processing.getObject(a10['OUTPUT'])
        a20 = processing.runalg("qgis:clip",a11,ly,None)
        a21 = processing.getObject(a20['OUTPUT'])
        a30 = processing.runalg("qgis:polygonstolines", a21, None)
        a31 = processing.getObject(a30['OUTPUT'])
        a40 = processing.runalg('qgis:explodelines', a31, None)
        a41 = processing.getObject(a40['OUTPUT'])
        a50 = processing.runalg('qgis:deleteduplicategeometries', a41, grid_out)
        a51 = processing.getObject(a50['OUTPUT'])
        QgsMapLayerRegistry.instance().addMapLayer(a51)
