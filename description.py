#!/usr/bin/env python3
import os

current_dir = os.getcwd()
print(current_dir)
root_folder = current_dir + '/orders' # remplacez cela par le chemin du dossier racine que vous souhaitez parcourir
exclude_list = ['__init__.py', 'description.py', 'manage.py', 'apps.py']
include_list = ['forms.py', 'views.py', 'urls.py', 'admin.py', 'models.py']
for subdir, dirs, files in os.walk(root_folder):
    for file in files:

        if file.endswith(".py") and os.path.basename(file) not in exclude_list and os.path.basename(file) in include_list: # vérifie si le fichier a l'extension .py
            print(file)
            # exit(0)
            filepath = os.path.join(subdir, file)
            with open(filepath, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write("#!/usr/bin/env python3\n") # ajoutez la première ligne de commentaire
                f.write('"""This module is about : {0}\n"""\n'.format(file)) # ajoutez la deuxième ligne de commentaire
                f.write(content)
