# Lab 4: Getting Started with GeoDjango

**Web GIS — Districts from PostGIS**

This lab implements a database-driven map of Pakistan's 160 districts using Django, GeoDjango, PostgreSQL/PostGIS and Leaflet. The polygons are stored in PostGIS, exposed through a Django GeoJSON endpoint, and visualized in the browser.

---

## Checkpoint 1 — Django Setup and Versions

![Checkpoint 1: Django project setup](Screenshots/CP1%20django.png)

![Checkpoint 1: Software version evidence](Screenshots/CP1%20version.png)

The Django project `webgis` and application `districts` were created and verified in a Python virtual environment.

## Checkpoint 2 — PostgreSQL and PostGIS

![Checkpoint 2: PostgreSQL/PostGIS verification](Screenshots/CP2.png)

PostgreSQL 18 and PostGIS 3.6.0 were used. A PostGIS-enabled database named `webgis` was prepared for the lab.

## Checkpoint 3 — Django Database Configuration

![Checkpoint 3: Database migrations in the terminal](Screenshots/CP3%20terminal.png)

![Checkpoint 3: Django database tables in pgAdmin](Screenshots/CP3%20table.png)

Django successfully connected to PostgreSQL/PostGIS and applied the initial migrations. The geospatial GDAL and GEOS libraries were verified separately.

## Checkpoint 4 — District Spatial Model

![Checkpoint 4: Spatial model SQL](Screenshots/CP4%20SQL.png)

![Checkpoint 4: District database columns](Screenshots/CP4%20column.png)

The `District` model stores names, provinces, population, area and `MultiPolygon` geometry in EPSG:4326. The migration created a GiST index on the geometry column, enabling efficient spatial queries.

## Checkpoint 5 — Loading the District Data

![Checkpoint 5: District import](Screenshots/CP5%20import.png)

![Checkpoint 5: Django ORM verification](Screenshots/CP5%20ORM.png)

The district GeoJSON was loaded into the database. The application confirmed **160 districts**, and Django ORM was used to inspect the imported records.

## Checkpoint 6 — Django Admin

![Checkpoint 6: Province filtering](Screenshots/CP6%20province.png)

![Checkpoint 6: Lahore admin evidence A](Screenshots/CP6%20Lahore%20%28a%29.png)

![Checkpoint 6: Lahore admin evidence B](Screenshots/CP6%20Lahore%20%28b%29.png)

![Checkpoint 6: Lahore admin evidence C](Screenshots/CP6%20Lahore%20%28c%29.png)

The district model was registered in Django Admin for authorized data management. The screenshots document filtering and inspecting/editing district records.

## Checkpoint 7 — Django GeoJSON API and Leaflet Map

![Checkpoint 7: PostGIS district web map](Screenshots/CP7%20map.png)

![Checkpoint 7: GeoJSON API request in browser Network panel](Screenshots/CP7%20network.png)

The Leaflet map draws **160 districts** from the Django/PostGIS database, rather than loading a local static file. Districts are symbolized by province, and tooltips show the district and province names. The Esri World Topographic Map was used after direct OSM tile requests were blocked.

**Network verification**

| Property | Observed result |
|---|---|
| Request | `/api/districts/` |
| Status | `200 OK` |
| Content type | `application/geo+json` |
| Response `Content-Length` | 1,026,495 bytes (approximately 1.03 MB) |

*Note: HTTP Content-Length is the response-body size, not necessarily the transferred size shown in the Network Size column.*

## Checkpoint 8 — PostGIS Spatial Query (Bonus)

![Checkpoint 8: Spatial-query click popup](Screenshots/CP8%20pop.png)

![Checkpoint 8: SQL area-comparison results](Screenshots/CP8%20area%20query.png)

A click on the map sends latitude and longitude to `/api/where/`. The backend constructs a geographic point and uses GeoDjango's `geom__contains` lookup, corresponding to a PostGIS spatial containment query. The API returned successful responses during testing.

### Area comparison



| District | Stored area (km²) | Geodesic area (km²) | Web Mercator area (km²) |
|---|---:|---:|---:|
| Lahore | **[1730]** | **[1730]** | **[2385]** |
| Gilgit | **[4016]** | **[4015]** | **[6133]** |
| Gwadar | **[11574]** | **[11574]** | **[14244]** |

**Interpretation:** Web Mercator is intended primarily for web-map display, not accurate area measurement. Its areal distortion increases toward higher latitudes. For measuring district areas, a suitable geodesic calculation or locally appropriate projected coordinate system is preferable.

---

## Software versions

| Software | Version verified during the lab |
|---|---|
| Python | 3.13.9 |
| Django | 6.1.2 |
| PostgreSQL | 18 |
| PostGIS | 3.6.0 |
| GDAL (GeoDjango/OSGeo4W) | 3.13.3 |
| GEOS (GeoDjango/OSGeo4W) | 3.15.0-CAPI-1.21.0 |

## Installation and configuration errors

The following issues occurred while setting up the lab and were resolved:

