## Option 2: Resampling to guarantee 10 valid QLD points (not used in main pipeline)

Option 1 generates 10 random lat/long points inside a rectangular bounding box around
Queensland. Since Queensland's real coastline isn't a rectangle, some of those points
inevitably land in the ocean or in neighbouring states — in our case, only 7 of 10
landed inside the real QLD boundary.

Option 2 fixes this using **rejection sampling**: generate candidate points one at a
time, check each against the real QLD boundary, and only keep the ones that fall
inside. Keep going until exactly 10 valid points have been collected.

### Concepts covered

- **`shapely.Point`**: represents a single location (like a labelled pin on a map).
  Immutable, and built from `(x, y)` — i.e. `(longitude, latitude)`, not `(latitude, longitude)`.
- **`Point` vs `GeometryArray`**: `gpd.points_from_xy()` always returns a collection
  (a `GeometryArray`), even for a single input — indexing with `[0]` or building a
  `Point` directly avoids this when only one point is needed.
- **Directionality of spatial checks**: `point.within(polygon)` asks "is this point
  inside that shape?" — the reverse, `polygon.contains(point)`, asks the same thing
  from the other direction. Both work; `shape.within(point)` does not (a shape can't
  fit inside a point).
- **`.coords` vs `.x`/`.y`**: `.coords` returns coordinates wrapped in a list of tuples
  (since geometries like `LineString` can have many), so a single `Point`'s coordinates
  come out nested — `.flatten()` or `.x`/`.y` avoid that extra nesting.
- **Reproducibility**: `np.random.seed(42)` set once, before any `np.random` calls,
  makes "random" generation deterministic — same seed, same points, every run. Without
  it, re-running the script silently produces a different dataset each time.
- **Rejection sampling**: generate a candidate, test it, keep it only if it passes —
  repeat until enough valid results are collected. A general-purpose technique used
  well beyond this project.

### What was built

A `while` loop that:
1. Generates a single random `(longitude, latitude)` point
2. Tests it against the real QLD boundary (`qld.union_all()`) using `.within()`
3. Appends it to `valid_points` only if it falls inside QLD
4. Repeats until 10 valid points are collected

The resulting coordinates were combined with freshly generated `construction_type`
and `sum_insured` values (same method as Stage 1) to build a complete 10-row exposure
dataset, saved separately as `exposure_data_resampled.csv`, and re-validated to confirm
all 10 points fall inside QLD.

### When is a `while` loop the right approach vs bulk-generate-and-filter?

At small scale (10 points), looping one candidate at a time is fine. At larger scale
(e.g. 10,000 rows), it isn't — `numpy`/`geopandas` operations are **vectorized**,
meaning a check like `.within()` can test an entire array of points against a boundary
in one fast call, rather than looping row-by-row in (much slower) native Python.

**The scaled-up equivalent of this loop** would instead:
1. Generate more candidate points than needed at once (e.g. 15,000, anticipating the
   ~70% hit rate observed for QLD within its bounding box)
2. Run a single vectorized `.within()` check across all of them, producing a `True`/`False`
   column
3. Filter to the `True` rows and trim to the exact number needed

This is essentially Option 1's method, scaled up with a buffer to guarantee enough
valid rows — two fast vectorized operations instead of thousands of individual Python
loop iterations.

**When a loop genuinely is the better choice:**
- The valid/invalid "hit rate" is unknown or very low, so it's hard to guess how many
  extra candidates to bulk-generate up front
- Each candidate depends on a more complex, sequential process (e.g. simulating a
  multi-step cyclone track) rather than a single independent random draw
- While learning or debugging the underlying logic, since a loop is easier to reason
  about step-by-step than a single vectorized operation

**General principle:** vectorize when the operation is uniform across rows and the
expected yield is roughly predictable (most data-generation/filtering tasks, including
this project at scale). Loop when the process is inherently sequential, the yield is
unpredictable, or clarity while learning matters more than raw speed.