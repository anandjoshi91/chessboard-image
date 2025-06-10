"""
Chessboard Image - Generate chess board images from FEN notation.

A pure Python library for creating beautiful chess board images from FEN strings
using customizable themes with base64-encoded pieces and board colors.
"""

import json
import base64
import io
import os
from PIL import Image, ImageDraw
from pathlib import Path
import tempfile
import pkg_resources

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Chess piece mapping
PIECE_MAP = {
    'K': 'wK', 'Q': 'wQ', 'R': 'wR', 'B': 'wB', 'N': 'wN', 'P': 'wP',
    'k': 'bK', 'q': 'bQ', 'r': 'bR', 'b': 'bB', 'n': 'bN', 'p': 'bP'
}


class ChessImageGeneratorError(Exception):
    """Base exception for chess image generator errors."""
    pass


class ThemeNotFoundError(ChessImageGeneratorError):
    """Raised when requested theme is not found."""
    pass


class InvalidFENError(ChessImageGeneratorError):
    """Raised when FEN notation is invalid."""
    pass


def get_default_theme_path():
    """Get path to default theme file."""
    try:
        return pkg_resources.resource_filename(__name__, 'theme.json')
    except:
        # Fallback for development
        return Path(__file__).parent / 'theme.json'


def load_theme(theme_file=None, theme_name="wikipedia"):
    """
    Load chess theme from JSON file.
    
    Args:
        theme_file (str, optional): Path to theme JSON file. If None, uses default.
        theme_name (str): Theme name to use (default: "wikipedia")
    
    Returns:
        dict: Theme data with pieces and board colors
        
    Raises:
        ThemeNotFoundError: If theme file or theme name not found
    """
    if theme_file is None:
        theme_file = get_default_theme_path()
    
    theme_path = Path(theme_file)
    
    if not theme_path.exists():
        raise ThemeNotFoundError(f"Theme file not found: {theme_file}")
    
    try:
        with open(theme_path, 'r') as f:
            themes = json.load(f)
    except json.JSONDecodeError as e:
        raise ThemeNotFoundError(f"Invalid JSON in theme file: {e}")
    
    if theme_name not in themes:
        available = list(themes.keys())
        raise ThemeNotFoundError(f"Theme '{theme_name}' not found. Available themes: {available}")
    
    return themes[theme_name]


def decode_base64_image(base64_data):
    """
    Decode base64 image data to PIL Image.
    
    Args:
        base64_data (str): Base64 image data (with or without data URL prefix)
    
    Returns:
        PIL.Image: Decoded image
        
    Raises:
        ChessImageGeneratorError: If image decoding fails
    """
    try:
        # Remove data URL prefix if present
        if base64_data.startswith('data:image'):
            base64_data = base64_data.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_data)
        return Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise ChessImageGeneratorError(f"Failed to decode base64 image: {e}")


def parse_fen(fen):
    """
    Parse FEN notation into 8x8 board array.
    
    Args:
        fen (str): FEN notation string
        
    Returns:
        list: 8x8 board array with piece symbols
        
    Raises:
        InvalidFENError: If FEN notation is invalid
    """
    try:
        board = []
        fen_board = fen.split()[0]  # Take only the board part
        
        rows = fen_board.split('/')
        if len(rows) != 8:
            raise InvalidFENError(f"FEN must have 8 rows, got {len(rows)}")
        
        for row_idx, row in enumerate(rows):
            board_row = []
            for char in row:
                if char.isdigit():
                    # Empty squares
                    count = int(char)
                    if count < 1 or count > 8:
                        raise InvalidFENError(f"Invalid empty square count: {count}")
                    board_row.extend([''] * count)
                elif char in PIECE_MAP:
                    # Piece
                    board_row.append(char)
                else:
                    raise InvalidFENError(f"Invalid character in FEN: '{char}'")
            
            if len(board_row) != 8:
                raise InvalidFENError(f"Row {row_idx + 1} has {len(board_row)} squares, expected 8")
            
            board.append(board_row)
        
        return board
    except Exception as e:
        if isinstance(e, InvalidFENError):
            raise
        raise InvalidFENError(f"Failed to parse FEN: {e}")


