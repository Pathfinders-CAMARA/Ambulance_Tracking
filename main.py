import folium
import time
import math
import random

LAT_MIN, LAT_MAX = 48.8570, 48.8620
LON_MIN, LON_MAX = 2.2920, 2.2980

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def is_inside_geofence(ambulance_loc, car_loc, radius):
    distance = haversine(ambulance_loc[0], ambulance_loc[1], car_loc[0], car_loc[1])
    return distance <= radius

def display_map(ambulance_location, car_location, radius):
    map_object = folium.Map(location=car_location, zoom_start=16)

    folium.Marker(
        location=ambulance_location,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(map_object)

    folium.Marker(
        location=car_location,
        icon=folium.Icon(color='blue', icon='car')
    ).add_to(map_object)

    folium.Circle(
        location=car_location,
        radius=radius,
        color='green',
        fill=True,
        fill_opacity=0.3
    ).add_to(map_object)

    map_object.save('ambulance_map.html')

def move_within_bounds(location, step_size=0.0003):
    new_lat = location[0] + random.choice([-step_size, step_size])
    new_lon = location[1] + random.choice([-step_size, step_size])

    new_lat = max(LAT_MIN, min(new_lat, LAT_MAX))
    new_lon = max(LON_MIN, min(new_lon, LON_MAX))

    return new_lat, new_lon

def move_smoothly(ambulance_location, target_location, speed=0.0003):
    lat_diff = target_location[0] - ambulance_location[0]
    lon_diff = target_location[1] - ambulance_location[1]

    step_lat = (lat_diff / abs(lat_diff)) * min(abs(lat_diff), speed) if lat_diff != 0 else 0
    step_lon = (lon_diff / abs(lon_diff)) * min(abs(lon_diff), speed) if lon_diff != 0 else 0

    new_lat = ambulance_location[0] + step_lat
    new_lon = ambulance_location[1] + step_lon

    return new_lat, new_lon

if __name__ == '__main__':
    ambulance_location = (48.8584, 2.2945)
    car_location = (48.8600, 2.2960)
    radius = 200

    inside_geofence = False

    while True:
        display_map(ambulance_location, car_location, radius)

        distance = haversine(ambulance_location[0], ambulance_location[1], car_location[0], car_location[1])
        print(f"Distance: {distance:.2f} meters")

        is_inside = is_inside_geofence(ambulance_location, car_location, radius)
        
        if is_inside and not inside_geofence:
            print("🚨 ALERT: Ambulance entered geofence!")
            inside_geofence = True
        elif not is_inside and inside_geofence:
            print("🚨 ALERT: Ambulance exited geofence!")
            inside_geofence = False

        ambulance_location = move_smoothly(ambulance_location, car_location, speed=0.0002)
        car_location = move_within_bounds(car_location, step_size=0.0005)

        time.sleep(3)
