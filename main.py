from kivy import platform
import sys
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.main_screen import MainScreen
from screens.add_transaction_screen import AddTransactionScreen
from screens.history_screen import HistoryScreen
from screens.reports_screen import ReportsScreen
from screens.settings_screen import SettingsScreen
from kivy.core.window import Window
from database import Database

#Window.size = (350, 600)

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
    
class FinanceTrackerApp(MDApp):
    def build(self):
        #self.theme_cls.theme_style="Dark"
        self.db = Database()
        self.sm = ScreenManager()
        
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(AddTransactionScreen(name='add_transaction'))
        self.sm.add_widget(HistoryScreen(name='history'))
        self.sm.add_widget(ReportsScreen(name='reports'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        return self.sm
    
    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            if not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def on_stop(self):
        self.db.close()

    
    def go_home(self):
        self.sm.current='main'

if __name__ == '__main__':
    FinanceTrackerApp().run()
