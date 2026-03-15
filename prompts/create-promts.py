import mlflow

# 1. Адрес  MLflow сервера
mlflow.set_tracking_uri("http://localhost:5001")

# 2. Определим имя для нашего "сборника" промптов (можете придумать свое)
#    Оно будет отображаться в интерфейсе MLflow.
prompt_collection_name = "my_homework_prompts"

print(f"Регистрируем промпты в коллекции: {prompt_collection_name}")

# --- ПРОМПТ ВЕРСИЯ 1 ---
prompt_v1 = mlflow.genai.register_prompt(
    name=prompt_collection_name,
    template="Переведи следующий текст на английский язык: {{text_to_translate}}",
    commit_message="Начальная версия промпта для перевода",
    tags={"task": "translation", "language_pair": "ru-en", "version": "1.0"}
)
print(f"Создана версия {prompt_v1.version}")

# --- ПРОМПТ ВЕРСИЯ 2 (Улучшенная) ---
prompt_v2 = mlflow.genai.register_prompt(
    name=prompt_collection_name,
    template="""Ты — профессиональный переводчик. Переведи следующий текст с русского на английский.
Сохрани стиль и тон оригинала. Текст для перевода: '{{text_to_translate}}'""",
    commit_message="Улучшенная версия: добавлен контекст для лучшего качества перевода",
    tags={"task": "translation", "language_pair": "ru-en", "version": "2.0", "status": "improved"}
)
print(f"Создана версия {prompt_v2.version}")

# --- ПРОМПТ ВЕРСИЯ 3 (Для другой задачи) ---
prompt_v3 = mlflow.genai.register_prompt(
    name=prompt_collection_name,
    template="""Напиши краткое содержание следующего текста в {sentence_count} предложениях:
---
{{text_to_summarize}}
---""",
    commit_message="Добавлен промпт для саммаризации текста",
    tags={"task": "summarization", "version": "1.0"}
)
print(f"Создана версия {prompt_v3.version}")

print("Готово! Проверьте результат в веб-интерфейсе MLflow.")