def parse_line(line):
    """Extrait l'adresse et la valeur d'une ligne."""
    # Exemple de ligne : "Adresse: 0x7ffcb0321000 | Valeur: 0x1234567890abcdef"
    parts = line.split('|')
    if len(parts) != 2:
        return None  # Si la ligne ne suit pas le format attendu, la sauter
    address = parts[0].strip().split(":")[1].strip()
    value = parts[1].strip().split(":")[1].strip()
    return address, value

def subtract_files_and_keep_diff(file1, file2, output_file=None):
    """Soustrait les lignes du premier fichier au deuxième et garde celles qui sont communes, mais avec des valeurs différentes."""
    
    # Lire toutes les lignes des deux fichiers
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()
    
    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    # Dictionnaires pour stocker les adresses et leurs valeurs
    data1 = {}
    data2 = {}

    # Parser les lignes du premier fichier
    for line in lines1:
        result = parse_line(line)
        if result:
            address, value = result
            data1[address] = value

    # Parser les lignes du deuxième fichier
    for line in lines2:
        result = parse_line(line)
        if result:
            address, value = result
            data2[address] = value

    # Liste pour stocker les lignes à garder
    result_lines = []

    # Comparer les adresses et les valeurs
    for address in data1:
        if address in data2:
            # Si l'adresse existe dans les deux fichiers et que les valeurs sont différentes
            if data1[address] != data2[address]:
                # Créer la ligne à afficher
                result_lines.append(f"Adresse: {address} | Valeur: {data1[address]}\n")
                result_lines.append(f"Adresse: {address} | Valeur: {data2[address]}\n")

    # Si un fichier de sortie est spécifié, on écrit les résultats dedans
    if output_file:
        with open(output_file, 'w') as out:
            out.writelines(result_lines)
        print(f"Les lignes avec des adresses communes mais des valeurs différentes ont été enregistrées dans {output_file}.")
    else:
        # Sinon, on affiche les résultats à l'écran
        for line in result_lines:
            print(line, end="")

# Appel de la fonction pour comparer et garder les adresses communes avec des valeurs différentes
subtract_files_and_keep_diff('stack_memory_diff.txt', 'stack_memory_output13.txt', output_file='stack_memory_diff.txt')