def generate_image(fen, output_path=None, size=400, theme_file=None, theme_name="wikipedia", player_pov="white"):
    """
    Generate chess board image from FEN notation.
    
    Args:
        fen (str): FEN notation string
        output_path (str, optional): Output file path. If None, uses temp file.
        size (int): Board size in pixels (default: 400)
        theme_file (str, optional): Path to theme JSON file. If None, uses default.
        theme_name (str): Theme name to use (default: "wikipedia")
        player_pov (str): Player perspective - "white" or "black" (default: "white")
    
    Returns:
        str: Path to generated image file
        
    Raises:
        InvalidFENError: If FEN notation is invalid
        ThemeNotFoundError: If theme not found
        ChessImageGeneratorError: If image generation fails
    """
    # Validate player_pov
    if player_pov not in ["white", "black"]:
        raise ChessImageGeneratorError(f"player_pov must be 'white' or 'black', got '{player_pov}'")
    
    # Load theme
    theme = load_theme(theme_file, theme_name)
    
    # Set output path
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.png')
    
    # Parse FEN
    board = parse_fen(fen)
    
    try:
        # Create board image
        img = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        square_size = size // 8
        
        # Get board colors from theme
        light_color, dark_color = theme['board']
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                
                color = light_color if (row + col) % 2 == 0 else dark_color
                draw.rectangle([x1, y1, x2, y2], fill=color)
        
        # Place pieces
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece in PIECE_MAP:
                    piece_key = PIECE_MAP[piece]
                    
                    if piece_key in theme['pieces']:
                        # Decode base64 piece image
                        base64_data = theme['pieces'][piece_key][0]  # Take first item from array
                        piece_img = decode_base64_image(base64_data)
                        
                        # Resize piece to fit square
                        piece_img = piece_img.resize((square_size, square_size), Image.Resampling.LANCZOS)
                        
                        x = col * square_size
                        y = row * square_size
                        
                        # Paste with transparency if available
                        if piece_img.mode == 'RGBA':
                            img.paste(piece_img, (x, y), piece_img)
                        else:
                            img.paste(piece_img, (x, y))
        
        # Rotate image if viewing from black's perspective
        if player_pov == "black":
            img = img.rotate(180)
        
        # Save image
        img.save(output_path, 'PNG')
        return output_path
        
    except Exception as e:
        raise ChessImageGeneratorError(f"Failed to generate image: {e}")


def generate_bytes(fen, size=400, theme_file=None, theme_name="wikipedia", player_pov="white"):
    """
    Generate chess board image as bytes.
    
    Args:
        fen (str): FEN notation string
        size (int): Board size in pixels (default: 400)
        theme_file (str, optional): Path to theme JSON file
        theme_name (str): Theme name to use (default: "wikipedia")
        player_pov (str): Player perspective - "white" or "black" (default: "white")
    
    Returns:
        bytes: PNG image data
    """
    image_path = generate_image(fen, size=size, theme_file=theme_file, theme_name=theme_name, player_pov=player_pov)
    try:
        with open(image_path, 'rb') as f:
            return f.read()
    finally:
        os.unlink(image_path)


def generate_pil(fen, size=400, theme_file=None, theme_name="wikipedia", player_pov="white"):
    """
    Generate chess board as PIL Image object.
    
    Args:
        fen (str): FEN notation string
        size (int): Board size in pixels (default: 400)
        theme_file (str, optional): Path to theme JSON file
        theme_name (str): Theme name to use (default: "wikipedia")
        player_pov (str): Player perspective - "white" or "black" (default: "white")
    
    Returns:
        PIL.Image: Image object
    """
    image_path = generate_image(fen, size=size, theme_file=theme_file, theme_name=theme_name, player_pov=player_pov)
    try:
        return Image.open(image_path)
    finally:
        os.unlink(image_path)


def list_themes(theme_file=None):
    """
    List available themes.
    
    Args:
        theme_file (str, optional): Path to theme JSON file. If None, uses default.
        
    Returns:
        list: Available theme names
    """
    if theme_file is None:
        theme_file = get_default_theme_path()
    
    theme_path = Path(theme_file)
    
    if not theme_path.exists():
        return []
    
    try:
        with open(theme_path, 'r') as f:
            themes = json.load(f)
        return list(themes.keys())
    except:
        return []


def get_theme_info(theme_name="wikipedia", theme_file=None):
    """
    Get information about a specific theme.
    
    Args:
        theme_name (str): Theme name (default: "wikipedia")
        theme_file (str, optional): Path to theme JSON file
        
    Returns:
        dict: Theme information including colors and available pieces
    """
    theme = load_theme(theme_file, theme_name)
    
    return {
        'name': theme_name,
        'board_colors': theme['board'],
        'pieces': list(theme['pieces'].keys()),
        'piece_count': len(theme['pieces'])
    }