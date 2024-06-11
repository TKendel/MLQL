import xml.etree.ElementTree as ET
import pandas as pd
import os
import gpxpy

def parse_gpx(file_path):
    points = []
    with open(file_path, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    point_data = {
                        'Timestamp': point.time,
                        'Latitude': point.latitude,
                        'Longitude': point.longitude,
                        'Elevation': point.elevation,
                        'Speed': float(point.extensions[0].text) if point.extensions else None,
                        'Course': float(point.extensions[1].text) if len(point.extensions) > 1 else None,
                        'hAcc': float(point.extensions[2].text) if len(point.extensions) > 2 else None,
                        'vAcc': float(point.extensions[3].text) if len(point.extensions) > 3 else None,
                    }
                    points.append(point_data)
    return points

def parse_export_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    heart_rates = []
    for record in root.findall('Record'):
        if record.get('type') == 'HKQuantityTypeIdentifierHeartRate':
            heart_rate_data = {
                'value': float(record.get('value')),
                'startDate': record.get('startDate'),
                'endDate': record.get('endDate')
            }
            heart_rates.append(heart_rate_data)
    
    heart_rate_df = pd.DataFrame(heart_rates)
    heart_rate_df['startDate'] = pd.to_datetime(heart_rate_df['startDate'])
    heart_rate_df['endDate'] = pd.to_datetime(heart_rate_df['endDate'])
    
    workouts = []
    for workout in root.findall('Workout'):
        workout_data = {
            'workoutActivityType': workout.get('workoutActivityType'),
            'duration': float(workout.get('duration', 0)),
            'totalEnergyBurned': float(workout.get('totalEnergyBurned', 0)),
            'startDate': workout.get('startDate'),
            'endDate': workout.get('endDate')
        }
        workouts.append(workout_data)
    
    workout_df = pd.DataFrame(workouts)
    workout_df['startDate'] = pd.to_datetime(workout_df['startDate'])
    workout_df['endDate'] = pd.to_datetime(workout_df['endDate'])
    return heart_rate_df, workout_df

def integrate_data(gpx_data, heart_rate_data, workout_data):
    heart_rate_data['startDate'] = heart_rate_data['startDate'].dt.tz_convert('UTC')
    heart_rate_data['endDate'] = heart_rate_data['endDate'].dt.tz_convert('UTC')
    workout_data['startDate'] = workout_data['startDate'].dt.tz_convert('UTC')
    workout_data['endDate'] = workout_data['endDate'].dt.tz_convert('UTC')
    gpx_data['Timestamp'] = pd.to_datetime(gpx_data['Timestamp']).dt.tz_convert('UTC')
    
    merged_data = pd.merge_asof(gpx_data.sort_values('Timestamp'), 
                                heart_rate_data.sort_values('startDate'), 
                                left_on='Timestamp', 
                                right_on='startDate', 
                                direction='backward')
    
    merged_data = pd.merge_asof(merged_data.sort_values('Timestamp'),
                                workout_data.sort_values('startDate'),
                                left_on='Timestamp',
                                right_on='startDate',
                                direction='backward')
    
    merged_data.rename(columns={
        'value': 'HeartRate',
        'startDate_x': 'startDate_y',
        'endDate_x': 'endDate_y',
        'startDate_y': 'startDate_y_workout',
        'endDate_y': 'endDate_y_workout'
    }, inplace=True)
    
    merged_data = merged_data[['Timestamp', 'Latitude', 'Longitude', 'Elevation', 'Speed', 'Course', 'HeartRate',
                               'duration', 'totalEnergyBurned', 'workoutActivityType']]
    
    merged_data.rename(columns={
        'startDate_y': 'startDate_y',
        'endDate_y': 'endDate_y',
        'workoutActivityType': 'Activity'
    }, inplace=True)
    
    return merged_data

def label_activities(row):
    if 'Cycling' in row['Activity']:
        return 'biking'
    elif 'Running' in row['Activity']:
        return 'running'
    elif 'Walking' in row['Activity']:
        return 'walking'
    elif row['Speed'] < 1 and row['HeartRate'] < 100:
        return 'relaxing'
    else:
        return 'unknown'

def main(gpx_directory, export_xml_path, output_file):
    all_gpx_data = []

    # Parse all GPX files
    for root, dirs, files in os.walk(gpx_directory):
        for file in files:
            if file.endswith('.gpx'):
                file_path = os.path.join(root, file)
                gpx_data = parse_gpx(file_path)
                all_gpx_data.extend(gpx_data)


    gpx_df = pd.DataFrame(all_gpx_data)
    heart_rate_df, workout_df = parse_export_xml(export_xml_path)
    integrated_data = integrate_data(gpx_df, heart_rate_df, workout_df)
    integrated_data['Activity'] = integrated_data.apply(label_activities, axis=1)

    integrated_data.to_csv(output_file, index=False)
    print(f"Integrated data saved to {output_file}")



gpx_directory = 'apple_health_export/workout-routes'
export_xml_path = 'apple_health_export/export.xml'
output_file = 'integrated_workout_data.csv'
main(gpx_directory, export_xml_path, output_file)
