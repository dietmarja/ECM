# scripts/curriculum_generator/templates/css_generator.py
"""
CSS generation for curriculum visualizations
"""

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CSSGenerator:
    """Generates CSS styles for curriculum HTML output"""
    
    def __init__(self):
        self.theme_colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'accent': '#e74c3c',
            'warning': '#f39c12',
            'info': '#9b59b6',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
    
    def generate_curriculum_css(self, theme: str = 'modern') -> str:
        """Generate complete CSS for curriculum visualization"""
        
        if theme == 'modern':
            return self._generate_modern_theme_css()
        elif theme == 'classic':
            return self._generate_classic_theme_css()
        else:
            return self._generate_modern_theme_css()
    
    def _generate_modern_theme_css(self) -> str:
        """Generate modern theme CSS"""
        
        return f"""
/* Modern Curriculum Visualization Styles */
:root {{
    --primary-color: {self.theme_colors['primary']};
    --secondary-color: {self.theme_colors['secondary']};
    --accent-color: {self.theme_colors['accent']};
    --warning-color: {self.theme_colors['warning']};
    --info-color: {self.theme_colors['info']};
    --light-color: {self.theme_colors['light']};
    --dark-color: {self.theme_colors['dark']};
    --border-radius: 8px;
    --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}}

/* Reset and Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--dark-color);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-top: 20px;
    margin-bottom: 20px;
}}

/* Header Styles */
.curriculum-header {{
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--light-color);
}}

.curriculum-header h1 {{
    color: var(--dark-color);
    margin-bottom: 15px;
    font-size: 2.5rem;
    font-weight: 700;
}}

.header-badges {{
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}}

.domain-badge,
.topic-badge,
.eqf-badge {{
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    color: white;
}}

.domain-badge {{
    background: var(--primary-color);
}}

.topic-badge {{
    background: var(--secondary-color);
}}

.eqf-badge {{
    background: var(--info-color);
}}

/* Overview Section */
.overview-section {{
    margin-bottom: 40px;
}}

.overview-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}}

.metric-card {{
    background: var(--light-color);
    padding: 25px;
    border-radius: var(--border-radius);
    text-align: center;
    border-left: 4px solid var(--primary-color);
    transition: var(--transition);
}}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--box-shadow);
}}

.metric-card h3 {{
    color: var(--dark-color);
    margin-bottom: 10px;
    font-size: 1rem;
    font-weight: 600;
}}

.metric-value {{
    font-size: 2.2rem;
    font-weight: bold;
    color: var(--primary-color);
    display: block;
}}

.metric-text {{
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--dark-color);
    display: block;
}}

/* Tab Navigation */
.tab-navigation {{
    display: flex;
    background: var(--light-color);
    border-radius: var(--border-radius);
    padding: 5px;
    margin-bottom: 30px;
    overflow-x: auto;
}}

.tab-button {{
    background: transparent;
    border: none;
    padding: 12px 20px;
    cursor: pointer;
    border-radius: calc(var(--border-radius) - 2px);
    font-weight: 500;
    transition: var(--transition);
    white-space: nowrap;
}}

.tab-button:hover {{
    background: rgba(52, 152, 219, 0.1);
}}

.tab-button.active {{
    background: var(--primary-color);
    color: white;
}}

/* Tab Content */
.tab-content {{
    display: none;
    animation: fadeIn 0.3s ease-in;
}}

.tab-content.active {{
    display: block;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Components Table */
.components-table-container {{
    overflow-x: auto;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}}

.components-table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}

.components-table th,
.components-table td {{
    padding: 15px 12px;
    text-align: left;
    border-bottom: 1px solid var(--light-color);
}}

.components-table th {{
    background: var(--dark-color);
    color: white;
    font-weight: 600;
    position: sticky;
    top: 0;
}}

.components-table tr:hover {{
    background: rgba(52, 152, 219, 0.05);
}}

/* Component Type Rows */
.work-based-row {{
    background: rgba(46, 204, 113, 0.1);
}}

.practical-row {{
    background: rgba(243, 156, 18, 0.1);
}}

.theoretical-row {{
    background: rgba(155, 89, 182, 0.1);
}}

.mixed-row {{
    background: rgba(52, 152, 219, 0.1);
}}

/* Badges */
.ects-badge {{
    background: var(--accent-color);
    color: white;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}}

.type-badge {{
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
}}

.type-badge.work-based {{
    background: var(--secondary-color);
}}

.type-badge.practical {{
    background: var(--warning-color);
}}

.type-badge.theoretical {{
    background: var(--info-color);
}}

.type-badge.mixed {{
    background: var(--primary-color);
}}

/* Semester View */
.semester-section {{
    margin-bottom: 30px;
    border: 1px solid var(--light-color);
    border-radius: var(--border-radius);
    overflow: hidden;
}}

.semester-header {{
    background: var(--primary-color);
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.semester-header h3 {{
    margin: 0;
    font-size: 1.2rem;
}}

.semester-ects {{
    background: rgba(255, 255, 255, 0.2);
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.9rem;
}}

.semester-components {{
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}}

/* Component Cards */
.component-card {{
    border: 1px solid var(--light-color);
    border-radius: var(--border-radius);
    padding: 20px;
    transition: var(--transition);
}}

.component-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--box-shadow);
}}

.component-card h4 {{
    margin-bottom: 10px;
    color: var(--dark-color);
}}

.component-details {{
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    align-items: center;
}}

.component-type {{
    background: var(--light-color);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
}}

.component-outcomes ul {{
    margin-left: 20px;
    margin-top: 5px;
}}

.component-outcomes li {{
    margin-bottom: 5px;
    font-size: 0.9rem;
}}

/* Component Card Types */
.work-based-card {{
    border-left: 4px solid var(--secondary-color);
}}

.practical-card {{
    border-left: 4px solid var(--warning-color);
}}

.theoretical-card {{
    border-left: 4px solid var(--info-color);
}}

.mixed-card {{
    border-left: 4px solid var(--primary-color);
}}

/* Pathway Styles */
.pathway-section {{
    margin-bottom: 30px;
}}

.pathway-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}}

.pathway-card {{
    border: 1px solid var(--light-color);
    border-radius: var(--border-radius);
    padding: 20px;
    transition: var(--transition);
}}

.pathway-card:hover {{
    box-shadow: var(--box-shadow);
}}

.pathway-card.vertical {{
    border-left: 4px solid var(--primary-color);
}}

.pathway-card.horizontal {{
    border-left: 4px solid var(--secondary-color);
}}

.pathway-details {{
    display: flex;
    gap: 10px;
    margin: 10px 0;
}}

.eqf-level,
.ects-info {{
    background: var(--light-color);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
}}

/* Competency Styles */
.competency-table-container {{
    overflow-x: auto;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-top: 20px;
}}

.competency-table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}

.competency-table th,
.competency-table td {{
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid var(--light-color);
}}

.competency-table th {{
    background: var(--dark-color);
    color: white;
}}

.framework-badge {{
    background: var(--info-color);
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8rem;
}}

.confidence-high {{
    color: var(--secondary-color);
    font-weight: 600;
}}

.confidence-medium {{
    color: var(--warning-color);
    font-weight: 600;
}}

.confidence-low {{
    color: var(--accent-color);
    font-weight: 600;
}}

/* Assessment Styles */
.assessment-overview {{
    display: grid;
    gap: 30px;
}}

.assessment-summary {{
    background: var(--light-color);
    padding: 20px;
    border-radius: var(--border-radius);
}}

.summary-stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}}

.stat-item {{
    display: flex;
    justify-content: space-between;
    padding: 10px;
    background: white;
    border-radius: 4px;
}}

.stat-label {{
    font-weight: 500;
}}

.stat-value {{
    font-weight: 600;
    color: var(--primary-color);
}}

.methods-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
}}

.method-card {{
    background: var(--light-color);
    padding: 20px;
    border-radius: var(--border-radius);
    text-align: center;
}}

.method-stats {{
    display: flex;
    justify-content: space-around;
    margin-top: 10px;
    font-size: 0.9rem;
}}

/* Footer */
.curriculum-footer {{
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--light-color);
    color: #7f8c8d;
    font-size: 0.9rem;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .container {{
        margin: 10px;
        padding: 15px;
    }}
    
    .curriculum-header h1 {{
        font-size: 2rem;
    }}
    
    .overview-grid {{
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }}
    
    .tab-navigation {{
        flex-direction: column;
    }}
    
    .semester-components {{
        grid-template-columns: 1fr;
    }}
    
    .pathway-grid {{
        grid-template-columns: 1fr;
    }}
}}

@media (max-width: 480px) {{
    .header-badges {{
        flex-direction: column;
        align-items: center;
    }}
    
    .semester-header {{
        flex-direction: column;
        gap: 10px;
    }}
    
    .pathway-details {{
        flex-direction: column;
        gap: 5px;
    }}
}}

/* Print Styles */
@media print {{
    body {{
        background: white;
    }}
    
    .container {{
        box-shadow: none;
        margin: 0;
    }}
    
    .tab-navigation {{
        display: none;
    }}
    
    .tab-content {{
        display: block !important;
        page-break-inside: avoid;
    }}
    
    .component-card,
    .pathway-card {{
        page-break-inside: avoid;
    }}
}}
"""
