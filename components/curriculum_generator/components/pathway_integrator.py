#!/usr/bin/env python3
# scripts/curriculum_generator/components/pathway_integrator.py

"""
Learning Pathway Integration Component
Integrates pathway mapping with curriculum generation
"""

from learning_pathway_mapper import LearningPathwayMapper
import json

class PathwayIntegrator:
    """Integrates learning pathway mapping with curriculum generation"""
    
    def __init__(self, modules_data: List[Dict], role_definitions: Dict[str, Any]):
        self.pathway_mapper = LearningPathwayMapper(modules_data, role_definitions)
    
    def enhance_curriculum_with_pathways(self, curriculum: Dict, target_role: str = None) -> Dict:
        """Enhance curriculum with comprehensive pathway information"""
        
        # Generate pathway map for the target role
        pathway_map = self.pathway_mapper.generate_learning_pathway_map(target_role)
        
        # Add pathway section to curriculum
        curriculum["section_12_learning_pathways"] = {
            "title": "Learning Pathway and Progression Framework",
            "description": "Comprehensive mapping of learning progression routes and credential stacking options",
            "pathway_overview": pathway_map["pathway_overview"],
            "progression_routes": pathway_map["progression_routes"],
            "credential_stacking": pathway_map["credential_stacking"],
            "role_transitions": pathway_map["role_transitions"],
            "flexible_pathways": pathway_map["flexible_pathways"],
            "visual_map_data": self.pathway_mapper.generate_visual_pathway_map(pathway_map)
        }
        
        # Enhance module information with pathway context
        if "section_4_course_organization" in curriculum:
            curriculum["section_4_course_organization"]["pathway_context"] = {
                "current_position": "This curriculum forms part of comprehensive learning pathways",
                "progression_options": pathway_map["pathway_overview"]["applicable_pathways"],
                "next_steps": self._generate_next_steps(curriculum, pathway_map),
                "stacking_opportunities": self._identify_stacking_opportunities(curriculum, pathway_map)
            }
        
        return curriculum
    
    def _generate_next_steps(self, curriculum: Dict, pathway_map: Dict) -> List[str]:
        """Generate specific next steps for this curriculum"""
        
        current_eqf = curriculum.get("programme_specification", {}).get("eqf_level", 6)
        current_ects = curriculum.get("programme_specification", {}).get("ects_points", 5)
        
        next_steps = []
        
        # Suggest next EQF level
        if current_eqf < 8:
            next_steps.append(f"Progress to EQF Level {current_eqf + 1} modules for advanced competency")
        
        # Suggest ECTS accumulation
        if current_ects < 30:
            next_steps.append(f"Accumulate additional {30 - current_ects} ECTS for professional qualification")
        
        # Suggest complementary domains
        next_steps.append("Explore complementary domains to broaden sustainability competency")
        
        return next_steps
    
    def _identify_stacking_opportunities(self, curriculum: Dict, pathway_map: Dict) -> List[Dict]:
        """Identify specific credential stacking opportunities"""
        
        opportunities = []
        
        # Check micro-credential stacking
        for stack_id, stack_info in pathway_map.get("credential_stacking", {}).get("micro_credential_stacking", {}).items():
            opportunities.append({
                "type": "micro_credential",
                "name": stack_info["name"],
                "additional_requirements": stack_info.get("modules", []),
                "total_ects": stack_info.get("total_ects", 0),
                "duration": stack_info.get("duration", "Unknown")
            })
        
        return opportunities
