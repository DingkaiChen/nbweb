require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/FeatureLayer",
    "esri/layers/GraphicsLayer",
    "esri/Graphic",
    "esri/geometry/Point",
    "esri/geometry/Multipoint",
    "esri/symbols/SimpleMarkerSymbol",
    "esri/symbols/PictureMarkerSymbol",
    "esri/widgets/LayerList",
    "dojo/domReady!"
], function (Map, MapView, FeatureLayer,GraphicsLayer,Graphic, Point, Multipoint, SimpleMarkerSymbol, PictureMarkerSymbol, LayerList) {
    //Code to create the map and view will go here
    var map = new Map({
        basemap: "topo"
    });

    var view = new MapView({
        container: "viewDiv",   //Reference to the DOM node that will contain the view
        map: map,               //Reference to the map object created in step 3
        center: [121.5, 29.8],
        zoom: 10
    });

    /*---Add soil plots into view---*/
    var symbolC = new SimpleMarkerSymbol({
        color: [226, 119, 40],
        size: 8,
        outline: { // autocasts as new SimpleLineSymbol()
            color: [255, 255, 255],
            width: 1
        }
    });
    var soilPoints = new Multipoint();
    dojo.query(".SoilPlots div").forEach(function (item) {
        var x = item.getElementsByTagName("p");
        soilPoints.addPoint(new Point({
            longitude: x[0].innerText,
            latitude: x[1].innerText
        }));
    });
    var graphicC = new Graphic({
        geometry: soilPoints,
        symbol: symbolC
    });
    //view.graphics.add(graphicC);


    /*---Add water plots into view---*/
    var symbolA = new SimpleMarkerSymbol({
        color: [40, 119, 226],
        size:8,
        outline: { // autocasts as new SimpleLineSymbol()
            color: [255, 255, 255],
            width: 1
        }
    });
    var waterPoints = new Multipoint();
    dojo.query(".WaterPlots div").forEach(function (item) {
        var x = item.getElementsByTagName("p");
        waterPoints.addPoint(new Point({
            longitude: x[0].innerText,
            latitude: x[1].innerText
        }));
    });
    var graphicA = new Graphic({
        geometry: waterPoints,
        symbol: symbolA
    });

    /*---Add vegi plots into view---*/
    var symbolB = new SimpleMarkerSymbol({
        color: [119, 226, 40],
        size: 8,
        outline: { // autocasts as new SimpleLineSymbol()
            color: [255, 255, 255],
            width: 1
        }
    });
    var vegiPoints = new Multipoint();
    dojo.query(".VegiPlots div").forEach(function (item) {
        var x = item.getElementsByTagName("p");
        vegiPoints.addPoint(new Point({
            longitude: x[0].innerText,
            latitude: x[1].innerText
        }));
    });
    var graphicB = new Graphic({
        geometry: vegiPoints,
        symbol: symbolB
    });

    /*---Add air routine plots into view---*/
    var symbolD = new SimpleMarkerSymbol({
        color: [255, 0, 40],
        size: 8,
        outline: { // autocasts as new SimpleLineSymbol()
            color: [255, 255, 255],
            width: 1
        }
    });
    var airRoutinePoints = new Multipoint();
    dojo.query(".AirPlots div").forEach(function (item) {
        var x = item.getElementsByTagName("p");
        airRoutinePoints.addPoint(new Point({
            longitude: x[0].innerText,
            latitude: x[1].innerText
        }));
    });
    var graphicD = new Graphic({
        geometry: airRoutinePoints,
        symbol: symbolD
    });

    /*---Create a Graphics Layer---*/
    var soilLayer = new GraphicsLayer();
    soilLayer.title = "soil monitor plots";
    soilLayer.graphics.add(graphicC);
    map.add(soilLayer);

    var airLayer1 = new GraphicsLayer();
    airLayer1.title = "air monitor plots";
    airLayer1.graphics.add(graphicD);
    map.add(airLayer1);

    var vegiLayer = new GraphicsLayer();
    vegiLayer.title = "forest monitor plots";
    vegiLayer.graphics.add(graphicB);
    map.add(vegiLayer);

    var waterLayer = new GraphicsLayer();
    waterLayer.title = "water monitor plots";
    waterLayer.graphics.add(graphicA);
    map.add(waterLayer);


    /*---Layer List---*/
    var layerList = new LayerList({
        view: view
    });
    // Adds widget below other elements in the top left corner of the view
    view.ui.add(layerList, {
        position: "top-right"
    });
    
});
