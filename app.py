from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'd5cf03f598f21b9ae89cd38f1a93226b'

# ดึงข้อมูลสภาพอากาศ
def getWeatherData(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def recommend_crops(humidity, temperature, rain):
    recommendations = []

    # คำแนะนำเกี่ยวกับอุณหภูมิ
    if temperature < 15:
        recommendations.append("อุณหภูมิต่ำเกินไป อาจทำให้พืชบางชนิดไม่เจริญเติบโต เช่น ข้าวโพดและมันสำปะหลัง")
    elif 15 <= temperature <= 25:
        recommendations.append("อุณหภูมิเหมาะสมสำหรับการปลูกพืชหลายชนิด แต่ไม่เหมาะกับพืชที่ชอบอากาศร้อน")
    elif 25 < temperature < 35:
        recommendations.append("อุณหภูมิที่เหมาะสมสำหรับการปลูกพืชเช่น ข้าว")
    else:
        recommendations.append("อุณหภูมิสูงเกินไป อาจทำให้พืชแห้งตายได้")

    # คำแนะนำเกี่ยวกับความชื้น
    if humidity > 70:
        recommendations.append("ความชื้นสูงเหมาะสำหรับการปลูกข้าว แต่ระวังปัญหาการเกิดโรคเชื้อรา")
    elif humidity < 50:
        recommendations.append("ความชื้นต่ำอาจทำให้พืชขาดน้ำ ควรเลือกปลูกพืชที่ทนต่อความแห้งแล้ง เช่น ข้าวโพด")
    else:
        recommendations.append("ความชื้นอยู่ในระดับปานกลาง สามารถปลูกพืชหลายชนิดได้")

    # คำแนะนำเกี่ยวกับปริมาณน้ำฝน
    if rain > 60:
        recommendations.append("ปริมาณน้ำฝนสูง อาจทำให้เกิดน้ำท่วมและส่งผลต่อการปลูกพืช")
    elif rain < 10:
        recommendations.append("ปริมาณน้ำฝนต่ำ อาจทำให้พืชขาดน้ำ ควรหาวิธีการชลประทาน")
    else:
        recommendations.append("ปริมาณน้ำฝนอยู่ในระดับปานกลาง เหมาะสำหรับการปลูกพืชหลายชนิด")

    # แนะนำพืชที่เหมาะสม
    if humidity > 70 and 25 < temperature < 35:
        recommendations.append("แนะนำให้ปลูกข้าว เนื่องจากความชื้นสูงและอุณหภูมิที่เหมาะสม")
    elif humidity < 50 and temperature > 30:
        recommendations.append("แนะนำให้ปลูกข้าวโพด เพราะทนต่อความแห้งแล้งและอุณหภูมิสูง")
    elif humidity >= 50 and (temperature < 25 or temperature > 35):
        recommendations.append("แนะนำให้ปลูกมันสำปะหลัง เนื่องจากสามารถทนต่ออุณหภูมิที่หลากหลายและความชื้นปานกลาง")
    else:
        recommendations.append("สภาพอากาศไม่เหมาะสำหรับการปลูกพืชผลหลัก อาจพิจารณาปลูกพืชอื่น ๆ ที่ทนต่อสภาพนี้ได้")
    return "  ".join(recommendations)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/weather', methods=['GET', 'POST'])
def weatherform():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = getWeatherData(city_name)

        if weather_data['cod'] == 200:
            weather = {
                'city': city_name,
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'wind_speed': weather_data['wind']['speed'],
                'wind_direction': weather_data['wind']['deg'],
                'rain': weather_data.get('rain', {}).get('1h', 0)
            }
            # แนะนำพืชผล
            recommendation = recommend_crops(weather['humidity'], weather['temperature'],weather['rain'])
            return render_template('weather2.html', weather=weather, recommendation=recommendation, city=city_name)
        else:
            # ถ้าหาเมืองไม่เจอ
            error_message = "ไม่พบข้อมูลสภาพอากาศสำหรับเมืองนี้ โปรดตรวจสอบชื่อเมืองและลองใหม่อีกครั้ง!"
            return render_template('weather1.html', error=error_message)
    else:
        return render_template('weather1.html')

if __name__ == '__main__':
    app.run(debug=True)