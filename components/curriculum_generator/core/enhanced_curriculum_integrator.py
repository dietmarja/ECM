# scripts/curriculum_generator/core/enhanced_curriculum_integrator.py
"""
Enhanced Curriculum Integrator - Integrates enhanced module selector with existing curriculum generator
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.curriculum_generator.components.enhanced_module_selector import EnhancedModuleSelector

class EnhancedCurriculumIntegrator:
    """
    Integrates enhanced module selection with existing curriculum generation workflow
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.module_selector = EnhancedModuleSelector()
    
    def enhance_unit_with_smart_modules(self, unit: Dict[str, Any], role_id: str, 
                                      topic: str, eqf_level: int) -> Dict[str, Any]:
        """
        Enhance a learning unit with intelligently selected modules
        """
        # Get modules for this specific unit context
        target_modules = 3  # 3 modules per unit is reasonable
        selected_modules = self.module_selector.select_modules_for_curriculum(
            role_id=role_id,
            topic=topic,
            eqf_level=eqf_level,
            target_modules=target_modules,
            min_score_threshold=0.4
        )
        
        # Remove duplicates based on module ID
        unique_modules = []
        seen_ids = set()
        for module in selected_modules:
            module_id = module.get('id')
            if module_id and module_id not in seen_ids:
                unique_modules.append(module)
                seen_ids.add(module_id)
        
        # Enhance unit with selected modules
        enhanced_unit = unit.copy()
        enhanced_unit['selected_modules'] = unique_modules[:3]  # Limit to top 3
        enhanced_unit['module_count'] = len(unique_modules[:3])
        
        # Add content categorization
        all_categories = set()
        for module in unique_modules[:3]:
            categories = self.module_selector.classify_module_content(module)
            all_categories.update(categories)
        
        enhanced_unit['content_categories'] = list(all_categories)
        enhanced_unit['enhanced_selection'] = True
        
        return enhanced_unit
    
    def generate_enhanced_curriculum_summary(self, units: List[Dict[str, Any]], 
                                           role_id: str, topic: str) -> Dict[str, Any]:
        """
        Generate enhanced curriculum summary with D2.1 compliance analysis
        """
        all_modules = []
        for unit in units:
            if 'selected_modules' in unit:
                all_modules.extend(unit['selected_modules'])
        
        # Remove duplicates from all modules
        unique_modules = []
        seen_ids = set()
        for module in all_modules:
            module_id = module.get('id')
            if module_id and module_id not in seen_ids:
                unique_modules.append(module)
                seen_ids.add(module_id)
        
        # Analyze coverage
        coverage = self.module_selector.analyze_curriculum_coverage(unique_modules, role_id, topic)
        
        return {
            'total_unique_modules': len(unique_modules),
            'modules_used': [f"{m['id']}: {m['name']}" for m in unique_modules],
            'coverage_analysis': coverage,
            'enhancement_applied': True
        }

def integrate_enhanced_modules_into_curriculum(curriculum: Dict[str, Any], 
                                             role_id: str, topic: str, eqf_level: int,
                                             project_root: Path) -> Dict[str, Any]:
    """
    Main integration function to enhance existing curriculum with smart module selection
    """
    integrator = EnhancedCurriculumIntegrator(project_root)
    
    # Enhance learning units
    enhanced_units = []
    for unit in curriculum.get('learning_units', []):
        enhanced_unit = integrator.enhance_unit_with_smart_modules(unit, role_id, topic, eqf_level)
        enhanced_units.append(enhanced_unit)
    
    # Generate summary
    enhancement_summary = integrator.generate_enhanced_curriculum_summary(enhanced_units, role_id, topic)
    
    # Update curriculum
    enhanced_curriculum = curriculum.copy()
    enhanced_curriculum['learning_units'] = enhanced_units
    enhanced_curriculum['enhancement_summary'] = enhancement_summary
    enhanced_curriculum['enhanced_module_selection'] = True
    
    print(f"🔧 Enhanced curriculum with smart module selection:")
    print(f"   📦 {enhancement_summary['total_unique_modules']} unique modules selected")
    print(f"   🎯 Role alignment: {enhancement_summary['coverage_analysis']['role_alignment']:.1f}%")
    print(f"   📋 Content coverage: {list(enhancement_summary['coverage_analysis']['content_coverage'].keys())}")
    
    return enhanced_curriculum
