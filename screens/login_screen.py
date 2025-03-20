from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty
from database import Database
from kivy.lang import Builder


Builder.load_file('./kv/login_screen.kv')
class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    user_id = NumericProperty(None)

    # Default settigns are set in this screen
    default_spent_categories = ['Alimentação', 'Transporte', 'Lazer', 'Outros']
    default_income_categories = ['Nhonga', 'Taxi', 'Putaria', 'Barbearia']

    def do_login(self):
        db = Database()
        user_id = db.get_user(self.username.text, self.password.text)
        if user_id:
            self.user_id = user_id[0]
            self.manager.current = 'main'
        else:
            self.ids.error_label.text = "Usuário ou senha incorretos"
        db.close()

    def create_account(self):
        db = Database()
        if db.add_user(self.username.text, self.password.text):
            self.user_id = db.get_user(self.username.text, self.password.text)[0] # This is like a section that hold the user id for internal use

            # Creating default categories for the new user:
            income_type = 'Receita'
            spent_type = 'Despesa'
            for income_category in self.default_income_categories:
                db.add_transaction_categories(self.user_id, income_type, income_category)

            for spent_category in self.default_spent_categories:
                db.add_transaction_categories(self.user_id, spent_type, spent_category)

            self.manager.current = 'main'
        else:
            self.ids.error_label.text = "Nome de usuário já existe"
        db.close()