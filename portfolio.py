import requests
from tkinter import *
import pandas as pd
from datetime import datetime
import os

class Aplicacao:
    def __init__(self):
        self.layout = Tk()
        self.layout.title("Clima São Paulo")
        self.layout.geometry("350x200")

        self.tela = Frame(self.layout)

        self.descricao = Label(self.tela, text='Buscar temperatura em São Paulo:')
        self.buscar = Button(self.tela, text='Buscar', command=self.buscar_temp)
        self.resultado = Label(self.tela, text='', font=('Arial', 12))

        self.tela.pack()
        self.descricao.pack(pady=5)
        self.buscar.pack(pady=5)
        self.resultado.pack(pady=10)

        mainloop()

    def buscar_temp(self):
        api_key = '1e9f218933860d7cfe513218b2df2b16'
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao%20Paulo,BR&appid={api_key}&units=metric&lang=pt_br'

        try:
            resposta = requests.get(url)
            dados = resposta.json()

            if resposta.status_code == 200:
                temp = dados['main']['temp']
                umidade = dados['main']['humidity']
                clima_desc = dados['weather'][0]['description']

                status_umidade = self.classificar_umidade(umidade)
                data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                # Exibir resultado na interface
                self.resultado.config(text=f'Temp: {temp}°C\nUmidade: {umidade}% ({status_umidade})\n{clima_desc}')

                # Salvar no arquivo CSV
                self.salvar_dados(data_hora, temp, status_umidade)

            else:
                erro_api = dados.get("message", "Erro desconhecido")
                self.resultado.config(text=f'Erro: {erro_api}')
        except Exception as e:
            self.resultado.config(text=f'Erro: {str(e)}')

    def classificar_umidade(self, umidade):
        if umidade < 30:
            return 'Baixa'
        elif 30 <= umidade <= 60:
            return 'Ideal'
        else:
            return 'Alta'

    def salvar_dados(self, data_hora, temp, status_umidade):
        arquivo = 'dados_clima.csv'
        nova_linha = {'Data/Hora': data_hora, 'Temperatura (°C)': temp, 'Status Umidade': status_umidade}

        if os.path.exists(arquivo):
            df = pd.read_csv(arquivo)
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        else:
            df = pd.DataFrame([nova_linha])

        df.to_csv(arquivo, index=False)

tl = Aplicacao()