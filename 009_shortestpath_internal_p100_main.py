# Please run this code on the python console in QGIS
# To measure the shortest distance
#    from each point of buildings inside a residential area
#    to each point of hypotherical ends of the area (north, south, east, and west ends)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *


studyareas = ['0057','0150','0175','0183','0186','0207','0226','0237','0276','0295',
              '0324','0330','0421','0443','0466','0467','0480','0517','0547']
studyareas = ['0556']
studyareas = ['0606','0633','0670','0717','0995','1009','1079','1132','1135',
              '1332','1373','1539','1552','1781','1861','2015','2589','2874']

pa100 = []
output = '.../011_pa100_2_main.txt'

for starea in studyareas:
   	filename = '.../walk_effi_2nd/' + starea + '/001_aptent_xy.txt'
	filename2 = '.../walk_effi_2nd/' + starea + '/001_nsew_xy_main.txt'
	basenetwork = '.../walk_effi_2nd/' + starea + '/002_grid_100_45_line.shp'
    # Pre-defined data1: Location of buildings (x/y) inside a residential area in meter
	#filename = '.../walk_effi_2nd/0057/001_aptent_xy.txt'
	with open(filename) as data:
		lines = data.readlines()
	aptloc = []
	for line in lines:
		aptloc.append(line.split())
	# Pre-defined data2: Location of north, south, east, and west ends of the area (x/y) in meter
	#filename2 = '.../walk_effi_2nd/0057/001_nsew_xy.txt'
	with open(filename2) as data2:
		lines = data2.readlines()
	dest = []
	for line in lines:
		dest.append(line.split())
	# Prepare a list of elements, each of which is a set of x/y coordinates of each building as a starting point and those of each end as a destination point
	#     For a building1 and a west end of a area, the element of coordiates should be [x_building1, y_building1, x_westend, y_westend]
	#     Thus, the length of the list equals to the length of list of buildings multiplied by the length of destination (4)
	#     For instance, if there are 11 buildings in a residential area, the length of a list of coordinate elements for the buildings is 44 and seems as followinF:
	#           [[x_bldg1, y_blgd1, x_northend, y_northend], [x_bldg1, y_blgd1, x_southend, y_southend], .... , [x_bldg11, y_blgd11, x_westend, y_westend]]
	df = []
	for m in range(0,len(aptloc)):
		for n in range(0,len(dest)):
			cc = aptloc[m] + dest[n]
			df.append(cc)
	# Prepare an empty list of shortest distances between buildings and the area ends
	#     Measure the shortest distance from each coordiate element contained in df
	#     Assign the empty list of shortest distances (list name : pathlen) the shortest distances measured from the list df:
	#			[dist_bldg1_north, dist_bldg1_south, dist_bldg1_east, dist_bldg1_west, .... , dist_bldg11_north, dist_bldg11_south, dist_bldg11_east, dist_bldg11_west]
	#     The length of pathlen and df should be the same
	#basenetwork = ".../walk_effi_2nd/0057/002_grid_50_45_line.shp"
	v = QgsVectorLayer(basenetwork, "temp","ogr")
	QgsMapLayerRegistry.instance().addMapLayer(v)
	pathlen = []
	for o in range(0,len(df)):
		vl = qgis.utils.iface.mapCanvas().currentLayer()
		director = QgsLineVectorLayerDirector(vl, -1, '', '', '', 3)
		properter = QgsDistanceArcProperter()
		director.addProperter(properter)
		crs = qgis.utils.iface.mapCanvas().mapRenderer().destinationCrs()
		builder = QgsGraphBuilder(crs)
		pStart = QgsPoint(float(df[o][0]),float(df[o][1]))
		pStop = QgsPoint(float(df[o][2]),float(df[o][3]))
		tiedPoints = director.makeGraph(builder, [pStart, pStop])
		graph = builder.graph()
		tStart = tiedPoints[0]
		tStop = tiedPoints[1]
		idStart = graph.findVertex(tStart)
		tree = QgsGraphAnalyzer.shortestTree(graph, idStart, 0)
		idStart = tree.findVertex(tStart)
		idStop = tree.findVertex(tStop)
		if idStop == -1:
			print "Path not found"
		else:
			p = []
			while (idStart != idStop):
				l = tree.vertex(idStop).inArc()
				if len(l) == 0:
					break
				e = tree.arc(l[0])
				p.insert(0, tree.vertex(e.inVertex()).point())
				idStop = e.outVertex()
		p.insert(0, tStart)
		rb = QgsRubberBand(qgis.utils.iface.mapCanvas())
		rb.setColor(Qt.red)
		for pnt in p:
			rb.addPoint(pnt)
		dl = [0]*(len(p)-1)
		for i in range(0,(len(p)-1)):
			v = ((p[i][0]-p[i+1][0])**2 + (p[i][1]-p[i+1][1])**2)**0.5
			dl[i] = v
		w = sum(dl)
		pathlen.append(w)
	# Group the distance elements in pathlen by building and create a new list (list name: sublist) and it seems as followinF:
	#    [[bldg1_north,bldg1_south,bldg1_east, bldg1_west], [bldg2_north,bldg2_south,bldg2_east, bldg2_west], .... , [bldg11_north,bldg11_south,bldg11_east, bldg11_west]]
	# The length of sublist should be the same as the number of buildings
	# Sum the shortest lengths by building and create a list totaling the shortest distances from each building (list name: totlen)
	sublist = [pathlen[n:n+4] for n in range(0, len(pathlen), 4)]
	totlen = []
	for r in range(0,len(sublist)):
		w = sum(sublist[r])
		totlen.append(w)
	pa_sd = sum(totlen)/len(totlen)
	pa100.append(pa_sd)


with open(output, 'w') as f:
    f.write(str(pa100))
