import time
from ptrace.debugger import PtraceDebugger
import struct

# PID du processus Alex4 (remplace par le bon PID)
alex4_pid = 2342  # Remplace par le PID du processus Alex4

def pause_process(pid):
    """Attache au processus avec PTRACE et le met en pause."""
    debugger = PtraceDebugger()
    process = debugger.addProcess(pid, False)  # Attacher au processus sans suivre les fils
    process.syscall()  # Suspendre l'exécution à l'appel système
    print(f"Processus {pid} mis en pause.")
    return debugger, process

def resume_process(debugger, process):
    """Reprend l'exécution du processus."""
    process.cont()  # Continuer l'exécution du processus
    debugger.quit()  # Détacher et quitter le débogueur
    print(f"Processus {process.pid} repris.")

def modify_memory(process, address, new_value):
    """Modifie la valeur à une adresse mémoire spécifique dans le processus."""
    # Modifier la valeur en mémoire à l'adresse spécifiée
    try:
        process.writeBytes(address, struct.pack('<Q', new_value))  # '<Q' pour un entier 64 bits (little-endian)
        print(f"Modification de la mémoire à l'adresse {hex(address)} avec la nouvelle valeur {hex(new_value)}.")
    except Exception as e:
        print(f"Erreur lors de la modification de la mémoire: {e}")

# Adresse mémoire à modifier et nouvelle valeur
address = 0x5587e9abbc48  # Remplace avec l'adresse mémoire réelle
new_value = 0x12  # Nouvelle valeur à insérer en hexadécimal

# Mettre en pause le processus Alex4
debugger, process = pause_process(alex4_pid)

# Modifier la mémoire à l'adresse spécifiée
modify_memory(process, address, new_value)

# Attendre 5 secondes pour vérifier que tout est bien en place
time.sleep(5)

# Reprendre le processus Alex4
resume_process(debugger, process)

