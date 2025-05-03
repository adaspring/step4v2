import os
import json
import deepl

def main():
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set.")

    translator = deepl.Translator(auth_key)

    input_file = "translatable.json"
    output_file = "translated.json"
    target_lang = "FR"  # Change this to your preferred language code

    with open(input_file, "r", encoding="utf-8") as f:
        translatable_map = json.load(f)

    translated_map = {}
    for token, text in translatable_map.items():
        try:
            result = translator.translate_text(text, target_lang=target_lang)
            translated_map[token] = result.text
        except Exception as e:
            print(f"Failed to translate token {token}: {e}")
            translated_map[token] = text

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated_map, f, indent=2, ensure_ascii=False)

    print(f"✅ Translation completed: {output_file}")

if __name__ == "__main__":
    main()
