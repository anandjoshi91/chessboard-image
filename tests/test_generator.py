#!/usr/bin/env python3
"""
Basic tests for chessboard image generator.
"""

import pytest
import tempfile
import os
from chessboard_image import (
    generate_image,
    generate_bytes,
    generate_pil,
    list_themes,
    get_theme_info,
    InvalidFENError,
    ThemeNotFoundError,
    ChessImageGeneratorError
)


class TestChessboardImage:
    """Test cases for chessboard image generator."""
    
    def test_generate_image_basic(self):
        """Test basic image generation."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            output_path = generate_image(fen, tmp.name, size=200)
            
            # Check file was created
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
            
            # Cleanup
            os.unlink(output_path)
    
    def test_generate_bytes(self):
        """Test generating image as bytes."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"  # Simple position
        
        image_bytes = generate_bytes(fen, size=100)
        
        assert isinstance(image_bytes, bytes)
        assert len(image_bytes) > 0
        assert image_bytes.startswith(b'\x89PNG')  # PNG header
    
    def test_generate_pil(self):
        """Test generating PIL Image object."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        
        pil_image = generate_pil(fen, size=100)
        
        assert pil_image.mode in ['RGB', 'RGBA']
        assert pil_image.size == (100, 100)
    
    def test_different_sizes(self):
        """Test different board sizes."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        
        for size in [200, 400, 600]:
            pil_image = generate_pil(fen, size=size)
            assert pil_image.size == (size, size)
    
    def test_list_themes(self):
        """Test listing available themes."""
        themes = list_themes()
        
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert 'wikipedia' in themes
    
    def test_get_theme_info(self):
        """Test getting theme information."""
        info = get_theme_info('wikipedia')
        
        assert isinstance(info, dict)
        assert 'name' in info
        assert 'board_colors' in info
        assert 'pieces' in info
        assert 'piece_count' in info
        assert info['name'] == 'wikipedia'
        assert len(info['board_colors']) == 2
        assert info['piece_count'] == 12
    
    def test_invalid_fen(self):
        """Test invalid FEN handling."""
        invalid_fens = [
            "",
            "invalid",
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP",  # Missing parts
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/extra w KQkq - 0 1",  # Too many rows
        ]
        
        for fen in invalid_fens:
            with pytest.raises(InvalidFENError):
                generate_bytes(fen)
    
    def test_theme_not_found(self):
        """Test theme not found error."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        
        with pytest.raises(ThemeNotFoundError):
            generate_bytes(fen, theme_name="nonexistent_theme")
    
    def test_different_themes(self):
        """Test using different themes."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        themes = list_themes()
        
        for theme in themes:
            image_bytes = generate_bytes(fen, size=100, theme_name=theme)
            assert len(image_bytes) > 0
    
    def test_coordinates_feature(self):
        """Test board coordinate generation."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        
        # Test without coordinates (default)
        no_coords_bytes = generate_bytes(fen, size=100, show_coordinates=False)
        assert len(no_coords_bytes) > 0
        
        # Test with coordinates
        with_coords_bytes = generate_bytes(fen, size=100, show_coordinates=True)
        assert len(with_coords_bytes) > 0
        
        # Images should be different (with coordinates should be larger)
        assert no_coords_bytes != with_coords_bytes
        
        # Test coordinates with both perspectives
        white_coords = generate_bytes(fen, size=100, player_pov="white", show_coordinates=True)
        black_coords = generate_bytes(fen, size=100, player_pov="black", show_coordinates=True)
        
        # Should be different due to different perspective and coordinate labeling
        assert white_coords != black_coords
    
    def test_coordinates_with_pil(self):
        """Test coordinates with PIL Image output."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        
        # Without coordinates
        img_no_coords = generate_pil(fen, size=100, show_coordinates=False)
        assert img_no_coords.size == (100, 100)
        
        # With coordinates (should be larger due to margin)
        img_with_coords = generate_pil(fen, size=100, show_coordinates=True)
        assert img_with_coords.size == (140, 140)  # 100 + 2*20 margin
    
    def test_player_perspective(self):
        """Test different player perspectives."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        
        # Test white perspective (default)
        white_bytes = generate_bytes(fen, size=100, player_pov="white")
        assert len(white_bytes) > 0
        
        # Test black perspective (flipped board)
        black_bytes = generate_bytes(fen, size=100, player_pov="black")
        assert len(black_bytes) > 0
        
        # Images should be different (board is flipped)
        assert white_bytes != black_bytes
    
    def test_invalid_player_pov(self):
        """Test invalid player perspective values."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        
        with pytest.raises(ChessImageGeneratorError):
            generate_bytes(fen, player_pov="invalid")
        
        with pytest.raises(ChessImageGeneratorError):
            generate_bytes(fen, player_pov="red")
    
    def test_complex_position(self):
        """Test complex chess position."""
        # Position from famous game
        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
        
        pil_image = generate_pil(fen, size=300)
        assert pil_image.size == (300, 300)
    
    def test_endgame_position(self):
        """Test endgame position with few pieces."""
        fen = "8/1B6/8/8/8/8/1K3Qqr/7k w KQkq - 0 1"
        
        image_bytes = generate_bytes(fen, size=250)
        assert len(image_bytes) > 0


if __name__ == "__main__":
    pytest.main([__file__])