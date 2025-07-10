"""
Enhanced Output Manager for T3.2/T3.4 compliant curriculum generation
Clean implementation without f-string issues
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class OutputManager:
    """Manages output generation for curricula and educational profiles"""

    def __init__(self, project_root: Path):
        """Initialize output manager with project root path"""
        self.project_root = project_root


    def _build_framework_alignment_section(self, framework_alignment):
        """Build framework alignment section with European recognition details"""
        if not framework_alignment:
            return []

        html_parts = []
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">🌍 Framework Alignment</div>')
        html_parts.append('<div class="section-content">')

        european_frameworks = framework_alignment.get('european_frameworks', {})
        framework_mappings = european_frameworks.get('framework_mappings', {})
        recognition_mechanisms = european_frameworks.get('recognition_mechanisms', {})

        if framework_mappings:
            html_parts.append('<div class="framework-mappings">')
            html_parts.append('<h4>Framework Mappings</h4>')
            for framework, items in framework_mappings.items():
                html_parts.append('<div class="framework-item">')
                html_parts.append('<strong>' + framework.upper() + ':</strong>')
                html_parts.append('<ul>')
                for item in items:
                    html_parts.append('<li>' + item + '</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')
            html_parts.append('</div>')

        if recognition_mechanisms:
            html_parts.append('<div class="recognition-mechanisms">')
            html_parts.append('<h4>Recognition Mechanisms</h4>')
            for mechanism, description in recognition_mechanisms.items():
                html_parts.append('<div class="mechanism-item">')
                html_parts.append('<strong>' + mechanism.replace('_', ' ').title() + ':</strong>')
                html_parts.append('<p>' + description + '</p>')
                html_parts.append('</div>')
            html_parts.append('</div>')

        html_parts.append('</div>')
        html_parts.append('</section>')

        return html_parts



    def save_curriculum(self, curriculum: Dict[str, Any], output_dir: str, topic: str, eqf_level: int, role_id: str) -> List[str]:
        """Save complete curriculum with educational profile"""

        # Create output directory
        curriculum_dir = Path(output_dir)
        curriculum_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        role_name = curriculum.get('metadata', {}).get('role_name', role_id)
        safe_topic = topic.replace(' ', '_').replace('/', '_').upper()
        timestamp = datetime.now().strftime('%Y%m%d')

        filename_base = f"{role_id}_{safe_topic}_{eqf_level}_{timestamp}"

        json_filename = f"{filename_base}.json"
        html_filename = f"{filename_base}.html"
        summary_filename = f"{filename_base}_summary.json"

        json_path = curriculum_dir / json_filename
        html_path = curriculum_dir / html_filename
        summary_path = curriculum_dir / summary_filename

        output_files = []

        try:
            # Save JSON curriculum
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(curriculum, f, indent=2, ensure_ascii=False)
            output_files.append(str(json_path))

            # Generate and save HTML
            html_content = self._generate_curriculum_html(curriculum, role_name, eqf_level)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            output_files.append(str(html_path))

            # Save summary
            summary = self._create_curriculum_summary(curriculum)
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            output_files.append(str(summary_path))

            print(f"✅ Saved curriculum files: {len(output_files)} files")

        except Exception as e:
            print(f"❌ Error saving curriculum: {e}")

        return output_files

    def save_educational_profile_standalone(self, educational_profile, topic, eqf_level):
        """Save standalone educational profile with clean HTML generation"""

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

            # Generate clean HTML
            html_content = self._generate_comprehensive_educational_profile_html(
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

    def _generate_comprehensive_educational_profile_html(self, profile, role_name, eqf_level):
        """Generate comprehensive HTML with all enhanced sections for any role"""

        # Extract all enhanced data
        role_id = profile.get('role_id', 'Unknown')
        target_ects = profile.get('target_ects', 60)
        profile_type = profile.get('profile_type', 'standard')

        enhanced_competencies = profile.get('enhanced_competencies', [])
        framework_alignment = profile.get('framework_alignment', {})
        modular_structure = profile.get('modular_structure', {})
        career_progression = profile.get('realistic_career_progression', {})

        print(f"🔍 Generating comprehensive HTML for {role_name}")
        print(f"   Enhanced competencies: {len(enhanced_competencies)}")
        print(f"   Framework alignment: {bool(framework_alignment)}")
        print(f"   Modular structure: {bool(modular_structure)}")
        print(f"   Career progression: {bool(career_progression)}")

        html_parts = []

        # Build enhanced HTML sections
        html_parts.extend(self._build_html_header(role_name, role_id, eqf_level, target_ects, profile_type))
        html_parts.extend(self._build_profile_overview(profile, role_name, eqf_level))
        html_parts.extend(self._build_enhanced_competencies_section(enhanced_competencies))
        html_parts.extend(self._build_framework_alignment_section(framework_alignment))
        html_parts.extend(self._build_modular_structure_section(modular_structure))
        html_parts.extend(self._build_career_progression_section(career_progression))
        html_parts.extend(self._build_standard_sections(profile))  # Keep existing sections
        html_parts.extend(self._build_html_footer(profile))

        return '\n'.join(html_parts)

    def _build_html_header(self, role_name, role_id, eqf_level, target_ects, profile_type):
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<title>Educational Profile: ' + role_name + '</title>')
        html_parts.append(self._get_simple_css())
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append('<header class="header">')
        html_parts.append('<h1>📋 Educational Profile: ' + role_name + '</h1>')
        html_parts.append('<div class="metadata">')
        html_parts.append('<span class="badge">Role: ' + role_id + '</span>')
        html_parts.append('<span class="badge">EQF Level ' + str(eqf_level) + '</span>')
        html_parts.append('<span class="badge">' + str(target_ects) + ' ECTS</span>')
        html_parts.append('<span class="badge">' + profile_type.title() + '</span>')
        html_parts.append('</div>')
        html_parts.append('</header>')
        html_parts.append('<main>')
        return html_parts

    def _build_profile_overview(self, profile, role_name, eqf_level):
        html_parts = []
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">📋 Profile Overview</div>')
        html_parts.append('<div class="section-content">')
        html_parts.append('<div class="profile-info">')
        html_parts.append('<div class="info-card">')
        html_parts.append('<h3>Role Information</h3>')
        html_parts.append('<p><strong>Role:</strong> ' + role_name + ' (' + profile.get('role_id', 'Unknown') + ')</p>')
        html_parts.append('<p><strong>EQF Level:</strong> ' + str(eqf_level) + '</p>')
        html_parts.append('<p><strong>Profile Type:</strong> ' + profile.get('profile_type', 'standard').title() + '</p>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</section>')
        return html_parts

    def _build_enhanced_competencies_section(self, competencies):
        """Build enhanced competencies with framework mappings"""
        if not competencies:
            return []

        html_parts = []
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">🌱 Enhanced Sustainability Competencies</div>')
        html_parts.append('<div class="section-content">')
        html_parts.append('<div class="competencies-grid">')

        for comp in competencies:
            comp_name = comp.get('competency_name', 'Unknown Competency')
            comp_level = comp.get('competency_level', 'Proficient').lower()
            learning_outcomes = comp.get('learning_outcomes', [])
            eqf_alignment = comp.get('eqf_alignment', '')
            framework_mappings = comp.get('framework_mappings', {})
            is_transversal = comp.get('transversal', False)

            html_parts.append('<div class="competency-item enhanced">')
            html_parts.append('<div class="competency-header">')
            html_parts.append('<strong>' + comp_name + '</strong>')
            html_parts.append('<span class="level level-' + comp_level + '">(' + comp_level.title() + ')</span>')
            html_parts.append('</div>')

            if eqf_alignment:
                html_parts.append('<div class="eqf-alignment">')
                html_parts.append('<strong>EQF Alignment:</strong> ' + eqf_alignment)
                html_parts.append('</div>')

            if is_transversal:
                html_parts.append('<div class="transversal-badge">Transversal Competency</div>')

            html_parts.append('<ul class="competency-outcomes">')
            for outcome in learning_outcomes:
                html_parts.append('<li>' + outcome + '</li>')
            html_parts.append('</ul>')

            if framework_mappings:
                html_parts.append('<div class="framework-mappings">')
                html_parts.append('<h5>Framework Mappings:</h5>')
                for framework, items in framework_mappings.items():
                    html_parts.append('<div class="framework-item">')
                    html_parts.append('<strong>' + framework.replace('_', '-').upper() + ':</strong> ')
                    html_parts.append(', '.join(items))
                    html_parts.append('</div>')
                html_parts.append('</div>')

            html_parts.append('</div>')

        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</section>')

        return html_parts

    def _build_modular_structure_section(self, modular_structure):
        """Build modular ECTS breakdown section"""
        if not modular_structure:
            return []

        html_parts = []
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">📚 Modular Structure & ECTS Breakdown</div>')
        html_parts.append('<div class="section-content">')

        total_ects = modular_structure.get('total_ects', 0)
        semesters = modular_structure.get('semesters', 0)
        modules = modular_structure.get('modules', [])

        html_parts.append('<div class="modular-overview">')
        html_parts.append('<p><strong>Total ECTS:</strong> ' + str(total_ects) + '</p>')
        html_parts.append('<p><strong>Duration:</strong> ' + str(semesters) + ' semesters</p>')
        html_parts.append('<p><strong>Modules:</strong> ' + str(len(modules)) + '</p>')
        html_parts.append('</div>')

        if modules:
            html_parts.append('<div class="modules-grid">')
            for module in modules:
                html_parts.append('<div class="module-card">')
                html_parts.append('<h4>' + module.get('code', '') + ': ' + module.get('name', '') + '</h4>')
                html_parts.append('<div class="module-meta">')
                html_parts.append('<span class="ects-badge">' + str(module.get('ects', 0)) + ' ECTS</span>')
                html_parts.append('<span class="semester-badge">Semester ' + str(module.get('semester', 1)) + '</span>')
                html_parts.append('</div>')

                frameworks = module.get('frameworks', [])
                if frameworks:
                    html_parts.append('<div class="module-frameworks">')
                    html_parts.append('<strong>Frameworks:</strong> ' + ', '.join(frameworks))
                    html_parts.append('</div>')

                html_parts.append('</div>')
            html_parts.append('</div>')

        html_parts.append('</div>')
        html_parts.append('</section>')

        return html_parts

    def _build_career_progression_section(self, career_progression):
        """Build realistic career progression with salary ranges"""
        if not career_progression:
            return []

        html_parts = []
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">🚀 Realistic Career Progression</div>')
        html_parts.append('<div class="section-content">')
        html_parts.append('<div class="career-stages">')

        stages = {
            'immediate': 'Immediate Opportunities',
            'short_term': 'Short-term Progression',
            'long_term': 'Long-term Aspirations'
        }

        for stage_id, stage_title in stages.items():
            stage_data = career_progression.get(stage_id, {})
            if stage_data:
                html_parts.append('<div class="career-stage">')
                html_parts.append('<h4>' + stage_title + '</h4>')
                html_parts.append('<div class="stage-meta">')
                html_parts.append('<span class="timeframe">' + stage_data.get('timeframe', '') + '</span>')
                html_parts.append('<span class="salary-range">' + stage_data.get('salary_range', '') + '</span>')
                html_parts.append('</div>')

                roles = stage_data.get('roles', [])
                if roles:
                    html_parts.append('<ul class="stage-roles">')
                    for role in roles:
                        html_parts.append('<li>' + role + '</li>')
                    html_parts.append('</ul>')

                html_parts.append('</div>')

        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</section>')

        return html_parts

    def _build_standard_sections(self, profile):
        html_parts = []

        sustainability_competencies = profile.get('sustainability_competencies', [])
        programme_outcomes = profile.get('programme_outcomes', [])
        entry_requirements = profile.get('entry_requirements', {})
        assessment_methods = profile.get('assessment_methods', [])
        industry_sectors = profile.get('industry_sectors', [])
        career_pathways = profile.get('career_pathways', [])
        typical_employers = profile.get('typical_employers', [])
        professional_bodies = profile.get('professional_bodies', [])
        certification_pathways = profile.get('certification_pathways', [])
        cpd_requirements = profile.get('cpd_requirements', {})

        if programme_outcomes:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🎯 Programme Learning Outcomes</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<ul class="programme-outcomes">')
            for outcome in programme_outcomes:
                html_parts.append('<li>' + outcome + '</li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if sustainability_competencies:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🌱 Sustainability Competencies</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="competencies-grid">')

            for comp in sustainability_competencies:
                comp_name = comp.get('competency_name', 'Unknown Competency')
                comp_level = comp.get('competency_level', 'Proficient').lower()
                learning_outcomes = comp.get('learning_outcomes', [])

                html_parts.append('<div class="competency-item">')
                html_parts.append('<div class="competency-header">')
                html_parts.append('<strong>' + comp_name + '</strong>')
                html_parts.append('<span class="level level-' + comp_level + '">(' + comp_level.title() + ')</span>')
                html_parts.append('</div>')
                html_parts.append('<ul class="competency-outcomes">')
                for outcome in learning_outcomes:
                    html_parts.append('<li>' + outcome + '</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')

            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if entry_requirements:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">📚 Entry Requirements</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="requirements-grid">')

            for req_type, req_text in entry_requirements.items():
                if req_text:
                    html_parts.append('<div class="requirement-card">')
                    html_parts.append('<h4>' + req_type.replace('_', ' ').title() + '</h4>')
                    html_parts.append('<p>' + str(req_text) + '</p>')
                    html_parts.append('</div>')

            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if assessment_methods:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">📊 Assessment Methods</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="two-column-list">')
            for method in assessment_methods:
                html_parts.append('<div class="list-item">' + method + '</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if industry_sectors:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🏭 Industry Sectors</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="two-column-list">')
            for sector in industry_sectors:
                html_parts.append('<div class="list-item">' + sector + '</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if career_pathways:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🚀 Career Pathways</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="two-column-list">')
            for pathway in career_pathways:
                html_parts.append('<div class="list-item">' + pathway + '</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if professional_bodies:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🤝 Professional Bodies</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="two-column-list">')
            for body in professional_bodies:
                html_parts.append('<div class="list-item">' + body + '</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if certification_pathways:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🏆 Certification Pathways</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="two-column-list">')
            for pathway in certification_pathways:
                html_parts.append('<div class="list-item">' + pathway + '</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        if cpd_requirements:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">📈 Continuing Professional Development</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="requirements-grid">')

            for cpd_type, cpd_value in cpd_requirements.items():
                if cpd_value:
                    html_parts.append('<div class="requirement-card">')
                    html_parts.append('<h4>' + cpd_type.replace('_', ' ').title() + '</h4>')
                    html_parts.append('<p>' + str(cpd_value) + '</p>')
                    html_parts.append('</div>')

            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        return html_parts

    def _build_html_footer(self, profile):
        html_parts = []
        html_parts.append('</main>')
        html_parts.append('<footer class="footer">')
        html_parts.append('<p><strong>Educational Profile</strong> generated by DSCG v3.1</p>')
        html_parts.append('<p>Generated: ' + str(profile.get('generated_date', 'Unknown')) + '</p>')
        html_parts.append('</footer>')
        html_parts.append('</div>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        return html_parts

    def _get_simple_css(self):
        """Get simple CSS without f-string complications"""
        return '''<style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #667eea; color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; }
        .header h1 { font-size: 2rem; margin-bottom: 1rem; }
        .metadata { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
        .badge { background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; }
        .section { background: white; margin-bottom: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .section-header { background: #667eea; color: white; padding: 1rem 2rem; font-size: 1.3rem; font-weight: bold; }
        .section-content { padding: 2rem; }
        .profile-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
        .info-card { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #667eea; }
        .info-card h3 { color: #667eea; margin-bottom: 1rem; }
        .programme-outcomes { list-style: none; padding: 0; }
        .programme-outcomes li { background: #f8f9fa; padding: 1rem; margin-bottom: 1rem; border-radius: 8px; border-left: 4px solid #10b981; }
        .competencies-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
        .competency-item { background: #f0f9ff; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10b981; }
        .competency-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
        .level { padding: 0.2rem 0.6rem; border-radius: 10px; font-size: 0.8rem; font-weight: bold; }
        .level-proficient { background: #10b981; color: white; }
        .level-advanced { background: #3b82f6; color: white; }
        .level-expert { background: #8b5cf6; color: white; }
        .competency-outcomes { margin-left: 1rem; }
        .two-column-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .list-item { background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; }
        .requirements-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
        .requirement-card { background: #fef3c7; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #f59e0b; }
        .requirement-card h4 { color: #d97706; margin-bottom: 0.5rem; }
        .footer { text-align: center; padding: 2rem; color: #666; background: white; border-radius: 10px; margin-top: 2rem; }
        @media (max-width: 768px) {
            .profile-info, .competencies-grid, .two-column-list, .requirements-grid { grid-template-columns: 1fr; }
        }
        </style>'''

    def _generate_curriculum_html(self, curriculum, role_name, eqf_level):
        """Generate basic curriculum HTML"""
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html><head><title>Curriculum: ' + role_name + '</title></head>')
        html_parts.append('<body><h1>Curriculum for ' + role_name + '</h1>')
        html_parts.append('<p>EQF Level: ' + str(eqf_level) + '</p>')
        html_parts.append('</body></html>')
        return '\n'.join(html_parts)

    def _create_curriculum_summary(self, curriculum):
        """Create curriculum summary"""
        metadata = curriculum.get('metadata', {})
        return {
            'title': metadata.get('title', 'Unknown'),
            'role': metadata.get('role_id', 'Unknown'),
            'eqf_level': metadata.get('eqf_level', 0),
            'ects': metadata.get('actual_ects', 0),
            'generated': metadata.get('generated_date', 'Unknown')
        }
