import os

data_dir = r'C:\Users\mbexkes3\Downloads\MIDAS-open\uk-daily-rain-obs'
all_files = {}
name_filename = {}
for path, dir, files in os.walk(data_dir):
    if data_dir == path:
        continue
    directory_name = path
    directory_name = directory_name.split('\\')
    name_filename[directory_name[-1].replace('-', '')] = directory_name[-1]
    files.remove(files[0])
    all_files[directory_name[-1].replace('-','')] = files
    all_files[directory_name[-1].replace('-','')].append(path)

print(all_files)

array = []
for key,value in all_files.items():
    string = key.split('\\')
    array.append(f'{string[-1]}')
import streamlit as st
for key,value in all_files.items():
    all_files[key].remove(all_files[key][0])
import pandas as pd


st.title('Rainfall in the North of Scotland')
option = st.selectbox('Select region:', array)
st.write('Region selected:',option)

filename = os.path.join(all_files[option][-1], all_files[option][-2])

data = pd.read_csv(filename, skiprows = 61)
st.header(f'Most recent Year rainfall: {option}')
data['Date'] = data['ob_date']
data['Percipitation Amount'] = data['prcp_amt']

st.line_chart(data, x = 'Date', y = 'Percipitation Amount')

locations = {}

with open(r'C:\Users\mbexkes3\Downloads\MIDAS-open\excel_list_station_details.csv') as new_file:
    for line in new_file:
        line = line.strip()
        line = line.replace(' ','')
        line = line.split(',')
        for key,value in all_files.items():
            if key in (line[1].replace(':','')).lower():
                print(line[1].lower())
                locations[key] = (float(line[-3]),float(line[-2]))
import folium
from streamlit_folium import st_folium
m = folium.Map(location=[locations['baltasound'][0], locations['baltasound'][1]], zoom_start=6)
folium.Marker([locations['baltasound'][0], locations['baltasound'][1]], popup= key, tooltip=key).add_to(m)

mean_years = {}
for key,value in locations.items():
    direct = os.path.join(data_dir,name_filename[key])
    year_mean = []
    for csv_file in all_files[key]:
        if 'lock' in csv_file:
            continue
        csv = os.path.join(direct,csv_file)
        if 'csv' not in csv:
            continue
        df = pd.read_csv(csv,skiprows=61)
        mean = round(df['prcp_amt'].mean(skipna=True),2)
        year = (csv.split('_')[-1])[:4]
        year_mean.append((year,mean))
    mean_years[key] = year_mean
    folium.Marker([locations[key][0], locations[key][1]], popup=key, tooltip=key).add_to(m)
years = []
mean_rain = []

for item in mean_years[option]:
    years.append(item[0])
    mean_rain.append(item[1])

print(option)
print(years)
print(mean_rain)

data_table = {'Year':years,'Avg Rainfall':mean_rain}
df = pd.DataFrame(data_table)
st.sidebar.title(f'Average Rainfall Per Year Table for {option}')
st.sidebar.table(df)
st.header('Map of weather stations for regions')
st_data = st_folium(m, width=725)
