# Prelim analysis script for QGIS (requires GEE plugin)
import ee
from ee_plugin import Map
import geopandas as gpd
import json
import os


# Set path to wd
path = os.path.join("/","Users","MT","Nextcloud","Projects","GOV-BGD20GIZ7333_CRISC_AI")

# helper function: lookup shp index by city/levell geodataframe format, ee object construct
def shp_to_ee_fmt(city, level):
    dic = {'Satkhira':{2:56,3:469,4:4307},'Sirajganj':{2:59,3:496,4:4493}}
    ind = dic[city][level]
    shp_path = os.path.join(path,"CRISC_RS","bgd_adm_bbs_20201113_SHP","bgd_admbnda_adm"+str(level)+"_bbs_20201113.shp")
    gdf = gpd.read_file(shp_path, crs='EPSG:4326')
    x = gdf.iloc[ind:ind+1,:]
    data = json.loads(x.to_json())
    return data['features'][0]['geometry']['coordinates']

# Histogram function
def histo(dist, band, bins, city, level):
    aoi = ee.Geometry.MultiPolygon(shp_to_ee_fmt(city = city, level = level))
    arr = np.array(dist.sampleRectangle(region=aoi).get(band).getInfo())
    data = arr.flatten()
    fig, ax = plt.subplots(figsize=(15,5))
    sns.histplot(data, bins=bins,ax=ax)
    plt.title('Distribution: '+city, fontsize=20)

# Source shp: https://data.humdata.org/dataset/administrative-boundaries-of-bangladesh-as-of-2015

