import nltk
import csv
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


class IRS:
    stemmer = nltk.stem.PorterStemmer()

    def __init__(self, number_of_row):
        self.number_of_row = number_of_row

    def __detected_word(self, word: str) -> str:
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

    def __lemmatization_word(self, word: str) -> str:
        pos_wod = self.__detected_word(word)
        res_word = wn._morphy(word, pos_wod)
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemNoun = lemmatizer.lemmatize(word, pos=wn.NOUN)
        lemVerb = lemmatizer.lemmatize(word, pos=wn.VERB)
        lemAdj = lemmatizer.lemmatize(word, pos=wn.ADJ)
        lemAdv = lemmatizer.lemmatize(word, pos=wn.ADV)
        lemAdjS = lemmatizer.lemmatize(word, pos=wn.ADJ_SAT)
        if len(res_word) > 0:
            word_lem = res_word.pop()
            # print(f"{pos_wod}\nw {word}\n{wn.NOUN} {lemNoun}\n{wn.VERB} {lemVerb}\n{wn.ADJ} {lemAdj}\n{wn.ADV} {lemAdv}\n{wn.ADJ_SAT} {lemAdjS}\n")
            if (lemNoun != lemVerb
                    or (lemNoun == lemVerb
                        and lemVerb == lemAdj
                        and lemAdv == lemAdv)
                    and not re.match(""".*le$""", word_lem)):
                return self.stemmer.stem(word_lem)
            elif word_lem == word and pos_wod == wn.NOUN and re.match(""".*ing$""", word_lem):
                return self.stemmer.stem(word_lem)
            else:
                return word_lem
        else:
            return word

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
            wt[i] = re.sub("""^\\.""", "", wt[i])
            wt[i] = re.sub("""/$""", "", wt[i])
            wt[i] = re.sub("""^/""", "", wt[i])
            wt[i] = re.sub("""-$""", "", wt[i])
            wt[i] = re.sub("""^-""", "", wt[i])
            wt[i] = re.sub("""_$""", "", wt[i])
            wt[i] = re.sub("""^_""", "", wt[i])
            wt[i] = re.sub("""/$""", "", wt[i])
            wt[i] = re.sub("""^/""", "", wt[i])
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
            wt[i] = self.__lemmatization_word(wt[i])
        wt.sort()
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
        ite = 0
        for i in arr_delete:
            del arr[i - ite]
            ite += 1
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
            ite = 0
            for row in csv_reader:
                # jump from row with index 0 (name of column)
                if ite > 0:
                    # remove rate and popularity so worked with title and plot
                    row = row[:-3]
                    # join name and plot in one string
                    text += " ".join(row) + " "
                    # exit loop when ...
                    if ite == self.number_of_row + 1:
                        break
                ite = ite + 1
            text = " ".join(text.split("-"))
        return text

    def read_title_and_plot(self, arr_of_exception: list = None) -> list:
        arr = []
        with open('train.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            ite = 0
            if arr_of_exception is None:
                for row in csv_reader:
                    arr.append({"id": ite-1, "title": row[0], "plot": row[1]})
                    if ite == self.number_of_row:
                        break
                    ite += 1
                arr = arr[1:]
            else:
                for row in csv_reader:
                    if ite-1 not in arr_of_exception or len(arr_of_exception) == 0:
                        arr.append({"id": ite-1, "title": row[0], "plot": row[1]})
                    if ite == self.number_of_row:
                        break
                    ite += 1
                arr = arr[1:]
            return arr

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
        all_list_words.sort()
        all_dict_words = {}
        for i in all_list_words:
            all_dict_words[i] = {"frequency": 0, "title": [], "plot": []}
        for i in range(len(list_dynamic)):
            for j in range(len(list_dynamic[i]["title"])):
                all_dict_words[list_dynamic[i]["title"][j]]["title"].append({list_dynamic[i]["id"]: j})
        for i in range(len(list_dynamic)):
            for j in range(len(list_dynamic[i]["plot"])):
                all_dict_words[list_dynamic[i]["plot"][j]]["plot"].append({list_dynamic[i]["id"]: j})
        for i in all_dict_words:
            all_dict_words[i]["frequency"] = len(all_dict_words[i]["title"]) + len(all_dict_words[i]["plot"])
        return all_dict_words

    def edit_read_title_and_plot(self):
        arr_of_indexes = [i for i in range(self.number_of_row)]
        arr_adding_indexes = []
        arr_deleting_indexes = []
        print("""\033[93mfor ending process positional living type "\033[4mexit()\033[0m\033[93m" and enter\033[0m
                \r\033[95m1. add format:\033[0m
                \rid, title, plot
                \r\033[92m(exam:1, dars bazyabi etelaat, darsi shirin ke imani mehr tadris karde)\033[0m\n
                \r\033[95m2. delete format:\033[0m
                \rid
                \r\033[92m(exam:1)\033[0m\n""")
        while True:
            print(arr_of_indexes)
            input_text = input("enter => ")
            print("\033[93m#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#\033[0m")
            if input_text == "exit()":
                print("\033[91mprocess positional ended\033[0m")
                break
            text_list = input_text.split(',')
            # print(text_list)
            if not (len(text_list) == 3 or len(text_list) == 1):
                print("\033[91mformat input not correct\033[0m")
            for i in range(len(text_list)):
                text_list[i] = text_list[i].strip()
            try:
                int(text_list[0])
            except ValueError:
                print("\033[91mid should be integer\033[0m")
                continue
            id_dataset = int(text_list[0])
            if len(text_list) == 1:
                if id_dataset in arr_of_indexes:
                    for i in range(len(arr_of_indexes)):
                        if arr_of_indexes[i] == id_dataset:
                            del arr_of_indexes[i]
                            arr_deleting_indexes.append(i)
                            print("deleted", i)
                            break
                else:
                    print("not delete")
            elif len(text_list) == 3:
                if id_dataset not in arr_of_indexes:
                    title_dataset = text_list[1]
                    plot_title = text_list[2]
                    arr_of_indexes.append(id_dataset)
                    arr_of_indexes.sort()
                    arr_adding_indexes.append({"id": id_dataset, "title": title_dataset, "plot": plot_title})
                    print("add: id =", id_dataset, " title =", title_dataset, " plot =", plot_title)
                else:
                    print("not add")
        for i in range(len(arr_adding_indexes)):
            for j in range(len(arr_deleting_indexes)):
                if arr_adding_indexes[i]["id"] == arr_deleting_indexes[j]:
                    del arr_adding_indexes[i]
                    del arr_deleting_indexes[j]
        com_arr = self.read_title_and_plot(arr_deleting_indexes) + arr_adding_indexes
        return com_arr

