import matplotlib.figure
import matplotlib.patches
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Radiobutton
from tkinter.ttk import Combobox
from datetime import date
from functools import partial

# Функция для поиска нынешней даты
def find_today():
    return date.today().strftime("%d.%m.%Y")

#функция для подсчета общего числа калорий
def summ():
    connect = sqlite3.connect('archive.db')
    cursor = connect.cursor()
    cursor.execute('''SELECT kkal FROM archive WHERE date = ?''', [find_today()])
    items=cursor.fetchall()
    summa=0
    for item in items:
        summa += item[0]
    connect.close()
    return summa

# Окно при запуске приложения и вычислении его нормы ккал
def ckal_calculator():
    global ckal
    # функция для подсчета нормы ккал, исходя из физических нагрузок
    def calculeter():
        if my_activiti.get() == "Physical activity is absent or minimal":
            ckal.set(int((my_height.get() * 6.25 + my_weight.get() * 10 - my_age.get() * 5 + my_gender.get()) * 1.2))
        elif my_activiti.get() == "Midle workouts 2-3 times a week":
            ckal.set(int((my_height.get() * 6.25 + my_weight.get() * 10 - my_age.get() * 5 + my_gender.get()) * 1.38))
        elif my_activiti.get() == "Midle workouts 4-5 times a week":
            ckal.set(int((my_height.get() * 6.25 + my_weight.get() * 10 - my_age.get() * 5 + my_gender.get()) * 1.46))
        elif my_activiti.get() == "Workout every day":
            ckal.set(int((my_height.get() * 6.25 + my_weight.get() * 10 - my_age.get() * 5 + my_gender.get()) * 1.64))
        elif my_activiti.get() == "Workout every day + physical work":
            ckal.set(int((my_height.get() * 6.25 + my_weight.get() * 10 - my_age.get() * 5 + my_gender.get()) * 1.9))

    # окошко расчёта калорий
    window = Tk()
    window.title('Calorie Calculation')
    window.geometry("300x350")
    window['bg'] = 'lavender'

    label = Label(text="Enter your personal data", bg="lavender")
    label.pack(pady=5)

    # создаем переменные
    my_height = IntVar()
    my_weight = IntVar()
    my_age = IntVar()
    my_gender = IntVar()
    my_activiti = StringVar()
    ckal = IntVar()

    # блок невидимых рамок для красивого интерфейса
    f_1 = Frame(window)
    f_2 = Frame(window)
    f_3 = Frame(window)
    f_4 = Frame(window)
    f_5 = Frame(window)
    f_6 = Frame(window)

    # ввод данных
    height_label = Label(f_1, text="Height ", bg="lavender")
    height_entry = Entry(f_1, width=8, textvariable=my_height)
    height2_label = Label(f_1, text="cm ", bg="lavender")

    weight_label = Label(f_2, text="Weight ", bg="lavender")
    weight_entry = Entry(f_2, width=8, textvariable=my_weight)
    weight2_label = Label(f_2, text="kg ", bg="lavender")

    age_label = Label(f_3, text="Age ", bg="lavender")
    age_entry = Entry(f_3, width=8, textvariable=my_age)

    gender_label = Label(f_4, text="Gender ", bg="lavender")
    rad1 = Radiobutton(f_4, text='М', value=4, variable=my_gender)
    rad2 = Radiobutton(f_4, text='W', value=-161, variable=my_gender)

    activiti_label = Label(f_5, text="Activity ", bg="lavender")
    activiti = Combobox(f_5, textvariable=my_activiti, width=48,
                        values=["Physical activity is absent or minimal",
                                "Midle workouts 2-3 times a week",
                                "Midle workouts 4-5 times a week",
                                "Workout every day",
                                "Workout every day + physical work"])

    # вывод данных
    ckal_label1 = Label(f_6, text="Your calories norm: ", bg="lavender")
    ckal_label2 = Label(f_6, textvariable=ckal, bg="lavender")
    ckal_label3 = Label(f_6, text="kcal ", bg="lavender")

    message_button = Button(text="Get to know", bg="pink", command=calculeter)

    # упорядочивание элементов окна
    f_1.pack(pady=5)
    f_2.pack(pady=5)
    f_3.pack(pady=5)
    f_4.pack(pady=5)
    f_5.pack(pady=5)
    message_button.pack(pady=5)
    f_6.pack(pady=5)

    height_label.pack(side=LEFT)
    weight_label.pack(side=LEFT)
    age_label.pack(side=LEFT)
    gender_label.pack(side=LEFT)
    activiti_label.pack(side=LEFT)
    ckal_label1.pack(side=LEFT)

    height_entry.pack(side=LEFT)
    height2_label.pack(side=LEFT)
    weight_entry.pack(side=LEFT)
    weight2_label.pack(side=LEFT)
    age_entry.pack(side=LEFT)
    rad1.pack(side=LEFT)
    rad2.pack(side=LEFT)
    activiti.pack(side=LEFT)
    ckal_label2.pack(side=LEFT)
    ckal_label3.pack(side=LEFT)

    btn = Button(window, text="Save", bg="pink", command=window.destroy)
    btn.pack(pady=30, side=TOP)

    window.mainloop()

    return ckal

