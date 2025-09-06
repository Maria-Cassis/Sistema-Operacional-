import random
import os

class Processo:
    def __init__(self, pid, tempo_total_execucao):
        self.pid = pid
        self.tempo_total_execucao = tempo_total_execucao
        self.tempo_processado = 0
        self.contador_programa = 0
        self.estado = 'PRONTO'
        self.num_operacoes_es = 0
        self.num_usos_cpu = 0
        self.quantum_restante = 0

    def __str__(self):
        return (f"PID: {self.pid}\n"
                f"Tempo Processado (TP): {self.tempo_processado}\n"
                f"Contador de Programa (CP): {self.contador_programa}\n"
                f"Estado do Processo (EP): {self.estado}\n"
                f"Nº de Operações de E/S (NES): {self.num_operacoes_es}\n"
                f"Nº de Usos da CPU (N_CPU): {self.num_usos_cpu}\n")


def salvar_tabela_processos(processos, arquivo='tabela_de_processos.txt'):
    with open(arquivo, 'w') as f:
        f.write("--- Tabela de Processos ---\n\n")
        for p in processos.values():
            f.write(str(p) + "--------------------\n")

def executar_simulacao():
    tempos_execucao = {
        0: 10000, 1: 5000, 2: 7000, 3: 3000, 4: 3000,
        5: 8000, 6: 2000, 7: 5000, 8: 4000, 9: 10000
    }
    
    processos = {pid: Processo(pid, tempo) for pid, tempo in tempos_execucao.items()}
    
    fila_prontos = list(range(10))
    fila_bloqueados = []

    print("Iniciando a simulação...")
    
    ciclos_globais = 0
    
    while fila_prontos or fila_bloqueados:
        ciclos_globais += 1

        processos_desbloqueados = []
        for pid_bloqueado in fila_bloqueados:
            if random.random() < 0.3: 
                processos[pid_bloqueado].estado = 'PRONTO'
                print(f"[{ciclos_globais}] PID {pid_bloqueado} >> DESBLOQUEADO >> PRONTO")
                processos_desbloqueados.append(pid_bloqueado)

        for pid_desbloqueado in processos_desbloqueados:
            fila_bloqueados.remove(pid_desbloqueado)
            fila_prontos.append(pid_desbloqueado)
        
        if not fila_prontos:
            continue

        pid_executando = fila_prontos.pop(0)
        p = processos[pid_executando]
        
        p.estado = 'EXECUTANDO'
        p.num_usos_cpu += 1
        p.quantum_restante = 1000
        
        print(f"[{ciclos_globais}] PID {p.pid}: PRONTO >> EXECUTANDO")

        executando_por_quantum = True
        
        while p.quantum_restante > 0 and p.tempo_processado < p.tempo_total_execucao:
            p.tempo_processado += 1
            p.contador_programa = p.tempo_processado + 1
            p.quantum_restante -= 1

            if random.random() < 0.01:  
                p.num_operacoes_es += 1
                p.estado = 'BLOQUEADO'
                print(f"PID {p.pid} EXECUTANDO >> BLOQUEADO")
                print(f"Dados salvos:")
                print(p)
                salvar_tabela_processos(processos)
                fila_bloqueados.append(p.pid)
                executando_por_quantum = False
                break
        
        if executando_por_quantum:
            if p.tempo_processado >= p.tempo_total_execucao:
                p.estado = 'TERMINADO'
                print(f"\n--- PID {p.pid} TERMINADO ---")
                print(p)
                print("------------------------------\n")
            else:
                p.estado = 'PRONTO'
                print(f"PID {p.pid} EXECUTANDO >> PRONTO (Troca de Contexto)")
                print(f"Dados salvos:")
                print(p)
                salvar_tabela_processos(processos)
                fila_prontos.append(p.pid)

if __name__ == "__main__":
    executar_simulacao()

    
