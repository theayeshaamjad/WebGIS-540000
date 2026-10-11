# Lab 2: District Explorer — Building a Web Map from a Shapefile

   
**Live website:** [Insert your public GitHub Pages URL after publishing]  
**GitHub repository:** [Insert your GitHub repository URL]

## Checkpoints


---

## Checkpoint 1: Set Up the Project

![Checkpoint 1 — Project structure](screenshots/CP%201.png)

The web mapping project was prepared in Visual Studio Code using separate `index.html`, `style.css`, and `app.js` files, together with a `data` folder for the GeoJSON layer.

## Checkpoint 2: Prepare the Data in QGIS

![Checkpoint 2 — File-size measurements](screenshots/CP%202%20table.png)

![Checkpoint 2 — Comparison of simplified geometries](screenshots/CP%202.png)

The original administrative level 2 district layer was inspected in QGIS and exported in four GeoJSON versions using EPSG:4326. Versions A and B differ in coordinate precision; versions C and D additionally use geometry simplification. Version C, simplified with approximately 100 m tolerance and coordinate precision 5, was used for the interactive map.

### File-size measurements

| Version | Processing performed | Size (MB) | Percentage of Version A |
|:--|:--|--:|--:|
| Original shapefile | Sum of ADM2 `.shp`, `.shx`, `.dbf`, `.prj`, and `.cpg` components | [Enter measured size] | N/A |
| A | Direct conversion to GeoJSON | [Enter measured size A] | 100% |
| B | Coordinate precision of 5 decimal places | [Enter measured size B] | [Calculate] |
| C | Simplified approximately 100 m; precision 5 | [Enter measured size C] | [Calculate] |
| D | Simplified approximately 1 km; precision 5 | [Enter measured size D] | [Calculate] |

**Calculation:** Percentage of A = (version size ÷ Version A size) × 100.

**Why can GeoJSON be larger than a shapefile?** GeoJSON stores coordinates and attributes as human-readable text, including field names and punctuation. Shapefiles use a compact binary format for their geometry, which can require less storage for the same boundaries. Simplification and lower coordinate precision can reduce GeoJSON file size, at the cost of fine boundary detail.

## Checkpoint 3: Read the GeoJSON Data as Text

### Section 4.2 — Find the structure

**1. What is the type of the outermost object?**  
`FeatureCollection`.

**2. How many entries are in the `features` array?**  
**160 features**, confirmed from the actual `districts.geojson` used for the map.

**3. Take the first feature. What is its geometry type?**  
`Polygon`. The first feature represents **Bagh**, Azad Kashmir. (The dataset also contains some `MultiPolygon` features, but the *first* feature is a `Polygon`.)

**4. How many levels of square brackets are there before the first number in its coordinates?**  
**Three** nested square-bracket levels: `[[[longitude, latitude], ... ]]`, consistent with the first feature being a `Polygon`.

**5. List the keys inside its `properties`.**  
`district`, `province`, `pcode`, `pop_2023`, `area_km2`.

### Section 4.3 — Check the coordinate order

The first coordinate pair is **`[73.69622, 34.08025]`**. The first number represents **longitude** and the second represents **latitude**. Both values fall within Pakistan's approximate geographic ranges, so the coordinate order is correct.

### Section 4.4 — Check that the rings close

The first and last coordinate pairs of the first polygon's outer ring are both **`[73.69622, 34.08025]`**. Therefore, that ring is correctly closed.

## Checkpoint 4: Build the Webpage

![Checkpoint 4 — Webpage opened in Live Server](screenshots/CP%204.png)

The HTML document defines the page heading, province selector, district count, and map container. CSS provides the layout. The initial page was tested through Live Server before adding the district boundaries.

## Checkpoint 5: Load the Data with JavaScript

![Checkpoint 5 — Browser Console](screenshots/CP%205.png)

Leaflet initializes the map, with bounds set around Pakistan. JavaScript loads the `data/districts.geojson` file using `fetch()` and `await`. The browser Console confirms that the dataset contains **160 features**. Array operations (`map`, `filter`, and `Set`) allow inspection of district names and distinct province values.

## Checkpoint 6: Draw the Districts and Inspect Network Activity

