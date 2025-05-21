import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

library = Library()

root = tk.Tk()
root.title("Library Management System")
root.geometry("700x500")
root.configure(padx=20, pady=20)

# ========= Functions =========

def toggle_ebook_fields():
    if ebook_var.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Download size required for eBooks.")
            return
        try:
            size_float = float(size)
        except ValueError:
            messagebox.showerror("Error", "Download size must be a number.")
            return
        book = EBook(title, author, isbn, size_float)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added to the library.")
    update_book_list()
    clear_entries()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed from library.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        listbox.delete(0, tk.END)
        if books:
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)
    ebook_var.set(False)
    toggle_ebook_fields()

# ========= Widgets =========

form_frame = tk.Frame(root)
form_frame.grid(row=0, column=0, sticky="nw")

# Title
tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="e")
title_entry = tk.Entry(form_frame, width=30)
title_entry.grid(row=0, column=1)

# Author
tk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky="e")
author_entry = tk.Entry(form_frame, width=30)
author_entry.grid(row=1, column=1)

# ISBN
tk.Label(form_frame, text="ISBN:").grid(row=2, column=0, sticky="e")
isbn_entry = tk.Entry(form_frame, width=30)
isbn_entry.grid(row=2, column=1)

# eBook Checkbox
ebook_var = tk.BooleanVar()
ebook_checkbox = tk.Checkbutton(form_frame, text="eBook?", variable=ebook_var, command=toggle_ebook_fields)
ebook_checkbox.grid(row=3, column=0, sticky="e")

# Size
tk.Label(form_frame, text="Download Size (MB):").grid(row=3, column=1, sticky="w")
size_entry = tk.Entry(form_frame, width=15, state='disabled')
size_entry.grid(row=3, column=1, padx=140)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

tk.Button(button_frame, text="Add Book", command=add_book, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Lend Book", command=lend_book, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Return Book", command=return_book, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Remove Book", command=remove_book, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="View Books by Author", command=view_books_by_author, width=43).grid(row=2, column=0, columnspan=2, pady=5)

# Book List
tk.Label(root, text="Library Inventory:").grid(row=2, column=0, sticky="w")
listbox = tk.Listbox(root, width=80, height=10)
listbox.grid(row=3, column=0, pady=10)

update_book_list()

root.mainloop()
