import folium
from folium.plugins import BeautifyIcon
import geopandas as gpd


ZONE_COLOR_MAP = {
    "1": "#0200FF",
    "2": "#FF955C",
    "3": "#BEBDFF",
    "4": "#FFC5A6",
    "5": "#706FFF",
    "6": "#FF5900",
    "7": "#5B008C",
    "8": "#FDEF5E",
    "9": "#BB3EFF",
    "10": "#BBAB00",
    "11": "#E1A9FF",
    "12": "#F7F400",
}

START_END_MAP = {
    "Peaches Squirrell Complex": "#FF0000",
}

def style_zones(feature):
    zone_no = str(feature["properties"].get("Zone"))

    return {
        "fillColor": ZONE_COLOR_MAP.get(zone_no),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5
    }

def style_start_end(feature):
    name = str(feature["properties"].get("Name"))

    return {
        "fillColor": START_END_MAP.get(zone_no),
        "color": "black",
    }


zones = gpd.read_file("../data/clean_up_zones.geojson")
zone_label_points = gpd.read_file("../data/clean_up_zone_label_points.geojson")
start_and_end = gpd.read_file("../data/start_and_end.geojson")
pull_offs = gpd.read_file("../data/riverside_pull_offs.geojson")

m = folium.Map(
    location=[35.474, -83.336],
    zoom_start=12,
    tiles=None
)


folium.GeoJson(
    zones,
    name="Cleanup Zones",
    style_function=style_zones
).add_to(m)

for _, row in zone_label_points.iterrows():
    lat = row.geometry.y
    lon = row.geometry.x

    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-family: Gadugi, Arial, sans-serif;
                font-size:20px;
                font-weight:bold;
                color:black;
                white-space: nowrap;    
                text-shadow:
                        -1px -1px 0 white,
                        1px -1px 0 white,
                        -1px  1px 0 white,
                        1px  1px 0 white;
                text-align:center;
            ">
                {row["Label"]}
            </div>
            """
        )
    ).add_to(m)

for _, row in start_and_end.iterrows():
    lat = row.geometry.y
    lon = row.geometry.x

    name = row["Name"]
    color = START_END_MAP.get(name)

    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"

    popup_html = f"""
    <div style="font-size:14px;">
        <b>{name}</b><br><br>
        <a href="{directions_url}" target="_blank" style="
            display:block;
            padding:8px;
            background:#007bff;
            color:white;
            text-align:center;
            border-radius:5px;
            text-decoration:none;
        ">
            Get Directions
        </a>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-size:40px;
                color:{color};
                text-align:center; 
            ">
                ★
            </div>
            """
        ),

        tooltip=name,
        popup=folium.Popup(popup_html, max_width=250)

    ).add_to(m)

for _, row in pull_offs.iterrows():
    lat = row.geometry.y
    lon = row.geometry.x

    name = row["Location"]

    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"

    popup_html = f"""
    <div style="font-size:14px;">
        <a href="{directions_url}" target="_blank" style="
            display:block;
            padding:8px;
            background:#007bff;
            color:white;
            text-align:center;
            border-radius:5px;
            text-decoration:none;
        ">
            Get Directions
        </a>
    </div>
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color="black",
        weight=2,
        fill=True,
        fill_color="white",
        fill_opacity=1,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=None
    ).add_to(m)


folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite"
).add_to(m)

folium.TileLayer(
    "OpenStreetMap",
    name="Standard"
).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m.save("../docs/index.html")
