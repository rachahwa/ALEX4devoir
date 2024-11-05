# ALEX4devoir


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
