# Extend GitHub Repo Traffic Tracking Beyond 14 Days

The GitHub traffic graph offers insights into visitor history, but it's limited to just the past 14 days. To overcome this limitation, we have built a simple web app that allows long-term tracking of GitHub repository traffic. This application is designed to automatically retrieve traffic data from your GitHub repository and append the latest records to those previously saved on a local server.

## Key Features:

- Long-Term Traffic Data Tracking: Keep a comprehensive history of your repository's traffic.
- Automatic Data Retrieval: The app automatically fetches and updates your traffic data.
- Simple Deployment: Built using Flask, this application can be easily deployed on your own web server.

## Getting Started:

To deploy this web application for your own use, you only need to make a few simple modifications in the ```app.py``` file:

- **GitHub ID**: Replace with your own GitHub username.
- **Repository Name**: Specify the repository you wish to track.
- **Personal Access Token**: Enter your GitHub personal access token to authorize data retrieval. <br >

Live Deployment Example: <br >
To see a demo, visit the following deployment: https://cellscopes.humphreyslab.com

<img src="https://github.com/HaojiaWu/14days_and_more/blob/main/demo.png" width="1000"> <br>
