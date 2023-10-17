# Undergraduate Thesis
<p>
  This repository contains all scripts written for my undergraduate thesis, "Shoreline Change Analysis of Cagliliog, 
  Tinambac, Camarines Sur, Philippines  Using CoastSat, QGIS, and CoastCR," conducted with 
  Bruzo R. and Casasis G.. Our goal was to conduct shoreline change analysis using a fully open-source workflow by ensuring data 
  interoperability between the different tools we used.
</p>

<p>
  <i>The undergraduate thesis project data is also available in this repository</i>
</p>

The following tools were essential for the completion of this project:
<ul>
  <li>
    <a href="https://www.qgis.org/en/site/">QGIS</a> for data visualization
  </li>
  <li>
    <a href="https://qgis.org/pyqgis/master/">pyqgis</a> for creating and manipulating QGIS geometries and features
  </li>
  <li>
    <a href="https://github.com/kvos/CoastSat">CoastSat</a> for automating shoreline and shoreline transect intersection detection
  </li>
  <li>
    <a href="https://github.com/alejandro-gomez/CoastCR">CoastCR</a> for calculating shoreline change statistics
  </li>
</ul>

The scripts written for this project were used to:
<ul>
  <li>
    <p>
      Automate the creation of shoreline transects to be used for the detection of shoreline positions  
    </p>
    <p>
      <img src="https://github.com/derUbermenk/undergraduate-thesis/assets/72653808/a1f1bb7b-b9bc-4e7e-b3f9-61b1a906b894" alt="Generated Transects" style="width: 60%; height: 60%;">
    </p>
  </li>
  <li>
    <p>
      Convert data into workable formats
    </p>
    <p>
      <img src="https://github.com/derUbermenk/undergraduate-thesis/assets/72653808/b38fd45d-8c5e-4d1f-a98d-6a1d9c5c2d86" alt="workable formats" style="width: 60%; height: 60%;">
    </p>
  </li>
  <li>
    <p>
      Smoothen detected shoreline traces
    </p>
    <p>
       <img src="https://github.com/derUbermenk/undergraduate-thesis/assets/72653808/39c774c0-a2f7-472e-8a6a-900e46f75685" alt="smooth shorelines" style="width: 60%; height: 60%;">
    </p>
  </li>
  <li>
    <p>
      Visualize results
    </p>
    <p>
      <img src="https://github.com/derUbermenk/undergraduate-thesis/assets/72653808/837ebdca-4bc4-42f0-a9e5-ab7d6fb1055e" alt="visualized results" style="width: 60%; height: 60%;">
    </p>
  </li>
</ul>

# Citations

<p>
Gómez-Pazo, A., Payo, A., Paz-Delgado, M.V., Delgadillo-Calzadilla, M.A. (2022). Open Digital Shoreline Analysis System: ODSAS v1.0. Journal of Marine Science and Engineering, 10, 26. DOI: https://doi.org/10.3390/jmse10010026
</p>

<p>
Vos K., Splinter K.D., Harley M.D., Simmons J.A., Turner I.L. (2019). CoastSat: a Google Earth Engine-enabled Python toolkit to extract shorelines from publicly available satellite imagery. Environmental Modelling and Software. 122, 104528. https://doi.org/10.1016/j.envsoft.2019.104528 (Open Access)
</p>
