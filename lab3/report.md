
# Lab 3: District Dashboard — Layers, Controls and Interaction

---

## Checkpoint 1: Set Up the Project

![Checkpoint 1 — Project Structure](screenshots/Checkpoint%201.png)

The Lab 3 project was created in the existing WebGIS repository while preserving Lab 2. Separate `index.html`, `style.css`, and `app.js` files were created, and the district GeoJSON data from Lab 2 was reused in the `lab3/data` folder.

---

## Checkpoint 2: Make a Point Layer in QGIS

![Checkpoint 2 — Centroid and Point on Surface](screenshots/Checkpoint%202.png)

### Centroid and Point-on-Surface Comparison

The Centroids and Point on Surface tools were applied to the district polygons in QGIS.

The comparison identified **Sibi, Balochistan**, as the district whose geometric centroid falls outside its own boundary.

The Point on Surface tool was selected for the population symbols because it guarantees that each point lies inside its corresponding district. This prevents a symbol from appearing to represent a neighbouring district.

### Exported Point Layer

| Measurement | Result |
|---|---|
| Output file | `district_points.geojson` |
| Feature count | 160 |
| Coordinate system | EPSG:4326 — WGS 84 |
| Coordinate precision | 5 decimal places |
| File size | **[Enter actual file size]** |

The exported point layer retains the district attributes, including `pop_2023`, for use in proportional-symbol mapping.

---

## Checkpoint 3: The Page, Map and Basemaps

![Checkpoint 3 — Esri Tile Request](screenshots/Checkpoint%203.png)

Three basemaps were configured in Leaflet:

- Light (Carto Positron)
- OpenStreetMap
- Satellite (Esri)

The layer control allows the user to switch between basemaps while preserving the thematic overlays.

### Esri Tile URL Inspection

The Network tab was used to inspect a successful Esri satellite tile request.

**Recorded request URL:**

`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/5/12/22`

| URL Component | Value | Description |
|---|---|---|
| Zoom level (`z`) | 5 | Map zoom level |
| Tile row (`y`) | 12 | Tile row |
| Tile column (`x`) | 22 | Tile column |

**Answer:** Esri uses the URL order `{z}/{y}/{x}`. The first number indicates the zoom level, the second identifies the tile row, and the third identifies the tile column.

The request returned HTTP status **200 OK**, confirming successful loading of the satellite tile.

---

## Checkpoint 4: Population Density Choropleth

![Checkpoint 4 — Population Density Map](screenshots/Checkpoint%204.png)

The district boundaries were displayed as a population-density choropleth using the 2023 census population and district area.

Population density was calculated using:

**Population density = Population / Area (km²)**

The map uses five blue classes to represent population density.

### Population Density Classification

| Population Density (people/km²) | Colour |
|---|---|
| Up to 50 | Very light blue |
| Above 50 to 150 | Light blue |
| Above 150 to 400 | Medium blue |
| Above 400 to 1,000 | Dark blue |
| Above 1,000 | Very dark blue |
| Missing census data | Grey |

### Why Use Population Density?

Population density allows districts of different geographical sizes to be compared meaningfully.

Unlike total population, density accounts for the area occupied by the population. Therefore, it is more appropriate for colouring administrative polygons.

The dashboard successfully displays **160 districts**, a population-density legend, and a layer control containing the three basemaps and thematic overlay.

---

## Checkpoint 5: Hover Highlighting and Information Panel

![Checkpoint 5 — District Highlighting](screenshots/Checkpoint%205.png)

### District Zoom Interaction

![Checkpoint 5 — Zoom to District](screenshots/Checkpoint%205%20zoom%20in.png)

The dashboard was configured with mouseover, mouseout and click events for district polygons.

### Hover Highlighting

When the cursor moves over a district:

- Its boundary becomes thicker and darker.
- A tooltip displays the district name.
- The information panel updates with the district attributes.

The information panel displays the district name, province, population, area, population density and current zoom level.

### Example: Kohlu District

| Attribute | Value |
|---|---|
| District | Kohlu |
| Province | Balochistan |
| Population | 260,220 |
| Area | 7,728.1 km² |
| Population density | Approximately 34 people/km² |

When the cursor moves away, `resetStyle()` restores the original district symbology.

Clicking a district activates `fitBounds()`, which adjusts the map view to the selected district's geographical extent.

The district information panel was positioned at the bottom-left to avoid overlapping with the layer control and legend.

---

## Checkpoint 6: Proportional Symbols in Their Own Pane

### Population Circles and Density Map

