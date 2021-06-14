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

# Get Sentinal
#aoi_bd = ee.Feature(ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh')).first()).geometry()
#first = (ee.ImageCollection('COPERNICUS/S2_SR')
         # .filterBounds(aoi_bd)
         # .filterDate('2019-01-01', '2019-12-31')
         # .sort('CLOUDY_PIXEL_PERCENTAGE')
         # .first())

#AOI: Satkhira District (Khulna Division)
aoi = ee.Geometry.MultiPolygon(shp_to_ee_fmt(city = 'Sirajganj', level = 3))

# initialize the map
Map.addLayer(viirs.clip(aoi), {}, "VIIRS-DNB Nightlights", opacity=0.5)
Map.addLayer(ghslSet.clip(aoi), ghslSetVis, 'GHSL Degree of Urbanization', opacity=0.5)
Map.addLayer(ghslPop.clip(aoi), ghslPopVis, 'GHSL Population', opacity=0.5)
Map.addLayer(srtm.clip(aoi), {'min':-1, 'max':14}, 'SRTM Elevation', opacity = 0.6)
Map.addLayer(water.clip(aoi), waterVis, 'JRC Water Prevalence', opacity = 0.6)
Map.centerObject(aoi, 13)
#Map.addLayer(
#    first.clip(aoi), {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 2000}, 'first')
