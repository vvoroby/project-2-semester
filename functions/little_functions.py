"""
Закрывает текущее окно, открывает главное окно
"""
def open_main(window_now):
    window_now.destroy()
    main()

"""
Закрывает текущее окно, открывает окно с приемом пищи
"""
def open_meal(window_main, meal, bg_color, fg_color):
    window_main.destroy()
    windows(meal, bg_color, fg_color)

"""
Закрывает текущее окно, открывает окно архива
"""
def open_archive(window_main):
    window_main.destroy()
    archive()

"""
Закрывает текущее окно, открывает окно калькулятора
"""
def open_cakculator(window_main):
    window_main.destroy()
    ckal_calculator()

"""
Закрывает текущее окно, открывает окно для добавления в БД
"""
def open_insert_new_product(window_meal, meal, bg_color, fg_color):
    window_meal.destroy()
    insert_new_product(meal, bg_color, fg_color)

"""
Функция для поиска сегодняшней даты при помощи модудя datetime
"""
def find_today():
    return date.today().strftime("%d.%m.%Y")
