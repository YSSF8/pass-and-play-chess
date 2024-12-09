# Pass-and-Play Chess

Pass-and-Play Chess is a simple chess game where two players can take turns to play on the same device. The game is built using Pygame and is intended for casual play.

## Features

- Two-player gameplay on the same device
- Basic chess piece movement and rules
- Highlighting valid moves, last move, and selected piece
- Pawn promotion to queen
- Detection of checkmate
- Replay option after a game is over

## Requirements

- Python 3.x
- Pygame

## Installation

First, ensure you have Python and Pygame installed. You can install Pygame using pip:

```sh
pip install pygame
```

After installing the requirements, download or clone this repository:

```sh
git clone https://github.com/YSSF8/pass-and-play-chess.git
cd pass-and-play-chess
```

## Running the Game

To start the game, simply run the `game.py` file:

```sh
python game.py
```

## How to Play

1. The game starts with the white pieces moving first.
2. Click on a piece to see its valid moves highlighted in green.
3. Click on a valid move to move the selected piece.
4. The game will automatically detect and announce checkmate.
5. After the game ends, you can click the "Replay" button to start a new game.

## Game Controls

- **Left Mouse Button**: Select and move pieces
- **Close Window Button**: Exit the game

## Contributing

Contributions are welcome! If you find bugs or have enhancements in mind, feel free to fork the repository and create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
