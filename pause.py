
from ptrace.debugger import PtraceDebugger
import time

# PID du processus Alex4 (remplace par le bon PID)
alex4_pid = 4294  # Remplace par le PID du processus Alex4

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

# Mettre en pause le processus Alex4
debugger, process = pause_process(alex4_pid)

# Attendre 5 secondes
time.sleep(5)

# Reprendre le processus Alex4
resume_process(debugger, process)

