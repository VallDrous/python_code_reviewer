from google import genai
from google.genai import types, errors
from reviewer.schemas import CodeReview

def analize_code(user_api_key, files_code):
    system_prompt = """
    Ти досвідчений Senior Python Developer з 10-річним стажем. 
    Твоє завдання: проводити Code Review.
    1. Перевіряй відповідність PEP 8.
    2. Шукай вразливості (SQL injections, unsafe eval, insecure secrets).
    3. Пропонуй рефакторинг для покращення Time Complexity та Readable Code.
    Будь лаконічним, критичним, але конструктивним. Відповідай українською мовою.
    """
    try:
        client = genai.Client(api_key=user_api_key)
        response = client.models.generate_content(model='gemini-2.5-flash', config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                response_schema=CodeReview,
                response_mime_type="application/json"
            ), contents=files_code)
        if response.parsed is None:
            return {'result': "Помилка: Модель не змогла згенерувати структуровану відповідь.", 'is_error': True}
        
        return {'result' : response.parsed, 'is_error' : False}
    except errors.ClientError as e:
        if "429" in str(e):
            return {'result' : "Помилка: Вичерпано ліміт запитів (Resource Exhausted). Спробуйте пізніше.", 'is_error' : True}
        elif "400" in str(e):
            return {'result' : "Помилка: Неправильний API-ключ або некоректний формат даних (InvalidArgument).", 'is_error' : True}
        else:
            return {'result' : f"Виникла помилка клієнта: {e}", 'is_error' : True}

    except errors.ServerError as e:
        return {'result' : "Помилка сервера Google: Сервіс тимчасово недоступний. Спробуйте через кілька хвилин.", 'is_error' : True}

    except Exception as e:
        return {'result' : f"Сталася невідома помилка: {str(e)}", 'is_error' : True}