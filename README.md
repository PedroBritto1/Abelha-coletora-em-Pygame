# Abelha Coletora 🐝

Jogo 2D feito em Python com Pygame, desenvolvido em grupo como trabalho da faculdade.

## Como jogar
Você controla uma abelha que coleta pólen nas flores e o leva até a colmeia,
um de cada vez, desviando das ameaças do mapa.

- **Setas ou WASD:** mover
- **Espaço:** arrancada
- **R:** reiniciar

## Regras
- Ameaças: aranhas (fio vertical) e sapos (língua)
- Os arbustos funcionam como paredes
- Você começa com 3 vidas
- Cada pólen entregue vale 100 pontos
- **Vitória:** entregar 10 pólens em 90 segundos
- **Derrota:** perder todas as vidas ou o tempo acabar

## Como executar
1. Instale o Python 3 e o Pygame:
   ```bash
   pip install pygame
   ```
2. Clone o repositório:
   ```bash
   git clone https://github.com/PedroBritto1/Abelha-coletora-em-Pygame
   ```
3. Execute:
   ```bash
   python Jogo.py
   ```

## Detalhes técnicos
- Mapa em matriz carregado a partir de um arquivo .txt, com colisão
- Animações da abelha e das ameaças
