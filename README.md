# Catastrophe Modelling in Insurance — QLD Cyclone Exposure
 
Learning project applying an insurance pricing background to catastrophe modelling, building a simplified cyclone loss model for Queensland using Python. Each stage is documented in its own notebook, with the reasoning, mistakes and fixes included.
 
## Stages
- [x] Stage 1: Synthetic exposure data & pandas fundamentals
- [x] Stage 2: Geospatial basics, coastal exposure data & wind regions
- [ ] Stage 3: Hazard modelling (parametric wind field from a cyclone track)
- [ ] Stage 4: Vulnerability curves
- [ ] Stage 5: Financial loss module
- [ ] Stage 6: Stochastic event simulation
## What's in the repo
- `01_exposure_exploration.ipynb` — Stages 1 and 2: synthetic exposure data, GeoDataFrames, the Queensland boundary, a 50 km coastal zone, and a spatial join to wind regions
- `02a_qld_boundary_resampling.ipynb` — side quest: rejection sampling to guarantee points fall inside Queensland
- `mapping.py` — reusable folium helpers (layer, legend and simplification functions)
- `exposure_data_coastal_wind.csv` — the Stage 2 output: 10 synthetic coastal properties with a wind region
- `outputs/` — saved interactive maps (HTML)
## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy geopandas shapely folium matplotlib jupyter ipykernel
```
 
The wind regions shapefile is not included in the repo (see below). Download it from the link in "Data sources" and unzip it into a `data/` folder before running the Stage 2 join.
 
## Data sources and attribution
- **Wind region boundaries:** "1170.2 Wind Regions for Australia", Geoscience Australia (data.gov.au), https://data.gov.au/data/dataset/1170-2-wind-regions-for-australia. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The dataset is Geoscience Australia's indicative interpretation of AS/NZS 1170.2:2021 and is not suitable for design purposes; the standard takes precedence. Used here for a learning project only, reprojected and spatially joined to synthetic property locations. No endorsement by Geoscience Australia or Standards Australia is implied.
- **State boundaries:** Natural Earth, Admin 1 – States, Provinces (public domain), https://www.naturalearthdata.com/
## Known limitations
- All property data is synthetic. Locations are sampled uniformly across a 50 km coastal strip, so they cluster in sparsely populated Far North Queensland and none fall in South East Queensland; a population-weighted sample would be more realistic.
- Wind regions are coarse zone labels from a 20-polygon dataset, not wind speeds. Two properties close together can fall either side of a zone boundary. Stage 3 replaces the label with a continuous wind speed.
- This is a simplified teaching model, not a commercial catastrophe model, and the outputs are not suitable for pricing or underwriting.
 