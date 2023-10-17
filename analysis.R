# Load libraries
library(sf)
library(CoastCR)

working_dir = getwd()

# format file paths 
intersects_path= paste(
  working_dir,
  "rates/input/intersects.shp",
  sep="/"
) 

normals_path = paste(
  working_dir,
  "rates/input/normals.shp",
  sep="/"
)

table_csv_path= paste(
  working_dir,
  "rates/input/shorelines_processed.csv",
  sep="/"
)

output_path = paste(
  working_dir,
  "rates",
  "output",
  sep="/"
)

# Intersections shapefile
shp <- st_read(intersects_path)

# Normals shapefile
normals <- st_read(normals_path)

# Table with dates and associated uncertainty
table <- st_read(table_csv_path)

# Define baseline position. Offshore = OFF; Onshore = ON; Mixed = MIX.
position = "ON"


# Define outputs names
out_points <- paste(
  output_path,
  "int_filter.shp",
  sep="/"
)
 
out_name <- paste(
  output_path,
  "normals_rates.shp",
  sep="/"
)
 
coast_var(
  shp, normals,
  table, position,
  out_points, out_name
)