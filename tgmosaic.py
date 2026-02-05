# -*- coding: utf-8 -*-
"""
Нарезка горизонтальной картинки на плитки 100×100 для склейки эмодзи в Telegram.
По длине (ширине) режем на куски по 100 px; высота фиксируется 100 px.
Последний неполный кусок дополняется прозрачностью.
"""

from PIL import Image
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


TILE_SIZE = 100
FILL_COLOR = (0, 0, 0, 0)  # прозрачность для «пустоты»


def split_horizontal(path, output_folder, tile_size=TILE_SIZE, fill_color=FILL_COLOR):
    """
    Делит изображение по длине на плитки tile_size×tile_size.
    Высота картинки приводится к tile_size, последний столбец при неполной ширине дополняется fill_color.
    """
    img = Image.open(path)
    img.load()
    w, h = img.size

    # Конвертируем в RGBA, чтобы последний кусок можно было дополнять прозрачностью
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Масштабируем с сохранением пропорций: высота = tile_size, ширина меняется пропорционально
    if h != tile_size:
        resample = getattr(Image, "Resampling", Image).LANCZOS
        new_w = max(1, round(w * tile_size / h))
        img = img.resize((new_w, tile_size), resample)
        w, h = img.size

    os.makedirs(output_folder, exist_ok=True)
    count = 0

    for x in range(0, w, tile_size):
        box = (x, 0, min(x + tile_size, w), h)
        tile = img.crop(box)

        # Неполный последний кусок по ширине — дополняем пустотой
        if tile.size[0] < tile_size or tile.size[1] < tile_size:
            new_tile = Image.new("RGBA", (tile_size, tile_size), fill_color)
            new_tile.paste(tile, (0, 0))
            tile = new_tile

        tile.save(os.path.join(output_folder, f"tile_{count}.png"))
        count += 1

    return count


def run_gui():
    root = tk.Tk()
    root.title("TG Mosaic — нарезка 100×100 для эмодзи")
    root.minsize(400, 180)
    root.resizable(True, False)

    path_var = tk.StringVar()
    folder_var = tk.StringVar()
    status_var = tk.StringVar(value="Выберите картинку и папку для плиток.")

    def choose_image():
        p = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Все файлы", "*.*"),
            ],
        )
        if p:
            path_var.set(p)
            status_var.set("Файл выбран. Укажите папку и нажмите «Нарезать».")

    def choose_folder():
        d = filedialog.askdirectory(title="Папка для сохранения плиток")
        if d:
            folder_var.set(d)
            status_var.set("Папка выбрана. Нажмите «Нарезать».")

    def run_split():
        path = path_var.get().strip()
        folder = folder_var.get().strip()
        if not path:
            messagebox.showwarning("Нет файла", "Выберите изображение.")
            return
        if not os.path.isfile(path):
            messagebox.showerror("Ошибка", f"Файл не найден:\n{path}")
            return
        if not folder:
            messagebox.showwarning("Нет папки", "Выберите папку для сохранения плиток.")
            return
        try:
            n = split_horizontal(path, folder)
            status_var.set(f"Готово: сохранено плиток — {n}")
            messagebox.showinfo("Готово", f"Создано плиток: {n}\nПапка: {folder}")
        except Exception as e:
            status_var.set("Ошибка")
            messagebox.showerror("Ошибка", str(e))

    f = ttk.Frame(root, padding=12)
    f.pack(fill=tk.BOTH, expand=True)

    ttk.Label(f, text="Изображение:").grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
    ttk.Entry(f, textvariable=path_var, width=50).grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
    ttk.Button(f, text="Обзор…", command=choose_image).grid(row=1, column=1, padx=(8, 0), pady=(0, 8))

    ttk.Label(f, text="Папка для плиток:").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
    ttk.Entry(f, textvariable=folder_var, width=50).grid(row=3, column=0, sticky=tk.EW, pady=(0, 8))
    ttk.Button(f, text="Обзор…", command=choose_folder).grid(row=3, column=1, padx=(8, 0), pady=(0, 8))

    btn = ttk.Button(f, text="Нарезать", command=run_split)
    btn.grid(row=4, column=0, columnspan=2, pady=(8, 4))

    ttk.Label(f, textvariable=status_var, foreground="gray").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(4, 0))

    f.columnconfigure(0, weight=1)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
