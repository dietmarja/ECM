# scripts/curriculum_generator/core/output_manager.py

"""
Enhanced Output Manager for T3.2/T3.4 compliant curriculum generation
Supports comprehensive educational profiles with full schema compliance
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class OutputManager:
    """Enhanced output manager with full T3.2 educational profile support"""

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

    def save_curriculum_files(self, curriculum: Dict[str, Any], topic: str, eqf_level: int) -> List[str]:
        """Save curriculum files in multiple formats"""
        saved_files = []
        
        try:
            # Extract basic info
            role_id = curriculum.get('role_id', 'UNKNOWN')
            timestamp = datetime.now().strftime('%Y%m%d')
            
            # Clean topic for filename
            clean_topic = ''.join(c.upper() if c.isalnum() else '_' for c in topic)
            base_filename = f"{role_id}_{clean_topic}_{eqf_level}_{timestamp}"
            
            # Save JSON curriculum
            json_file = self.project_root / 'output' / 'curricula' / f"{base_filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(curriculum, f, indent=2, ensure_ascii=False)
            saved_files.append(str(json_file))
            
            # Save HTML curriculum
            html_file = self.project_root / 'output' / 'curricula' / f"{base_filename}.html"
            html_content = self._generate_curriculum_html(curriculum, topic, eqf_level)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            saved_files.append(str(html_file))
            
            # Save summary
            summary_file = self.project_root / 'output' / 'curricula' / f"{base_filename}_summary.json"
            summary = self._generate_curriculum_summary(curriculum)
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            saved_files.append(str(summary_file))
            
            print(f"✅ Saved curriculum files: {len(saved_files)} files")
            return saved_files
            
        except Exception as e:
            print(f"❌ Error saving curriculum files: {e}")
            return []

    def save_educational_profile_standalone(self, educational_profile: Dict[str, Any], 
                                          topic: str, eqf_level: int) -> List[str]:
        """Save educational profile as standalone files"""
        saved_files = []
        
        try:
            # Extract info for filename
            role_id = educational_profile.get('role_id', 'UNKNOWN')
            timestamp = datetime.now().strftime('%Y%m%d')
            base_filename = f"EP_{role_id}_{eqf_level}_{timestamp}"
            
            # Save JSON profile
            json_file = self.project_root / 'output' / 'educational_profiles' / f"{base_filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(educational_profile, f, indent=2, ensure_ascii=False)
            saved_files.append(str(json_file))
            
            # Save HTML profile
            html_file = self.project_root / 'output' / 'educational_profiles' / f"{base_filename}.html"
            role_name = educational_profile.get('role_name', f'{role_id} Professional')
            html_content = self._generate_clean_educational_profile_html(
                educational_profile, role_name, eqf_level
            )
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            saved_files.append(str(html_file))
            
            print(f"✅ Saved educational profile: {base_filename}.json")
            print(f"✅ Saved educational profile HTML: {base_filename}.html")
            return saved_files
            
        except Exception as e:
            print(f"❌ Error saving educational profile: {e}")
            return []

    def _generate_clean_educational_profile_html(self, profile, role_name, eqf_level):
        """Generate clean HTML without f-string issues - ENHANCED for full schema compliance"""
        
        # Extract data safely - ENHANCED DATA EXTRACTION
        role_id = profile.get('role_id', 'Unknown')
        target_ects = profile.get('target_ects', 60)
        profile_type = profile.get('profile_type', 'standard')
        
        # Enhanced competencies (schema: enhanced_competencies)
        enhanced_competencies = profile.get('enhanced_competencies', [])
        sustainability_competencies = profile.get('sustainability_competencies', [])
        # Use enhanced_competencies if available, fallback to sustainability_competencies
        competencies_to_show = enhanced_competencies if enhanced_competencies else sustainability_competencies
        
        # Programme outcomes
        programme_outcomes = profile.get('learning_outcomes_programme', [])
        if not programme_outcomes:
            programme_outcomes = profile.get('programme_outcomes', [])
        
        # Entry requirements and assessment methods (already handled)
        entry_requirements = profile.get('entry_requirements', {})
        assessment_methods = profile.get('assessment_methods', [])
        
        # Role context
        role_context = profile.get('role_context', {})
        industry_sectors = role_context.get('industry_sectors', [])
        career_pathways = role_context.get('career_pathways', [])
        
        # NEW: Typical employers (schema required field)
        typical_employers = profile.get('typical_employers', [])
        if not typical_employers:
            typical_employers = role_context.get('typical_employers', [])
        
        # NEW: Modular structure (schema required field)
        modular_structure = profile.get('modular_structure', {})
        
        # NEW: Realistic career progression (schema required field)
        realistic_career_progression = profile.get('realistic_career_progression', {})
        
        # Professional recognition
        professional_recognition = profile.get('professional_recognition', {})
        professional_bodies = professional_recognition.get('professional_bodies', [])
        certification_pathways = professional_recognition.get('certification_pathways', [])
        cpd_requirements = professional_recognition.get('cpd_requirements', {})
        
        print(f"🔍 Enhanced HTML generation for {role_name}")
        print(f"   Enhanced competencies: {len(competencies_to_show)}")
        print(f"   Modular structure: {'Available' if modular_structure else 'Missing'}")
        print(f"   Career progression: {'Available' if realistic_career_progression else 'Missing'}")
        print(f"   Typical employers: {len(typical_employers)}")

        # Build HTML using string concatenation (no f-strings) - ENHANCED SECTIONS
        html_parts = []
        
        # Header (unchanged)
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<title>Educational Profile: ' + role_name + '</title>')
        html_parts.append(self._get_enhanced_css())  # Updated CSS call
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        
        # Header section (unchanged)
        html_parts.append('<header class="header">')
        html_parts.append('<h1>📋 Educational Profile: ' + role_name + '</h1>')
        html_parts.append('<div class="metadata">')
        html_parts.append('<span class="badge">Role: ' + role_id + '</span>')
        html_parts.append('<span class="badge">EQF Level ' + str(eqf_level) + '</span>')
        html_parts.append('<span class="badge">' + str(target_ects) + ' ECTS</span>')
        html_parts.append('<span class="badge">T3.2 Compliant</span>')
        html_parts.append('</div>')
        html_parts.append('</header>')
        
        html_parts.append('<main>')
        
        # Profile Overview (unchanged)
        html_parts.append('<section class="section">')
        html_parts.append('<div class="section-header">📋 Profile Overview</div>')
        html_parts.append('<div class="section-content">')
        html_parts.append('<div class="profile-info">')
        html_parts.append('<div class="info-card">')
        html_parts.append('<h3>Role Information</h3>')
        html_parts.append('<p><strong>Role:</strong> ' + role_name + ' (' + role_id + ')</p>')
        html_parts.append('<p><strong>EQF Level:</strong> ' + str(eqf_level) + '</p>')
        html_parts.append('<p><strong>Profile Type:</strong> ' + profile_type.title() + '</p>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</section>')

        # NEW: Modular Structure Section (Schema Required)
        if modular_structure:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🧩 Modular Structure</div>')
            html_parts.append('<div class="section-content">')
            
            # ECTS and Duration Overview
            total_ects = modular_structure.get('total_ects', 0)
            total_ects_by_level = modular_structure.get('total_ects_by_level', {})
            semesters = modular_structure.get('semesters', 0)
            
            html_parts.append('<div class="modular-overview">')
            
            if total_ects:
                html_parts.append('<div class="overview-card">')
                html_parts.append('<h4>📚 Total ECTS</h4>')
                html_parts.append('<p class="big-number">' + str(total_ects) + '</p>')
                html_parts.append('</div>')
            
            if total_ects_by_level:
                html_parts.append('<div class="overview-card">')
                html_parts.append('<h4>📊 ECTS by EQF Level</h4>')
                for level, ects in total_ects_by_level.items():
                    html_parts.append('<p>EQF ' + str(level) + ': ' + str(ects) + ' ECTS</p>')
                html_parts.append('</div>')
            
            if semesters:
                html_parts.append('<div class="overview-card">')
                html_parts.append('<h4>📅 Duration</h4>')
                html_parts.append('<p class="big-number">' + str(semesters) + ' Semesters</p>')
                html_parts.append('</div>')
            
            html_parts.append('</div>')
            
            # Modules Breakdown
            modules = modular_structure.get('modules', [])
            if modules:
                html_parts.append('<div class="modules-section">')
                html_parts.append('<h3>📖 Course Modules</h3>')
                html_parts.append('<div class="modules-grid">')
                
                for module in modules:
                    module_code = module.get('code', 'N/A')
                    module_name = module.get('name', 'Unknown Module')
                    module_ects = module.get('ects', 5)
                    module_semester = module.get('semester', 1)
                    module_frameworks = module.get('frameworks', [])
                    
                    html_parts.append('<div class="module-card">')
                    html_parts.append('<div class="module-header">')
                    html_parts.append('<h4>' + module_code + '</h4>')
                    html_parts.append('<span class="semester-badge">Semester ' + str(module_semester) + '</span>')
                    html_parts.append('</div>')
                    html_parts.append('<h5>' + module_name + '</h5>')
                    html_parts.append('<p class="ects-info">' + str(module_ects) + ' ECTS</p>')
                    
                    if module_frameworks:
                        html_parts.append('<div class="frameworks-tags">')
                        for framework in module_frameworks:
                            html_parts.append('<span class="framework-tag">' + framework + '</span>')
                        html_parts.append('</div>')
                    
                    html_parts.append('</div>')
                
                html_parts.append('</div>')
                html_parts.append('</div>')
            
            html_parts.append('</div>')
            html_parts.append('</section>')

        # NEW: Realistic Career Progression Section (Schema Required)
        if realistic_career_progression:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🚀 Career Progression</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="career-timeline">')
            
            # Process each career stage
            career_stages = [
                ('immediate', 'Immediate Opportunities', '🎯'),
                ('short_term', 'Short Term Goals', '📈'),
                ('long_term', 'Long Term Vision', '🌟')
            ]
            
            for stage_key, stage_title, stage_icon in career_stages:
                stage_data = realistic_career_progression.get(stage_key, {})
                if stage_data:
                    timeframe = stage_data.get('timeframe', 'N/A')
                    salary_range = stage_data.get('salary_range', 'N/A')
                    roles = stage_data.get('roles', [])
                    
                    html_parts.append('<div class="career-stage">')
                    html_parts.append('<div class="stage-header">')
                    html_parts.append('<h3>' + stage_icon + ' ' + stage_title + '</h3>')
                    html_parts.append('<div class="stage-meta">')
                    html_parts.append('<span class="timeframe">' + timeframe + '</span>')
                    html_parts.append('<span class="salary">' + salary_range + '</span>')
                    html_parts.append('</div>')
                    html_parts.append('</div>')
                    
                    if roles:
                        html_parts.append('<div class="roles-list">')
                        html_parts.append('<h4>Typical Roles:</h4>')
                        html_parts.append('<ul>')
                        for role in roles:
                            html_parts.append('<li>' + role + '</li>')
                        html_parts.append('</ul>')
                        html_parts.append('</div>')
                    
                    html_parts.append('</div>')
            
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Enhanced Competencies Section (Updated to handle schema format)
        if competencies_to_show:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🌱 Enhanced Competencies</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="competencies-grid">')
            
            for comp in competencies_to_show:
                comp_name = comp.get('competency_name', 'Unknown Competency')
                comp_level = comp.get('competency_level', 'Proficient').lower()
                eqf_alignment = comp.get('eqf_alignment', '')
                is_transversal = comp.get('transversal', False)
                learning_outcomes = comp.get('learning_outcomes', [])
                framework_mappings = comp.get('framework_mappings', {})
                
                html_parts.append('<div class="competency-item enhanced">')
                html_parts.append('<div class="competency-header">')
                html_parts.append('<strong>' + comp_name + '</strong>')
                html_parts.append('<div class="competency-badges">')
                html_parts.append('<span class="level level-' + comp_level + '">' + comp_level.title() + '</span>')
                if is_transversal:
                    html_parts.append('<span class="badge-transversal">Transversal</span>')
                if eqf_alignment:
                    html_parts.append('<span class="badge-eqf">' + eqf_alignment + '</span>')
                html_parts.append('</div>')
                html_parts.append('</div>')
                
                # Learning outcomes
                if learning_outcomes:
                    html_parts.append('<div class="learning-outcomes">')
                    html_parts.append('<h5>Learning Outcomes:</h5>')
                    html_parts.append('<ul class="competency-outcomes">')
                    for outcome in learning_outcomes:
                        html_parts.append('<li>' + outcome + '</li>')
                    html_parts.append('</ul>')
                    html_parts.append('</div>')
                
                # Framework mappings
                if framework_mappings:
                    html_parts.append('<div class="framework-mappings">')
                    html_parts.append('<h5>Framework Alignments:</h5>')
                    for framework, items in framework_mappings.items():
                        if items:
                            framework_display = framework.replace('_', '-').upper()
                            html_parts.append('<div class="framework-group">')
                            html_parts.append('<strong>' + framework_display + ':</strong>')
                            html_parts.append('<span class="framework-items">' + ', '.join(items) + '</span>')
                            html_parts.append('</div>')
                    html_parts.append('</div>')
                
                html_parts.append('</div>')
            
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Programme Learning Outcomes (unchanged but keeping for completeness)
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

        # Entry Requirements (enhanced formatting)
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

        # Assessment Methods (enhanced)
        if assessment_methods:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">📊 Assessment Methods</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="assessment-grid">')
            for method in assessment_methods:
                html_parts.append('<div class="assessment-item">')
                html_parts.append('<span class="assessment-icon">✓</span>')
                html_parts.append('<span class="assessment-text">' + method + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Industry Sectors (enhanced)
        if industry_sectors:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🏭 Industry Sectors</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="sectors-grid">')
            for sector in industry_sectors:
                html_parts.append('<div class="sector-item">')
                html_parts.append('<span class="sector-icon">🏢</span>')
                html_parts.append('<span class="sector-text">' + sector + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # NEW: Typical Employers Section (Schema Required)
        if typical_employers:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🏢 Typical Employers</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="employers-grid">')
            for employer in typical_employers:
                html_parts.append('<div class="employer-item">')
                html_parts.append('<span class="employer-icon">🎯</span>')
                html_parts.append('<span class="employer-text">' + employer + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Career Pathways (if not covered in realistic_career_progression)
        if career_pathways and not realistic_career_progression:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🚀 Career Pathways</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="pathways-grid">')
            for pathway in career_pathways:
                html_parts.append('<div class="pathway-item">')
                html_parts.append('<span class="pathway-icon">📈</span>')
                html_parts.append('<span class="pathway-text">' + pathway + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Professional Bodies (enhanced)
        if professional_bodies:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🤝 Professional Bodies</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="bodies-grid">')
            for body in professional_bodies:
                html_parts.append('<div class="body-item">')
                html_parts.append('<span class="body-icon">🏛️</span>')
                html_parts.append('<span class="body-text">' + body + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Certification Pathways (enhanced)
        if certification_pathways:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">🏆 Certification Pathways</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="certifications-grid">')
            for pathway in certification_pathways:
                html_parts.append('<div class="certification-item">')
                html_parts.append('<span class="cert-icon">🎖️</span>')
                html_parts.append('<span class="cert-text">' + pathway + '</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # CPD Requirements (enhanced)
        if cpd_requirements:
            html_parts.append('<section class="section">')
            html_parts.append('<div class="section-header">📈 Continuing Professional Development</div>')
            html_parts.append('<div class="section-content">')
            html_parts.append('<div class="cpd-grid">')
            
            for cpd_type, cpd_value in cpd_requirements.items():
                if cpd_value:
                    html_parts.append('<div class="cpd-card">')
                    html_parts.append('<h4>' + cpd_type.replace('_', ' ').title() + '</h4>')
                    html_parts.append('<p>' + str(cpd_value) + '</p>')
                    html_parts.append('</div>')
            
            html_parts.append('</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')

        # Footer and closing
        html_parts.append('</main>')
        html_parts.append('<footer class="footer">')
        html_parts.append('<p><strong>Educational Profile</strong> generated by DSCG v3.1</p>')
        html_parts.append('<p>Generated: ' + str(profile.get('creation_date', 'Unknown')) + '</p>')
        html_parts.append('<p><em>Full T3.2 Schema Compliance</em></p>')
        html_parts.append('</footer>')
        html_parts.append('</div>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        # Join all parts
        return '\n'.join(html_parts)

    def _get_enhanced_css(self):
        """Enhanced CSS for full schema compliance - replaces _get_simple_css"""
        return '''<style>
        /* Base Styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* Header */
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        .header h1 { font-size: 2.2rem; margin-bottom: 1rem; font-weight: 600; }
        .metadata { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
        .badge { background: rgba(255,255,255,0.2); padding: 0.6rem 1.2rem; border-radius: 25px; font-weight: 500; backdrop-filter: blur(10px); }
        
        /* Sections */
        .section { background: white; margin-bottom: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden; }
        .section-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.2rem 2rem; font-size: 1.4rem; font-weight: 600; }
        .section-content { padding: 2rem; }
        
        /* Profile Info */
        .profile-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
        .info-card { background: #f8f9fa; padding: 1.8rem; border-radius: 12px; border-left: 5px solid #667eea; }
        .info-card h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.2rem; }
        
        /* Modular Structure */
        .modular-overview { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .overview-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; }
        .overview-card h4 { font-size: 1rem; margin-bottom: 0.5rem; opacity: 0.9; }
        .big-number { font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0; }
        
        .modules-section { margin-top: 2rem; }
        .modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; margin-top: 1rem; }
        .module-card { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 10px; padding: 1.5rem; transition: transform 0.2s ease; }
        .module-card:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .module-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
        .module-header h4 { color: #667eea; font-size: 1.1rem; }
        .semester-badge { background: #10b981; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; }
        .ects-info { color: #666; font-weight: 500; margin: 0.5rem 0; }
        .frameworks-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.8rem; }
        .framework-tag { background: #e0e7ff; color: #5b21b6; padding: 0.2rem 0.6rem; border-radius: 10px; font-size: 0.75rem; }
        
        /* Career Progression */
        .career-timeline { display: flex; flex-direction: column; gap: 2rem; }
        .career-stage { background: #f8f9fa; border-radius: 12px; padding: 1.8rem; border-left: 5px solid #10b981; }
        .stage-header { margin-bottom: 1rem; }
        .stage-header h3 { color: #10b981; font-size: 1.3rem; margin-bottom: 0.5rem; }
        .stage-meta { display: flex; gap: 1rem; flex-wrap: wrap; }
        .timeframe { background: #e0f2fe; color: #0277bd; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500; }
        .salary { background: #e8f5e8; color: #2e7d32; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500; }
        .roles-list h4 { color: #555; margin-bottom: 0.5rem; }
        .roles-list ul { margin-left: 1.2rem; }
        .roles-list li { margin-bottom: 0.3rem; color: #666; }
        
        /* Enhanced Competencies */
        .competencies-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
        .competency-item.enhanced { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.8rem; border-radius: 12px; border-left: 5px solid #10b981; }
        .competency-header { margin-bottom: 1.2rem; }
        .competency-badges { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
        .level { padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
        .level-proficient { background: #10b981; color: white; }
        .level-advanced { background: #3b82f6; color: white; }
        .level-expert { background: #8b5cf6; color: white; }
        .badge-transversal { background: #f59e0b; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem; }
        .badge-eqf { background: #6366f1; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem; }
        
        .learning-outcomes { margin: 1rem 0; }
        .learning-outcomes h5 { color: #374151; margin-bottom: 0.5rem; }
        .competency-outcomes { margin-left: 1.2rem; }
        .competency-outcomes li { margin-bottom: 0.4rem; color: #555; }
        
        .framework-mappings { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb; }
        .framework-mappings h5 { color: #374151; margin-bottom: 0.5rem; }
        .framework-group { margin-bottom: 0.5rem; }
        .framework-items { color: #666; margin-left: 0.5rem; }
        
        /* Grid Components */
        .assessment-grid, .sectors-grid, .employers-grid, .pathways-grid, .bodies-grid, .certifications-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 1rem; 
        }
        
        .assessment-item, .sector-item, .employer-item, .pathway-item, .body-item, .certification-item {
            background: #f8f9fa; 
            padding: 1.2rem; 
            border-radius: 10px; 
            border-left: 4px solid #667eea; 
            display: flex; 
            align-items: center; 
            gap: 0.8rem;
            transition: transform 0.2s ease;
        }
        
        .assessment-item:hover, .sector-item:hover, .employer-item:hover, .pathway-item:hover, .body-item:hover, .certification-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .assessment-icon, .sector-icon, .employer-icon, .pathway-icon, .body-icon, .cert-icon { 
            font-size: 1.2rem; 
            flex-shrink: 0; 
        }
        
        /* Programme Outcomes */
        .programme-outcomes { list-style: none; padding: 0; }
        .programme-outcomes li { background: #f0fdf4; padding: 1.2rem; margin-bottom: 1rem; border-radius: 10px; border-left: 5px solid #10b981; }
        
        /* Requirements Grid */
        .requirements-grid, .cpd-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
        .requirement-card, .cpd-card { background: #fef3c7; padding: 1.8rem; border-radius: 12px; border-left: 5px solid #f59e0b; }
        .requirement-card h4, .cpd-card h4 { color: #d97706; margin-bottom: 0.8rem; font-size: 1.1rem; }
        
        /* Footer */
        .footer { text-align: center; padding: 2rem; color: #666; background: white; border-radius: 15px; margin-top: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        
        /* Responsive */
        @media (max-width: 768px) {
            .profile-info, .competencies-grid, .modular-overview, .modules-grid, .assessment-grid, .sectors-grid, .employers-grid, .pathways-grid, .bodies-grid, .certifications-grid, .requirements-grid, .cpd-grid { 
                grid-template-columns: 1fr; 
            }
            .career-timeline { gap: 1.5rem; }
            .stage-meta { flex-direction: column; gap: 0.5rem; }
        }
        </style>'''

    def _generate_curriculum_html(self, curriculum: Dict[str, Any], topic: str, eqf_level: int) -> str:
        """Generate HTML for curriculum display"""
        role_id = curriculum.get('role_id', 'Unknown')
        role_name = curriculum.get('role_name', 'Unknown Role')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curriculum: {role_name} - {topic}</title>
    {self._get_enhanced_css()}
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📚 Curriculum: {role_name}</h1>
            <div class="metadata">
                <span class="badge">Topic: {topic}</span>
                <span class="badge">EQF Level {eqf_level}</span>
                <span class="badge">T3.2/T3.4 Compliant</span>
            </div>
        </header>
        
        <main>
            <section class="section">
                <div class="section-header">📋 Curriculum Overview</div>
                <div class="section-content">
                    <div class="profile-info">
                        <div class="info-card">
                            <h3>Basic Information</h3>
                            <p><strong>Role:</strong> {role_name} ({role_id})</p>
                            <p><strong>Topic:</strong> {topic}</p>
                            <p><strong>EQF Level:</strong> {eqf_level}</p>
                            <p><strong>Total ECTS:</strong> {curriculum.get('total_ects', 'N/A')}</p>
                        </div>
                    </div>
                </div>
            </section>
        </main>
        
        <footer class="footer">
            <p><strong>Curriculum</strong> generated by DSCG v3.1</p>
            <p>Generated: {datetime.now().isoformat()}</p>
        </footer>
    </div>
</body>
</html>"""
        return html_content

    def _generate_curriculum_summary(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Generate curriculum summary for analysis"""
        return {
            'role_id': curriculum.get('role_id', 'Unknown'),
            'role_name': curriculum.get('role_name', 'Unknown'),
            'total_ects': curriculum.get('total_ects', 0),
            'modules_count': len(curriculum.get('modules', [])),
            'semesters': curriculum.get('semesters', 0),
            'compliance_standards': curriculum.get('compliance_standards', []),
            'generation_timestamp': datetime.now().isoformat(),
            'framework_alignment': curriculum.get('framework_alignment', {}),
            'summary_version': '3.1'
        }
