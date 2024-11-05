# ALEX4devoir


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
from ptrace.debugger import PtraceDebugger
import time

alex4_pid = xxxxx  # Remplacez "xxxxx" par le PID récupéré

def pause_process(pid):
    """Attache au processus et le met en pause."""
    debugger = PtraceDebugger()
    process = debugger.addProcess(pid, False)
    process.syscall()
    print(f"Processus {pid} mis en pause.")
    return debugger, process

# Mettre en pause le processus
debugger, process = pause_process(alex4_pid)

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
## Étape 6 :

