from flask import Flask, request, jsonify
from stt import stt
import json
import base64
from wav_convert import convert_m4a_to_base64, audio_score
from neodo import to_llm,to_llm2,topics,generate_script_feedback
import urllib3
import requests
# print(audio_score('C:/Users/user/Downloads/nd/nd/tests/a503.m4a'))
# print(stt())https://neodo-backends3bucket.s3.ap-northeast-2.amazonaws.com/44c9bada-13fa-418d-a6fc-95e39786efc3.m4a


def record_save(record):
    url = record
    a=record.split('/')
    record=a[-1]
    save_path = f'C:/Users/user/Downloads/nd/imgs/{record}'  # 저장할 경로C:\Users\user\Downloads\nd\imgs
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"파일이 {save_path}에 저장되었습니다.")
    else:
        print(f"파일 다운로드에 실패했습니다. 상태 코드: {response.status_code}")
    return save_path


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지
app.url_map.strict_slashes = False
@app.route("/test/") 
def aaaa():
    return "Hello, World!"

@app.route("/", methods=['POST']) 
def hello_world():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        record = data['record']
        atmosphere = data['atmosphere']
        audience = data['audience']
        scale= data['scale']
        purpose= data['purpose']
        deadline= data['deadline']

        record_path = record_save(record)
        originalStt = stt(record_path)
        score = audio_score(record_path)
        conclusion1 = "이번 발표는 주제와 무관한 내용으로 구성되어 있어서 효과 적인 발표로서의 요소가 부족합니다. 발표의 목적과 주제를 명확하게 전달하고자 한다면 해당 내용을 구체적으로 다루는 것이 중요합니다. 발표 내용과 관련하여 아래와 같은 피드백을 제공해 드립 니다.\n\n이 발표는 명확한 주제와 구조가 없으며, 청중에게 유익한 정보나 인사이트를 제공하지 못했습니다. 발표를 효과적으로 전달하기 위해서는 다음과 같은 점을 개선해야 합니다.\n\n1. 발표 의 목적과 주제를 명확히 설정하고 발표의 구조를 구성해야 합니다.\n2. 청중의 관심을 끌 수 있는 흥미로운 내용이나 유용한 정보를 제공해야 합니다.\n3. 발표의 핵심 메시지를 강조하여 청중에게 명확하게 전달해야 합니다.\n\n발표를 보다 효과적으로 전달하기 위해서는 주제와 관련된 적절한 내용을 선정하고, 구조화된 포맷으로 발표의 틀을 잡는 것이 중요합니다. 발표가 청중에게 유익하 고 인상적인 경험이 되도록 노력해 주세요."#to_llm(originalStt, atmosphere, purpose, scale, audience, deadline)
        conclusion = to_llm2(originalStt)
        response = {
            "originalStt" : originalStt,
            "score": score[0],
            "conclusion" : conclusion,
            "topics" : topics(originalStt)
        }
        print(response)
   
        response = json.dumps(response, ensure_ascii=False)
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}

    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON data", "details": str(e)}), 400

@app.route("/coach", methods=['POST']) 
def test_():

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        record = data['record']


        record_path = record_save(record)
        originalStt = stt(record_path)
        score = audio_score(record_path)
        conclusion1 = "이번 발표는 주제와 무관한 내용으로 구성되어 있어서 효과 적인 발표로서의 요소가 부족합니다. 발표의 목적과 주제를 명확하게 전달하고자 한다면 해당 내용을 구체적으로 다루는 것이 중요합니다. 발표 내용과 관련하여 아래와 같은 피드백을 제공해 드립 니다.\n\n이 발표는 명확한 주제와 구조가 없으며, 청중에게 유익한 정보나 인사이트를 제공하지 못했습니다. 발표를 효과적으로 전달하기 위해서는 다음과 같은 점을 개선해야 합니다.\n\n1. 발표 의 목적과 주제를 명확히 설정하고 발표의 구조를 구성해야 합니다.\n2. 청중의 관심을 끌 수 있는 흥미로운 내용이나 유용한 정보를 제공해야 합니다.\n3. 발표의 핵심 메시지를 강조하여 청중에게 명확하게 전달해야 합니다.\n\n발표를 보다 효과적으로 전달하기 위해서는 주제와 관련된 적절한 내용을 선정하고, 구조화된 포맷으로 발표의 틀을 잡는 것이 중요합니다. 발표가 청중에게 유익하 고 인상적인 경험이 되도록 노력해 주세요."#
        conclusion = to_llm2(originalStt)
        response = {
            "originalStt" : originalStt,
            "score": score[0],
            "conclusion" : conclusion
        }
        print(response)
   
        response = json.dumps(response, ensure_ascii=False)
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}

    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON data", "details": str(e)}), 400

