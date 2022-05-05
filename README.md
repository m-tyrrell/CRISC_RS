# Repo for preliminary CRISC Remote Sensing analyses

## Project: GIZ 81263741 - Climate Resilient Inclusive Smart Cities (CRISC)
CRISC tackles the core issue of national and local-decision makers in urban development who are not in a position to systematically shape their development and investment planning both in a climate-sensitive manner and in accordance with the local needs of the vulnerable population. The project uses the methodological approach of promoting planning capacities and investment decisions for climate resilient and inclusive urban development through training and advisory services.

## Analysis
GIS Analyses for 2 Bangladeshi cities (Srirajganj and Satkhira) in QGIS format (Google Earth Engine plugin): using the following layers masked for GAUL Administrative Level 3 ('Sadar'):
1. OSM
2. VIIRS Nightlights Average Radiance 2019 median (approx. 500m resolution; B&W scale from dark to light indicating higher luminance)
3. GHSL Settlements Classification 2015 (1Km resolution)
- Black: Inhabited areas
- Dark Green: RUR (rural grid cells)
- Light Green: LDC (low density clusters)
- White: HDC (high density clusters)
4. GHSL Population Estimations 2015 (250m resolution with scale from dark to light colours indicating higher population)
5. SRTM Elevation (90m resolution; B&W scale from dark to light indicating higher elevation values)
6. JRC Water surface levels: Occurrence 1984-1999, 2000-2020 (30m resolution; scale from light to dark blue indicating higher water prevalence; no colour = water never detected)
7. Flowminder Bangladesh poverty estimates (2011-2013) by 1km grid (https://royalsocietypublishing.org/doi/full/10.1098/rsif.2016.0690)
8. Sirajgang ONLY - UPPR poverty data as a project in the geopackage. 

 
**Info on the two files:**
Satkhira (RS_Satkhira.qgz) - note this is a simple qgz file that links from GEE.
Sirajganj (RS_Sirajganj.gpkg) - 2 projects in the geopackage:
-'UPPR Poverty' contains only the UPPR poverty layers;
-'Sirajganj Multi' contains all layers.