| Error encountered | Resolution |
|---|---|
| `py : The term 'py' is not recognized` | Used the available `python` executable instead of the Windows `py` launcher. |
| `OSError: [WinError 127] The specified procedure could not be found` | Configured OSGeo4W library paths and resolved DLL loading for GDAL/GEOS. |
| `FATAL: password authentication failed for user "postgres"` | Corrected the PostgreSQL password and supplied it through `WEBGIS_DB_PASSWORD` in the terminal environment. |
| `fe_sendauth: no password supplied` | Correctly populated the environment variable before running migrations. |
| `FATAL: database "webgis" does not exist` | Identified a database name with a trailing space, then configured a correctly named `webgis` database. |
| `TemplateDoesNotExist: districts/map.html` | Corrected the template folder to `districts/templates/districts/map.html`. |
| OpenStreetMap tiles returned HTTP 403 | Switched the Leaflet background to Esri World Topographic Map. |

**Important before submission:** The manual requests the **full text of every installation error**, not only the summary above. Paste the complete relevant terminal traceback(s) under this paragraph. Exclude passwords, database credentials and secrets.

### Full installation error logs

**Error 1 — GDAL Library Loading Error

Error encountered:

OSError: [WinError 127] The specified procedure could not be found

Cause: Django could not correctly load the GDAL library and its dependencies from OSGeo4W.

Solution: The OSGeo4W library paths were configured using C:\OSGeo4W\bin. The correct GDAL and GEOS DLL files were identified, and GDAL was preloaded before GeoDjango initialization.

Verification: GDAL 3.13.3 and GEOS 3.15.0 loaded successfully.

Error 2 — PostgreSQL Authentication Failed

Error encountered:

FATAL: password authentication failed for user "postgres"

A subsequent attempt also produced:

FATAL: fe_sendauth: no password supplied

Cause: Django initially received an incorrect or missing PostgreSQL password.

Solution: The correct password was provided securely through the WEBGIS_DB_PASSWORD environment variable in PowerShell instead of hardcoding it in settings.py.

Verification: The database connection was subsequently authenticated successfully.

Error 3 — PostgreSQL Database Not Found

Error encountered:

django.db.utils.OperationalError:
FATAL: database "webgis" does not exist

Cause: The originally created PostgreSQL database was named webgis , with an extra trailing space, while Django was configured to connect to webgis.

Solution: A correctly named webgis database was configured, the PostGIS extension was enabled, and the Django migrations were executed again.

Verification: The migrations completed successfully, and the required Django and spatial tables were visible in pgAdmin.

Error 4 — Python Launcher Not Recognized

Error encountered:

py : The term 'py' is not recognized as the name
of a cmdlet, function, script file, or operable program.

Cause: The Windows Python launcher was not available.

Solution: The existing Python 3.13.9 installation was used directly through the python command.

Verification: Python and Django commands executed successfully inside the virtual environment.**

---

## Section 9.4 — Questions and Answers

### 1. What can Django and PostGIS do instead of making visitors download an entire GeoJSON file? Give two examples.

A Django/PostGIS-backed application can execute filtering or spatial queries on the server and return only the requested results. In this lab, the API can (1) return only a requested province's districts through `/api/districts/?province=Sindh`, and (2) identify which district contains a clicked location through `/api/where/?lat=33.6423&lng=72.9906`.

### 2. Why read the database password from an environment variable instead of placing it in `settings.py`?

An environment variable keeps the password separate from the project source code, reducing the risk of accidentally publishing credentials in a GitHub repository. Different computers or deployments can use their own credentials without editing tracked source files.

### 3. What does the `USING GIST` index do, and which query benefits from it?

The GiST index speeds up spatial searches by narrowing the set of candidate geometries. The spatial containment lookup `geom__contains`, represented by `ST_Contains` in PostGIS, can benefit from that index when finding the district containing a point.

### 4. Why does the loading script convert some Polygon geometries to MultiPolygon?

The Django geometry field is a `MultiPolygonField`, while source GeoJSON geometries may be either `Polygon` or `MultiPolygon`. Wrapping individual polygons as multipolygons makes the input compatible with the model field and avoids geometry-type errors during import.

### 5. Who should and should not have Django Admin access?

Authorized data administrators and GIS staff responsible for verifying and updating official district records should have appropriately restricted admin access. Ordinary visitors should only use the public map and query API; they should not be allowed to edit or delete source records.

### 6. Where are the different latitude/longitude orders used, and how does the extension avoid confusion?

Leaflet represents positions as `[lat, lng]`, such as `setView([30.3753, 69.3451], 5)` and `e.latlng`. GeoDjango/GEOS creates geographic points as `Point(lng, lat, srid=4326)` because longitude is the x-coordinate. The API uses explicitly named URL parameters, `lat` and `lng`, which the view reads separately before constructing the point in the required order.

---

## Conclusion

The lab demonstrates how Django, GeoDjango, PostGIS and Leaflet can work together to build a database-backed web GIS. District geometries were imported into a spatial database and published through a Django API for interactive mapping. The optional extension adds server-side point-in-polygon identification and an area-comparison query.

**Submission:** GitHub repository and this report. Lab 4 has no GitHub Pages live URL because GitHub Pages cannot run Django and PostGIS.
