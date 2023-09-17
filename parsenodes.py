file = input('Quel fichier voulez vous parse?: ')
table = input('Comment voulez vous nommer la table de donnée?:')
fichier= table +".sql"
f = open(file, 'r')
f2 = open(fichier,'w')
next(f)
for line in f:
    items = line.rstrip("\n").split(";")
    ligne = "INSERT INTO " + table + (" VALUES (") + items[0]
    for item in items[1:] :
        if(item == items[3]):
            item = item.replace("'","-")
            ligne = ligne  +"," "'" + item + "'"
            break
        item = item.replace("'", "''")
        ligne = ligne + "," + item
    ligne = ligne + ");\n"
    f2.write(ligne)