from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
#import matplotlib.pyplot as plt
#from io import BytesIO
#import base64
from database import Database
from kivy.lang import Builder
#Thirtyparty libraries
from kivy_charts.pie_chart import PieChart


Builder.load_file('./kv/reports_screen.kv')

class ReportsScreen(Screen):
    spents_report_image = ObjectProperty(None)
    incomes_report_image = ObjectProperty(None)

    def on_pre_enter(self, *args):         
        self.spents_report_image.clear_widgets()
        self.incomes_report_image.clear_widgets()
        self.generate_report(transaction_type='Despesa')
        self.generate_report(transaction_type='Receita')


    def generate_report(self, transaction_type):
        db = Database()
        user_id = self.manager.get_screen('login').user_id  # Implemente isso no LoginScreen
        transactions = db.get_transactions(user_id)
        categories = {}
        for transaction in transactions:
            # We check if the the type of transaction, if it an income or spent
            if transaction[2] == transaction_type:
                # We are taking only the categories of the specified type of transaction
                category = transaction[3]
                amount = transaction[4]
                if category in categories:
                    categories[category] += amount
                else:
                    categories[category] = amount

        '''
        print(categories)
        labels = list(categories.keys())
        values = list(categories.values())

        plt.figure(figsize=(7, 5))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(f'{transaction_type} por Categoria')

        #plt.bar(labels, values, color='blue')
        #plt.figure(figsize=(7, 5))
        #plt.xlabel('Categorias')
        #plt.ylabel('Valor')
        #plt.title(f'{transaction_type} por Categoria')
        

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        '''
        if transaction_type == "Despesa":
            #self.spents_report_image.source = f'data:image/png;base64,{image_base64}'
            #plt.close()
            chart = PieChart(data=categories, colors=['#ff6347', '#4682b4', '#32cd32'], size_hint=(1, 1), percentage_font_size=20, legend_label_font_size=20)
            self.spents_report_image.add_widget(chart)
            db.close()
        elif transaction_type == "Receita":
            #self.incomes_report_image.source = f'data:image/png;base64,{image_base64}'
            #plt.close()
            chart = PieChart(data=categories, colors=['#ff6347', '#4682b4', '#32cd32'], size_hint=(1, 1), percentage_font_size=20, legend_label_font_size=20)
            self.incomes_report_image.add_widget(chart)
            db.close()

        
