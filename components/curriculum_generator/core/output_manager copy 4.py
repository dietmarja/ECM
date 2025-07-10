# scripts/curriculum_generator/core/output_manager.py
"""
Enhanced Output Manager for T3.2/T3.4 compliant curriculum generation
BASED ON output_manager_reconstructed.py with enhanced curriculum HTML generation
Supports comprehensive educational profiles with full schema compliance
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class OutputManager:
    """Enhanced output manager with full T3.2 educational profile support and rich curriculum HTML"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.setup_output_directories()

    def setup_output_directories(self):
        """Create necessary output directories"""
        directories = [
            'output/curricula',
            'output/educational_profiles',
            'output/summaries',
            'output/pathways'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)

    def save_curriculum(
        self,
        curriculum: Dict[str, Any],
        output_dir: str,
        topic: str,
        eqf_level: int,
        role_id: str
    ) -> List[str]:
        """FIXED: Save curriculum files AND rich educational profile HTML"""
        saved_files = []
        
        try:
            # Extract basic info
            timestamp = datetime.now().strftime('%Y%m%d')
            
            # Clean topic for filename
            clean_topic = ''.join(c.upper() if c.isalnum() else '_' for c in topic)
            base_filename = f"{role_id}_{clean_topic}_{eqf_level}_{timestamp}"
            
            # Ensure output directory exists
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            print(f"💾 FIXED: Saving curriculum with rich educational profile...")
            
            # Save JSON curriculum
            json_file = output_path / f"{base_filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(curriculum, f, indent=2, ensure_ascii=False)
            saved_files.append(str(json_file))
            
            # Save curriculum HTML using existing method
            html_file = output_path / f"{base_filename}.html"
            html_content = self._generate_rich_curriculum_html(curriculum, topic, eqf_level)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            saved_files.append(str(html_file))
            
            # Save summary
            summary_file = output_path / f"{base_filename}_summary.json"
            summary = self._generate_curriculum_summary(curriculum)
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            saved_files.append(str(summary_file))
            
            # CRITICAL FIX: Extract and save RICH educational profile HTML
            educational_profile = curriculum.get('educational_profile', {})
            if educational_profile:
                print(f"🏗️ FIXED: Generating rich educational profile HTML...")
                print(f"   Rich data check:")
                print(f"     - Enhanced competencies: {len(educational_profile.get('enhanced_competencies', []))}")
                print(f"     - Modular structure: {'Present' if educational_profile.get('modular_structure') else 'Missing'}")
                print(f"     - Career progression: {'Present' if educational_profile.get('realistic_career_progression') else 'Missing'}")
                
                # Generate rich educational profile files using existing methods
                role_name = educational_profile.get('role_name', f'{role_id} Professional')
                profile_files = self._save_rich_educational_profile_simple(
                    educational_profile, topic, eqf_level, role_id, role_name
                )
                saved_files.extend(profile_files)
                
                print(f"✅ FIXED: Generated rich educational profile files: {len(profile_files)}")
            else:
                print(f"⚠️ No educational profile found in curriculum")
            
            print(f"✅ FIXED: Saved curriculum + educational profile files: {len(saved_files)} files")
            return saved_files
            
        except Exception as e:
            print(f"❌ Error saving curriculum files: {e}")
            import traceback
            traceback.print_exc()
            return []

    def save_educational_profile_standalone_enhanced(
        self,
        educational_profile: Any,
        topic: str,
        eqf_level: int
    ) -> List[str]:
        """Save standalone educational profile with enhanced template"""

        # Create output directory
        profile_dir = self.project_root / "output" / "educational_profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)

        # Generate filenames
        role_id = educational_profile.get('role_id', 'UNKNOWN')
        role_name = educational_profile.get('role_name', 'Unknown Role')
        profile_id = educational_profile.get('profile_id', f'EP_{role_id}_{eqf_level}')

        json_filename = f"{profile_id}.json"
        html_filename = f"{profile_id}.html"

        json_path = profile_dir / json_filename
        html_path = profile_dir / html_filename

        try:
            # Save JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(educational_profile, f, indent=2, ensure_ascii=False)

            # Generate enhanced HTML using new template
            html_content = self._generate_enhanced_educational_profile_html(
                educational_profile, role_name, eqf_level
            )

            # Save HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✅ Saved educational profile: {json_filename}")
            print(f"✅ Saved educational profile HTML: {html_filename}")

            return [str(json_path), str(html_path)]

        except Exception as e:
            print(f"❌ Error saving educational profile: {e}")
            return []

    def _convert_educational_profile_to_dict(self, educational_profile: Any) -> Dict[str, Any]:
        """Convert educational profile object to JSON-serializable dictionary"""
        from dataclasses import asdict, is_dataclass

        def convert_to_dict(obj):
            """Recursively convert objects to dictionaries"""
            if is_dataclass(obj):
                return asdict(obj)
            elif hasattr(obj, '__dict__'):
                # Handle regular objects with __dict__
                result = {}
                for key, value in obj.__dict__.items():
                    if not key.startswith('_'):  # Skip private attributes
                        result[key] = convert_to_dict(value)
                return result
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_dict(value) for key, value in obj.items()}
            else:
                # Basic types (str, int, float, bool, None)
                return obj

        if isinstance(educational_profile, dict):
            # Already a dictionary, just ensure all nested objects are converted
            return convert_to_dict(educational_profile)
        else:
            # Convert object to dictionary
            return convert_to_dict(educational_profile)

    def _save_html_educational_profile(self, profile_data: Dict[str, Any], file_path: Path) -> None:
        """Save educational profile as HTML"""

        html_content = self._generate_educational_profile_html(
            profile_data, 
            profile_data.get('role_name', 'Unknown Role'), 
            profile_data.get('target_eqf_level', 6)
        )

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            raise ValueError(f"Error saving Educational Profile HTML: {e}")

    def _generate_educational_profile_html(self, profile: dict, role_name: str, eqf_level: int) -> str:
        """Generate comprehensive educational profile HTML using JSON data"""

        print(f"🔍 Generating HTML for {role_name} (EQF {eqf_level})")

        # Extract data with debug output
        role_id = profile.get('role_id', 'Unknown')
        target_ects = profile.get('target_ects', 60)
        profile_type = profile.get('profile_type', 'standard')

        # Get rich content from educational_profiles.json
        sustainability_competencies = profile.get('sustainability_competencies', [])
        programme_outcomes = profile.get('learning_outcomes_programme', [])
        entry_requirements = profile.get('entry_requirements', {})
        assessment_methods = profile.get('assessment_methods', [])

        print(f"📊 Data found:")
        print(f"   Competencies: {len(sustainability_competencies)}")
        print(f"   Programme outcomes: {len(programme_outcomes)}")
        print(f"   Entry requirements: {bool(entry_requirements)}")
        print(f"   Assessment methods: {len(assessment_methods)}")

        # Professional context
        role_context = profile.get('role_context', {})
        industry_sectors = role_context.get('industry_sectors', [])
        career_pathways = role_context.get('career_pathways', [])
        typical_employers = role_context.get('typical_employers', [])

        # Professional recognition
        professional_recognition = profile.get('professional_recognition', {})
        professional_bodies = professional_recognition.get('professional_bodies', [])
        certification_pathways = professional_recognition.get('certification_pathways', [])
        cpd_requirements = professional_recognition.get('cpd_requirements', {})

        print(f"   Industry sectors: {len(industry_sectors)}")
        print(f"   Career pathways: {len(career_pathways)}")
        print(f"   Professional bodies: {len(professional_bodies)}")

        # Semester structure
        semester_structure = profile.get('semester_structure', {})
        semesters = semester_structure.get('semesters', [])

        profile_badge_class = "profile-standard" if profile_type == "standard" else "profile-reduced"
        profile_badge_text = "Standard Profile" if profile_type == "standard" else "Reduced Profile"

        # Build comprehensive HTML with all sections
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>Educational Profile: {role_name}</title>',
            '    <style>',
            '        * { margin: 0; padding: 0; box-sizing: border-box; }',
            '        body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }',
            '        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }',
            '        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }',
            '        .header h1 { font-size: 2.5rem; margin-bottom: 1.5rem; }',
            '        .metadata { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }',
            '        .badge { background: rgba(255, 255, 255, 0.25); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; }',
            '        .profile-standard { background-color: #10b981 !important; }',
            '        .profile-reduced { background-color: #f59e0b !important; }',
            '        .section { background: white; margin-bottom: 2rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden; }',
            '        .section-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem 2rem; font-size: 1.5rem; font-weight: 600; }',
            '        .section-content { padding: 2rem; }',
            '        .profile-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }',
            '        .info-card { background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea; }',
            '        .info-card h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.2rem; }',
            '        .programme-outcomes { list-style: none; padding: 0; }',
            '        .programme-outcomes li { background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%); padding: 1rem 1.5rem; margin-bottom: 1rem; border-radius: 8px; border-left: 4px solid #10b981; position: relative; }',
            '        .competencies-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }',
            '        .competency-item { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #10b981; }',
            '        .competency-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }',
            '        .level { padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }',
            '        .level-proficient { background: #10b981; color: white; }',
            '        .level-advanced { background: #3b82f6; color: white; }',
            '        .level-expert { background: #8b5cf6; color: white; }',
            '        .competency-outcomes { margin-left: 1.5rem; margin-top: 0.5rem; }',
            '        .two-column-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }',
            '        .list-item { background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; }',
            '        .requirements-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }',
            '        .requirement-card { background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f59e0b; }',
            '        .requirement-card h4 { color: #d97706; margin-bottom: 0.5rem; }',
            '        .footer { text-align: center; padding: 2rem; color: #666; background: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-top: 3rem; }',
            '        @media (max-width: 768px) { .profile-info { grid-template-columns: 1fr; } .competencies-grid { grid-template-columns: 1fr; } .two-column-list { grid-template-columns: 1fr; } .requirements-grid { grid-template-columns: 1fr; } }',
            '    </style>',
            '</head>',
            '<body>',
            '    <div class="container">',
            '        <header class="header">',
            f'            <h1>📋 Educational Profile: {role_name}</h1>',
            '            <div class="metadata">',
            f'                <span class="badge">Role: {role_id}</span>',
            f'                <span class="badge">EQF Level {eqf_level}</span>',
            f'                <span class="badge">{target_ects} ECTS</span>',
            '                <span class="badge">T3.2 Compliant</span>',
            f'                <span class="badge {profile_badge_class}">{profile_badge_text}</span>',
            '            </div>',
            '        </header>',
            '        <main>'
        ]

        # Profile Overview Section
        html_parts.extend([
            '            <section class="section">',
            '                <div class="section-header">📋 Profile Overview</div>',
            '                <div class="section-content">',
            '                    <div class="profile-info">',
            '                        <div class="info-card">',
            '                            <h3>Role Information</h3>',
            f'                            <p><strong>Role:</strong> {role_name} ({role_id})</p>',
            f'                            <p><strong>EQF Level:</strong> {eqf_level}</p>',
            f'                            <p><strong>Profile Type:</strong> {profile_type.title()}</p>',
            '                        </div>',
            '                        <div class="info-card">',
            '                            <h3>Programme Structure</h3>',
            f'                            <p><strong>Target ECTS:</strong> {target_ects}</p>',
            f'                            <p><strong>Duration:</strong> {len(semesters)} semesters</p>',
            f'                            <p><strong>Learning Mode:</strong> {profile.get("learning_mode", "flexible")}</p>',
            '                        </div>',
            '                        <div class="info-card">',
            '                            <h3>Delivery Methods</h3>',
            f'                            <p><strong>Methods:</strong> {", ".join(profile.get("delivery_methods", ["blended"]))}</p>',
            '                            <p><strong>Compliance:</strong> T3.2, T3.4, EQF, ECTS, ECVET</p>',
            '                        </div>',
            '                    </div>',
            '                </div>',
            '            </section>'
        ])

        # Programme Learning Outcomes
        if programme_outcomes:
            html_parts.extend([
                '            <section class="section">',
                '                <div class="section-header">🎯 Programme Learning Outcomes</div>',
                '                <div class="section-content">',
                '                    <ul class="programme-outcomes">'
            ])
            for outcome in programme_outcomes:
                html_parts.append(f'                        <li>{outcome}</li>')
            html_parts.extend([
                '                    </ul>',
                '                </div>',
                '            </section>'
            ])

        # Sustainability Competencies
        if sustainability_competencies:
            print(f"✅ Adding {len(sustainability_competencies)} competencies to HTML")
            html_parts.extend([
                '            <section class="section">',
                '                <div class="section-header">🌱 Sustainability Competencies</div>',
                '                <div class="section-content">',
                '                    <div class="competencies-grid">'
            ])

            for comp in sustainability_competencies:
                comp_name = comp.get('competency_name', 'Unknown Competency')
                comp_level = comp.get('competency_level', 'Proficient').lower()
                learning_outcomes = comp.get('learning_outcomes', [])

                print(f"   Adding competency: {comp_name} ({comp_level})")

                html_parts.extend([
                    '                        <div class="competency-item">',
                    '                            <div class="competency-header">',
                    f'                                <strong>{comp_name}</strong>',
                    f'                                <span class="level level-{comp_level}">{comp_level.title()}</span>',
                    '                            </div>',
                    '                            <ul class="competency-outcomes">'
                ])
                for outcome in learning_outcomes:
                    html_parts.append(f'                                <li>{outcome}</li>')
                html_parts.extend([
                    '                            </ul>',
                    '                        </div>'
                ])

            html_parts.extend([
                '                    </div>',
                '                </div>',
                '            </section>'
            ])
        else:
            print("⚠️ No sustainability competencies found in profile data")

        # Footer
        html_parts.extend([
            '        </main>',
            '        <footer class="footer">',
            '            <p><strong>Educational Profile</strong> generated by DSCG v3.1 - T3.2/T3.4 Compliant</p>',
            f'            <p>Generated: {profile.get("creation_date", "Unknown")} | Version: {profile.get("version", "1.0")}</p>',
            '        </footer>',
            '    </div>',
            '</body>',
            '</html>'
        ])

        html_content = '\n'.join(html_parts)
        print(f"✅ HTML generated successfully with {len(html_content)} characters")
        return html_content

    def _generate_enhanced_educational_profile_html(self, profile, role_name, eqf_level):
        """Generate enhanced HTML - wrapper for compatibility"""
        return self._generate_educational_profile_html(profile, role_name, eqf_level)

    def create_reduced_educational_profile(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        core_skills: List[str] = None
    ) -> Dict[str, Any]:
        """Create reduced educational profile when full role data not available"""

        print(f"📋 Creating reduced educational profile for {role_id}...")

        timestamp = datetime.now().isoformat()
        core_skills = core_skills or []

        # Calculate basic semester structure
        num_semesters = max(2, (target_ects + 15) // 30)
        ects_per_semester = target_ects // num_semesters

        semesters = []
        for i in range(num_semesters):
            semester = {
                'semester_number': i + 1,
                'semester_name': f"Semester {i + 1}",
                'focus_area': "Foundation" if i == 0 else ("Capstone" if i == num_semesters - 1 else "Specialization"),
                'target_ects': ects_per_semester + (1 if i < (target_ects % num_semesters) else 0),
                'duration_weeks': 15,
                'learning_objectives': [
                    f"Develop competencies for {role_name}",
                    f"Apply knowledge in {topic}",
                    "Demonstrate professional skills"
                ]
            }
            semesters.append(semester)

        reduced_profile = {
            'profile_id': f"EP_REDUCED_{role_id}_{datetime.now().strftime('%Y%m%d')}",
            'role_id': role_id,
            'role_name': role_name,
            'profile_title': f"Reduced Educational Profile: {role_name} in {topic}",
            'profile_type': 'reduced',

            'target_eqf_level': eqf_level,
            'target_ects': target_ects,
            'duration_semesters': num_semesters,
            'learning_mode': 'flexible',
            'delivery_methods': ['blended', 'online'],

            'semester_breakdown': semesters,

            'core_competencies': [
                {
                    'competency_name': skill.replace('_', ' ').title(),
                    'competency_level': 'Proficient',
                    'learning_outcomes': [f"Demonstrate {skill.replace('_', ' ')}"]
                }
                for skill in core_skills
            ],

            'learning_outcomes_programme': [
                f"Demonstrate competency as {role_name}",
                f"Apply skills in {topic} context",
                "Integrate professional knowledge"
            ],

            'micro_credentials': [
                {
                    'credential_id': f"MC_{role_id}_S{i+1}",
                    'credential_name': f"{role_name} - Semester {i+1}",
                    'ects_value': semester['target_ects'],
                    'recognition_level': 'semester'
                }
                for i, semester in enumerate(semesters)
            ],

            'creation_date': timestamp,
            'version': '1.0-reduced',
            'compliance_frameworks': ['EQF', 'ECTS']
        }

        return reduced_profile

    def _extract_educational_profile(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Extract educational profile data from curriculum"""

        profile_data = curriculum.get('educational_profile', {}).copy()

        # Add additional context from curriculum
        if 'metadata' in curriculum:
            profile_data['curriculum_metadata'] = curriculum['metadata']

        if 'curriculum_structure' in curriculum:
            profile_data['implemented_structure'] = curriculum['curriculum_structure']

        if 'micro_credentials' in curriculum:
            profile_data['micro_credentials'] = curriculum['micro_credentials']

        if 'workplace_integration' in curriculum:
            profile_data['workplace_integration'] = curriculum['workplace_integration']

        if 'accreditation' in curriculum:
            profile_data['accreditation'] = curriculum['accreditation']

        return profile_data

    # =============================================================================
    # RICH EDUCATIONAL PROFILE LOADING - MISSING FUNCTIONALITY
    # =============================================================================

    def load_educational_profile_from_json(
        self, 
        role_id: str, 
        eqf_level: int = None, 
        profiles_file: str = "input/educational_profiles/educational_profiles.json"
    ) -> Dict[str, Any]:
        """Load rich educational profile from educational_profiles.json"""
        
        print(f"📋 Loading rich educational profile for {role_id} from JSON...")
        
        try:
            profiles_path = self.project_root / profiles_file
            with open(profiles_path, 'r', encoding='utf-8') as f:
                all_profiles = json.load(f)
            
            # Find matching profile
            for profile in all_profiles:
                if profile.get('id') == role_id:
                    print(f"✅ Found rich profile for {role_id}")
                    print(f"   Enhanced competencies: {len(profile.get('enhanced_competencies', []))}")
                    print(f"   Modular structure: {'Available' if profile.get('modular_structure') else 'Missing'}")
                    print(f"   Career progression: {'Available' if profile.get('realistic_career_progression') else 'Missing'}")
                    return profile
            
            print(f"⚠️ No rich profile found for {role_id}, creating enhanced default...")
            return self._create_enhanced_default_profile(role_id, eqf_level)
            
        except FileNotFoundError:
            print(f"⚠️ Educational profiles file not found, creating enhanced default...")
            return self._create_enhanced_default_profile(role_id, eqf_level)
        except Exception as e:
            print(f"❌ Error loading profiles: {e}")
            return self._create_enhanced_default_profile(role_id, eqf_level)

    def _save_rich_educational_profile_simple(
        self,
        educational_profile: Dict[str, Any],
        topic: str,
        eqf_level: int,
        role_id: str,
        role_name: str
    ) -> List[str]:
        """EXTENDED NUCLEAR FIX: All sections included"""
        
        try:
            from datetime import datetime
            from pathlib import Path
            import json
            
            print(f"🔧 EXTENDED NUCLEAR: Complete save for {role_name}...")
            
            # Create output directory directly
            profile_output_path = self.project_root / "output" / "educational_profiles"
            profile_output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate filenames directly
            timestamp = datetime.now().strftime('%Y%m%d')
            topic_clean = topic.upper().replace(' ', '_')
            profile_id = f"EP_{role_id}_{topic_clean}_{eqf_level}_{timestamp}"
            
            json_path = profile_output_path / f"{profile_id}.json"
            html_path = profile_output_path / f"{profile_id}.html"
            
            # Save JSON directly
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(educational_profile, f, indent=2, ensure_ascii=False)
            
            # Generate COMPLETE HTML with ALL sections
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Profile: {role_name}</title>
    <style>
        /* RICH CSS matching working version */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
        .header h1 {{ font-size: 2.2rem; margin-bottom: 1rem; font-weight: 600; }}
        .metadata {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }}
        .badge {{ background: rgba(255,255,255,0.2); padding: 0.6rem 1.2rem; border-radius: 25px; font-weight: 500; backdrop-filter: blur(10px); }}
        .section {{ background: white; margin-bottom: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden; }}
        .section-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.2rem 2rem; font-size: 1.4rem; font-weight: 600; }}
        .section-content {{ padding: 2rem; }}
        .competencies-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }}
        .competency-item {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.8rem; border-radius: 12px; border-left: 5px solid #10b981; }}
        .competency-header {{ margin-bottom: 1.2rem; }}
        .level {{ padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }}
        .level-proficient {{ background: #10b981; color: white; }}
        .level-advanced {{ background: #3b82f6; color: white; }}
        .level-expert {{ background: #8b5cf6; color: white; }}
        .competency-outcomes {{ margin-left: 1.2rem; }}
        .competency-outcomes li {{ margin-bottom: 0.4rem; color: #555; }}
        .modular-overview {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
        .overview-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; }}
        .overview-card h4 {{ font-size: 1rem; margin-bottom: 0.5rem; opacity: 0.9; }}
        .big-number {{ font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0; }}
        .modules-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; margin-top: 1rem; }}
        .module-card {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 10px; padding: 1.5rem; transition: transform 0.2s ease; }}
        .module-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .module-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
        .module-header h4 {{ color: #667eea; font-size: 1.1rem; }}
        .semester-badge {{ background: #10b981; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }}
        .ects-info {{ color: #666; font-weight: 500; margin: 0.5rem 0; }}
        .career-timeline {{ display: flex; flex-direction: column; gap: 2rem; }}
        .career-stage {{ background: #f8f9fa; border-radius: 12px; padding: 1.8rem; border-left: 5px solid #10b981; }}
        .stage-header {{ margin-bottom: 1rem; }}
        .stage-header h3 {{ color: #10b981; font-size: 1.3rem; margin-bottom: 0.5rem; }}
        .stage-meta {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        .timeframe {{ background: #e0f2fe; color: #0277bd; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500; }}
        .salary {{ background: #e8f5e8; color: #2e7d32; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500; }}
        .roles-list {{ margin-top: 1rem; }}
        .roles-list h4 {{ color: #555; margin-bottom: 0.5rem; }}
        .roles-list ul {{ margin-left: 1.2rem; }}
        .roles-list li {{ margin-bottom: 0.3rem; color: #666; }}
        .requirements-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }}
        .requirement-card {{ background: #fef3c7; padding: 1.8rem; border-radius: 12px; border-left: 5px solid #f59e0b; }}
        .requirement-card h4 {{ color: #d97706; margin-bottom: 0.8rem; font-size: 1.1rem; }}
        .assessment-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
        .assessment-item {{ background: #f8f9fa; padding: 1.2rem; border-radius: 10px; border-left: 4px solid #667eea; display: flex; align-items: center; gap: 0.8rem; }}
        .sectors-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
        .sector-item {{ background: #f8f9fa; padding: 1.2rem; border-radius: 10px; border-left: 4px solid #667eea; display: flex; align-items: center; gap: 0.8rem; }}
        .cpd-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }}
        .cpd-card {{ background: #fef3c7; padding: 1.8rem; border-radius: 12px; border-left: 5px solid #f59e0b; }}
        .cpd-card h4 {{ color: #d97706; margin-bottom: 0.8rem; font-size: 1.1rem; }}
        .footer {{ text-align: center; padding: 2rem; color: #666; background: white; border-radius: 15px; margin-top: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
    </style>
</head>
<body>
<div class="container">
    <header class="header">
        <h1>📋 Educational Profile: {role_name}</h1>
        <div class="metadata">
            <span class="badge">Role: {role_id}</span>
            <span class="badge">EQF Level {eqf_level}</span>
            <span class="badge">T3.2 Compliant</span>
            <span class="badge">EXTENDED NUCLEAR</span>
        </div>
    </header>
    <main>"""
            
            # SECTION 1: Enhanced Competencies (working pattern)
            competencies = educational_profile.get('enhanced_competencies', educational_profile.get('sustainability_competencies', []))
            if competencies:
                html_content += """
        <section class="section">
            <div class="section-header">🌱 Enhanced Competencies</div>
            <div class="section-content">
                <div class="competencies-grid">"""
                for comp in competencies:
                    comp_name = comp.get('competency_name', 'Unknown')
                    comp_level = comp.get('competency_level', 'Proficient').lower()
                    outcomes = comp.get('learning_outcomes', [])
                    html_content += f"""
                    <div class="competency-item">
                        <div class="competency-header">
                            <strong>{comp_name}</strong>
                            <span class="level level-{comp_level}">{comp_level.title()}</span>
                        </div>
                        <ul class="competency-outcomes">"""
                    for outcome in outcomes:
                        html_content += f"<li>{outcome}</li>"
                    html_content += """
                        </ul>
                    </div>"""
                html_content += """
                </div>
            </div>
        </section>"""

            # SECTION 2: Modular Structure (working pattern)
            modular = educational_profile.get('modular_structure', {})
            if modular:
                modules = modular.get('modules', [])
                semesters = modular.get('semesters', 3)
                total_ects = modular.get('total_ects_by_level', {}).get(str(eqf_level), 60)
                
                html_content += f"""
        <section class="section">
            <div class="section-header">🧩 Modular Structure</div>
            <div class="section-content">
                <div class="modular-overview">
                    <div class="overview-card">
                        <h4>📊 ECTS by EQF Level</h4>
                        <p>EQF {eqf_level}: {total_ects} ECTS</p>
                    </div>
                    <div class="overview-card">
                        <h4>📅 Duration</h4>
                        <p class="big-number">{semesters}</p>
                        <p>Semesters</p>
                    </div>
                </div>
                <div class="modules-section">
                    <h3>📖 Course Modules</h3>
                    <div class="modules-grid">"""
                for module in modules:
                    code = module.get('code', 'N/A')
                    name = module.get('name', 'Unknown Module')
                    semester = module.get('semester', 1)
                    ects = module.get('ects', {})
                    if isinstance(ects, dict):
                        ects_display = f"EQF {eqf_level}: {ects.get(str(eqf_level), 5)} ECTS"
                    else:
                        ects_display = f"{ects} ECTS"
                    
                    html_content += f"""
                        <div class="module-card">
                            <div class="module-header">
                                <h4>{code}</h4>
                                <span class="semester-badge">Semester {semester}</span>
                            </div>
                            <h5>{name}</h5>
                            <p class="ects-info">{ects_display}</p>
                        </div>"""
                html_content += """
                    </div>
                </div>
            </div>
        </section>"""

            # SECTION 3: Career Progression (NEW - same pattern)
            career_progression = educational_profile.get('realistic_career_progression', {})
            if career_progression:
                html_content += """
        <section class="section">
            <div class="section-header">🚀 Career Progression</div>
            <div class="section-content">
                <div class="career-timeline">"""
                
                stage_config = {
                    'immediate': {'icon': '🎯', 'title': 'Immediate Opportunities'},
                    'short_term': {'icon': '📈', 'title': 'Short Term Goals'},
                    'long_term': {'icon': '🌟', 'title': 'Long Term Vision'}
                }
                
                for stage_key, stage_data in career_progression.items():
                    if stage_key in stage_config:
                        config = stage_config[stage_key]
                        timeframe = stage_data.get('timeframe', 'N/A')
                        salary_range = stage_data.get('salary_range', 'N/A')
                        roles = stage_data.get('roles', [])
                        
                        html_content += f"""
                    <div class="career-stage">
                        <div class="stage-header">
                            <h3>{config["icon"]} {config["title"]}</h3>
                            <div class="stage-meta">
                                <span class="timeframe">{timeframe}</span>
                                <span class="salary">{salary_range}</span>
                            </div>
                        </div>
                        <div class="roles-list">
                            <h4>Typical Roles:</h4>
                            <ul>"""
                        for role in roles:
                            html_content += f"<li>{role}</li>"
                        html_content += """
                            </ul>
                        </div>
                    </div>"""
                
                html_content += """
                </div>
            </div>
        </section>"""

            # SECTION 4: Entry Requirements (NEW - same pattern)
            entry_requirements = educational_profile.get('entry_requirements', {})
            if entry_requirements:
                html_content += """
        <section class="section">
            <div class="section-header">📚 Entry Requirements</div>
            <div class="section-content">
                <div class="requirements-grid">"""
                
                req_mapping = {
                    'academic': 'Academic',
                    'professional': 'Professional', 
                    'technical': 'Technical',
                    'domain': 'Domain'
                }
                
                for req_key, req_title in req_mapping.items():
                    req_text = entry_requirements.get(req_key, f'No {req_key} requirements specified')
                    html_content += f"""
                    <div class="requirement-card">
                        <h4>{req_title}</h4>
                        <p>{req_text}</p>
                    </div>"""
                
                html_content += """
                </div>
            </div>
        </section>"""

            # SECTION 5: Assessment Methods (NEW - same pattern)
            assessment_methods = educational_profile.get('assessment_methods', [])
            if assessment_methods:
                html_content += """
        <section class="section">
            <div class="section-header">📊 Assessment Methods</div>
            <div class="section-content">
                <div class="assessment-grid">"""
                
                for method in assessment_methods:
                    html_content += f"""
                    <div class="assessment-item">
                        <span>✓</span>
                        <span>{method}</span>
                    </div>"""
                
                html_content += """
                </div>
            </div>
        </section>"""

            # SECTION 6: Industry Sectors (NEW - same pattern)
            industry_sectors = educational_profile.get('industry_sectors', [])
            if industry_sectors:
                html_content += """
        <section class="section">
            <div class="section-header">🏭 Industry Sectors</div>
            <div class="section-content">
                <div class="sectors-grid">"""
                
                for sector in industry_sectors:
                    html_content += f"""
                    <div class="sector-item">
                        <span>🏢</span>
                        <span>{sector}</span>
                    </div>"""
                
                html_content += """
                </div>
            </div>
        </section>"""

            # SECTION 7: CPD Requirements (NEW - same pattern)
            cpd_requirements = educational_profile.get('cpd_requirements', {})
            if cpd_requirements:
                html_content += """
        <section class="section">
            <div class="section-header">📈 Continuing Professional Development</div>
            <div class="section-content">
                <div class="cpd-grid">"""
                
                cpd_mapping = {
                    'annual_hours': 'Annual Hours',
                    'certification_maintenance': 'Certification Maintenance',
                    'conference_participation': 'Conference Participation',
                    'professional_networking': 'Professional Networking',
                    'knowledge_updates': 'Knowledge Updates'
                }
                
                for cpd_key, cpd_title in cpd_mapping.items():
                    cpd_value = cpd_requirements.get(cpd_key, 'Not specified')
                    html_content += f"""
                    <div class="cpd-card">
                        <h4>{cpd_title}</h4>
                        <p>{cpd_value}</p>
                    </div>"""
                
                html_content += """
                </div>
            </div>
        </section>"""

            # Footer
            html_content += """
    </main>
    <footer class="footer">
        <p><strong>Educational Profile</strong> generated by DSCG v3.1 - EXTENDED NUCLEAR FIX</p>
        <p><em>Full T3.2 Schema Compliance with ALL Rich Sections</em></p>
    </footer>
</div>
</body>
</html>"""
            
            # Save HTML directly
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ EXTENDED NUCLEAR: Saved ALL sections:")
            print(f"   JSON: {json_path}")
            print(f"   HTML: {html_path}")
            
            return [str(json_path), str(html_path)]
            
        except Exception as e:
            print(f"❌ EXTENDED NUCLEAR method failed: {e}")
            import traceback
            traceback.print_exc()
            return []
    def _create_enhanced_default_profile(self, role_id: str, eqf_level: int) -> Dict[str, Any]:
        """Create enhanced default profile with rich structure when JSON not available"""
        
        timestamp = datetime.now().isoformat()
        
        # Rich enhanced competencies (mimicking the structure from EP_STS_4_20250601.html)
        enhanced_competencies = [
            {
                "competency_name": f"Advanced {role_id} Professional Practice",
                "competency_level": "Advanced",
                "transversal": False,
                "eqf_alignment": f"Level {eqf_level}: Specialized professional implementation with autonomous capability",
                "learning_outcomes": [
                    f"Configure and maintain sophisticated sustainability systems relevant to {role_id} practice",
                    f"Implement advanced {role_id} methodologies with automated processes and integration",
                    f"Provide expert-level support and guidance for {role_id} tools and platforms",
                    f"Troubleshoot and optimize {role_id} system performance using advanced analytics",
                    f"Design and implement custom solutions for {role_id} challenges and requirements"
                ],
                "framework_mappings": {
                    "e_cf": ["B.2 Component Integration", "C.1 User Support", "E.4 Relationship Management"],
                    "digcomp": ["3.2 Integrating and re-elaborating", "5.1 Solving technical problems"],
                    "greencomp": ["3.1 Exploratory thinking", "2.2 Critical thinking"]
                }
            },
            {
                "competency_name": f"Sustainable {role_id} Implementation & System Support",
                "competency_level": "Proficient",
                "transversal": False,
                "learning_outcomes": [
                    f"Deploy sustainability-focused {role_id} tools across organizational systems",
                    f"Support implementation of circular economy tracking relevant to {role_id}",
                    f"Maintain compliance software and ensure data integrity for {role_id} processes",
                    f"Configure integration solutions for {role_id} data exchange",
                    f"Implement automation solutions for routine {role_id} tasks"
                ],
                "framework_mappings": {
                    "e_cf": ["B.3 Testing", "C.3 Service Delivery"],
                    "digcomp": ["3.4 Programming", "5.3 Creatively using technologies"],
                    "greencomp": ["3.2 Sustainability and equity"]
                }
            },
            {
                "competency_name": f"{role_id} Training & Professional Development",
                "competency_level": "Advanced",
                "transversal": True,
                "learning_outcomes": [
                    f"Design and deliver comprehensive {role_id} training programs",
                    f"Apply ethical frameworks to {role_id} professional decisions",
                    f"Facilitate adoption of {role_id} technologies and methodologies",
                    f"Develop documentation and knowledge sharing for {role_id} best practices",
                    f"Mentor junior professionals in {role_id} implementation and support"
                ],
                "framework_mappings": {
                    "greencomp": ["4.1 Collective action", "1.3 Supporting fairness"],
                    "digcomp": ["2.1 Interacting through technologies", "2.4 Collaborating through technologies"],
                    "e_cf": ["E.4 Relationship Management", "E.8 Information Security Management"]
                }
            }
        ]

        # Rich modular structure
        modular_structure = {
            "total_ects": {str(eqf_level): 50 if eqf_level <= 5 else 60},
            "total_ects_by_level": {str(eqf_level): 50 if eqf_level <= 5 else 60},
            "semesters": 3,
            "modules": [
                {
                    "code": f"{role_id}-101",
                    "name": f"{role_id} Platform Configuration & Integration",
                    "ects": {str(eqf_level): 12 if eqf_level <= 5 else 15},
                    "semester": 1,
                    "frameworks": ["e-CF B.2", "GreenComp 3.1"]
                },
                {
                    "code": f"{role_id}-102", 
                    "name": f"Sustainability Systems & Monitoring",
                    "ects": {str(eqf_level): 10 if eqf_level <= 5 else 12},
                    "semester": 1,
                    "frameworks": ["e-CF B.4", "DigComp 3.2"]
                },
                {
                    "code": f"{role_id}-201",
                    "name": f"Advanced {role_id} Implementation",
                    "ects": {str(eqf_level): 8 if eqf_level <= 5 else 10},
                    "semester": 2,
                    "frameworks": ["e-CF B.3", "DigComp 3.4"]
                },
                {
                    "code": f"{role_id}-202",
                    "name": f"Professional Support & Training",
                    "ects": {str(eqf_level): 10},
                    "semester": 2,
                    "frameworks": ["e-CF C.1", "DigComp 5.1"]
                },
                {
                    "code": f"{role_id}-203",
                    "name": f"User Training & Technology Adoption",
                    "ects": {str(eqf_level): 5 if eqf_level <= 5 else 8},
                    "semester": 2,
                    "frameworks": ["GreenComp 4.1", "e-CF E.4"]
                },
                {
                    "code": f"{role_id}-301",
                    "name": f"Capstone: {role_id} Implementation Project",
                    "ects": {str(eqf_level): 5},
                    "semester": 3,
                    "frameworks": ["e-CF C.3", "GreenComp 4.3"]
                }
            ]
        }

        # Rich career progression
        realistic_career_progression = {
            "immediate": {
                "timeframe": "0-2 years",
                "salary_range": "€25,000-35,000" if eqf_level <= 5 else "€30,000-45,000",
                "roles": [
                    f"{role_id} Specialist",
                    f"Junior {role_id} Consultant", 
                    f"{role_id} Support Specialist"
                ]
            },
            "short_term": {
                "timeframe": "2-5 years", 
                "salary_range": "€35,000-50,000" if eqf_level <= 5 else "€45,000-65,000",
                "roles": [
                    f"Senior {role_id} Specialist",
                    f"Lead {role_id} Consultant",
                    f"{role_id} Team Lead"
                ]
            },
            "long_term": {
                "timeframe": "5-10 years",
                "salary_range": "€50,000-70,000" if eqf_level <= 5 else "€65,000-90,000", 
                "roles": [
                    f"Manager of {role_id} Services",
                    f"Director of {role_id} Operations",
                    f"Independent {role_id} Consultant"
                ]
            }
        }

        return {
            "id": role_id,
            "profile_name": f"Enhanced {role_id} Educational Profile",
            "profile_type": "Enhanced_Standard",
            "target_eqf_level": eqf_level,
            "target_ects": 50 if eqf_level <= 5 else 60,
            "creation_date": timestamp,
            "version": "3.1_enhanced",
            
            # Rich content sections
            "enhanced_competencies": enhanced_competencies,
            "modular_structure": modular_structure,
            "realistic_career_progression": realistic_career_progression,
            
            # Standard sections
            "learning_outcomes_programme": [
                f"Configure and maintain sophisticated {role_id} systems with custom integrations",
                f"Implement advanced {role_id} methodologies with automated processes",
                f"Design and deliver comprehensive {role_id} training programs",
                f"Apply ethical frameworks to {role_id} professional decisions",
                f"Mentor and support junior professionals in {role_id} practice"
            ],
            
            "entry_requirements": {
                "academic": "Secondary education completion (high school diploma) or equivalent qualification" if eqf_level <= 5 else "Bachelor's degree or equivalent professional experience",
                "professional": "No prior work experience required, though basic technical aptitude beneficial" if eqf_level <= 5 else "2-3 years relevant professional experience",
                "technical": f"Basic {role_id} experience and familiarity with relevant software platforms",
                "domain": f"Familiarity with {role_id} tools, systems, and awareness of sustainability practices"
            },
            
            "assessment_methods": [
                "Practical demonstrations",
                "Skills assessments", 
                "Portfolio development",
                f"{role_id} configuration projects",
                f"{role_id} support simulations",
                "System deployment case studies"
            ],
            
            "role_context": {
                "industry_sectors": [
                    f"{role_id} Support and Services Companies",
                    "Software Implementation and Training Organizations",
                    "Corporate IT and Technology Departments", 
                    "Sustainability Technology Vendors",
                    "System Administration and Managed Services",
                    "Technical Training and Education Providers"
                ],
                "typical_employers": [
                    "Sustainability Software Vendors (SAP, Salesforce, Microsoft)",
                    "IT Services Companies (Accenture, IBM Services, Cognizant)",
                    "Corporate IT Departments (Fortune 500 companies)",
                    "Implementation Partners (Systems Integrators, Consultancies)",
                    "Technology Support Companies (Specialized IT Support)",
                    "Training Organizations (Corporate Universities, Technical Training)"
                ]
            },
            
            "professional_recognition": {
                "cpd_requirements": {
                    "annual_hours": 20 if eqf_level <= 5 else 25,
                    "certification_maintenance": "30-60 hours every 2-3 years",
                    "conference_participation": "Minimum 1 major technology or sustainability conference annually",
                    "professional_networking": "Active participation in technical communities and user groups",
                    "knowledge_updates": "Quarterly review of platform updates and technology developments"
                }
            }
        }

    def save_rich_educational_profile_from_json(
        self,
        role_id: str,
        topic: str = "Digital Sustainability", 
        eqf_level: int = 6,
        output_dir: str = None
    ) -> List[str]:
        """Save rich educational profile loaded from JSON with all enhanced sections"""
        
        print(f"📋 Generating RICH educational profile for {role_id}...")
        
        # Load rich profile from JSON or create enhanced default
        rich_profile = self.load_educational_profile_from_json(role_id, eqf_level)
        
        # Add role name if not present
        if 'role_name' not in rich_profile:
            # Get role name from roles.json if available
            role_name = self._get_role_name_from_roles_json(role_id)
            rich_profile['role_name'] = role_name
        
        # Save using enhanced method
        return self.save_educational_profile_standalone_enhanced(
            rich_profile, topic, eqf_level
        )

    def _get_role_name_from_roles_json(self, role_id: str) -> str:
        """Get role name from roles.json"""
        try:
            roles_path = self.project_root / "input/roles/roles.json"
            with open(roles_path, 'r', encoding='utf-8') as f:
                roles_data = json.load(f)
            
            for role in roles_data:
                if role.get('id') == role_id:
                    return role.get('name', f'{role_id} Professional')
            
            # Fallback role names
            role_names = {
                'DAN': 'Data Analyst',
                'DSE': 'Data Engineer', 
                'DSI': 'Data Scientist',
                'DSM': 'Digital Sustainability Manager',
                'DSL': 'Digital Sustainability Lead',
                'DSC': 'Digital Sustainability Consultant',
                'SDD': 'Software Developer for Sustainability',
                'SSD': 'Sustainable Solution Designer',
                'STS': 'Sustainability Technical Specialist',
                'SBA': 'Sustainability Business Analyst'
            }
            return role_names.get(role_id, f'{role_id} Professional')
            
        except Exception as e:
            print(f"⚠️ Could not load role name: {e}")
            return f'{role_id} Professional'

    def _normalize_profile_fields_for_html(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize rich profile fields to match HTML generator expectations"""
        
        normalized = profile.copy()
        
        # Map enhanced_competencies to sustainability_competencies for HTML compatibility
        if 'enhanced_competencies' in profile:
            normalized['sustainability_competencies'] = profile['enhanced_competencies']
            print(f"✅ Mapped {len(profile['enhanced_competencies'])} enhanced_competencies to sustainability_competencies")
        
        # Map top-level fields to role_context structure expected by HTML generator
        if 'role_context' not in normalized:
            normalized['role_context'] = {}
        
        # Move industry_sectors and typical_employers to role_context
        if 'industry_sectors' in profile:
            normalized['role_context']['industry_sectors'] = profile['industry_sectors']
            print(f"✅ Mapped {len(profile['industry_sectors'])} industry_sectors to role_context")
            
        if 'typical_employers' in profile:
            normalized['role_context']['typical_employers'] = profile['typical_employers']
            print(f"✅ Mapped {len(profile['typical_employers'])} typical_employers to role_context")
        
        # Map CPD requirements to professional_recognition structure
        if 'professional_recognition' not in normalized:
            normalized['professional_recognition'] = {}
            
        if 'cpd_requirements' in profile:
            normalized['professional_recognition']['cpd_requirements'] = profile['cpd_requirements']
            print(f"✅ Mapped cpd_requirements to professional_recognition")
        
        # Handle assessment_methods structure (schema has EQF level keys)
        if 'assessment_methods' in profile and isinstance(profile['assessment_methods'], dict):
            # Find the first available EQF level or use a default
            for eqf_key in ['4', '5', '6', '7', '8']:
                if eqf_key in profile['assessment_methods']:
                    normalized['assessment_methods'] = profile['assessment_methods'][eqf_key]
                    print(f"✅ Mapped assessment_methods from EQF level {eqf_key}")
                    break
        
        # Handle entry_requirements structure (schema has EQF level keys)  
        if 'entry_requirements' in profile and isinstance(profile['entry_requirements'], dict):
            # Find the first available EQF level or use a default
            for eqf_key in ['4', '5', '6', '7', '8']:
                if eqf_key in profile['entry_requirements']:
                    normalized['entry_requirements'] = profile['entry_requirements'][eqf_key]
                    print(f"✅ Mapped entry_requirements from EQF level {eqf_key}")
                    break
        
        # Ensure required fields for HTML generation
        if 'learning_outcomes_programme' not in normalized:
            # Extract from enhanced_competencies if available
            if 'enhanced_competencies' in profile:
                outcomes = []
                for comp in profile['enhanced_competencies']:
                    outcomes.extend(comp.get('learning_outcomes', [])[:2])  # Take first 2 from each
                normalized['learning_outcomes_programme'] = outcomes[:6]  # Max 6 total
                print(f"✅ Generated {len(normalized['learning_outcomes_programme'])} programme outcomes from competencies")
        
        return normalized

    def save_educational_profile_standalone_enhanced(
        self,
        educational_profile: Any,
        topic: str,
        eqf_level: int
    ) -> List[str]:
        """Save standalone educational profile with FIXED field mapping"""

        # Create output directory
        profile_dir = self.project_root / "output" / "educational_profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)

        # FIXED: Proper role ID and name extraction
        if isinstance(educational_profile, dict):
            role_id = educational_profile.get('id', educational_profile.get('role_id', 'UNKNOWN'))
            role_name = educational_profile.get('role_name', self._get_role_name_from_roles_json(role_id))
        else:
            role_id = getattr(educational_profile, 'id', getattr(educational_profile, 'role_id', 'UNKNOWN'))
            role_name = getattr(educational_profile, 'role_name', self._get_role_name_from_roles_json(role_id))

        # Add role_name to profile if missing
        if isinstance(educational_profile, dict):
            educational_profile['role_name'] = role_name
        else:
            educational_profile.role_name = role_name

        print(f"🔧 Processing profile for {role_name} ({role_id})")

        # Generate proper filenames
        timestamp = datetime.now().strftime('%Y%m%d')
        topic_clean = topic.upper().replace(' ', '_')
        profile_id = f"EP_{role_id}_{topic_clean}_{eqf_level}_{timestamp}"
        
        json_filename = f"{profile_id}.json"
        html_filename = f"{profile_id}.html"

        json_path = profile_dir / json_filename
        html_path = profile_dir / html_filename

        try:
            # Convert to dict and normalize fields
            if isinstance(educational_profile, dict):
                profile_dict = educational_profile
            else:
                profile_dict = self._convert_educational_profile_to_dict(educational_profile)
            
            # FIXED: Normalize fields for HTML compatibility
            normalized_profile = self._normalize_profile_fields_for_html(profile_dict)
            
            # Save JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(normalized_profile, f, indent=2, ensure_ascii=False)

            # Generate HTML using normalized profile
            html_content = self._generate_educational_profile_html(
                normalized_profile, role_name, eqf_level
            )

            # Save HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✅ Saved FIXED educational profile: {json_filename}")
            print(f"✅ Saved FIXED educational profile HTML: {html_filename}")

            return [str(json_path), str(html_path)]

        except Exception as e:
            print(f"❌ Error saving educational profile: {e}")
            import traceback
            traceback.print_exc()
            return []

    def save_rich_educational_profile_from_json_fixed(
        self,
        role_id: str,
        topic: str = "Digital Sustainability", 
        eqf_level: int = 6,
        output_dir: str = None
    ) -> List[str]:
        """FIXED: Save rich educational profile with proper field mapping"""
        
        print(f"📋 Generating FIXED RICH educational profile for {role_id}...")
        
        # Load rich profile from JSON or create enhanced default
        rich_profile = self.load_educational_profile_from_json(role_id, eqf_level)
        
        # Add role name if not present
        if 'role_name' not in rich_profile:
            role_name = self._get_role_name_from_roles_json(role_id)
            rich_profile['role_name'] = role_name
        
        # Save using FIXED enhanced method
        return self.save_educational_profile_standalone_enhanced(
            rich_profile, topic, eqf_level
        )

    def _generate_rich_curriculum_html(self, curriculum: Dict[str, Any], topic: str, eqf_level: int) -> str:
        """Generate RICH HTML curriculum matching the DSM structure"""
        
        metadata = curriculum.get('metadata', {})
        quality_metrics = curriculum.get('quality_metrics', {})
        semesters = curriculum.get('curriculum_structure', {}).get('semester_breakdown', [])
        modules = curriculum.get('modules', [])
        educational_profile = curriculum.get('educational_profile', {})
        learning_pathways = curriculum.get('learning_pathways', {})
        assessment_framework = curriculum.get('assessment_framework', {})
        
        role_id = metadata.get('role_id', 'Unknown')
        role_name = metadata.get('role_name', 'Unknown Role')
        actual_ects = metadata.get('actual_ects', 0)
        num_modules = metadata.get('num_modules', 0)
        
        # Extract quality metrics
        ects_efficiency = quality_metrics.get('ects_efficiency', 0)
        topic_relevance = quality_metrics.get('topic_relevance', 0)
        topic_coverage = quality_metrics.get('topic_coverage', 0)
        flexibility_score = quality_metrics.get('flexibility_score', 0)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{role_name} in {topic}</title>
{self._get_enhanced_css()}
</head>
<body>
<div class="container">
<header class="header">
<h1>📚 {role_name} in {topic}</h1>
<div class="metadata">
<span class="badge">Role: {role_id}</span>
<span class="badge">EQF Level {eqf_level}</span>
<span class="badge">{actual_ects} ECTS</span>
<span class="badge">{num_modules} Modules</span>
<span class="badge">{len(semesters)} Semesters</span>
<span class="badge">T3.2/T3.4 Compliant</span>
</div>
</header>
<main>
<section class="section">
<div class="section-header">📋 Curriculum Overview</div>
<div class="section-content">
<div class="overview-grid">
<div class="overview-card">
<h3>📚 Programme Details</h3>
<p><strong>Focus:</strong> {topic}</p>
<p><strong>ECTS:</strong> {actual_ects} (target: {metadata.get('target_ects', actual_ects)})</p>
<p><strong>Duration:</strong> {len(semesters)} semesters</p>
<p><strong>Delivery:</strong> blended, online</p>
</div>
<div class="overview-card">
<h3>📊 Quality Metrics</h3>
<p><strong>ECTS Efficiency:</strong> {ects_efficiency}%</p>
<p><strong>Topic Relevance:</strong> {topic_relevance}/10</p>
<p><strong>Topic Coverage:</strong> {topic_coverage}%</p>
<p><strong>Flexibility Score:</strong> {flexibility_score}%</p>
</div>
</div>
</div>
</section>"""

        # Add semester structure
        if semesters:
            html_content += """
<section class="section">
<div class="section-header">📅 Semester Structure</div>
<div class="section-content">"""
            
            for semester in semesters:
                semester_modules = semester.get('modules', [])
                semester_name = semester.get('semester_name', f"Semester {semester.get('semester_number', 1)}")
                focus_area = semester.get('focus_area', 'General Focus')
                target_ects = semester.get('target_ects', 0)
                objectives = semester.get('learning_objectives', [])
                
                html_content += f"""
<div class="semester-card">
<div class="semester-header">
<h3>{semester_name}</h3>
<div class="semester-meta">
<span class="focus-badge">{focus_area}</span>
<span class="ects-badge">{target_ects} ECTS</span>
<span class="modules-badge">{len(semester_modules)} Modules</span>
</div>
</div>"""
                
                if objectives:
                    html_content += """
<div class="objectives">
<h4>Learning Objectives:</h4>
<ul>"""
                    for objective in objectives:
                        html_content += f"<li>{objective}</li>"
                    html_content += """
</ul>
</div>"""
                
                if semester_modules:
                    html_content += """
<div class="semester-modules">
<h4>Modules:</h4>
<div class="modules-grid">"""
                    for module in semester_modules:
                        module_name = module.get('module_name', 'Unknown Module')
                        module_ects = module.get('ects', 5)
                        thematic_area = module.get('thematic_area', 'General')
                        html_content += f"""
<div class="module-mini-card">
<h5>{module_name}</h5>
<p class="module-info">{module_ects} ECTS • {thematic_area}</p>
</div>"""
                    html_content += """
</div>
</div>"""
                
                html_content += "</div>"
            
            html_content += """
</div>
</section>"""

        # Add module catalog
        if modules:
            html_content += """
<section class="section">
<div class="section-header">📖 Complete Module Catalog</div>
<div class="section-content">
<div class="modules-catalog">"""
            
            for module in modules:
                module_title = module.get('title', 'Unknown Module')
                module_desc = module.get('description', '')
                module_ects = module.get('ects', 5)
                module_eqf = module.get('eqf_level', 6)
                thematic_area = module.get('thematic_area', 'General')
                delivery_methods = module.get('delivery_methods', [])
                topics = module.get('topics', [])
                
                html_content += f"""
<div class="module-card">
<div class="module-card-header">
<h4>{module_title}</h4>
<div class="module-badges">
<span class="ects-badge">{module_ects} ECTS</span>
<span class="eqf-badge">EQF {module_eqf}</span>
<span class="area-badge">{thematic_area}</span>
</div>
</div>
<p class="module-description">{module_desc}</p>
<div class="delivery-methods">
<strong>Delivery:</strong> 
<span>{', '.join(delivery_methods)}</span>
</div>"""
                
                if topics:
                    html_content += """
<div class="module-topics">
<strong>Topics:</strong> """
                    for topic_item in topics[:10]:  # Show max 10 topics
                        html_content += f'<span class="topic-tag">{topic_item}</span>'
                    html_content += """
</div>"""
                
                html_content += "</div>"
            
            html_content += """
</div>
</div>
</section>"""

        # Footer
        generator_version = metadata.get('generator_version', 'DSCG v3.1')
        curriculum_id = curriculum.get('curriculum_id', 'N/A')
        generated_date = metadata.get('generated_date', '')
        
        html_content += f"""
</main>
<footer class="footer">
<p><strong>Curriculum Generated by {generator_version}</strong></p>
<p>Generated: {generated_date}</p>
<p><em>T3.2 & T3.4 Compliant Digital Sustainability Curriculum</em></p>
</footer>
</div>
</body>
</html>"""

        return html_content

    def _get_enhanced_css(self) -> str:
        """Get enhanced CSS for rich curriculum HTML"""
        return """
        <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .header h1 { font-size: 2.5rem; margin-bottom: 1.5rem; }
        .metadata { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
        .badge { background: rgba(255, 255, 255, 0.25); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; }
        .section { background: white; margin-bottom: 2rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden; }
        .section-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem 2rem; font-size: 1.5rem; font-weight: 600; }
        .section-content { padding: 2rem; }
        .overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
        .overview-card { background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea; }
        .overview-card h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.2rem; }
        .semester-card { background: white; margin-bottom: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }
        .semester-header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .semester-meta { display: flex; gap: 0.5rem; }
        .focus-badge, .ects-badge, .modules-badge { background: rgba(255, 255, 255, 0.25); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; }
        .objectives { padding: 1.5rem; }
        .objectives h4 { color: #10b981; margin-bottom: 1rem; }
        .semester-modules { padding: 1.5rem; background: #f8f9fa; }
        .modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .module-mini-card { background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; }
        .module-mini-card h5 { color: #667eea; margin-bottom: 0.5rem; }
        .module-info { font-size: 0.9rem; color: #666; }
        .modules-catalog { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1.5rem; }
        .module-card { background: white; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }
        .module-card-header { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .module-badges { display: flex; gap: 0.5rem; }
        .ects-badge, .eqf-badge, .area-badge { background: rgba(255, 255, 255, 0.25); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; }
        .module-description { padding: 1.5rem; }
        .delivery-methods, .module-topics { padding: 0 1.5rem 1.5rem; }
        .topic-tag { background: #e0f2fe; color: #0369a1; padding: 0.2rem 0.6rem; margin-right: 0.5rem; border-radius: 12px; font-size: 0.8rem; }
        .footer { text-align: center; padding: 2rem; color: #666; background: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-top: 3rem; }
        @media (max-width: 768px) { .overview-grid { grid-template-columns: 1fr; } .modules-catalog { grid-template-columns: 1fr; } .modules-grid { grid-template-columns: 1fr; } }
        </style>
        """

    def _generate_curriculum_summary(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Generate curriculum summary"""
        metadata = curriculum.get('metadata', {})
        
        return {
            'curriculum_id': curriculum.get('curriculum_id', ''),
            'role_id': metadata.get('role_id', ''),
            'role_name': metadata.get('role_name', ''),
            'topic': metadata.get('topic', ''),
            'eqf_level': metadata.get('eqf_level', 6),
            'actual_ects': metadata.get('actual_ects', 0),
            'num_modules': metadata.get('num_modules', 0),
            'num_semesters': len(curriculum.get('curriculum_structure', {}).get('semester_breakdown', [])),
            'generated_date': metadata.get('generated_date', ''),
            'generator_version': metadata.get('generator_version', 'DSCG v3.1')
        }