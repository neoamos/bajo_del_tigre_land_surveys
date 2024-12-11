import csv
from geopy import distance, point
import simplekml



def csv_to_kml(csv_file, kml_file, start_point_name="1", start_point=point.Point(10.303392, -84.812765)):
  print("\nParsing", csv_file)
  # Create a new KML file
  kml = simplekml.Kml()

  graph = {}
  # Read the CSV file
  with open(csv_file, "r") as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        graph[row["start_point"]] = row

  points = [(start_point.longitude, start_point.latitude)]
  current_point_name = start_point_name
  while current_point_name in graph:
    print("Point", current_point_name, start_point.latitude, start_point.longitude)
    row = graph[current_point_name]
    bearing = int(row['bearing_degrees']) + (int(row['bearing_minutes']) / 60) 
    if "bearing_dir1" in row:
       bearing = adjust_bearing_with_directions(row["bearing_dir1"], bearing, row["bearing_dir2"])
    distance_ = float(row['distance_in_meters'])
    end_point = distance.distance(meters=distance_).destination(start_point, bearing=bearing)
    points.append((end_point[1], end_point[0]))

    start_point = end_point
    del graph[current_point_name]
    current_point_name = row["end_point"]

  # Add points to kml
  # kml.newpolygon(name="Atrium Garden", outerboundaryis=points)
  kml.newlinestring(name="Survey", coords=points)
  # Save the KML file
  kml.save(kml_file)

def adjust_bearing_with_directions(dir1, decimal_degrees, dir2):
  # Adjust based on the directions
  if dir1 == "N" and dir2 == "E":
      result = decimal_degrees
  elif dir1 == "S" and dir2 == "E":
      result = 180 - decimal_degrees
  elif dir1 == "S" and dir2 == "W":
      result = 180 + decimal_degrees
  elif dir1 == "N" and dir2 == "W":
      result = 360 - decimal_degrees
  else:
      raise ValueError("Invalid combination of cardinal directions")

  return result

csv_to_kml("tables/newswanger.csv", "kml/newswanger.kml", start_point_name="3", start_point=point.Point(10.303341, -84.812733))
csv_to_kml("tables/vandusen.csv", "kml/vandusen.kml", start_point_name="2", start_point=point.Point(10.30412729456411, -84.8137766303226))
csv_to_kml("tables/susie.csv", "kml/susie.kml", start_point_name="1", start_point=point.Point(10.304411077823092, -84.81334478414315))
csv_to_kml("tables/bob.csv", "kml/bob.kml", start_point_name="1", start_point=point.Point(10.304256656035564, -84.81357896242079))