def extract_cities(filename):
    file = open(filename)
    i = 0
    lista_linhas = []

    for line in file:
        if '.jpg' not in line and 'alto' not in line:
            lista_linhas.append(line)
        
    print(lista_linhas)

extract_cities('table.txt')