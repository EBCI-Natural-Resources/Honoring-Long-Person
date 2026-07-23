import folium
from folium.plugins import BeautifyIcon
import geopandas as gpd
from branca.element import Element


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

### CUSTOM CSS FOR LAYER CONTROL

css = """
<style>
.leaflet-control-layers {
    font-size: 16px !important;
}

.leaflet-control-layers label {
    font-size: 16px !important;
}

.leaflet-control-layers-selector {
    transform: scale(1.3);
    margin-right: 5px;
}
</style>
"""

### CUSTOM CSS FOR MAP INFORMATION PANEL

info_panel = """
<style>
#map-info-panel {
    position: fixed;
    bottom: 10px;
    left: 10px;
    z-index: 9999;

    background: white;
    border: 2px solid #444;
    border-radius: 10px;

    width: 300px;

    box-shadow: 0 2px 10px rgba(0,0,0,0.3);

    font-family: Gadugi, Arial, sans-serif;
}

#map-info-header {
    background: #007bff;
    color: white;
    padding: 10px;
    border-radius: 8px 8px 0 0;
    font-size: 18px;
    font-weight: bold;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

#map-info-content {
    padding: 12px;
    font-size: 14px;
    max-height: 500px;
    overflow-y: auto;
}

.toggle-btn {
    cursor: pointer;
    border: none;
    background: white;
    color: #007bff;
    font-weight: bold;
    border-radius: 4px;
    padding: 2px 8px;
}
</style>

<div id="map-info-panel">

    <div id="map-info-header">
        Honoring Long Person Map
        <button class="toggle-btn" onclick="toggleInfoPanel()">
            −
        </button>
    </div>

    <div id="map-info-content">

        <h4 style="font-weight:bold;">Legend</h4>

        <div style="height:10px;"></div>

        <p>
            <span style="
                display:inline-block;
                width:24px;
                height:16px;
                border:1px solid black;
                background: linear-gradient(
                    to right,
                    rgba(2, 0, 255, 0.5) 0%,
                    rgba(2, 0, 255, 0.5) 25%,
                    rgba(255, 149, 92, 0.5) 25%,
                    rgba(255, 149, 92, 0.5) 50%,
                    rgba(91, 0, 140, 0.5) 50%,
                    rgba(91, 0, 140, 0.5) 75%,
                    rgba(253, 239, 94, 0.5) 75%,
                    rgba(253, 239, 94, 0.5) 100%
                );
                margin-right:8px;
            "></span>

            Cleanup Zone
        </p>

        <div style="height:5px;"></div>

        <p>
            <span style="
                display:inline-block;
                width:12px;
                height:12px;
                border:2px solid black;
                border-radius:50%;
                background:white;
                margin-right:8px;
            "></span>

            Pull-Off Location
        </p>

        <p>
            <span style="
                font-size:18px;
                color:red;
                margin-right:8px;
            ">★</span>

            Start/End Location
        </p>

        <br>

        <h4 style="font-weight:bold;">Navigation</h4>

        <div style="height:10px;"></div>

        <p>
            Click on the start/end location or any of the pull-off locations to get directions to that place.
        </p>

        <br>

        <h4 style="font-weight:bold;">Modifying the Map</h4>

        <div style="height:10px;"></div>

        <p>
            <ul>
                <li>Click the "Satellite" and "Standard" buttons in the top right corner to choose a basemap.</li>
                <li>Toggle the boxes in the top right corner to select which layers appear.</li>
            </ul>
        </p>
    </div>

</div>

<script>
function toggleInfoPanel() {

    var content = document.getElementById("map-info-content");
    var button = document.querySelector(".toggle-btn");

    if (content.style.display === "none") {
        content.style.display = "block";
        button.innerHTML = "−";
    } else {
        content.style.display = "none";
        button.innerHTML = "+";
    }
}
</script>
"""

###

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

pull_off_layer = folium.FeatureGroup(
    name="Pull-Off Locations",
    show=True
)

for _, row in pull_offs.iterrows():
    lat = row.geometry.y
    lon = row.geometry.x

    popup_html = f"""
    <div style="font-size:14px;">
        <a href="https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
           target="_blank"
           style="
             display:block;
             padding:8px;
             background:#007bff;
             color:white;
             text-align:center;
             border-radius:5px;
             text-decoration:none;">
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
    ).add_to(pull_off_layer)

pull_off_layer.add_to(m)


folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite"
).add_to(m)

folium.TileLayer(
    "OpenStreetMap",
    name="Standard"
).add_to(m)

m.get_root().header.add_child(Element(css))

folium.LayerControl(collapsed=True).add_to(m)

m.get_root().html.add_child(Element(info_panel))

m.save("../docs/index.html")
