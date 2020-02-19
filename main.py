#from flask import *
from flask import Flask, render_template, request
from flask import Response
from flask import abort, Flask, redirect, url_for

import pandas as pd
import numpy as np
import osmnx as ox
import networkx as nx
from sklearn.neighbors import KDTree
import folium
import random


app = Flask(__name__)


@app.route("/menukedua")
def menu_kedua():
    return render_template("menu_kedua.html")

@app.route('/post_field2', methods=['POST'])
def form_post1():

    lat_in1 = float(request.form['lat_in1'])
    lng_in1 = float(request.form['long_out1'])

    lat_in2 = float(request.form['lat_in2'])
    lng_in2 = float(request.form['long_out2'])

    lat_in3 = float(request.form['lat_in3'])
    lng_in3 = float(request.form['long_out3'])

    
    lat_center  = float(request.form['lat_center'])
    long_center = float(request.form['long_center'])

    bikin_rute_multiple(lat_center,long_center,lat_in1,lng_in1,lat_in2,lng_in2,lat_in3,lng_in3)

    return redirect(url_for('menu_kedua'))

def bikin_rute_multiple(lat_center,long_center,lat_in1,lng_in1,lat_in2,lng_in2,lat_in3,lng_in3):
    titik_1       = [lat_in1, lng_in1]
    titik_2       = [lat_in2, lng_in2]
    titik_3       = [lat_in3, lng_in3]

    #titik_1 = [-6.921169, 107.601442]
    #titik_2 = [-6.928275, 107.604579]
    #titik_3 = [-6.922519, 107.607146]

    bandung = (lat_center, long_center)
    G = ox.graph_from_point(bandung, distance=600)

    nodes, _ = ox.graph_to_gdfs(G)
    #ambil attribut edges pada G 
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True, node_geometry=False, fill_edge_geometry=False)

    #kasi nilai random antara 1-10 pada G['weight']
    edges['weight'] = np.random.randint(1,10, size=len(edges))
    #campur ke G 
    G = ox.gdfs_to_graph(nodes,edges)
    #deklarasi tree untuk mendeteksi closest nodes pada titik awal dan tujuan
    tree = KDTree(nodes[['y', 'x']], metric='euclidean')

    point1     = tree.query([titik_1], k=1, return_distance=False)[0]
    point2     = tree.query([titik_2], k=1, return_distance=False)[0]
    point3     = tree.query([titik_3], k=1, return_distance=False)[0]

    #dapat nodes terdekat
    closest_node_to_1 = nodes.iloc[point1].index.values[0]
    closest_node_to_2 = nodes.iloc[point2].index.values[0]
    closest_node_to_3 = nodes.iloc[point3].index.values[0]

    route1 = nx.dijkstra_path(G, closest_node_to_1,closest_node_to_2,weight='weight')
    route2 = nx.dijkstra_path(G, closest_node_to_2,closest_node_to_3,weight='weight')

    tooltip = 'Click me!'

    basemap = ox.plot_route_folium(G, route1, route_color='red')
    basemap2 = ox.plot_route_folium(G, route2, route_color='orange',route_map = basemap)

    folium.Marker(location=titik_1,popup='<i>titik 1 </i>', icon=folium.Icon(color='red')).add_to(basemap2)
    folium.Marker(location=titik_2,popup='<i>titik 2 </i>',icon=folium.Icon(color='orange')).add_to(basemap2)
    folium.Marker(location=titik_3,popup='<i>titik 3 </i>',icon=folium.Icon(color='blue')).add_to(basemap2)


    basemap2.save(outfile= "C:/xampp/htdocs/js/flask2/templates/multiple_djikstra.html")

@app.route("/menu")
def menu_utama():
    return render_template("menu_utama.html")

@app.route('/post_field', methods=['POST'])
def form_post():
    lat_in = float(request.form['lat_input'])
    lng_in = float(request.form['long_input'])

    lat_out = float(request.form['lat_out'])
    lng_out = float(request.form['long_out'])
    
    lat_center  = float(request.form['lat_center'])
    long_center = float(request.form['long_center'])

    bikin_rute(lat_in,lng_in,lat_center,long_center,lat_out,lng_out)

    return redirect(url_for('menu_utama'))

def bikin_rute(lat_input,long_input,lat_center,long_center,lat_output,long_output):
    titik_awal       = [lat_input, long_input]
    titik_tujuan     = [lat_output, long_output]
    bandung = (lat_center, long_center)
    G = ox.graph_from_point(bandung, distance=600)

    nodes, _ = ox.graph_to_gdfs(G)
    #ambil attribut edges pada G 
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True, node_geometry=False, fill_edge_geometry=False)

    #kasi nilai random antara 1-10 pada G['weight']
    edges['weight'] = np.random.randint(1,10, size=len(edges))
    #campur ke G 
    G = ox.gdfs_to_graph(nodes,edges)
    #deklarasi tree untuk mendeteksi closest nodes pada titik awal dan tujuan
    tree = KDTree(nodes[['y', 'x']], metric='euclidean')

    awal    = tree.query([titik_awal], k=1, return_distance=False)[0]
    tujuan  = tree.query([titik_tujuan], k=1, return_distance=False)[0]

    #dapat nodes terdekat
    closest_node_to_awal   = nodes.iloc[awal].index.values[0]
    closest_node_to_tujuan = nodes.iloc[tujuan].index.values[0]
    route = nx.dijkstra_path(G, closest_node_to_awal,closest_node_to_tujuan,weight='weight')
    basemap = ox.plot_route_folium(G, route, route_color='green')
    folium.Marker(location=titik_awal,icon=folium.Icon(color='red')).add_to(basemap)
    folium.Marker(location=titik_tujuan,icon=folium.Icon(color='green')).add_to(basemap)
    basemap.save(outfile= "C:/xampp/htdocs/js/flask2/templates/djikstra.html")


@app.route("/view_single_djikstra")
def view_single():
    return render_template("djikstra.html")

@app.route("/view_multiple_djikstra")
def view_multiple():
    return render_template("multiple_djikstra.html")



if __name__ == "__main__":
    app.run(debug=True)
