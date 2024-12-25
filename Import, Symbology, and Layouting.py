
#1.ADD Downloaded Raster to QGIS
fileName = 'E:/NDWI.tif'

fileInfo = QFileInfo(fileName)
fname = fileInfo.baseName()

rlayer = iface.addRasterLayer(fileName, fname)

stats = rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
# print(stats)
min = stats.minimumValue
max = stats.maximumValue

#2. Symbology
color = QgsColorRampShader()
color.setColorRampType(QgsColorRampShader.Interpolated)

ListColor = [QgsColorRampShader.ColorRampItem(min, QColor(90,215,209)),\
            QgsColorRampShader.ColorRampItem(max, QColor(43,8,215))
            ]
color.setColorRampItemList(ListColor)

shader = QgsRasterShader()
shader.setRasterShaderFunction(color)

renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(),1, shader)
renderer.setClassificationMax(1)
renderer.setClassificationMin(-1)
rlayer.setRenderer(renderer)

#3.Layouting Map
from qgis.PyQt import QtGui


layers = QgsProject.instance().mapLayersByName('NDWI')
layer = layers[0]

project = QgsProject.instance()
manager = project.layoutManager()
layoutName = 'NDWI'
layout_list = manager.printLayouts()
#romve any dupplicate layout
for layout in layout_list :
    if layout.name() == layoutName:
        manager.removeLayout(layout)
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layoutName)

#change Page Orientation 
pc = layout.pageCollection()
pc.page(0).setPageSize('A4', QgsLayoutItemPage.Orientation.Portrait)

manager.addLayout(layout)

#remove map item in layout
map = QgsLayoutItemMap(layout)
map.setRect(20,20,20,20)

#set the map extent
ms = QgsMapSettings()
ms.setLayers([layer])
rect = QgsRectangle(416185.409,9126715.020,421060.409,9133380.659)
canvas = iface.mapCanvas()
map.setExtent(rect)
layout.addLayoutItem(map)


map.attemptMove(QgsLayoutPoint(7,20,QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(195,265, QgsUnitTypes.LayoutMillimeters))

#4. Add legend
legend = QgsLayoutItemLegend(layout)
legend.setTitle ("Legend")
layerTree = QgsLayerTree ()
layerTree.addLayer(layer)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(155 , 40, QgsUnitTypes.LayoutMillimeters))

#5. add scale bar
scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Single Box')
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(3)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(1)
scalebar.setLinkedMap(map)
scalebar.setUnitLabel('Kilometers')
scalebar.update()
layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(19, 270, QgsUnitTypes.LayoutMillimeters))

#6. add title

title = QgsLayoutItemLabel(layout)
title.setText("NDWI some Area of Bantul Regency")
title.setFont(QFont('Araboto-Black',25))
title.adjustSizeToText()

title.attemptResize(QgsLayoutSize(150,title.boundingRect().height()))
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(11, 7, QgsUnitTypes.LayoutMillimeters))

#9. export Map

exporter = QgsLayoutExporter(layout)
fn = 'E:/NDWI some Area of Bantul Regency.pdf' #put anywhere you want
exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())

#Sources Learning : 
#gis.stackexchange.com
#youtube channel : geospatial school
#meta AI