viirs = ee.Image(ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG").filterDate("2019-01-01","2019-12-31").median().select('avg_rad'))
srtm = ee.Image("CGIAR/SRTM90_V4").select('elevation')
srtmVis = {'min':-1, 'max':14,'palette':['#f7fcfd','#e5f5f9','#ccece6','#99d8c9','#66c2a4','#41ae76','#238b45','#005824']}
water = ee.Image("JRC/GSW1_3/GlobalSurfaceWater").select('occurrence')
waterVis= {"min":0, "max":50,"palette":['lightblue', 'blue'], "bands":"occurrence"}
ghslSet = ee.ImageCollection('JRC/GHSL/P2016/SMOD_POP_GLOBE_V1').filter(ee.Filter.date('2015-01-01', '2015-12-31')).select('smod_code').median();
ghslSetVis= {"min":0.0, "max":3.0,"palette":['000000', '448564', '70daa4', 'ffffff']}
ghslPop = ee.ImageCollection("JRC/GHSL/P2016/POP_GPW_GLOBE_V1").filter(ee.Filter.date('2015-01-01', '2015-12-31')).select('population_count').median();
ghslPopVis= {"min":0.0, "max":5000.0,"palette":['000000', '448564', '70daa4', 'ffffff']}

# Flowminder Poverty Predictions based on mobile data (https://royalsocietypublishing.org/doi/full/10.1098/rsif.2016.0690)
# 2011 estimates of mean DHS wealth index score per grid square 
pov_wi = ee.Image('users/marktyrrell111/bgd2011wipov')
# 2013 estimates of income in USD per grid square 
pov_inc = ee.Image('users/marktyrrell111/bgd2013incpov')
# 013 estimates of mean likelihood of living in poverty per grid square, as defined by $2.50 a day poverty line
pov_prop = ee.Image('users/marktyrrell111/bgd2013ppipov')

# Get Sentinal
#aoi_bd = ee.Feature(ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh')).first()).geometry()
#first = (ee.ImageCollection('COPERNICUS/S2_SR')
         # .filterBounds(aoi_bd)
         # .filterDate('2019-01-01', '2019-12-31')
         # .sort('CLOUDY_PIXEL_PERCENTAGE')
         # .first())


#AOI: Satkhira District (Khulna Division)
#___________________________________________
aoi = ee.Geometry.MultiPolygon(shp_to_ee_fmt(city = 'Satkhira', level = 3))

# initialize the map
Map.addLayer(viirs.clip(aoi), {}, "VIIRS-DNB Nightlights", opacity=0.5)
Map.addLayer(ghslSet.clip(aoi), ghslSetVis, 'GHSL Degree of Urbanization', opacity=0.5)
Map.addLayer(ghslPop.clip(aoi), ghslPopVis, 'GHSL Population', opacity=0.5)
Map.addLayer(srtm.clip(aoi), {'min':-1, 'max':14}, 'SRTM Elevation', opacity = 0.6)
Map.addLayer(water.clip(aoi), waterVis, 'JRC Water Prevalence', opacity = 0.6)
Map.addLayer(pov_inc.clip(aoi), {'min':130, 'max':200, "palette":['red', 'yellow']}, "BD Poverty: Income", opacity=0.6)
Map.addLayer(pov_wi.clip(aoi), {'min':-0.2, 'max':1.2, "palette":['red', 'yellow']}, "BD cPoverty: Wealth Index", opacity=0.6)
Map.centerObject(aoi, 13)

#AOI: Sirajganj District (Khulna Division)
#___________________________________________
aoi = ee.Geometry.MultiPolygon(shp_to_ee_fmt(city = 'Sirajganj', level = 3))

# initialize the map
Map.addLayer(viirs.clip(aoi), {}, "VIIRS-DNB Nightlights", opacity=0.5)
Map.addLayer(ghslSet.clip(aoi), ghslSetVis, 'GHSL Degree of Urbanization', opacity=0.5)
Map.addLayer(ghslPop.clip(aoi), ghslPopVis, 'GHSL Population', opacity=0.5)
Map.addLayer(srtm.clip(aoi), {'min':5, 'max':25}, 'SRTM Elevation', opacity = 0.6)
Map.addLayer(water.clip(aoi), waterVis, 'JRC Water Prevalence', opacity = 0.6)
Map.addLayer(pov_inc.clip(aoi), {'min':120, 'max':210, "palette":['red', 'yellow']}, "BD Poverty: Income", opacity=0.6)
Map.addLayer(pov_wi.clip(aoi), {'min':-0.75, 'max':1.1, "palette":['red', 'yellow']}, "BD cPoverty: Wealth Index", opacity=0.6)
Map.centerObject(aoi, 13)


#AOI: Sirajganj District (Khulna Division) UPPR POVERTY LAYERS
#___________________________________________
aoi = ee.Geometry.MultiPolygon(shp_to_ee_fmt(city = 'Sirajganj', level = 3))

shp_path = os.path.join(path,"CRISC_RS","All","Poor_settlement_without_single.shp")
# UPPR feature collection: Sirajganj
# UPPR feature collection: Sirajganj
# shp_to_ee without geemap
import shapefile
shp_path = os.path.join(path,"CRISC_RS","All","Poor_settlement_without_single.shp")
in_gdf = gpd.read_file(shp_path)
out_gdf = in_gdf.to_crs(epsg="4326")
out_shp = shp_path.replace(".shp", "_gcs.shp")
out_gdf.to_file(out_shp)
in_shp = out_shp
reader = shapefile.Reader(in_shp)
out_dict = reader.__geo_interface__
uppr = ee.FeatureCollection(out_dict["features"])
#uppr = geemap.shp_to_ee(shp_path)
# Extract relevant polygons by class
p1 = uppr.filterMetadata('Pov_Quart','equals','Extremely Poor')
p2 = uppr.filterMetadata('Pov_Quart','equals','Marginally poor')
p3 = uppr.filterMetadata('Pov_Quart','equals','Moderately Poor')
p4 = uppr.filterMetadata('Pov_Quart','equals','Very Poor')

vis_params = {
    'color': '000000', 
    'pointSize': 1,
    'pointShape': 'circle',
    'width': 0.5,
    'lineType': 'solid',
}
#Extremely Poor
vis_params.update({"fillColor": "E30B17AA"})
Map.addLayer(p1.style(**vis_params), vis_params, 'UPPR: Extremely Poor')
#Marginally poor
vis_params.update({"fillColor": "CCCCCCAA"})
Map.addLayer(p2.style(**vis_params), vis_params, 'UPPR: Marginally Poor')
#Moderately Poor
vis_params.update({"fillColor": "FEEAC0AA"})
Map.addLayer(p3.style(**vis_params), vis_params, 'UPPR: Moderately Poor')
#Very Poor
vis_params.update({"fillColor": "FDA883AA"})
Map.addLayer(p4.style(**vis_params), vis_params, 'UPPR: Very Poor')
Map.centerObject(aoi, 12)
