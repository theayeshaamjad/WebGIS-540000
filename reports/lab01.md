# Lab 01: First Web Map Report
**Name:** Ayesha Amjad
**Course:** Web GIS, SCEE-IGIS, NUST

## Checkpoint Screenshots
1. **Checkpoint 1:** ![Checkpoint 1](Checkpoint%201.png)
2. **Checkpoint 2:** ![Checkpoint 2](Checkpoint%202.png)
3. **Checkpoint 3:** ![Checkpoint 3](Checkpoint%203.png)
4. **Checkpoint 4:** ![Checkpoint 4](Checkpoint%204.png)
5. **Checkpoint 5 (Live Site):** ![Checkpoint 5](Checkpoint%205.png)

## Conceptual Questions

**1. What is the difference in network requests before and after adding Leaflet?**
Before adding Leaflet, the browser only fetched the single `index.html` file. Now, it also downloads the Leaflet CSS and JavaScript libraries, alongside dozens of 256x256 pixel `.png` map tile images that fetch dynamically as the map is panned and zoomed.

**2. What is the difference between HTML and CSS in this lab?**
HTML provides the raw structure and elements of the page (such as the `<h1>` heading and the `<div id="map">` container). CSS dictates the visual presentation and layout (such as the dark blue background color, the custom header card, and forcing the map container to be 550 pixels high).

**3. How do you view the network requests made by the browser?**
Open the browser's Developer Tools (F12), navigate to the Network tab, check the "Disable cache" box, and refresh the page to observe all incoming server requests.

**4. Why use Live Server instead of just double-clicking the HTML file?**
A real local server mimics a production web environment. Opening the file directly via a `file:///` path triggers strict browser security policies (CORS) that will block the map from loading external data files later in the course.

**5. If a map marker appears in the middle of the ocean instead of a city, what went wrong?**
The latitude and longitude coordinates are likely swapped. Leaflet expects coordinates in a strict `[latitude, longitude]` order.