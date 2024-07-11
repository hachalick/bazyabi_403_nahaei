import json


class UtilsIR:
    def save_json_file(self, data: list | dict, name_file: str = "result"):
        with open(f"{name_file}.json", 'w') as file:
            json.dump(data, file)

    def remove_frequency_words_from_list(self, data: list) -> list:
        return list(dict.fromkeys(data))

    def int_to_binary(self, number: int, bite: int = 0) -> str:
        if bite == 0:
            return bin(number)[2:]
        else:
            count = int(len(bin(number)[2:])/bite)+1
            return bin(number)[2:].zfill(bite * count)

    def binary_to_int(self, number: str) -> int:
        return int(number, 2)

    def binary_to_vb_code(self, number: str, bite: int) -> str:
        vb_code = []
        length_number = len(number)
        for i in range(int(length_number/bite)):
            if (i + 1) * bite == length_number:
                vb_code.append("1")
            else:
                vb_code.append("0")
            vb_code.append(number[i*bite:(i+1)*bite])
        return "".join(vb_code)

    def create_list_bigrams(self, word: str, return_reg: bool = True) -> list :
        list_k_gram = []
        word = word.lower()
        for i in range(len(word) - 1):
            if return_reg:
                list_k_gram.append(".*"+word[i:i+2]+".*")
            else:
                list_k_gram.append(word[i:i+2])
        return list_k_gram


