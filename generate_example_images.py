#!/usr/bin/env python3
"""
Generate example images for chessboard-image package documentation.
Creates theme showcases and example position images in examples/images/
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import chessboard_image as cbi

def create_directory():
    """Create examples/images directory if it doesn't exist"""
    os.makedirs("examples/images", exist_ok=True)
    print("📁 Created examples/images/ directory")

def generate_theme_examples():
    """Generate starting position for each theme"""
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    themes = cbi.list_themes()
    
    print(f"\n🎨 Generating theme examples for {len(themes)} themes...")
    
    for theme in themes:
        filename = f"examples/images/theme_{theme}.png"
        cbi.generate_image(start_fen, filename, size=400, theme_name=theme)
        print(f"✓ Generated {filename}")

def generate_position_examples():
    """Generate example positions showcasing different features"""
    
    print("\n🏁 Generating position examples...")
    
    examples = [
        # Basic examples
        {
            "name": "starting_position",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "size": 400,
            "description": "Starting position"
        },
        {
            "name": "starting_position_coords",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 
            "size": 400,
            "show_coordinates": True,
            "description": "Starting position with coordinates"
        },
        {
            "name": "starting_position_black_pov",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "size": 400,
            "player_pov": "black",
            "show_coordinates": True,
            "description": "Starting position from Black's perspective"
        },
        
        # Famous positions
        {
            "name": "scholars_mate",
            "fen": "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 1",
            "size": 400,
            "show_coordinates": True,
            "description": "Scholar's Mate"
        },
        {
            "name": "sicilian_defense", 
            "fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
            "size": 400,
            "theme_name": "alpha",
            "description": "Sicilian Defense (Alpha theme)"
        },
        {
            "name": "endgame_position",
            "fen": "8/1p1b4/p7/3ppk2/6p1/2P4p/PP3B1K/5B2 b - - 0 1",
            "size": 400,
            "player_pov": "black",
            "show_coordinates": True,
            "description": "Endgame position from Black's perspective"
        },
        
        # Different themes showcase
        {
            "name": "ruy_lopez_wikipedia",
            "fen": "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
            "size": 400,
            "theme_name": "wikipedia",
            "description": "Ruy Lopez (Wikipedia theme)"
        },
        {
            "name": "french_defense_alpha",
            "fen": "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3",
            "size": 400,
            "theme_name": "alpha", 
            "description": "French Defense (Alpha theme)"
        }
    ]
    
    for example in examples:
        filename = f"examples/images/{example['name']}.png"
        
        # Extract parameters
        params = {
            "fen": example["fen"],
            "output_path": filename,
            "size": example.get("size", 400),
            "theme_name": example.get("theme_name", "wikipedia"),
            "player_pov": example.get("player_pov", "white"),
            "show_coordinates": example.get("show_coordinates", False)
        }
        
        cbi.generate_image(**params)
        print(f"✓ Generated {filename} - {example['description']}")

def generate_comparison_examples():
    """Generate side-by-side comparison examples"""
    
    print("\n🔄 Generating comparison examples...")
    
    # White vs Black perspective
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
    
    cbi.generate_image(fen, "examples/images/comparison_white_pov.png", 
                      size=400, show_coordinates=True, player_pov="white")
    print("✓ Generated comparison_white_pov.png")
    
    cbi.generate_image(fen, "examples/images/comparison_black_pov.png",
                      size=400, show_coordinates=True, player_pov="black") 
    print("✓ Generated comparison_black_pov.png")
    
    # With and without coordinates
    cbi.generate_image(fen, "examples/images/comparison_no_coords.png",
                      size=400, show_coordinates=False)
    print("✓ Generated comparison_no_coords.png")
    
    cbi.generate_image(fen, "examples/images/comparison_with_coords.png", 
                      size=400, show_coordinates=True)
    print("✓ Generated comparison_with_coords.png")

def generate_cli_examples():
    """Generate examples that demonstrate CLI usage"""
    
    print("\n💻 Generating CLI demonstration examples...")
    
    # These show what CLI commands would generate
    examples = [
        {
            "file": "cli_basic.png",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "size": 400,
            "description": "CLI: Basic generation"
        },
        {
            "file": "cli_with_options.png", 
            "fen": "8/1B6/8/8/8/8/1K3Qqr/7k w KQkq - 0 1",
            "size": 500,
            "theme_name": "alpha",
            "player_pov": "black",
            "show_coordinates": True,
            "description": "CLI: All options (-s 500 -t alpha -p black -c)"
        }
    ]
    
    for example in examples:
        cbi.generate_image(
            example["fen"],
            f"examples/images/{example['file']}",
            size=example.get("size", 400),
            theme_name=example.get("theme_name", "wikipedia"),
            player_pov=example.get("player_pov", "white"),
            show_coordinates=example.get("show_coordinates", False)
        )
        print(f"✓ Generated {example['file']} - {example['description']}")

def create_image_index():
    """Create an index file describing all generated images"""
    
    index_content = """# Example Images Index

This directory contains example images generated by the chessboard-image package.

## Theme Examples
- `theme_wikipedia.png` - Starting position with Wikipedia theme (default)
- `theme_alpha.png` - Starting position with Alpha theme  
- `theme_uscf.png` - Starting position with USCF theme
- `theme_wisteria.png` - Starting position with Wisteria theme
- `theme_sakura.png` - Starting position with Sakura theme

## Position Examples
- `starting_position.png` - Basic starting position
- `starting_position_coords.png` - Starting position with coordinates
- `starting_position_black_pov.png` - Starting position from Black's perspective
- `scholars_mate.png` - Scholar's Mate position with coordinates
- `sicilian_defense.png` - Sicilian Defense with Alpha theme
- `endgame_position.png` - Endgame from Black's perspective with coordinates

## Comparison Examples
- `comparison_white_pov.png` - Position from White's perspective
- `comparison_black_pov.png` - Same position from Black's perspective  
- `comparison_no_coords.png` - Position without coordinates
- `comparison_with_coords.png` - Same position with coordinates

## CLI Examples
- `cli_basic.png` - Basic CLI usage result
- `cli_with_options.png` - CLI with all options enabled

All images are 400x400 pixels unless otherwise noted.
"""
    
    with open("examples/images/README.md", "w") as f:
        f.write(index_content)
    
    print("✓ Created examples/images/README.md index file")

def main():
    """Generate all example images"""
    print("🎯 Generating example images for chessboard-image package...")
    
    try:
        create_directory()
        generate_theme_examples()
        generate_position_examples()
        generate_comparison_examples()
        generate_cli_examples()
        create_image_index()
        
        print("\n🎉 All example images generated successfully!")
        print("📁 Check the examples/images/ directory")
        
        # Count generated images
        import glob
        image_count = len(glob.glob("examples/images/*.png"))
        print(f"📊 Generated {image_count} PNG images")
        
    except Exception as e:
        print(f"❌ Error generating examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())