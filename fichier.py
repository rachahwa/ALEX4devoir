
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