![Checkpoint 6 — District boundaries](screenshots/CP%206.png)

![Checkpoint 6 — Network requests and map tile preview](screenshots/CP%206%20Network.png)

The district boundaries were displayed using `L.geoJSON()`, initially with grey fill and white outlines. The webpage displayed a count of **160 districts**. The browser Network panel was used to inspect the GeoJSON request separately from the basemap image-tile requests.

### Browser network measurements

| Measurement | Recorded result |
|:--|:--|
| Version C (`districts.geojson`) request size | [Enter value from Network → Size] |
| Version C load time, no throttling | [Enter measured time] |
| Version C load time, Slow 3G | [Enter measured time] |
| Version A load time, Slow 3G | [Enter measured time] |
| Number of `.png` tile requests | [Enter counted value] |
| Zoom level of selected tile | [Enter zoom value from tile URL] |
| Individual basemap tile dimensions | 256 × 256 pixels |

**Observation:** The browser fetches the district GeoJSON as a single geographic dataset, whereas the OpenStreetMap background is composed of multiple image tiles. Additional tiles are requested as the map is moved or zoomed.

## Checkpoint 7: Classify by Population, Add Popups and a Legend

![Checkpoint 7 — Choropleth map, legend, and district popup](screenshots/CP%207.png)

Districts were classified into five population categories using the `pop_2023` attribute. The choropleth uses the manual's classification thresholds and reserves grey for districts without census population data.

| Population class | Colour |
|:--|:--|
| Up to 300,000 | Light peach (`#fdd0a2`) |
| More than 300,000, up to 750,000 | Orange (`#fd8d3c`) |
| More than 750,000, up to 1,500,000 | Deep orange (`#f16913`) |
| More than 1,500,000, up to 3,000,000 | Dark orange (`#d94801`) |
| More than 3,000,000 | Dark brown (`#7f2704`) |
| Missing population data | Grey (`#c9cfd1`) |

**Why these breaks?** The manual's five thresholds provide an interpretable distinction between lower- and higher-population districts. Showing missing census values in grey prevents missing data from being interpreted as low population.

**Popup verification:** The screenshot shows **Lasbela, Balochistan**, with population **680,977** and area **14,057.4 km²**, confirming that the popup retrieves district attributes.

## Checkpoint 8: Filter with a Province Control (Extension)

### All provinces

![Checkpoint 8 — All provinces](screenshots/CP%208%20all%20provinces.png)

When **All provinces** is selected, the map displays the complete dataset of **160 districts**.

### Punjab selected

![Checkpoint 8 — Punjab filter](screenshots/CP%208%20punjab.png)

The province list was generated from unique `province` values in the GeoJSON. Selecting Punjab filters the features, removes the previous district layer, redraws only the matching districts, zooms to their combined bounds, and updates the district count. The population classification and legend remain available.

## Checkpoint 9: Measure and Compare Coordinate-System Areas (Extension)

![Checkpoint 9 — Area comparison table](screenshots/CP%209%20Table.png)

### Additional QGIS measurement evidence

![Checkpoint 9 — Additional screenshot 1](screenshots/9%20R1.png)

![Checkpoint 9 — Additional screenshot 2](screenshots/9%20R2.png)

The original ADM2 district layer was exported separately to **EPSG:3857 (Web Mercator)** and **EPSG:32643 (UTM Zone 43N)**. An `area_calc` field was calculated as `$area / 1000000`, with planimetric measurements, to express areas in square kilometres. Five districts were selected from south to north using `adm2_name`, and `center_lat` was used to represent latitude.

### Measured comparison of five districts

| District | Latitude (°N) | EPSG:3857 area (km²) | EPSG:32643 area (km²) | Difference (%) |
|:--|--:|--:|--:|--:|
| Thatta | 24.6942 | 9,290.54 | 7,726.26 | 20.25 |
| Sukkur | 27.5453 | 6,607.97 | 5,217.10 | 26.66 |
| Multan | 29.9259 | 4,874.97 | 3,656.22 | 33.33 |
| Rawalpindi | 33.5413 | 7,529.13 | 5,225.48 | 44.09 |
| Gilgit | 35.9668 | 6,135.03 | 4,013.13 | 52.87 |

