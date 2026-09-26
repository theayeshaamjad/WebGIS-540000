# Lab 01: First Web Map Report
**Name:** Ayesha Amjad
**Course:** Web GIS, SCEE-IGIS, NUST

## Checkpoint Screenshots

**1. Checkpoint 1:** 

![Checkpoint 1](Checkpoint%201.png)

**2. Checkpoint 2:**

![Checkpoint 2](Checkpoint%202.png)

**3. Checkpoint 3:**

![Checkpoint 3](Checkpoint%203.png)

**4. Checkpoint 4:**

![Checkpoint 4](Checkpoint%204.png)

**5. Checkpoint 5 (https://theayeshaamjad.github.io/WebGIS-540000/):**

![Checkpoint 5](Checkpoint%205.png)

## Conceptual Questions

**1. What is the difference in network requests before and after adding Leaflet?**
At first the browser only had to fetch index.html, since that was the entire page. After Leaflet was added, the browser also had to download the Leaflet CSS and JavaScript files, and then fetch a separate small image for every map tile drawn on screen. Each tile is its own request, so panning or zooming the map generates many more of them.

**2. What is the difference between HTML and CSS in this lab?**
HTML defines the structure and content of the page, like <div id="map"></div>, which creates the container that will hold the map. CSS defines how that content looks, like the rule #map { border-radius: 12px; }, which rounds the container's corners..

**3. Why does the #map rule need a height, when the h1 rule does not?**
An empty <div> has zero height by default, so Leaflet has no space to display the map. You must set a CSS height. An <h1> doesn’t need this because its text gives it a natural height.

**4.  You opened your page through Live Server at 127.0.0.1 instead of double-clicking the file. Give one reason this matters.**
Opening a file directly uses file:///, which browsers restrict from loading external data files. Live Server runs the page through 127.0.0.1, allowing the files to load properly like they would on a real website.

**5. A classmate’s marker appears in the sea near Africa instead of in Islamabad. What is almost certainly wrong, and how would you fix it?**
The latitude and longitude are swapped. Leaflet uses [latitude, longitude], while GeoJSON uses [longitude, latitude]. Swapping them to the correct order places the point in the right location.