"""
Chessboard Image - Generate beautiful chess board images from FEN notation.

A pure Python library for creating chess board images using customizable themes
with base64-encoded pieces and board colors. No external dependencies except PIL.

Example:
    >>> from chessboard_image import generate_image
    >>> generate_image("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "board.png")
    'board.png'
"""

from .generator import (
    generate_image,
    generate_bytes,
    generate_pil,
    list_themes,
    get_theme_info,
    load_theme,
    ChessImageGeneratorError,
    ThemeNotFoundError,
    InvalidFENError,
    __version__,
    __author__,
    __email__
)

__all__ = [
    'generate_image',
    'generate_bytes', 
    'generate_pil',
    'list_themes',
    'get_theme_info',
    'load_theme',
    'ChessImageGeneratorError',
    'ThemeNotFoundError', 
    'InvalidFENError',
    '__version__'
]

# Convenience aliases
fen_to_image = generate_image
fen_to_bytes = generate_bytes
fen_to_pil = generate_pil