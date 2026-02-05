# -*- coding: utf-8 -*-
"""
TG Mosaic для Android — нарезка картинки на плитки 100×100 для эмодзи в Telegram.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.utils import platform
import os

# Импортируем логику нарезки
from tgmosaic import split_horizontal, TILE_SIZE


class FileChooserPopup(Popup):
    """Попап для выбора файла или папки"""
    def __init__(self, callback, mode='file', **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.mode = mode
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        if mode == 'file':
            from kivy.uix.filechooser import FileChooserListView
            chooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.webp'])
            chooser.bind(on_selection=self.on_file_selected)
        else:
            from kivy.uix.filechooser import FileChooserIconView
            chooser = FileChooserIconView()
            chooser.bind(on_selection=self.on_folder_selected)
        
        layout.add_widget(Label(text='Выберите изображение' if mode == 'file' else 'Выберите папку', size_hint_y=None, height=30))
        layout.add_widget(chooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_cancel = Button(text='Отмена')
        btn_cancel.bind(on_press=lambda x: self.dismiss())
        btn_layout.add_widget(btn_cancel)
        layout.add_widget(btn_layout)
        
        self.content = layout
        self.chooser = chooser
    
    def on_file_selected(self, chooser, selection):
        if selection:
            self.callback(selection[0])
            self.dismiss()
    
    def on_folder_selected(self, chooser, selection):
        if selection:
            self.callback(selection[0])
            self.dismiss()


class TGMosaicApp(App):
    def build(self):
        self.title = 'TG Mosaic'
        
        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Заголовок
        title = Label(
            text='TG Mosaic\nНарезка 100×100 для эмодзи',
            size_hint_y=None,
            height=80,
            font_size=24,
            halign='center'
        )
        title.bind(text_size=title.setter('size'))
        main_layout.add_widget(title)
        
        # Поле изображения
        img_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=80)
        img_layout.add_widget(Label(text='Изображение:', size_hint_y=None, height=25, halign='left'))
        img_row = BoxLayout(spacing=10, size_hint_y=None, height=50)
        self.img_input = TextInput(
            hint_text='Путь к изображению',
            multiline=False,
            size_hint_x=0.7
        )
        img_btn = Button(text='Обзор', size_hint_x=0.3)
        img_btn.bind(on_press=self.choose_image)
        img_row.add_widget(self.img_input)
        img_row.add_widget(img_btn)
        img_layout.add_widget(img_row)
        main_layout.add_widget(img_layout)
        
        # Поле папки
        folder_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=80)
        folder_layout.add_widget(Label(text='Папка для плиток:', size_hint_y=None, height=25, halign='left'))
        folder_row = BoxLayout(spacing=10, size_hint_y=None, height=50)
        self.folder_input = TextInput(
            hint_text='Папка для сохранения',
            multiline=False,
            size_hint_x=0.7
        )
        folder_btn = Button(text='Обзор', size_hint_x=0.3)
        folder_btn.bind(on_press=self.choose_folder)
        folder_row.add_widget(self.folder_input)
        folder_row.add_widget(folder_btn)
        folder_layout.add_widget(folder_row)
        main_layout.add_widget(folder_layout)
        
        # Кнопка нарезки
        self.split_btn = Button(
            text='Нарезать',
            size_hint_y=None,
            height=60,
            font_size=18
        )
        self.split_btn.bind(on_press=self.run_split)
        main_layout.add_widget(self.split_btn)
        
        # Статус
        self.status_label = Label(
            text='Выберите картинку и папку для плиток.',
            size_hint_y=None,
            height=50,
            halign='center',
            color=(0.6, 0.6, 0.6, 1)
        )
        self.status_label.bind(text_size=self.status_label.setter('size'))
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def choose_image(self, instance):
        """Выбор изображения"""
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                from jnius import autoclass, cast
                from android import activity
                from android.activity import ActivityResultListener
                
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                
                def on_permission_result(permissions, results):
                    if all(results):
                        intent = Intent(Intent.ACTION_GET_CONTENT)
                        intent.setType("image/*")
                        currentActivity.startActivityForResult(intent, 1001)
                        self.status_label.text = 'Выберите изображение в файловом менеджере'
                
                request_permissions([Permission.READ_EXTERNAL_STORAGE], on_permission_result)
            except:
                # Fallback: используем текстовое поле
                self.status_label.text = 'Введите путь к файлу вручную (например: /sdcard/Pictures/image.jpg)'
        else:
            popup = FileChooserPopup(
                callback=self.on_image_selected,
                mode='file',
                title='Выберите изображение',
                size_hint=(0.9, 0.9)
            )
            popup.open()
    
    def choose_folder(self, instance):
        """Выбор папки"""
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                
                def on_permission_result(permissions, results):
                    if all(results):
                        # На Android используем стандартную папку Downloads
                        downloads = '/sdcard/Download/tgmosaic_tiles'
                        try:
                            os.makedirs(downloads, exist_ok=True)
                            self.folder_input.text = downloads
                            self.status_label.text = f'Папка: {downloads}'
                        except:
                            # Альтернатива: внутреннее хранилище
                            app_dir = os.path.join(os.path.expanduser('~'), 'tgmosaic_tiles')
                            os.makedirs(app_dir, exist_ok=True)
                            self.folder_input.text = app_dir
                            self.status_label.text = f'Папка: {app_dir}'
                
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE], on_permission_result)
            except:
                # Fallback: используем внутреннее хранилище
                app_dir = os.path.join(os.path.expanduser('~'), 'tgmosaic_tiles')
                os.makedirs(app_dir, exist_ok=True)
                self.folder_input.text = app_dir
                self.status_label.text = f'Папка: {app_dir}'
        else:
            popup = FileChooserPopup(
                callback=self.on_folder_selected,
                mode='folder',
                title='Выберите папку',
                size_hint=(0.9, 0.9)
            )
            popup.open()
    
    def on_image_selected(self, path):
        """Обработка выбранного изображения"""
        self.img_input.text = path
        self.status_label.text = 'Файл выбран. Укажите папку и нажмите «Нарезать».'
    
    def on_folder_selected(self, path):
        """Обработка выбранной папки"""
        self.folder_input.text = path
        self.status_label.text = 'Папка выбрана. Нажмите «Нарезать».'
    
    def run_split(self, instance):
        """Запуск нарезки"""
        path = self.img_input.text.strip()
        folder = self.folder_input.text.strip()
        
        if not path:
            self.show_error('Выберите изображение.')
            return
        
        if not os.path.isfile(path):
            self.show_error(f'Файл не найден:\n{path}')
            return
        
        if not folder:
            self.show_error('Выберите папку для сохранения плиток.')
            return
        
        try:
            self.status_label.text = 'Обработка...'
            self.split_btn.disabled = True
            
            count = split_horizontal(path, folder)
            
            self.status_label.text = f'Готово! Сохранено плиток: {count}'
            self.status_label.color = (0, 0.8, 0, 1)
            
            self.show_success(f'Создано плиток: {count}\nПапка: {folder}')
            
        except Exception as e:
            Logger.exception('Ошибка при нарезке')
            self.status_label.text = 'Ошибка'
            self.status_label.color = (0.8, 0, 0, 1)
            self.show_error(str(e))
        finally:
            self.split_btn.disabled = False
    
    def show_error(self, message):
        """Показ ошибки"""
        popup = Popup(
            title='Ошибка',
            content=Label(text=message, padding=20),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Показ успешного результата"""
        popup = Popup(
            title='Готово',
            content=Label(text=message, padding=20),
            size_hint=(0.8, 0.4)
        )
        popup.open()


if __name__ == '__main__':
    TGMosaicApp().run()
