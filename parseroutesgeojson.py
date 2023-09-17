import json
file = input('Quel fichier voulez vous parse?: ')
table = input('Comment voulez vous nommer la table de donnée?:')
fichier= table +".sql"
with open(file) as f:
    data = json.load(f)
f2 = open(fichier,'w')
for feature in data['features']:
    for key in feature['geometry']['coordinates']:
        item1 = feature['properties']['route_type']
        item2 = feature['properties']['route_I']
        item3 = feature['properties']['route_name']
        ligne = "INSERT INTO " + table + (' VALUES (') + str(key[1]) + ','  + str(key[0]) + ',' + str(item1) + ',' + str(item2) + ',' + '\'' + str(item3) + '\''
        ligne = ligne + ');\n'
        f2.write(ligne)