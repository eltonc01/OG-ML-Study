import pandas as pd
from openpyxl import load_workbook
import geopy.distance
import math
from shapely.geometry.point import Point
import numpy

df_direction = pd.read_csv(r'C:\Users\elton\projects\hourly wind direction.csv')
df_speed = pd.read_csv(r'C:\Users\elton\projects\daily wind speed.csv')
df_ozone = pd.read_csv(r'C:\Users\elton\projects\no2.csv')
df_wells = pd.read_excel(r'C:\Users\elton\projects\fracking wells.xlsx')
df_sites = pd.read_excel(r'C:\Users\elton\projects\prevalence sites original.xlsx')
df_cities = pd.read_csv(r'C:\Users\elton\projects\co city data.csv')

wb = load_workbook(r'C:\Users\elton\projects\template.xlsx')
sheet = wb.active


def well_activity_center(lat_input, long_input):
    lat_input = float(lat_input)
    long_input = float(long_input)
    for num1 in range(0, 8):
        name = 'str'
        if num1 == 0:
            name = 'wells_north.csv'
        elif num1 == 1:
            name = 'wells_northeast.csv'
        elif num1 == 2:
            name = 'wells_east.csv'
        elif num1 == 3:
            name = 'wells_southeast.csv'
        elif num1 == 4:
            name = 'wells_south.csv'
        elif num1 == 5:
            name = 'wells_southwest.csv'
        elif num1 == 6:
            name = 'wells_west.csv'
        elif num1 == 7:
            name = 'wells_northwest.csv'
        lat = [0]
        long = [0]
        val = [0]
        toprow = {'Latitude': lat, 'Longitude': long, 'Value': val}
        df = pd.DataFrame(toprow)
        df.to_csv(name)
    loc = [lat_input, long_input]
    for row in range(0, len(df_wells)):
        temp_lat = df_wells.loc[row, 'Latitude']
        temp_long = df_wells.loc[row, 'Longitude']
        temp_loc = [temp_lat, temp_long]
        dist = geopy.distance.distance(loc, temp_loc).km
        if 20 <= dist <= 50:
            value = df_wells.loc[row, 'Oil or Gas']
            '''if value > 0.1:
                value = value - (value * 0.5)
            if value < 0.1:
                value = 0.1'''
            hyp = math.hypot(abs(lat_input - temp_lat), abs(long_input - temp_long))
            # print(f'Hyp: {hyp}')
            angle = 0
            adj_dist = abs(long_input - temp_long)
            adj_dist_ref = -(long_input - temp_long)
            opp = -(lat_input - temp_lat)
            # print(f'Adj: {adj_dist_ref}, Opp: {opp}')
            rad = (abs(adj_dist) / hyp)
            deg = math.degrees(math.acos(rad))
            # print(f'Deg: {deg}')
            if opp < 0:
                if adj_dist_ref < 0:
                    angle = 90 - deg + 180
                elif adj_dist_ref > 0:
                    angle = deg + 90
            elif opp > 0:
                if adj_dist_ref < 0:
                    angle = deg + 270
                elif adj_dist_ref > 0:
                    angle = 90 - deg
            # print(f'Angle: {angle}')
            if angle <= 22.5 or angle > 337.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_north.csv', mode='a', index=False, header=False)
            elif 67.5 >= angle > 22.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_northeast.csv', mode='a', index=False, header=False)
            elif 112.5 >= angle > 67.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_east.csv', mode='a', index=False, header=False)
            elif 157.5 >= angle > 112.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_southeast.csv', mode='a', index=False, header=False)
            elif 202.5 >= angle > 157.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_south.csv', mode='a', index=False, header=False)
            elif 247.5 >= angle > 202.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_southwest.csv', mode='a', index=False, header=False)
            elif 292.5 >= angle > 247.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_west.csv', mode='a', index=False, header=False)
            elif 337.5 >= angle > 292.5:
                data = {
                    'Latitude': [temp_lat],
                    'Longitude': [temp_long],
                    'Value': [value]
                }
                df = pd.DataFrame(data)
                df.to_csv('wells_northwest.csv', mode='a', index=False, header=False)
    df_north = pd.read_csv('wells_north.csv')
    df_northeast = pd.read_csv('wells_northeast.csv')
    df_east = pd.read_csv('wells_east.csv')
    df_southeast = pd.read_csv('wells_southeast.csv')
    df_south = pd.read_csv('wells_south.csv')
    df_southwest = pd.read_csv('wells_southwest.csv')
    df_west = pd.read_csv('wells_west.csv')
    df_northwest = pd.read_csv('wells_northwest.csv')
    nlat_avg = 0
    nlong_avg = 0
    for n in range(0, len(df_north)):
        nlat_avg += df_north.iloc[n, 0]
        nlong_avg += df_north.iloc[n, 1]
    if len(df_north) != 1:
        # print(nlat_avg)
        # print(nlong_avg)
        nlat_avg = nlat_avg / (len(df_north) - 1)
        nlong_avg = nlong_avg / (len(df_north) - 1)
    ncenter = [nlat_avg, nlong_avg]
    nelat_avg = 0
    nelong_avg = 0
    for n in range(0, len(df_northeast)):
        nelat_avg += df_northeast.iloc[n, 0]
        nelong_avg += df_northeast.iloc[n, 1]
    if len(df_northeast) != 1:
        nelat_avg = nelat_avg / (len(df_northeast) - 1)
        nelong_avg = nelong_avg / (len(df_northeast) - 1)
    necenter = [nelat_avg, nelong_avg]
    elat_avg = 0
    elong_avg = 0
    for n in range(0, len(df_east)):
        elat_avg += df_east.iloc[n, 0]
        elong_avg += df_east.iloc[n, 1]
    if len(df_east) != 1:
        elat_avg = elat_avg / (len(df_east) - 1)
        elong_avg = elong_avg / (len(df_east) - 1)
    ecenter = [elat_avg, elong_avg]
    selat_avg = 0
    selong_avg = 0
    for n in range(0, len(df_southeast)):
        selat_avg += df_southeast.iloc[n, 0]
        selong_avg += df_southeast.iloc[n, 1]
    if len(df_southeast) != 1:
        selat_avg = selat_avg / (len(df_southeast) - 1)
        selong_avg = selong_avg / (len(df_southeast) - 1)
    secenter = [selat_avg, selong_avg]
    slat_avg = 0
    slong_avg = 0
    for n in range(0, len(df_south)):
        slat_avg += df_south.iloc[n, 0]
        slong_avg += df_south.iloc[n, 1]
    if len(df_south) != 1:
        slat_avg = slat_avg / (len(df_south) - 1)
        slong_avg = slong_avg / (len(df_south) - 1)
    scenter = [slat_avg, slong_avg]
    swlat_avg = 0
    swlong_avg = 0
    for n in range(0, len(df_southwest)):
        swlat_avg += df_southwest.iloc[n, 0]
        swlong_avg += df_southwest.iloc[n, 1]
    if len(df_southwest) != 1:
        swlat_avg = swlat_avg / (len(df_southwest) - 1)
        swlong_avg = swlong_avg / (len(df_southwest) - 1)
    swcenter = [swlat_avg, swlong_avg]
    wlat_avg = 0
    wlong_avg = 0
    for n in range(0, len(df_west)):
        wlat_avg += df_west.iloc[n, 0]
        wlong_avg += df_west.iloc[n, 1]
    if len(df_west) != 1:
        wlat_avg = wlat_avg / (len(df_west) - 1)
        wlong_avg = wlong_avg / (len(df_west) - 1)
    wcenter = [wlat_avg, wlong_avg]
    nwlat_avg = 0
    nwlong_avg = 0
    for n in range(0, len(df_northwest)):
        nwlat_avg += df_northwest.iloc[n, 0]
        nwlong_avg += df_northwest.iloc[n, 1]
    if len(df_northwest) != 1:
        nwlat_avg = nwlat_avg / (len(df_northwest) - 1)
        nwlong_avg = nwlong_avg / (len(df_northwest) - 1)
    nwcenter = [nwlat_avg, nwlong_avg]

    return ncenter, necenter, ecenter, secenter, scenter, swcenter, wcenter, nwcenter, df_north, df_northeast, df_east, df_southeast, df_south, df_southwest, df_west, df_northwest

    # ncenter, necenter, ecenter, secenter, scenter, swcenter, wcenter, nwcenter


