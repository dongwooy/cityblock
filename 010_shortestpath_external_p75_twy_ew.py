from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *

studyareas = ['0057','0150','0175','0183','0186','0207','0226','0237','0276','0295',
              '0324','0330','0421','0443','0466','0467','0480','0517','0547','0556',
              '0606','0633','0670','0717','0995','1009','1079','1132','1135','1332',
              '1373','1539','1552','1781','1861','2015','2589','2874']

pa75 = []
output = '.../011_pa75_ext_twy_ew.txt'

for starea in studyareas:
   	filename = '.../walk_effi_2nd/' + starea + '/001_nsew_xy_twy_ew.txt'
	filename2 = '.../walk_effi_2nd/' + starea + '/001_nsew_xy_twy_ew.txt'
	basenetwork = '.../walk_effi_2nd/' + starea + '/002_grid_75_45_line.shp'
	with open(filename) as data:
		lines = data.readlines()
	aptloc = []
	for line in lines:
		aptloc.append(line.split())
	with open(filename2) as data2:
		lines = data2.readlines()
	dest = []
	for line in lines:
		dest.append(line.split())
	df = []
	for m in range(0,len(aptloc)):
		for n in range(0,len(dest)):
			cc = aptloc[m] + dest[n]
			df.append(cc)
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
	sublist = [pathlen[n:n+4] for n in range(0, len(pathlen), 4)]
	totlen = []
	for r in range(0,len(sublist)):
		w = sum(sublist[r])
		totlen.append(w)
	pa_sd = (sum(totlen)/len(totlen))/4
	pa75.append(pa_sd)


with open(output, 'w') as f:
    f.write(str(pa75))
