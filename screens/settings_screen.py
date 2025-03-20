import sqlite3
from database import Database
import pandas as pd
import os
import sys

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder


Builder.load_file('./kv/settings_screen.kv')

if 'android' in sys.modules:
    from android.permissions import request_permissions, Permission, check_permission
    from android.storage import primary_external_storage_path

    def request_storage_permissions():
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    import os

    def get_files_directory():
        files_dir = f'{str(primary_external_storage_path())}/Finance Track/'
        # Verifica se o diretório existe, caso contrário, cria
        if not os.path.exists(files_dir):
            request_storage_permissions()
            os.makedirs(files_dir)
        return files_dir
else:
    def request_storage_permissions():
        pass  # Não faz nada no desktop
    def get_files_directory():
        p = os.path.expanduser('~')
        print(p)
        return os.path.expanduser('~')

class SettingsScreen(Screen):
    transaction_type = ObjectProperty(None)
    category = ObjectProperty(None)

    def add_category(self):
        db = Database()
        user_id = self.manager.get_screen('login').user_id
        transaction_type = self.transaction_type.text
        category = self.category.text

        db.add_transaction_categories(user_id, transaction_type, category)
        self.manager.current = 'main'
        db.close()
    
    def export_to(self):
        conn = sqlite3.connect('finance.db')
        user_id = self.manager.get_screen('login').user_id
        db = Database()

        nomes_coluna = ['Tipo', 'Categoria', 'Montante', 'Data', 'Descrição']
        
        data = pd.DataFrame(db.get_transaction_to_export(user_id=user_id))

        if data.shape[1] == len(nomes_coluna):  # Verifica se o número de colunas bate com 'nomes_coluna'
            data.columns = nomes_coluna
        
        # Exporta para o Excel
        data.to_excel(os.path.join(get_files_directory(), 'relatorio.xlsx'), sheet_name='escrituração financeira', index=False)

        okay_btn = MDFlatButton(text='Okay', on_release=self.close_dialog)

        self.dialog = MDDialog(title='Info.:', text=f'Escrituracao finaceira salva em {get_files_directory()}', buttons=[okay_btn])
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

