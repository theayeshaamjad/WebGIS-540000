
# Lab 3: District Dashboard — Layers, Controls and Interaction

**Interactive web map:** [View the published Lab 3 dashboard](https://theayeshaamjad.github.io/WebGIS-540000/lab3/)

**GitHub repository:** [WebGIS-540000](https://github.com/theayeshaamjad/WebGIS-540000)

---

## Checkpoint 1: Set Up the Project

![Checkpoint 1 — Lab 3 project structure](Checkpoint%20Screenshots/Checkpoint%201.png)

Lab 3 was created as a separate folder in the existing WebGIS repository, preserving the Lab 2 map. The project uses `index.html`, `style.css`, and `app.js`, with the district GeoJSON copied from Lab 2 into `lab3/data/`.

---

## Checkpoint 2: Make a Point Layer in QGIS

![Checkpoint 2 — Centroid and point on surface](Checkpoint%20Screenshots/Checkpoint%202.png)

The **Centroids** and **Point on Surface** tools were applied to the district polygons. **Sibi, Balochistan**, is the irregularly shaped district whose geometric centroid was identified outside its boundary. A point on surface is guaranteed to lie inside its own polygon, making it more suitable for placing district population symbols.

### Exported Point-Layer Measurements

| Item | Recorded Value |
|---|---|
| File | `district_points.geojson` |
| Number of point features | **160** |
| Coordinate reference system | **EPSG:4326 (WGS 84)** |
| Export coordinate precision | **5 decimal places** |
| File size | **64.7 KB (66,291 bytes)** |

The point features inherit district attributes, including `pop_2023`, which is used to size the proportional symbols.

---

## Checkpoint 3: The Page, Map and Basemaps

![Checkpoint 3 — Esri tile request in Network tab](Checkpoint%20Screenshots/Checkpoint%203.png)

The Leaflet layer control offers three basemaps: **Light (Carto Positron)**, **OpenStreetMap**, and **Satellite (Esri)**. The Network tab was used to inspect an Esri World Imagery tile request.

**Observed Esri request URL:**

`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/5/12/22`

| URL Component | Value | Meaning |
|---|---:|---|
| `z` | 5 | Zoom level |
| `y` | 12 | Tile row |
| `x` | 22 | Tile column |

**Answer:** The Esri tile URL uses `{z}/{y}/{x}` order. The screenshot shows an HTTP **200 OK** response, confirming the selected satellite tile loaded successfully. The default district map was subsequently viewed over OpenStreetMap because the CARTO tiles displayed an API-key notice.

---

## Checkpoint 4: Population Density Choropleth

![Checkpoint 4 — Density map, legend and layer control](Checkpoint%20Screenshots/Checkpoint%204.png)

District polygons were shaded using **population density**, calculated dynamically from `pop_2023 / area_km2`. Density (people per km²) is more appropriate for a choropleth than a total-population count because it accounts for different district areas.

| Population Density (people/km²) | Map Colour |
|---|---|
| 50 or below | Very light blue |
| Above 50 to 150 | Light blue |
| Above 150 to 400 | Medium blue |
| Above 400 to 1,000 | Dark blue |
| Above 1,000 | Very dark blue |
| Missing census population | Grey |

The dashboard displayed **160 districts**, a density legend, and a layer control with three basemaps and the **Population density** overlay.

---

## Checkpoint 5: Highlighting and an Information Panel

![Checkpoint 5 — District hover interaction](Checkpoint%20Screenshots/Checkpoint%205.png)

![Checkpoint 5 — Zoom to selected district](Checkpoint%20Screenshots/Checkpoint%205%20zoom%20in.png)

Hovering over a district darkens and thickens its outline, displays a tooltip, and updates the district information panel. Moving the pointer away calls `resetStyle()` to restore its original colour. Clicking a district calls `fitBounds()` to zoom to its extent. The information panel was positioned at bottom-left so that it does not overlap the legend or layer control.

---

## Checkpoint 6: Proportional Symbols in Their Own Pane

### District Population Circles

![Checkpoint 6A — Population symbols above the density layer](Checkpoint%20Screenshots/Checkpoint%206A.png)

The dashboard represents **population counts** using orange proportional circle markers placed above the blue density polygons. The markers use a separate pane named `symbols` with `z-index: 450`, keeping them above the default polygon overlay pane (`z-index: 400`). Districts with missing census population values are excluded from the circle layer.

The radius is calculated as `Math.sqrt(population) / 160`. Taking the square root makes **circle area**, rather than radius, proportional to population. The circle legend shows references for 1 million, 4 million and 10 million people.

### NUST Overlay — Zoom Level 5

![Checkpoint 6B — NUST overlay at zoom level 5](Checkpoint%20Screenshots/Checkpoint%206B%20Nust%205.png)

### NUST Overlay — Zoom Level 10

![Checkpoint 6B — NUST overlay at zoom level 10](Checkpoint%20Screenshots/Checkpoint%206B%20Nust%2010.png)

At zoom level 5, the 25 km geographic circle around NUST appears small at the national scale. At zoom level 10, it takes up a much larger screen area, while the 6-pixel campus marker stays approximately the same screen size.

**`L.circle()` measures radius in metres; `L.circleMarker()` measures radius in pixels.** The 25 km circle can be compared with the Leaflet scale bar.

---

## Checkpoint 7: Map Events — On and Off

![Checkpoint 7 — Coordinate popup over the Arabian Sea](Checkpoint%20Screenshots/Checkpoint%207.png)

The **Show coordinates on click** checkbox adds or removes a map click handler.

### Part 7.3 — Event Experiments

**1. Click the sea, then a district with the checkbox enabled.**

Clicking the Arabian Sea south of Karachi produced the coordinate popup shown in the screenshot: **24.6836°N, 66.6650°E**. A district click also activates the district's click-to-zoom behaviour; the map-level coordinate handler can run as well when the click reaches the map.

**2. Click the legend with and without click-propagation protection.**

`L.DomEvent.disableClickPropagation(div)` prevents legend clicks from reaching the map. Temporarily removing it allows a legend click to propagate and activate the map's coordinate handler. The protection must be restored after testing.

**3. Untick the checkbox and click the sea.**

Once the checkbox is turned off, `map.off('click', showCoordinates)` removes the handler, so subsequent sea clicks do not create new coordinate popups.

**Explanation:** `showCoordinates` is a named function, so the same handler reference is supplied to both `map.on()` and `map.off()`. The information panel also updates its displayed zoom level after `zoomend`.

---

## Checkpoint 8: Filter by Province (Extension)

![Checkpoint 8 — Gilgit Baltistan with the layer control open](Checkpoint%20Screenshots/Checkpoint%208.png)

Selecting **Gilgit Baltistan** filters the map to **14 districts**. The districts appear grey and no orange population circles are displayed because the supplied `pop_2023` values are missing for these districts. This means **population data are unavailable**, not that their population is zero.

| Check | Observed Result |
|---|---|
| Province | Gilgit Baltistan |
| Displayed district count | 14 |
| District density colour | Grey (missing census data) |
| Population circles | None |
| Overlay control | Both density and population listed and enabled |

The layer control references permanent `districtGroup` and `circleGroup` objects, so the overlays can continue to be switched on and off after the filtered contents are rebuilt.

---

## Checkpoint 9: SVG Versus Canvas (Extension)

### SVG Mode — Elements Panel

![Checkpoint 9 — SVG rendering](Checkpoint%20Screenshots/Checkpoint%209%20SVG.png)

### Canvas Mode — Elements Panel

![Checkpoint 9 — Canvas rendering](Checkpoint%20Screenshots/Checkpoint%209%20Canvas.png)

Five `draw(all)` timings were recorded for each renderer using the browser Console.

**SVG readings (ms):** 54.0, 35.7, 34.3, 41.7, 45.3

**Sorted SVG readings:** 34.3, 35.7, **41.7**, 45.3, 54.0

**Canvas readings (ms):** 66.0, 55.5, 35.7, 37.1, 36.1

**Sorted Canvas readings:** 35.7, 36.1, **37.1**, 55.5, 66.0

### Renderer Comparison Table

| Measurement | SVG | Canvas |
|---|---|---|
| `draw(all)`, median of five | **41.7 ms** | **37.1 ms** |
| Elements inside `leaflet-overlay-pane` | **160 SVG paths** | **1 canvas element** |
| Hover highlighting still works? | **Yes** | **Yes** |
| Can one district be inspected in Elements? | **Yes**, as a separate SVG path | **No**, not as a separate DOM path |

### Interpretation

Canvas was **4.6 ms faster** than SVG by the median measure in this five-run experiment, a relatively small difference for only 160 districts.

SVG represents each district as an individual DOM `<path>` element; Canvas paints all district geometries onto a shared drawing surface.

Both still support Leaflet's geographic hover interactions, but Canvas does not expose each district as a separate DOM element.

For a larger, more detailed **tehsil (ADM3)** dataset with many more features and vertices, Canvas would be expected to offer a greater advantage by reducing the number of DOM elements. Actual performance would still depend on geometry complexity and the browser/device and should be tested.

---

## Section 10.3: Final Questions

### Question 1

**Lab 2 shaded districts by population. Name one large, thinly populated district and one small, crowded one, and explain how each would mislead on the Lab 2 map.**

**Answer:**

**Chagai, Balochistan** is large and sparsely populated, with **269,192 people across 44,476.9 km²**.

**Lahore, Punjab** is much smaller but crowded, with **13,004,135 people across 1,729.9 km²**.

On Lab 2's count-based choropleth, the huge mapped area of Chagai attracts visual attention even though its population is low, while densely populated Lahore occupies a comparatively small patch.

Shading by people per km² supports a fairer comparison between different-sized districts.

### Question 2

**radiusFor takes a square root. What would the map suggest about Lahore against a district of 3 million if it did not?**

**Answer:**

Lahore has about **4.3 times** the population of a 3-million-person district.

If radius increased directly with population rather than its square root, circle **area** would be about **18.8 times** as large, exaggerating the comparison.

Using the square root makes circle area approximately proportional to population.

### Question 3

**Why does the layer control hold districtGroup rather than the L.geoJSON layer itself?**

**Answer:**

`districtGroup` is a persistent layer-group object.

When a province is selected, the old GeoJSON layer is discarded and a newly filtered layer is added to the same group.

The layer control can therefore continue toggling the current district polygons.

If it referenced the original GeoJSON layer directly, it would point to an outdated object after filtering.

### Question 4

**What would go wrong if the circles were drawn in overlayPane instead of the symbols pane? Describe what the user would see when hovering.**

**Answer:**

In the same pane, a hovered district's `bringToFront()` action could put its polygon above the orange population circles, making the circles appear hidden or partially covered.

A separate `symbols` pane with a higher z-index keeps population circles visible above the highlighted polygons.

### Question 5

**Why can map.off remove showCoordinates, when it could not remove an anonymous function passed to map.on?**

**Answer:**

`showCoordinates` is a named function, so `map.on()` and `map.off()` receive the **same function reference**.

An anonymous function written directly inside `map.on()` without saving a reference cannot later be identified by `map.off()` for removal.

### Question 6

**On the NUST overlay, which circle would you use to show a 25 km evacuation zone, and which to mark the campus on a national map? Why?**

**Answer:**

Use **`L.circle()`** for the 25 km evacuation zone because its radius is measured in **metres** and represents real geographic distance.

Use **`L.circleMarker()`** for the campus location because its radius is measured in **pixels** and stays visually consistent as the map is zoomed in or out.
