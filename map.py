from branca.element import Template
from matplotlib import cm, colors
import folium
import branca
import json
import csv
import os

m = folium.Map(location=[40, 60.0060], zoom_start=3, tiles='Cartodb dark_matter')

file_path = 'Scenarios.csv'
data = []
headers = ['Location', 'Lattitude', 'Longitude', 'Type']

routes_path = 'Shipping Routes'
road_routes_path = 'Road Routes'
scenario_routes_path = 'Scenario Routes.csv'
road_route_file_names = os.listdir(road_routes_path)
routes_file_names = os.listdir(routes_path)

with open(file_path, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    data = list(csv_reader)

with open(scenario_routes_path, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    scenario_routes = {}
    for row in csv_reader:
        key = row['Origin'] + '_' + row['Destination']
        scenario_routes[key] = {col: row[col] for col in row if col != 'Origin' and col != 'Destination'}

def map_size(units):
    return (units / 234500) * 50 + 5

#log_norm = colors.LogNorm(vmin=500, vmax=234500)
norm = colors.Normalize(vmin=500, vmax=234500)
viridis = cm.get_cmap('plasma')
def color_code(units):
    rgba = viridis(norm(units))
    hex_color = colors.to_hex(rgba)
    return hex_color

def width_code(units):
    return (units /134500) * 6 + 2

scenario1 = folium.FeatureGroup(name="Scenario 1", show=True, control=True)
scenario2 = folium.FeatureGroup(name="Scenario 2", show=False, control=True)
scenario3 = folium.FeatureGroup(name="Scenario 3.1", show=False, control=True)
scenario4 = folium.FeatureGroup(name="Scenario 3.2", show=False, control=True)
scenario5 = folium.FeatureGroup(name="Scenario 3.2 reasonable", show=False, control=True)
scenario6 = folium.FeatureGroup(name="Scenario 3.2 min co2", show=False, control=True)

def popup_route(code1='', code2='', units='', dist='', mode=''):
    html = """<!DOCTYPE html>
            <html>
            <table style="border-collapse: collapse; font-family: Arial, sans-serif">
            <tbody>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Source</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(code1) + """
            </tr>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Destination</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(code2) + """
            </tr>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Units</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(units) + """
            </tr>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Distance</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(dist + ' km') + """
            </tr>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Freight</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(mode) + """
            </tr>
            </tbody>
            </table>
            </html>
            """ 
    return html

for route in routes_file_names:
    for i in [3,4,5,6]:
        if i == 3:
            scenario = scenario3
        elif i == 4:
            scenario = scenario4
        elif i == 5:
            scenario = scenario5
        elif i == 6:
            scenario = scenario6
        if route.endswith('.geojson'):
            source, destination = route.removesuffix('.geojson').split('_')
            info = scenario_routes[f"{source}_{destination}"]
            if float(info[f'Units Scenario {i} Sea']) != 0:
                geojson_file = routes_path + '/' + route
                with open(geojson_file, 'r') as f:
                    geojson_data = json.load(f)

                coordinates = geojson_data['features'][0]['geometry']['coordinates']
                polyline_coordinates = [[lat, lon] for lon, lat in coordinates]

                html = popup_route(code1=source, code2=destination, dist=info['Distance Sea'], units=info[f'Units Scenario {i} Sea'], mode='Sea')
                iframe = branca.element.IFrame(html=html,width=510,height=280)
                popup = folium.Popup(folium.Html(html, script=True), max_width=500)

                folium.PolyLine(
                    locations=polyline_coordinates,
                    color=color_code(float(info[f'Units Scenario {i} Sea'])),  
                    #color="red",                  
                    weight=width_code(float(info[f'Units Scenario {i} Sea'])),                        
                    opacity=0.8,
                    popup = popup                 
                ).add_to(scenario)

for route in road_route_file_names:
    for i in [3,4,5,6]:
        if i == 3:
            scenario = scenario3
        elif i == 4:
            scenario = scenario4
        elif i == 5:
            scenario = scenario5
        elif i == 6:
            scenario = scenario6
        if route.endswith('.geojson'):
            source, destination = route.removesuffix('.geojson').split('_')
            info = scenario_routes[f"{source}_{destination}"]
            if float(info[f'Units Scenario {i} Road']) != 0:
                geojson_file = road_routes_path + '/' + route
                with open(geojson_file, 'r') as f:
                    geojson_data = json.load(f)

                coordinates = geojson_data['coordinates']
                polyline_coordinates = [[lat, lon] for lon, lat in coordinates]

                html = popup_route(code1=source, code2=destination, dist=info['Distance Road'], units=info[f'Units Scenario {i} Road'], mode='Road')
                iframe = branca.element.IFrame(html=html,width=510,height=280)
                popup = folium.Popup(folium.Html(html, script=True), max_width=500)

                folium.PolyLine(
                    locations=polyline_coordinates,  
                    color=color_code(float(info[f'Units Scenario {i} Road'])),   
                    #color="red",                 
                    weight=width_code(float(info[f'Units Scenario {i} Road'])),                        
                    opacity=0.8,
                    popup = popup                   
                ).add_to(scenario)

manufacturers_list = []
cross_docks_list = []
distribution_centers_list = []
retailers_list = []
optional_source_list = []

for row in data:
    if row['Type'] == 'Manufacturer':
        manufacturers_list.append(row)
    elif row['Type'] == 'Cross Dock':
        cross_docks_list.append(row)
    elif row['Type'] == 'Distribution':
        distribution_centers_list.append(row)
    elif row['Type'] == 'Retailer':
        retailers_list.append(row)
    elif row['Type'] == 'OptionalSource':
        optional_source_list.append(row)

for manu in manufacturers_list:
    for cd in cross_docks_list:
        for i in [1,2,3,4,5,6]:
            suffix = ''
            if i == 1:
                scenario = scenario1
            elif i == 2:
                scenario = scenario2
            elif i == 3:
                suffix = ' Air'
                scenario = scenario3
            elif i == 4:
                suffix = ' Air'
                scenario = scenario4
            elif i == 5:
                suffix = ' Air'
                scenario = scenario5
            elif i == 6:
                suffix = ' Air'
                scenario = scenario6
            info = scenario_routes[f"{manu['ID']}_{cd['ID']}"]
            html = popup_route(code1=manu['ID'], code2=cd['ID'], dist=info['Distance Air'], units=info[f'Units Scenario {i}{suffix}'], mode='Air')
            iframe = branca.element.IFrame(html=html,width=510,height=280)
            popup = folium.Popup(folium.Html(html, script=True), max_width=500)
            if float(info[f'Units Scenario {i}{suffix}']) != 0:
                folium.PolyLine([[float(manu['Latitude']), float(manu['Longitude'])], [float(cd['Latitude']), float(cd['Longitude'])]], color=color_code(float(info[f'Units Scenario {i}{suffix}'])), weight=width_code(float(info[f'Units Scenario {i}{suffix}'])), 
                    opacity=0.8, popup=popup).add_to(scenario)

for cd in cross_docks_list:
    for dc in distribution_centers_list:
        for i in [1,2,3,4,5,6]:
            suffix = ''
            if i == 1:
                scenario = scenario1
            elif i == 2:
                scenario = scenario2
            elif i == 3:
                suffix = ' Air'
                scenario = scenario3
            elif i == 4:
                suffix = ' Air'
                scenario = scenario4
            elif i == 5:
                suffix = ' Air'
                scenario = scenario5
            elif i == 6:
                suffix = ' Air'
                scenario = scenario6
            info = scenario_routes[f"{cd['ID']}_{dc['ID']}"]
            html = popup_route(code1=cd['ID'], code2=dc['ID'], dist=info['Distance Air'], units=info[f'Units Scenario {i}{suffix}'], mode='Air')
            iframe = branca.element.IFrame(html=html,width=510,height=280)
            popup = folium.Popup(folium.Html(html, script=True), max_width=500)
            if float(info[f'Units Scenario {i}{suffix}']) != 0:
                folium.PolyLine([[float(cd['Latitude']), float(cd['Longitude'])], [float(dc['Latitude']), float(dc['Longitude'])]], color=color_code(float(info[f'Units Scenario {i}{suffix}'])), weight=width_code(float(info[f'Units Scenario {i}{suffix}'])), 
                    opacity=0.8, popup=popup).add_to(scenario)
            
for dc in distribution_centers_list:
    for r in retailers_list:
        for i in [1,2,3,4,5,6]:
            suffix = ''
            if i == 1:
                scenario = scenario1
            elif i == 2:
                scenario = scenario2
            elif i == 3:
                suffix = ' Air'
                scenario = scenario3
            elif i == 4:
                suffix = ' Air'
                scenario = scenario4
            elif i == 5:
                suffix = ' Air'
                scenario = scenario5
            elif i == 6:
                suffix = ' Air'
                scenario = scenario6
            info = scenario_routes[f"{dc['ID']}_{r['ID']}"]
            html = popup_route(code1=dc['ID'], code2=r['ID'], dist=info['Distance Air'], units=info[f'Units Scenario {i}{suffix}'], mode='Air')
            iframe = branca.element.IFrame(html=html,width=510,height=280)
            popup = folium.Popup(folium.Html(html, script=True), max_width=500)
            if float(info[f'Units Scenario {i}{suffix}']) != 0:
                folium.PolyLine([[float(dc['Latitude']), float(dc['Longitude'])], [float(r['Latitude']), float(r['Longitude'])]], color=color_code(float(info[f'Units Scenario {i}{suffix}'])), weight=width_code(float(info[f'Units Scenario {i}{suffix}'])), 
                    opacity=0.8, popup=popup).add_to(scenario)
            
for ops in optional_source_list:
    for dc in distribution_centers_list:
        for i in [1,2,3,4,5,6]:
            suffix = ''
            if i == 1:
                scenario = scenario1
            elif i == 2:
                scenario = scenario2
            elif i == 3:
                suffix = ' Air'
                scenario = scenario3
            elif i == 4:
                suffix = ' Air'
                scenario = scenario4
            elif i == 5:
                suffix = ' Air'
                scenario = scenario5
            elif i == 6:
                suffix = ' Air'
                scenario = scenario6
            info = scenario_routes[f"{ops['ID']}_{dc['ID']}"]
            html = popup_route(code1=ops['ID'], code2=dc['ID'], dist=info['Distance Air'], units=info[f'Units Scenario {i}{suffix}'], mode='Air')
            iframe = branca.element.IFrame(html=html,width=510,height=280)
            popup = folium.Popup(folium.Html(html, script=True), max_width=500)
            if float(info[f'Units Scenario {i}{suffix}']) != 0:
                folium.PolyLine([[float(ops['Latitude']), float(ops['Longitude'])], [float(dc['Latitude']), float(dc['Longitude'])]], color=color_code(float(info[f'Units Scenario {i}{suffix}'])), weight=width_code(float(info[f'Units Scenario {i}{suffix}'])), 
                    opacity=0.8, popup=popup).add_to(scenario)

def popup_circle(code='', country='', type='', units=''):
    name = code + ' (' + country + ')'
    html = """<!DOCTYPE html>
            <html>
            <head>
            <h4 style="margin-bottom:10";>{}</h4>""".format(name) + """
            </head>
            <table style="border-collapse: collapse; font-family: Arial, sans-serif">
            <tbody>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Type</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(type) + """
            </tr>
            <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">Units</span></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{}</td>""".format(units) + """
            </tr>
            </tbody>
            </table>
            </html>
            """ 
    return html

for row in data:
    for i in [1,2,3,4,5,6]:
        if i == 1:
            scenario = scenario1
        elif i == 2:
            scenario = scenario2
        elif i == 3:
            scenario = scenario3
        elif i == 4:
            scenario = scenario4
        elif i == 5:
            suffix = ' Air'
            scenario = scenario5
        elif i == 6:
            suffix = ' Air'
            scenario = scenario6
        if float(row[f'Units Scenario {i}']) != 0:
            html = popup_circle(code=row['ID'], country=row['Country'], type=row['Type'], units=row[f'Units Scenario {i}'])
            iframe = branca.element.IFrame(html=html,width=510,height=280)
            popup = folium.Popup(folium.Html(html, script=True), max_width=500)
            if row['Type'] == 'Manufacturer':
                folium.CircleMarker(
                    [float(row['Latitude']), float(row['Longitude'])],
                    popup=popup, 
                    radius=map_size(float(row[f'Units Scenario {i}'])), weight=2, fill=True, fill_opacity = 0.8,
                    color = 'red', fill_color = 'red'
                ).add_to(scenario)
            elif row['Type'] == 'Cross Dock':
                folium.CircleMarker(
                    [float(row['Latitude']), float(row['Longitude'])],
                    popup=popup, 
                    radius=map_size(float(row[f'Units Scenario {i}'])), weight=2, fill=True, fill_opacity = 0.8,
                    color = 'blue', fill_color = 'blue'
                ).add_to(scenario)
            elif row['Type'] == 'Retailer':
                folium.CircleMarker(
                    [float(row['Latitude']), float(row['Longitude'])],
                    popup=popup, 
                    radius=map_size(float(row[f'Units Scenario {i}'])), weight=2, fill=True, fill_opacity = 0.8,
                    color = 'green', fill_color = 'green'
                ).add_to(scenario)
            elif row['Type'] == 'Distribution':
                folium.CircleMarker(
                    [float(row['Latitude']), float(row['Longitude'])],
                    popup=popup, 
                    radius=map_size(float(row[f'Units Scenario {i}'])), weight=2, fill=True, fill_opacity = 0.8,
                    color = 'yellow', fill_color = 'yellow'
                ).add_to(scenario)
            elif row['Type'] == 'OptionalSource':
                folium.CircleMarker(
                    [float(row['Latitude']), float(row['Longitude'])],
                    popup=popup, 
                    radius=map_size(float(row[f'Units Scenario {i}'])), weight=2, fill=True, fill_opacity = 0.8,
                    color = 'white', fill_color = 'white'
                ).add_to(scenario)


scenario1.add_to(m)
scenario2.add_to(m)
scenario3.add_to(m)
scenario4.add_to(m)
scenario5.add_to(m)
scenario6.add_to(m)

folium.LayerControl().add_to(m)

plasma_colors = [cm.plasma(i / (5 - 1)) for i in range(5)]
plasma_colors = [colors.to_hex(color) for color in plasma_colors]
colormap = branca.colormap.LinearColormap(
    colors=plasma_colors,
    vmin=500, vmax=234500,
    caption='Number of units' 
)
colormap_html = colormap._repr_html_()

positioned_colormap_html = f"""
<div id="custom-colormap" style="
    position: fixed !important; 
    top: 20px !important; left: 50% !important; transform: translateX(-50%) !important;
    background-color: white; opacity: 0.85; padding: 10px; border-radius: 5px;
    border: 2px solid grey; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    display: block !important; z-index: 9999 !important;">
    {colormap_html}
</div>
"""

legend_html = '''
<div style="position: fixed; 
    bottom: 50px; left: 50px; width: 200px; height: 150px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    background-color:white; opacity: 0.85; padding: 10px;
    border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
    <div style="display: flex; align-items: center;">
        <i class="fa fa-circle" style="color:red; margin-right: 8px; opacity: 0.9; text-shadow: 0px 0px 1px red;"></i> Manufacturers
    </div>
    <div style="display: flex; align-items: center;">
        <i class="fa fa-circle" style="color:blue; margin-right: 8px; opacity: 0.8; opacity: 0.9; text-shadow: 0px 0px 1px blue;"></i> Cross Docks
    </div>
    <div style="display: flex; align-items: center;">
        <i class="fa fa-circle" style="color:yellow; margin-right: 8px; opacity: 0.8; opacity: 0.9; text-shadow: 0px 0px 1px yellow;"></i> Distribution Centers
    </div>
    <div style="display: flex; align-items: center;">
        <i class="fa fa-circle" style="color:green; margin-right: 8px; opacity: 0.8; opacity: 0.9; text-shadow: 0px 0px 1px green;"></i> Retailers
    </div>
    <div style="display: flex; align-items: center;">
        <i class="fa fa-circle" style="color:white; margin-right: 8px; opacity: 0.8; opacity: 0.9; text-shadow: 0px 0px 2px black;"></i> New Facilities
    </div>
</div>
'''

legend_template = Template('''
{% macro html(this, kwargs) %}
    ''' + legend_html + '''
{% endmacro %}
''')

colmap_template = Template('''
{% macro html(this, kwargs) %}
    ''' + positioned_colormap_html + '''
{% endmacro %}
''')

legend = branca.element.MacroElement()
legend._template = legend_template

colmap = branca.element.MacroElement()
colmap._template = colmap_template

legend.add_to(m)
colmap.add_to(m)

m.save("map.html")
