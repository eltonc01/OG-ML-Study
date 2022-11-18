import pandas as pd
from openpyxl import load_workbook
from modules import wind_direction, city_wind_strength, well_activity_center
import geopy.distance

df_direction = pd.read_csv(r'C:\Users\elton\projects\hourly wind direction.csv')
df_speed = pd.read_csv(r'C:\Users\elton\projects\daily wind speed.csv')
df_ozone = pd.read_csv(r'C:\Users\elton\projects\nox.csv')
df_wells = pd.read_excel(r'C:\Users\elton\projects\fracking wells.xlsx')
df_sites = pd.read_excel(r'C:\Users\elton\projects\prevalence sites no2.xlsx')
df_cities = pd.read_csv(r'C:\Users\elton\projects\co city data.csv')

wb = load_workbook(r'C:\Users\elton\projects\template.xlsx')
sheet = wb.active

june = '2021-06'
july = '2021-07'
aug = '2021-08'

old_lat = df_ozone.loc[0, 'Latitude']

site = True
p = False
for row in range(1, len(df_ozone)):
    latitude = df_ozone.loc[row, 'Latitude']
    longitude = df_ozone.loc[row, 'Longitude']
    name = df_ozone.loc[row, 'Local Site Name']
    key = df_ozone.loc[row, 'Date Local']
    '''if key.find(june) != -1 or key.find(july) != -1 or key.find(aug) != -1:
        pass
    else:
        continue'''
    print(name)
    if latitude == old_lat and p is True:
        continue
    s = False
    t = False
    for r1 in range(0, len(df_sites)):
        if round(latitude, 4) == round(df_sites.loc[r1, 'Latitude'], 4) and round(longitude, 4) == round(
                df_sites.loc[r1, 'Longitude'], 4):
            prev = r1
            if df_sites.loc[r1, 'Exempt'] == 'Yes':
                s = True
            t = True
            break
    if t is False:
        continue
    if s is True:
        continue
    date = df_ozone.loc[row, 'Date Local']
    wind = wind_direction(latitude, longitude, date)
    print(wind)
    n = wind[0]
    ne = wind[1]
    e = wind[2]
    se = wind[3]
    swind = wind[4]
    sw = wind[5]
    w = wind[6]
    nw = wind[7]
    if n == 0 and ne == 0 and e == 0 and se == 0 and s == 0 and sw == 0 and w == 0 and nw == 0:
        p = True
        continue
    p = False
    if latitude != old_lat or site is True:
        wells = well_activity_center(latitude, longitude, n, ne, e, se, s, sw, w, nw)
        north = wells[0]
        northeast = wells[1]
        east = wells[2]
        southeast = wells[3]
        south = wells[4]
        southwest = wells[5]
        west = wells[6]
        northwest = wells[7]
        cities = city_wind_strength(latitude, longitude)
        cn = cities[0]
        cne = cities[1]
        ce = cities[2]
        cse = cities[3]
        cs = cities[4]
        csw = cities[5]
        cw = cities[6]
        cnw = cities[7]
        site = False
    for r in range(0, len(df_speed)):
        if date == df_speed.loc[r, 'Date Local']:
            speed = df_speed.loc[r, 'Arithmetic Mean']
            break
    df_north1 = pd.read_csv('wells_north.csv')
    df_northeast1 = pd.read_csv('wells_northeast.csv')
    df_east1 = pd.read_csv('wells_east.csv')
    df_southeast1 = pd.read_csv('wells_southeast.csv')
    df_south1 = pd.read_csv('wells_south.csv')
    df_southwest1 = pd.read_csv('wells_southwest.csv')
    df_west1 = pd.read_csv('wells_west.csv')
    df_northwest1 = pd.read_csv('wells_northwest.csv')
    north_iter = 0
    northeast_iter = 0
    east_iter = 0
    southeast_iter = 0
    south_iter = 0
    southwest_iter = 0
    west_iter = 0
    northwest_iter = 0

    z = float(speed)
    a = 5

    for direc in range(0, 8):
        site_coord = [latitude, longitude]
        if direc == 0:
            L = geopy.distance.distance(site_coord, north).km
            s = 0.0
            for num in range(1, len(df_north1)):
                if pd.isnull(df_north1.iloc[num, 2]) is True:
                    continue
                s += float(round(df_north1.iloc[num, 2], 3))
            s = (s / 2) + ((z) - 5)
            x = n
            if L != 0:
                north_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                north_iter = 0
        elif direc == 1:
            L = geopy.distance.distance(site_coord, northeast).km
            s = 0.0
            for num in range(1, len(df_northeast1)):
                if pd.isnull(df_northeast1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_northeast1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = ne
            if L != 0:
                northeast_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                northeast_iter = 0
        elif direc == 2:
            L = geopy.distance.distance(site_coord, east).km
            s = 0.0
            for num in range(1, len(df_east1)):
                if pd.isnull(df_east1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_east1.iloc[num, 2]), 3)
            x = e
            s = (s / 2) + ((5 * z) - 25)
            if L != 0:
                east_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                east_iter = 0
        elif direc == 3:
            L = geopy.distance.distance(site_coord, southeast).km
            s = 0.0
            for num in range(1, len(df_southeast1)):
                if pd.isnull(df_southeast1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_southeast1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = se
            if L != 0:
                southeast_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                southeast_iter = 0
        elif direc == 4:
            L = geopy.distance.distance(site_coord, south).km
            s = 0.0
            for num in range(1, len(df_south1)):
                if pd.isnull(df_south1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_south1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = swind
            if L != 0:
                south_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                south_iter = 0
        elif direc == 5:
            L = geopy.distance.distance(site_coord, southwest).km
            s = 0.0
            for num in range(1, len(df_southwest1)):
                if pd.isnull(df_southwest1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_southwest1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = sw
            if L != 0:
                southwest_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                southwest_iter = 0
        elif direc == 6:
            L = geopy.distance.distance(site_coord, west).km
            s = 0.0
            for num in range(1, len(df_west1)):
                if pd.isnull(df_west1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_west1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = w
            if L != 0:
                west_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                west_iter = 0
        elif direc == 7:
            L = geopy.distance.distance(site_coord, northwest).km
            s = 0.0
            for num in range(1, len(df_northwest1)):
                if pd.isnull(df_northwest1.iloc[num, 2]) is True:
                    continue
                s += round(float(df_northwest1.iloc[num, 2]), 3)
            s = (s / 2) + ((5 * z) - 25)
            x = nw
            if L != 0:
                northwest_iter = (15 / L) * (s) * x / a * 10
            if s < 0:
                northwest_iter = 0

    bn = round(cn, 2) * round(n, 2)
    bne = round(cne, 2) * round(ne, 2)
    be = round(ce, 2) * round(e, 2)
    bse = round(cse, 2) * round(se, 2)
    bs = round(cs, 2) * round(swind, 2)
    bsw = round(csw, 2) * round(sw, 2)
    bw = round(cw, 2) * round(w, 2)
    bnw = round(cnw, 2) * round(nw, 2)

    wind_prevalence = north_iter + northeast_iter + east_iter + \
                      southeast_iter + south_iter + southwest_iter + west_iter + northwest_iter
    if wind_prevalence == 0:
        continue
    total = df_sites.loc[r1, 'Value']
    city = df_sites.loc[prev, 'City Prevalence']
    city1 = (bn + bne + be + bse + bs + bsw + bw + bnw) / 30
    city2 = city / 35
    city_prevalence = city1 + city2
    city_multiplier = city_prevalence
    if city_multiplier >= 1:
        city_multiplier = 1
    city_multiplier = (12.6 * city_multiplier)
    print(city1)
    print(city_prevalence)
    # prevalence = df_sites.loc[r1, 'Prevalence']
    # overall = wind_prevalence + prevalence
    prevalence = df_sites.loc[r1, 'Prevalence 2']
    overall = prevalence + wind_prevalence
    mean = df_ozone.loc[row, "Arithmetic Mean"]
    mean2 = df_ozone.loc[row, "Arithmetic Mean"] - city_multiplier
    if mean2 < 0:
        mean2 = 0
    maximum = df_ozone.loc[row, '1st Max Value']
    maximum2 = df_ozone.loc[row, '1st Max Value'] - city_multiplier
    if maximum2 < 0:
        maximum2 = 0
    old_lat = latitude
    print(f'{overall}: {mean}')
    sheet.append([prevalence, mean, mean2, maximum, maximum2, wind_prevalence, overall, city_prevalence, total, z, name])

wb.save(r'C:\Users\elton\projects\wind and ozone summer.xlsx')
