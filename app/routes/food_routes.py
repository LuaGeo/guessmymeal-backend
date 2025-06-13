# app/routes/food_routes.py
from flask import Blueprint, request, jsonify, send_file
from app.models.food_detector import FoodDetector
from PIL import Image
import io
import base64

food_bp = Blueprint('food', __name__)
detector = FoodDetector()

@food_bp.route('/analyze', methods=['POST'])
def analyze_food():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        # Processar a imagem
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        
        # Detectar alimentos
        annotated_img, results = detector.detect_food(image)
        
        # Converter a imagem anotada para base64
        img_byte_arr = io.BytesIO()
        annotated_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        
        # Preparar lista de alimentos detectados
        detected_foods = []
        if len(results.boxes) > 0:
            for box in results.boxes:
                confidence = box.conf.item()
                class_id = box.cls.item()
                class_name = results.names[int(class_id)]
                detected_foods.append({
                    'name': class_name,
                    'confidence': confidence
                })
        
        return jsonify({
            'success': True,
            'detected_foods': detected_foods,
            'annotated_image': img_base64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500