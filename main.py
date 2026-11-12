import random
import urllib.parse
import datetime
import time
import json
import requests
import os
import random
from scrapper import avr_prices, avr_prices_by_brand, avr_prices_distritos, avr_price_specific_distrito, avr_prices_concelhos, avr_price_specific_concelho,prices_concelho

def make_url(distrito,concelho):
    ntfy_url = os.environ.get("NTFY_BASE_URL")
    url= f"{ntfy_url}_{distrito}_{concelho}"

    return url

def produce_msg():
    for distrito in os.listdir("contacts"):
        concelhos = json.load(open(f"contacts/{distrito}"))
        distrito=distrito.strip(".json")


        for concelho in concelhos:
            print(f"{distrito}\t{concelho}")

            average_prices, _= avr_prices()
            #average_prices_by_brand, _= avr_prices_by_brand(5)
            #average_prices_distritos, _ = avr_prices_distritos()
            average_price_specific_distrito, _ = avr_price_specific_distrito(distrito)
            #average_prices_concelhos, _ = avr_prices_concelhos(distrito)
            average_price_specific_concelho, _ = avr_price_specific_concelho(distrito, concelho)
            precos_concelho, _ = prices_concelho(distrito, concelho)


            #text_final = f"\n{average_prices_by_brand}\n"
            #send_msg(text_final,distrito,concelho)
            #
            #text_final = f"\n{average_prices_concelhos}\n"
            #send_msg(text_final,distrito,concelho)
            #text_final = f"\n{average_prices_distritos}\n"
            #send_msg(text_final,distrito,concelho)


            text_final = f"\n🚗{precos_concelho}\n"
            send_msg(text_final,distrito,concelho)
            time.sleep(random.randrange(5, 10))

            text_final = f"\n🔵{average_price_specific_concelho}\n"
            #time.sleep(15)
            send_msg(text_final,distrito,concelho)
            time.sleep(random.randrange(5, 10))
            print("Finished concelhos page")

            text_final = f"\n⚪{average_price_specific_distrito}\n"
            #time.sleep(15)
            send_msg(text_final,distrito,concelho)

            time.sleep(random.randrange(5,10))
            print("Finished distritos page")

            text_final = f"\n⚠️{average_prices}\n\n"
            #time.sleep(15)
            send_msg(text_final,distrito,concelho)
            print("Finished main page")
            print("Finished!")

    #return text_final

def daily_update():
    for distrito in os.listdir("contacts"):
        concelhos = json.load(open(f"contacts/{distrito}"))
        distrito=distrito.strip(".json")


        for concelho in concelhos:
            print(f"{distrito}\t{concelho}")

            precos_concelho, _ = prices_concelho(distrito, concelho)



            text_final = f"\n🚗{precos_concelho}\n"
            send_msg(text_final,distrito,concelho)
            time.sleep(random.randrange(5, 10))


            print("Finished! Daily update.")



def send_msg(text_final,distrito,concelho):

        #webhook = concelhos[concelho]["webhook"] #ifttt whatsapp webhook
        #print(webhook)
        #text_final = produce_msg(distrito.strip(".json"), concelho)

        #print(f"sending at: {datetime.datetime.now()}\nto: {nome}")
        #print(len(text_final))

        #headers = {
        #    "Content-Type": "text/plain",
        #}
        #text_norm = urllib.parse.quote_plus(text_final, encoding='utf-8')

        #print(text_final)
        #response = requests.post(f"{webhook}?value1={text_final}") #ifttt whatsapp webhook

        headers = {
            "Content-Type": "text/plain; charset=utf-8",
            #"Title": "Teste",
            "Priority": "low",
            #"Tags": "warning"
        }
        blocos = text_final.split("\n\n")
        buffer=""
        for bloco in blocos[::-1]:
            #print(bloco)



            if len(buffer) > 2900:

                response = requests.post(make_url(distrito,concelho), data=buffer.encode(encoding='utf-8'), headers=headers)
                print(f"Status: {response.status_code}")
                buffer=""
                time.sleep(15)



            buffer += f"{bloco}\n\n"

        final_text = buffer.split("\n\n")
        final_buffer=""

        for bloco in final_text[::-1]:
            final_buffer+=f"{bloco}\n\n"
            #print(final_buffer)

        response = requests.post(make_url(distrito,concelho),data=final_buffer.encode(encoding='utf-8'), headers=headers)

        print(f"Status: {response.status_code}")
        time.sleep(15)


#Using callmebot
'''
def send_buffer(nome,telefone,api_key,text):

    print(urllib.parse.unquote_plus(text, encoding='utf-8'))

    url = f"https://api.callmebot.com/whatsapp.php?phone={telefone}&text={text}&apikey={api_key}"

    try:
        response = requests.get(url)
        print(f"Status: {response.status_code} {response.reason}")
        #print(f"Body: {response.text}")
        if response.status_code == 200:
            print(f"Sucesso: Mensagem enviada para {nome} ({telefone})")


        else:
            print(response.json())
            print(f"Error (Status {response.status_code}) {response.reason}")


            while response.status_code == 210:
                time.sleep(240 * 60)
                try:
                    response = requests.get(url)
                    print(f"Status: {response.status_code} {response.reason}")
                    print(f"Body: {response.text}")
                    if response.status_code == 200:
                        print(f"Sucesso: Mensagem enviada para {nome} ({telefone})")


                    else:
                        print(response.json())
                        print(f"Error (Status {response.status_code}) {response.reason}")

                except Exception as e:
                    print(f"Falha na conexão ao tentar enviar {nome} ({telefone})")
                    # print(e)


    except Exception as e:
        print(f"Falha na conexão ao tentar enviar {nome} ({telefone})")
        #print(e)

    time.sleep(60)

    buffer = ""
def send_msg():

    #https://www.callmebot.com/blog/free-api-whatsapp-messages/

    for distrito in os.listdir("contacts"):
        concelhos = json.load(open(f"contacts/{distrito}"))




        
        #{
        #  "braga" :
        #    {
        #        "nome": "example",
        #        "telefone": "+351",
        #        "apikey": ""
        #    }
        
        #}
        


        for concelho in concelhos:
            nome = concelhos[concelho]["nome"]
            api_key = concelhos[concelho]["apikey"]
            telefone = concelhos[concelho]["telefone"]



            text_final = produce_msg(distrito.strip(".json"),concelho)

            #print(text_final)
            print(f"sending buffer at:{datetime.datetime.now()}")
            text_norm = urllib.parse.quote_plus(text_final)
            buffer=""
            linhas = text_final.split("\n\n")
            #print(len(text_final))

            for linha in linhas:
                buffer += f"\n\n{linha}"
                buffer_parsed = urllib.parse.quote_plus(buffer, encoding='utf-8')

                if len(buffer_parsed) >700:
                    print(len(buffer_parsed))

                    send_buffer(nome,telefone,api_key,buffer_parsed)

                    buffer=""


            #flushout do buffer restante
            buffer_parsed = urllib.parse.quote_plus(buffer, encoding='utf-8')
            send_buffer(nome, telefone, api_key, buffer_parsed)

#16 messages per 240 minutes

#I allow callmebot to send me messages
#+34 694 25 79 52

'''

if __name__ == '__main__':
    produce_msg()
