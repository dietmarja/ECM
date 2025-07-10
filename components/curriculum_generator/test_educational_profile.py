# test_educational_profile.py
from pathlib import Path
from components.docx_generator import DocxGenerator
import json

def adapt_profile_structure(original_profile):
    """Adapt the JSON profile structure to what DocxGenerator expects"""
    
    # Extract learning outcomes for EQF level 7 (default)
    learning_outcomes_by_eqf = original_profile.get('learning_outcomes_by_eqf', {})
    eqf_7_outcomes = learning_outcomes_by_eqf.get('7', [])
    
    # Extract core competencies
    core_competency_areas = original_profile.get('core_competency_areas', [])
    
    # Create the adapted structure
    adapted_profile = {
        'role_definition': {
            'id': original_profile.get('id', 'ROLE'),
            'name': original_profile.get('profile_name', 'Professional'),
            'description': original_profile.get('role_description', 'Professional role'),
            'main_area': 'Digital Sustainability'
        },
        'metadata': {
            'eqf_level': 7,  # Default to EQF 7 for DSL
            'role_name': original_profile.get('profile_name', 'Professional')
        },
        'enhanced_competencies': {
            'core_competencies': [
                {'name': area, 'description': f'Professional competency in {area.lower()}'}
                for area in core_competency_areas
            ],
            'learning_outcomes': eqf_7_outcomes,
            'framework_mappings': original_profile.get('framework_alignment', {})
        },
        'realistic_career_progression': original_profile.get('career_progression', {}),
        'typical_employers': {
            'primary_sectors': original_profile.get('industry_application', [])
        },
        'cpd_requirements': {
            'certification_maintenance': {
                'renewal_period_years': 3,
                'cpd_hours_required': 40
            }
        }
    }
    
    return adapted_profile

# Load sample profile data
with open('../../input/educational_profiles/educational_profiles.json', 'r') as f:
    profiles_data = json.load(f)

print(f"Loaded data type: {type(profiles_data)}")
print(f"Number of profiles: {len(profiles_data)}")

# Find DSL profile in the list
dsl_profile = None
for profile in profiles_data:
    if profile.get('id') == 'DSL':
        print("Found DSL profile!")
        print(f"Profile name: {profile.get('profile_name')}")
        print(f"Core competency areas: {profile.get('core_competency_areas', [])}")
        
        # Adapt the structure
        dsl_profile = adapt_profile_structure(profile)
        break

if dsl_profile:
    print("Generating CEN/TS 17 compliant DOCX...")
    generator = DocxGenerator(Path('../../'))
    output_path = Path('../../output/compact_appendix/test_dsl_profile_cen_ts_17.docx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    result = generator.generate_educational_profile_docx(dsl_profile, output_path)
    print(f'✅ CEN/TS 17 compliant profile generated: {result}')
else:
    print('❌ DSL profile not found')
    print('Available profile IDs:')
    for profile in profiles_data:
        print(f'  - {profile.get("id", "unknown")}: {profile.get("profile_name", "unknown")}')
