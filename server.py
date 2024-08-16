from flask import Flask, render_template, request, jsonify
from waitress import serve
import app_settings as app_settings
from api.Export_Flows import main, download_flows
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/test')
def test():
    print('ffds')
    return render_template("test.html")

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
    
@app.route('/api/export', methods=['POST'])
def api_endpoint():
    response_data = ''
    try:
        response_data =  main()
        print(response_data)
        return jsonify({'message': 'API call successful', 'data': 'good'})
    except:
        print(response_data)
        print(jsonify({'message': 'API call failed', 'error': str('error')}), 500)
        return render_template("index.html")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
