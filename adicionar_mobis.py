import mobi
import sys
import os
import painel

categorias = sys.argv[1:]
swfs_path = ''
icons_path = ''
painel.login()
def adicionar_categoria(categoria):
    id_pagina = painel.get_id()
    painel.adicionar_pagina(id_pagina, categoria.split('\\')[-1])
    for pasta in os.listdir(categoria):
        if pasta.lower() == 'swf' or pasta.lower() == 'swfs':
            swfs_path = os.path.abspath(os.path.join(categoria, pasta))
        if pasta.lower() == 'icon' or pasta.lower() == 'icons':
            icons_path = os.path.abspath(os.path.join(categoria, pasta))
    for swf in os.listdir(swfs_path):
        swf_path = os.path.join(swfs_path, swf)
        icon_path = os.path.join(icons_path, swf.replace('.swf', '_icon.png'))
        item_id = painel.get_id()
        classname = painel.get_classname(os.path.join(swf_path, swf))
        nome = painel.criar_nome(classname)
        description = "Categoria: " + categoria.split('\\')[-1]
        furniture = mobi.Furniture(id=item_id)
        catalalog = mobi.Catalog(id_pagina, item_id=item_id)
        mobi1 = mobi.Mobi(swf_path, icon_path, item_id, classname, nome, description, furniture, catalalog)
        mobi1.add()

for categoria in categorias:
    adicionar_categoria(categoria)



#input()


