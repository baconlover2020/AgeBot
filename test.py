import shutil
import os

pasta_categorias = "temp_categorias"
for categoria in os.listdir(pasta_categorias):
    shutil.unpack_archive(os.path.join(pasta_categorias,categoria), pasta_categorias)
    os.remove(os.path.join(pasta_categorias,categoria))