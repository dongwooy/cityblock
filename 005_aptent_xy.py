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
	input = ".../cityblock2/walk_effi_2nd/" + i + "/001_aptent.shp"
	output = ".../cityblock2/walk_effi_2nd/" + i + "/001_aptent_xy.txt"
	a1 = processing.runalg('qgis:exportaddgeometrycolumns', input, 0, None)
	a2 = processing.getObject(a1['OUTPUT'])
	feats = []
	#layer = processing.getObject(a1['OUTPUT'])
	for feat in a2.getFeatures():
	#for feat in layer.getFeatures():
		msgout = '%s %s\n' % (feat['xcoord'],feat['ycoord'])
		unicode_message = msgout.encode('utf-8')
		feats.append(unicode_message)
	with open(output, 'w') as f:
		for item in feats:
			f.write(item)
	f.close()
