#!/usr/bin/env python3
# scripts/curriculum_generator/core/eu_theme_generator.py
"""
EU Official Theme Generator
Based on official European Union flag colors and design principles
"""

from typing import Dict, Any

class EUThemeGenerator:
    """Generates EU-compliant themes for educational content"""
    
    def __init__(self):
        # Official EU flag colors
        self.eu_blue = '#003399'      # EU Blue (Pantone 661 C, RAL 5005)
        self.eu_yellow = '#FFCC00'    # EU Yellow (Pantone 116 C, RAL 2007)
        
        # Create EU theme variations
        self.eu_themes = {
            'eu_official': self._create_eu_official_theme(),
            'eu_professional': self._create_eu_professional_theme(),
            'eu_academic': self._create_eu_academic_theme(),
            'eu_digital': self._create_eu_digital_theme()
        }
    
    def _create_eu_official_theme(self) -> Dict[str, Any]:
        """Official EU theme - formal and institutional"""
        return {
            'name': 'EU Official',
            'description': 'Official European Union colors for institutional use',
            'colors': {
                'primary': '#003399',        # EU Blue
                'secondary': '#0066CC',      # Lighter EU Blue
                'accent': '#FFCC00',         # EU Yellow
                'success': '#2E7D32',        # EU Green (sustainable development)
                'warning': '#FFCC00',        # EU Yellow
                'danger': '#C62828',         # EU Red (alerts)
                'info': '#1976D2',           # Information Blue
                'background': '#F8F9FA',     # Very Light Gray
                'surface': '#FFFFFF',        # White
                'text': '#1A1A1A',           # Dark Gray
                'text_secondary': '#003366', # Dark EU Blue
                'border': '#E0E0E0',         # Light Gray
                'border_accent': '#FFCC00'   # EU Yellow borders
            },
            'gradients': {
                'primary': 'linear-gradient(135deg, #003399 0%, #0066CC 100%)',
                'accent': 'linear-gradient(135deg, #FFCC00 0%, #FFD700 100%)',
                'background': 'linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%)'
            },
            'usage': 'official_documents'
        }
    
    def _create_eu_professional_theme(self) -> Dict[str, Any]:
        """Professional EU theme - for business and professional education"""
        return {
            'name': 'EU Professional',
            'description': 'Professional EU theme for business education',
            'colors': {
                'primary': '#003399',        # EU Blue
                'secondary': '#1E3A8A',      # Deep Blue
                'accent': '#FFCC00',         # EU Yellow
                'success': '#047857',        # Professional Green
                'warning': '#F59E0B',        # Professional Amber
                'danger': '#DC2626',         # Professional Red
                'info': '#0369A1',           # Professional Blue
                'background': '#F1F5F9',     # Subtle Blue-Gray
                'surface': '#FFFFFF',        # White
                'text': '#1E293B',           # Slate Gray
                'text_secondary': '#003399', # EU Blue
                'border': '#CBD5E1',         # Light Blue-Gray
                'border_accent': '#FFCC00'   # EU Yellow
            },
            'gradients': {
                'primary': 'linear-gradient(135deg, #003399 0%, #1E3A8A 100%)',
                'accent': 'linear-gradient(135deg, #FFCC00 0%, #F59E0B 100%)',
                'background': 'linear-gradient(135deg, #F1F5F9 0%, #FFFFFF 100%)'
            },
            'usage': 'professional_training'
        }
    
    def _create_eu_academic_theme(self) -> Dict[str, Any]:
        """Academic EU theme - for universities and formal education"""
        return {
            'name': 'EU Academic',
            'description': 'Academic EU theme for higher education institutions',
            'colors': {
                'primary': '#003399',        # EU Blue
                'secondary': '#2563EB',      # Academic Blue
                'accent': '#FFCC00',         # EU Yellow
                'success': '#059669',        # Academic Green
                'warning': '#D97706',        # Academic Orange
                'danger': '#DC2626',         # Academic Red
                'info': '#0284C7',           # Academic Sky Blue
                'background': '#F8FAFC',     # Academic Light
                'surface': '#FFFFFF',        # White
                'text': '#0F172A',           # Academic Dark
                'text_secondary': '#003366', # Dark EU Blue
                'border': '#E2E8F0',         # Academic Border
                'border_accent': '#FFCC00'   # EU Yellow
            },
            'gradients': {
                'primary': 'linear-gradient(135deg, #003399 0%, #2563EB 100%)',
                'accent': 'linear-gradient(135deg, #FFCC00 0%, #FCD34D 100%)',
                'background': 'linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)'
            },
            'usage': 'academic_institutions'
        }
    
    def _create_eu_digital_theme(self) -> Dict[str, Any]:
        """Digital EU theme - for online learning and digital platforms"""
        return {
            'name': 'EU Digital',
            'description': 'Modern EU theme for digital learning platforms',
            'colors': {
                'primary': '#003399',        # EU Blue
                'secondary': '#3B82F6',      # Modern Blue
                'accent': '#FFCC00',         # EU Yellow
                'success': '#10B981',        # Digital Green
                'warning': '#F59E0B',        # Digital Amber
                'danger': '#EF4444',         # Digital Red
                'info': '#06B6D4',           # Digital Cyan
                'background': '#F9FAFB',     # Digital Light
                'surface': '#FFFFFF',        # White
                'text': '#111827',           # Digital Dark
                'text_secondary': '#003399', # EU Blue
                'border': '#D1D5DB',         # Digital Border
                'border_accent': '#FFCC00'   # EU Yellow
            },
            'gradients': {
                'primary': 'linear-gradient(135deg, #003399 0%, #3B82F6 100%)',
                'accent': 'linear-gradient(135deg, #FFCC00 0%, #FDE047 100%)',
                'background': 'linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%)'
            },
            'usage': 'digital_platforms'
        }
    
    def get_all_eu_themes(self) -> Dict[str, Dict[str, Any]]:
        """Get all EU themes"""
        return self.eu_themes
    
    def get_eu_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get specific EU theme"""
        return self.eu_themes.get(theme_name, self.eu_themes['eu_official'])
    
    def generate_css_variables(self, theme_name: str) -> str:
        """Generate CSS variables for EU theme"""
        theme = self.get_eu_theme(theme_name)
        colors = theme['colors']
        gradients = theme.get('gradients', {})
        
        css_vars = ":root {\n"
        css_vars += f"  /* {theme['name']} Theme - {theme['description']} */\n"
        
        # Color variables
        for var_name, color_value in colors.items():
            css_var_name = f"--{var_name.replace('_', '-')}"
            css_vars += f"  {css_var_name}: {color_value};\n"
        
        # Gradient variables
        for grad_name, grad_value in gradients.items():
            css_var_name = f"--gradient-{grad_name.replace('_', '-')}"
            css_vars += f"  {css_var_name}: {grad_value};\n"
        
        # EU-specific variables
        css_vars += f"\n  /* EU Official Colors */\n"
        css_vars += f"  --eu-blue: {self.eu_blue};\n"
        css_vars += f"  --eu-yellow: {self.eu_yellow};\n"
        css_vars += f"  --eu-blue-rgb: 0, 51, 153;\n"
        css_vars += f"  --eu-yellow-rgb: 255, 204, 0;\n"
        
        css_vars += "}"
        
        return css_vars
    
    def generate_theme_preview(self, theme_name: str) -> str:
        """Generate HTML preview of EU theme"""
        theme = self.get_eu_theme(theme_name)
        colors = theme['colors']
        
        html = f"""
        <div style="padding: 20px; font-family: Arial, sans-serif;">
            <h3 style="color: {colors['primary']}; margin-bottom: 20px;">
                🇪🇺 {theme['name']} Theme Preview
            </h3>
            <p style="color: {colors['text_secondary']}; margin-bottom: 20px;">
                {theme['description']}
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="background: {colors['primary']}; color: white; padding: 15px; border-radius: 8px;">
                    <strong>Primary</strong><br>{colors['primary']}
                </div>
                <div style="background: {colors['secondary']}; color: white; padding: 15px; border-radius: 8px;">
                    <strong>Secondary</strong><br>{colors['secondary']}
                </div>
                <div style="background: {colors['accent']}; color: {colors['text']}; padding: 15px; border-radius: 8px;">
                    <strong>Accent</strong><br>{colors['accent']}
                </div>
                <div style="background: {colors['success']}; color: white; padding: 15px; border-radius: 8px;">
                    <strong>Success</strong><br>{colors['success']}
                </div>
            </div>
            
            <div style="background: {colors['surface']}; border: 2px solid {colors['border']}; border-radius: 8px; padding: 20px;">
                <h4 style="color: {colors['primary']}; margin-top: 0;">Sample Content</h4>
                <p style="color: {colors['text']};">
                    This is how text appears in the {theme['name']} theme. 
                    <span style="color: {colors['text_secondary']};">Secondary text uses EU blue.</span>
                </p>
                <button style="background: {colors['primary']}; color: white; border: none; padding: 10px 20px; border-radius: 5px; margin-right: 10px;">
                    Primary Button
                </button>
                <button style="background: {colors['accent']}; color: {colors['text']}; border: none; padding: 10px 20px; border-radius: 5px;">
                    Accent Button
                </button>
            </div>
        </div>
        """
        
        return html

# Integration function for existing theme system
def integrate_eu_themes_into_system():
    """Integrate EU themes into the existing theme configuration system"""
    
    eu_generator = EUThemeGenerator()
    eu_themes = eu_generator.get_all_eu_themes()
    
    # Convert to format expected by existing theme system
    integrated_themes = {}
    
    for theme_id, theme_data in eu_themes.items():
        integrated_themes[theme_id] = {
            'name': theme_data['name'],
            'description': theme_data['description'],
            'colors': {
                'primary': theme_data['colors']['primary'],
                'secondary': theme_data['colors']['secondary'],
                'accent': theme_data['colors']['accent'],
                'background': theme_data['colors']['background'],
                'surface': theme_data['colors']['surface'],
                'text': theme_data['colors']['text'],
                'border': theme_data['colors']['border']
            },
            'eu_official': True,
            'compliance': 'EU_institutional_guidelines',
            'usage': theme_data.get('usage', 'general')
        }
    
    return integrated_themes
