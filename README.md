# ALEX4devoir


*Alex4 est un jeu de plateforme rétro au style pixelisé, dans lequel on incarne un crocodile explorant des niveaux remplis d'obstacles.*

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
