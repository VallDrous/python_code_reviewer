**Python code Reviewer**
    Інструмент для автоматичного аналізу Python-коду за допомогою LLM.

    Технологічний стек

    Backend: google.genai, pydantic.
    Frontend: Streamlit.
    Менеджер пакетів: uv.

Встановлення та запуск
1. **Клонуйте репозиторій:**
    ```bash
    git clone https://github.com/VallDrous/LLM.git
    cd python_code_reviewer
    ```
2. **Встановіть залежності:**

    uv sync

3. **Запустіть додаток:**

    uv run streamlit run src/reviewer/client_part.py

Функціонал

Бот вміє:
* Аналіз відповідності стандарту PEP 8.
* Пошук вразливостей у коді (Security check).
* Поради щодо рефакторингу та оптимізації складності.
* Оцінювання коду за 10-бальною шкалою.