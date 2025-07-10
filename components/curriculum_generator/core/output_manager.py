#!/usr/bin/env python3
# scripts/curriculum_generator/core/output_manager.py
"""
Enhanced Output Manager - T3.2/T3.4 Compliant with DOCX Support
Fixed compatibility for educational profiles and curricula with multi-format output
Enhanced with COMPACT MODE support for appendix generation
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class OutputManager:
    """Manages output generation for educational profiles and curricula with DOCX support"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.default_output_dir = project_root / 'output'
        
        # Initialize DOCX generator
        try:
            from scripts.curriculum_generator.components.docx_generator import DocxGenerator
            self.docx_generator = DocxGenerator(project_root)
            self.docx_available = True
            print("✅ DOCX generation capability initialized")
        except ImportError as e:
            print(f"⚠️ DOCX generation not available: {e}")
            print("   Install python-docx: pip install python-docx")
            self.docx_generator = None
            self.docx_available = False
        
    def save_educational_profile_standalone(self, 
                                          educational_profile: Dict[str, Any],
                                          topic: str = "Digital Sustainability",
                                          eqf_level: int = 6,
                                          output_docx: bool = False,
                                          theme_name: str = "material_gray",
                                          compact_mode: bool = False) -> List[str]:
        """Save standalone educational profile with JSON, HTML, and optionally DOCX"""
        
        try:
            # Create output directory - use compact_appendix for compact mode
            if compact_mode:
                output_dir = self.default_output_dir / 'compact_appendix'
            else:
                output_dir = self.default_output_dir / 'educational_profiles'
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            metadata = educational_profile.get('metadata', {})
            role_id = metadata.get('role_id', 'UNKNOWN')
            role_name = metadata.get('role_name', 'Unknown Role')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            
            topic_safe = topic.replace(" ", "_").replace("/", "_")
            
            # Add COMPACT prefix for compact mode
            prefix = "COMPACT_EP_" if compact_mode else "EP_"
            filename_base = f"{prefix}{role_id}_EQF{eqf_level}_{topic_safe}_{timestamp}"
            
            generated_files = []
            
            # Save JSON
            json_file = output_dir / f"{filename_base}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(educational_profile, f, indent=2, ensure_ascii=False)
            generated_files.append(str(json_file))
            print(f"✅ Educational Profile JSON saved: {json_file.name}")
            
            # Generate and save HTML
            html_content = self._generate_educational_profile_html(educational_profile)
            html_file = output_dir / f"{filename_base}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_files.append(str(html_file))
            print(f"✅ Educational Profile HTML saved: {html_file.name}")
            
            # Generate and save DOCX if requested and available
            if output_docx and self.docx_available:
                try:
                    docx_file = output_dir / f"{filename_base}.docx"
                    self.docx_generator.generate_educational_profile_docx(
                        educational_profile, docx_file, theme_name, compact_mode
                    )
                    generated_files.append(str(docx_file))
                    print(f"✅ Educational Profile DOCX saved: {docx_file.name}")
                except Exception as e:
                    print(f"⚠️ DOCX generation failed: {e}")
            elif output_docx and not self.docx_available:
                print("⚠️ DOCX generation requested but not available (install python-docx)")
            
            return generated_files
            
        except Exception as e:
            print(f"❌ Error saving educational profile: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def save_curriculum_with_all_formats(self,
                                       curriculum: Dict[str, Any],
                                       curriculum_html: str,
                                       output_dir: str,
                                       topic: str,
                                       eqf_level: int,
                                       role_id: str,
                                       theme_name: str = "material_gray",
                                       output_docx: bool = False,
                                       include_profile: bool = False,
                                       compact_mode: bool = False) -> List[Path]:
        """Save curriculum in all requested formats (HTML, JSON, optionally DOCX)"""
        
        # Use compact_appendix directory for compact mode
        if compact_mode and not output_dir.endswith('compact_appendix'):
            output_path = Path(output_dir).parent / 'compact_appendix'
        else:
            output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename components
        topic_safe = topic.replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        # Get ECTS for filename
        metadata = curriculum.get('metadata', {})
        actual_ects = metadata.get('actual_ects', metadata.get('target_ects', 0))
        
        # Add COMPACT prefix for compact mode
        prefix = "COMPACT_" if compact_mode else "FINAL_V2_"
        base_filename = f"{prefix}{role_id}_EQF{eqf_level}_{actual_ects}ECTS_{timestamp}"
        
        output_files = []
        
        # 1. Save HTML curriculum
        html_file = output_path / f"{base_filename}_curriculum.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(curriculum_html)
        output_files.append(html_file)
        print(f"✅ Curriculum HTML saved: {html_file.name}")
        
        # 2. Save JSON curriculum
        json_file = output_path / f"{base_filename}_curriculum.json"
        clean_curriculum = self._prepare_for_json(curriculum)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(clean_curriculum, f, indent=2, ensure_ascii=False)
        output_files.append(json_file)
        print(f"✅ Curriculum JSON saved: {json_file.name}")
        
        # 3. Save DOCX curriculum if requested and available
        if output_docx and self.docx_available:
            try:
                docx_file = output_path / f"{base_filename}_curriculum.docx"
                self.docx_generator.generate_curriculum_docx(
                    curriculum, docx_file, theme_name, compact_mode
                )
                output_files.append(docx_file)
                print(f"✅ Curriculum DOCX saved: {docx_file.name}")
            except Exception as e:
                print(f"⚠️ Curriculum DOCX generation failed: {e}")
        elif output_docx and not self.docx_available:
            print("⚠️ DOCX generation requested but not available (install python-docx)")
        
        # 4. Save educational profile if requested
        if include_profile:
            educational_profile = curriculum.get('educational_profile', {})
            if educational_profile:
                # JSON profile
                profile_json_file = output_path / f"{base_filename}_profile.json"
                clean_profile = self._prepare_for_json(educational_profile)
                
                with open(profile_json_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_profile, f, indent=2, ensure_ascii=False)
                output_files.append(profile_json_file)
                
                # DOCX profile if requested
                if output_docx and self.docx_available:
                    try:
                        profile_docx_file = output_path / f"{base_filename}_profile.docx"
                        self.docx_generator.generate_educational_profile_docx(
                            educational_profile, profile_docx_file, theme_name, compact_mode
                        )
                        output_files.append(profile_docx_file)
                        print(f"✅ Educational Profile DOCX saved: {profile_docx_file.name}")
                    except Exception as e:
                        print(f"⚠️ Educational Profile DOCX generation failed: {e}")
        
        # Generate DOCX file
        try:
            from scripts.curriculum_generator.components.docx_generator import DocxGenerator
            from datetime import datetime
            
            print("🔧 Generating DOCX file...")
            
            docx_generator = DocxGenerator(self.project_root)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            docx_file = self.output_dir / f"FINAL_V2_{role_id}_EQF{eqf_level}_{ects}ECTS_{timestamp}_curriculum.docx"
            
            # Create curriculum text for DOCX (simplified for now)
            simple_curriculum = f"""Curriculum 
Digital Sustainability Professional Development Course
Specialization: Data Analyst
EQF Level: {eqf_level}
ECTS: {ects} credits
Total Study Hours: {ects * 25} hours
Delivery: Blended (Online + Practical + Work-Based Option)
Modules: 3 Micro-Modules
Credential Format: Stackable Micro-Credentials + Certificate

1. 🎯 Programme Learning Outcomes (Aligned with EQF Level {eqf_level} Descriptors)
Upon successful completion, participants will be able to:

Apply ESG and sustainability reporting standards to organizational datasets.
Transform and validate sustainability datasets using data wrangling techniques.
Create dashboards to communicate sustainability impact to stakeholders."""
            
            docx_generator.generate_compact_curriculum_docx(
                curriculum_text=simple_curriculum,
                role_id=role_id,
                eqf_level=eqf_level,
                ects=ects,
                output_path=docx_file
            )
            
            output_files.append(docx_file)
            print(f"✅ Curriculum DOCX saved: {docx_file.name}")
            
        except Exception as e:
            print(f"❌ DOCX generation failed: {e}")
        print(f"📁 Enhanced output saved: {len(output_files)} files")
        return output_files
    
    def save_compact_profile(self, educational_profile: Dict[str, Any], 
                           topic: str, eqf_level: int, theme_name: str) -> List[str]:
        """Save compact educational profile specifically for appendix use"""
        return self.save_educational_profile_standalone(
            educational_profile=educational_profile,
            topic=topic,
            eqf_level=eqf_level,
            output_docx=True,
            theme_name=theme_name,
            compact_mode=True
        )
    
    def save_compact_curriculum(self, curriculum: Dict[str, Any], 
                              curriculum_html: str, output_dir: str,
                              topic: str, eqf_level: int, role_id: str, 
                              theme_name: str) -> List[Path]:
        """Save compact curriculum specifically for appendix use"""
        return self.save_curriculum_with_all_formats(
            curriculum=curriculum,
            curriculum_html=curriculum_html,
            output_dir=output_dir,
            topic=topic,
            eqf_level=eqf_level,
            role_id=role_id,
            theme_name=theme_name,
            output_docx=True,
            include_profile=False,
            compact_mode=True
        )
    
    def _prepare_for_json(self, data: Any) -> Any:
        """Prepare data structure for JSON serialization"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned[key] = self._prepare_for_json(value)
            return cleaned
        elif isinstance(data, list):
            return [self._prepare_for_json(item) for item in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif hasattr(data, 'isoformat'):  # datetime objects
            return data.isoformat()
        else:
            return str(data)
    
    def _generate_educational_profile_html(self, profile: Dict[str, Any]) -> str:
        """Generate comprehensive HTML for educational profile - FIXED VERSION"""
        
        try:
            metadata = profile.get('metadata', {})
            role_def = profile.get('role_definition', {})
            career_prog = profile.get('realistic_career_progression', {})
            employers = profile.get('typical_employers', {})
            competencies = profile.get('enhanced_competencies', {})
            modular = profile.get('modular_structure', {})
            assessment = profile.get('assessment_methods', {})
            entry_req = profile.get('entry_requirements', {})
            cpd = profile.get('cpd_requirements', {})
            
            # FIXED: Generate career progression HTML safely
            career_html = ""
            if career_prog:
                entry_level = career_prog.get('entry_level', {})
                progression_roles = career_prog.get('progression_roles', [])
                
                salary_range = entry_level.get('salary_range_eur', {})
                min_salary = salary_range.get('min', 30000) if isinstance(salary_range, dict) else 30000
                max_salary = salary_range.get('max', 50000) if isinstance(salary_range, dict) else 50000
                
                career_html = f"""
                <div class="career-entry">
                    <h4>🎯 Entry Level: {entry_level.get('title', 'Professional')}</h4>
                    <p><strong>Salary Range:</strong> €{min_salary:,} - €{max_salary:,}</p>
                    <p><strong>Experience:</strong> {entry_level.get('experience_required', 'Entry level')}</p>
                </div>
                <div class="career-progression">
                    <h4>📈 Career Progression</h4>
                """
                
                for role in progression_roles:
                    if isinstance(role, dict):  # Safety check
                        additional_skills = role.get('additional_skills_needed', [])
                        skills_text = ', '.join(additional_skills) if isinstance(additional_skills, list) else str(additional_skills)
                        
                        career_html += f"""
                        <div class="progression-step">
                            <h5>{role.get('title', 'Senior Role')}</h5>
                            <p><strong>Timeline:</strong> {role.get('years_to_achieve', '3-5')} years</p>
                            <p><strong>Salary Increase:</strong> {role.get('salary_increase_percent', '30-50')}%</p>
                            <p><strong>Skills Needed:</strong> {skills_text}</p>
                        </div>
                        """
                career_html += "</div>"
            
            # FIXED: Generate employers HTML safely
            employers_html = ""
            if employers:
                primary = employers.get('primary_sectors', [])
                secondary = employers.get('secondary_sectors', [])
                emerging = employers.get('emerging_opportunities', [])
                
                # Ensure lists
                primary = primary if isinstance(primary, list) else []
                secondary = secondary if isinstance(secondary, list) else []
                emerging = emerging if isinstance(emerging, list) else []
                
                employers_html = f"""
                <div class="employer-sectors">
                    <div class="sector-group">
                        <h4>🏢 Primary Employers</h4>
                        <ul>{''.join(f'<li>{sector}</li>' for sector in primary)}</ul>
                    </div>
                    <div class="sector-group">
                        <h4>🏭 Secondary Sectors</h4>
                        <ul>{''.join(f'<li>{sector}</li>' for sector in secondary)}</ul>
                    </div>
                    <div class="sector-group">
                        <h4>🚀 Emerging Opportunities</h4>
                        <ul>{''.join(f'<li>{opp}</li>' for opp in emerging)}</ul>
                    </div>
                </div>
                """
            
            # FIXED: Generate competencies HTML safely
            competencies_html = ""
            if competencies:
                learning_outcomes = competencies.get('learning_outcomes', [])
                framework_mappings = competencies.get('framework_mappings', {})
                core_competencies = competencies.get('core_competencies', [])
                
                # Ensure learning_outcomes is a list
                if isinstance(learning_outcomes, list):
                    outcomes_list = ''.join(f'<li>{outcome}</li>' for outcome in learning_outcomes)
                else:
                    outcomes_list = '<li>Learning outcomes will be defined</li>'
                
                # FIXED: Framework mappings safety
                frameworks_html = ""
                if isinstance(framework_mappings, dict):
                    for framework, codes in framework_mappings.items():
                        framework_name = str(framework).upper().replace('_', '-')
                        if isinstance(codes, list):
                            codes_text = ', '.join(str(code) for code in codes[:4])  # Show first 4 codes
                        else:
                            codes_text = str(codes)
                        frameworks_html += f'<span class="framework-badge">{framework_name}: {codes_text}</span>'
                
                # FIXED: Core competencies safety
                competencies_list = ""
                if isinstance(core_competencies, list):
                    for comp in core_competencies:
                        if isinstance(comp, dict):
                            competencies_list += f"""
                            <div class="competency-item">
                                <h5>{comp.get('name', 'Core Competency')}</h5>
                                <p>{comp.get('description', 'Professional competency')}</p>
                                <span class="proficiency-badge">{comp.get('proficiency_level', 'Professional')}</span>
                            </div>
                            """
                        else:
                            # Handle string competencies
                            competencies_list += f"""
                            <div class="competency-item">
                                <h5>{str(comp)}</h5>
                                <p>Core professional competency</p>
                                <span class="proficiency-badge">Professional</span>
                            </div>
                            """
                
                competencies_html = f"""
                <div class="learning-outcomes">
                    <h4>🎯 Target LLLearning Outcomes</h4>
                    <ul>{outcomes_list}</ul>
                </div>
                <div class="framework-mappings">
                    <h4>🗺️ Framework Alignment</h4>
                    <div class="frameworks-container">{frameworks_html}</div>
                </div>
                <div class="core-competencies">
                    <h4>💪 Core Competencies</h4>
                    {competencies_list}
                </div>
                """
            
            # FIXED: Generate modular structure HTML safely
            modular_html = ""
            if modular:
                total_ects = modular.get('total_ects', 60)
                duration = modular.get('duration_semesters', 2)
                modules = modular.get('modules', [])
                semesters = modular.get('semesters', [])
                
                modules_list = ""
                if isinstance(modules, list):
                    for module in modules:
                        if isinstance(module, dict):
                            modules_list += f"""
                            <div class="module-item">
                                <h5>{module.get('name', 'Module')} ({module.get('ects', 7.5)} ECTS)</h5>
                                <p><strong>Semester:</strong> {module.get('semester', 1)} | <strong>Delivery:</strong> {module.get('delivery_mode', 'Blended')}</p>
                                <p><strong>Relevance:</strong> {module.get('relevance_score', 80)}%</p>
                            </div>
                            """
                
                semesters_list = ""
                if isinstance(semesters, list):
                    for sem in semesters:
                        if isinstance(sem, dict):
                            semesters_list += f"""
                            <div class="semester-item">
                                <h5>Semester {sem.get('semester_number', 1)}</h5>
                                <p>{sem.get('ects', 30)} ECTS | {sem.get('modules_count', 4)} modules</p>
                            </div>
                            """
                
                modular_html = f"""
                <div class="program-overview">
                    <h4>📚 Program Structure</h4>
                    <p><strong>Total:</strong> {total_ects} ECTS | <strong>Duration:</strong> {duration} semester(s)</p>
                </div>
                <div class="semester-breakdown">
                    <h4>📅 Semester Breakdown</h4>
                    {semesters_list}
                </div>
                <div class="modules-list">
                    <h4>📖 Modules</h4>
                    {modules_list}
                </div>
                """
            
            # FIXED: Generate assessment HTML safely
            assessment_html = ""
            if assessment:
                primary_methods = assessment.get('primary_methods', [])
                practical_comp = assessment.get('practical_components', {})
                
                if isinstance(primary_methods, list):
                    methods_list = ''.join(f'<li>{method}</li>' for method in primary_methods)
                else:
                    methods_list = '<li>Assessment methods will be defined</li>'
                
                practical_percent = practical_comp.get('percentage', 50) if isinstance(practical_comp, dict) else 50
                
                assessment_html = f"""
                <div class="assessment-methods">
                    <h4>📝 How You'll Be Assessed</h4>
                    <ul>{methods_list}</ul>
                    <p><strong>Practical Components:</strong> {practical_percent}% of assessment</p>
                    <p><strong>Final Assessment:</strong> {assessment.get('final_assessment', 'Capstone project')}</p>
                </div>
                """
            
            # FIXED: Generate entry requirements HTML safely
            entry_html = ""
            if entry_req:
                entry_html = f"""
                <div class="entry-requirements">
                    <h4>🎓 Entry Requirements</h4>
                    <p><strong>Education:</strong> {entry_req.get('formal_education', 'Secondary education')}</p>
                    <p><strong>Experience:</strong> {entry_req.get('professional_experience', 'No experience required')}</p>
                    <p><strong>Digital Skills:</strong> {entry_req.get('digital_competencies', 'Basic digital literacy')}</p>
                    <p><strong>Language:</strong> {entry_req.get('language_requirements', 'English proficiency')}</p>
                </div>
                """
            
            # FIXED: Generate CPD HTML safely
            cpd_html = ""
            if cpd:
                cert_maint = cpd.get('certification_maintenance', {})
                micro_learning = cpd.get('micro_learning_opportunities', {})
                
                renewal_years = cert_maint.get('renewal_period_years', 3) if isinstance(cert_maint, dict) else 3
                cpd_hours = cert_maint.get('cpd_hours_required', 40) if isinstance(cert_maint, dict) else 40
                max_recognition = micro_learning.get('maximum_recognition', 10) if isinstance(micro_learning, dict) else 10
                
                cpd_html = f"""
                <div class="cpd-requirements">
                    <h4>🔄 Continuing Professional Development</h4>
                    <p><strong>Renewal Period:</strong> {renewal_years} years</p>
                    <p><strong>CPD Hours Required:</strong> {cpd_hours} hours</p>
                    <p><strong>Stackable Credits:</strong> Up to {max_recognition} ECTS per renewal</p>
                </div>
                """
            
            # Generate the final HTML
            role_name = role_def.get('name', 'Professional')
            role_id = role_def.get('id', 'ROLE')
            role_area = role_def.get('main_area', 'Digital Sustainability')
            eqf_level = metadata.get('eqf_level', 6)
            generation_date = metadata.get('generation_date', datetime.now().isoformat())
            
            return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Profile: {role_name} - EQF Level {eqf_level}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary-color: #2E7D32;
            --secondary-color: #1976D2;
            --accent-color: #FF6F00;
            --background-color: #FAFAFA;
            --surface-color: #FFFFFF;
            --text-color: #212121;
            --border-color: #E0E0E0;
        }}
        
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: var(--text-color); background: var(--background-color); padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        .header {{ background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; padding: 3rem 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .header h2 {{ font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9; }}
        .metadata {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; }}
        .badge {{ background: rgba(255,255,255,0.25); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; }}
        
        .section {{ background: var(--surface-color); margin: 2rem 0; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden; }}
        .section-header {{ background: linear-gradient(135deg, var(--secondary-color) 0%, #1565C0 100%); color: white; padding: 1.5rem 2rem; font-size: 1.3rem; font-weight: 600; }}
        .section-content {{ padding: 2rem; }}
        
        .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        .three-column {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
        
        .career-entry {{ background: #E8F5E8; padding: 1.5rem; border-radius: 10px; border-left: 5px solid var(--primary-color); margin-bottom: 1.5rem; }}
        .career-progression {{ background: #FFF3E0; padding: 1.5rem; border-radius: 10px; border-left: 5px solid var(--accent-color); }}
        .progression-step {{ background: rgba(255,255,255,0.8); padding: 1rem; margin: 1rem 0; border-radius: 8px; border-left: 3px solid var(--accent-color); }}
        
        .employer-sectors {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }}
        .sector-group {{ background: #F3E5F5; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #9C27B0; }}
        .sector-group h4 {{ color: #7B1FA2; margin-bottom: 1rem; }}
        .sector-group ul {{ list-style-type: none; }}
        .sector-group li {{ padding: 0.3rem 0; }}
        .sector-group li:before {{ content: "• "; color: #9C27B0; font-weight: bold; }}
        
        .learning-outcomes {{ background: #E3F2FD; padding: 1.5rem; border-radius: 10px; border-left: 5px solid var(--secondary-color); margin-bottom: 1.5rem; }}
        .learning-outcomes ul {{ padding-left: 1.5rem; }}
        .learning-outcomes li {{ margin: 0.5rem 0; }}
        
        .framework-mappings {{ background: #F1F8E9; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #689F38; margin-bottom: 1.5rem; }}
        .frameworks-container {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem; }}
        .framework-badge {{ background: #C8E6C9; color: #2E7D32; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; }}
        
        .core-competencies {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }}
        .competency-item {{ background: #FFF8E1; padding: 1rem; border-radius: 8px; border-left: 3px solid #FFA000; }}
        .proficiency-badge {{ background: #FF8F00; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; }}
        
        .program-overview {{ background: #E8EAF6; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #3F51B5; margin-bottom: 1.5rem; }}
        .semester-breakdown {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
        .semester-item {{ background: #F3E5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #9C27B0; }}
        .modules-list {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }}
        .module-item {{ background: #EFEBE9; padding: 1rem; border-radius: 8px; border-left: 3px solid #8D6E63; }}
        
        .assessment-methods {{ background: #FFF3E0; padding: 1.5rem; border-radius: 10px; border-left: 5px solid var(--accent-color); }}
        .assessment-methods ul {{ padding-left: 1.5rem; }}
        .assessment-methods li {{ margin: 0.5rem 0; }}
        
        .entry-requirements {{ background: #E0F2F1; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #00695C; }}
        .cpd-requirements {{ background: #FCE4EC; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #C2185B; }}
        
        .footer {{ text-align: center; padding: 2rem; color: #666; background: rgba(255,255,255,0.8); border-radius: 10px; margin-top: 3rem; }}
        
        @media (max-width: 768px) {{ 
            .two-column, .three-column {{ grid-template-columns: 1fr; }}
            .metadata {{ flex-direction: column; align-items: center; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎓 Educational Profile</h1>
            <h2>{role_name} - EQF Level {eqf_level}</h2>
            <div class="metadata">
                <span class="badge">Role: {role_id}</span>
                <span class="badge">Area: {role_area}</span>
            </div>
        </header>
        
        <main>
            <section class="section">
                <div class="section-header">💼 Career Progression & Opportunities</div>
                <div class="section-content">
                    {career_html}
                </div>
            </section>
            
            <section class="section">
                <div class="section-header">🏢 Typical Employers</div>
                <div class="section-content">
                    {employers_html}
                </div>
            </section>
            
            <section class="section">
                <div class="section-header">🎯 Competences</div>
                <div class="section-content">
                    {competencies_html}
                </div>
            </section>
            
            <section class="section">
                <div class="section-header">📚 Program Structure</div>
                <div class="section-content">
                    {modular_html}
                </div>
            </section>
            
            <div class="two-column">
                <section class="section">
                    <div class="section-header">📝 Assessment</div>
                    <div class="section-content">
                        {assessment_html}
                    </div>
                </section>
                
                <section class="section">
                    <div class="section-header">🎓 Entry Requirements</div>
                    <div class="section-content">
                        {entry_html}
                    </div>
                </section>
            </div>
            
            <section class="section">
                <div class="section-header">🔄 Professional Development</div>
                <div class="section-content">
                    {cpd_html}
                </div>
            </section>
        </main>
        
        <footer class="footer">
            <p><strong>Educational Profile</strong></p>
            <p>Generated: {generation_date}</p>
        </footer>
    </div>
</body>
</html>
            """
            
        except Exception as e:
            print(f"❌ Error generating HTML: {e}")
            import traceback
            traceback.print_exc()
            return f"<html><body><h1>Error generating profile</h1><p>{str(e)}</p></body></html>"
