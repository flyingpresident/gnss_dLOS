import numpy as np
import pyproj


def gcs2llh(xyz):
    '''    
    gcs2llh converts geocentric XYZ coordinates to WGS84 Latitude-Longitude-Height coordinates. 

    Input: 
    xyz: Geocentric coordinates (N*3, where N is the number of sites, in meters) 
    
    Output: 
        llh: Longitude (Column 0), Latitude (Column 1), and height (Column 2, in meters)
    
    Yosuke Aoki, January 2022
    '''

    xyzT = np.transpose(xyz)

    x = xyzT[0]
    y = xyzT[1]
    z = xyzT[2]

    transformer = pyproj.Transformer.from_crs("epsg:7789", "epsg:4326")
    # EPSG:7789 = ITRF2014 
    # EPSG:4326 = WGS84

    lat, lon, height = transformer.transform(xyzT[0], xyzT[1], xyzT[2])

    llh0 = [lon, lat, height]
    llh = np.transpose(llh0)
    
    return llh


def ll2UTM(ll, EPSG):
    '''
    ll2UTM converts Longitude-Latitude coordinates in WGS84 into the specified UTM coordinates. 

    Input: 
        ll: Longitude (Column 0) and Latitude (Column 1) in degrees 
        EPSG: Coordinate system                 
            EPSG:32651 	UTM51 (120-126E)
            EPSG:32652 	UTM52 (126-132E)
            EPSG:32653 	UTM53 (132-138E)
            EPSG:32654 	UTM54 (138-144E)
            EPSG:32655 	UTM55 (144-150E)
    Output:  
        xy: UTM coordinates in kilometers

    Yosuke Aoki, January 2022
    '''
    llT = np.transpose(ll)
    lat = llT[1]
    lon = llT[0]

    tr = pyproj.Transformer.from_proj(4326, EPSG)

    x, y = tr.transform(lat, lon)
    x_km = x / 1000
    y_km = y / 1000

    xy = np.transpose([x_km, y_km]) 

    return xy 

