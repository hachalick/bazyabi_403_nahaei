import nltk
import csv
import re
import math
import editdistance

from classes.utils import UtilsIR

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.collocations import BigramCollocationFinder

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


class IRS:
    stemmer = nltk.stem.PorterStemmer()
    __func_utils = UtilsIR()

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
        com_arr = self.read_title_and_plot(arr_deleting_indexes) + arr_adding_indexes
        return com_arr

    def change_list_dict_of_index_to_list_index(self, dict_of_word: dict):
        # chang arr of obj to arr of index
        for i in dict_of_word:
            list_index_title = []
            list_index_plot = []
            if len(dict_of_word[i]["title"]) > 0:
                for j in range(len(dict_of_word[i]["title"])):
                    list_index_title.append(list(dict_of_word[i]["title"][j])[0])
                dict_of_word[i]["title"] = list_index_title
            if len(dict_of_word[i]["plot"]) > 0:
                for j in range(len(dict_of_word[i]["plot"])):
                    list_index_plot.append(list(dict_of_word[i]["plot"][j])[0])
                dict_of_word[i]["plot"] = list_index_plot
            list_all_index = list_index_title + list_index_plot
            list_all_index.sort()
            clear_list_all_index = self.__func_utils.remove_frequency_words_from_list(list_all_index)
            dict_of_word[i] = clear_list_all_index
        return dict_of_word

    def __vb_code(self, list_index: list):
        vb_code = []
        binary_number = self.__func_utils.int_to_binary(list_index[0], 7)
        vb_code.append(self.__func_utils.binary_to_vb_code(binary_number, 7))
        for j in range(len(list_index[1:])):
            index_after = list_index[j + 1]
            index_before = list_index[j]
            binary_number = self.__func_utils.int_to_binary(index_after - index_before, 7)
            vb_code.append(self.__func_utils.binary_to_vb_code(binary_number, 7))
        return "".join(vb_code)

    def vb_code(self, dict_of_word: dict) -> dict:
        dict_of_vb_code_word = {}
        for i in dict_of_word:
            dict_of_vb_code_word[i] = self.__vb_code(dict_of_word[i])
        return dict_of_vb_code_word

    def __g_code(self, number: int):
        if number == 0:
            return "0"
        length_g_code = ""
        number_of_one_length_g_code = int(math.log(number, 2))
        for i in range(number_of_one_length_g_code):
            length_g_code += "1"
        length_g_code += "0"
        binary_number = self.__func_utils.int_to_binary(number)
        offset_g_code = binary_number[1:]
        return length_g_code + offset_g_code

    def g_code(self, dict_of_word: dict) -> dict:
        dict_of_g_code_word = {}
        int(math.log(1, 2))
        for i in dict_of_word:
            g_code = []
            g_code.append(self.__g_code(dict_of_word[i][0]))
            for j in range(len(dict_of_word[i][1:])):
                index_after = dict_of_word[i][j + 1]
                index_before = dict_of_word[i][j]
                g_code.append(self.__g_code(index_after - index_before))
            dict_of_g_code_word[i] = "".join(g_code)
        return dict_of_g_code_word

    def get_query(self):
        text = "grumplyi"
        return text

    def find_bigrams(self, query: str, words: dict):
        tokenize_user_query = self.tokenizer(query)
        dict_word_matching_trigram = {}
        for word in words:
            dict_word_matching_trigram[word] = []
            for word_query in tokenize_user_query:
                for bigrams in self.__func_utils.create_list_bigrams(word_query):
                    if re.match(bigrams, word) is not None:
                        dict_word_matching_trigram[word].append(bigrams[2:4])
        list_word_del = []
        for word in dict_word_matching_trigram:
            if len(dict_word_matching_trigram[word]) == 0:
                list_word_del.append(word)
        for i in list_word_del:
            del dict_word_matching_trigram[i]
        # print(dict_word_matching_trigram)
        dict_rate_matching_trigram = {}
        for i in dict_word_matching_trigram:
            dict_rate_matching_trigram[len(dict_word_matching_trigram[i])] = {}
        for i in dict_word_matching_trigram:
            dict_rate_matching_trigram[len(dict_word_matching_trigram[i])][i] = dict_word_matching_trigram[i]
        list_rate_number = list(dict_rate_matching_trigram)
        list_rate_number.sort(reverse=True)
        list_jaccard_editdistance = []
        for i in list_rate_number:
            for j in dict_rate_matching_trigram[i]:
                bigrams_word = self.__func_utils.create_list_bigrams(j, False)
                bigrams_query = self.__func_utils.create_list_bigrams(query, False)
                eshterak = i
                ejtema = len(self.__func_utils.remove_frequency_words_from_list(bigrams_word + bigrams_query))
                jaccard = int((eshterak/ejtema)*100000)/1000
                editdistance_word = editdistance.eval(query, j)
                list_jaccard_editdistance.append({"word": j, "editdistance": editdistance_word, "jaccard": jaccard})
        sorted_data = sorted(list_jaccard_editdistance, key=lambda x: x['jaccard'], reverse=True)
        list_jaccard_editdistance.sort(key=lambda x: x['jaccard'])
        min_jacard = 40
        list_top_jacard = []
        for i in sorted_data:
            if i['jaccard'] > min_jacard:
                list_top_jacard.append(i)
        sorted_data = sorted(list_top_jacard, key=lambda x: x['editdistance'])
        list_jaccard_editdistance.sort(key=lambda x: x['editdistance'])
        print(sorted_data[0])

    def calculate_tf(self, list_of_words: list):
        dict_of_words = {}
        for i in list_of_words:
            dict_of_words[i] = 0
        for i in list_of_words:
            dict_of_words[i] += 1
        dict_tf = {}
        for i in dict_of_words:
            dict_tf[i] = math.log(dict_of_words[i]) + 1
        return dict_tf

    def calculate_score(self, list_tf: list):
        list_score = []
        for i in list_tf:
            sum = 0
            for j in i["title"]:
                sum += i["title"][j]
            for j in i["plot"]:
                sum += i["plot"][j]
            list_score.append(
                {"id": i["id"], "score": sum,
                 "title": i["title"],
                 "plot": i["plot"]})
        max_score = {"id": -1, "score": 0}
        for i in list_score:
            if i["score"] > max_score["score"]:
                max_score["id"] = i["id"]
                max_score["score"] = i["score"]
        print(max_score)

    def create_list_title(self, query: list, list_dict_title_and_title: list, weight_tf: int = 1):
        print("query: ", query)
        list_tf = []
        for i in list_dict_title_and_title:
            for j in query:
                if j in i["title"]:
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_tf:
            for j in i["title"]:
                i["title"][j] *= weight_tf
        print(list_tf)
        list_score = []
        for i in list_tf:
            sum = 0
            for j in i["title"]:
                sum += i["title"][j]
            for j in i["plot"]:
                sum += i["plot"][j]
            list_score.append(
                {"id": i["id"], "score": sum,
                 "title": i["title"],
                 "plot": i["plot"]})
        max_score = {"id": -1, "score": 0}
        for i in list_score:
            if i["score"] > max_score["score"]:
                max_score["id"] = i["id"]
                max_score["score"] = i["score"]
        print(max_score)

    def create_list_plot(self, query: list, list_dict_title_and_plot: list, weight_tf: int = 1):
        print("query: ", query)
        list_tf = []
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["plot"]:
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_tf:
            for j in i["plot"]:
                i["plot"][j] *= weight_tf
        print(list_tf)
        list_score = []
        for i in list_tf:
            sum = 0
            for j in i["title"]:
                sum += i["title"][j]
            for j in i["plot"]:
                sum += i["plot"][j]
            list_score.append(
                {"id": i["id"], "score": sum,
                 "title": i["title"],
                 "plot": i["plot"]})
        max_score = {"id": -1, "score": 0}
        for i in list_score:
            if i["score"] > max_score["score"]:
                max_score["id"] = i["id"]
                max_score["score"] = i["score"]
        print(max_score)
