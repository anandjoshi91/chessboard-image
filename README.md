# Chessboard Image

[![PyPI version](https://badge.fury.io/py/chessboard-image.svg)](https://badge.fury.io/py/chessboard-image)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pure Python library for generating beautiful chess board images from FEN (Forsyth-Edwards Notation) strings. Create professional-looking chess diagrams with customizable themes, piece sets, and board colors.

## Features

✨ **Pure Python** - No external dependencies except PIL/Pillow  
🎨 **Multiple Themes** - Built-in themes with beautiful piece sets  
🎯 **FEN Support** - Generate boards from any valid FEN notation  
📱 **Flexible Output** - Save as file, get bytes, or PIL Image object  
🔧 **Customizable** - Easy to add custom themes and piece sets  
⚡ **Fast** - No browser dependencies, pure image composition  

## Installation

```bash
pip install chessboard-image
```

## Quick Start

```python
from chessboard_image import generate_image

# Generate starting position
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
generate_image(fen, "chess_board.png", size=512)
```

## Usage

### Basic Usage

```python
import chessboard_image as cbi

# Starting position
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Generate and save image (White's perspective - default)
cbi.generate_image(start_fen, "start_position.png", size=400)

# Generate from Black's perspective
cbi.generate_image(start_fen, "start_position_black.png", size=400, player_pov="black")

# Generate with coordinates shown
cbi.generate_image(start_fen, "start_with_coords.png", size=400, show_coordinates=True)

# Get image as bytes (useful for web APIs)
image_bytes = cbi.generate_bytes(start_fen, size=300)

# Get PIL Image object for further processing
pil_image = cbi.generate_pil(start_fen, size=500, player_pov="black", show_coordinates=True)
pil_image.show()  # Display the image
```

### Board Coordinates

You can add file (a-h) and rank (1-8) labels to the board:

```python
# Show coordinates with default white perspective
cbi.generate_image(fen, "board_with_coords.png", show_coordinates=True)

# Show coordinates with black perspective
# Files: h-a (left to right), Ranks: 8-1 (bottom to top)
cbi.generate_image(fen, "board_black_coords.png", player_pov="black", show_coordinates=True)

# Coordinates automatically adjust for perspective:
# White POV: files a-h, ranks 1-8 (bottom to top)
# Black POV: files h-a, ranks 8-1 (bottom to top)
```

### Player Perspective

By default, boards are generated from White's perspective (White pieces at bottom). You can generate from Black's perspective by setting `player_pov="black"`, which flips the board so Black pieces appear at the bottom while keeping all pieces upright:

```python
# White's perspective (default) - White pieces at bottom
cbi.generate_image(fen, "white_view.png", player_pov="white")

# Black's perspective - Black pieces at bottom, pieces stay upright
cbi.generate_image(fen, "black_view.png", player_pov="black")

# Works with all output formats
black_bytes = cbi.generate_bytes(fen, player_pov="black")
black_pil = cbi.generate_pil(fen, player_pov="black")
```

### Using Different Themes

```python
# List available themes
themes = cbi.list_themes()
print("Available themes:", themes)  # ['wikipedia', 'alpha', ...]

# Use different theme
cbi.generate_image(
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    "italian_game.png", 
    size=600,
    theme_name="alpha"
)

# Get theme information
theme_info = cbi.get_theme_info("wikipedia")
print(f"Board colors: {theme_info['board_colors']}")
print(f"Pieces available: {theme_info['piece_count']}")
```

### Custom Themes

Create your own theme file:

```python
# Load custom theme
cbi.generate_image(
    fen, 
    "custom_board.png",
    theme_file="my_themes.json",
    theme_name="my_custom_theme"
)
```

### Error Handling

```python
try:
    cbi.generate_image("invalid_fen", "board.png")
except cbi.InvalidFENError as e:
    print(f"Invalid FEN: {e}")
except cbi.ThemeNotFoundError as e:
    print(f"Theme error: {e}")
except cbi.ChessImageGeneratorError as e:
    print(f"Generation error: {e}")
```

## API Reference

### Core Functions

#### `generate_image(fen, output_path=None, size=400, theme_file=None, theme_name="wikipedia", player_pov="white", show_coordinates=False)`

Generate chess board image from FEN notation.

**Parameters:**
- `fen` (str): FEN notation string
- `output_path` (str, optional): Output file path. If None, uses temp file.
- `size` (int): Board size in pixels (default: 400)
- `theme_file` (str, optional): Path to custom theme JSON file
- `theme_name` (str): Theme name to use (default: "wikipedia")
- `player_pov` (str): Player perspective - "white" or "black" (default: "white")
- `show_coordinates` (bool): Show file/rank labels (default: False)

**Returns:** `str` - Path to generated image file

**Raises:** `InvalidFENError`, `ThemeNotFoundError`, `ChessImageGeneratorError`

#### `generate_bytes(fen, size=400, theme_file=None, theme_name="wikipedia", player_pov="white", show_coordinates=False)`

Generate chess board image as bytes.

**Returns:** `bytes` - PNG image data

#### `generate_pil(fen, size=400, theme_file=None, theme_name="wikipedia", player_pov="white", show_coordinates=False)`

Generate chess board as PIL Image object.

**Returns:** `PIL.Image` - Image object

#### `list_themes(theme_file=None)`

List available themes.

**Returns:** `list` - Available theme names

#### `get_theme_info(theme_name="wikipedia", theme_file=None)`

Get information about a specific theme.

**Returns:** `dict` - Theme information including colors and pieces

### Convenience Aliases

```python
# Alternative function names
cbi.fen_to_image()  # Same as generate_image()
cbi.fen_to_bytes()  # Same as generate_bytes()
cbi.fen_to_pil()    # Same as generate_pil()
```

## Built-in Themes

The library comes with several built-in themes:

- **wikipedia** - Classic pieces from Wikipedia (default)
- **alpha** - Clean, modern piece design with purple accents

Each theme includes:
- 12 piece images (6 pieces × 2 colors) as base64-encoded PNGs
- Custom board colors (light and dark squares)

## Custom Themes

Create custom themes by making a JSON file:

```json
{
  "my_theme": {
    "pieces": {
      "bB": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "bK": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "bN": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "bP": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "bQ": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "bR": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wB": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wK": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wN": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wP": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wQ": ["data:image/png;base64,iVBORw0KGgoAAAANS..."],
      "wR": ["data:image/png;base64,iVBORw0KGgoAAAANS..."]
    },
    "board": ["#F0D9B5", "#B58863"]
  }
}
```

**Piece naming convention:**
- First letter: `b` (black) or `w` (white)
- Second letter: `K` (king), `Q` (queen), `R` (rook), `B` (bishop), `N` (knight), `P` (pawn)

**Board colors:** `[light_square_color, dark_square_color]` in hex format

## Examples

### Generate Famous Positions

```python
import chessboard_image as cbi

# Scholar's Mate from White's perspective
scholars_mate = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
cbi.generate_image(scholars_mate, "scholars_mate_white.png", size=500)

# Same position from Black's perspective
cbi.generate_image(scholars_mate, "scholars_mate_black.png", size=500, player_pov="black")

# Sicilian Defense
sicilian = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
cbi.generate_image(sicilian, "sicilian_defense.png", size=500)

# King and Queen vs King endgame
endgame = "8/8/8/8/8/3QK3/8/7k w - - 0 1"
cbi.generate_image(endgame, "kq_vs_k.png", size=400)
```

### Batch Processing

```python
import chessboard_image as cbi

positions = [
    ("start", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
    ("ruy_lopez", "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"),
    ("french_defense", "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3")
]

for name, fen in positions:
    # Generate both perspectives
    cbi.generate_image(fen, f"{name}_white.png", size=400, theme_name="alpha", player_pov="white")
    cbi.generate_image(fen, f"{name}_black.png", size=400, theme_name="alpha", player_pov="black")
    print(f"Generated {name} from both perspectives")
```

### Web API Integration

```python
from flask import Flask, send_file, request
import chessboard_image as cbi
import io

app = Flask(__name__)

@app.route('/board/<path:fen>')
def get_board_image(fen):
    try:
        # Get optional query parameters
        size = int(request.args.get('size', 400))
        theme = request.args.get('theme', 'wikipedia')
        player_pov = request.args.get('pov', 'white')
        
        # Generate image bytes
        image_bytes = cbi.generate_bytes(fen, size=size, theme_name=theme, player_pov=player_pov)
        
        # Return as downloadable image
        return send_file(
            io.BytesIO(image_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='chessboard.png'
        )
    except cbi.InvalidFENError:
        return "Invalid FEN notation", 400
    except Exception as e:
        return f"Error: {e}", 500
```

## Requirements

- Python 3.7+
- Pillow (PIL) for image processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/anandjoshi91/chessboard-image.git
cd chessboard-image
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Changelog

### 1.1.3
- Initial release
- Support for FEN notation
- Built-in 5 themes [alpha, wikipedia, uscf, wisteria, sakura]
- Generate image from pov of black or white player
- Add optional file and rank coordinates