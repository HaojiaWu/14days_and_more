from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import json
import plotly
import csv
import os
import datetime
import numpy as np
import requests

app = Flask(__name__)

def fetch_traffic_data(owner, repo, token):
    ACCESS_TOKEN = token
    OWNER = owner
    REPO = repo
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
    headers = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        views_data = response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
    traffic_data_new = pd.DataFrame(pd.DataFrame(views_data)['views'].tolist())
    return traffic_data_new

def update_traffic_data():
    traffic_data_old = pd.read_csv("traffic_data_current.csv", index_col=0)
    traffic_data_old.to_csv("traffic_data_old.csv")
    traffic1 = fetch_traffic_data("your_ID", "your_repo", "use_your_own_token")
    traffic2 = fetch_traffic_data("your_other_ID", "your_other_fork_reop", "use_your_own_token")
    merged_df = pd.merge(traffic1, traffic2, on='timestamp', how='outer', suffixes=('_df1', '_df2'))
    for col in ['count', 'uniques']:
        merged_df[f'{col}_df1'].fillna(0, inplace=True)
        merged_df[f'{col}_df2'].fillna(0, inplace=True)
        merged_df[col] = merged_df[f'{col}_df1'] + merged_df[f'{col}_df2']
    traffic_data_new = merged_df[['timestamp', 'count', 'uniques']]
    date1=traffic_data_old["timestamp"].tolist()
    date2=traffic_data_new["timestamp"].tolist()
    diff_dates = list(set(date2) - set(date1))
    diff_rows = traffic_data_new[traffic_data_new['timestamp'].isin(diff_dates)]
    traffic_data_update = traffic_data_old._append(diff_rows, ignore_index=True)
    traffic_data_update.to_csv("traffic_data_current.csv")


update_traffic_data()

@app.route('/')
def index():
    traffic_file = 'traffic_data_current.csv'
    if os.path.exists(traffic_file):
        traffic_data = pd.read_csv(traffic_file, index_col=0)
        traffic_data['count'] = np.cumsum(traffic_data['count'].tolist())
        fig_views = px.line(traffic_data, x='timestamp', y='count', title='GitHub Views Over Time',
             labels={
                     "timestamp": "Date",
                     "count": "Total views"
                 }
             ).update_layout(plot_bgcolor='lavenderblush')
        traffic_data['uniques'] = np.cumsum(traffic_data['uniques'].tolist())
        fig_uniques = px.line(traffic_data, x='timestamp', y='uniques', title='GitHub Visitors Over Time',
             labels={
                     "timestamp": "Date",
                     "uniques": "Unique Visitors"
                 }
             ).update_layout(plot_bgcolor='lightcyan').update_traces(line=dict(color='darkred'))
        graphJSON = json.dumps({
            'views': json.loads(fig_views.to_json()),
            'uniques': json.loads(fig_uniques.to_json()),
        }, cls=plotly.utils.PlotlyJSONEncoder)

    else:
        graphJSON = None
  
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)

