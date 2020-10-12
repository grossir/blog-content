import tika
from tika import unpack
import requests
import os
import re

try:
    # NOTE: paquete personal
    from datautils import tika_utils
    tika_utils.start_tika()
except:
    pass



DIRNAME = os.path.dirname(os.path.abspath(__file__))

r = requests.get("http://www.minem.gob.pe/minem/archivos/file/DGAAM/mapas/minas_abandonadas/cusco/map_Cusc.pdf")
filepath = F"{DIRNAME}/src_pdfs/minas_abandonadas_cusco.pdf"
with open(filepath, "wb") as F:
    F.write(r.content)


x = tika.unpack.from_file(filepath)

ejemplo = x['content'].split('MINA INACTIVA', 1)[1].split("Nombre de Mina")[1]
ejemplo2 = x['content'].split('MINA INACTIVA', 1)[1].split("Nombre de Mina")[3]

# NOTE: revisar imagen
with open('tmp.jpg', 'wb') as F:
    F.write(x['attachments']['image86.jpg'])


REGEX_IMG_PATH = re.compile("image[0-9]+\\.jpg")
sorted(re.findall(REGEX_IMG_PATH, ejemplo))
sorted(re.findall(REGEX_IMG_PATH, ejemplo2))


fields = [
    'Código',
    'Nombre del Titular',
    'Año de Abandono',
    'Departamento',
    'Cuenca',
    'Acceso',
    'Ubicación',
    'Norte',
    'Este',
    'Zona',
    'Altitud',
    'Geología',
    'Mineralogía',
    'Geomorfología',
    'Hidrología',
    'Desmonte',
    'Depósito Relaves',
    'Contaminación',
    'Observaciones',
]

exclude_img_name = {"image85.jpg", "image87.jpg"}
structured_data = []

for txt_mina in x['content'].split('MINA INACTIVA', 1)[1].split("Nombre de Mina")[1:]:
    new_mine = {'Nombre de Mina': txt_mina.split("Có")[0].strip(" :")}

    for index, field in enumerate(fields):
        next_field = fields[index + 1] if index != len(fields) - 1 else 'MINA INACTIVA'
        new_mine[field] = " ".join(txt_mina.split(field)[1].split(next_field)[0].split(None)).strip(": ")
    
    img_name = set(re.findall(REGEX_IMG_PATH, txt_mina)).difference(exclude_img_name)
    new_mine['img_binary'] = x['attachments'][img_name.pop()]
    
    structured_data.append(new_mine)