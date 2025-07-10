# scripts/curriculum_generator/components/enhanced_html_generator.py
"""
Enhanced HTML Generator with UOL Explanations
Adds comprehensive UOL explanations to generated curricula
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.curriculum_generator.components.uol_explanation_generator import UOLExplanationGenerator

def enhance_curriculum_html_with_uol_explanation(original_html: str, curriculum_data: dict) -> str:
    """Add UOL explanation to curriculum HTML"""
    
    explanation_generator = UOLExplanationGenerator()
    
    # Generate UOL explanation section
    uol_html = explanation_generator.generate_html_explanation_section(
        curriculum_data, "learner_focused"
    )
    
    # Find insertion point (after header, before curriculum content)
    insertion_markers = [
        '<div class="curriculum-content">',
        '<div class="main-content">',
        '<main>',
        '<body>'
    ]
    
    for marker in insertion_markers:
        if marker in original_html:
            # Insert UOL explanation after the marker
            enhanced_html = original_html.replace(
                marker,
                f"{marker}\n{uol_html}\n"
            )
            return enhanced_html
    
    # Fallback: add at the beginning of body content
    if '<body>' in original_html:
        return original_html.replace('<body>', f'<body>\n{uol_html}\n')
    
    # Last resort: prepend to content
    return f"{uol_html}\n{original_html}"

def add_uol_explanation_to_json(curriculum_data: dict) -> dict:
    """Add UOL explanation to curriculum JSON data"""
    
    explanation_generator = UOLExplanationGenerator()
    
    # Add learner-focused explanation
    learner_explanation = explanation_generator.generate_uol_explanation_for_curriculum(
        curriculum_data, "learner_focused"
    )
    
    # Add institution-focused explanation
    institution_explanation = explanation_generator.generate_uol_explanation_for_curriculum(
        curriculum_data, "institution_focused"
    )
    
    # Add to curriculum data
    enhanced_curriculum = curriculum_data.copy()
    enhanced_curriculum["uol_explanations"] = {
        "for_learners": learner_explanation,
        "for_institutions": institution_explanation,
        "explanation_version": "v1.0",
        "generated_timestamp": explanation_generator.explanations["learner_focused"].get("timestamp", "2025-06-07")
    }
    
    return enhanced_curriculum
