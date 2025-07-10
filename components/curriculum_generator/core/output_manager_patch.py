# scripts/curriculum_generator/core/output_manager_patch.py
"""
PATCH: Fix EQF alignment display and Profile Type normalization
"""

def patch_competency_eqf_alignment(comp, eqf_level):
    """Ensure all competencies have EQF alignment text"""
    eqf_alignment = comp.get('eqf_alignment', '')
    
    # If no EQF alignment provided, generate appropriate fallback
    if not eqf_alignment:
        comp_level = comp.get('competency_level', 'Proficient')
        if comp_level.lower() == 'advanced':
            eqf_alignment = f"Level {eqf_level}: Advanced specialized skills with autonomous responsibility"
        elif comp_level.lower() == 'expert':
            eqf_alignment = f"Level {eqf_level}: Expert-level mastery with leadership and innovation capability"
        else:  # Proficient
            eqf_alignment = f"Level {eqf_level}: Specialized professional skills with guided autonomy"
    
    return eqf_alignment

def normalize_profile_type_for_display(profile_type):
    """Normalize profile type for better display"""
    if not profile_type:
        return "Standard"
    
    # Convert Enhanced_Standard to Enhanced Standard
    normalized = profile_type.replace('_', ' ')
    
    # Handle common cases
    type_mappings = {
        'Enhanced Standard': 'Enhanced Standard',
        'Enhanced Reduced': 'Reduced Profile', 
        'Fallback': 'Fallback Profile',
        'Standard': 'Standard Profile'
    }
    
    return type_mappings.get(normalized, normalized)
