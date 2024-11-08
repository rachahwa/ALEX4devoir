# ALEX4devoir Wassila et Léa


*Alex4 est un jeu de plateforme rétro au style pixelisé, dans lequel on incarne un crocodile explorant des niveaux remplis d'obstacles.*

Dans ce devoir, vous pourrez retrouver les différentes étapes de notre réflexion. En revanche, elles pourront ne pas toute se retrouver dans le code finale car nous aurons jugé qu'elles ne sont pas forcément nécéssaire. 
## Étape 1 : Trouver le PID du jeu

Utilisez la commande suivante pour obtenir le PID du jeu `alex4` :

```bash
pgrep alex4
```

## Étape 2 : Code pour mettre en pause le jeu

Une fois le PID récupéré, utilisez le code ci-dessous pour mettre en pause le processus du jeu. 
Le PID est évidemment à inclure à l'endroit indiqué par un commentaire.

```bash

import os
import time
from ptrace.debugger import PtraceDebugger

# Remplace par le PID du processus que tu veux attacher
alex4_pid = 3183  # Assure-toi que ce PID est valide et actif

def is_process_running(pid):
    """Vérifie si un processus est en cours d'exécution."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def get_stack_line(pid):
    """Récupère la ligne correspondant à la pile du processus."""
    with open(f'/proc/{pid}/maps', 'r') as f:
        for line in f:
            if 'stack' in line:
                return line.strip()  # Retourne la ligne complète
    return None

def pause_process(pid):
    """Attache au processus et le met en pause."""
    debugger = PtraceDebugger()
    process = debugger.addProcess(pid, False)
    process.syscall()
    print(f"Processus {pid} mis en pause.")
    return debugger, process

def resume_process(debugger, process):
    """Reprend l'exécution du processus."""
    try:
        process.cont()
        debugger.quit()
        print(f"Processus {process.pid} repris.")
    except Exception as e:
        print(f"Erreur lors de la reprise du processus : {e}")

# Vérifie si le processus est en cours d'exécution
if not is_process_running(alex4_pid):
    print(f"Le processus {alex4_pid} n'est pas en cours d'exécution.")
else:
    # Mettre en pause le processus
    debugger, process = pause_process(alex4_pid)

    # Récupérer et afficher la ligne de la pile
    stack_line = get_stack_line(alex4_pid)
    if stack_line:
        print("Ligne de la pile:")
        print(stack_line)
    else:
        print("Aucune ligne de pile trouvée.")

    # Attendre 5 secondes
    time.sleep(5)

    # Vérifie à nouveau si le processus est toujours en cours d'exécution avant de le reprendre
    if is_process_running(alex4_pid):
        resume_process(debugger, process)
    else:
        print(f"Le processus {alex4_pid} n'est plus en cours d'exécution.")

```

## Bibliothèque Ptrace 

**Ptrace** est une bibliothèque Unix qui il permet à un programme d'inspecter et de contrôler l'exécution d'un autre processus. Elle est souvent utilisée dans le développement et le débogage pour :

1. **Suivre l’exécution** : Elle permet de surveiller chaque étape d’un processus, comme les appels système effectués.
2. **Modifier le processus** : On peut altérer l'état d'un processus, en changeant ses variables ou son flux d'exécution.
3. **Débogage** : Elle aide à détecter et corriger des erreurs en permettant l'inspection de la mémoire et des registres.

Ainsi vous pourrez remarquer que c'est la bibliothèque nous avons choisie d'utiliser ici.

## Etape 3 : Récupération de la mémoire 

```bash
# Récupérer et afficher les adresses de la pile
    stack_addresses = get_stack_addresses(alex4_pid)
    print("Adresses de la pile:")
    for addr in stack_addresses:
        print(addr)
```

## Etape 4 : Récupération de la ligne stack

```bash
stack_line = get_stack_line(alex4_pid)
    if stack_line:
        print("Ligne de la pile:")
        print(stack_line)
    else:
        print("Aucune ligne de pile trouvée.")
```

## Etape 5 : Affichage de l'intervalle 
```bash
def display_stack_memory(debugger, process, stack_start, stack_end, step=8):
    """Affiche les valeurs en mémoire depuis le début de la pile."""
    current_address = stack_start
    while current_address < stack_end:
        try:
            # Lire un bloc de mémoire à l'adresse courante
            data = read_memory(process, current_address, step)
            # Interpréter ces données comme un nombre (pour les adresses 64-bits)
            value = struct.unpack('<Q', data)[0]  # <Q pour un entier non signé 64-bits
            print(f"Adresse: {hex(current_address)} | Valeur: {hex(value)}")
            current_address += step
        except Exception as e:
            print(f"Erreur lors de la lecture de la mémoire à {hex(current_address)}: {e}")
            break
```
## Étape 6 : Création d'un fichier .txt

