from database import Database
import functools
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('./kv/history_screen.kv')

class HistoryScreen(Screen):
    transactions_list = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update_history()

    def update_history(self):
        db = Database()
        user_id = self.manager.get_screen('login').user_id  # Implemente isso no LoginScreen
        transactions = db.get_transactions(user_id)
        self.transactions_list.clear_widgets()

        for transaction in transactions:
            transaction_id = transaction[0]

            # Criando um BoxLayout para a linha da transação
            transaction_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=80,  # Ajustado para acomodar ThreeLineListItem
                padding=[10, 5],
                spacing=10
            )

            # ThreeLineListItem para exibir os detalhes da transação
            transaction_label = ThreeLineListItem(
                text=f"{transaction[2]}: {transaction[5]}",  # Título principal: Tipo de transacao
                secondary_text=f"Categoria: {transaction[3]}",  # Segunda linha
                tertiary_text=f"Montante: {transaction[4]}",  # Terceira linha
                size_hint_x=0.7,
                size_hint_y=None,
                height=50
            )

            # Layout para os botões (Edição e Exclusão)
            buttons_layout = BoxLayout(
                orientation='horizontal',
                size_hint_x=0.3,
                spacing=10,
                height=50
            )

            edit_btn = MDIconButton(icon='pencil', size_hint=(None, None), size=(40, 40), pos_hint = {'center_x': .5, 'center_y': .5})
            delete_btn = MDIconButton(icon='delete', size_hint=(None, None), size=(40, 40), pos_hint = {'center_x': .5, 'center_y': .5})
            
            delete_btn.bind(on_release=functools.partial(self.delete_user_transaction, transaction_id))
            edit_btn.bind(on_release=functools.partial(self.update_user_transaction))

            buttons_layout.add_widget(edit_btn)
            buttons_layout.add_widget(delete_btn)

            # Adicionando os widgets ao layout principal
            transaction_box.add_widget(transaction_label)
            transaction_box.add_widget(buttons_layout)

            self.transactions_list.add_widget(transaction_box)

        db.close()

    def delete_user_transaction(self, transaction_id, instance):
        db = Database()
        user_id = self.manager.get_screen('login').user_id
        db.delete_transaction(user_id, transaction_id)
        self.transactions_list.remove_widget(instance.parent.parent)
        db.close()
    
    def update_user_transaction(self, instance):
        """
        Here we have a popup to hold the button
        while we develop the functionality if editing the transaction
        """
        
        
        okay_btn = MDFlatButton(text='Okay', on_release=self.close_dialog)
        self.dialog = MDDialog(title='Info.:', text=f'Esta funcionalidade esta em desenvolvimento\nContcte o programador Oscar Namicano para mais info\nou aguarde ate ser desenvolvida', buttons=[okay_btn])
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()




        