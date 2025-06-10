#!/usr/bin/env python3
"""
Command line interface for chessboard image generator.
"""

import argparse
import sys
from . import (
    generate_image, 
    list_themes, 
    get_theme_info,
    __version__,
    InvalidFENError,
    ThemeNotFoundError,
    ChessImageGeneratorError
)


def main():
    """Main command line interface."""
    parser = argparse.ArgumentParser(
        description='Generate chess board images from FEN notation',
        prog='chessboard-image'
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate chess board image')
    gen_parser.add_argument('fen', help='FEN notation string')
    gen_parser.add_argument('-o', '--output', default='chessboard.png', help='Output file path')
    gen_parser.add_argument('-s', '--size', type=int, default=400, help='Board size in pixels')
    gen_parser.add_argument('-t', '--theme', default='wikipedia', help='Theme name')
    gen_parser.add_argument('--theme-file', help='Custom theme file path')
    gen_parser.add_argument('-p', '--player-pov', choices=['white', 'black'], default='white', 
                          help='Player perspective (default: white)')
    gen_parser.add_argument('-c', '--coordinates', action='store_true', 
                          help='Show file/rank coordinates (a-h, 1-8)')
    
    # List themes command
    list_parser = subparsers.add_parser('themes', help='List available themes')
    list_parser.add_argument('--theme-file', help='Custom theme file path')
    
    # Theme info command
    info_parser = subparsers.add_parser('info', help='Get theme information')
    info_parser.add_argument('theme_name', help='Theme name')
    info_parser.add_argument('--theme-file', help='Custom theme file path')
    
    # Examples command
    examples_parser = subparsers.add_parser('examples', help='Show usage examples')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'generate':
            result_path = generate_image(
                args.fen,
                args.output,
                size=args.size,
                theme_name=args.theme,
                theme_file=args.theme_file,
                player_pov=args.player_pov,
                show_coordinates=args.coordinates
            )
            print(f"✓ Chess board image saved: {result_path}")
            print(f"  Theme: {args.theme}")
            print(f"  Size: {args.size}x{args.size}")
            print(f"  Perspective: {args.player_pov.title()}'s view")
            if args.coordinates:
                print(f"  Coordinates: Shown")
            
        elif args.command == 'themes':
            themes = list_themes(args.theme_file)
            if themes:
                print("Available themes:")
                for theme in themes:
                    print(f"  - {theme}")
            else:
                print("No themes found.")
                
        elif args.command == 'info':
            info = get_theme_info(args.theme_name, args.theme_file)
            print(f"Theme: {info['name']}")
            print(f"Board colors: {info['board_colors']}")
            print(f"Pieces: {info['piece_count']} available")
            print(f"Piece codes: {', '.join(info['pieces'])}")
            
        elif args.command == 'examples':
            show_examples()
            
        return 0
        
    except InvalidFENError as e:
        print(f"✗ Invalid FEN: {e}", file=sys.stderr)
        return 1
    except ThemeNotFoundError as e:
        print(f"✗ Theme error: {e}", file=sys.stderr)
        return 1
    except ChessImageGeneratorError as e:
        print(f"✗ Generation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


def show_examples():
    """Show usage examples."""
    examples = [
        ("Starting position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("Sicilian Defense", "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"),
        ("Italian Game", "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"),
        ("King & Queen vs King", "8/8/8/8/8/3QK3/8/7k w - - 0 1"),
    ]
    
    print("Usage Examples:")
    print("=" * 50)
    
    for name, fen in examples:
        print(f"\n{name}:")
        print(f"  chessboard-image generate '{fen}' -o {name.lower().replace(' ', '_')}.png")
    
    print("\nOther commands:")
    print("  chessboard-image themes")
    print("  chessboard-image info wikipedia")
    print("  chessboard-image generate 'FEN' -s 600 -t alpha")
    print("  chessboard-image generate 'FEN' -p black  # Black's perspective")
    print("  chessboard-image generate 'FEN' -c  # Show coordinates")
    print("  chessboard-image generate 'FEN' --player-pov black --coordinates -s 500")


if __name__ == '__main__':
    sys.exit(main())