![Checkpoint 6A — Proportional Population Symbols](screenshots/Checkpoint%206A.png)

Population was represented using proportional orange circle markers placed above the population-density polygons.

A separate pane named `symbols`, with a z-index of 450, ensures that the circles remain visible above the district polygons.

### Circle Size Calculation

The circle radius was calculated using:

`radius = Math.sqrt(population) / 160`

The square root was used because the area of a circle increases with the square of its radius. This ensures that the visual area of each circle is proportional to the district population.

Districts with missing population values were excluded from the proportional-symbol layer.

The legend provides reference circles for populations of 1 million, 4 million and 10 million.

### NUST Overlay — Zoom Level 5

![Checkpoint 6B — NUST Zoom Level 5](screenshots/Checkpoint%206B%20Nust%205.png)

At zoom level 5, the 25 km geographical circle around NUST appears relatively small on the national map.

### NUST Overlay — Zoom Level 10

![Checkpoint 6B — NUST Zoom Level 10](screenshots/Checkpoint%206B%20Nust%2010.png)

At zoom level 10, the same geographical circle occupies a much larger portion of the screen, while the 6-pixel circle marker maintains approximately the same visual size.

### Observation

`L.circle()` defines its radius in metres and represents a geographical distance.

In contrast, `L.circleMarker()` defines its radius in screen pixels and remains visually consistent across zoom levels.

The 25 km geographical circle can also be compared with the map's distance scale bar.

---

## Checkpoint 7: Map Events — On and Off

![Checkpoint 7 — Coordinate Popup](screenshots/Checkpoint%207.png)

The coordinate-click handler was implemented using a checkbox that enables or disables coordinate popups on the map.

### Experiment 1: Coordinate Clicks

With the checkbox enabled, clicking the Arabian Sea south of Karachi displayed a popup containing the selected location's coordinates.

**Recorded coordinates:**

- Latitude: 24.6836° N
- Longitude: 66.6650° E

District polygons also have their own click handler, which zooms to the selected district. With the coordinate option enabled, map-level coordinate events can also occur.

### Experiment 2: Legend Click Propagation

The legend uses `L.DomEvent.disableClickPropagation()` to prevent clicks inside the legend from activating the underlying map.

When this protection is removed temporarily, legend clicks can propagate to the map and activate the coordinate-click handler.

Restoring `disableClickPropagation()` prevents this unwanted interaction.

### Experiment 3: Disabling Coordinate Popups

When the checkbox is unchecked, the `showCoordinates` handler is removed through `map.off()`.

Further clicks on the sea no longer generate coordinate popups.

### Explanation

The named function `showCoordinates` can be registered using `map.on()` and removed using `map.off()` because both operations refer to the same function.

This demonstrates controlled event registration and removal in Leaflet.

---

## Checkpoint 8: Filter by Province (Extension)

![Checkpoint 8 — Gilgit Baltistan Filter](screenshots/Checkpoint%208.png)

The province filter was tested by selecting **Gilgit Baltistan** from the drop-down menu.

### Observed Results

| Measurement | Result |
|---|---|
| Selected province | Gilgit Baltistan |
| Number of districts | 14 |
| Population density shading | Grey |
| Proportional population circles | Not displayed |
| Population density overlay | Enabled |
| Population overlay | Enabled |

All 14 districts appeared grey because the supplied dataset does not contain population values for these districts.

No proportional population circles were displayed because the `hasPopulation()` filter excludes features with missing `pop_2023` values.

### Interpretation

The absence of circles represents missing census information, not zero population.

The dashboard should clearly communicate the unavailability of population data to prevent misleading interpretations.

The layer control uses persistent feature groups, allowing the district layers to be rebuilt after province filtering while maintaining overlay controls.

---

## Checkpoint 9: SVG Versus Canvas Rendering (Extension)

### SVG Rendering

![Checkpoint 9 — SVG Elements](screenshots/Checkpoint%209%20SVG.png)

### Canvas Rendering

![Checkpoint 9 — Canvas Element](screenshots/Checkpoint%209%20Canvas.png)

### Drawing-Time Measurements

Five measurements were recorded for each rendering mode using the browser Developer Tools Console.

**SVG measurements (ms):**

54.0, 35.7, 34.3, 41.7, 45.3

**Canvas measurements (ms):**

66.0, 55.5, 35.7, 37.1, 36.1

### Median Calculations

Sorted SVG values:

34.3, 35.7, **41.7**, 45.3, 54.0

**SVG median = 41.7 ms**

Sorted Canvas values:

35.7, 36.1, **37.1**, 55.5, 66.0