**Percentage difference:**

`((Area in EPSG:3857 − Area in EPSG:32643) / Area in EPSG:32643) × 100`

**Example — Rawalpindi:**  
`((7529.13 − 5225.48) / 5225.48) × 100 ≈ 44.09%`

### Section 10.4 — Answer these

**1. Does the percentage difference grow or shrink as you move north?**  
The difference **increases northward**, rising from **20.25% for Thatta** (24.6942°N) to **52.87% for Gilgit** (35.9668°N). This is consistent with the increasing area distortion of Web Mercator at higher latitudes.

**2. The predicted inflation factor is `1 / cos²(latitude)`. Compute it for one of your districts and compare it with the measured difference.**  
For **Rawalpindi**, at **33.5413°N**:

- Predicted factor: `1 / cos²(33.5413°) ≈ 1.43947`.
- Predicted percentage inflation: `(1.43947 − 1) × 100 ≈ 43.95%`.
- Measured percentage difference from the two QGIS areas: **44.09%**.

The difference is approximately **0.14 percentage points**, so the measured result is close to the latitude-based prediction.

**3. Which of the two figures would you put in a report, and why?**  
I would use an area measured in an **appropriate local projected coordinate system**, such as the applicable UTM zone, rather than Web Mercator. Web Mercator considerably inflates areas. The laboratory uses EPSG:32643 for its comparison, although a different local UTM zone may be more appropriate for districts outside Zone 43N.

---

## Section 11.4: Final Questions

**1. Version D is far smaller than version A. Give one situation in which version D would be the wrong choice.**  
Version D would be inappropriate for a detailed map of individual district boundaries or for close-up boundary inspection. Its approximately 1 km simplification can remove bends and smaller features and introduce visible boundary inaccuracies. Version C is more appropriate for the national-level interactive map developed in this lab.

**2. The page makes one request for your GeoJSON file and dozens for tiles. Explain the difference in how those two kinds of data reach the browser.**  
The browser downloads the GeoJSON district boundaries and attributes in one request to `data/districts.geojson`. The basemap is delivered as many separate raster image tiles requested from OpenStreetMap according to the map's location and zoom level. Panning or zooming can trigger additional tile requests.

**3. Why does the map container need a height when the heading does not?**  
The map is drawn inside an initially empty HTML `<div>`, which has no natural height. The CSS `#map` height gives Leaflet a visible area in which to render the map. The heading contains text, so the browser automatically gives it height.

**4. `draw` removes the existing layer before adding a new one. What would go wrong if it did not?**  
Each selection would add a new GeoJSON layer over the previous layer rather than replacing it. District polygons would overlap, old provinces could remain visible, and repeated filtering would reduce performance. Removing the previous layer keeps the map synchronized with the current province selection.

**5. A classmate's districts all appear in the same colour. List two possible causes and how you would tell them apart.**  
**Cause 1 — Wrong attribute name:** The classification may refer to `pop_2023` even though the loaded data uses another field name. I would inspect the first feature's `properties` object in the Console to check whether `pop_2023` exists.  
**Cause 2 — Invalid population values:** The field may exist but contain nonnumeric text, thousands separators, or placeholders. I would inspect several actual `pop_2023` values in the Console or QGIS attribute table and confirm that they can be compared numerically. The working map demonstrates that the supplied GeoJSON contains usable values for its coloured districts.

**6. You open the page by double-clicking `index.html` instead of using Live Server. The basemap appears but the districts do not. Explain why.**  
Double-clicking the file opens it using the `file:///` protocol. Browser security restrictions can prevent `fetch()` from loading the separate local GeoJSON file under that protocol, even when external basemap tiles appear. Running the page through Live Server provides an HTTP address, allowing the GeoJSON request to work.

---

## Publication and Submission

The completed site must be published through **GitHub Pages**, with the repository set to **Public**, using **Settings → Pages → Deploy from a branch → `main` → `/(root)`**. The final LMS submission must contain:

1. **GitHub repository URL:** [Insert after pushing the repository].
2. **Published interactive map URL:** [Insert after enabling GitHub Pages].

**Note:** `http://127.0.0.1:5500/` is a local development address and is not the public link to submit.
