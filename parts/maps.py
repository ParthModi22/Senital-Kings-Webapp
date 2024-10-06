import streamlit as st
import leafmap.foliumap as leafmap
def map():
    st.set_page_config(layout="wide")

    # Instructions and inference
    st.markdown(
        """
        ## Instructions
        1. Select a map layer for the left side of the split map from the dropdown.
        2. View the selected split map on the right side.
        3. Select a different map layer for the right side of the split map.

        Explore the different land cover maps and their implications for sustainable development!
        """
    )

    # Create columns for map selection and display
    col1, col2, col3 = st.columns([1, 3, 1])

    # List of available map layers
    map_layers = [
        'OpenStreetMap', 'FWS NWI Wetlands', 'FWS NWI Wetlands Raster',
        'NLCD 2021 CONUS Land Cover', 'NLCD 2019 CONUS Land Cover',
        'NLCD 2016 CONUS Land Cover', 'NLCD 2013 CONUS Land Cover',
        'NLCD 2011 CONUS Land Cover', 'NLCD 2008 CONUS Land Cover',
        'NLCD 2006 CONUS Land Cover', 'NLCD 2004 CONUS Land Cover',
        'NLCD 2001 CONUS Land Cover', 'USGS NAIP Imagery',
        'USGS NAIP Imagery False Color', 'USGS NAIP Imagery NDVI',
        'USGS Hydrography', 'USGS 3DEP Elevation', 'USGS 3DEP Elevation Index',
        'ESA Worldcover 2020', 'ESA Worldcover 2020 S2 FCC',
        'ESA Worldcover 2020 S2 TCC', 'ESA Worldcover 2021',
        'ESA Worldcover 2021 S2 FCC', 'ESA Worldcover 2021 S2 TCC',
        'BaseMapDE.Color', 'BaseMapDE.Grey', 'BasemapAT.basemap',
        'BasemapAT.grau', 'BasemapAT.highdpi', 'BasemapAT.orthofoto',
        'BasemapAT.overlay', 'BasemapAT.surface', 'BasemapAT.terrain',
        'CartoDB.DarkMatter', 'CartoDB.DarkMatterNoLabels',
        'CartoDB.DarkMatterOnlyLabels', 'CartoDB.Positron',
        'CartoDB.PositronNoLabels', 'CartoDB.PositronOnlyLabels',
        'CartoDB.Voyager', 'CartoDB.VoyagerLabelsUnder',
        'CartoDB.VoyagerNoLabels', 'CartoDB.VoyagerOnlyLabels',
        'CyclOSM', 'Esri.AntarcticBasemap', 'Esri.AntarcticImagery',
        'Esri.ArcticImagery', 'Esri.ArcticOceanBase',
        'Esri.ArcticOceanReference', 'Esri.NatGeoWorldMap',
        'Esri.OceanBasemap', 'Esri.WorldGrayCanvas', 'Esri.WorldImagery',
        'Esri.WorldPhysical', 'Esri.WorldShadedRelief',
        'Esri.WorldStreetMap', 'Esri.WorldTerrain', 'Esri.WorldTopoMap',
        'FreeMapSK', 'Gaode.Normal', 'Gaode.Satellite',
        'HikeBike.HikeBike', 'HikeBike.HillShading', 'JusticeMap.americanIndian',
        'JusticeMap.asian', 'JusticeMap.black', 'JusticeMap.hispanic',
        'JusticeMap.income', 'JusticeMap.multi', 'JusticeMap.nonWhite',
        'JusticeMap.plurality', 'JusticeMap.white', 'MtbMap',
        'NASAGIBS.ASTER_GDEM_Greyscale_Shaded_Relief', 'NASAGIBS.BlueMarble',
        'NASAGIBS.BlueMarble3031', 'NASAGIBS.BlueMarble3413',
        'NASAGIBS.BlueMarbleBathymetry3031', 'NASAGIBS.BlueMarbleBathymetry3413',
        'NASAGIBS.MEaSUREsIceVelocity3031', 'NASAGIBS.MEaSUREsIceVelocity3413',
        'NASAGIBS.ModisAquaBands721CR', 'NASAGIBS.ModisAquaTrueColorCR',
        'NASAGIBS.ModisTerraAOD', 'NASAGIBS.ModisTerraBands367CR',
        'NASAGIBS.ModisTerraBands721CR', 'NASAGIBS.ModisTerraChlorophyll',
        'NASAGIBS.ModisTerraLSTDay', 'NASAGIBS.ModisTerraSnowCover',
        'NASAGIBS.ModisTerraTrueColorCR', 'NASAGIBS.ViirsEarthAtNight2012',
        'NASAGIBS.ViirsTrueColorCR', 'OPNVKarte', 'OneMapSG.Default',
        'OneMapSG.Grey', 'OneMapSG.LandLot', 'OneMapSG.Night',
        'OneMapSG.Original', 'OpenAIP', 'OpenFireMap',
        'OpenRailwayMap', 'OpenSeaMap', 'OpenSnowMap.pistes',
        'OpenStreetMap.BZH', 'OpenStreetMap.BlackAndWhite',
        'OpenStreetMap.CH', 'OpenStreetMap.DE', 'OpenStreetMap.HOT',
        'OpenStreetMap.Mapnik', 'OpenTopoMap', 'SafeCast',
        'Stadia.AlidadeSatellite', 'Stadia.AlidadeSmooth',
        'Stadia.AlidadeSmoothDark', 'Stadia.OSMBright',
        'Stadia.Outdoors', 'Stadia.StamenTerrain',
        'Stadia.StamenTerrainBackground', 'Stadia.StamenTerrainLabels',
        'Stadia.StamenTerrainLines', 'Stadia.StamenToner',
        'Stadia.StamenTonerBackground', 'Stadia.StamenTonerLabels',
        'Stadia.StamenTonerLines', 'Stadia.StamenTonerLite',
        'Stadia.StamenWatercolor', 'Strava.All', 'Strava.Ride',
        'Strava.Run', 'Strava.Water', 'Strava.Winter',
        'SwissFederalGeoportal.JourneyThroughTime',
        'SwissFederalGeoportal.NationalMapColor',
        'SwissFederalGeoportal.NationalMapGrey',
        'SwissFederalGeoportal.SWISSIMAGE', 'TopPlusOpen.Color',
        'TopPlusOpen.Grey', 'USGS.USImagery',
        'USGS.USImageryTopo', 'USGS.USTopo',
        'WaymarkedTrails.cycling', 'WaymarkedTrails.hiking',
        'WaymarkedTrails.mtb', 'WaymarkedTrails.riding',
        'WaymarkedTrails.skating', 'WaymarkedTrails.slopes',
        'nlmaps.grijs', 'nlmaps.luchtfoto', 'nlmaps.pastel',
        'nlmaps.standaard', 'nlmaps.water'
    ]

    # Selection boxes in the left and right columns
    with col1:
        left_layer = st.selectbox("Select left split map:", map_layers)

    with col3:
        right_layer = st.selectbox("Select right split map:", map_layers)

    # Create the map with the selected layers, centered on the USA
    m = leafmap.Map(center=(37.0902, -95.7129), zoom=4)
    m.split_map(left_layer=left_layer, right_layer=right_layer)

    # Add legends to the map based on selected layers
    left_legend = None
    right_legend = None

    if "NLCD" in left_layer:
        left_legend = "NLCD"
    elif "NWI" in left_layer:
        left_legend = "NWI"
    elif "MODIS" in left_layer:
        left_legend = "MODIS/051/MCD12Q1"
    elif "GLOBCOVER" in left_layer:
        left_legend = "GLOBCOVER"
    elif "JAXA/PALSAR" in left_layer:
        left_legend = "JAXA/PALSAR"
    elif "Oxford" in left_layer:
        left_legend = "Oxford"
    elif "AAFC/ACI" in left_layer:
        left_legend = "AAFC/ACI"
    elif "COPERNICUS/CORINE/V20/100m" in left_layer:
        left_legend = "COPERNICUS/CORINE/V20/100m"
    elif "COPERNICUS/Landcover/100m/Proba-V/Global" in left_layer:
        left_legend = "COPERNICUS/Landcover/100m/Proba-V/Global"
    elif "USDA/NASS/CDL" in left_layer:
        left_legend = "USDA/NASS/CDL"
    elif "ESA_WorldCover" in left_layer:
        left_legend = "ESA_WorldCover"

    if "NLCD" in right_layer:
        right_legend = "NLCD"
    elif "NWI" in right_layer:
        right_legend = "NWI"
    elif "MODIS" in right_layer:
        right_legend = "MODIS/051/MCD12Q1"
    elif "GLOBCOVER" in right_layer:
        right_legend = "GLOBCOVER"
    elif "JAXA/PALSAR" in right_layer:
        right_legend = "JAXA/PALSAR"
    elif "Oxford" in right_layer:
        right_legend = "Oxford"
    elif "AAFC/ACI" in right_layer:
        right_legend = "AAFC/ACI"
    elif "COPERNICUS/CORINE/V20/100m" in right_layer:
        right_legend = "COPERNICUS/CORINE/V20/100m"
    elif "COPERNICUS/Landcover/100m/Proba-V/Global" in right_layer:
        right_legend = "COPERNICUS/Landcover/100m/Proba-V/Global"
    elif "USDA/NASS/CDL" in right_layer:
        right_legend = "USDA/NASS/CDL"
    elif "ESA_WorldCover" in right_layer:
        right_legend = "ESA_WorldCover"

        # # Adding legends to the right side of the map
        # if left_legend:
        #     m.add_legend(builtin_legend=left_legend, position='topleft')  # Move left legend to top right
        # if right_legend:
        #     m.add_legend(builtin_legend=right_legend, position='bottomright')  # Keep right legend at bottom right


    # Display the map
    with col2:
        m.to_streamlit(height=700)
