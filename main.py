import json
import os
import uuid

# настройки
DATA_FILE = "library.json"


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except:
        return []


def make_book(title, author, genre, year, description="", ol_key=""):
    return {
        "id": str(uuid.uuid4())[:8], "title": title, "author": author,
        "genre": genre, "year": year, "description": description,
        "ol_key": ol_key, "is_read": False, "is_favorite": False,
    }


def book_str(b):
    st = "✓ Прочитана" if b["is_read"] else "✗ Не прочитана"
    fv = " ★" if b["is_favorite"] else ""
    return f'[{b["id"]}] «{b["title"]}» — {b["author"]} ({b["year"]}, {b["genre"]}) [{st}]{fv}'


def book_detail(b):
    return (
        f'  ID:          {b["id"]}\n'
        f'  Название:    {b["title"]}\n'
        f'  Автор:       {b["author"]}\n'
        f'  Жанр:        {b["genre"]}\n'
        f'  Год издания: {b["year"]}\n'
        f'  Описание:    {b["description"] or "—"}\n'
        f'  Статус:      {"Прочитана" if b["is_read"] else "Не прочитана"}\n'
        f'  Избранное:   {"Да" if b["is_favorite"] else "Нет"}'
    )


def find(books, bid):
    return next((b for b in books if b["id"] == bid), None)


def search(books, q):
    q = q.lower()
    return [b for b in books if q in b["title"].lower() or q in b["author"].lower() or q in b["description"].lower()]


def is_dup(books, title, author):
    t, a = title.lower().strip(), author.lower().strip()
    return any(b["title"].lower().strip() == t and b["author"].lower().strip() == a for b in books)


def pause():
    input("\n   Enter — вернуться в меню...")


def header(text):
    print(f"\n{'=' * 55}\n  {text}\n{'=' * 55}")


def print_list(books):
    if not books:
        print("  Книги не найдены.")
    else:
        for b in books:
            print(f"  {book_str(b)}")


def input_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except:
            print("  Ошибка: введите целое число.")


def menu_add(books):
    header("Добавление книги")
    title = input("  Название: ").strip()
    if not title:
        print("  Ошибка: пустое название.")
        return
    author = input("  Автор: ").strip()
    if not author:
        print("  Ошибка: пустой автор.")
        return
    genre = input("  Жанр: ").strip()
    if not genre:
        print("  Ошибка: пустой жанр.")
        return
    year = input_int("  Год издания: ")
    desc = input("  Описание (необязательно): ").strip()
    b = make_book(title, author, genre, year, desc)
    books.append(b)
    save_books(books)
    print(f"\n   Добавлена: {book_str(b)}")


def menu_view(books):
    header("Просмотр библиотеки")
    if not books:
        print("  Библиотека пуста.")
        return
    print("  Сортировка:  1-название  2-автор  3-год  0-без")
    sc = input("  > ").strip()
    print("  Фильтр:  1-жанр  2-прочитанные  3-непрочитанные  0-без")
    fc = input("  > ").strip()

    result = list(books)
    if fc == "1":
        genres = sorted(set(b["genre"] for b in books))
        if genres: print(f"  Жанры: {', '.join(genres)}")
        g = input("  Жанр: ").strip()
        result = [b for b in result if b["genre"].lower() == g.lower()]
    elif fc == "2":
        result = [b for b in result if b["is_read"]]
    elif fc == "3":
        result = [b for b in result if not b["is_read"]]

    if sc == "1":
        result = sorted(result, key=lambda b: b["title"].lower())
    elif sc == "2":
        result = sorted(result, key=lambda b: b["author"].lower())
    elif sc == "3":
        result = sorted(result, key=lambda b: b["year"])

    header(f"Результат ({len(result)})")
    print_list(result)
    pause()


def menu_search(books):
    header("Поиск книги")
    q = input("  Ключевое слово: ").strip()
    if not q:
        print("  Пустой запрос.")
        return
    res = search(books, q)
    print(f"\n  Найдено: {len(res)}")
    print_list(res)
    pause()


def menu_details(books):
    header("Подробности о книге")
    b = find(books, input("  ID книги: ").strip())
    if not b:
        print("  Книга не найдена.")
        return
    print(book_detail(b))
    pause()


def menu_favorite(books):
    header("Избранное — добавить / удалить")
    b = find(books, input("  ID книги: ").strip())
    if not b:
        print("  Книга не найдена.")
        return
    b["is_favorite"] = not b["is_favorite"]
    save_books(books)
    print(f'   «{b["title"]}» {"добавлена в избранное" if b["is_favorite"] else "удалена из избранного"}.')


def menu_status(books):
    header("Изменение статуса")
    b = find(books, input("  ID книги: ").strip())
    if not b:
        print("  Книга не найдена.")
        return
    print(f'  Сейчас: {"Прочитана" if b["is_read"] else "Не прочитана"}')
    print("    1. Прочитана    2. Не прочитана")
    c = input("  > ").strip()
    if c in ("1", "2"):
        b["is_read"] = c == "1"
        save_books(books)
        print(f'  ✓ «{b["title"]}» → {"Прочитана" if b["is_read"] else "Не прочитана"}.')
    else:
        print("  Неверный выбор.")


def menu_favorites(books):
    header("Избранные книги")
    fav = [b for b in books if b["is_favorite"]]
    print_list(fav)
    if fav: pause()


def menu_delete(books):
    header("Удаление книги")
    b = find(books, input("  ID книги: ").strip())
    if not b:
        print("  Книга не найдена.")
        return
    print(f'  Удалить «{b["title"]}»? (да/нет)')
    if input("  > ").strip().lower() in ("да", "д", "y", "yes"):
        books.remove(b)
        save_books(books)
        print(f'  ✓ «{b["title"]}» удалена.')
    else:
        print("  Отменено.")


books = load_books()

MENU = [
    ("1", "Добавить книгу", menu_add),
    ("2", "Просмотр библиотеки", menu_view),
    ("3", "Поиск книги", menu_search),
    ("4", "Подробности о книге", menu_details),
    ("5", "Добавить / убрать из избранного", menu_favorite),
    ("6", "Изменить статус (прочитана / не прочитана)", menu_status),
    ("7", "Избранные книги", menu_favorites),
    ("8", "Удалить книгу", menu_delete),
    ("0", "Выход", None),
]

while True:
    header("T-Библиотека — Главное меню")
    for k, l, _ in MENU:
        print(f"    {k}. {l}")
    print(f"\n  В библиотеке: {len(books)} книг")

    ch = input("\n  Ваш выбор: ").strip()
    if ch == "0":
        print("\n  До свидания!\n")
        quit(0)
    h = next((f for k, _, f in MENU if k == ch), None)
    if h:
        h(books)
    else:
        print("  Неверный пункт меню.")
