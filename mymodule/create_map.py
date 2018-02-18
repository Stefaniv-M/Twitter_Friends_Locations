import folium

# This is a module with functions to create html map:

def create_layer(layer_display_name, layers_list):
    """
    (str, list) -> None
    This function adds layer called layer_display_name to list of layers called layers_list.
    """
    layers_list.append(folium.FeatureGroup(name=layer_display_name))
    return None


def add_layers(layers_list, my_map):
    """
    (list, folium.folium.map) -> None
    This function adds all layers in list called layers_list to map called my_map.
    """
    for layer_1 in layers_list:
        my_map.add_child(layer_1)
    my_map.add_child(folium.LayerControl())
    return None


def add_mark(popup_str, lat, lon, layers_list):
    """
    (str, float, float, list) -> None
    This function adds pointer with latitude lat and longitude lon,
    and popup popup_str to the map.
    """
    # I had to remove ' and " from popup because they caused error in map:
    popup_str = popup_str.replace("'", "_")
    popup_str = popup_str.replace('"', "_")

    layers_list[0].add_child(folium.Marker(location=[lat, lon],
                                           popup=popup_str,
                                           icon=folium.Icon()))


def save_html_map(names_list):
    """
    This function saves map with names and locations into a project folder.
    :param names_list: list
    :return: None
    """
    my_map = folium.Map(location=[49.817545, 24.023932], tiles="Mapbox Bright")

    # Creating two layers:
    layers_list = []
    create_layer("Names", layers_list)
    create_layer("Empty Layer", layers_list)

    # Adding markers:
    for tuple_1 in names_list:
        add_mark(tuple_1[1], tuple_1[2][0], tuple_1[2][1], layers_list)

    add_layers(layers_list, my_map)

    # Saving map:
    my_map.save("map_with_names.html")

    return None