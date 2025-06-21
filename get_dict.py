import requests
import json
import re

def rename_language(language):
    replacements = {
        "Muduapa": "Vitu",
        # Add more replacements here if needed
    }
    return replacements.get(language, language)

def extract_definition(definition_html):
    match = re.search(r'title="([^"]+)"', definition_html)
    if not match:
        return None
    definition = match.group(1).lower()
    if ':' in definition:
        return None
    if definition == "five":
        return "5"
    if definition == "fifth":
        return "5th"
    return definition

url = "https://en.wiktionary.org/api/rest_v1/page/definition/lima"
response = requests.get(url)
data = response.json()

language_map = {}

for section, entries in data.items():
    for entry in entries:
        language = rename_language(entry["language"])
        entry_definition_htmls = entry.get("definitions", [])
        entry_definitions = {extract_definition(d.get("definition", "")) for d in entry_definition_htmls}
        entry_definitions.discard(None)

        if language not in language_map:
            language_map[language] = {"name": language, "definitions": set()}

        language_map[language]["definitions"].update(entry_definitions)

# Filter languages without "5" and prepare otherMeanings
to_delete = []
for language, entry in language_map.items():
    if "5" not in entry["definitions"]:
        to_delete.append(language)
    else:
        other = sorted(d for d in entry["definitions"] if d != "5")
        if other:
            entry["otherMeanings"] = other
        del entry["definitions"]

for language in to_delete:
    del language_map[language]

result = list(language_map.values())

with open("dict.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    print('wrote dict.json')