# Таблица при нажатии на кнопку архив
def archive():
    def find_product_from_day():
        my_frame.delete(*my_frame.get_children()) ##очищает таблицу

        connect = sqlite3.connect('archive.db')  ##делаем запрос к базе данных
        cursor = connect.cursor()
        cursor.execute('''SELECT meal,name,g,kkal,p,f,c  FROM archive WHERE date = ?''', [date_entry.get()])
        all_products = cursor.fetchall()
        connect.close()
        for item in all_products:
            my_frame.insert(parent='', index='end', values=item)
            my_frame.pack()

    window = Tk()
    window.title("Archive")
    window.geometry('350x620')
    window['bg'] = 'Lavender'

    title = Label(window, text="Archive", bg="Lavender", fg="purple4", font=70, width=30)
    title.pack(pady=5)

    my_date = StringVar()

    frame = Frame(window)
    date_label = Label(frame, text="Date ", bg="lavender")
    date_entry = Entry(frame, width=10, textvariable=my_date)
    date_label.pack(side=LEFT)
    date_entry.pack(side=RIGHT)
    frame.pack(pady=5)

    message_button = Button(window, text="Find", bg="pink", command=find_product_from_day)
    message_button.pack(pady=15)

    # Таьлица
    main_frame = Frame(window)
    main_frame.pack(pady=40)

    # бегунок
    frame_scroll = Scrollbar(main_frame)
    frame_scroll.pack(side=RIGHT, fill=Y)

    frame_scroll = Scrollbar(main_frame, orient='horizontal')
    frame_scroll.pack(side=BOTTOM, fill=X)

    my_frame = ttk.Treeview(main_frame, yscrollcommand=frame_scroll.set, xscrollcommand=frame_scroll.set)
    my_frame.pack()

    frame_scroll.config(command=my_frame.yview)
    frame_scroll.config(command=my_frame.xview)

    # определение колонок
    my_frame['columns'] = (
    'player_eating', 'player_product', 'player_mass', 'player_kkal', 'player_p', 'player_f', 'player_c')

    # формат колонок
    my_frame.column("#0", width=0, stretch=NO)
    my_frame.column("player_eating", anchor=CENTER, width=80)
    my_frame.column("player_product", anchor=CENTER, width=150)
    my_frame.column("player_mass", anchor=CENTER, width=80)
    my_frame.column("player_kkal", anchor=CENTER, width=80)
    my_frame.column("player_p", anchor=CENTER, width=80)
    my_frame.column("player_f", anchor=CENTER, width=80)
    my_frame.column("player_c", anchor=CENTER, width=80)

    # заголовки колонок
    my_frame.heading("#0", text="", anchor=CENTER)
    my_frame.heading("player_eating", text="Meal", anchor=CENTER)
    my_frame.heading("player_product", text="Product name", anchor=CENTER)
    my_frame.heading("player_mass", text="Mass", anchor=CENTER)
    my_frame.heading("player_kkal", text="Kcal", anchor=CENTER)
    my_frame.heading("player_p", text="Proteins", anchor=CENTER)
    my_frame.heading("player_f", text="Fats", anchor=CENTER)
    my_frame.heading("player_c", text="Carbohydrates", anchor=CENTER)

    # кнопка СОХРАНЕНИЯ и выхода
    btn = Button(window, text="Close", bg="pink", relief=RAISED, bd=1, command=window.destroy)
    btn.pack(side=TOP, pady=60)

    window.mainloop()

