from classes.IR import IRS

number_of_row = 3
ir_system = IRS(number_of_row)
# text_all_file = ir_system.read_all_row()
# list_token = ir_system.tokenizer(text_all_file)
# list_clean_token = ir_system.clean_word(list_token)
# print("\033[95manswer 1:\033[0m\n", list_clean_token, "\n")
# dict_token = ir_system.generate_stopwords(list_clean_token)
# list_rank = ir_system.add_value_to_list(dict_token)
# sorted_dict = ir_system.sort_dict(dict_token, list_rank, 55)
# print("\033[95manswer 2:\033[0m\n", sorted_dict, "\n")
# text_title_and_plot = ir_system.read_title_and_plot()
# list_tokenize_title_and_plot = ir_system.tokenize_title_and_plot(text_title_and_plot)
# posting_title_and_plot = ir_system.posting_title_and_plot(list_tokenize_title_and_plot)
# print("\033[95manswer 3:\033[0m\n", posting_title_and_plot, "\n")
print("\033[94mنمایه ایجاد شده باید قابلیت حذف و اضافه تک سند را داشته باشد. برای اضافه شدن سند، یک رشته داده میشود که اطالعات "
      + "مربوط به سند شامل id و plot و title در آن با کاما جدا شده است. برای حذف سند نیز id آن داده میشود.\033[0m")
text_title_and_plot_with_change = ir_system.edit_read_title_and_plot()
list_tokenize_title_and_plot_with_change = ir_system.tokenize_title_and_plot(text_title_and_plot_with_change)
posting_title_and_plot_with_change = ir_system.posting_title_and_plot(list_tokenize_title_and_plot_with_change)
print("\033[95manswer 4:\033[0m\n", posting_title_and_plot_with_change, "\n")
