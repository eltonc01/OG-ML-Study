import pandas as pd
import geopy.distance

df_wells = pd.read_excel(r'fracking wells.xlsx')
df_sites = pd.read_excel(r'prevalence sites.xlsx')
df_cities = pd.read_csv(r'co city data.csv')

a = 0.8
b = 2
c = 3
d = 10
e = 20
f = 50

for site_row in range(0, len(df_sites)):
    a_value = 0
    b_value = 0
    c_value = 0
    d_value = 0
    e_value = 0
    f_value = 0
    site_lat = df_sites.loc[site_row, 'Latitude']
    site_long = df_sites.loc[site_row, 'Longitude']
    location = [site_lat, site_long]
    for row in range(0, len(df_cities)):
        pop = df_cities.loc[row, 'Population']
        if pd.isnull(pop) is True:
            continue
        clat = df_cities.loc[row, 'CENTLAT']
        clong = df_cities.loc[row, 'CENTLON']
        cor = [clat, clong]
        cdistance = geopy.distance.distance(location, cor).km
        if pop >= 500000:
            radius = 15
            stren = 10
        elif pop >= 400000:
            radius = 12
            stren = 8
        elif pop >= 300000:
            radius = 8
            stren = 6
        elif pop >= 100000:
            radius = 6
            stren = 5
        elif pop >= 50000:
            radius = 4
            stren = 3
        elif pop >= 10000:
            radius = 3
            stren = 2
        elif pop >= 5000:
            radius = 2
            stren = 1
        else:
            radius = 1
            stren = 0.1
        dist2 = cdistance - (radius / 3)
        dist3 = cdistance - (radius * 2 / 3)
        dist4 = cdistance - radius
        df_cities.at[row, 'Radius'] = radius
        df_cities.at[row, 'Strength'] = stren

        if cdistance <= a:
            a_value += stren
            continue
        elif dist2 <= a:
            a_value += stren
            continue
        elif dist3 <= a:
            a_value += stren
            continue
        elif dist4 <= a:
            a_value += stren
            continue
        elif cdistance <= b:
            b_value += stren
            continue
        elif dist2 <= b:
            b_value += stren
            continue
        elif dist3 <= b:
            b_value += stren
            continue
        elif dist4 <= b:
            b_value += stren
            continue
        elif cdistance <= c:
            c_value += stren
            continue
        elif dist2 <= c:
            c_value += stren
            continue
        elif dist3 <= c:
            c_value += stren
            continue
        elif dist4 <= c:
            c_value += stren
            continue
        elif cdistance <= d:
            d_value += stren
            continue
        elif dist2 <= d:
            d_value += stren
            continue
        elif dist3 <= d:
            d_value += stren
            continue
        elif dist4 <= d:
            d_value += stren
            continue
        elif cdistance <= e:
            e_value += stren
            continue
        elif dist2 <= e:
            e_value += stren
            continue
        elif dist3 <= e:
            e_value += stren
            continue
        elif dist4 <= e:
            e_value += stren
            continue

    prevalence = (2 * a_value) + (1 * b_value) + (0.5 * c_value) + (0.2 * d_value) + (0.01 * e_value) * 3
    prevalence = round(prevalence, 3)
    print(prevalence)
    df_sites.at[site_row, 'City Prevalence'] = prevalence

df_sites.to_excel(r'prevalence sites.xlsx')
df_cities.to_csv(r'co city data.csv')