```bash
import os
import time
from ptrace.debugger import PtraceDebugger
import struct

# Remplace par le PID du processus que tu veux attacher
alex4_pid = 2342  # Assure-toi que ce PID est valide et actif

def is_process_running(pid):
    """Vérifie si un processus est en cours d'exécution."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def get_stack_line(pid):
    """Récupère la ligne correspondant à la pile du processus."""
    with open(f'/proc/{pid}/maps', 'r') as f:
        for line in f:
            if 'stack' in line:
                return line.strip()  # Retourne la ligne complète
    return None

def pause_process(pid):
    """Attache au processus et le met en pause."""
    debugger = PtraceDebugger()
    process = debugger.addProcess(pid, False)
    process.syscall()
    print(f"Processus {pid} mis en pause.")
    return debugger, process

def resume_process(debugger, process):
    """Reprend l'exécution du processus."""
    try:
        process.cont()
        debugger.quit()
        print(f"Processus {process.pid} repris.")
    except Exception as e:
        print(f"Erreur lors de la reprise du processus : {e}")

def read_memory(process, address, size):
    """Lit un bloc de mémoire à partir d'une adresse spécifique."""
    data = process.readBytes(address, size)
    return data

def display_stack_memory(debugger, process, stack_start, stack_end, step=8, file=None):
    """Affiche les valeurs en mémoire depuis le début de la pile."""
    current_address = stack_start
    while current_address < stack_end:
        try:
            # Lire un bloc de mémoire à l'adresse courante
            data = read_memory(process, current_address, step)
            # Interpréter ces données comme un nombre (pour les adresses 64-bits)
            value = struct.unpack('<Q', data)[0]  # <Q pour un entier non signé 64-bits
            # Si un fichier est passé, on l'écrit dedans, sinon on affiche dans la console
            if file:
                file.write(f"Adresse: {hex(current_address)} | Valeur: {hex(value)}\n")
            else:
                print(f"Adresse: {hex(current_address)} | Valeur: {hex(value)}")
            current_address += step
        except Exception as e:
            print(f"Erreur lors de la lecture de la mémoire à {hex(current_address)}: {e}")
            break

# Vérifie si le processus est en cours d'exécution
if not is_process_running(alex4_pid):
    print(f"Le processus {alex4_pid} n'est pas en cours d'exécution.")
else:
    # Mettre en pause le processus
    debugger, process = pause_process(alex4_pid)

    # Récupérer et afficher la ligne de la pile
    stack_line = get_stack_line(alex4_pid)
    if stack_line:
        print("Ligne de la pile:")
        print(stack_line)
        
        # Extraire l'adresse de début et de fin de la pile à partir de /proc/{pid}/maps
        # Exemple : 7ffcb0321000-7ffcb0342000 r--p 00000000 00:00 0  /lib/x86_64-linux-gnu/libc-2.31.so
        addresses = stack_line.split(' ')[0].split('-')
        stack_start = int(addresses[0], 16)
        stack_end = int(addresses[1], 16)

        # Créer ou ouvrir un fichier pour enregistrer les résultats
        with open('stack_memory_output13.txt', 'w') as file:
            file.write(f"Exploration de la pile pour le processus {alex4_pid}:\n")
            display_stack_memory(debugger, process, stack_start, stack_end, file=file)

            print("Les valeurs de la pile ont été enregistrées dans 'stack_memory_output3.txt'.")
    else:
        print("Aucune ligne de pile trouvée.")

    # Attendre 5 secondes
    time.sleep(5)

    # Vérifie à nouveau si le processus est toujours en cours d'exécution avant de le reprendre
    if is_process_running(alex4_pid):
        resume_process(debugger, process)
    else:
        print(f"Le processus {alex4_pid} n'est plus en cours d'exécution.")
```

## Etape 6 : Comparaison

L'étape de comparaison a été un point sur lequel nous avons passé beaucoup de temps, mais qui s'est avéré inutile à la fin, car nous avons décidé de changer notre démarche.

L'objectif est de comparer deux fichiers crées précédemment (de stack) en supprimant toutes les lignes similaires. Lorsqu'une adresse n'est présente que dans un fichier, elle est égalemment supprimée. Cette technique est fastidieuse car, il faut réitérer l'opération une multitude de fois pour obtenir la ligne voulue sachant que le fichier peut-être assez imposant.  
[fichier python pour comparer les fichiers](comparaison.py)

## Etape 7 : Scanmem

Finalement la méthode d'avant n'était pas concluante.
Nous avons donc installé scanmem et gdb.  

```bash
sudo apt install scanmem
sudo apt install gdb
```

Scanmem permet de scanner la mémoire d'alex4. Une fois scanmem lancé il faut préciser le pid de notre jeu.    
![Capture d'écran 2024-11-05 114329](https://github.com/user-attachments/assets/48123e5f-a7e2-4118-949a-478869cffd36)  
Ensuite on lui indique score qu'on a sur le jeu et on réitère jusqu'a qu'il nous reste plus qu'une ligne.    
![Capture d'écran 2024-11-05 114607](https://github.com/user-attachments/assets/0d8ce73e-fbd6-49f2-8682-51c372a1c5f3)  
![Capture d'écran 2024-11-05 114619](https://github.com/user-attachments/assets/4baee73e-12da-4d13-bc32-947b921f19b7)  

## Etape 8 : Insertion
Une fois qu'on a réussi à retrouver notre addresse nous pouvons utiliser GDB qui nous permettra de modifier la valeur dans l'adresse mémoire. Dans notre cas nous pouvons donc changer le score grace a l'addresse retrouver.
[code pour modifier valeur adresse mémoire](inserer.py)

