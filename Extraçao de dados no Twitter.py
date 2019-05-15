from tweepy import *
from pandas import DataFrame
from textblob import TextBlob
from matplotlib.pyplot import *
import numpy as np

def twitter():

    auth = OAuthHandler('RIvAic3yDT8qxHKT4NymRQ275', 'MnKzqdrUKjFM4kMHueLeJhwgC9BIqo3p1cT86u2Tgv3ZzqkHCp')
    auth.set_access_token('73785515-UEoT86lpEHin4a8h4gleH6fOjvPJRWNO9xoV0Rpej', 'xUYRBW7rJ8QiZtQ0tc9HOHu05IGez5CLPCTJwOdyfDBP7')

    '''
    try:
        usuario = input("Informe o usuario: ")
    except TweepError:
        print(TweepError.message[0]['code'])
    '''
    op = 'n'
    usuario = input("Informe o usuario: ")
    api = API(auth)
    user = api.get_user(usuario)

    def usuario_novo(): #Funçao para novo usuario
        usuario = input("Informe o usuario: ")
        user = api.get_user(usuario)
        print("Nome do usuario: ", user.name, "\n")
        return usuario

    def infor(user): #Informações do usuario atual
        print("Seguindo: ", user.friends_count)  # Quantas pessoas ele/a segue
        print("Seguidores: ", user.followers_count)  # Quantas pessoas seguem ele/a
        print("Localização do usuario: ", user.location)  # Local do perfil
        print("Linguagem do usuario:", user.lang)  # linguagem do usuario
        print('foto do usuario:', user.profile_image_url)  # foto de perfil
        print("\n")
        op = input("Finalizar? (s) ou (n) \n")
        return op

    def amigos(user): #Informa lista de amigos do usuario e suas respectivas informaçoes
        for friend in user.followers(): #lista de amigos do usuario
            print("nome de usuario: ",friend.screen_name, "\n nome no perfil: ",friend.name) #amigo do usuario
            print("Seguidores: ",friend.followers_count) #Numero de seguidores do amigo
            print("Seguindo: ", friend.friends_count)  # Quantas pessoas ele/a segue
        op = input("Finalizar? (s) ou (n) \n")
        return op

    def publica(user): #Informa as publicações do usuario
        analysis = None

        tweets_publicos = api.user_timeline(user_id = user.id, count=10, page=1)# Publicações da timeline publica do usuario inserido
        for tweet in tweets_publicos:
            frase = TextBlob(tweet.text)
            if frase.detect_language() != 'en':
                traducao = TextBlob(str(frase.translate(to='en')))
                print('Autor: {0} Tweet: {1} - Sentimento: {2}'.format(tweet.author.name,tweet.text, traducao.sentiment.polarity))
            else:
                print('Tweet: {0} - Sentimento: {1}'.format(tweet.text, frase.sentiment.polarity))
        op = input("Finalizar? (s) ou (n) \n")
        return op

    def pesquica(): #Realiza pesquisa sobre o tema referente e mostra usuarios
        pesquica_input = input("pesquisar sobre : ")
        resultados = []
        usuarios = []
        sentimentos = []
        num = 0

        for tweet in Cursor(api.search, q=pesquica_input).items(10):
            #print(tweet.text, '\n')
            analysis = TextBlob(tweet.text)
            resultados.append(tweet)

            usuarios.append(tweet.author.name)
            sentimentos.append(analysis.sentiment.polarity)


        def process_results(resultados):
            id_list = [tweet.id for tweet in resultados]
            lista = DataFrame(id_list, columns=["id"])

            # lista["ID"] = [tweet.author.id for tweet in results]
            # lista["descrição"] = [tweet.author.description for tweet in resultados]
            lista["Usuario"] = [tweet.author.name for tweet in resultados]
            #lista["seguindo"] = [tweet.author.followers_count for tweet in resultados]
            #lista["seguidores"] = [tweet.author.friends_count for tweet in resultados]
            lista["texto"] = [tweet.text for tweet in resultados]
            lista["localização"] = [tweet.author.location for tweet in resultados]
            lista["Sentimentos"] = analysis.sentiment.polarity


            return lista
        lista = process_results(resultados)
        print(lista.head())
        y_axis = sentimentos
        x_axis = range(len(lista))
        bar(x_axis, y_axis, color='orange')

        show()

        op = input("Finalizar? (s) ou (n) \n")
        return op

    print("Nome do usuario: ", user.name,"\n") #Imprime o nome do usuario

    while op == 'n' or op == 'N':
        selec = input("O que deseja fazer? \n ver publicações (publica) \n ver amigos (amigos) \n ver informações (infor) \n Pesquisar sobre tema (pesquisa) \n Novo usuario (user) \n Finalizar (s) \n")
        if selec == 'publica': #Se selecionada a opçao de Publicações do usuario atual
            op = publica(user)
        elif selec == 'amigos':#Se selecionada a opçao de Amigos do usuario atual
            op = amigos(user)
        elif selec == 'infor':#Se selecionada a opçao de Informações do usuario atual
            op = infor(user)
        elif selec == 'user': #Usado para alterar o usuario atual
            usuario = usuario_novo()
            user = api.get_user(usuario)
        elif selec == "pesquisa": #Se selecionada a opção realizar pesquisa
            op = pesquica()
        elif selec == 's' or op == 's':#Se selecionada a opção Finalizar
            break
        else:
            print("Opção Invalida \n")
            continue

    return 0


rede = input("Qual rede social deseja buscar: \n (twitter)")

if rede == 'twitter':
    twitter()
else:
    print("rede invalida ou inexistente")
