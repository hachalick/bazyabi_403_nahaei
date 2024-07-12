from classes.IR import IRS
from classes.utils import UtilsIR


class Answer:
    __ir_system = None
    __func_utils = UtilsIR()

    def __init__(self, number_of_row=-1):
        self.__ir_system = IRS(number_of_row)

    def q1(self):
        text_all_file = self.__ir_system.read_all_row()
        list_token = self.__ir_system.tokenizer(text_all_file)
        list_clean_token = self.__ir_system.clean_word(list_token)
        self.__func_utils.save_json_file(list_clean_token, "answer1")
        text_question = """\033[94mاین تابع یک متن انگلیسی ورودی گرفته و توکنهای مربوط به آنرا در قالب یک لیست خروجی میدهد
        \rلیست خروجی شامل تعدادی توکن است که عملیات folding case ، stemming و lemmatization روی آنها اجرا شده است. در ضمن عالئم نگارشی نباید به عنوان توکن در نظر گرفته شود"""
        print(text_question)
        print("\033[95manswer 1:\033[0m\n", list_clean_token, "\n")

    def q2(self, out_of: int = -1):
        text_all_file = self.__ir_system.read_all_row()
        list_token = self.__ir_system.tokenizer(text_all_file)
        list_clean_token = self.__ir_system.clean_word(list_token)
        dict_token = self.__ir_system.generate_stopwords(list_clean_token)
        list_rank = self.__ir_system.add_value_to_list(dict_token)
        sorted_dict = self.__ir_system.sort_dict(dict_token, list_rank, out_of)
        self.__func_utils.save_json_file(sorted_dict, "answer2")
        text_question = """\033[94mاین بخش باید توسط خودتان و بدون استفاده از کد آماده پیادهسازی شود
        \rterm های موجود در مجموعه دادگان را بر اساس تکرار آنها مرتب کرده و پرتکرارترین آنها را به عنوان words-stop در نظر بگیرید\033[0m"""
        print(text_question)
        print("\033[95manswer 2:\033[0m\n", sorted_dict, "\n")

    def q3(self):
        text_title_and_plot = self.__ir_system.read_title_and_plot()
        list_tokenize_title_and_plot = self.__ir_system.tokenize_title_and_plot(text_title_and_plot)
        posting_title_and_plot = self.__ir_system.posting_title_and_plot(list_tokenize_title_and_plot)
        self.__func_utils.save_json_file(posting_title_and_plot, "answer3")
        text_question = """\033[94mبرای هر term باید مشخص باشد که آن term در عنوان چه فیلمهایی و در چه جایگاهی از عنوان هر فیلم قرار گرفته است
        \rهمچنین برای هر term باید مشخص باشد که آن term در طرح داستان چه فیلمهایی و در چه جایگاهی از طرح داستان هر فیلم قرار گرفته است\033[0m"""
        print(text_question)
        print("\033[95manswer 3:\033[0m\n", posting_title_and_plot, "\n")

    def q4(self):
        text_title_and_plot_with_change = self.__ir_system.edit_read_title_and_plot()
        list_tokenize_title_and_plot_with_change = self.__ir_system.tokenize_title_and_plot(text_title_and_plot_with_change)
        posting_title_and_plot_with_change = self.__ir_system.posting_title_and_plot(list_tokenize_title_and_plot_with_change)
        self.__func_utils.save_json_file(posting_title_and_plot_with_change, "answer4")
        text_question = """\033[94mنمایه ایجاد شده باید قابلیت حذف و اضافه تک سند را داشته باشد
        \rبرای اضافه شدن سند، یک رشته داده میشود که اطالعات مربوط به سند شامل id و plot و title در آن با کاما جدا شده است. برای حذف سند نیز id آن داده میشود"""
        print(text_question)
        print("\033[95manswer 4:\033[0m\n", posting_title_and_plot_with_change, "\n")

    def q5(self):
        text_title_and_plot = self.__ir_system.read_title_and_plot()
        list_tokenize_title_and_plot = self.__ir_system.tokenize_title_and_plot(text_title_and_plot)
        posting_title_and_plot = self.__ir_system.posting_title_and_plot(list_tokenize_title_and_plot)
        dict_list_index = self.__ir_system.change_list_dict_of_index_to_list_index(posting_title_and_plot)
        vb_code = self.__ir_system.vb_code(dict_list_index)
        g_code = self.__ir_system.g_code(dict_list_index)
        self.__func_utils.save_json_file(dict_list_index, "answer5.1")
        self.__func_utils.save_json_file(vb_code, "answer5.2")
        self.__func_utils.save_json_file(g_code, "answer5.3")
        text_question = """\033[94mذخیرهسازی به ۳ روش صورت میگیرد
        \rبدون فشردهسازی - فشردهسازی از روش code-gam - فشردهسازی از روش .byte-varia"""
        print(text_question)
        print("\033[95manswer 5.1 (without):\033[0m\n", dict_list_index, "\n")
        print("\033[95manswer 5.2 (vb code):\033[0m\n", vb_code, "\n")
        print("\033[95manswer 5.3 (g code):\033[0m\n", g_code, "\n")

    def q6(self):
        text_title_and_plot = self.__ir_system.read_title_and_plot()
        list_tokenize_title_and_plot = self.__ir_system.tokenize_title_and_plot(text_title_and_plot)
        posting_title_and_plot = self.__ir_system.posting_title_and_plot(list_tokenize_title_and_plot)
        user_query = self.__ir_system.get_query()
        self.__ir_system.find_bigrams(user_query, posting_title_and_plot)

    def q7(self):
        text_title_and_plot = self.__ir_system.read_title_and_plot()
        list_tokenize_title_and_plot = self.__ir_system.tokenize_title_and_plot(text_title_and_plot)
        query_title = "casino heat babe the a"
        query_title_tokenized_plot = self.__ir_system.tokenizer(query_title)
        list_title_tf = self.__ir_system.create_list_title(query_title_tokenized_plot, list_tokenize_title_and_plot)
        dict_score_title_tf = self.__ir_system.calculate_score(list_title_tf)
        query_plot = "family"
        query_plot_tokenized_plot = self.__ir_system.tokenizer(query_plot)
        list_plot_tf = self.__ir_system.create_list_plot(query_plot_tokenized_plot, list_tokenize_title_and_plot)
        dict_score_plot_tf = self.__ir_system.calculate_score(list_plot_tf)
        comparison_high_score = self.__ir_system.comparison_high_score(dict_score_title_tf, dict_score_plot_tf)
        print(comparison_high_score)
