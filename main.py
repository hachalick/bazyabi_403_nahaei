import nltk
import csv
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


class Main:
    def __init__(self, number_of_row):
        self.number_of_row = number_of_row

    def detected_word(self, word: str) -> str:
        empty_list = [word]
        ans = nltk.pos_tag(empty_list, lang='eng')
        val: str = ans[0][1]
        if val.startswith("V"):
            return wn.VERB
        elif val.startswith("R"):
            return wn.ADV
        elif val.startswith("J"):
            return wn.ADJ
        else:
            return wn.NOUN

    def tokenizer(self, main_text: str) -> list:
        wt = word_tokenize(main_text)
        for i in range(len(wt)):
            wt[i] = wt[i].casefold()
            wt[i] = re.sub("""â€™s""", "", wt[i])
            wt[i] = re.sub("""â€™""", "", wt[i])
            wt[i] = re.sub("""â€œ""", "", wt[i])
            wt[i] = re.sub("""â€¦""", "", wt[i])
            wt[i] = re.sub("""â€""", "", wt[i])
            wt[i] = re.sub("""\\.$""", "", wt[i])
            match wt[i]:
                case "n't":
                    wt[i] = "not"
                case "'ll":
                    wt[i] = "will"
                case "'s":
                    wt[i] = "is"
                case "'ve":
                    wt[i] = "have"
                case "'re":
                    wt[i] = "are"
            if wt[i].startswith("'") and wt[i][1:].isalnum():
                wt[i] = wt[i][1:]
            res_word = wn._morphy(wt[i], self.detected_word(wt[i]))
            if len(res_word) > 0:
                wt[i] = res_word.pop()
            lemmatizer = nltk.stem.WordNetLemmatizer()
            # lemNoun = lemmatizer.lemmatize(wt[i], pos=wn.NOUN)
            # lemVerb = lemmatizer.lemmatize(wt[i], pos=wn.VERB)
            # lemAdj = lemmatizer.lemmatize(wt[i], pos=wn.ADJ)
            # lemAdv = lemmatizer.lemmatize(wt[i], pos=wn.ADV)
            # lemAdjS = lemmatizer.lemmatize(wt[i], pos=wn.ADJ_SAT)
        return wt

    def clean_word(self, arr: list) -> list:
        arr_delete = []
        for i in range(len(arr)):
            match arr[i]:
                case "":
                    arr_delete.append(i)
                case "/":
                    arr_delete.append(i)
                case "\\":
                    arr_delete.append(i)
                case ".":
                    arr_delete.append(i)
                case "..":
                    arr_delete.append(i)
                case "...":
                    arr_delete.append(i)
                case "....":
                    arr_delete.append(i)
                case ",":
                    arr_delete.append(i)
                case ";":
                    arr_delete.append(i)
                case ":":
                    arr_delete.append(i)
                case "?":
                    arr_delete.append(i)
                case "!":
                    arr_delete.append(i)
                case "@":
                    arr_delete.append(i)
                case "$":
                    arr_delete.append(i)
                case "%":
                    arr_delete.append(i)
                case "^":
                    arr_delete.append(i)
                case "&":
                    arr_delete.append(i)
                case "*":
                    arr_delete.append(i)
                case "(":
                    arr_delete.append(i)
                case ")":
                    arr_delete.append(i)
                case "-":
                    arr_delete.append(i)
                case "--":
                    arr_delete.append(i)
                case "_":
                    arr_delete.append(i)
                case "=":
                    arr_delete.append(i)
                case "+":
                    arr_delete.append(i)
                case "#":
                    arr_delete.append(i)
                case '“':
                    arr_delete.append(i)
                case '”':
                    arr_delete.append(i)
                case '``':
                    arr_delete.append(i)
                case "\'":
                    arr_delete.append(i)
                case "\'\'":
                    arr_delete.append(i)
                case "\'\'":
                    arr_delete.append(i)
                case "\'\'":
                    arr_delete.append(i)
        iter = 0
        for i in arr_delete:
            del arr[i - iter]
            iter += 1
        return arr

    def generate_stopwords(self, arr_worlds: list):
        arr_worlds.sort()
        dic = {}
        for i in arr_worlds:
            if i not in dic:
                dic[i] = 1
            else:
                dic[i] = dic[i] + 1
        return dic

    def add_value_to_list(self, dict_token: dict) -> list:
        new_list = []
        for i in dict_token:
            new_list.append(dict_token[i])
        new_list = list(dict.fromkeys(new_list))
        new_list.sort(reverse=True)
        return new_list

    def sort_dict(self, dict_token_no_sort: dict, arr_sort: list, out_of: int = -1) -> dict:
        new_dict = {}
        for i in arr_sort:
            for j in dict_token_no_sort:
                if out_of < 0 and dict_token_no_sort[j] == i:
                    new_dict[j] = i
                elif out_of >= i and dict_token_no_sort[j] == i:
                    new_dict[j] = i
        return new_dict

    def read_all_row(self) -> str:
        text = ""
        with open('train.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            iter = 0
            for row in csv_reader:
                text += " ".join(row) + " "
                if iter == self.number_of_row:
                    break
                iter = iter + 1
            text = " ".join(text.split("-"))
        return text

    def read_title_and_plot(self) -> list:
        arr = []
        with open('train.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            iter = 0
            for row in csv_reader:
                arr.append({"title": row[0], "plot": row[1]})
                if iter == self.number_of_row:
                    break
                iter += 1
        return arr[1:]

    def tokenize_title_and_plot(self, list_dynamic: list) -> list:
        for i in range(len(list_dynamic)):
            token_title = self.tokenizer(list_dynamic[i]["title"])
            token_title_clean = self.clean_word(token_title)
            list_dynamic[i]["title"] = token_title_clean
            token_plot = self.tokenizer(list_dynamic[i]["plot"])
            token_plot_clean = self.clean_word(token_plot)
            list_dynamic[i]["plot"] = token_plot_clean
        return list_dynamic

    def posting_title_and_plot(self, list_dynamic: list) -> dict:
        all_list_title = []
        all_list_plot = []
        for i in range(len(list_dynamic)):
            all_list_title = all_list_title + list_dynamic[i]["title"]
        for i in range(len(list_dynamic)):
            all_list_plot = all_list_plot + list_dynamic[i]["plot"]
        all_list_title = list(dict.fromkeys(all_list_title))
        all_list_plot = list(dict.fromkeys(all_list_plot))
        all_list_title.sort()
        all_list_plot.sort()
        all_list_words = all_list_plot + all_list_title
        all_list_words = list(dict.fromkeys(all_list_words))
        all_dict_words = {}
        for i in all_list_words:
            all_dict_words[i] = {"frequency": 0, "title": [], "plot": []}
        for i in range(len(list_dynamic)):
            for j in range(len(list_dynamic[i]["title"])):
                all_dict_words[list_dynamic[i]["title"][j]]["title"].append({i: j})
        for i in range(len(list_dynamic)):
            for j in range(len(list_dynamic[i]["plot"])):
                all_dict_words[list_dynamic[i]["plot"][j]]["plot"].append({i: j})
        for i in all_dict_words:
            all_dict_words[i]["frequency"] = len(all_dict_words[i]["title"]) + len(all_dict_words[i]["plot"])
        return all_dict_words


mainM = Main(3)
text_all_file = mainM.read_all_row()
list_token = mainM.tokenizer(text_all_file)
list_clean_token = mainM.clean_word(list_token)
print("answer 1:\n", list_clean_token, "\n")
dict_token = mainM.generate_stopwords(list_clean_token)
list_rank = mainM.add_value_to_list(dict_token)
sorted_dict = mainM.sort_dict(dict_token, list_rank, 55)
print("answer 2:\n", sorted_dict, "\n")
text_title_and_plot = mainM.read_title_and_plot()
list_tokenize_title_and_plot = mainM.tokenize_title_and_plot(text_title_and_plot)
posting_title_and_plot = mainM.posting_title_and_plot(list_tokenize_title_and_plot)
print("answer 3:\n", posting_title_and_plot, "\n")