@app.route("/script", methods=['POST']) 
def _script():

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        script = data['script']



        script_feedback1 = "이번 발표는 주제와 무관한 내용으로 구성되어 있어서 효과 적인 발표로서의 요소가 부족합니다. 발표의 목적과 주제를 명확하게 전달하고자 한다면 해당 내용을 구체적으로 다루는 것이 중요합니다. 발표 내용과 관련하여 아래와 같은 피드백을 제공해 드립 니다.\n\n이 발표는 명확한 주제와 구조가 없으며, 청중에게 유익한 정보나 인사이트를 제공하지 못했습니다. 발표를 효과적으로 전달하기 위해서는 다음과 같은 점을 개선해야 합니다.\n\n1. 발표 의 목적과 주제를 명확히 설정하고 발표의 구조를 구성해야 합니다.\n2. 청중의 관심을 끌 수 있는 흥미로운 내용이나 유용한 정보를 제공해야 합니다.\n3. 발표의 핵심 메시지를 강조하여 청중에게 명확하게 전달해야 합니다.\n\n발표를 보다 효과적으로 전달하기 위해서는 주제와 관련된 적절한 내용을 선정하고, 구조화된 포맷으로 발표의 틀을 잡는 것이 중요합니다. 발표가 청중에게 유익하 고 인상적인 경험이 되도록 노력해 주세요."#
        script_feedback = generate_script_feedback(script)
        response = {
            "feedback" : script_feedback
        }
        print(response)
   
        response = json.dumps(response, ensure_ascii=False)
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}

    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON data", "details": str(e)}), 400

@app.route("/script/edit", methods=['POST']) 
def _rescript():

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        script = data['script']
        edited_script = data['edited_script']
        script_feedback =data['script_feedback']





        script_feedback1 = "이번 발표는 주제와 무관한 내용으로 구성되어 있어서 효과 적인 발표로서의 요소가 부족합니다. 발표의 목적과 주제를 명확하게 전달하고자 한다면 해당 내용을 구체적으로 다루는 것이 중요합니다. 발표 내용과 관련하여 아래와 같은 피드백을 제공해 드립 니다.\n\n이 발표는 명확한 주제와 구조가 없으며, 청중에게 유익한 정보나 인사이트를 제공하지 못했습니다. 발표를 효과적으로 전달하기 위해서는 다음과 같은 점을 개선해야 합니다.\n\n1. 발표 의 목적과 주제를 명확히 설정하고 발표의 구조를 구성해야 합니다.\n2. 청중의 관심을 끌 수 있는 흥미로운 내용이나 유용한 정보를 제공해야 합니다.\n3. 발표의 핵심 메시지를 강조하여 청중에게 명확하게 전달해야 합니다.\n\n발표를 보다 효과적으로 전달하기 위해서는 주제와 관련된 적절한 내용을 선정하고, 구조화된 포맷으로 발표의 틀을 잡는 것이 중요합니다. 발표가 청중에게 유익하 고 인상적인 경험이 되도록 노력해 주세요."#
        edited_script_feedback = edited_script_feedback(script,script_feedback, edited_script)
        response = {
            "feedback" : edited_script_feedback
        }
        print(response)
   
        response = json.dumps(response, ensure_ascii=False)
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}

    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON data", "details": str(e)}), 400





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)