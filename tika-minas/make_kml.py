from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pykml.factory import ATOM_ElementMaker as ATOM
from pyproj import Proj, CRS, Transformer
import os
from lxml import etree

DIRNAME = os.path.dirname(os.path.abspath(__file__))

# NOTE: esta herramienta da las coordenadas correctas https://awsm-tools.com/geo/utm-to-geographic
proj = Proj("+proj=utm +zone=19 +south +area=C +ellps=WGS84 +datum=WGS84")
trans = Transformer.from_proj(proj, CRS("EPSG:4326"))
lat, lon = trans.transform(179719, 8508565)


def parse_coords(coord:str) -> int:
    return int(coord.replace(",","").replace(".0", ""))

def build_cdata_description(*args) -> str:
    return "<![CDATA[ <div>"  +  "</div> <br><br> <div>".join(*args) + "</div> ]]>"



keys_to_print = [
    'Acceso',
    'Ubicación',
    'Geología',
    'Mineralogía',
]

os.makedirs(f"{DIRNAME}/minas_abandonadas", exist_ok=True)
os.makedirs(f"{DIRNAME}/minas_abandonadas/images", exist_ok=True)


kml = KML.kml(KML.Document(
    KML.name("Minas abandonadas del Cusco"),
    ATOM.author(ATOM.name("Gianfranco Rossi"))
))

for mine in structured_data:
    name = KML.name(mine['Nombre de Mina'])

    proj = Proj(f"+proj=utm +zone={mine['Zona']} +south +area=C +ellps=WGS84 +datum=WGS84")
    trans = Transformer.from_proj(proj, CRS("EPSG:4326"))
    lat, lon = trans.transform(parse_coords(mine['Este']), parse_coords(mine['Norte']))

    img_name = f"{mine['Nombre de Mina']}.jpg".replace(" ", "_")
    img_relative_path = f"./minas_abandonadas/images/{img_name}"
    with open(img_relative_path, 'wb') as F:
        F.write(mine['img_binary'])
    img_link = KML.Link( KML.href(img_relative_path) )
    
    point = KML.Point(KML.coordinates(f"{lon},{lat},0"))
    lookat = KML.LookAt(
        KML.latitude(lat),
        KML.longitude(lon),
        KML.altitude(0),
        KML.altitudeMode("relativeToGround"),
    )

    description = KML.description(
        build_cdata_description(  [ f"<b>{key}</b>: {mine[key].capitalize()}" for key in keys_to_print]  )  
    )

    place = KML.Placemark(name, point, description,img_link)
    kml.Document.append(place)



with open(f'{DIRNAME}/minas_abandonadas/output.kml', 'w') as output:
    output.write(etree.tostring(kml, pretty_print=True).decode('utf-8'))