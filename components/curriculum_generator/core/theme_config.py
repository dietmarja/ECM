#!/usr/bin/env python3
# scripts/curriculum_generator/core/theme_config.py
"""
Global Theme Configuration for DSCG
Centralized theme management across all systems
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class GlobalThemeConfig:
    """Centralized theme configuration for all DSCG systems"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file = project_root / 'config' / 'global_theme.json'
        self.default_theme = 'material_gray'
        
        # Available themes
        self.available_themes = [
            'material_gray',
            'material_blue', 
            'material_green',
            'material_purple',
            'sustainability_green',
            'digital_blue',
            'corporate_navy'
        ]
        
        # Load or create config
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load existing config or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Create default config
        default_config = {
            'global_theme': self.default_theme,
            'system_themes': {
                'curriculum_generator': self.default_theme,
                'educational_profiles': self.default_theme,
                'web_interface': self.default_theme,
                'deliverables': self.default_theme
            },
            'last_updated': None,
            'available_themes': self.available_themes
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_theme(self, system_name: Optional[str] = None, override_theme: Optional[str] = None) -> str:
        """
        Get theme for a system with override capability
        
        Priority:
        1. override_theme (command line argument)
        2. system-specific theme
        3. global theme
        4. default theme
        """
        if override_theme and override_theme in self.available_themes:
            return override_theme
        
        if system_name and system_name in self.config.get('system_themes', {}):
            return self.config['system_themes'][system_name]
        
        return self.config.get('global_theme', self.default_theme)
    
    def set_global_theme(self, theme: str) -> bool:
        """Set global theme for all systems"""
        if theme not in self.available_themes:
            return False
        
        self.config['global_theme'] = theme
        # Update all system themes to match
        for system in self.config.get('system_themes', {}):
            self.config['system_themes'][system] = theme
        
        self.config['last_updated'] = str(Path(__file__).stat().st_mtime)
        self._save_config(self.config)
        return True
    
    def set_system_theme(self, system_name: str, theme: str) -> bool:
        """Set theme for specific system"""
        if theme not in self.available_themes:
            return False
        
        if 'system_themes' not in self.config:
            self.config['system_themes'] = {}
        
        self.config['system_themes'][system_name] = theme
        self.config['last_updated'] = str(Path(__file__).stat().st_mtime)
        self._save_config(self.config)
        return True
    
    def get_available_themes(self) -> list:
        """Get list of available themes"""
        return self.available_themes.copy()
    
    def get_config_summary(self) -> str:
        """Get human-readable config summary"""
        global_theme = self.config.get('global_theme', self.default_theme)
        system_themes = self.config.get('system_themes', {})
        
        summary = f"🎨 Global Theme Configuration\n"
        summary += f"=" * 40 + "\n"
        summary += f"Global Theme: {global_theme}\n\n"
        summary += f"System-Specific Themes:\n"
        
        for system, theme in system_themes.items():
            summary += f"  {system}: {theme}\n"
        
        summary += f"\nAvailable Themes: {', '.join(self.available_themes)}\n"
        return summary

# Convenience functions for easy integration
def get_theme_for_system(system_name: str, override_theme: Optional[str] = None, project_root: Optional[Path] = None) -> str:
    """Get theme for a system - convenience function"""
    if not project_root:
        project_root = Path(__file__).parent.parent.parent
    
    theme_config = GlobalThemeConfig(project_root)
    return theme_config.get_theme(system_name, override_theme)

def set_global_theme(theme: str, project_root: Optional[Path] = None) -> bool:
    """Set global theme - convenience function"""
    if not project_root:
        project_root = Path(__file__).parent.parent.parent
    
    theme_config = GlobalThemeConfig(project_root)
    return theme_config.set_global_theme(theme)

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file = project_root / 'config' / 'global_theme.json'
        self.default_theme = 'material_gray'
        
        # Import EU themes
        from scripts.curriculum_generator.core.eu_theme_generator import integrate_eu_themes_into_system
        eu_themes = integrate_eu_themes_into_system()
        
        # Enhanced available themes with EU official themes
        self.available_themes = [
            'material_gray',
            'material_blue', 
            'material_green',
            'material_purple',
            'sustainability_green',
            'digital_blue',
            'corporate_navy',
            # EU Official Themes
            'eu_official',        # 🇪🇺 Official EU institutional theme
            'eu_professional',    # 🇪🇺 Professional EU business theme  
            'eu_academic',        # 🇪🇺 Academic EU university theme
            'eu_digital'          # 🇪🇺 Modern EU digital platform theme
        ]
        
        # EU themes metadata
        self.eu_themes_info = {
            'eu_official': {
                'flag': '🇪🇺',
                'category': 'EU Official',
                'description': 'Institutional EU theme using official flag colors',
                'best_for': 'Government, official documents, institutional use',
                'colors': {'primary': '#003399', 'accent': '#FFCC00'}
            },
            'eu_professional': {
                'flag': '🇪🇺',
                'category': 'EU Professional', 
                'description': 'Professional EU theme for business education',
                'best_for': 'Corporate training, professional development',
                'colors': {'primary': '#003399', 'accent': '#FFCC00'}
            },
            'eu_academic': {
                'flag': '🇪🇺',
                'category': 'EU Academic',
                'description': 'Academic EU theme for higher education',
                'best_for': 'Universities, academic institutions, formal education',
                'colors': {'primary': '#003399', 'accent': '#FFCC00'}
            },
            'eu_digital': {
                'flag': '🇪🇺',
                'category': 'EU Digital',
                'description': 'Modern EU theme for digital learning platforms',
                'best_for': 'Online learning, digital platforms, e-learning',
                'colors': {'primary': '#003399', 'accent': '#FFCC00'}
            }
        }
        
        # Load or create config
        self.config = self._load_or_create_config()
    
    def get_eu_themes_info(self) -> Dict[str, Any]:
        """Get information about EU themes"""
        return self.eu_themes_info
    
    def is_eu_theme(self, theme_name: str) -> bool:
        """Check if theme is an EU official theme"""
        return theme_name.startswith('eu_')
    
    def get_config_summary(self) -> str:
        """Get human-readable config summary with EU themes highlighted"""
        global_theme = self.config.get('global_theme', self.default_theme)
        system_themes = self.config.get('system_themes', {})
        
        summary = f"🎨 Global Theme Configuration\n"
        summary += f"=" * 40 + "\n"
        summary += f"Global Theme: {global_theme}"
        if self.is_eu_theme(global_theme):
            eu_info = self.eu_themes_info.get(global_theme, {})
            summary += f" {eu_info.get('flag', '🇪🇺')} {eu_info.get('category', 'EU Theme')}"
        summary += "\n\n"
        
        summary += f"System-Specific Themes:\n"
        for system, theme in system_themes.items():
            eu_indicator = ""
            if self.is_eu_theme(theme):
                eu_info = self.eu_themes_info.get(theme, {})
                eu_indicator = f" {eu_info.get('flag', '🇪🇺')}"
            summary += f"  {system}: {theme}{eu_indicator}\n"
        
        summary += f"\n🇪🇺 EU Official Themes Available:\n"
        for theme_id, info in self.eu_themes_info.items():
            summary += f"  {info['flag']} {theme_id}: {info['description']}\n"
        
        summary += f"\nAll Available Themes: {', '.join(self.available_themes)}\n"
        return summary
