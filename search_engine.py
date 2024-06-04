import pandas as pd
import re
from tkinter import *
from tkinter import ttk

# Load the CSV file into a DataFrame
df = pd.read_csv('./imsdb_movie_scripts.csv')

# Split and flatten writers and genres
all_genres = sorted(set(genre.strip() for genres in df['Genres'].dropna() for genre in genres.split(',')))
all_writers = sorted(set(writer.strip() for writers in df['Writers'].dropna() for writer in writers.split(',')))

# Function to search for a word in specified columns
def search_by_word(df, word, columns):
    word = word.lower()
    pattern = re.compile(word)
    mask = df[columns].apply(lambda x: x.str.lower().str.contains(pattern))
    return df[mask.any(axis=1)]

# Function to filter movies by year range
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

# Function to filter movies by writer
def filter_by_writer(df, writer):
    writer = writer.lower()
    return df[df['Writers'].str.lower().str.contains(writer)]

# Function to search movies based on various criteria
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

# Function to handle the search button click
def handle_search():
    word = word_entry.get()
    genre = genre_var.get()
    writer = writer_entry.get()
    start_year = start_date_entry.get()
    end_year = end_date_entry.get()
    
    # Convert empty strings to None
    word = word if word else None
    genre = genre if genre else None
    writer = writer if writer else None
    start_year = int(start_year) if start_year else None
    end_year = int(end_year) if end_year else None
    
    results = search_movies(df, word=word, genre=genre, writer=writer, start_year=start_year, end_year=end_year)
    
    # Clear the results listbox
    results_listbox.delete(0, END)
    
    # Insert the results into the listbox
    for title in results:
        results_listbox.insert(END, title)

# Function for autocomplete suggestions for writers
def update_writers_listbox(*args):
    search_term = writer_entry_var.get().lower()
    matching_writers = [writer for writer in all_writers if writer.lower().startswith(search_term)]
    writer_listbox.delete(0, END)
    for writer in matching_writers:
        writer_listbox.insert(END, writer)
    writer_listbox.place(x=writer_entry.winfo_x(), y=writer_entry.winfo_y() + writer_entry.winfo_height())

def on_writer_select(event):
    selected_writer = writer_listbox.get(writer_listbox.curselection())
    writer_entry_var.set(selected_writer)
    writer_listbox.place_forget()

def on_writer_entry_focus_out(event):
    if not writer_listbox.winfo_containing(event.x_root, event.y_root):
        writer_listbox.place_forget()

# Create the main window
root = Tk()
root.title("Movie Search Engine")

# Create the input fields and labels
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
writer_entry_var = StringVar()
writer_entry = Entry(root, textvariable=writer_entry_var)
writer_entry.grid(row=2, column=1, padx=10, pady=5)
writer_entry_var.trace_add('write', update_writers_listbox)
writer_entry.bind("<FocusOut>", on_writer_entry_focus_out)

writer_listbox = Listbox(root, height=5)
writer_listbox.bind("<<ListboxSelect>>", on_writer_select)

start_date_label = Label(root, text="Start Year (YYYY):")
start_date_label.grid(row=3, column=0, padx=10, pady=5, sticky=E)
start_date_entry = Entry(root)
start_date_entry.grid(row=3, column=1, padx=10, pady=5)

end_date_label = Label(root, text="End Year (YYYY):")
end_date_label.grid(row=4, column=0, padx=10, pady=5, sticky=E)
end_date_entry = Entry(root)
end_date_entry.grid(row=4, column=1, padx=10, pady=5)

# Create the search button
search_button = Button(root, text="Search", command=handle_search)
search_button.grid(row=5, column=0, columnspan=2, pady=10)

# Create the results listbox
results_listbox = Listbox(root, width=50, height=15)
results_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the main event loop
root.mainloop()
