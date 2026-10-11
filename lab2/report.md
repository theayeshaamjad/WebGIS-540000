
# Lab 2: District Explorer — Building a Web Map from a Shapefile
 

**Live Web Map:** [District Explorer — Lab 2](https://theayeshaamjad.github.io/WebGIS-540000/lab2/)

**GitHub Repository:** [WebGIS-540000](https://github.com/theayeshaamjad/WebGIS-540000)

---

## Checkpoint 1: Set Up the Project

![Checkpoint 1 — Project Setup](screenshots/CP%201.png)

The WebGIS project was organized in Visual Studio Code using three separate files: `index.html` for webpage structure, `style.css` for appearance, and `app.js` for JavaScript functionality. A `data` folder was created to store the district GeoJSON file.

---

## Checkpoint 2: Prepare the Data in QGIS

### Data Preparation and File-Size Comparison

![Checkpoint 2 — Measurement Table](screenshots/CP%202%20table.png)

![Checkpoint 2 — Geometry Comparison](screenshots/CP%202.png)

The Pakistan administrative level 2 district dataset was inspected in QGIS and exported into four GeoJSON versions using EPSG:4326 (WGS 84).

- **Version A:** Direct shapefile-to-GeoJSON conversion.
- **Version B:** Coordinate precision reduced to five decimal places.
- **Version C:** Geometry simplified using approximately 100 m tolerance and precision 5.
- **Version D:** Geometry simplified using approximately 1 km tolerance and precision 5.

Version C was selected for the interactive District Explorer because it provides a practical balance between file size and boundary detail at the national map scale.

### Question: Why can GeoJSON be larger than a shapefile?

GeoJSON stores geometry coordinates and attributes as readable text, including repeated field names and punctuation. Shapefiles store geometry in a more compact binary format. Therefore, GeoJSON can require more storage for the same geographic features. Reducing coordinate precision and simplifying geometry can significantly decrease its size.

---

## Checkpoint 3: Read the GeoJSON Data as Text

### Section 4.2 — Find the Structure

**1. What is the type of the outermost object?**

The outermost object is a `FeatureCollection`, which stores multiple geographic features together.

**2. How many entries are in the features array?**

The GeoJSON contains **160 district features**, verified from the actual dataset used in the web map.

**3. Take the first feature. What is its geometry type?**

The first feature has `Polygon` geometry and represents Bagh district, Azad Kashmir.

**4. How many levels of square brackets are there before the first number in its coordinates?**

There are **three nested square-bracket levels**, consistent with GeoJSON Polygon geometry.

Example coordinate structure:

`[[[73.69622, 34.08025], ...]]`

**5. List the keys inside its properties.**

The first feature contains these five property keys:

- `district`
- `province`
- `pcode`
- `pop_2023`
- `area_km2`

### Section 4.3 — Check the Coordinate Order

The first coordinate pair is:

`[73.69622, 34.08025]`

In GeoJSON, coordinates are stored in **longitude, latitude** order.

- Longitude: 73.69622° E
- Latitude: 34.08025° N

Both values fall within Pakistan's expected geographic ranges. Therefore, the coordinate order is correct.

### Section 4.4 — Check That the Rings Close

The first and last coordinate pairs of the first polygon's outer ring are identical:

`[73.69622, 34.08025]`

Therefore, the outer polygon ring is correctly closed.

---

## Checkpoint 4: Build the Webpage

![Checkpoint 4 — HTML and CSS Webpage](screenshots/CP%204.png)

The District Explorer webpage was developed using HTML and CSS. The page contains a heading, subtitle, province selection control, district count, and a map container.

The webpage was successfully tested using the VS Code Live Server extension before loading the district data.

The map container was assigned an explicit height to provide space for Leaflet to display the map.

---

## Checkpoint 5: Load the Data with JavaScript

![Checkpoint 5 — JavaScript Console](screenshots/CP%205.png)

A Leaflet map was initialized and centred on Pakistan. Geographic bounds were applied to restrict map movement outside the intended region.

The district GeoJSON dataset was loaded using JavaScript's `fetch()` method and `await`.

The browser Console confirmed the presence of **160 geographic features**.

JavaScript array methods were used to inspect the dataset:

- `map()` extracts district names from features.
- `filter()` selects records matching a condition.
- `Set` identifies distinct province names.

These operations demonstrate how geographic attributes can be inspected and processed using JavaScript.

---

## Checkpoint 6: Draw the Districts and Inspect Network Activity

### Displaying District Boundaries

![Checkpoint 6 — District Boundaries](screenshots/CP%206.png)

District boundaries were displayed using the Leaflet `L.geoJSON()` function.

The initial map used grey polygon fills with white outlines. A total of **160 districts** was successfully displayed.

The `draw()` function was configured to remove an existing GeoJSON layer before drawing a new one, avoiding overlapping layers when filtering.

### Browser Network Activity

![Checkpoint 6 — Network Requests](screenshots/CP%206%20Network.png)

The Network tab in browser Developer Tools was used to examine the loading of geographic data and OpenStreetMap tiles.

### Observation

The GeoJSON file is requested as one dataset containing district boundaries and attributes. In contrast, the OpenStreetMap basemap is assembled from multiple raster image tiles.

Each map tile is downloaded through a separate request. Panning or zooming the map generates additional tile requests.

Slow 3G throttling was used to assess loading performance under a slower network connection.

---

## Checkpoint 7: Classify by Population, Add Popups and a Legend

![Checkpoint 7 — Population Choropleth](screenshots/CP%207.png)

The district boundaries were classified into five population categories using the `pop_2023` attribute.

A colour-coded legend was added to explain the population distribution, and interactive popups were enabled to display district attributes.

### Population Classification

| Population Category | Colour | Hex Code |
|---|---|---|
| Up to 300,000 | Light peach | `#fdd0a2` |
| Above 300,000 to 750,000 | Light orange | `#fd8d3c` |
| Above 750,000 to 1,500,000 | Orange | `#f16913` |
| Above 1,500,000 to 3,000,000 | Dark orange | `#d94801` |
| Above 3,000,000 | Dark brown | `#7f2704` |
| Missing census data | Grey | `#c9cfd1` |

### Why Were These Classification Breaks Used?

The five population classes follow the thresholds provided in the lab manual and distinguish districts according to population size.

Districts without recorded census population were assigned grey instead of being included in the lowest population class. This prevents missing data from being misinterpreted as low population.

### Popup Verification

The interactive popup was successfully tested for **Lasbela, Balochistan**.

The popup displayed:

- District: Lasbela
- Province: Balochistan
- Population: 680,977
- Area: 14,057.4 km²

This confirms that district attributes were retrieved and displayed correctly.

---

## Checkpoint 8: Filter with a Province Control (Extension)

### All Provinces

![Checkpoint 8 — All Provinces](screenshots/CP%208%20all%20provinces.png)

When **All provinces** is selected, the complete dataset of **160 districts** is displayed.

### Punjab Province Selected

![Checkpoint 8 — Punjab](screenshots/CP%208%20punjab.png)

A dynamic province drop-down was developed using JavaScript.

The province names were extracted from the GeoJSON dataset using `map()` and `Set`.

When Punjab is selected, the `filter()` method retains only the districts belonging to Punjab.

The map automatically redraws the selected features, adjusts the view to the selected province, and updates the district count.

The population classification and legend remain functional after filtering.

---

## Checkpoint 9: Measure and Compare Coordinate-System Areas (Extension)

### Coordinate-System Measurements

![Checkpoint 9 — Area Comparison](screenshots/CP%209%20Table.png)


- **EPSG:3857:** WGS 84 / Pseudo-Mercator
- **EPSG:32643:** WGS 84 / UTM Zone 43N

An `area_calc` field was created using the expression:

`$area / 1000000`

The calculated polygon areas were expressed in square kilometres.

Five districts were selected from southern to northern Pakistan to compare area distortion at different latitudes.

### Measured Area Comparison

| District | Latitude (°N) | EPSG:3857 Area (km²) | UTM Area (km²) | Difference (%) |
|---|---:|---:|---:|---:|
| Thatta | 24.6942 | 9,290.54 | 7,726.26 | 20.25 |
| Sukkur | 27.5453 | 6,607.97 | 5,217.10 | 26.66 |
| Multan | 29.9259 | 4,874.97 | 3,656.22 | 33.33 |
| Rawalpindi | 33.5413 | 7,529.13 | 5,225.48 | 44.09 |
| Gilgit | 35.9668 | 6,135.03 | 4,013.13 | 52.87 |

**Percentage difference formula:**

Difference (%) = [(Area in EPSG:3857 − Area in UTM) / Area in UTM] × 100

**Example: Rawalpindi**

Difference = [(7529.13 − 5225.48) / 5225.48] × 100

**Difference = 44.09%**

### Section 10.4 — Answer These

**1. Does the percentage difference grow or shrink as you move north?**

The percentage difference increases toward the north.

In the selected districts, the difference rises from **20.25% in Thatta** at latitude 24.6942°N to **52.87% in Gilgit** at latitude 35.9668°N.

This demonstrates that Web Mercator area distortion increases at higher latitudes.

**2. The predicted inflation factor is 1/cos²(latitude). Compute it for one of your districts and compare it with the measured difference.**

Rawalpindi was selected for the calculation.

Latitude = **33.5413°N**

Predicted inflation factor:

`1 / cos²(33.5413°) ≈ 1.4395`

Predicted percentage inflation:

`(1.4395 − 1) × 100 ≈ 43.95%`

Measured difference from the QGIS area calculations:

**44.09%**

The predicted and measured results differ by approximately **0.14 percentage points**, showing close agreement with the theoretical distortion factor.

**3. Which of the two figures would you put in a report, and why?**

I would use the area measured in an appropriate UTM projection rather than Web Mercator.

Web Mercator introduces significant area distortion, whereas an appropriate local UTM projection provides more reliable measurements.

The lab uses UTM Zone 43N for comparison, although a different UTM zone may be more appropriate for districts located outside Zone 43N.

---

## Section 11.4: Final Questions

### Question 1

**Version D is far smaller than version A. Give one situation in which version D would be the wrong choice.**

Version D would be unsuitable for a detailed district-level map requiring accurate representation of administrative boundaries.

Its approximately 1 km simplification removes smaller boundary details and may introduce visible inaccuracies at larger map scales.

Version C was therefore selected for the interactive national district map because it provides a better balance between file size and geographic detail.

### Question 2

**The page makes one request for your GeoJSON file and dozens for tiles. Explain the difference in how those two kinds of data reach the browser.**

The browser downloads the GeoJSON file through a single request containing the district geometries and their attributes.

The OpenStreetMap basemap is delivered through multiple individual image-tile requests.

Each tile represents a small section of the basemap, and additional requests are generated when the user pans or zooms.

### Question 3

**Why does the map container need a height when the heading does not?**

An empty HTML `<div>` has no natural height, so Leaflet cannot display a visible map unless the container height is specified in CSS.

A heading contains text, which automatically gives it height.

Therefore, the `#map` CSS rule requires an explicit height, while the heading does not.

### Question 4

**draw removes the existing layer before adding a new one. What would go wrong if it did not?**

Without removing the existing layer, each province selection would add another district layer over the previous one.

This would create overlapping polygons, display outdated selections, and gradually reduce performance.

Removing the old layer ensures that only the currently selected districts remain visible.

### Question 5

**A classmate's districts all appear in the same colour. List two possible causes and how you would tell them apart.**

**Cause 1: Incorrect population attribute name**

The JavaScript classification may reference an attribute that does not exist in the loaded GeoJSON.

I would inspect the first feature's `properties` object in the browser Console and verify that `pop_2023` is present.

**Cause 2: Invalid population values**

The population attribute may contain text values, thousands separators, or placeholders that cannot be compared numerically.

I would inspect the actual `pop_2023` values in the Console or QGIS attribute table and check whether they contain valid numerical data.

These checks distinguish a missing field from a field containing unusable values.

### Question 6

**You open the page by double-clicking index.html instead of using Live Server. The basemap appears but the districts do not. Explain why.**

Opening `index.html` directly uses the `file:///` protocol.

Browser security restrictions can block JavaScript's `fetch()` method from reading a separate local GeoJSON file, even when external basemap tiles load successfully.

Live Server provides an HTTP address, allowing the GeoJSON request to work correctly.

---


