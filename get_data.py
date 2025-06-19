import requests

url = "https://en.wiktionary.org/api/rest_v1/page/definition/lima"
response = requests.get(url)
data = response.json()

languages_with_lima_as_five = []

for lang_code, entries in data.items():
    for entry in entries:
        definitions = entry.get("definitions", [])
        for d in definitions:
            if '/wiki/five' in d.get("definition", "").lower():
                languages_with_lima_as_five.append(entry["language"])
                break

print(languages_with_lima_as_five)
print(len(languages_with_lima_as_five))