# Окна
def windows(meal, bg_color, fg_color):
    # калькулятор расчета кбжу по массе
    def calculation(selected_products):
        calculated_selected_product = []
        for item in selected_products:
            if type(item) == str:
                calculated_selected_product.append(item)
            else:
                calculated_selected_product.append(item * int(new_mass_entry.get()) / 100)
        return tuple(calculated_selected_product)

    # функция добавляет продукт в таблицу
    def add_product():
        connect = sqlite3.connect('n_base.db')  ##делаем запрос к базе данных
        cursor = connect.cursor()
        cursor.execute('''SELECT * FROM n_base WHERE name = ?''', [new_product_entry.get().title()])
        calculated_selected_product = calculation(cursor.fetchone())
        connect.close()

        # записываем значение в таблицу
        my_frame.insert(parent='', index='end', values=calculated_selected_product)
        my_frame.pack()

        new_product_entry.delete(0, END)  ##очищает окно ввода
        new_mass_entry.delete(0, END)

        add_product_to_base(calculated_selected_product)

    # функция добавляет продукт в БД
    def add_product_to_base(calculated_selected_product):
        # добавить запись в базу данных
        added_calculated_selected_product = []
        added_calculated_selected_product.append(find_today())
        added_calculated_selected_product.append(meal.lower())
        for item in calculated_selected_product:
            added_calculated_selected_product.append(item)

        connect = sqlite3.connect('archive.db')
        cursor = connect.cursor()
        cursor.execute('''INSERT INTO archive (date,meal,name,g,kkal,p,f,c) VALUES (?,?,?,?,?,?,?,?)''',
                       tuple(added_calculated_selected_product))
        connect.commit()
        connect.close()

    # функция удаляет продукт из таблицы
    def delete_product():
        # захватить запись в переменную
        selected = my_frame.focus()
        deleted_selected_product = my_frame.item(selected, 'values')

        # удалить запись из таблицы
        selected_item = my_frame.selection()[0]
        my_frame.delete(selected_item)

        delete_product_from_base(deleted_selected_product)

    # функция удаляет продукт из БД
    def delete_product_from_base(deleted_selected_product):
        ## удалить запись из базы данных
        connect = sqlite3.connect('archive.db')
        cursor = connect.cursor()
        cursor.execute("DELETE FROM archive WHERE name = ? AND g = ?",
                       [deleted_selected_product[0], deleted_selected_product[1]])
        connect.commit()
        connect.close()

    # Таблица при нажатии на кнопку завтрак
    window = Tk()
    window.title(meal)
    window.geometry('350x620')
    window['bg'] = bg_color

    title = Label(window, text=meal, bg=bg_color, fg=fg_color, font=70, width=30)
    title.pack()

    main_frame = Frame(window)
    main_frame.pack()

    # бегунок
    frame_scroll = Scrollbar(main_frame)
    frame_scroll.pack(side=RIGHT, fill=Y)

    frame_scroll = Scrollbar(main_frame, orient='horizontal')
    frame_scroll.pack(side=BOTTOM, fill=X)

    my_frame = ttk.Treeview(main_frame, yscrollcommand=frame_scroll.set, xscrollcommand=frame_scroll.set)
    my_frame.pack()

    frame_scroll.config(command=my_frame.yview)
    frame_scroll.config(command=my_frame.xview)

    # определение колонок
    my_frame['columns'] = ('player_product', 'player_mass', 'player_kkal', 'player_p', 'player_f', 'player_c')

    # формат колонок
    my_frame.column("#0", width=0, stretch=NO)
    my_frame.column("player_product", anchor=CENTER, width=150)
    my_frame.column("player_mass", anchor=CENTER, width=80)
    my_frame.column("player_kkal", anchor=CENTER, width=80)
    my_frame.column("player_p", anchor=CENTER, width=80)
    my_frame.column("player_f", anchor=CENTER, width=80)
    my_frame.column("player_c", anchor=CENTER, width=80)

    # заголовки колонок
    my_frame.heading("#0", text="", anchor=CENTER)
    my_frame.heading("player_product", text="Product name", anchor=CENTER)
    my_frame.heading("player_mass", text="Mass", anchor=CENTER)
    my_frame.heading("player_kkal", text="Kcal", anchor=CENTER)
    my_frame.heading("player_p", text="Proteins", anchor=CENTER)
    my_frame.heading("player_f", text="Fats", anchor=CENTER)
    my_frame.heading("player_c", text="Carbohydrates", anchor=CENTER)

    # добавляем продукты в таблицу, добавленные ранее
    connect = sqlite3.connect('archive.db')  ##делаем запрос к базе данных
    cursor = connect.cursor()
    cursor.execute('''SELECT name,g,kkal,p,f,c  FROM archive WHERE date = ? AND meal = ?''', [find_today(), meal.lower()])
    all_products = cursor.fetchall()
    connect.close()
    for item in all_products:
        my_frame.insert(parent='', index='end', values=item)
        my_frame.pack()

    # таблица для добавления данных
    low_frame = Frame(window)
    low_frame.pack(pady=50)

    # заголовки
    new_product = Label(low_frame, text="Product")
    new_product.grid(row=0, column=0)

    new_mass = Label(low_frame, text="Mass")
    new_mass.grid(row=0, column=1)

    # окна для ввода данных
    my_product = StringVar()
    my_mass = IntVar()

    new_product_entry = Entry(low_frame, textvariable=my_product)
    new_product_entry.grid(row=1, column=0)

    new_mass_entry = Entry(low_frame, textvariable=my_mass)
    new_mass_entry.grid(row=1, column=1)

    # Кнопки
    select_button = Button(window, text="Add", command=add_product)
    select_button.pack(pady=5)

    delete_button = Button(window, text="Delete", command=delete_product)
    delete_button.pack(pady=5)

    btn = Button(window, text="Close", bg="pink", fg="HotPink4", relief=RAISED, bd=1, command=window.destroy)
    btn.pack(side=TOP, pady=40)

    window.mainloop()

