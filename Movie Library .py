import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Основное окно приложения
root = tk.Tk()
root.title("Movie Library")
root.geometry("700x600")

# ------- Вводные поля -------
tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5, sticky='w')
title_entry = tk.Entry(root, width=25)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5, sticky='w')
genre_entry = tk.Entry(root, width=25)
genre_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5, sticky='w')
year_entry = tk.Entry(root, width=25)
year_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Рейтинг").grid(row=3, column=0, padx=5, pady=5, sticky='w')
rating_entry = tk.Entry(root, width=25)
rating_entry.grid(row=3, column=1, padx=5, pady=5)

# ------- Таблица фильмов -------
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

# ------- Фильтры -------
tk.Label(root, text="Фильтр по жанру").grid(row=4, column=0, padx=5, pady=5, sticky='w')
genre_filter_var = tk.StringVar()
genre_filter = ttk.Combobox(root, textvariable=genre_filter_var, width=23)
genre_filter['values'] = ['Все']
genre_filter.current(0)
genre_filter.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по году").grid(row=4, column=2, padx=5, pady=5, sticky='w')
year_filter_var = tk.StringVar()
year_filter = ttk.Combobox(root, textvariable=year_filter_var, width=23)
year_filter['values'] = ['Все']
year_filter.current(0)
year_filter.grid(row=4, column=3, padx=5, pady=5)

# ------- Данные -------
movies = []

def load_data():
    global movies
    if os.path.exists("movies.json"):
        with open("movies.json", "r", encoding="utf-8") as f:
            try:
                movies = json.load(f)
            except json.JSONDecodeError:
                movies = []
    refresh_table()

def save_data():
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def refresh_table():
    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)
    # Обновление фильтров
    update_filter_options()
    genre_filter_value = genre_filter_var.get()
    year_filter_value = year_filter_var.get()
    for movie in movies:
        show = True
        # Фильтр по жанру
        if genre_filter_value != 'Все' and movie['Жанр'] != genre_filter_value:
            show = False
        # Фильтр по году
        if year_filter_value != 'Все' and str(movie['Год']) != year_filter_value:
            show = False
        if show:
            tree.insert("", "end", values=(
                movie['Название'],
                movie['Жанр'],
                movie['Год'],
                movie['Рейтинг']
            ))

def update_filter_options():
    # Обновление значений фильтров
    genres = set(movie['Жанр'] for movie in movies)
    years = set(str(movie['Год']) for movie in movies)
    genre_filter['values'] = ['Все'] + sorted(genres)
    year_filter['values'] = ['Все'] + sorted(years)

def add_movie():
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return
    if not year.isdigit():
        messagebox.showerror("Ошибка", "Год должен быть числом")
        return
    try:
        rating_value = float(rating)
        if not (0 <= rating_value <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
        return

    movie = {
        "Название": title,
        "Жанр": genre,
        "Год": int(year),
        "Рейтинг": rating_value
    }
    movies.append(movie)
    save_data()
    refresh_table()
    # Очистка полей
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

def apply_filters(event=None):
    refresh_table()

# Кнопка добавить
add_button = tk.Button(root, text="Добавить фильм", command=add_movie)
add_button.grid(row=7, column=0, columnspan=2, pady=10)

# Связываем фильтры с обновлением таблицы
genre_filter.bind("<<ComboboxSelected>>", apply_filters)
year_filter.bind("<<ComboboxSelected>>", apply_filters)

# Загружаем данные при запуске
load_data()

# Запуск
root.mainloop()