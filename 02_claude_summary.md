# Stage 2 Summary: Geospatial Basics, Coastal Exposure Data & Wind Regions

## Environment & tooling
- Installed `geopandas`, `shapely` and `folium` into the existing venv, and verified with `pip list` and an import check (geopandas 1.1.4 — a recent `1.x` release, so older `0.x` tutorials can occasionally have outdated syntax)
- The first `matplotlib` plot took ~26 seconds because it builds a font cache once; later plots were instant
- Folium maps showing the message *"Make this notebook trusted… File → Trust Notebook"* — that text comes from `branca` (folium's dependency) and is written for classic Jupyter; VS Code has no such menu. It is a known VS Code/Jupyter rendering bug, not a trust problem. Workarounds:
  - add a markdown cell below the map, or restart/reopen VS Code, to force a repaint
  - `m.show_in_browser()` or `m.save("name.html")` plus Live Preview
  - render through an `IFrame`, or update `folium` and `ipywidgets` and reload the window
- A cell only displays a map if the map variable is the **last line** of the cell — an assignment or a loop on its own prints nothing
- Pin icons (`folium.Marker` with the default icon) can fail to appear inline even when the HTML file shows them; `folium.CircleMarker` draws plain vector shapes and avoids this
- Updating a GitHub token: sign out and back in via VS Code's Accounts icon, or generate a new personal access token, clear the cached one with `git credential-osxkeychain erase`, and check `git remote -v` for an embedded old token. VS Code shows git login prompts as an input box at the top of the window, not in the terminal
- Previewing markdown in VS Code: Cmd+Shift+V (new tab) or Cmd+K then V (side by side)
- Naming notebooks with zero-padded numbers (`02a_...`) keeps file sorting predictable once there are 10+ files

## Geospatial concepts
- **Goal of the stage:** give the exposure data spatial awareness — so questions like "is this property inside this zone?" can be answered in code, not by eyeballing a map
- A **GeoDataFrame** is a DataFrame plus a `geometry` column, built with `gpd.points_from_xy(longitude, latitude)` — **x is longitude, y is latitude**, the reverse of how we say "lat/long"
- **`shapely.Point`** is a single immutable location, like one labelled pin on a map. It gains abilities plain numbers lack: `.within()`, `.distance()`, `.buffer()`
- One pin vs a box of pins: `points_from_xy()` always returns a `GeometryArray` (a collection), even for one input, so `.coords` fails on it. Use `[0]` or build a single `Point(long, lat)` directly
- `.coords` wraps coordinates in an extra layer; `.x`/`.y` or `.flatten()` avoid the nesting
- **Direction matters:** `point.within(polygon)` is the same question as `polygon.contains(point)`; `polygon.within(point)` is meaningless
- `qld.union_all()` merges a GeoDataFrame's geometries into one shape (Queensland is a `MultiPolygon` because of offshore islands)
- Real boundary data from Natural Earth's Admin 1 states/provinces dataset, read directly from a zipped URL and filtered with `name == "Queensland"` and `iso_a2 == "AU"` (the dataset has 122 columns, mostly translated names). The ABS official state boundaries are a more precise alternative to swap in later
- Sampling inside a rectangular bounding box around Queensland puts points in the ocean and in other states (7 of 10 landed inside), because the state isn't a rectangle

## Reproducibility & sampling
- **Random seeds:** `np.random.seed(42)`, set once before any random calls, makes the data identical on every run. Without it, re-running the script silently changed the dataset and made earlier results (`in_qld`, the CSV, the map) stale
- **Option 1:** filter to the valid points (`gdf[gdf["in_qld"]]`, then `.reset_index(drop=True)` to clean up the index gaps)
- **Option 2 (`02a` notebook):** **rejection sampling** — generate a candidate, test it, keep it only if valid, repeat until enough are collected. Built as a `while` loop with single `Point` objects
- **Loop vs vectorised:** at scale, generate a large batch, add a True/False column with `.within()`, and filter — much faster than a Python loop. A loop is better when the yield is unknown, the process is sequential, or clarity matters while learning
- **Hit rate:** the mean of a boolean column is the fraction of `True` values. Candidates needed ≈ target ÷ hit rate, plus a safety margin
- **Exact vs estimated area:** polygon `.area` is exact (the shoelace formula, a sum over edges); the sampled hit rate is a Monte Carlo estimate of the same ratio, with error shrinking like 1/√n. Comparing them is a useful sanity check

## Coastal buffer
- A cat model needs exposure near the coast; the filtered points were mostly inland (longitudes 145–148.5)
- **CRS:** `EPSG:4326` is lat/long in degrees; `EPSG:3577` (Australian Albers) is in metres. Buffer in metres, not degrees, so the distance is real. `set_crs()` labels coordinates; `to_crs()` converts them. Everything must share a CRS before geometries are compared
- **Two traps:** buffer units depend on the CRS, and shrinking Queensland alone would also strip strips along the NSW/NT/SA land borders. Fix: build the shape from **all of Australia**, shrink it 50 km (a negative buffer), subtract that interior, and intersect the strip with Queensland
- Reading the plot: the unbroken rim around the coast, tiny islands vanishing entirely under the shrink (counted as coast), and Queensland looking tilted in Albers is just the projection — shapes shift, areas stay true
- Sampled hit rate 0.057 vs exact area ratio 0.0603 — consistent within sampling noise (standard error ≈ 0.005 at 2,000 candidates)
- **Known limitation:** sampling uniformly across the strip puts many points in sparsely populated Cape York and none in South East Queensland. Weighting by population would be more realistic

## Hazard layer: AS/NZS 1170.2 wind regions
- Source: Geoscience Australia's "1170.2 Wind Regions for Australia" (data.gov.au), a shapefile in GDA2020 (`EPSG:7844`). Several files make up one shapefile (`.shp`, `.dbf`, `.shx`, `.prj`, ...) and must stay together; geopandas loads the `.shp` and finds the rest
- Reading the `.shp.xml` metadata and the specification PDF: the data reflects the **2021 edition** of the standard (produced February 2022), is licensed CC BY 4.0, is Geoscience Australia's indicative interpretation, and is not suitable for design purposes (the standard prevails)
- Columns: `region` is the wind region code (A0 to A5, B1, B2, C, D); `area` is a place name for the polygon. I initially treated `area` as a size and had to correct that — check the data dictionary before assuming what a column holds. `Shape_Leng`/`Shape_Area` are in degrees, so ignore them for real measurements
- How the zones were built: the ASGS coastline was smoothed (50 km tolerance), buffered inland by 50, 100, 150 and 200 km, subtracted into bands, and intersected with zone definitions; all remaining interior is A0. This is the same negative-buffer idea used for the coastal zone above
- The codes are labels, not wind speeds, and the PDF does not define them. The layer has only 20 polygons, so the zones are coarse
- Attribution (required by CC BY): credit Geoscience Australia, link the licence, state that the data was reprojected and joined, and imply no endorsement. Keep the download in a `data/` folder listed in `.gitignore`

## Spatial joins
- `gpd.sjoin(left, right, how="left", predicate="within")` is a SQL `LEFT JOIN` where the match condition is spatial: each property picks up the attributes of the polygon it falls in
- `how="left"` keeps every property (unmatched ones get `NaN`); `how="inner"` silently drops unmatched properties
- The new columns (`area`, `region`, `index_right`) are always added; only their values depend on a match. `index_right` is the row number of the matching polygon, and should be dropped before any second join
- `within` is strict: a point exactly on an edge matches nothing, and ends up as `NaN`. `intersects` also counts the edge, so a point on a shared edge matches two polygons and is duplicated into two rows — which would double-count `sum_insured` in any total
- Checks after every join: `len(joined)` (10 means no duplicates and no dropped rows) and `joined["region"].isna().sum()` (0 means every property found a polygon). The row count alone cannot show an unmatched property
- Reproject the polygon layer to the points' CRS first (`wind.to_crs(gdf_coastal.crs)`)
- Result: 10 properties, 9 in region C and 1 in B1 (policy 3, just south of 25°S). The B1/C change appears as a straight horizontal edge near 25°S on the plot, so two properties about 40 km apart get different labels — a cliff edge that continuous wind speeds (Stage 3) avoid. I have not checked that line against Figure 3.1 of the standard
- Zoomed plots showed the points clearly inside their polygons, not sitting on edges

## Visualisation
- `gdf.plot()` for a quick check; overlay layers by passing `ax=ax`
- Saving a plot: `ax.figure.savefig("name.png", dpi=300, bbox_inches="tight")`, in the **same cell** as the plot
- Axis styling: `fontweight="bold"` on `set_title`/`set_xlabel`/`set_ylabel`, or `plt.rcParams` for a session-wide default
- Legends: `label=` on each layer plus `ax.legend()`; `groupby("construction_type")` for one legend entry per type; a `Patch` for polygons that don't appear automatically
- Minor tick marks: `ax.minorticks_on()` (without calling `ax.grid()`), styled with `tick_params`
- **Consistent colours:** geopandas spreads its colour map across however many categories are in the data it is given, so the same region changed colour between plots (4 regions vs 10). Fix with a fixed `region_colours` dictionary and a `groupby` loop
- Folium popups accept HTML built with f-strings (`<br>`, `<b>`, `:,.0f` for thousands separators). Adjacent string literals are joined with nothing between them, so a missing `<br>` silently glues two lines together
- The final map: wind regions (clipped to Queensland with `gpd.clip`, simplified, coloured from `region_colours`, with a hover tooltip), the Queensland outline, a coastal zone that starts switched off, properties coloured by construction type, two legends, and a layer toggle. Layers draw in the order they are added, so put the wind layer first. `show=False` needs a real boolean — the string `'False'` is truthy and leaves the layer on
- Marker shapes instead of colour: `folium.DivIcon` with small HTML/CSS shapes (triangle via `clip-path`, square, circle via `border-radius`), which also avoids image-file icons; this frees colour to show wind region
- `itertuples()` is faster and cleaner than `iterrows()` in the marker loop (`r.policy_id` instead of `row['policy_id']`)
- `simplify(0.01)` keeps the saved HTML small; it is for display only, and the original layers are used for spatial work. Clear notebook outputs before committing so embedded maps don't bloat the `.ipynb`

## Project structure: `mapping.py`
- Reusable folium helpers (`simplified`, `add_layer`, `add_legend`) moved into `mapping.py` beside the notebooks and imported with `from mapping import ...`. Dataset-specific colour dictionaries stay in the notebook
- `%load_ext autoreload` and `%autoreload 2` re-import the module whenever it changes, avoiding kernel restarts
- This follows the hybrid approach from Stage 1: notebooks for exploration, `.py` files for reusable logic
- A rewrite that looked more efficient was mostly about reducing repetition and improving reuse, not speed: with 10 points the runtime is trivial

## Python & debugging lessons
- A `SyntaxError` is often reported on the line *after* the real mistake — a missing comma at the end of the line above
- `df[:, 0]`-style slicing needs a numpy array, not a list; a ragged `np.array(...)` can come out as shape `(10,)` instead of `(10, 2)` — check `.shape` first
- `.within()` belongs to GeoDataFrames (`gdf`), not plain DataFrames (`df`)
- A `KeyError: 'region'` came from looping over `gdf_coastal` (made before the join) instead of `joined`; `sjoin` returns a new table and leaves the original unchanged
- An assignment (`x = ...`) displays nothing in a notebook; a bare variable on the last line does
- Variable naming consistency matters (`m` vs `n` for different maps)

## What was built
- A seeded, reproducible exposure pipeline, and a synthetic QLD dataset restricted to a **50 km coastal zone**: 10 properties, with every point confirmed inside Queensland and inside the coastal zone
- That dataset joined to the AS/NZS 1170.2 wind regions and saved as `exposure_data_coastal_wind.csv`
- A separate rejection-sampling dataset (`exposure_data_resampled.csv`) in `02a_qld_boundary_resampling.ipynb`
- An interactive folium map with wind regions, the boundary, the coastal zone, and properties with popups showing wind region
- `mapping.py` with reusable map helpers

## Next
- Stage 3, hazard modelling: define a synthetic cyclone track, measure each property's distance to it (in metres, `EPSG:3577`), and turn distance into a wind speed with a parametric profile (Holland model). Wind speed per property replaces the coarse zone label
- Optional: sample the portfolio so each wind region is represented, since 9 of 10 properties currently fall in region C