# вызов окна с рачсетом нормы ккал и сохранение нормы
ckal = ckal_calculator()

window = Tk()

# иконка приложения
# photo = PhotoImage(file='58431506a9a7d158c60a2227.png')
# window.iconphoto(False, photo)

window.title("App:'Calories Calculator'")
window.geometry('350x620')
window['bg'] = 'Lavender'

hat = Frame(window)
hat['bg'] = 'lavender'

title = Label(hat, text=find_today(), bg = 'lavender', fg="purple4", font=70, width=20)
title.pack(pady=3, side=LEFT)

btn = Button(hat, text ='Archive', bg="pink", fg ="HotPink4", relief=RAISED, bd = 6, width=12, command=archive)
btn.pack(pady=3, side=RIGHT)

hat.pack()

# кнопка выбора завтрака
btn = Button(window, text ='Breakfast', bg="Linen", fg ='SandyBrown', font=90, width=30, height=1, relief=RAISED, bd=6, command=partial(windows, "Breakfast", "Linen", "SandyBrown"))
btn.pack(pady=3, side=TOP)

# кнопка выбора обеда
btn = Button(window, text="Lunch", bg="Honeydew", fg ="DarkSeaGreen", font=70, width=30, height=1, relief=RAISED, bd=6, command=partial(windows, "Lunch", "Honeydew", "DarkSeaGreen"))
btn.pack(pady=2, side=TOP)

# кнопка выбора ужина
btn = Button(window, text="Dinner", bg="AliceBlue", fg ="CornflowerBlue", font=70, width=30, height=1, relief=RAISED, bd=6, command=partial(windows, "Dinner", "AliceBlue", "CornflowerBlue"))
btn.pack(pady=2, side=TOP)

# кнопка выбора перекуса
btn = Button(window, text="Snack", bg="MistyRose", fg ="PaleVioletRed", font=70, width=30, height=1, relief=RAISED, bd=6, command=partial(windows, "Snack", "MistyRose", "PaleVioletRed"))
btn.pack(pady=2, side=TOP)

#диаграмма для сводки
fig = matplotlib.figure.Figure(figsize=(4,3), facecolor="Lavender")
ax = fig.add_subplot(111)

ax.pie([summ(),ckal.get()-summ()], colors = ("lightcoral", "yellowgreen"),
       wedgeprops=dict(width=0.5),
       autopct='%1.1f%%')
ax.legend([f"Eaten:{summ()} kcal",
          f"Left: {ckal.get()-summ()} kcal"])
circle=matplotlib.patches.Circle((0,0), 0.3, color='lavender')
ax.add_artist(circle)
ax.axis('equal')
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()
canvas.draw()

# кнопка СОХРАНЕНИЯ и выхода
btn = Button(window, text="Close", bg="Pink", fg="HotPink4", relief=RAISED, bd = 1, command=window.destroy)
btn.pack(side=TOP)

window.mainloop()
