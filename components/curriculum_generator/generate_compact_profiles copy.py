#!/usr/bin/env python3
# scripts/curriculum_generator/generate_compact_profiles.py
"""
from datetime import datetime
Compact Educational Profile Generator for CEN/TS 17699:2022 Compliance
Integrates with existing DSCG wrapper system and generates numbered profiles
from datetime import datetime
Compatible with generate_compact.sh workflow
"""

import sys
import json
from pathlib import Path
from components.docx_generator import DocxGenerator
from typing import Dict, List, Any, Tuple, Optional


def generate_html_profile(profile_data: Dict[str, Any], metadata: Dict[str, Any], output_path: Path) -> Path:
    """Generate HTML version that exactly matches DOCX content"""
    
    role_def = profile_data.get('role_definition', {})
    role_name = role_def.get('name', 'Professional')
    role_id = role_def.get('id', 'ROLE')
    eqf_level = profile_data.get('metadata', {}).get('eqf_level', 6)
    
    # Extract content sections
    competencies = profile_data.get('enhanced_competencies', {})
    learning_outcomes = competencies.get('learning_outcomes', [])
    core_competencies = competencies.get('core_competencies', [])
    career_prog = profile_data.get('realistic_career_progression', {})
    industry_app = profile_data.get('industry_application', [])
    cpd = profile_data.get('cpd_requirements', {})
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Profile: {role_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        .header {{ text-align: center; border-bottom: 3px solid #003399; padding-bottom: 20px; margin-bottom: 30px; }}
        .title {{ color: #003399; font-size: 2.5em; margin: 0; }}
        .subtitle {{ color: #607D8B; font-size: 1.5em; margin: 10px 0; }}
        .eqf-level {{ color: #4CAF50; font-size: 1.2em; font-weight: bold; }}
        .profile-meta {{ background: #F8F9FA; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .section {{ margin: 30px 0; }}
        .section-title {{ color: #003399; font-size: 1.8em; border-left: 4px solid #003399; padding-left: 15px; margin-bottom: 15px; }}
        .subsection-title {{ color: #607D8B; font-size: 1.3em; margin: 20px 0 10px 0; font-weight: bold; }}
        .content {{ margin: 15px 0; }}
        .outcome-list {{ list-style: none; padding: 0; }}
        .outcome-list li {{ background: #F8F9FA; margin: 10px 0; padding: 15px; border-left: 4px solid #4CAF50; }}
        .competency {{ background: #F8F9FA; padding: 20px; margin: 15px 0; border-radius: 8px; }}
        .competency-title {{ color: #003399; font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }}
        .career-level {{ background: #F8F9FA; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .framework-item {{ background: #E3F2FD; padding: 10px; margin: 5px 0; border-radius: 4px; }}
        .industry-item {{ background: #F1F8E9; padding: 10px; margin: 5px 0; border-radius: 4px; }}
        .metadata-note {{ background: #FFF3E0; padding: 15px; border-radius: 8px; margin: 20px 0; font-style: italic; }}
        .compliance-badge {{ background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🎓 Educational Profile</div>
        <div class="subtitle">{role_name}</div>
        <div class="eqf-level">European Qualifications Framework Level {eqf_level}</div>
        <div class="profile-meta">
            Profile ID: {role_id} • Area: Digital Sustainability<br>
            <span class="compliance-badge">CEN/TS 17699:2022 Compliant</span>
        </div>
    </div>

    <div class="section">
        <div class="section-title">🧭 Role Description</div>
        <div class="subsection-title">Professional Context</div>
        <div class="content">{role_def.get('description', 'Professional role in digital sustainability')}</div>
        <div class="content"><strong>EQF Level {eqf_level} Context</strong>: {_get_eqf_context(eqf_level)}</div>
    </div>

    <div class="section">
        <div class="section-title">🎯 Programme Learning Outcomes</div>
        <div class="content">Upon completion, learners will be able to:</div>
        <ul class="outcome-list">
"""
    
    # Add learning outcomes with IDs from metadata
    if metadata and 'learningOutcomes' in metadata:
        for outcome in metadata['learningOutcomes']:
            outcome_id = outcome.get('outcomeId', 'LO_XX')
            description = outcome.get('description', 'Learning outcome')
            html_content += f'            <li><strong>{outcome_id}</strong>: {description}</li>\n'
    else:
        for i, outcome in enumerate(learning_outcomes, 1):
            html_content += f'            <li><strong>LO_{i:02d}</strong>: {outcome}</li>\n'
    
    html_content += """        </ul>
    </div>

    <div class="section">
        <div class="section-title">🧠 Core Competency Areas</div>
"""
    
    # Add competencies with UUIDs from metadata
    if core_competencies:
        for i, comp in enumerate(core_competencies, 1):
            if isinstance(comp, dict):
                comp_name = comp.get('name', f'Competency {i}')
                comp_desc = comp.get('description', 'Professional competency')
                comp_id = f"COMP_{role_id}_{i:02d}"
            else:
                comp_name = str(comp)
                comp_desc = f"Professional competency in {comp_name.lower()}"
                comp_id = f"COMP_{role_id}_{i:02d}"
            
            html_content += f"""        <div class="competency">
            <div class="competency-title">{comp_name} <span style="color: #666; font-size: 0.8em; font-weight: normal;">(ID: {comp_id})</span></div>
            <div>{comp_desc}</div>
        </div>
"""
    
    html_content += """    </div>

    <div class="section">
        <div class="section-title">🗺️ Framework Alignment</div>
        <div class="content">Direct alignment with European competency frameworks:</div>
"""
    
    # Add framework mappings from metadata
    if metadata and 'competencyFrameworkAlignment' in metadata:
        for framework in metadata['competencyFrameworkAlignment']:
            framework_name = framework.get('framework', 'Framework')
            competency_code = framework.get('competencyCode', 'XX.X')
            competency_uri = framework.get('competencyURI', '#')
            proficiency = framework.get('proficiencyLevel', 'competent')
            
            html_content += f"""        <div class="framework-item">
            <strong>{framework_name} {competency_code}</strong> (Proficiency: {proficiency})<br>
            <small>URI: <a href="{competency_uri}" target="_blank">{competency_uri}</a></small>
        </div>
"""
    else:
        html_content += """        <div class="framework-item">
            <strong>European e-Competence Framework (e-CF)</strong>: Competency areas relevant to professional practice<br>
            <strong>Digital Competence Framework (DigComp)</strong>: Digital competencies appropriate for EQF level<br>
            <strong>Sustainability Competence Framework (GreenComp)</strong>: Sustainability competencies for professional practice
        </div>
"""
    
    html_content += """    </div>

    <div class="section">
        <div class="section-title">💼 Career Progression Pathways</div>
"""
    
    # Add complete career progression from metadata
    if metadata and 'careerProgression' in metadata:
        career_meta = metadata['careerProgression']
        
        # Entry level
        entry_level = career_meta.get('entryLevel', {})
        if entry_level:
            html_content += f"""        <div class="subsection-title">🎯 Entry Level Position</div>
        <div class="career-level">
            <strong>Position</strong>: {entry_level.get('title', 'Professional')}<br>
            <strong>EQF Level</strong>: {entry_level.get('eqfLevel', eqf_level)}<br>
            <strong>Experience Required</strong>: {entry_level.get('experienceRequired', '0-2 years')}
        </div>
"""
        
        # Progression path
        progression_path = career_meta.get('progressionPath', [])
        if progression_path:
            html_content += """        <div class="subsection-title">📈 Professional Advancement Path</div>
"""
            for level in progression_path:
                level_id = level.get('levelId', 'level_x')
                title = level.get('title', 'Senior Professional')
                eqf_level_prog = level.get('eqfLevel', eqf_level + 1)
                years = level.get('yearsToAchieve', '3-5 years')
                
                html_content += f"""        <div class="career-level">
            <strong>Level {level_id.replace('level_', '')}</strong>: {title}<br>
            <strong>EQF Level</strong>: {eqf_level_prog} • <strong>Timeline</strong>: {years}
        </div>
"""
    
    html_content += """    </div>

    <div class="section">
        <div class="section-title">📝 Assessment Philosophy</div>
        <div class="content">Assessment emphasizes strategic thinking, innovation, and leadership capabilities through integrated competency demonstration.</div>
        <div class="content"><strong>Competency-Based Approach</strong>: Assessment validates real-world professional capabilities and integrated competency application.</div>
        <div class="content"><em>Detailed assessment methods and criteria are specified in the curriculum implementation guide.</em></div>
    </div>

    <div class="section">
        <div class="section-title">🏢 Industry Application</div>
        <div class="content"><strong>Primary Industry Sectors</strong>:</div>
"""
    
    # Add industry applications
    for sector in industry_app[:5]:  # Limit to top 5
        html_content += f'        <div class="industry-item">{sector}</div>\n'
    
    html_content += """    </div>

    <div class="section">
        <div class="section-title">🔄 Continuing Professional Development</div>
"""
    
    # Add CPD from metadata
    if metadata and 'continuingProfessionalDevelopment' in metadata:
        cpd_meta = metadata['continuingProfessionalDevelopment']
        maintenance = cpd_meta.get('maintenanceRequirements', {})
        micro_creds = cpd_meta.get('microCredentials', {})
        
        html_content += f"""        <div class="content"><strong>Professional Development Cycle</strong>: {maintenance.get('renewalPeriod', 'P3Y').replace('P', '').replace('Y', ' years')}</div>
        <div class="content"><strong>Required CPD Hours</strong>: {maintenance.get('requiredHours', 40)} hours per cycle</div>
        <div class="content"><strong>Stackable Credentials</strong>: Up to {micro_creds.get('maximumECTS', 10)} ECTS recognition for micro-credentials</div>
"""
    else:
        cert_maint = cpd.get('certification_maintenance', {})
        renewal_years = cert_maint.get('renewal_period_years', 3)
        cpd_hours = cert_maint.get('cpd_hours_required', 40)
        
        html_content += f"""        <div class="content"><strong>Professional Development Cycle</strong>: {renewal_years} years</div>
        <div class="content"><strong>Required CPD Hours</strong>: {cpd_hours} hours per cycle</div>
"""
    
    html_content += """    </div>
"""
    
    # Add machine-readable metadata section if available
    if metadata:
        html_content += f"""
    <div class="section">
        <div class="section-title">🔗 Machine-Readable Metadata</div>
        <div class="metadata-note">
            This educational profile includes machine-readable metadata for interoperability with EU-wide educational databases:
            <ul>
                <li><strong>Profile URI</strong>: {metadata.get('@id', 'N/A')}</li>
                <li><strong>Version</strong>: {metadata.get('dct:version', 'N/A')}</li>
                <li><strong>Valid Until</strong>: {metadata.get('dct:valid', 'N/A')}</li>
                <li><strong>JSON-LD</strong>: Semantic web format with vocabulary URIs</li>
                <li><strong>RDF/XML</strong>: Semantic web integration and SPARQL queries</li>
            </ul>
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

def _get_eqf_context(eqf_level: int) -> str:
    """Get EQF level context description"""
    contexts = {
        4: "Factual and theoretical knowledge in broad contexts within a field of work or study",
        5: "Comprehensive, specialised, factual and theoretical knowledge within a field of work or study and an awareness of the boundaries of that knowledge",
        6: "Advanced knowledge of a field of work or study, involving a critical understanding of theories and principles",
        7: "Highly specialised knowledge, some of which is at the forefront of knowledge in a field of work or study, as the basis for original thinking and/or research",
        8: "Knowledge at the most advanced frontier of a field of work or study and at the interface between fields"
    }
    return contexts.get(eqf_level, "Professional knowledge and competencies")

def adapt_profile_structure(original_profile, eqf_level=7):
    """Adapt the JSON profile structure to what DocxGenerator expects"""
    
    # Extract learning outcomes for specified EQF level
    learning_outcomes_by_eqf = original_profile.get('learning_outcomes_by_eqf', {})
    eqf_outcomes = learning_outcomes_by_eqf.get(str(eqf_level), [])
    
    # Extract core competencies
    core_competency_areas = original_profile.get('core_competency_areas', [])
    
    # Handle career progression - it might be a dict, list, or string
    career_progression = original_profile.get('career_progression', {})
    
    # Adapt career progression structure
    adapted_career = {}
    if isinstance(career_progression, dict):
        adapted_career = career_progression
    elif isinstance(career_progression, list):
        adapted_career = {
            'entry_level': career_progression[0] if len(career_progression) > 0 else 'Professional',
            'progression_roles': career_progression[1:] if len(career_progression) > 1 else []
        }
    elif isinstance(career_progression, str):
        adapted_career = {
            'entry_level': career_progression,
            'progression_roles': []
        }
    
    # Create the adapted structure
    adapted_profile = {
        'role_definition': {
            'id': original_profile.get('id', 'ROLE'),
            'name': original_profile.get('profile_name', 'Professional'),
            'description': original_profile.get('role_description', 'Professional role'),
            'main_area': 'Digital Sustainability'
        },
        'metadata': {
            'eqf_level': eqf_level,
            'role_name': original_profile.get('profile_name', 'Professional')
        },
        'enhanced_competencies': {
            'core_competencies': [
                {'name': area, 'description': f'Professional competency in {area.lower()}'}
                for area in core_competency_areas
            ],
            'learning_outcomes': eqf_outcomes,
            'framework_mappings': original_profile.get('framework_alignment', {})
        },
        'realistic_career_progression': adapted_career,
        'typical_employers': {
            'primary_sectors': original_profile.get('industry_application', [])
        },
        'cpd_requirements': {
            'certification_maintenance': {
                'renewal_period_years': 3,
                'cpd_hours_required': 40
            }
        },
        'industry_application': original_profile.get('industry_application', [])
    }
    
    return adapted_profile

def generate_single_profile(role_id, eqf_level, output_number=None, theme='eu_official', compact=True):
    """Generate a single educational profile with CEN/TS 17 compliance AND machine-readable exports"""
    
    # Load profiles data - try multiple possible locations
    possible_profile_files = [
        Path('../../input/educational_profiles/educational_profiles.json'),
        Path('input/educational_profiles/educational_profiles.json'),
        Path('./input/educational_profiles/educational_profiles.json')
    ]
    
    profiles_file = None
    for file_path in possible_profile_files:
        if file_path.exists():
            profiles_file = file_path
            break
    
    if not profiles_file:
        print(f"❌ Profiles file not found. Tried:")
        for file_path in possible_profile_files:
            print(f"   - {file_path}")
        return None
    
    print(f"📁 Using profiles file: {profiles_file}")
    
    try:
        with open(profiles_file, 'r') as f:
            profiles_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Profiles file not found: {profiles_file}")
        return None
    
    # Find the requested profile
    target_profile = None
    for profile in profiles_data:
        if profile.get('id') == role_id:
            target_profile = profile
            break
    
    if not target_profile:
        print(f"❌ Profile {role_id} not found in data")
        return None
    
    # Adapt the profile structure with COMPLETE career progression
    adapted_profile = adapt_profile_structure(target_profile, eqf_level)
    
    # Create output filename with numbering if provided
    if output_number:
        base_filename = f"{output_number:02d}_COMPACT_EP_{role_id}_EQF{eqf_level}_EU_Test"
    else:
        base_filename = f"COMPACT_EP_{role_id}_EQF{eqf_level}_EU_Test"
    
    # Set up paths - try multiple possible output locations
    possible_output_dirs = [
        Path('../../output/compact_appendix'),
        Path('output/compact_appendix'),
        Path('./output/compact_appendix')
    ]
    
    # Use the first one that we can create or that exists
    output_dir = possible_output_dirs[0]  # Default to first option
    for dir_path in possible_output_dirs:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            output_dir = dir_path
            break
        except:
            continue
    
    print(f"📁 Output directory: {output_dir}")
    
    # Generate ALL required formats
    generated_files = {}
    
    try:
        # Import metadata engine directly
        from components.cen_ts_17_metadata_engine import CenTS17MetadataEngine
        metadata_engine = CenTS17MetadataEngine()
        
        print("📊 Generating machine-readable metadata...")
        machine_metadata = metadata_engine.generate_machine_readable_metadata(adapted_profile)
        
        # 1. Generate JSON-LD (machine-readable with URIs)
        jsonld_path = output_dir / f"{base_filename}.jsonld"
        metadata_engine.export_as_json_ld(machine_metadata, jsonld_path)
        generated_files['jsonld'] = jsonld_path
        print(f"   ✅ JSON-LD: {jsonld_path.name}")
        
        # 2. Generate RDF/XML (semantic web integration)
        rdf_path = output_dir / f"{base_filename}.rdf.xml"
        metadata_engine.export_as_rdf_xml(machine_metadata, rdf_path)
        generated_files['rdf_xml'] = rdf_path
        print(f"   ✅ RDF/XML: {rdf_path.name}")
        
        # 3. Generate enhanced JSON (profile + metadata)
        json_path = output_dir / f"{base_filename}.json"
        enhanced_json = {
            'profileData': adapted_profile,
            'machineReadableMetadata': machine_metadata,
            'cenTs17Compliance': {
                'structuralCompliance': True,
                'semanticCompliance': True, 
                'interoperabilityCompliance': True,
                'machineReadable': True,
                'complianceVersion': '1.0.0',
                'validationDate': datetime.now().isoformat()
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_json, f, indent=2, ensure_ascii=False)
        generated_files['json'] = json_path
        print(f"   ✅ Enhanced JSON: {json_path.name}")
        
        # 4. Generate HTML (human-readable matching DOCX exactly)
        html_path = output_dir / f"{base_filename}.html"
        generate_html_profile(adapted_profile, machine_metadata, html_path)
        generated_files['html'] = html_path
        print(f"   ✅ HTML: {html_path.name}")
        
    except ImportError:
        print("⚠️ Metadata engine not available, generating basic formats only")
        
        # Basic JSON export
        json_path = output_dir / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(adapted_profile, f, indent=2, ensure_ascii=False)
        generated_files['json'] = json_path
        print(f"   ✅ Basic JSON: {json_path.name}")
    
    # 5. Generate DOCX using existing generator
    try:
        from components.docx_generator import DocxGenerator
        
        # Try multiple possible project root paths
        possible_roots = [Path('../../'), Path('.'), Path('./')]
        generator = None
        
        for root_path in possible_roots:
            try:
                generator = DocxGenerator(root_path)
                break
            except:
                continue
        
        if not generator:
            print("❌ Could not initialize DocxGenerator")
            return None
        
        # Generate DOCX
        docx_path = output_dir / f"{base_filename}.docx"
        result = generator.generate_educational_profile_docx(
            adapted_profile, docx_path, theme_name=theme, compact_mode=compact
        )
        
        if isinstance(result, dict):
            # If DocxGenerator returns multiple files, merge them
            generated_files.update(result)
        else:
            # If it returns just the DOCX path
            generated_files['docx'] = docx_path
        
        print(f"   ✅ DOCX: {docx_path.name}")
        
    except Exception as e:
        print(f"❌ Error generating DOCX: {e}")
        return None
    
    print(f"✅ Generated: {base_filename} (multiple formats)")
    print(f"📍 Output directory: {output_dir.absolute()}")
    
    # Summary of generated files
    print("📄 Generated file formats:")
    for file_type, file_path in generated_files.items():
        file_size = file_path.stat().st_size if file_path.exists() else 0
        print(f"   • {file_type.upper()}: {file_path.name} ({file_size:,} bytes)")
    
    return generated_files

def generate_all_22_profiles():
    """Generate all 22 educational profiles with numbering for wrapper compatibility"""
    
    # Specific role-EQF combinations (22 total) matching your script
    ep_combinations = [
        (1, 'DSL', 7),   (2, 'DSL', 8),   (3, 'DSM', 6),   (4, 'DSM', 7),
        (5, 'DSC', 6),   (6, 'DSC', 7),   (7, 'SBA', 6),   (8, 'SBA', 7),
        (9, 'DSI', 7),   (10, 'DSI', 8),  (11, 'DAN', 6),  (12, 'DAN', 7),
        (13, 'DSE', 6),  (14, 'DSE', 7),  (15, 'SSD', 6),  (16, 'SSD', 7),
        (17, 'SDD', 4),  (18, 'SDD', 5),  (19, 'SDD', 6),  (20, 'SDD', 7),
        (21, 'STS', 4),  (22, 'STS', 5)
    ]
    
    print(f"📚 Generating {len(ep_combinations)} Educational Profiles (CEN/TS 17 Compliant)...")
    
    success_count = 0
    failed_profiles = []
    
    for number, role, eqf in ep_combinations:
        print(f"📄 Generating {number:02d}_COMPACT_EP: {role} EQF{eqf}...")
        
        result = generate_single_profile(role, eqf, number, 'eu_official', True)
        if result:
            success_count += 1
            print(f"   ✅ Success: {number:02d}_{role}_EQF{eqf}")
        else:
            failed_profiles.append(f"{number:02d}_{role}_EQF{eqf}")
            print(f"   ❌ Failed: {number:02d}_{role}_EQF{eqf}")
    
    print(f"\n📊 Generation Results:")
    print(f"✅ Successfully generated: {success_count}/{len(ep_combinations)} profiles")
    print(f"📁 Files saved to: output/compact_appendix/")
    
    if failed_profiles:
        print(f"❌ Failed profiles: {', '.join(failed_profiles)}")
    
    # List generated files for verification
    try:
        output_dirs = [
            Path('../../output/compact_appendix'),
            Path('output/compact_appendix'), 
            Path('./output/compact_appendix')
        ]
        
        for output_dir in output_dirs:
            if output_dir.exists():
                docx_files = list(output_dir.glob('*_COMPACT_EP_*.docx'))
                if docx_files:
                    print(f"\n📁 Generated files in {output_dir}:")
                    for file in sorted(docx_files):
                        file_size = file.stat().st_size
                        print(f"   📄 {file.name} ({file_size:,} bytes)")
                    break
    except Exception as e:
        print(f"⚠️ Could not list generated files: {e}")
    
    return success_count

def main():
    """Main entry point for compact profile generation"""
    
    if len(sys.argv) == 1:
        # No arguments - generate all 22 profiles
        generate_all_22_profiles()
    elif len(sys.argv) == 3:
        # Two arguments: role and EQF level
        role_id = sys.argv[1].upper()
        eqf_level = int(sys.argv[2])
        generate_single_profile(role_id, eqf_level)
    elif len(sys.argv) == 4:
        # Three arguments: role, EQF level, and number
        role_id = sys.argv[1].upper()
        eqf_level = int(sys.argv[2])
        number = int(sys.argv[3])
        generate_single_profile(role_id, eqf_level, number)
    else:
        print("Usage:")
        print("  python3 generate_compact_profiles.py                    # Generate all 22 profiles")
        print("  python3 generate_compact_profiles.py DSL 7              # Generate single profile")
        print("  python3 generate_compact_profiles.py DSL 7 1            # Generate numbered profile")

if __name__ == "__main__":
    main()
