from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename
from database import init_db, insert_data
from cleansing import clean_text, clean_csv, clean_text_with_sastrawi
from database import DATABASE
import os, sqlite3, json

app = Flask(__name__)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
      'app_name': "Cleansing API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

class CleanText(Resource):
  def post(self):
    try:
      text = request.form['text']
      processed_text = clean_text(text)
      cleaned_text = clean_text_with_sastrawi(processed_text)
      print(f"Debug CleanText: {cleaned_text}")  # Add debug print
      insert_data(cleaned_text=cleaned_text)
      response = json.dumps('{"cleaned_text":'+ cleaned_text)
      print(f"Debug CleanText Response Type: {type(response)}")  # Ensure it's a proper Response object
      return response, 200
    except Exception as e:
      print(f"Error in CleanText: {e}")
      return json.dumps({'error': str(e)}), 500
  
class UploadCSV(Resource):
  def post(self):
    if 'file' not in request.files:
      return json.dumps({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
      return json.dumps({"error": "No selected file"}), 400
    if file:
      filename = secure_filename(file.filename)
      upload_dir = os.path.join(os.getcwd(), 'uploads')
      download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            
      # Buat direktori 'uploads' jika belum ada
      os.makedirs(upload_dir, exist_ok=True)
            
      file_path = os.path.join(upload_dir, filename)
      file.save(file_path)
      try:
        df = clean_csv(file_path)
        cleaned_file_path = os.path.join(download_dir, f'cleaned_{filename}')

        # Simpan file yang telah dibersihkan ke direktori Downloads
        df.to_csv(cleaned_file_path, index=False)
        insert_data(file_path=cleaned_file_path)

        response = json.dumps({'message': 'File cleaned and saved', 'file_path': cleaned_file_path})
        print(f"Debug UploadCSV Response: {response}")  # Add debug print
        return response, 200
      
      except KeyError as e:
        return json.dumps({'error': str(e)}), 400

api.add_resource(CleanText, '/clean_text')
api.add_resource(UploadCSV, '/upload_csv')

if __name__ == '__main__':
  init_db()
  app.run(debug=True)
