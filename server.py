from flask import Flask, render_template, request, jsonify
from waitress import serve
import app_settings as app_settings
from api.export.Export_Flows import download_flows
from api.export.Export_Modules import download_modules
from api.export.Export_Bots import download_bots
from api.export.Export_Queues import download_queues
import subprocess
import os
app = Flask(__name__)

@app.route('/test')
def test():
    print('ffds')
    return render_template("test.html")

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(current_dir, "downloads")
    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    return render_template("index.html")


@app.route('/index_response', methods=['POST'])
def index_response():
    app_settings.settings['SOURCE_ACCESS_KEY'] = request.form['source_access_key']
    app_settings.settings['SOURCE_SECRET_KEY'] = request.form['source_secret_key']
    app_settings.settings['SOURCE_SESSION_TOKEN'] = request.form['source_session_token']
    app_settings.settings['SOURCE_INSTANCE_ID'] = request.form['source_instance_id']
    app_settings.settings['SOURCE_REGION'] = request.form['source_region']
    app_settings.settings['DESTINATION_ACCESS_KEY'] = request.form['dest_access_key']
    app_settings.settings['DESTINATION_SECRET_KEY'] = request.form['dest_secret_key']
    app_settings.settings['DESTINATION_SESSION_TOKEN'] = request.form['dest_session_token']
    app_settings.settings['DESTINATION_INSTANCE_ID'] = request.form['dest_instance_id']
    app_settings.settings['DESTINATION_REGION'] = request.form['dest_region']
    settings = app_settings.settings
    if (request.form['action'] == 'export'):
        return render_template("export.html", settings=settings)
    else:
        return render_template("error.html")

@app.route('/download_flows', methods=['POST'])
def download_flows_route():
    response = download_flows()
    if response['statusResponse'] == 'GOOD':
         return jsonify({'status': 'executed', 'statusCode': response['statusCode'], 'data': response})
    else:
        return jsonify({'status': 'failed', 'statusCode': response['statusCode'], 'exception':response['exception']})
@app.route('/download_modules', methods=['POST'])
def download_modules_route():
    response = download_modules()
    if response['statusResponse'] == 'GOOD':
         return jsonify({'status': 'executed', 'statusCode': response['statusCode'], 'data': response})
    else:
        return jsonify({'status': 'failed', 'statusCode': response['statusCode'], 'exception':response['exception']})
@app.route('/download_bots', methods=['POST'])
def download_bots_route():
    response = download_bots()
    print('resp: ', response)
    if response['statusResponse'] == 'GOOD':
        return jsonify({'status': 'executed', 'statusCode': response['statusCode'], 'data': response})
    else:
        return jsonify({'status': 'failed', 'statusCode': response['statusCode'], 'exception':response['exception']})
@app.route('/download_queues', methods=['POST'])
def download_queues_route():
    response = download_queues()
    print('resp: ', response)
    if response['statusResponse'] == 'GOOD':
        return jsonify({'status': 'executed', 'statusCode': response['statusCode'], 'data': response})
    else:
        return jsonify({'status': 'failed', 'statusCode': response['statusCode'], 'exception':response['exception']})
        #return jsonify({'status': 'failed', 'message': 'An error occurred during the download process', 'error_code': response['statusCode']})

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
