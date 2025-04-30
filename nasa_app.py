import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

# pobiera i wyswietla
def fetch_images():
    query = entry.get()
    if not query:
        return

    # usun wczesniejsze obrazy
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Pobierz dane z NASA API
    url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    response = requests.get(url)
    data = response.json()

    items = data["collection"]["items"]


    # jesli nic nie znajdzie to zwraca

    if not items:
        result_label.config(text="Brak wyników.")
        return

    # jeśli znajdzie to zwraca

    result_label.config(text=f"Znaleziono {min(20, len(items))} zdjęć dla: {query}")

    columns = 5  # Liczba kolumn w siatce
    row = 0
    col = 0

    for idx, item in enumerate(items[:20]):
        try:
            image_url = item["links"][0]["href"]
            img_response = requests.get(image_url)
            img_data = Image.open(BytesIO(img_response.content))
            img_data = img_data.resize((200, 150))
            tk_image = ImageTk.PhotoImage(img_data)

            # Utwórz etykietę z obrazem i dodaj ją do siatki
            img_label = tk.Label(image_frame, image=tk_image, bg="white")
            img_label.image = tk_image
            img_label.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col >= columns:
                col = 0
                row += 1
        except Exception as e:
            print("Błąd wczytywania obrazka:", e)

# Główne okno
root = tk.Tk()
root.title("NASA Image Viewer")
root.geometry("700x850")
root.configure(bg="white")  # Tło całej aplikacji

# Pole do wpisywania
entry = ttk.Entry(root, width=50)
entry.pack(pady=10)

# Przycisk
search_button = ttk.Button(root, text="Szukaj", command=fetch_images)
search_button.pack(pady=5)

# wynik
result_label = tk.Label(root, text="", fg="white", bg="white", font=("Arial", 10))
result_label.pack()

# Obszar przewijany
canvas = tk.Canvas(root, bg="white", height=700)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

# miejsce z obrazami
image_frame = tk.Frame(canvas, bg="white")

# przewijanie
image_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=image_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

# suwak
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Start aplikacji
root.mainloop()
