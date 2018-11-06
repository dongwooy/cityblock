import processing
import os

studyareas = ['0057','0150','0175','0183','0186','0207','0226','0237','0276','0295',
                '0324','0330','0421','0443','0466','0467','0480','0517','0547','0556',
                '0606','0633','0670','0717','0995','1009','1079','1132','1135','1332',
                '1373','1539','1552','1781','1861','2015','2589','2874']


for i in studyareas:
    polygon_input = ".../cityblock2/walk_effi_2nd/" + i + "/000_studyarea.shp"
    freenet_input = ".../cityblock2/walk_effi_2nd/" + i + "/003_nongrid.shp"
    nongrid_out = ".../cityblock2/walk_effi_2nd/" + i + "/003_nongrid2.shp"
    labelff = i + "non-grid"
    if os.path.isfile(nongrid_out):
        os.remove(nongrid_out)

    vlayer = QgsVectorLayer(polygon_input, "temp","ogr")
    vlayer2 = QgsVectorLayer(freenet_input, "temp2","ogr")
    #qgis.utils.iface.setActiveLayer(vlayer)
    vlayer.selectAll()
    a1 = processing.runalg("qgis:polygonstolines", vlayer, None)
    a2 = processing.getObject(a1['OUTPUT'])
    a3 = processing.runalg("qgis:mergevectorlayers", [a2, vlayer2], None)
    a4 = processing.getObject(a3['OUTPUT'])
    a5 = processing.runalg("qgis:dissolve", a4, True, None, None)
    a6 = processing.getObject(a5['OUTPUT'])
    a7 = processing.runalg('qgis:explodelines', a6, None)
    a8 = processing.getObject(a7['OUTPUT'])
    a9 = processing.runalg('qgis:deleteduplicategeometries', a8, nongrid_out)
    a10 = processing.getObject(a9['OUTPUT'])
    QgsMapLayerRegistry.instance().addMapLayer(a6)