def city_wind_strength(lat_input, long_input):
    lat_input = float(lat_input)
    long_input = float(long_input)
    for num1 in range(0, 8):
        name = 'str'
        if num1 == 0:
            name = 'cities_north.csv'
        elif num1 == 1:
            name = 'cities_northeast.csv'
        elif num1 == 2:
            name = 'cities_east.csv'
        elif num1 == 3:
            name = 'cities_southeast.csv'
        elif num1 == 4:
            name = 'cities_south.csv'
        elif num1 == 5:
            name = 'cities_southwest.csv'
        elif num1 == 6:
            name = 'cities_west.csv'
        elif num1 == 7:
            name = 'cities_northwest.csv'
        lat = [0]
        long = [0]
        val = [0]
        rad = [0]
        stre = [0]
        toprow = {'Latitude': lat, 'Longitude': long, 'Value': val, 'Radius': rad, 'Strength': stre}
        df = pd.DataFrame(toprow)
        df.to_csv(name)
    loc = [lat_input, long_input]
    for row in range(0, len(df_cities)):
        radius = float(df_cities.loc[row, 'Radius'])
        if pd.isnull(radius) is True:
            continue
        temp_lat = df_cities.loc[row, 'CENTLAT']
        temp_long = df_cities.loc[row, 'CENTLON']
        temp_loc = [temp_lat, temp_long]
        name = df_cities.loc[row, 'BASENAME']
        dist = geopy.distance.distance(loc, temp_loc).km
        if dist - radius > 50:
            continue
        current_point = [temp_lat, temp_long]
        stren = df_cities.loc[row, 'Strength']
        stren = stren * 0.1
        pop = df_cities.loc[row, 'Population']
        for a in range(0, 3):
            if a == 0:
                b = 1 / 3
                order = 1
            elif a == 1:
                b = 2 / 3
                order = 0.5
            elif a == 2:
                b = 1
                order = 0.2
            lat = temp_lat
            long = temp_long
            temp_location = [temp_lat, temp_long]
            num = False
            while not num:
                dist = geopy.distance.distance(current_point, temp_location).km
                if round(dist, 1) == round(radius * b, 1):
                    num = True
                elif round(dist, 1) < round(radius * b, 1):
                    lat -= 0.0001
                elif round(dist, 1) > round(radius * b, 1):
                    lat += 0.0001
                temp_location = [lat, long]
            latref = temp_lat - lat
            tlat = temp_lat
            tlong = temp_long
            lnum = False
            while not lnum:
                t_loc = [tlat, tlong]
                t_dist = geopy.distance.distance(current_point, t_loc).km
                if round(t_dist, 1) == round(radius * b, 1):
                    lnum = True
                elif round(t_dist, 1) < round(radius * b, 1):
                    tlong -= 0.0001
                elif round(t_dist, 1) > round(radius * b, 1):
                    tlong += 0.0001
            longref = (abs(temp_long - tlong) + abs(latref)) / 2
            circle = Point(temp_lat, temp_long).buffer(longref)
            points = numpy.array(list(circle.exterior.coords))
            pnum1 = 0
            pnum2 = 0
            pnum3 = 0
            for row in range(0, len(points)):
                dist = geopy.distance.distance(loc, points[row]).km
                if 20 <= dist <= 50:
                    if order == 1:
                        pnum1 += 1
                    elif order == 0.5:
                        pnum2 += 1
                    elif order == 0.2:
                        pnum3 += 1
                    if order == 1 and pnum1 >= 40:
                        continue
                    elif order == 2 and pnum2 >= 40:
                        continue
                    elif order == 3 and pnum3 >= 40:
                        continue
                    value = pop
                    hyp = math.hypot(abs(lat_input - temp_lat), abs(long_input - temp_long))
                    # print(f'Hyp: {hyp}')
                    angle = 0
                    adj_dist = abs(long_input - temp_long)
                    adj_dist_ref = -(long_input - temp_long)
                    opp = -(lat_input - temp_lat)
                    # print(f'Adj: {adj_dist_ref}, Opp: {opp}')
                    rad = (abs(adj_dist) / hyp)
                    deg = math.degrees(math.acos(rad))
                    # print(f'Deg: {deg}')
                    if opp < 0:
                        if adj_dist_ref < 0:
                            angle = 90 - deg + 180
                        elif adj_dist_ref > 0:
                            angle = deg + 90
                    elif opp > 0:
                        if adj_dist_ref < 0:
                            angle = deg + 270
                        elif adj_dist_ref > 0:
                            angle = 90 - deg
                    # print(f'Angle: {angle}')
                    if angle <= 22.5 or angle > 337.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_north.csv', mode='a', index=False, header=False)
                    elif 67.5 >= angle > 22.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_northeast.csv', mode='a', index=False, header=False)
                    elif 112.5 >= angle > 67.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_east.csv', mode='a', index=False, header=False)
                    elif 157.5 >= angle > 112.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_southeast.csv', mode='a', index=False, header=False)
                    elif 202.5 >= angle > 157.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_south.csv', mode='a', index=False, header=False)
                    elif 247.5 >= angle > 202.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_southwest.csv', mode='a', index=False, header=False)
                    elif 292.5 >= angle > 247.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_west.csv', mode='a', index=False, header=False)
                    elif 337.5 >= angle > 292.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value],
                            'Radius': [order],
                            'Strength': [stren]
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('cities_northwest.csv', mode='a', index=False, header=False)

    df_north = pd.read_csv('cities_north.csv')
    df_northeast = pd.read_csv('cities_northeast.csv')
    df_east = pd.read_csv('cities_east.csv')
    df_southeast = pd.read_csv('cities_southeast.csv')
    df_south = pd.read_csv('cities_south.csv')
    df_southwest = pd.read_csv('cities_southwest.csv')
    df_west = pd.read_csv('cities_west.csv')
    df_northwest = pd.read_csv('cities_northwest.csv')
    n_value = 0
    for n in range(0, len(df_north)):
        n_value += df_north.iloc[n, 4] * df_north.iloc[n, 3] * 0.1
    ne_value = 0
    for n in range(0, len(df_northeast)):
        ne_value += df_northeast.iloc[n, 4] * df_northeast.iloc[n, 3] * 0.1
    e_value = 0
    for n in range(0, len(df_east)):
        e_value += df_east.iloc[n, 4] * df_east.iloc[n, 3] * 0.1
    se_value = 0
    for n in range(0, len(df_southeast)):
        se_value += df_southeast.iloc[n, 4] * df_southeast.iloc[n, 3] * 0.1
    s_value = 0
    for n in range(0, len(df_south)):
        s_value += df_south.iloc[n, 4] * df_south.iloc[n, 3] * 0.1
    sw_value = 0
    for n in range(0, len(df_southwest)):
        sw_value += df_southwest.iloc[n, 4] * df_southwest.iloc[n, 3] * 0.1
    w_value = 0
    for n in range(0, len(df_west)):
        w_value += df_west.iloc[n, 4] * df_west.iloc[n, 3] * 0.1
    nw_value = 0
    for n in range(0, len(df_northwest)):
        nw_value += df_northwest.iloc[n, 4] * df_northwest.iloc[n, 3] * 0.1

    return n_value, ne_value, e_value, se_value, s_value, sw_value, w_value, nw_value


