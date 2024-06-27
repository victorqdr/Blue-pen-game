# Blue Pen Game
Desenvolvido por Victor Quadri RA 1136643 e Bruno Prado RA 1136535
Este é o jogo Blue Pen Game, desenvolvido em Python utilizando a biblioteca Pygame.

import cx_Freeze

executaveis = [cx_Freeze.Executable(script="main.py", icon="recursos/icone.png")]

cx_Freeze.setup(
    name="Blue pen game",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": [
                "recursos/icone.png",
                "recursos/manoel.png",
                "recursos/fundo.png",
                "recursos/fundoStart.png",
                "recursos/fundoDead.png",
                "recursos/blackpen.png",
                "recursos/pen.png",
                "recursos/pensound.wav",
                "recursos/explosao.wav",
                "recursos/blueSound.mp3",
                "historico.txt"
            ],
        }
    },
    executables=executaveis
)