**Canvas median = 37.1 ms**

### Renderer Comparison Table

| Measurement | SVG | Canvas |
|---|---|---|
| `draw(all)`, median of five (ms) | 41.7 ms | 37.1 ms |
| Elements inside `leaflet-overlay-pane` | 160 SVG paths | 1 canvas |
| Hover highlighting still works? | Yes | Supported by Leaflet; verify interactively |
| Can one district be inspected in Elements? | Yes, as an SVG path | No individual DOM path |

### Interpretation

The measured median drawing time was **41.7 ms for SVG** and **37.1 ms for Canvas**.

Canvas was approximately **4.6 ms faster**, a relatively small difference for the 160-district dataset.

SVG represented the districts using 160 individual path elements in the browser's Document Object Model (DOM).

Canvas used a single drawing surface to render the polygon geometries, reducing the number of DOM elements.

### Expected Performance with a Tehsil-Level Dataset

A tehsil-level administrative dataset would contain more geographic features and often more complex boundaries than the district dataset.

SVG requires separate DOM elements for rendered geographic paths, increasing element-management and rendering overhead as the number of features grows.

Canvas draws many geographical features on shared drawing surfaces, reducing DOM overhead.

Therefore, Canvas would be expected to offer greater performance advantages for a dataset containing thousands of features, although the actual improvement depends on geometry complexity, browser performance and hardware.

---

# Section 10.3: Final Questions

## Question 1

**Lab 2 shaded districts by population. Name one large, thinly populated district and one small, crowded one, and explain how each would mislead on the Lab 2 map.**

**Answer:**

Chagai in Balochistan is a large, sparsely populated district, with approximately 269,192 people across 44,476.9 km².

Lahore is comparatively small but highly populated, with approximately 13,004,135 people across 1,729.9 km².

On a population-count choropleth, Chagai occupies a very large geographical area despite its low population density, while Lahore appears as a relatively small polygon despite containing a highly concentrated population.

This can lead viewers to misinterpret population distribution because polygon area strongly influences visual attention.

Population density is more appropriate for a choropleth because it accounts for geographical area and allows meaningful comparisons between districts.

## Question 2

**radiusFor takes a square root. What would the map suggest about Lahore against a district of 3 million if it did not?**

**Answer:**

Lahore has approximately 13 million people, about 4.3 times the population of a district containing 3 million people.

Without the square root, circle radius would increase directly with population. Because circle area increases with the square of its radius, Lahore's circle would appear approximately 18.8 times larger in area.

This would greatly exaggerate the population difference.

Taking the square root ensures that circle area, rather than radius, remains proportional to population.

## Question 3

**Why does the layer control hold districtGroup rather than the L.geoJSON layer itself?**

**Answer:**

The `districtGroup` is a persistent feature group that remains available even when its contents are cleared and rebuilt.

When the user changes the province, a new GeoJSON layer is created and added to this group.

If the layer control referenced the original GeoJSON layer directly, it would continue pointing to an outdated layer after filtering.

Using `districtGroup` ensures that the overlay control remains functional when the selected province changes.

## Question 4

**What would go wrong if the circles were drawn in overlayPane instead of the symbols pane? Describe what the user would see when hovering.**

**Answer:**

If the population circles and district polygons were placed in the same overlay pane, hovering over a district would call `bringToFront()` and move the highlighted polygon above the circles.

Consequently, some population circles could become hidden behind the highlighted polygon.

The separate `symbols` pane, with a higher z-index than the default overlay pane, ensures that proportional circles remain visible above the district polygons during hover interactions.

## Question 5

**Why can map.off remove showCoordinates, when it could not remove an anonymous function passed to map.on?**

**Answer:**

`showCoordinates` is a named function, allowing the same function reference to be passed to both `map.on()` and `map.off()`.

Leaflet identifies the registered handler using this function reference and removes it when the checkbox is disabled.

An anonymous function passed directly to `map.on()` without storing its reference cannot later be matched by `map.off()`.

Therefore, named or stored function references are necessary when event handlers need to be removed.

## Question 6

**On the NUST overlay, which circle would you use to show a 25 km evacuation zone, and which to mark the campus on a national map? Why?**

**Answer:**

I would use `L.circle()` to represent the 25 km evacuation zone because its radius is specified in metres and represents a real-world geographical distance.

I would use `L.circleMarker()` to represent the NUST campus location on a national map because its radius is measured in pixels and remains visually consistent across different zoom levels.

Therefore, `L.circle()` is appropriate for distance-based geographical zones, whereas `L.circleMarker()` is suitable for displaying point locations.

---
