# app/main.py
from flask import Flask, render_template, request, jsonify
import base64
import os

app = Flask(__name__)

# Максимальный размер файла - 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    print("Serving index page")  # Для отладки
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Flask is working!'})

@app.route('/convert', methods=['POST'])
def convert():
    try:
        print("Convert endpoint called")  # Для отладки
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Получаем ширину ASCII из формы (по умолчанию 80)
        cols = int(request.form.get('width', 80))

        # Сохраняем файл временно
        upload_path = "temp_input_image.jpg"
        file.save(upload_path)

        # Запускаем генерацию
        os.system(f"python3 ascii_converter.py {upload_path} {cols}")

        # Читаем сгенерированный фалй в память
        with open("ascii_output.jpg", "rb") as img_file:
            img_bytes = img_file.read()
            b64_data = base64.b64encode(img_bytes).decode('utf-8')
            data_url = f'data:image/jpeg;base64,{b64_data}'

        # Удалим временный файл
        os.remove(upload_path)

        with open("ascii_output.txt", "r", encoding="utf8") as f:
            data_text = f.read()

        return jsonify({
            "ascii_text": f"ACII output for: {file.filename}, width:{cols}\n{data_text}",
            "ascii_image": data_url
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Для отладки
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=80, debug=True)