def wind_direction(site_lat, site_long, date):
    val = False
    n = 0
    ne = 0
    e = 0
    se = 0
    s = 0
    sw = 0
    w = 0
    nw = 0
    v = 0
    b = False
    for r in range(0, len(df_direction)):
        val = False
        if round(site_lat, 3) == round(df_direction.loc[r, 'Latitude'], 3) and round(site_long, 3) == round(
                df_direction.loc[r, 'Longitude'], 3):
            if date == df_direction.loc[r, 'Date Local']:
                val = True
                b = True
                angle = df_direction.loc[r, 'Sample Measurement']
                if angle <= 22.5 or angle > 337.5:
                    n += 1
                elif 67.5 >= angle > 22.5:
                    ne += 1
                elif 112.5 >= angle > 67.5:
                    e += 1
                elif 157.5 >= angle > 112.5:
                    se += 1
                elif 202.5 >= angle > 157.5:
                    s += 1
                elif 247.5 >= angle > 202.5:
                    sw += 1
                elif 292.5 >= angle > 247.5:
                    w += 1
                elif 337.5 >= angle > 292.5:
                    nw += 1
        if val is True:
            points = n + ne + e + se + s + sw + w + nw
            for i in range(0, 8):
                if i == 0:
                    n = n / points
                elif i == 1:
                    ne = ne / points
                elif i == 2:
                    e = e / points
                elif i == 3:
                    se = se / points
                elif i == 4:
                    s = s / points
                elif i == 5:
                    sw = sw / points
                elif i == 6:
                    w = w / points
                elif i == 7:
                    nw = nw / points
        if b is True:
            v += 1
        if v >= 25:
            break
    n = round(n, 3)
    ne = round(ne, 3)
    e = round(e, 3)
    se = round(se, 3)
    s = round(s, 3)
    sw = round(sw, 3)
    w = round(w, 3)
    nw = round(nw, 3)

    return n, ne, e, se, s, sw, w, nw
