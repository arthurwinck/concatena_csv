def extract_cities(filename):
    file = open(filename)
    i = 0
    lista_cidades = []
    lista_cidades_final = []

    for line in file:
        if '.jpg' not in line and 'alto' not in line and '.png' not in line and '.JPG' not in line:
            lista_cidades.append(line)
        
    for cidade_row in lista_cidades:
        cidade_row_lista = cidade_row.split(' 	')

        for cidade in cidade_row_lista:
            if not any(char.isdigit() for char in cidade):
                cidade = cidade.replace('\t', '')
                cidade = cidade.upper()
                cidade = cidade.replace('Ã', 'A')
                cidade = cidade.replace('Á', 'A')
                cidade = cidade.replace('É', 'E')
                cidade = cidade.replace('Ó', 'O')
                
                lista_cidades_final.append(cidade)

    return lista_cidades_final

#extract_cities('table.txt')
#print(' 	')