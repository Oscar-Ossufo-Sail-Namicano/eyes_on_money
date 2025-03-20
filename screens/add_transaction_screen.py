from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window
from database import Database
from kivy.lang import Builder


Builder.load_file('./kv/add_transaction_screen.kv')

class AddTransactionScreen(Screen):
    type_spinner = ObjectProperty(None)
    category_spinner = ObjectProperty(None)
    amount_input = ObjectProperty(None)
    date_input = ObjectProperty(None)
    description_input = ObjectProperty(None)
    spent_categories = []
    income_categories = []


    def on_pre_enter(self, *args):
        self.income_categories.clear()
        self.spent_categories.clear()
        db = Database()
        user_id = self.manager.get_screen('login').user_id
        for category in list(db.get_transactions_categories(user_id, transaction_type='Despesa')):
            #
            self.spent_categories.append(str(category[0]))
        
        for category in list(db.get_transactions_categories(user_id, transaction_type='Receita')):
            #
            self.income_categories.append(str(category[0]))

    
    def add_transaction(self):
        if  self.amount_input.text == '':
            self.ids.error_label.text = 'O montante nao pode ser vazio'
            return
        
        elif  self.date_input.text == '':
            self.ids.error_label.text = 'Inique a data que efectuou este movimento'
            return
        
        elif self.type_spinner.text == 'Tipo':
            self.ids.error_label.text = "Selecione o tipo de transacao no campo 'Tipo'"
            return
        
        elif self.category_spinner.text == 'Categoria':
            self.ids.error_label.text = "Selecione a categoria desta transacao no campo 'Categoria'"
            return
        
        else:
            # it means the user gave all information

            if self.type_spinner.text == 'Despesa':
                # chacking if the category selected belongs to the type of the choosen transaction
                if self.category_spinner.text in self.spent_categories:
                    pass
                else:
                    self.ids.error_label.text = "A categoria selecionada ee do tipo Despesa e nao Receita"
                    return  
                
            elif self.type_spinner.text == 'Receita':
                # chacking if the category selected belongs to the type of the choosen transaction
                if self.category_spinner.text in self.income_categories:
                    pass
                else:
                    self.ids.error_label.text = "A categoria selecionada ee do tipo Receita e nao Despesa"
                    return 
                
        # Trablho futuro ee adicionar o tratamento de erros para o caso de incopatibilidade
        # entre o tipo de transacao e a categoria
        #
        
        db = Database()
        user_id = self.manager.get_screen('login').user_id  # Implemente isso no LoginScreen
        type = self.type_spinner.text
        category = self.category_spinner.text
        amount = float(self.amount_input.text)
        date = self.date_input.text
        description = self.description_input.text
        db.add_transaction(user_id, type, category, amount, date, description)
        db.close()
        self.manager.current = 'main'

    def get_date(self, instance, value, date_range):
        '''
        :type date: <class 'datetime.date'>
        
        Método chamado quando uma data é selecionada.
        :param instance: Instância do MDDatePicker
        :param value: Data selecionada (datetime.date)
        :param date_range: Lista de datas se um intervalo for selecionado
        '''
        self.date_input.text = value.strftime("%d/%m/%Y")  # Formata a data para o formato dd/mm/aaaa

    def show_date_picker(self):
        """
        This method is prided by kivimd
        your don't need to write it manualy
        Just copy and paste from the site packages folder
        """
        
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date)  # Vincula o evento on_save ao método get_date
        date_dialog.open()
        wind_width = Window.width
        Window.size = (Window.width * .999999, Window.height * 1)
        Window.size = (wind_width , Window.height * 1)


