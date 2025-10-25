import base64
import os
from flask import Flask, render_template, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Максимальный размер файла - 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Prometheus метрики
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])
CONVERSION_COUNT = Counter('app_conversions_total', 'Total image conversions')
CONVERSION_ERRORS = Counter('app_conversion_errors_total', 'Total conversion errors')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Считаем латенси запросов
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    
    # Считаем общее количество запросов
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    
    return response

@app.route('/')
def index():
    print("Serving index page")  # Для отладки
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Flask is working!'})

@app.route('/metrics')
def metrics():
    """Эндпоинт для сбора метрик Prometheus"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

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

        # Читаем сгенерированный файл в память
        with open("ascii_output.jpg", "rb") as img_file:
            img_bytes = img_file.read()
            b64_data = base64.b64encode(img_bytes).decode('utf-8')
            data_url = f'data:image/jpeg;base64,{b64_data}'

        # Удаляем временный файл
        os.remove(upload_path)

        with open("ascii_output.txt", "r", encoding="utf8") as f:
            data_text = f.read()

        # Увеличиваем счетчик успешных конвертаций
        CONVERSION_COUNT.inc()

        return jsonify({
            "ascii_text": f"ASCII output for: {file.filename}, width:{cols}\n{data_text}",
            "ascii_image": data_url
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # Для отладки
        # Увеличиваем счетчик ошибок
        CONVERSION_ERRORS.inc()
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/health')
def health():
    """Эндпоинт для проверки здоровья приложения"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=80, debug=False)  # debug=False для продакшена
