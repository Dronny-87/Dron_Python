import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator


# Перевод через Glosbe
def translate_glosbe(text, from_lang='sr', to_lang='ru'):
    url = f"https://glosbe.com/{from_lang}/{to_lang}/{text}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Поиск всех переводов на странице
        translations = soup.find_all('div', class_='inline leading-10')

        # Используем set для хранения уникальных переводов
        unique_translations = set()

        # Извлечение текста из найденных элементов и фильтрация пустых значений
        for t in translations:
            text = t.get_text(strip=True)
            clean_text = re.sub(r'\s*(noun|pronoun|masculine|feminine|neuter)\s*.*', '', text).strip()
            if clean_text:
                unique_translations.add(clean_text)

        result = list(unique_translations)

        return result if result else ["Перевод не найден (Glosbe)"]
    else:
        return [f"Ошибка: {response.status_code} (Glosbe)"]


# Функция для перевода предложения через Glosbe (слово за словом) с резервом на Google Translate
def translate_sentence_glosbe_with_fallback(text, from_lang='sr', to_lang='ru'):
    words = text.split()
    translations = []
    for word in words:
        # Получаем перевод через Glosbe
        word_translations = translate_glosbe(word, from_lang, to_lang)

        # Если перевод не найден или слишком короткий, используем Google как резерв
        if word_translations[0] == "Перевод не найден (Glosbe)" or len(word_translations[0]) == 0:
            word_translations = translate_google(word, from_lang, to_lang)

        translations.append(word_translations[0])
    return " ".join(translations)


# Перевод через Google Translate
def translate_google(text, from_lang='sr', to_lang='ru'):
    translator = Translator()
    try:
        result = translator.translate(text, src=from_lang, dest=to_lang)
        return [result.text]
    except Exception as e:
        return [f"Ошибка Google Translate: {str(e)}"]


# Основная программа
print('Вас приветствует создатель, ученик Питона, Dronny!!!')
if __name__ == "__main__":
    while True:  # Бесконечный цикл для повторных запросов
        direction = input(
            "Что будешь переводить? (1 - сербский на русский, 2 - русский на сербский, 3 - выход): ")

        if direction == '1':
            serbian_text = input("Приятель, введи текст на сербском языке: ")
            # Перевод через Glosbe с резервом на Google
            translations_glosbe = translate_sentence_glosbe_with_fallback(serbian_text, from_lang='sr', to_lang='ru')
            # Перевод через Google
            translations_google = translate_google(serbian_text, from_lang='sr', to_lang='ru')

        elif direction == '2':
            russian_text = input("Друг, введи текст на русском языке: ")
            # Перевод через Glosbe с резервом на Google
            translations_glosbe = translate_sentence_glosbe_with_fallback(russian_text, from_lang='ru', to_lang='sr')
            # Перевод через Google
            translations_google = translate_google(russian_text, from_lang='ru', to_lang='sr')

        elif direction == '3':
            print("Выход из программы.")
            break  # Выход из цикла
        else:
            print("Неверный выбор. Пожалуйста, попробуй снова.")
            continue  # Продолжить цикл

        # Вывод результатов
        print("Возможные переводы (Glosbe_v2):")
        print(f"- {translations_glosbe}")

        print("Возможные переводы (Google Translate):")
        for translation in translations_google:
            print(f"- {translation}")

    input("Нажмите Enter, чтобы выйти...")  # Ожидаем ввода пользователя перед закрытием
