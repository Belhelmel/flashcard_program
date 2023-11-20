import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

class FlashcardAppBase:
    def __init__(self, root):
        self.root = root
        self.root.title("Szótanuló alkalmazás")

        window_width = 400
        window_height = 250

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.flashcard_frame = tk.Frame(root)
        self.flashcard_label = tk.Label(self.flashcard_frame, text="", font=("Arial", 18))
        self.flashcard_label.pack(pady=20)
        self.imported_data = None
        self.current_index = 0
        self.create_menus()

    def create_menus(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Importálás", command=self.import_file)
        file_menu.add_command(label="Kilépés", command=self.root.destroy)

        practice_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Gyakorlás", menu=practice_menu)
        practice_menu.add_command(label="Angol-Magyar", command=self.start_practice_english_to_hungarian)
        practice_menu.add_command(label="Magyar-Angol", command=self.start_practice_hungarian_to_english)

    def import_file(self):
        if self.imported_data is not None:
            response = messagebox.askyesno("Figyelmeztetés", "Már importált. Másik fájlt választ?")
            if not response:
                return

        file_path = filedialog.askopenfilename(filetypes=[("Excel fájlok", "*.xlsx")])

        if file_path:
            try:
                df = pd.read_excel(file_path)
                self.check_columns(df)
            except pd.errors.EmptyDataError:
                messagebox.showwarning("Üres fájl", "A választott fájl nem lehet üres!")
            except pd.errors.ParserError:
                messagebox.showwarning("Rossz formátum", "Válasszon Excel .xlsx fájlt!")

    def check_columns(self, df):
        required_columns = {'English', 'Hungarian'}
        if all(column in df.columns for column in required_columns):
            self.imported_data = df
            messagebox.showinfo("Siker", "A fájl sikeresen importálódott!")
        else:
            messagebox.showwarning("Nem sikerült.", "Az adatok az A (English) és B (Hungarian) oszlopokban legyenek!")

    def start_practice_english_to_hungarian(self):
        self.start_practice('English', 'Hungarian')

    def start_practice_hungarian_to_english(self):
        self.start_practice('Hungarian', 'English')

    def start_practice(self, source_column, target_column):
        if self.imported_data is None:
            messagebox.showwarning("", "Nincs fájl importálva. Először importáljon egy megfelelő fájlt!")
            return

        pairs = list(zip(self.imported_data[source_column], self.imported_data[target_column]))
        random.shuffle(pairs)

        self.flashcard_frame.pack_forget()
        self.flashcard_frame.pack(pady=20)

        self.current_index = 0
        self.show_flashcard(pairs)

        self.clear_buttons()

        tk.Button(self.flashcard_frame, text="Tudtam", command=lambda: self.next_flashcard(pairs)).pack(side=tk.LEFT,
                                                                                                           padx=10)
        tk.Button(self.flashcard_frame, text="Fordítás", command=lambda: self.flip_flashcard(pairs)).pack(
            side=tk.LEFT, padx=10)
        tk.Button(self.flashcard_frame, text="Nem tudtam", command=lambda: self.repeat_flashcard(pairs)).pack(
            side=tk.LEFT, padx=10)
        tk.Button(self.flashcard_frame, text="Vissza a kezdőlapra", command=self.reset_interface).pack(side=tk.RIGHT,
                                                                                                     padx=10)

    def show_flashcard(self, pairs):
        source_word, target_word = pairs[self.current_index]
        self.flashcard_label.config(text=source_word)

    def flip_flashcard(self, pairs):
        current_index = self.current_index

        if current_index < len(pairs):
            source_word, target_word = pairs[current_index]

            if not hasattr(self, 'showing_target'):
                self.showing_target = False

            if self.showing_target:
                self.flashcard_label.config(text=source_word)
                self.showing_target = False
            else:
                self.flashcard_label.config(text=target_word)
                self.showing_target = True
        else:
            messagebox.showinfo("Gratulálok!", "Végeztél az összes kártyával.")

    def next_flashcard(self, pairs):
        self.current_index += 1
        if self.current_index < len(pairs):
            self.show_flashcard(pairs)
        else:
            messagebox.showinfo("Gratulálok!", "Végeztél az összes kártyával.")

    def repeat_flashcard(self, pairs):
        current_index = self.current_index

        if current_index < len(pairs):
            current_pair = pairs[current_index]

            pairs.pop(current_index)
            pairs.append(current_pair)

            self.next_flashcard(pairs)
        else:
            messagebox.showinfo("Gratulálok!", "Végeztél az összes kártyával.")

    def reset_interface(self):
        self.flashcard_frame.pack_forget()
        self.create_menus()

    def clear_buttons(self):
        for widget in self.flashcard_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()


class HungarianToEnglishFlashcardApp(FlashcardAppBase):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = HungarianToEnglishFlashcardApp(root)
    root.mainloop()
