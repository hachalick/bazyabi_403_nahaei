import json


class UtilsIR:
    def save_json_file(self, data):
        with open("result.json", 'w') as file:
            json.dump(data, file)

    def remove_frequency_words_from_list(self, data: list) -> list:
        return list(dict.fromkeys(data))