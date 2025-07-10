"""
Enhanced output management with complete HTML generation for T3.2/T3.4 compliance.
Handles saving curricula and educational profiles in multiple formats.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict, is_dataclass

class OutputManager:
    """Enhanced output manager with complete HTML generation"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def save_curriculum(
        self,
        curriculum: Dict[str, Any],
        output_dir: str,
        topic: str,
        eqf_level: int,
        role_id: str = "DSC"
    ) -> List[str]:
        """Save curriculum and educational profile in multiple formats"""

        print(f"💾 Saving curriculum and educational profile outputs...")

        # Generate file names
        timestamp = datetime.now().strftime("%Y%m%d")
        base_filename = self._generate_filename(topic, eqf_level, role_id, timestamp)

        # Ensure output directories exist
        curriculum_output_path = self.project_root / output_dir
        profile_output_path = self.project_root / "output" / "educational_profiles"

        curriculum_output_path.mkdir(parents=True, exist_ok=True)
        profile_output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # Save curriculum files
        json_file = curriculum_output_path / f"{base_filename}.json"
        self._save_json_curriculum(curriculum, json_file)
        saved_files.append(str(json_file))

        summary_file = curriculum_output_path / f"{base_filename}_summary.json"
        summary_data = self._generate_summary(curriculum)
        self._save_json_curriculum(summary_data, summary_file)
        saved_files.append(str(summary_file))

        # Enhanced HTML curriculum generation
        html_file = curriculum_output_path / f"{base_filename}.html"
        self._save_html_curriculum(curriculum, html_file, topic, eqf_level, role_id)
        saved_files.append(str(html_file))

        # Save Educational Profile if it exists
        if 'educational_profile' in curriculum:
            profile_filename = f"EP_{role_id}_{topic.upper().replace(' ', '_')}_{eqf_level}_{timestamp}"

            # Save Educational Profile as JSON
            profile_json_file = profile_output_path / f"{profile_filename}.json"
            profile_data = self._extract_educational_profile(curriculum)
            self._save_json_curriculum(profile_data, profile_json_file)
            saved_files.append(str(profile_json_file))

            # Save Educational Profile as HTML
            profile_html_file = profile_output_path / f"{profile_filename}.html"
            self._save_html_educational_profile(profile_data, profile_html_file)
            saved_files.append(str(profile_html_file))

            print(f"📋 Educational Profile saved: {profile_filename}")

        print(f"✅ Saved {len(saved_files)} output files")
        return saved_files

    def save_educational_profile_standalone(
        self,
        educational_profile: Any,
        topic: str = None,
        eqf_level: int = None,
        role_id: str = None,
        output_dir: str = None
    ) -> List[str]:
        """Save standalone educational profile with enhanced parameters"""

        print(f"📋 Saving standalone educational profile...")

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d")

        # Handle both dataclass objects and dictionaries
        if hasattr(educational_profile, 'role_id'):
            actual_role_id = educational_profile.role_id
        else:
            actual_role_id = educational_profile.get('role_id', role_id or 'UNKNOWN')

        topic_str = topic.upper().replace(' ', '_') if topic else "GENERAL"

        if hasattr(educational_profile, 'target_eqf_level'):
            eqf_str = str(educational_profile.target_eqf_level)
        else:
            eqf_str = str(eqf_level) if eqf_level else str(educational_profile.get('target_eqf_level', 6))

        profile_filename = f"EP_{actual_role_id}_{topic_str}_{eqf_str}_{timestamp}"

        # Determine output directory
        if output_dir:
            profile_output_path = Path(output_dir)
        else:
            profile_output_path = self.project_root / "output" / "educational_profiles"

        profile_output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # Convert educational profile to dict for saving
        profile_data = self._convert_educational_profile_to_dict(educational_profile)

        # Save as JSON
        profile_json_file = profile_output_path / f"{profile_filename}.json"
        self._save_json_curriculum(profile_data, profile_json_file)
        saved_files.append(str(profile_json_file))

        # Save as HTML
        profile_html_file = profile_output_path / f"{profile_filename}.html"
        self._save_html_educational_profile(profile_data, profile_html_file)
        saved_files.append(str(profile_html_file))

        print(f"✅ Standalone Educational Profile saved: {profile_filename}")
        return saved_files

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

        print(f"📋 Creating reduced educational profile for {role_name}...")

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

    def _save_html_educational_profile(self, profile_data: Dict[str, Any], file_path: Path) -> None:
        """Save educational profile as HTML"""

        html_content = self._generate_educational_profile_html(profile_data, profile_data.get('role_name', 'Unknown Role'), profile_data.get('target_eqf_level', 6))

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
        html = (
            f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Profile: {role_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6; color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 3rem 2rem; border-radius: 15px;
            margin-bottom: 2rem; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 1.5rem; }}
        .metadata {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }}
        .badge {{
            background: rgba(255, 255, 255, 0.25); padding: 0.5rem 1rem;
            border-radius: 25px; font-size: 0.9rem;
        }}
        .profile-standard {{ background-color: #10b981 !important; }}
        .profile-reduced {{ background-color: #f59e0b !important; }}
        .section {{
            background: white; margin-bottom: 2rem; border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden;
        }}
        .section-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 1.5rem 2rem; font-size: 1.5rem; font-weight: 600;
        }}
        .section-content {{ padding: 2rem; }}
        .profile-info {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        .info-card {{
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea;
        }}
        .info-card h3 {{ color: #667eea; margin-bottom: 1rem; font-size: 1.2rem; }}
        .programme-outcomes {{ list-style: none; padding: 0; }}
        .programme-outcomes li {{
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1rem 1.5rem; margin-bottom: 1rem; border-radius: 8px;
            border-left: 4px solid #10b981; position: relative;
        }}
        .programme-outcomes li:before {{
            content: "🎯"; position: absolute; left: -2px; top: 50%;
            transform: translateY(-50%); background: white; padding: 0.2rem; border-radius: 50%;
        }}
        .competencies-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .competency-item {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 1.5rem; border-radius: 10px; border-left: 5px solid #10b981;
        }}
        .competency-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 1rem;
        }}
        .level {{
            padding: 0.2rem 0.8rem; border-radius: 12px;
            font-size: 0.8rem; font-weight: bold;
        }}
        .level-proficient {{ background: #10b981; color: white; }}
        .level-advanced {{ background: #3b82f6; color: white; }}
        .level-expert {{ background: #8b5cf6; color: white; }}
        .competency-outcomes {{ margin-left: 1.5rem; margin-top: 0.5rem; }}
        .two-column-list {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }}
        .list-item {{
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;
        }}
        .requirements-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }}
        .requirement-card {{
            background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
            padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f59e0b;
        }}
        .requirement-card h4 {{ color: #d97706; margin-bottom: 0.5rem; }}
        .footer {{
            text-align: center; padding: 2rem; color: #666;
            background: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-top: 3rem;
        }}
        @media (max-width: 768px) {{
            .profile-info {{ grid-template-columns: 1fr; }}
            .competencies-grid {{ grid-template-columns: 1fr; }}
            .two-column-list {{ grid-template-columns: 1fr; }}
            .requirements-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📋 Educational Profile: {role_name}</h1>
            <div class="metadata">
                <span class="badge">Role: {role_id}</span>
                <span class="badge">EQF Level {eqf_level}</span>
                <span class="badge">{target_ects} ECTS</span>
                <span class="badge">T3.2 Compliant</span>
                <span class="badge {profile_badge_class}">{profile_badge_text}</span>
            </div>
        </header>

        <main>
            <section class="section">
                <div class="section-header">📋 Profile Overview</div>
                <div class="section-content">
                    <div class="profile-info">
                        <div class="info-card">
                            <h3>Role Information</h3>
                            <p><strong>Role:</strong> {role_name} ({role_id})</p>
                            <p><strong>EQF Level:</strong> {eqf_level}</p>
                            <p><strong>Profile Type:</strong> {profile_type.title()}</p>
                        </div>
                        <div class="info-card">
                            <h3>Programme Structure</h3>
                            <p><strong>Target ECTS:</strong> {target_ects}</p>
                            <p><strong>Duration:</strong> {len(semesters)} semesters</p>
                            <p><strong>Learning Mode:</strong> {profile.get('learning_mode', 'flexible')}</p>
                        </div>
                        <div class="info-card">
                            <h3>Delivery Methods</h3>
                            <p><strong>Methods:</strong> {', '.join(profile.get('delivery_methods', ['blended']))}</p>
                            <p><strong>Compliance:</strong> T3.2, T3.4, EQF, ECTS, ECVET</p>
                        </div>
                    </div>
                </div>
            </section>'''
        )

        # Programme Learning Outcomes
        if programme_outcomes:
            html += '''
            <section class="section">
                <div class="section-header">🎯 Programme Learning Outcomes</div>
                <div class="section-content">
                    <ul class="programme-outcomes">
                        {''.join([f'<li>{outcome}</li>' for outcome in programme_outcomes])}
                    </ul>
                </div>
            </section>'''

        # Entry Requirements
        if entry_requirements:
            html += '''
            <section class="section">
                <div class="section-header">📚 Entry Requirements</div>
                <div class="section-content">
                    <div class="requirements-grid">'''

            for req_type, req_text in entry_requirements.items():
                if req_text:
                    html += f'''
                        <div class="requirement-card">
                            <h4>{req_type.replace('_', ' ').title()}</h4>
                            <p>{req_text}</p>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''

        # Sustainability Competencies
        if sustainability_competencies:
            print(f"✅ Adding {len(sustainability_competencies)} competencies to HTML")
            html += '''
            <section class="section">
                <div class="section-header">🌱 Sustainability Competencies</div>
                <div class="section-content">
                    <div class="competencies-grid">'''

            for comp in sustainability_competencies:
                comp_name = comp.get('competency_name', 'Unknown Competency')
                comp_level = comp.get('competency_level', 'Proficient').lower()
                learning_outcomes = comp.get('learning_outcomes', [])

                print(f"   Adding competency: {comp_name} ({comp_level})")

                html += f'''
                        <div class="competency-item">
                            <div class="competency-header">
                                <strong>{comp_name}</strong>
                                <span class="level level-{comp_level}">({comp_level.title()})</span>
                            </div>
                            <ul class="competency-outcomes">{''.join([f'<li>{outcome}</li>' for outcome in learning_outcomes])}</ul>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''
        else:
            print("⚠️ No sustainability competencies found in profile data")

        # Assessment Methods
        if assessment_methods:
            html += '''
            <section class="section">
                <div class="section-header">📊 Assessment Methods</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{method}</div>' for method in assessment_methods])}
                    </div>
                </div>
            </section>'''

        # Industry Sectors
        if industry_sectors:
            html += '''
            <section class="section">
                <div class="section-header">🏭 Industry Sectors</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{sector}</div>' for sector in industry_sectors])}
                    </div>
                </div>
            </section>'''

        # Career Pathways
        if career_pathways:
            html += '''
            <section class="section">
                <div class="section-header">🚀 Career Pathways</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{pathway}</div>' for pathway in career_pathways])}
                    </div>
                </div>
            </section>'''

        # Typical Employers
        if typical_employers:
            html += '''
            <section class="section">
                <div class="section-header">🏢 Typical Employers</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{employer}</div>' for employer in typical_employers])}
                    </div>
                </div>
            </section>'''

        # Professional Bodies
        if professional_bodies:
            html += '''
            <section class="section">
                <div class="section-header">🤝 Professional Bodies</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{body}</div>' for body in professional_bodies])}
                    </div>
                </div>
            </section>'''

        # Certification Pathways
        if certification_pathways:
            html += '''
            <section class="section">
                <div class="section-header">🏆 Certification Pathways</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{cert}</div>' for cert in certification_pathways])}
                    </div>
                </div>
            </section>'''

        # CPD Requirements
        if cpd_requirements:
            html += '''
            <section class="section">
                <div class="section-header">📈 Continuing Professional Development</div>
                <div class="section-content">
                    <div class="requirements-grid">'''

            for cpd_type, cpd_value in cpd_requirements.items():
                if cpd_value:
                    html += f'''
                        <div class="requirement-card">
                            <h4>{cpd_type.replace('_', ' ').title()}</h4>
                            <p>{cpd_value}</p>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''

        html += f'''
        </main>

        <footer class="footer">
            <p><strong>Educational Profile</strong> generated by DSCG v3.1 - T3.2/T3.4 Compliant</p>
            <p>Generated: {profile.get('creation_date', 'Unknown')} | Version: {profile.get('version', '1.0')}</p>
        </footer>
    </div>
</body>
</html>'''

        print(f"✅ HTML generated successfully with {len(html)} characters")
        return html

    def _generate_enhanced_educational_profile_html(self, profile, role_name, eqf_level):
        """Generate enhanced HTML with all sections from educational_profiles.json"""

        # Extract data
        role_id = profile.get('role_id', 'Unknown')
        target_ects = profile.get('target_ects', 60)
        profile_type = profile.get('profile_type', 'standard')

        # Get rich content
        sustainability_competencies = profile.get('sustainability_competencies', [])
        programme_outcomes = profile.get('learning_outcomes_programme', [])
        entry_requirements = profile.get('entry_requirements', {})
        assessment_methods = profile.get('assessment_methods', [])

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

        # Semester structure
        semester_structure = profile.get('semester_structure', {})
        semesters = semester_structure.get('semesters', [])

        profile_badge_class = "profile-standard" if profile_type == "standard" else "profile-reduced"
        profile_badge_text = "Standard Profile" if profile_type == "standard" else "Reduced Profile"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Profile: {role_name}</title>
    <style>
        {self._get_enhanced_profile_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📋 Educational Profile: {role_name}</h1>
            <div class="metadata">
                <span class="badge">Role: {role_id}</span>
                <span class="badge">EQF Level {eqf_level}</span>
                <span class="badge">{target_ects} ECTS</span>
                <span class="badge">T3.2 Compliant</span>
                <span class="badge {profile_badge_class}">{profile_badge_text}</span>
            </div>
        </header>

        <main>
            <section class="section">
                <div class="section-header">📋 Profile Overview</div>
                <div class="section-content">
                    <div class="profile-info">
                        <div class="info-card">
                            <h3>Role Information</h3>
                            <p><strong>Role:</strong> {role_name} ({role_id})</p>
                            <p><strong>EQF Level:</strong> {eqf_level}</p>
                            <p><strong>Profile Type:</strong> {profile_type.title()}</p>
                        </div>
                        <div class="info-card">
                            <h3>Programme Structure</h3>
                            <p><strong>Target ECTS:</strong> {target_ects}</p>
                            <p><strong>Duration:</strong> {len(semesters)} semesters</p>
                            <p><strong>Learning Mode:</strong> {profile.get('learning_mode', 'flexible')}</p>
                        </div>
                        <div class="info-card">
                            <h3>Delivery Methods</h3>
                            <p><strong>Methods:</strong> {', '.join(profile.get('delivery_methods', ['blended']))}</p>
                            <p><strong>Compliance:</strong> T3.2, T3.4, EQF, ECTS, ECVET</p>
                        </div>
                    </div>
                </div>
            </section>'''

        # Programme Learning Outcomes
        if programme_outcomes:
            html += '''
            <section class="section">
                <div class="section-header">🎯 Programme Learning Outcomes</div>
                <div class="section-content">
                    <ul class="programme-outcomes">
                        {''.join([f'<li>{outcome}</li>' for outcome in programme_outcomes])}
                    </ul>
                </div>
            </section>'''

        # Entry Requirements
        if entry_requirements:
            html += '''
            <section class="section">
                <div class="section-header">📚 Entry Requirements</div>
                <div class="section-content">
                    <div class="requirements-grid">'''

            for req_type, req_text in entry_requirements.items():
                if req_text:
                    html += f'''
                        <div class="requirement-card">
                            <h4>{req_type.replace('_', ' ').title()}</h4>
                            <p>{req_text}</p>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''

        # Sustainability Competencies
        if sustainability_competencies:
            html += '''
            <section class="section">
                <div class="section-header">🌱 Sustainability Competencies</div>
                <div class="section-content">
                    <div class="competencies-grid">'''

            for comp in sustainability_competencies:
                comp_name = comp.get('competency_name', 'Unknown Competency')
                comp_level = comp.get('competency_level', 'Proficient').lower()
                learning_outcomes = comp.get('learning_outcomes', [])

                html += f'''
                        <div class="competency-item">
                            <div class="competency-header">
                                <strong>{comp_name}</strong>
                                <span class="level level-{comp_level}">({comp_level.title()})</span>
                            </div>
                            <ul class="competency-outcomes">{''.join([f'<li>{outcome}</li>' for outcome in learning_outcomes])}</ul>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''

        # Assessment Methods
        if assessment_methods:
            html += '''
            <section class="section">
                <div class="section-header">📊 Assessment Methods</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{method}</div>' for method in assessment_methods])}
                    </div>
                </div>
            </section>'''

        # Industry Sectors
        if industry_sectors:
            html += '''
            <section class="section">
                <div class="section-header">🏭 Industry Sectors</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{sector}</div>' for sector in industry_sectors])}
                    </div>
                </div>
            </section>'''

        # Career Pathways
        if career_pathways:
            html += '''
            <section class="section">
                <div class="section-header">🚀 Career Pathways</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{pathway}</div>' for pathway in career_pathways])}
                    </div>
                </div>
            </section>'''

        # Typical Employers
        if typical_employers:
            html += '''
            <section class="section">
                <div class="section-header">🏢 Typical Employers</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{employer}</div>' for employer in typical_employers])}
                    </div>
                </div>
            </section>'''

        # Professional Bodies
        if professional_bodies:
            html += '''
            <section class="section">
                <div class="section-header">🤝 Professional Bodies</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{body}</div>' for body in professional_bodies])}
                    </div>
                </div>
            </section>'''

        # Certification Pathways
        if certification_pathways:
            html += '''
            <section class="section">
                <div class="section-header">🏆 Certification Pathways</div>
                <div class="section-content">
                    <div class="two-column-list">
                        {''.join([f'<div class="list-item">{cert}</div>' for cert in certification_pathways])}
                    </div>
                </div>
            </section>'''

        # CPD Requirements
        if cpd_requirements:
            html += '''
            <section class="section">
                <div class="section-header">📈 Continuing Professional Development</div>
                <div class="section-content">
                    <div class="requirements-grid">'''

            for cpd_type, cpd_value in cpd_requirements.items():
                if cpd_value:
                    html += f'''
                        <div class="requirement-card">
                            <h4>{cpd_type.replace('_', ' ').title()}</h4>
                            <p>{cpd_value}</p>
                        </div>'''

            html += '''
                    </div>
                </div>
            </section>'''

        html += f'''
        </main>

        <footer class="footer">
            <p><strong>Educational Profile</strong> generated by DSCG v3.1 - T3.2/T3.4 Compliant</p>
            <p>Generated: {profile.get('creation_date', 'Unknown')} | Version: {profile.get('version', '1.0')}</p>
        </footer>
    </div>
</body>
</html>'''

        return html

    def _get_enhanced_profile_css_styles(self) -> str:
        """Get enhanced CSS styles for educational profile HTML."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .metadata {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(255, 255, 255, 0.25);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .profile-standard { background-color: #10b981 !important; }
        .profile-reduced { background-color: #f59e0b !important; }

        .section {
            background: white;
            margin-bottom: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 2rem;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .section-content {
            padding: 2rem;
        }

        .profile-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }

        .info-card {
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }

        .info-card h3 {
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }

        .programme-outcomes {
            list-style: none;
            padding: 0;
        }

        .programme-outcomes li {
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border-left: 4px solid #10b981;
            position: relative;
        }

        .programme-outcomes li:before {
            content: "🎯";
            position: absolute;
            left: -2px;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            padding: 0.2rem;
            border-radius: 50%;
        }

        .competencies-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .competency-item {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #10b981;
        }

        .competency-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .level {
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .level-proficient { background: #10b981; color: white; }
        .level-advanced { background: #3b82f6; color: white; }
        .level-expert { background: #8b5cf6; color: white; }

        .competency-outcomes {
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }

        .two-column-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }

        .list-item {
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .requirements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }

        .requirement-card {
            background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #f59e0b;
        }

        .requirement-card h4 {
            color: #d97706;
            margin-bottom: 0.5rem;
        }

        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            margin-top: 3rem;
        }

        @media (max-width: 768px) {
            .profile-info { grid-template-columns: 1fr; }
            .competencies-grid { grid-template-columns: 1fr; }
            .two-column-list { grid-template-columns: 1fr; }
            .requirements-grid { grid-template-columns: 1fr; }
        }
        """

    def _save_html_curriculum(self, curriculum: Dict[str, Any], file_path: Path, topic: str, eqf_level: int, role_id: str) -> None:
        """Save curriculum as comprehensive HTML"""

        html_content = self._generate_curriculum_html(curriculum, topic, eqf_level, role_id)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            raise ValueError(f"Error saving Curriculum HTML: {e}")

    def _generate_curriculum_html(self, curriculum: Dict[str, Any], topic: str, eqf_level: int, role_id: str) -> str:
        """Generate comprehensive curriculum HTML"""

        metadata = curriculum.get('metadata', {})
        educational_profile = curriculum.get('educational_profile', {})
        modules = curriculum.get('modules', [])
        quality_metrics = curriculum.get('quality_metrics', {})

        curriculum_title = f"{role_id} Digital Sustainability Curriculum: {topic}"

        # Generate modules HTML
        modules_html = ""
        total_ects = 0

        for i, module in enumerate(modules, 1):
            module_title = module.get('title', f'Module {i}')
            module_ects = module.get('ects', 5)
            module_level = module.get('level', 'Intermediate')
            module_topics = module.get('topics', [])
            module_outcomes = module.get('learning_outcomes', [])

            total_ects += module_ects

            topics_html = ''.join(f'<span class="topic-tag">{topic}</span>' for topic in module_topics[:5])
            outcomes_html = ''.join(f'<li>{outcome}</li>' for outcome in module_outcomes[:3])

            modules_html += f"""
            <div class="module-card">
                <div class="module-header">
                    <h4>{module_title}</h4>
                    <div class="module-meta">
                        <span class="ects-badge">{module_ects} ECTS</span>
                        <span class="level-badge level-{module_level.lower()}">{module_level}</span>
                    </div>
                </div>
                <div class="module-content">
                    <div class="topics-section">
                        <strong>Key Topics:</strong>
                        <div class="topics-tags">{topics_html}</div>
                    </div>
                    {f'<div class="outcomes-section"><strong>Learning Outcomes:</strong><ul>{outcomes_html}</ul></div>' if outcomes_html else ''}
                </div>
            </div>
            """

        # Quality metrics
        efficiency = quality_metrics.get('ects_efficiency', 0)
        relevance = quality_metrics.get('relevance_score', 0)
        coverage = quality_metrics.get('topic_coverage', 0)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{curriculum_title}</title>
    <style>
        {self._get_curriculum_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📚 {curriculum_title}</h1>
            <div class="metadata">
                <span class="badge">EQF Level {eqf_level}</span>
                <span class="badge">{total_ects} ECTS</span>
                <span class="badge">{len(modules)} Modules</span>
                <span class="badge">T3.2/T3.4 Compliant</span>
            </div>
        </header>

        <main>
            <section class="section">
                <div class="section-header">📊 Curriculum Overview</div>
                <div class="section-content">
                    <div class="overview-grid">
                        <div class="overview-card">
                            <h3>Programme Details</h3>
                            <p><strong>Topic:</strong> {topic}</p>
                            <p><strong>Role:</strong> {role_id}</p>
                            <p><strong>EQF Level:</strong> {eqf_level}</p>
                            <p><strong>Total ECTS:</strong> {total_ects}</p>
                        </div>
                        <div class="overview-card">
                            <h3>Structure</h3>
                            <p><strong>Modules:</strong> {len(modules)}</p>
                            <p><strong>Semesters:</strong> {educational_profile.get('duration_semesters', 'N/A')}</p>
                            <p><strong>Delivery:</strong> {', '.join(educational_profile.get('delivery_methods', ['Flexible']))}</p>
                        </div>
                        <div class="overview-card">
                            <h3>Quality Metrics</h3>
                            <p><strong>ECTS Efficiency:</strong> {efficiency:.1f}%</p>
                            <p><strong>Relevance Score:</strong> {relevance:.1f}/10</p>
                            <p><strong>Topic Coverage:</strong> {coverage:.1f}%</p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <div class="section-header">📚 Curriculum Modules</div>
                <div class="section-content">
                    <div class="modules-grid">
                        {modules_html}
                    </div>
                </div>
            </section>
        </main>

        <footer class="footer">
            <p><strong>Digital Sustainability Curriculum</strong> generated by DSCG v3.0</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | T3.2/T3.4 Compliant</p>
        </footer>
    </div>
</body>
</html>"""

        return html

    def _get_curriculum_css_styles(self) -> str:
        """Get CSS styles for curriculum HTML"""

        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .metadata {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(255, 255, 255, 0.25);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .section {
            background: white;
            margin-bottom: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 2rem;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .section-content {
            padding: 2rem;
        }

        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .overview-card {
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }

        .overview-card h3 {
            color: #667eea;
            margin-bottom: 1rem;
        }

        .modules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }

        .module-card {
            background: linear-gradient(135deg, #f8f9fc 0%, #e9ecef 100%);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .module-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .module-header {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .module-header h4 {
            font-size: 1.2rem;
        }

        .module-meta {
            display: flex;
            gap: 0.5rem;
        }

        .ects-badge {
            background: rgba(255, 255, 255, 0.3);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
        }

        .level-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: bold;
        }

        .level-beginner { background: #fbbf24; color: #92400e; }
        .level-intermediate { background: #34d399; color: #065f46; }
        .level-advanced { background: #60a5fa; color: #1e3a8a; }

        .module-content {
            padding: 1.5rem;
        }

        .topics-section {
            margin-bottom: 1rem;
        }

        .topics-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }

        .topic-tag {
            background: #e0e7ff;
            color: #3730a3;
            padding: 0.2rem 0.6rem;
            border-radius: 10px;
            font-size: 0.8rem;
        }

        .outcomes-section ul {
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }

        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            margin-top: 3rem;
        }
        """

    # Keep existing utility methods
    def _generate_filename(self, topic: str, eqf_level: int, role_id: str, timestamp: str) -> str:
        """Generate standardized filename"""
        topic_clean = str(topic).upper().replace(" ", "_").replace("-", "_")
        topic_clean = "".join(c for c in topic_clean if c.isalnum() or c == "_")
        return f"{role_id}_{topic_clean}_{eqf_level}_{timestamp}_DSC"

    def _save_json_curriculum(self, data: Dict[str, Any], file_path: Path) -> None:
        """Save curriculum data as JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error saving JSON file {file_path}: {e}")

    def _generate_summary(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary version of curriculum"""
        metadata = curriculum.get('metadata', {})
        educational_profile = curriculum.get('educational_profile', {})
        modules = curriculum.get('modules', [])
        quality_metrics = curriculum.get('quality_metrics', {})

        return {
            "metadata": metadata,
            "educational_profile_summary": {
                "profile_id": educational_profile.get('profile_id', ''),
                "role_name": educational_profile.get('role_name', ''),
                "target_eqf_level": educational_profile.get('target_eqf_level', 6),
                "target_ects": educational_profile.get('target_ects', 60),
                "duration_semesters": educational_profile.get('duration_semesters', 2)
            },
            "module_summary": {
                "total_modules": len(modules),
                "module_titles": [m.get('title', '') for m in modules],
                "total_ects": sum(m.get('ects', 5) for m in modules)
            },
            "quality_metrics": quality_metrics
        }
