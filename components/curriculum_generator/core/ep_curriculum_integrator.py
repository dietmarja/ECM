#!/usr/bin/env python3
# scripts/curriculum_generator/core/ep_curriculum_integrator.py
"""
Educational Profile - Curriculum Integration Manager
Links EPs with curriculum generation for T3.2/T3.4 compliance
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class EPCurriculumIntegrator:
    """Manages integration between Educational Profiles and Curriculum Generation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.ep_output_dir = project_root / 'output' / 'educational_profiles'
        self.ep_output_dir.mkdir(parents=True, exist_ok=True)
        
    def find_existing_ep(self, role_id: str, eqf_level: int) -> Optional[Dict[str, Any]]:
        """Find existing Educational Profile for role/EQF combination"""
        
        # Look for EP files matching role and EQF level
        pattern = f"EP_{role_id}_EQF{eqf_level}_*.json"
        ep_files = list(self.ep_output_dir.glob(pattern))
        
        if not ep_files:
            return None
        
        # Use the most recent file
        latest_file = max(ep_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                ep_data = json.load(f)
            
            print(f"✅ Found existing EP: {latest_file.name}")
            return ep_data
            
        except Exception as e:
            print(f"❌ Error loading EP {latest_file}: {e}")
            return None
    
    def create_ep_on_demand(self, role_id: str, eqf_level: int, topic: str = "Digital Sustainability") -> Optional[Dict[str, Any]]:
        """Create Educational Profile on-demand during curriculum generation"""
        
        try:
            from scripts.curriculum_generator.domain.educational_profiles import EnhancedEducationalProfilesManager
            from scripts.curriculum_generator.core.output_manager import OutputManager
            
            print(f"🔧 Creating EP on-demand for {role_id} (EQF {eqf_level})")
            
            # Generate EP
            ep_manager = EnhancedEducationalProfilesManager(self.project_root)
            ep_data = ep_manager.generate_comprehensive_profile(role_id, eqf_level)
            
            # Save EP for future use
            output_manager = OutputManager(self.project_root)
            files = output_manager.save_educational_profile_standalone(ep_data, topic, eqf_level)
            
            if files:
                print(f"✅ Created and saved EP: {len(files)} files")
                return ep_data
            else:
                print(f"❌ Failed to save EP")
                return ep_data  # Return data even if save failed
                
        except Exception as e:
            print(f"❌ Error creating EP on-demand: {e}")
            return None
    
    def get_or_create_ep(self, role_id: str, eqf_level: int, topic: str = "Digital Sustainability") -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Get existing EP or create on-demand
        Returns: (ep_data, source) where source is 'existing', 'created', or 'failed'
        """
        
        # First, try to find existing EP
        ep_data = self.find_existing_ep(role_id, eqf_level)
        if ep_data:
            return ep_data, 'existing'
        
        # If not found, create on-demand
        print(f"🔍 No existing EP found for {role_id} EQF{eqf_level}, creating on-demand...")
        ep_data = self.create_ep_on_demand(role_id, eqf_level, topic)
        
        if ep_data:
            return ep_data, 'created'
        else:
            return None, 'failed'
    
    def extract_curriculum_guidance_from_ep(self, ep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract curriculum guidance from Educational Profile"""
        
        if not ep_data:
            return {}
        
        # Extract key information for curriculum generation
        guidance = {
            'role_definition': ep_data.get('role_definition', {}),
            'enhanced_competencies': ep_data.get('enhanced_competencies', {}),
            'modular_structure': ep_data.get('modular_structure', {}),
            'assessment_methods': ep_data.get('assessment_methods', {}),
            'entry_requirements': ep_data.get('entry_requirements', {}),
            'typical_employers': ep_data.get('typical_employers', {}),
            'realistic_career_progression': ep_data.get('realistic_career_progression', {}),
            'cpd_requirements': ep_data.get('cpd_requirements', {})
        }
        
        # Extract specific curriculum parameters
        modular_structure = ep_data.get('modular_structure', {})
        
        guidance['curriculum_parameters'] = {
            'suggested_total_ects': modular_structure.get('total_ects', 60),
            'suggested_duration_semesters': modular_structure.get('duration_semesters', 2),
            'preferred_module_count': len(modular_structure.get('modules', [])),
            'delivery_flexibility': modular_structure.get('flexibility', {}),
            'assessment_approach': ep_data.get('assessment_methods', {}).get('primary_methods', [])
        }
        
        # Extract learning outcomes for curriculum alignment
        competencies = ep_data.get('enhanced_competencies', {})
        guidance['target_learning_outcomes'] = competencies.get('learning_outcomes', [])
        guidance['framework_mappings'] = competencies.get('framework_mappings', {})
        guidance['core_competencies'] = competencies.get('core_competencies', [])
        
        return guidance
    
    def list_available_eps(self) -> List[Dict[str, Any]]:
        """List all available Educational Profiles"""
        
        ep_files = list(self.ep_output_dir.glob("EP_*.json"))
        eps = []
        
        for ep_file in ep_files:
            try:
                # Parse filename to extract info
                filename = ep_file.stem
                parts = filename.split('_')
                
                if len(parts) >= 4:  # EP_ROLE_EQFLEVEL_TOPIC_TIMESTAMP
                    role_id = parts[1]
                    eqf_part = parts[2]  # e.g., "EQF6"
                    eqf_level = int(eqf_part.replace('EQF', ''))
                    
                    # Get file info
                    stat = ep_file.stat()
                    
                    eps.append({
                        'role_id': role_id,
                        'eqf_level': eqf_level,
                        'filename': ep_file.name,
                        'file_path': str(ep_file),
                        'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'file_size': stat.st_size
                    })
                    
            except Exception as e:
                print(f"❌ Error parsing EP file {ep_file}: {e}")
                continue
        
        # Sort by role_id, then eqf_level
        eps.sort(key=lambda x: (x['role_id'], x['eqf_level']))
        return eps
    
    def get_ep_summary(self, role_id: str, eqf_level: int) -> Optional[Dict[str, Any]]:
        """Get summary information about an EP without loading full data"""
        
        ep_data = self.find_existing_ep(role_id, eqf_level)
        if not ep_data:
            return None
        
        metadata = ep_data.get('metadata', {})
        role_def = ep_data.get('role_definition', {})
        competencies = ep_data.get('enhanced_competencies', {})
        modular = ep_data.get('modular_structure', {})
        
        return {
            'role_id': role_id,
            'role_name': role_def.get('name', 'Unknown'),
            'eqf_level': eqf_level,
            'generation_date': metadata.get('generation_date'),
            'total_ects': modular.get('total_ects', 0),
            'duration_semesters': modular.get('duration_semesters', 0),
            'learning_outcomes_count': len(competencies.get('learning_outcomes', [])),
            'core_competencies_count': len(competencies.get('core_competencies', [])),
            'framework_mappings': list(competencies.get('framework_mappings', {}).keys()),
            'exists': True
        }
    
    def validate_ep_for_curriculum(self, ep_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate that EP has necessary data for curriculum generation"""
        
        if not ep_data:
            return False, ["EP data is None or empty"]
        
        issues = []
        
        # Check essential sections
        required_sections = [
            'role_definition',
            'enhanced_competencies', 
            'modular_structure'
        ]
        
        for section in required_sections:
            if section not in ep_data:
                issues.append(f"Missing required section: {section}")
        
        # Check competencies
        competencies = ep_data.get('enhanced_competencies', {})
        if not competencies.get('learning_outcomes'):
            issues.append("No learning outcomes defined")
        
        if not competencies.get('core_competencies'):
            issues.append("No core competencies defined")
        
        # Check modular structure
        modular = ep_data.get('modular_structure', {})
        if not modular.get('total_ects'):
            issues.append("No total ECTS defined")
        
        is_valid = len(issues) == 0
        return is_valid, issues

# Convenience function for easy integration
def get_ep_for_curriculum(role_id: str, eqf_level: int, topic: str = "Digital Sustainability", project_root: Optional[Path] = None) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """
    Convenience function to get EP data and curriculum guidance
    Returns: (ep_data, curriculum_guidance)
    """
    if not project_root:
        project_root = Path(__file__).parent.parent.parent
    
    integrator = EPCurriculumIntegrator(project_root)
    ep_data, source = integrator.get_or_create_ep(role_id, eqf_level, topic)
    
    if ep_data:
        guidance = integrator.extract_curriculum_guidance_from_ep(ep_data)
        guidance['ep_source'] = source  # Track where EP came from
        
        # Validate EP
        is_valid, issues = integrator.validate_ep_for_curriculum(ep_data)
        guidance['ep_validation'] = {
            'is_valid': is_valid,
            'issues': issues
        }
        
        return ep_data, guidance
    else:
        return None, {'ep_source': 'failed', 'ep_validation': {'is_valid': False, 'issues': ['Failed to load or create EP']}}
