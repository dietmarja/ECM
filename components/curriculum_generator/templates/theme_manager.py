# scripts/curriculum_generator/templates/theme_manager.py
"""
Material Design Theme Manager
Handles theme loading and CSS injection for curriculum and profile generation
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class ThemeManager:
    """Manages Material Design themes for DSCG templates"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.themes_config = self._load_theme_config()
        self.available_themes = list(self.themes_config["themes"].keys())
        
        print(f"🎨 ThemeManager initialized with {len(self.available_themes)} themes")
        
    def _load_theme_config(self) -> Dict[str, Any]:
        """Load theme configuration from JSON file"""
        config_path = self.templates_dir / "shared" / "theme_config.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Loaded theme config: {config_path}")
            return config
        else:
            print(f"⚠️ Theme config not found: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Fallback theme configuration"""
        return {
            "themes": {
                "material_gray": {
                    "name": "Material Gray",
                    "css_file": "material_gray.css",
                    "primary_color": "#607D8B"
                }
            },
            "default_theme": "material_gray",
            "fallback_theme": "material_gray"
        }
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with descriptions"""
        themes = {}
        for theme_id, theme_data in self.themes_config["themes"].items():
            themes[theme_id] = theme_data.get("name", theme_id)
        return themes
    
    def get_theme_css(self, theme_name: Optional[str] = None) -> str:
        """Get CSS content for specified theme"""
        
        # Use default theme if none specified
        if not theme_name:
            theme_name = self.themes_config["default_theme"]
        
        # Validate theme exists
        if theme_name not in self.themes_config["themes"]:
            print(f"⚠️ Theme '{theme_name}' not found, using fallback")
            theme_name = self.themes_config["fallback_theme"]
        
        theme_data = self.themes_config["themes"][theme_name]
        css_file = theme_data["css_file"]
        
        # Load theme CSS
        css_paths = [
            self.templates_dir / "shared" / "styles" / css_file,
            self.templates_dir / "shared" / "styles" / "material_components.css"
        ]
        
        combined_css = ""
        for css_path in css_paths:
            if css_path.exists():
                with open(css_path, 'r', encoding='utf-8') as f:
                    combined_css += f"\n/* {css_path.name} */\n"
                    combined_css += f.read()
                    combined_css += "\n"
            else:
                print(f"⚠️ CSS file not found: {css_path}")
        
        print(f"✅ Loaded theme CSS: {theme_name}")
        return combined_css
    
    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """Get detailed information about a theme"""
        return self.themes_config["themes"].get(theme_name, {})
    
    def inject_theme_css(self, html_content: str, theme_name: Optional[str] = None) -> str:
        """Inject theme CSS directly into HTML content"""
        
        theme_css = self.get_theme_css(theme_name)
        
        # Find the closing </head> tag and inject CSS before it
        css_injection = f"""
    <style>
{theme_css}
    </style>
</head>"""
        
        if "</head>" in html_content:
            html_with_theme = html_content.replace("</head>", css_injection)
            print(f"✅ Injected theme CSS into HTML")
            return html_with_theme
        else:
            print("⚠️ No </head> tag found, appending CSS to content")
            return f"<style>{theme_css}</style>\n{html_content}"
