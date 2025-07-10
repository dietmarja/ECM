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
            html_content = self._generate_clean_educational_profile_html(
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

# scripts/curriculum_generator/core/output_manager.py (UPDATED - Part 1: Data Extraction Enhancement)

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
