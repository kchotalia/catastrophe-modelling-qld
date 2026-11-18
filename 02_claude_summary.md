# Stage 2 Summary: Geospatial Basics & Coastal Exposure Data

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

## Visualisation
- `gdf.plot()` for a quick check; overlay layers by passing `ax=ax`
- Saving a plot: `ax.figure.savefig("name.png", dpi=300, bbox_inches="tight")`, in the **same cell** as the plot
- Axis styling: `fontweight="bold"` on `set_title`/`set_xlabel`/`set_ylabel`, or `plt.rcParams` for a session-wide default
- Legends: `label=` on each layer plus `ax.legend()`; `groupby("construction_type")` for one legend entry per type; a `Patch` for polygons that don't appear automatically
- Minor tick marks: `ax.minorticks_on()` (without calling `ax.grid()`), styled with `tick_params`
- Folium popups accept HTML built with f-strings (`<br>`, `<b>`, `:,.0f` for thousands separators); colours come from a `colour_map` dictionary (named colours for `Marker` icons, any hex code for `CircleMarker`); folium has no built-in legend
- The final map combines the simplified Queensland boundary, the coastal zone, colour-coded properties, a legend and a `LayerControl` toggle; `simplify(0.01)` keeps the HTML small for display only. Clear notebook outputs before committing so embedded maps don't bloat the `.ipynb`

## Python & debugging lessons
- A `SyntaxError` is often reported on the line *after* the real mistake — a missing comma at the end of the line above
- `df[:, 0]`-style slicing needs a numpy array, not a list; a ragged `np.array(...)` can come out as shape `(10,)` instead of `(10, 2)` — check `.shape` first
- `.within()` belongs to GeoDataFrames (`gdf`), not plain DataFrames (`df`)
- An assignment (`x = ...`) displays nothing in a notebook; a bare variable on the last line does
- Variable naming consistency matters (`m` vs `n` for different maps)

## What was built
- A seeded, reproducible exposure pipeline, and a synthetic QLD dataset restricted to a **50 km coastal zone** (`exposure_data_coastal.csv`): 10 properties, with every point confirmed inside Queensland and inside the coastal zone
- A separate rejection-sampling dataset (`exposure_data_resampled.csv`) in `02a_qld_boundary_resampling.ipynb`
- An interactive folium map of the properties over the boundary and coastal zone

## Next
- Join the properties to a hazard layer: Geoscience Australia's "1170.2 Wind Regions for Australia" dataset (published on data.gov.au as a zip of about 18 MB). For Queensland, Region A is non-cyclonic, B intermediate (e.g. Gold Coast) and C cyclonic (e.g. Cairns, Townsville, Mackay)
- Before joining, check the file's `.crs` and `.columns`, then reproject to match the points. Keep the download in a `data/` folder listed in `.gitignore`