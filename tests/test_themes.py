#!/usr/bin/env python3
"""
Tests for theme functionality in chessboard image generator.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from chessboard_image import (
    load_theme,
    list_themes,
    get_theme_info,
    generate_image,
    ThemeNotFoundError,
    ChessImageGeneratorError
)


class TestThemes:
    """Test cases for theme functionality."""
    
    def test_load_default_theme(self):
        """Test loading default wikipedia theme."""
        theme = load_theme()
        
        assert isinstance(theme, dict)
        assert 'pieces' in theme
        assert 'board' in theme
        assert len(theme['pieces']) == 12  # 6 pieces × 2 colors
        assert len(theme['board']) == 2    # Light and dark colors
    
    def test_load_specific_theme(self):
        """Test loading specific theme by name."""
        themes = list_themes()
        
        for theme_name in themes:
            theme = load_theme(theme_name=theme_name)
            assert isinstance(theme, dict)
            assert 'pieces' in theme
            assert 'board' in theme
    
    def test_theme_structure(self):
        """Test that themes have correct structure."""
        theme = load_theme(theme_name="wikipedia")
        
        # Check pieces structure
        pieces = theme['pieces']
        expected_pieces = [
            'bB', 'bK', 'bN', 'bP', 'bQ', 'bR',  # Black pieces
            'wB', 'wK', 'wN', 'wP', 'wQ', 'wR'   # White pieces
        ]
        
        for piece in expected_pieces:
            assert piece in pieces
            assert isinstance(pieces[piece], list)
            assert len(pieces[piece]) >= 1
            assert pieces[piece][0].startswith('data:image/')
        
        # Check board colors
        board_colors = theme['board']
        assert isinstance(board_colors, list)
        assert len(board_colors) == 2
        
        # Check colors are valid hex
        for color in board_colors:
            assert isinstance(color, str)
            assert color.startswith('#')
            assert len(color) in [4, 7]  # #RGB or #RRGGBB
    
    def test_list_themes(self):
        """Test listing available themes."""
        themes = list_themes()
        
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert 'wikipedia' in themes
        
        # All theme names should be strings
        for theme in themes:
            assert isinstance(theme, str)
            assert len(theme) > 0
    
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
        assert isinstance(info['pieces'], list)
        assert info['piece_count'] == 12
    
    def test_theme_not_found(self):
        """Test handling of non-existent theme."""
        with pytest.raises(ThemeNotFoundError):
            load_theme(theme_name="nonexistent_theme")
        
        with pytest.raises(ThemeNotFoundError):
            get_theme_info("nonexistent_theme")
    
    def test_custom_theme_file(self):
        """Test loading custom theme file."""
        # Create a custom theme
        custom_theme = {
            "test_theme": {
                "pieces": {
                    "bB": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "bK": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "bN": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "bP": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "bQ": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "bR": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wB": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wK": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wN": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wP": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wQ": ["data:image/png;base64,iVBORw0KGgoAAAANS"],
                    "wR": ["data:image/png;base64,iVBORw0KGgoAAAANS"]
                },
                "board": ["#FF0000", "#00FF00"]  # Red and green for testing
            }
        }
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_theme, f)
            temp_theme_file = f.name
        
        try:
            # Test loading custom theme
            theme = load_theme(temp_theme_file, "test_theme")
            assert theme['board'] == ["#FF0000", "#00FF00"]
            
            # Test listing themes from custom file
            themes = list_themes(temp_theme_file)
            assert "test_theme" in themes
            
            # Test theme info from custom file
            info = get_theme_info("test_theme", temp_theme_file)
            assert info['name'] == "test_theme"
            assert info['board_colors'] == ["#FF0000", "#00FF00"]
            
        finally:
            # Cleanup
            os.unlink(temp_theme_file)
    
    def test_invalid_theme_file(self):
        """Test handling of invalid theme file."""
        # Test non-existent file
        with pytest.raises(ThemeNotFoundError):
            load_theme("nonexistent_file.json")
        
        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {")
            invalid_file = f.name
        
        try:
            with pytest.raises(ThemeNotFoundError):
                load_theme(invalid_file)
        finally:
            os.unlink(invalid_file)
    
    def test_theme_colors_valid(self):
        """Test that all theme colors are valid hex colors."""
        themes = list_themes()
        
        for theme_name in themes:
            theme = load_theme(theme_name=theme_name)
            colors = theme['board']
            
            for color in colors:
                # Should be hex color
                assert color.startswith('#')
                # Should be valid length
                assert len(color) in [4, 7]  # #RGB or #RRGGBB
                # Should contain only hex characters
                hex_part = color[1:]
                assert all(c in '0123456789ABCDEFabcdef' for c in hex_part)
    
    def test_base64_pieces_valid(self):
        """Test that piece images are valid base64 data URLs."""
        theme = load_theme(theme_name="wikipedia")
        pieces = theme['pieces']
        
        for piece_name, piece_data in pieces.items():
            assert isinstance(piece_data, list)
            assert len(piece_data) >= 1
            
            data_url = piece_data[0]
            assert isinstance(data_url, str)
            assert data_url.startswith('data:image/')
            assert ',base64,' in data_url or ','.join(data_url.split(',')[:-1]).endswith('base64')
    
    def test_generate_with_different_themes(self):
        """Test generating images with different themes."""
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"  # Simple position
        themes = list_themes()
        
        for theme_name in themes:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                try:
                    output_path = generate_image(
                        fen, 
                        tmp.name, 
                        size=100, 
                        theme_name=theme_name
                    )
                    
                    # Check file was created and has content
                    assert os.path.exists(output_path)
                    assert os.path.getsize(output_path) > 0
                    
                finally:
                    # Cleanup
                    if os.path.exists(tmp.name):
                        os.unlink(tmp.name)
    
    def test_theme_consistency(self):
        """Test that all themes have consistent structure."""
        themes = list_themes()
        
        for theme_name in themes:
            theme = load_theme(theme_name=theme_name)
            
            # All themes should have the same piece keys
            expected_pieces = {
                'bB', 'bK', 'bN', 'bP', 'bQ', 'bR',
                'wB', 'wK', 'wN', 'wP', 'wQ', 'wR'
            }
            
            actual_pieces = set(theme['pieces'].keys())
            assert actual_pieces == expected_pieces, f"Theme {theme_name} missing pieces: {expected_pieces - actual_pieces}"
            
            # All themes should have exactly 2 board colors
            assert len(theme['board']) == 2, f"Theme {theme_name} should have exactly 2 board colors"


if __name__ == "__main__":
    pytest.main([__file__])