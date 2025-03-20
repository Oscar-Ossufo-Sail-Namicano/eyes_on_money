from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from database import Database
from kivy.lang import Builder


Builder.load_file('./kv/main_screen.kv')
class MainScreen(Screen):
    balance_label = ObjectProperty(None)
    income_label = ObjectProperty(None)
    expense_label = ObjectProperty(None)
    username_label = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update_summary()
        username_label = self.manager.get_screen('login').username.text
        self.username_label.text = username_label


    def update_summary(self):
        db = Database()
        user_id = self.manager.get_screen('login').user_id  # Implemente isso no LoginScreen
        transactions = db.get_transactions(user_id)
        income = sum(t[4] for t in transactions if t[2] == 'Receita') # t[4] icorresponds to amount in trasactions table
        expense = sum(t[4] for t in transactions if t[2] == 'Despesa')
        self.income_label.text = f"Receitas:\nR$ {income:.2f}"
        self.expense_label.text = f"Despesas:\nR$ {expense:.2f}"
        self.balance_label.text = f"Saldo: R$ {income - expense:.2f}"
        db.close()
