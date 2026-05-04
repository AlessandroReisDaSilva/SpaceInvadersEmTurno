import os
import random

LARGURA = 20
ALTURA = 10
ARQUIVO = "ranking.txt"

def inicializar_grid():
    return [[' ' for _ in range(LARGURA)] for _ in range(ALTURA)]

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
        for linha in f: print(linha.strip())

def jogar():
    nome = input("Digite seu nome de recruta: ")
    grid = inicializar_grid()
    pos_jogador = LARGURA // 2
    aliens = [[1, i] for i in range(2, 16, 2)]
    vidas = 3
    pontos = 0
    nivel = 1

    while vidas > 0:
        if not aliens:
            nivel += 1
            aliens = [[1, i] for i in range(1, LARGURA-1, max(1, 4-nivel))]
            print(f"BOM TRABALHO! Iniciando Nível {nivel}...")

        for r in range(ALTURA):
            for c in range(LARGURA): grid[r][c] = ' '

        grid[ALTURA-1][pos_jogador] = 'A'
        for r, c in aliens:
            if r < ALTURA: grid[r][c] = 'W'
            if r >= ALTURA - 1:
                vidas = 0

        renderizar(grid, nome, vidas, pontos, nivel)
        if vidas <= 0: break

        print("COMANDOS: 'a' (esq), 'd' (dir), 's' (atirar). Ex: 'aaas' faz tudo de uma vez!")
        comandos = input("Ação: ").lower()

        for acao in comandos:
            if acao == 'a' and pos_jogador > 0: pos_jogador -= 1
            elif acao == 'd' and pos_jogador < LARGURA - 1: pos_jogador += 1
            elif acao == 's':

                for i, (ar, ac) in enumerate(aliens):
                    if ac == pos_jogador:
                        aliens.pop(i)
                        pontos += 10 * nivel
                        break

        chance_descida = 0.3 + (nivel * 0.1)
        if random.random() < min(chance_descida, 0.9):
            for a in aliens: a[0] += 1

    salvar_pontuacao(nome, pontos)
    print(f"\nGAME OVER, {nome}! Pontuação Final: {pontos}")
    carregar_ranking()

if __name__ == "__main__":
    jogar()
