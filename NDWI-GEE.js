var Polygon = ee.Geometry.Polygon([
  [110.29, -7.9],
  [110.29, -7.84],
  [110.24, -7.84],
  [110.24, -7.9]])
//print(Polygon);
var features = ee.Feature(Polygon,{name : 'Poly',num : 1});
Map.addLayer(features);
function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask).divide(10000);
}
var S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate('2024-01-01','2024-12-12')
    .filterBounds(Polygon)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',6))
          .map(maskS2clouds)
          .median();
var Green = S2.select('B3');
var NIR = S2.select('B8');

var NDWI = Green.subtract(NIR).divide(NIR.add(Green)).rename('NDWI');
//print(S2);
var visualization = {
  min: -0.711,
  max: 0.3
};
Map.addLayer(NDWI.clip(Polygon),visualization, 'NDWI');
//NDWI.clip(Polygon).getMap(visualization , function(data) {print(data)})

Export.image.toDrive({
  image:NDWI.clip(Polygon),
  description: 'NDWI',
 scale: 10,
  crs: 'EPSG:32749'
});