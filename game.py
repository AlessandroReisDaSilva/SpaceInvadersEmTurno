import os
import random

LARGURA = 20
ALTURA = 10
ARQUIVO = "ranking.txt"

def inicializar_grid():
    return [[' ' for _ in range(LARGURA)] for _ in range(ALTURA)]

def limpar_tela():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def renderizar(grid, nome, vidas, pontos, nivel):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f" JOGADOR: {nome} | VIDAS: {vidas} | PONTOS: {pontos} | NÍVEL: {nivel}")
    print("-" * (LARGURA + 2))
    for linha in grid:
        print("|" + "".join(linha) + "|")
    print("-" * (LARGURA + 2))


def salvar_pontuacao(nome, pontos):
    with open(ARQUIVO, "a") as f:
        f.write(f"{nome}:{pontos}\n")


def carregar_ranking():
    if not os.path.isfile(ARQUIVO): return
    print("\n--- RANKING DOS TOP JOGADORES ---")
    with open(ARQUIVO, "r") as f:
        for linha in f: 
            print(linha.strip())


def inicializar_aliens(nivel):
    espaco_aliens = max(1, 4 - nivel)
    return [[1, i] for i in range(1, LARGURA - 1, espaco_aliens)]


def movimento_jogador(pos_jogador, acao):
    if acao == 'a' and pos_jogador > 0:
        pos_jogador -= 1
    elif acao == 'd' and pos_jogador < LARGURA - 1:
        pos_jogador += 1
    return pos_jogador


def tiro(pos_jogador, aliens, nivel):
    pontos_ganhos = 0
    for i, (linha_alien, coluna_alien) in enumerate(aliens):
        if coluna_alien == pos_jogador:
            aliens.pop(i)
            pontos_ganhos = 10 * nivel
            break
    return pontos_ganhos


def atualizar_aliens(aliens, nivel):
    chance_descida = min(0.3 + (nivel * 0.1), 0.9)
    if random.random() < chance_descida:
        for alien in aliens:
            alien[0] += 1


def renderizar_grid(grid, pos_jogador, aliens):
    for r in range(ALTURA):
        for c in range(LARGURA):
            grid[r][c] = ' '
    
    grid[ALTURA - 1][pos_jogador] = 'A'
    
    for linha_alien, coluna_alien in aliens:
        if linha_alien < ALTURA:
            grid[linha_alien][coluna_alien] = 'W'


def verificar_colisoes_aliens(aliens):
    for linha_alien, _ in aliens:
        if linha_alien >= ALTURA - 1:
            return True
    return False


def jogar():
    nome = input("Digite seu nome de recruta: ")
    grid = inicializar_grid()
    pos_jogador = LARGURA // 2
    aliens = inicializar_aliens(1)
    vidas = 3
    pontos = 0
    nivel = 1

    while vidas > 0:
        if not aliens:
            nivel += 1
            aliens = inicializar_aliens(nivel)
            input(f"\nBOM TRABALHO! Iniciando Nível {nivel}... Pressione ENTER para continuar.")

        renderizar_grid(grid, pos_jogador, aliens)

        renderizar(grid, nome, vidas, pontos, nivel)

        if verificar_colisoes_aliens(aliens):
            vidas -= 1
            if vidas <= 0:
                break
            continue

        print("COMANDOS: 'a' (esq), 'd' (dir), 's' (atirar). Ex: 'aaas' faz tudo de uma vez!")
        comandos = input("Ação: ").lower()

        for acao in comandos:
            pos_jogador = movimento_jogador(pos_jogador, acao)
            
            if acao == 's':
                pontos += tiro(pos_jogador, aliens, nivel)

        atualizar_aliens(aliens, nivel)

    salvar_pontuacao(nome, pontos)
    limpar_tela()
    print(f"\nGAME OVER, {nome}! Pontuação Final: {pontos}")
    carregar_ranking()

if __name__ == "__main__":
    jogar()
