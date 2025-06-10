#!/usr/bin/env python3
"""
Basic usage examples for chessboard image generator.
"""

import chessboard_image as cbi

def main():
    """Demonstrate basic usage of the chessboard image generator."""
    
    print("Chessboard Image - Basic Examples")
    print("=" * 40)
    
    # Example 1: Starting position from White's perspective
    print("\n1. Generating starting position (White's perspective)...")
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    cbi.generate_image(start_fen, "starting_position_white.png", size=400)
    print("✓ Saved: starting_position_white.png")
    
    # Example 2: Starting position from Black's perspective
    print("\n2. Generating starting position (Black's perspective)...")
    cbi.generate_image(start_fen, "starting_position_black.png", size=400, player_pov="black")
    print("✓ Saved: starting_position_black.png")
    
    # Example 3: Famous opening - Sicilian Defense
    print("\n3. Generating Sicilian Defense...")
    sicilian_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    cbi.generate_image(sicilian_fen, "sicilian_defense.png", size=500, theme_name="alpha")
    print("✓ Saved: sicilian_defense.png (using alpha theme)")
    
    # Example 4: Endgame position
    print("\n4. Generating King and Queen vs King endgame...")
    endgame_fen = "8/8/8/8/8/3QK3/8/7k w - - 0 1"
    cbi.generate_image(endgame_fen, "kq_vs_k_endgame.png", size=300)
    print("✓ Saved: kq_vs_k_endgame.png")
    
    # Example 5: Get image as PIL object
    print("\n5. Working with PIL Image object...")
    pil_image = cbi.generate_pil(start_fen, size=200)
    print(f"✓ Generated PIL Image: {pil_image.size} pixels, mode: {pil_image.mode}")
    
    # Example 6: Get image as bytes
    print("\n6. Getting image as bytes...")
    image_bytes = cbi.generate_bytes(endgame_fen, size=150, player_pov="black")
    print(f"✓ Generated {len(image_bytes)} bytes of PNG data (Black's perspective)")
    
    # Example 7: List available themes
    print("\n7. Available themes:")
    themes = cbi.list_themes()
    for theme in themes:
        info = cbi.get_theme_info(theme)
        print(f"   - {theme}: {info['board_colors']} ({info['piece_count']} pieces)")
    
    print("\n" + "=" * 40)
    print("All examples completed successfully!")
    print("Check the generated PNG files in the current directory.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)