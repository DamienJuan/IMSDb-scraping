import pandas as pd
import re
import webbrowser
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry

df = pd.read_csv('./imsdb_movie_scripts.csv')

all_genres = sorted(set(genre.strip() for genres in df['Genres'].dropna() for genre in genres.split(',')))
all_writers = sorted(set(writer.strip() for writers in df['Writers'].dropna() for writer in writers.split(',')))

def search_by_word(df, word, columns):
    word = word.lower()
    pattern = re.compile(word)
    mask = df[columns].apply(lambda x: x.str.lower().str.contains(pattern))
    return df[mask.any(axis=1)]

def filter_by_year(df, start_year=None, end_year=None):
    if start_year and not end_year:
        mask = (df['Script Date'] >= start_year) | (df['Movie Release Date'] >= start_year)
    elif end_year and not start_year:
        mask = (df['Script Date'] <= end_year) | (df['Movie Release Date'] <= end_year)
    elif start_year and end_year:
        mask = ((df['Script Date'] >= start_year) & (df['Script Date'] <= end_year)) | \
               ((df['Movie Release Date'] >= start_year) & (df['Movie Release Date'] <= end_year))
    else:
        mask = pd.Series([True] * len(df))
    
    return df[mask]

def filter_by_writer(df, writer):
    writer = writer.lower()
    return df[df['Writers'].str.lower().str.contains(writer)]

def search_movies(df, word=None, genre=None, writer=None, start_year=None, end_year=None):
    result_df = df.copy()
    
    if word:
        result_df = search_by_word(result_df, word, ['Script', 'Genres'])
    if genre:
        result_df = search_by_word(result_df, genre, ['Genres'])
    if writer:
        result_df = filter_by_writer(result_df, writer)
    if start_year or end_year:
        result_df = filter_by_year(result_df, start_year, end_year)
    
    return result_df['Title'].unique()

def handle_search():
    word = word_entry.get()
    genre = genre_var.get()
    writer = writer_combobox.get()
    start_year = start_date_entry.get()
    end_year = end_date_entry.get()
    
    word = word if word else None
    genre = genre if genre else None
    writer = writer if writer else None
    start_year = int(start_year) if start_year else None
    end_year = int(end_year) if end_year else None
    
    results = search_movies(df, word=word, genre=genre, writer=writer, start_year=start_year, end_year=end_year)
    
    results_listbox.delete(0, END)
    
    for title in results:
        results_listbox.insert(END, title)

def on_listbox_select(event):
    selected_title = results_listbox.get(results_listbox.curselection())
    url = f"https://www.imsdb.com/scripts/{selected_title.replace(' ', '-')}.html"
    webbrowser.open(url)

root = Tk()
root.title("Movie Search Engine")

word_label = Label(root, text="Word:")
word_label.grid(row=0, column=0, padx=10, pady=5, sticky=E)
word_entry = Entry(root)
word_entry.grid(row=0, column=1, padx=10, pady=5)

genre_label = Label(root, text="Genre:")
genre_label.grid(row=1, column=0, padx=10, pady=5, sticky=E)
genre_var = StringVar()
genre_combobox = ttk.Combobox(root, textvariable=genre_var)
genre_combobox['values'] = all_genres
genre_combobox.grid(row=1, column=1, padx=10, pady=5)

writer_label = Label(root, text="Writer:")
writer_label.grid(row=2, column=0, padx=10, pady=5, sticky=E)
writer_combobox = AutocompleteEntry(root, completevalues=all_writers)
writer_combobox.grid(row=2, column=1, padx=10, pady=5)

start_date_label = Label(root, text="Start Year (YYYY):")
start_date_label.grid(row=3, column=0, padx=10, pady=5, sticky=E)
start_date_entry = Entry(root)
start_date_entry.grid(row=3, column=1, padx=10, pady=5)

end_date_label = Label(root, text="End Year (YYYY):")
end_date_label.grid(row=4, column=0, padx=10, pady=5, sticky=E)
end_date_entry = Entry(root)
end_date_entry.grid(row=4, column=1, padx=10, pady=5)

search_button = Button(root, text="Search", command=handle_search)
search_button.grid(row=5, column=0, columnspan=2, pady=10)

results_listbox = Listbox(root, width=50, height=15)
results_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
results_listbox.bind("<<ListboxSelect>>", on_listbox_select)

root.mainloop()
