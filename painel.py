import requests
import os
import urllib.parse
import shutil
import google_trans_new

if not os.path.exists('painel_ids.txt'):
    with open('painel_ids.txt', 'w+') as f:
        f.write('3535000')


def get_id():
    with open('painel_ids.txt', 'r') as f:
        _id = f.readline()
        new_id = int(_id) + 1
        with open('painel_ids.txt', 'w+') as w:
            w.write(str(new_id))
        return _id


def get_classname(swf_path):
    swf_path = swf_path.replace('\\', '/')
    return swf_path.split('/')[-1].replace('.swf', '').replace('_icon.png', '')


with requests.Session() as session:
    def login():
            print('---------- Inicializando painelway ----------')
            credenciais = {'i': 'Martinhamiguelangelo9',
                           'd': 'martinha123'}
            session.get('http://setoradministrativo.agehotel.info/login.php?securitysystem=AndersonAge')
            session.post('http://setoradministrativo.agehotel.info/login.php', data=credenciais)
            session.post('http://setoradministrativo.agehotel.info/pin.php', data={'pin': '154236'})
            print('Painel iniciado com sucesso.')
        
    def adicionar_pagina(id_pagina, nome_pagina, parent_id='4242000', icon_image='10'):
            print('Criando categoria no catalogo com ID: '+str(id_pagina)+' e nome: '+nome_pagina)
            pagina = {
            'id[]': id_pagina,
            'parent_id[]': parent_id,
            'type[]': 'DEFAULT',
            'caption[]': nome_pagina,
            'icon_color[]': '1',
            'icon_image[]': '10',
            'visible[]': '1',
            'enabled[]': '1',
            'min_rank[]': '1',
            'club_only[]': '0',
            'order_num[]': '1',
            'page_layout[]': 'default_3x3',
            'page_images[]': '[]',
            'page_texts[]': '[]',
            'min_sub[]': '0',
            'vip_only[]':'0',
            'link[]': 'undefined',
            'extra_data[]': ''}
            session.post('http://setoradministrativo.agehotel.info/index.php?page=add-catalog-pages', data=pagina)
            print('Categoria '+ nome_pagina +' criada com sucesso.')
            return nome_pagina

    def adicionar_icon(icon_path):
        icon_path = icon_path.replace('\\', '/').replace('"','')
        try:
            files = {'userfile[]': open(icon_path, 'rb')}
            session.post('http://setoradministrativo.agehotel.info/salvar_icon_catalogue.php', files=files)
            print(icon_path.split('/')[-1] +' foi hospedado.')
            return icon_path.split('/')[-1]
        except:
            print(f"Nao foi possivel encontrar o icon {icon_path}")

    def adicionar_icons(icons_path):
        icons_path = icons_path.replace('\\','/').replace('"','')
        print('---------- Hospedando Icones ----------')
        for icon in os.listdir(icons_path):
            adicionar_icon(os.path.join(icons_path,icon))
        print("Todos os icones foram hospedados.")
        

    def adicionar_swf(swf_path):
        swf_path = swf_path.replace('\\','/').replace('"','')
        files = {'userfile[]': open(swf_path, 'rb')}
        session.post('http://setoradministrativo.agehotel.info/salvar_swf2.php',files=files)
        print(swf_path.split('/')[-1] +' foi hospedado.')
        return swf_path.split('/')[-1]

    def adicionar_swfs(swfs_path):
        print('Hospedando SWF')
        for swf in os.listdir(swfs_path):
            adicionar_swf(os.path.join(swfs_path,swf))
        print('Todas SWFs da pasta foram hospedada')

    def criar_furnidata(classname, nome, descrição, _id=get_id()):
        return f"<furnitype id=\"{str(_id)}\" classname=\"{classname}\">\n<revision>500008</revision> \n<defaultdir>0</defaultdir> \n<xdim>1</xdim> <ydim>1</ydim> \n<partcolors> <color>0</color> \n<color>0</color> <color>0</color> \n</partcolors> <name>{nome}</name> \n<description>{descrição}</description> \n<adurl/> <offerid>-1</offerid> <buyout>0</buyout> \n<rentofferid>0</rentofferid> <rentbuyout>0</rentbuyout> \n<bc>0</bc> <excludeddynamic>0</excludeddynamic> <customparams/> <specialtype>1</specialtype> \n<canstandon>0</canstandon> <cansiton>0</cansiton> <canlayon>0</canlayon> </furnitype> \n"

    def criar_furnidatas(swf_path, categoria):
        print(f'---------- Criando furnidata para {categoria} ----------')
        furnidata = ''
        for c, swf in enumerate(os.listdir(swf_path), int(get_id())):
            furnidata += criar_furnidata(swf.replace('.swf', ''), criar_nome(swf), categoria)
        return furnidata

    def criar_nome(nome):
        nome = nome.replace('.swf','').lower()
        inverter = ['habbox','habblet','habbo','habb','hab']
        for coisa in inverter:
            if coisa in nome:
                nome = nome.replace(coisa,'###')
        nome = nome.replace('_', ' ')
        palavras = nome.split(' ')
        resultado  = ''
        for palavra in palavras:
            if not palavra[-1].isnumeric() and not palavra == ' ':
                resultado += palavra.capitalize() + ' '
        translator = google_trans_new.google_translator()
        resultado = translator.translate(resultado, lang_src='en' ,lang_tgt='pt')
        if type(resultado) == type([]):
            resultado = resultado[0]
        return resultado.replace('###', 'Age')

    def adicionar_furnidata(furnidata):
        data = {'furnitype': furnidata}
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-roomwcampo&table=room', data=data)
        print('Furnidata adicionado com sucesso:\n'+furnidata)
        return furnidata

    def adicionar_furniture(_id, public_name='steinlindo', item_name='steinlindo', _type='s' , width='1', length='1', stack_heigth='0', can_stack='1', can_sit='0', is_walkable='0',
                            sprite_id='', interaction_type='default', interaction_modes_count='10', vending_ids='0',
                            effect_id='0', variable_heights='0', song_id='0'):
        if sprite_id == '':
            sprite_id = _id
        furniture = {'id[]': _id, 'public_name[]': public_name, 'item_name[]': item_name, 'type[]': _type,
                     'width[]': width, 'length[]': length, 'stack_height[]': stack_heigth, 'can_stack[]': can_stack,
                     'can_sit[]': can_sit, 'is_walkable[]': is_walkable,'sprite_id[]': sprite_id,
                     'allow_recycle[]': '1', 'allow_trade[]': '1', 'allow_marketplace_sell[]': '1',
                     'allow_gift_back[]': '1', 'allow_gift[]': '1', 'allow_inventory_stack[]': '1',
                     'interaction_type[]': interaction_type, 'interaction_modes_count[]': interaction_modes_count,
                     'vending_ids[]': vending_ids, 'is_arrow[]': '0', 'foot_figure[]': '0', 'stack_multiplier[]': '0',
                     'subscriber[]': '0', 'effect_id[]': effect_id, 'variable_heights[]': variable_heights, 'flat_id[]': '-1', 'revision[]': '49500',
                     'description[]': 'Age', 'specialtype[]': '1', 'canlayon[]': '0', 'requires_rights[]': '1',
                     'song_id[]': song_id, 'date[]': '2020-10-04 19:31:41'}

        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-furniture', data=furniture)
        print(f"SQL adicionado: id:{_id} sprite_id:{sprite_id}")
        return furniture

    def adicionar_furnitures(swf_path, id_inicial):
        for _id, swf in enumerate(os.listdir(swf_path), id_inicial):
            adicionar_furniture(_id)
            print(swf.replace('.swf','') + ' adicionado ao furniture.')
        print('Todos os mobis foram adicionados ao furniture')

    def adicionar_catalogo(page_id, item_id='', catalog_name='', cost_credits='0', amount='1', song_id='0',
                 limited_sells='0', extradata='', badge_id='', cost_diamonds='0'):
        catalogo = {'page_id[]': page_id,
            'item_ids[]': item_id,
            'catalog_name[]': catalog_name,
            'cost_credits[]': cost_credits,
            'cost_snow[]': '0',
            'cost_pixels[]': '0',
            'amount[]': amount,
            'vip[]': '0',
            'achievement[]': '0',
            'song_id[]': song_id,
            'limited_sells[]': limited_sells,
            'limited_stack[]': '0',
            'offer_active[]': '1',
            'extraData[]': extradata,
            'badge_id[]': badge_id,
            'flat_id[]': '-1',
            'date[]': '2020-10-04 22:00:39',
            'cost_seasonal[]': '0',
            'cost_diamonds[]': cost_diamonds}
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-catalog-items', data=catalogo)
        print(f"ID {item_id} adicionado a pagina {page_id} com nome {catalog_name}")
        return catalogo

    def adicionar_catalogos(swf_path, id_pagina, nome_pagina, id_inicial, cost_credits='0', cost_diamonds='0'):
        for _id, swf in enumerate(os.listdir(swf_path), id_inicial):
            adicionar_catalogo(id_pagina, nome_pagina, _id, cost_credits, cost_diamonds)
            #print(swf + ' adicionado ao catalogo na pagina '+ nome_pagina)
        print('Todos os mobis foram adicionados ao catalogo')

    def hospedar_emblema1(url, título, descrição, código):
        if not url.startswith('http'):
            return

        response = requests.get(url, stream=True)
        with open('emblemas/'+código+'.gif', 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        files = {'userfile[]': open('emblemas/'+código+'.gif', 'rb')}
        session.post('http://setoradministrativo.agehotel.info/salvar_emblem.php', files=files)
        del response
        session.get('http://setoradministrativo.agehotel.info/index.php?page=badge_name&i%5B%5D='+urllib.parse.quote(código)+'&d%5B%5D='+urllib.parse.quote(título))
        session.get('http://setoradministrativo.agehotel.info/index.php?page=badge_desc&i%5B%5D='+urllib.parse.quote(código)+'&d%5B%5D='+urllib.parse.quote(descrição.replace('"','')))
        print('O emblema com código '+código+' foi hospedado com o nome '+título+' e descrição '+ descrição.replace('"',''))

    def gif_path(url, código):
        if not url.startswith('http'):
            return
        response = requests.get(url, stream=True)
        with open('emblemas/'+código+'.gif', 'wb') as f:
            shutil.copyfileobj(response.raw, f)
            del response
            return 'emblemas/'+código+'.gif'

    def hospedar_emblema(gif_path, código, título, descrição):
        hospedar_gif(gif_path)
        hospedar_nome(código, título)
        hospedar_desc(código, descrição)
        print('O emblema com código "'+código+'" foi hospedado com o nome "'+título+'" e descrição "'+ descrição.replace('"','')+'"')
        
    def hospedar_gif(gif_path):
        gif_path = gif_path.replace('\\','/')
        files = {'userfile[]':open(gif_path, 'rb')}
        session.post('http://setoradministrativo.agehotel.info/salvar_emblem.php', files=files)
        return gif_path.split('/')[-1] + ' foi hospedado'

    def hospedar_nome(código, título):
        session.get('http://setoradministrativo.agehotel.info/index.php?page=badge_name&i%5B%5D='+urllib.parse.quote(código)+'&d%5B%5D='+urllib.parse.quote(título))
        return 'O nome ' + título + ' foi adicionado ao código ' + código

    def hospedar_desc(código, descrição):
        session.get('http://setoradministrativo.agehotel.info/index.php?page=badge_desc&i%5B%5D='+urllib.parse.quote(código)+'&d%5B%5D='+urllib.parse.quote(descrição.replace('"','')))
        return 'A descrição ' + descrição + ' foi adicionado ao código ' + código


    def adicionar_music_furni(nome_arquivo, nome_música, artista, song_data):
        musica = {
            'name[]': nome_arquivo,
            'title[]': nome_música,
            'artist[]': artista,
            'song_data[]': song_data,
            'length[]': str(song_data)[-3:]
        }
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-furniture_music', data=musica)
        print('Uma nova musica foi adicionada ao music_furni com os parametros: ' + nome_arquivo + ' ' + song_data)
    
    def hospedar_mp3(mp3):
        musica = {'userfile': open(mp3, 'rb')}
        r = session.post('http://setoradministrativo.agehotel.info/salvar_mp3.php', files=musica)
        print(r.text)
    

    def adicionar_musica(mp3, song_data, nome_arquivo, nome_música, artista, song_id, _id):
        hospedar_mp3(mp3)
        adicionar_music_furni(nome_arquivo, nome_música, artista, song_data)
        adicionar_furniture(_id, stack_heigth='0.1', sprite_id='2319', interaction_type='musicdisc', interaction_modes_count='2', song_id=song_id)
        adicionar_catalogo(4206900, nome_música + ' - ' + artista, _id, song_id=song_id, extradata=nome_arquivo)

    def alterar_jogador(nome, moedas='0', diamantes='0', duckets='0'):
         session.get('http://setoradministrativo.agehotel.info/index.php?page=send_send&i=' + str(nome) +'&m='+ str(moedas)+'&di='+ str(diamantes)+'&du='+ str(duckets))


    def adicionar_mobi(swf_path, icon_path, _id, classname, nome, descrição, id_pagina, width='1', length='1', stack_heigth='0', can_stack='0', can_sit='0', is_walkable='0', sprite_id='default', interaction_type='default', interaction_modes_count='10', vending_ids='0', cost_credits='0', cost_diamonds='0', song_id='0', extra_data=''):
        adicionar_swf(swf_path.replace('\\', '/').replace('"', ''))
        adicionar_icon(icon_path.replace('\\', '/').replace('"', ''))
        adicionar_furnidata(criar_furnidata(_id, classname, nome, descrição))
        adicionar_furniture(_id, width=width, length=length, stack_heigth=stack_heigth, can_stack=can_stack, can_sit=can_sit, is_walkable=is_walkable, sprite_id=sprite_id, interaction_type=interaction_type, interaction_modes_count=interaction_modes_count, vending_ids=vending_ids)
        adicionar_catalogo(id_pagina, nome, _id, cost_credits=cost_credits, cost_diamonds=cost_diamonds, extradata=extra_data)
        
    