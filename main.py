# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform
from PIL import Image
import os

# Для Android — импортируем только то, что нужно
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from androidstorage4kivy import Chooser

TILE_SIZE = 100
FILL_COLOR = (0, 0, 0, 0)

def split_horizontal(path, output_folder):
    """Функция нарезки — без изменений, работает с реальными путями"""
    img = Image.open(path)
    w, h = img.size

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    if h != TILE_SIZE:
        resample = getattr(Image, "Resampling", Image).LANCZOS
        new_w = max(1, round(w * TILE_SIZE / h))
        img = img.resize((new_w, TILE_SIZE), resample)
        w, h = img.size

    os.makedirs(output_folder, exist_ok=True)
    count = 0

    for x in range(0, w, TILE_SIZE):
        box = (x, 0, min(x + TILE_SIZE, w), h)
        tile = img.crop(box)

        if tile.size[0] < TILE_SIZE or tile.size[1] < TILE_SIZE:
            new_tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), FILL_COLOR)
            new_tile.paste(tile, (0, 0))
            tile = new_tile

        tile.save(os.path.join(output_folder, f"tile_{count}.png"))
        count += 1

    return count

class MosaicApp(App):
    def build(self):
        self.title = "TG Mosaic"
        self.selected_image_uri = None   # храним URI
        self.selected_image_path = None  # реальный путь после конвертации
        self.output_folder_uri = None
        self.output_folder_path = None

        layout = BoxLayout(orientation='vertical', padding=12, spacing=10)

        self.img_label = Label(text="Изображение не выбрано", size_hint_y=0.1)
        layout.add_widget(self.img_label)
        btn_img = Button(text="Выбрать изображение", size_hint_y=0.1)
        btn_img.bind(on_press=self.select_image)
        layout.add_widget(btn_img)

        self.folder_label = Label(text="Папка не выбрана", size_hint_y=0.1)
        layout.add_widget(self.folder_label)
        btn_folder = Button(text="Выбрать папку", size_hint_y=0.1)
        btn_folder.bind(on_press=self.select_folder)
        layout.add_widget(btn_folder)

        btn_run = Button(text="Нарезать", size_hint_y=0.1)
        btn_run.bind(on_press=self.run_split)
        layout.add_widget(btn_run)

        self.status = Label(text="Готов к работе", size_hint_y=0.2, color=(0.5,0.5,0.5,1))
        layout.add_widget(self.status)

        # Запрос разрешений при запуске (только Android)
        if platform == 'android':
            if not check_permission(Permission.READ_EXTERNAL_STORAGE) or \
               not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ])

        return layout

    def select_image(self, instance):
        if platform == 'android':
            Chooser(choice=self._on_image_selected).choose_content()
        else:
            from kivy.uix.filechooser import FileChooserListView
            from kivy.uix.boxlayout import BoxLayout
            content = BoxLayout(orientation='vertical')
            filechooser = FileChooserListView(path=os.path.expanduser('~'))
            content.add_widget(filechooser)
            btn = Button(text='Выбрать', size_hint_y=0.1)
            content.add_widget(btn)
            popup = Popup(title='Выберите изображение', content=content,
                         size_hint=(0.9, 0.9))
            btn.bind(on_press=lambda x: self._set_image_desktop(filechooser.selection, popup))
            popup.open()

    def _on_image_selected(self, uri_list):
        """Колбэк для Android: получает список URI"""
        if uri_list and uri_list[0]:
            self.selected_image_uri = uri_list[0]
            # Конвертируем URI в реальный путь
            self.selected_image_path = Chooser.get_full_path(self.selected_image_uri)
            if self.selected_image_path:
                self.img_label.text = f"Изображение: {os.path.basename(self.selected_image_path)}"
                self.status.text = "Изображение выбрано"
            else:
                self.show_popup("Ошибка", "Не удалось получить путь к файлу")

    def _set_image_desktop(self, selection, popup):
        """Для десктопа"""
        popup.dismiss()
        if selection:
            self.selected_image_path = selection[0]
            self.img_label.text = f"Изображение: {os.path.basename(self.selected_image_path)}"
            self.status.text = "Изображение выбрано"

    def select_folder(self, instance):
        if platform == 'android':
            Chooser(choice=self._on_folder_selected).choose_content(directory=True)
        else:
            from kivy.uix.filechooser import FileChooserListView
            from kivy.uix.boxlayout import BoxLayout
            content = BoxLayout(orientation='vertical')
            filechooser = FileChooserListView(path=os.path.expanduser('~'), dirselect=True)
            content.add_widget(filechooser)
            btn = Button(text='Выбрать', size_hint_y=0.1)
            content.add_widget(btn)
            popup = Popup(title='Выберите папку', content=content,
                         size_hint=(0.9, 0.9))
            btn.bind(on_press=lambda x: self._set_folder_desktop(filechooser.selection, popup))
            popup.open()

    def _on_folder_selected(self, uri_list):
        """Колбэк для Android: выбор папки"""
        if uri_list and uri_list[0]:
            self.output_folder_uri = uri_list[0]
            # Конвертируем URI в путь
            self.output_folder_path = Chooser.get_full_path(self.output_folder_uri)
            if self.output_folder_path:
                self.folder_label.text = f"Папка: {os.path.basename(self.output_folder_path)}"
                self.status.text = "Папка выбрана"
            else:
                self.show_popup("Ошибка", "Не удалось получить путь к папке")

    def _set_folder_desktop(self, selection, popup):
        popup.dismiss()
        if selection:
            self.output_folder_path = selection[0]
            self.folder_label.text = f"Папка: {os.path.basename(self.output_folder_path)}"
            self.status.text = "Папка выбрана"

    def run_split(self, instance):
        if not self.selected_image_path:
            self.show_popup("Ошибка", "Сначала выберите изображение.")
            return
        if not self.output_folder_path:
            self.show_popup("Ошибка", "Сначала выберите папку для сохранения.")
            return
        if not os.path.isfile(self.selected_image_path):
            self.show_popup("Ошибка", f"Файл не найден:\n{self.selected_image_path}")
            return
        try:
            n = split_horizontal(self.selected_image_path, self.output_folder_path)
            self.status.text = f"Готово: сохранено плиток — {n}"
            self.show_popup("Успех", f"Создано плиток: {n}\nПапка: {self.output_folder_path}")
        except Exception as e:
            self.status.text = "Ошибка"
            self.show_popup("Ошибка", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.3))
        popup.open()

if __name__ == '__main__':
    MosaicApp().run()
