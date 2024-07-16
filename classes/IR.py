import nltk
import csv
import re
import math
import editdistance

from classes.utils import UtilsIR

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# nltk.download('prunkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


class IRS:
    __stemmer = nltk.stem.PorterStemmer()
    __lemmatizer = nltk.stem.WordNetLemmatizer()
    __func_utils = UtilsIR()
    __number_of_row = -1
    __filename = ""

    def __init__(self, number_of_row: int, filename: str) -> None:
        """
        :param number_of_row: int, number of rows to read from file
        :param filename: str, in main directory
        """
        self.__number_of_row = number_of_row
        self.__filename = filename

    def __detected_word(self, word: str) -> str:
        """
        get any word and detected is noun or verb or adj or adv
        :param word: str
        :return: "a" | "v" | "r" | "n"
        """
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

    def __lemmatize_and_stem_word(self, word: str) -> str:
        """
        get any word and do the lemmatization and stemming on the word
        :param word:str -> "is"
        :return:str -> "be"
        """
        pos_wod = self.__detected_word(word)
        res_word = wn._morphy(word, pos_wod)
        lemNoun = self.__lemmatizer.lemmatize(word, pos=wn.NOUN)
        lemVerb = self.__lemmatizer.lemmatize(word, pos=wn.VERB)
        lemAdj = self.__lemmatizer.lemmatize(word, pos=wn.ADJ)
        lemAdv = self.__lemmatizer.lemmatize(word, pos=wn.ADV)
        lemAdjS = self.__lemmatizer.lemmatize(word, pos=wn.ADJ_SAT)
        if len(res_word) > 0:
            word_lem = res_word.pop()
            if (lemNoun != lemVerb
                    or (lemNoun == lemVerb
                        and lemVerb == lemAdj
                        and lemAdv == lemAdv)
                    and not re.match(""".*le$""", word_lem)):
                return self.__stemmer.stem(word_lem)
            elif word_lem == word and pos_wod == wn.NOUN and re.match(""".*ing$""", word_lem):
                return self.__stemmer.stem(word_lem)
            else:
                return word_lem
        else:
            return word

    def tokenizer(self, text: str) -> list:
        """
        get a text and tokenize it to list of word
        :param text:str -> "Grumpier ..."
        :return:list -> [ word, punctuation, ... ]
        """
        wt = word_tokenize(text)
        for i in range(len(wt)):
            wt[i] = wt[i].casefold()
            wt[i] = re.sub("""â€™s""", "", wt[i])
            wt[i] = re.sub("""â€™""", "", wt[i])
            wt[i] = re.sub("""â€œ""", "", wt[i])
            wt[i] = re.sub("""â€¦""", "", wt[i])
            wt[i] = re.sub("""â€""", "", wt[i])
            wt[i] = re.sub("""أ©""", "", wt[i])
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
            wt[i] = self.__lemmatize_and_stem_word(wt[i])
        return wt

    def clean_word(self, list_of_words: list) -> list:
        """
        get list of words and remove punctuation indexes
        :param list_of_words:list -> [ word, ... ]
        :return:list -> [ word, ... ]
        """
        list_index_delete_from_list_of_word = []
        for i in range(len(list_of_words)):
            match list_of_words[i]:
                case "":
                    list_index_delete_from_list_of_word.append(i)
                case "/":
                    list_index_delete_from_list_of_word.append(i)
                case "\\":
                    list_index_delete_from_list_of_word.append(i)
                case ".":
                    list_index_delete_from_list_of_word.append(i)
                case "..":
                    list_index_delete_from_list_of_word.append(i)
                case "...":
                    list_index_delete_from_list_of_word.append(i)
                case "....":
                    list_index_delete_from_list_of_word.append(i)
                case ",":
                    list_index_delete_from_list_of_word.append(i)
                case ";":
                    list_index_delete_from_list_of_word.append(i)
                case ":":
                    list_index_delete_from_list_of_word.append(i)
                case "?":
                    list_index_delete_from_list_of_word.append(i)
                case "!":
                    list_index_delete_from_list_of_word.append(i)
                case "@":
                    list_index_delete_from_list_of_word.append(i)
                case "$":
                    list_index_delete_from_list_of_word.append(i)
                case "%":
                    list_index_delete_from_list_of_word.append(i)
                case "^":
                    list_index_delete_from_list_of_word.append(i)
                case "&":
                    list_index_delete_from_list_of_word.append(i)
                case "*":
                    list_index_delete_from_list_of_word.append(i)
                case "(":
                    list_index_delete_from_list_of_word.append(i)
                case ")":
                    list_index_delete_from_list_of_word.append(i)
                case "-":
                    list_index_delete_from_list_of_word.append(i)
                case "--":
                    list_index_delete_from_list_of_word.append(i)
                case "_":
                    list_index_delete_from_list_of_word.append(i)
                case "=":
                    list_index_delete_from_list_of_word.append(i)
                case "+":
                    list_index_delete_from_list_of_word.append(i)
                case "#":
                    list_index_delete_from_list_of_word.append(i)
                case '“':
                    list_index_delete_from_list_of_word.append(i)
                case '”':
                    list_index_delete_from_list_of_word.append(i)
                case '``':
                    list_index_delete_from_list_of_word.append(i)
                case "\'":
                    list_index_delete_from_list_of_word.append(i)
                case "\'\'":
                    list_index_delete_from_list_of_word.append(i)
                case "\'\'":
                    list_index_delete_from_list_of_word.append(i)
                case "\'\'":
                    list_index_delete_from_list_of_word.append(i)
        ite = 0
        for i in list_index_delete_from_list_of_word:
            del list_of_words[i - ite]
            ite += 1
        return list_of_words

    def generate_stopwords(self, list_of_words: list) -> dict:
        """
        get list of words and create dictionary of inner words list with frequency
        :param list_of_words:list -> [ word, ... ]
        :return:dict -> { word: frequency, ... }
        """
        list_of_words.sort()
        dic_of_words = {}
        for i in list_of_words:
            dic_of_words[i] = 1 if i not in dic_of_words else dic_of_words[i] + 1
        return dic_of_words

    def sort_dict_token_based_list(self, dict_token: dict, arr_sort: list, limit_show: int = -1) -> dict:
        """
        get dictionary of token - frequency and sorted based list int with optional limit show
        :param dict_token:dict -> { word: { frequency: 0, title: "...", plot: "...", }, ... }
        :param arr_sort:list -> [ high, ..., low ]
        :param limit_show:int -> -1: don't limit
        :return:
        """
        show_dict = {}
        del_dict = {}
        for i in arr_sort:
            for j in dict_token:
                if limit_show < 0 and dict_token[j] == i:
                    show_dict[j] = i
                elif limit_show >= i and dict_token[j] == i:
                    show_dict[j] = i
                elif limit_show < i and dict_token[j] == i:
                    del_dict[j] = i
        return {"deleted": del_dict, "showed": show_dict}

    def read_all_row(self) -> str:
        """
        reading the lines of the filename with the number of entered numbers
        :return: "title1 plot1 title2 plot2 ..."
        "Grumpier Old Man A Family ...."
        """
        text = ""
        with open(self.__filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            ite = 0
            for row in csv_reader:
                if ite > 0:
                    row = row[:-3]
                    text += " ".join(row) + " "
                    if ite == self.__number_of_row + 1:
                        break
                ite = ite + 1
            text = " ".join(text.split("-"))
        return text

    def read_title_and_plot(self, arr_of_exception: list = None) -> list:
        """
        reading the lines of the filename with the number of entered
        :param arr_of_exception: [ row, ... ]
        :return: [ { id: 0, title: "...", plot: "...", }, ... ]
        """
        arr = []
        with open(self.__filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            ite = 0
            if arr_of_exception is None:
                for row in csv_reader:
                    arr.append({"id": ite-1, "title": row[0], "plot": row[1]})
                    if ite == self.__number_of_row:
                        break
                    ite += 1
                arr = arr[1:]
            else:
                for row in csv_reader:
                    if ite-1 not in arr_of_exception or len(arr_of_exception) == 0:
                        arr.append({"id": ite-1, "title": row[0], "plot": row[1]})
                    if ite == self.__number_of_row:
                        break
                    ite += 1
                arr = arr[1:]
            return arr

    def read_row(self, row_id: int) -> dict:
        """
        read row from filename
        :param row_id: int -> 0
        :return: { id: row, title: "...", plot: "...", }
        """
        row_id += 1
        film = {}
        with open(self.__filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            ite = 0
            for row in csv_reader:
                if ite == row_id:
                    film = {"id": ite-1, "title": row[0], "plot": row[1]}
                    break
                ite += 1
        return film

    def tokenize_title_and_plot(self, list_title_and_plot: list) -> list:
        """
        tokenize title and plot on list title and plot
        :param list_title_and_plot:list -> [ { title: "...", plot: "...", }, ... ]
        :return:list -> [ { title: [ token, ... ], plot: [ token, ... ], }, ... ]
        """
        for index in range(len(list_title_and_plot)):
            token_title = self.tokenizer(list_title_and_plot[index]["title"])
            token_title_clean = self.clean_word(token_title)
            list_title_and_plot[index]["title"] = token_title_clean
            token_plot = self.tokenizer(list_title_and_plot[index]["plot"])
            token_plot_clean = self.clean_word(token_plot)
            list_title_and_plot[index]["plot"] = token_plot_clean
        return list_title_and_plot

    def posting_title_and_plot(self, list_dynamic: list) -> dict:
        """
        create posting list from list dict title and plot
        :param list_dynamic: list -> [ { title: "...", plot: "...", } ]
        :return: { word: { frequency: 0,
                           title: [ { index_row: index_word_in_sense, ... }, ... ],
                           plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        """
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

    def merge_title_and_plot_file_user(self):
        """
        get id title plot for add and id for delete and merged on result posting list
        :return:list -> [ { id: 0, title: "...", plot: "..." }, ... ]
        """
        arr_of_indexes = [i for i in range(self.__number_of_row)]
        arr_adding_indexes = []
        arr_deleting_indexes = []
        print("""\033[93mfor ending process positional living type "\033[4mexit()\033[0m\033[93m" and enter\033[0m
                \r\033[95m1. add format:\033[0m
                \rid, title, plot
                \r\033[92m(exam: 1, title test, plot test)\033[0m\n
                \r\033[95m2. delete format:\033[0m
                \rid
                \r\033[92m(exam: 1)\033[0m\n""")
        while True:
            print("list indexes:", arr_of_indexes)
            input_text = self.__func_utils.get_input("str")
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
                            arr_deleting_indexes.append(id_dataset)
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
        self.__func_utils.sort_list_of_dicts(com_arr, "id", False)
        return com_arr

    def change_list_dict_of_index_to_list_index(self, dict_of_word: dict):
        """
        get list of dict to create list of all index without frequency
        :param dict_of_word: dict -> { word: { frequency: 0,
                                       title: [ { index_row: index_word_in_sense, ... }, ... ],
                                       plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :return:list -> { word: [ index, ... ], ... }
        """
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

    def __vb_code(self, list_number: list) -> str:
        """
        calculate vb-code from list_number and return it in string format
        :param list_number: list -> [ number, ... ]
        :return: str -> "vb-code"
        """
        vb_code = []
        binary_number = self.__func_utils.int_to_binary(list_number[0], 7)
        vb_code.append(self.__func_utils.binary_to_vb_code(binary_number, 7))
        for j in range(len(list_number[1:])):
            index_after = list_number[j + 1]
            index_before = list_number[j]
            binary_number = self.__func_utils.int_to_binary(index_after - index_before, 7)
            vb_code.append(self.__func_utils.binary_to_vb_code(binary_number, 7))
        return "".join(vb_code)

    def vb_code(self, dict_of_word: dict) -> dict:
        """
        calculate vb-code from list indexes in dictionary of words and replace it with that list
        :param dict_of_word: dict -> { word: [ number, ... ], ... }
        :return: dict -> { word: "vb-code" , ... }
        """
        dict_of_vb_code_word = {}
        for i in dict_of_word:
            dict_of_vb_code_word[i] = self.__vb_code(dict_of_word[i])
        return dict_of_vb_code_word

    def __g_code(self, number: int) -> str:
        """
        get number and calculate g-code from that number
        :param number: int -> x > 0
        :return: str -> "g-code"
        """
        if number == 0:
            return ""
        length_g_code = ""
        number_of_one_length_g_code = int(math.log(number, 2))
        for i in range(number_of_one_length_g_code):
            length_g_code += "1"
        length_g_code += "0"
        binary_number = self.__func_utils.int_to_binary(number)
        offset_g_code = binary_number[1:]
        return length_g_code + offset_g_code

    def g_code(self, dict_of_word: dict) -> dict:
        """
        calculate g-code from list indexes in dictionary of words and replace it with that list
        :param dict_of_word: dict -> { word: [ number, ... ], ... }
        :return: { word: "g-code" , ... }
        """
        dict_of_g_code_word = {}
        for i in dict_of_word:
            list_g_code = [self.__g_code(dict_of_word[i][0])]
            for j in range(len(dict_of_word[i][1:])):
                index_after = dict_of_word[i][j + 1]
                index_before = dict_of_word[i][j]
                list_g_code.append(self.__g_code(index_after - index_before))
            dict_of_g_code_word[i] = "".join(list_g_code)
        return dict_of_g_code_word

    def find_bigrams(self, tokenize_query: list, dict_of_words: dict):
        """
        get
        :param tokenize_query: list -> [ word, ... ]
        :param dict_of_words:dict -> { word: { frequency: 0,
                                       title: [ { index_row: index_word_in_sense, ... }, ... ],
                                       plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :return: { word: [ bigram match on query, ... ], ... }
        """
        dict_word_matching_bigram = {}
        for word in dict_of_words:
            dict_word_matching_bigram[word] = []
            for word_query in tokenize_query:
                for bigrams in self.__func_utils.create_list_bigrams(word_query):
                    if re.match(bigrams, word) is not None:
                        dict_word_matching_bigram[word].append(bigrams[2:4])
        list_word_del = []
        for word in dict_word_matching_bigram:
            if len(dict_word_matching_bigram[word]) == 0:
                list_word_del.append(word)
        for i in list_word_del:
            del dict_word_matching_bigram[i]
        return dict_word_matching_bigram

    def dict_rating_bigrams(self, dict_of_words: dict):
        dict_rate_matching_bigram = {}
        for i in dict_of_words:
            dict_rate_matching_bigram[len(dict_of_words[i])] = {}
        for i in dict_of_words:
            dict_rate_matching_bigram[len(dict_of_words[i])][i] = dict_of_words[i]
        return dict_rate_matching_bigram

    def jccard_and_editdistance(self, query: str, dict_rate_matching_bigram: dict, min_jacard: float = 0.0):
        """
        calculate jccard and editdistance
        :param query: str -> "..."
        :param dict_rate_matching_bigram:dict -> { word: score, ... }
        :param min_jacard: float -> ignore words if jacard is less than min_jacard
        :return:
        """
        list_rate_number = list(dict_rate_matching_bigram)
        list_rate_number.sort(reverse=True)
        list_jaccard_editdistance = []
        for rate in list_rate_number:
            for j in dict_rate_matching_bigram[rate]:
                bigrams_word = self.__func_utils.create_list_bigrams(j, False)
                bigrams_query = self.__func_utils.create_list_bigrams(query, False)
                eshterak = rate
                ejtema = len(self.__func_utils.remove_frequency_words_from_list(bigrams_word + bigrams_query))
                jaccard = int((int(eshterak)/int(ejtema))*100000)/1000
                editdistance_word = editdistance.eval(query, j)
                list_jaccard_editdistance.append({"word": j, "editdistance": editdistance_word, "jaccard": jaccard})
        sort_list_jaccard_editdistance_base_jaccard = self.__func_utils.sort_list_of_dicts(list_jaccard_editdistance,
                                                                                           "jaccard")
        list_top_jacard = []
        for i in sort_list_jaccard_editdistance_base_jaccard:
            if i['jaccard'] > min_jacard:
                list_top_jacard.append(i)
        sort_list_jaccard_editdistance_base_editdistance = (
            self.__func_utils.sort_list_of_dicts(list_jaccard_editdistance, "editdistance", False))
        if len(sort_list_jaccard_editdistance_base_editdistance):
            return sort_list_jaccard_editdistance_base_editdistance[0]

    def calculate_tf(self, list_of_words: list):
        """
        calculate tf from list of words
        :param list_of_words: [ word, ... ]
        :return:
        """
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
        """
        calculate score from list of words - tf
        :param list_tf:
        :return:
        """
        list_score = []
        for i in list_tf:
            sum_score = 0
            for j in i["title"]:
                sum_score += i["title"][j]
            for j in i["plot"]:
                sum_score += i["plot"][j]
            list_score.append(
                {"id": i["id"], "score": sum_score,
                 "title": i["title"],
                 "plot": i["plot"]})
        sorted_data_base_score = self.__func_utils.sort_list_of_dicts(list_score, "score")
        return sorted_data_base_score

    def create_list_tf_title(self, query: list, list_dict_title_and_plot: list, weight_tf: float = 1.0):
        """
        create list of dict id and tf - title and tf of plot from list of words tokenize query and list of dict id and
        list tokenize title and list tokenize plot on titles and plot
        :param weight_tf: float -> 1.0
        :param query: list[str] -> [ word-tokenize-query, ... ]
        :param list_dict_title_and_plot: list[dict] -> { word: { frequency: 0,
                                                         title: [ { index_row: index_word_in_sense, ... }, ... ],
                                                         plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :return: [ { id: 0,
                     score: 0.0,
                     title: { word: tf, ... },
                     plot : { word: tf, ... }, } ... ]
        """
        list_tf = []
        list_id = []
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["title"] and i["id"] not in list_id:
                    list_id.append(i["id"])
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_tf:
            for j in i["title"]:
                i["title"][j] *= weight_tf
        return list_tf

    def create_list_tf_plot(self, query: list, list_dict_title_and_plot: list, weight_tf: float = 1.0):
        """
        create list of dict id and tf - title and tf of plot from list of words tokenize query and list of dict id and
        list tokenize title and list tokenize plot on plot
        :param weight_tf: float -> 1.0
        :param query: list[str] -> [ word-tokenize-query, ... ]
        :param list_dict_title_and_plot: list[dict] -> { word: { frequency: 0,
                                                         title: [ { index_row: index_word_in_sense, ... }, ... ],
                                                         plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :return: [ { id: 0,
                     score: 0.0,
                     title: { word: tf, ... },
                     plot : { word: tf, ... }, } ... ]
        """
        list_tf = []
        list_id = []
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["plot"] and i["id"] not in list_id:
                    list_id.append(i["id"])
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_tf:
            for j in i["plot"]:
                i["plot"][j] *= weight_tf
        return list_tf

    def create_list_tf_title_and_plot(self, query: list[str], list_dict_title_and_plot: list[dict]):
        """
        create list of dict id and tf - title and tf of plot from list of words tokenize query and list of dict id and
        list tokenize title and list tokenize plot on titles and plot
        :param query: list[str] -> [ word-tokenize-query, ... ]
        :param list_dict_title_and_plot: list[dict] -> { word: { frequency: 0,
                                                         title: [ { index_row: index_word_in_sense, ... }, ... ],
                                                         plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :return: [ { id: 0,
                     score: 0.0,
                     title: { word: tf, ... },
                     plot : { word: tf, ... }, } ... ]
        """
        list_tf = []
        list_id = []
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["title"] and i["id"] not in list_id:
                    list_id.append(i["id"])
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["plot"] and i["id"] not in list_id:
                    list_id.append(i["id"])
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        return list_tf

    def top_high_score(self, dict_score_title, dict_score_plot, limit: int = -1):
        """
        get dictionary of title and score and return top high with limit
        :param dict_score_title: dict ->
        :param dict_score_plot: dict ->
        :param limit: int -> from -1 to up
        :return:
        """
        list_all_score = dict_score_title + dict_score_plot
        sorted_data_base_score = self.__func_utils.sort_list_of_dicts(list_all_score, "score")
        if len(sorted_data_base_score) > limit:
            return sorted_data_base_score[:limit]
        else:
            return sorted_data_base_score

    def find_word_in_row(self, query: str, title_and_plot: dict):
        """
        f
        :param query:str -> "..."
        :param title_and_plot:dict -> { id: 0, title: "...", plot: "...", }
        :return:
        """
        split_query = query.split(" ")
        split_title = title_and_plot["title"].split(" ")
        split_plot = title_and_plot["plot"].split(" ")
        for word in split_query:
            tokenize_word = self.tokenizer(word)
            if len(tokenize_word) == 1:
                self.__find_words_in_list(tokenize_word[0], split_title)
                self.__find_words_in_list(tokenize_word[0], split_plot)
        title_and_plot["title"] = " ".join(split_title)
        title_and_plot["plot"] = " ".join(split_plot)

    def __find_words_in_list(self, word: str, list_doc: list):
        for index_word_text in range(len(list_doc)):
            tokenize_text = self.tokenizer(list_doc[index_word_text])
            cleaned_text = self.clean_word(tokenize_text)
            if len(cleaned_text) == 1:
                if cleaned_text[0] == word:
                    if index_word_text - 1 >= 0 and not re.match("^\033.*", list_doc[index_word_text-1]):
                        list_doc[index_word_text-1] = self.__func_utils.color_text(list_doc[index_word_text-1])
                    if index_word_text + 1 < len(list_doc) and not re.match("^\033.*", list_doc[index_word_text+1]):
                        list_doc[index_word_text+1] = self.__func_utils.color_text(list_doc[index_word_text+1])
                    if index_word_text - 2 >= 0 and not re.match("^\033.*", list_doc[index_word_text-2]):
                        list_doc[index_word_text-2] = self.__func_utils.color_text(list_doc[index_word_text-2])
                    if index_word_text + 2 < len(list_doc) and not re.match("^\033.*", list_doc[index_word_text+2]):
                        list_doc[index_word_text+2] = self.__func_utils.color_text(list_doc[index_word_text+2])
                    list_doc[index_word_text] = self.__func_utils.color_text(list_doc[index_word_text])


