# scripts/curriculum_generator/components/uol_learning_manager.py
"""
UOL (Units of Learning) Manager - GENERAL SOLUTION - FIXED
Distributes any ECTS amount into specified number of learning units for industry translation
Works with ANY role - creates competency-focused, stackable learning units
"""

import math
from typing import Dict, List, Any, Optional

class UOLLearningManager:
    """Manages UOL (Units of Learning) distribution for any role/ECTS combination"""
    
    def __init__(self):
        # MERGED: All required attributes in single __init__
        self.competency_progression_types = [
            "Foundation", "Development", "Application", "Integration", "Mastery", "Leadership"
        ]
        
        self.industry_action_verbs = [
            "Create", "Develop", "Implement", "Analyze", "Design", "Manage", 
            "Build", "Optimize", "Execute", "Evaluate", "Lead", "Coordinate"
        ]
        
        # Additional attributes from second init
        self.progression_levels = ['Foundation', 'Development', 'Application', 'Integration']
        self.delivery_approaches = ['Blended', 'Online', 'Practical', 'Workshop']
        self.assessment_methods = ['Competency demonstration', 'Portfolio', 'Project', 'Practical assessment']
        
        # Try to import the unit descriptor (may not exist yet)
        try:
            from scripts.curriculum_generator.components.learning_unit_descriptor import LearningUnitDescriptor
            self.unit_descriptor = LearningUnitDescriptor()
        except ImportError:
            self.unit_descriptor = None
            print("⚠️  LearningUnitDescriptor not available - using basic descriptions")
        
        print(f"✅ UOL Learning Manager initialized (GENERAL SOLUTION)")

    def distribute_ects_across_uol(self, total_ects: float, uol: int, role_id: str, topic: str) -> List[Dict[str, Any]]:
        """Distribute ECTS across specified Units of Learning (UOL)"""
        
        print(f"\n📊 Distributing ECTS across learning units:")
        print(f"   Total ECTS: {total_ects}")
        print(f"   Units of Learning: {uol}")
        print(f"   Role: {role_id}")
        print(f"   Topic: {topic}")
        
        # Calculate ECTS per unit with smart distribution
        base_ects_per_unit = total_ects / uol
        
        # Create learning units with varied ECTS (more realistic)
        learning_units = []
        remaining_ects = total_ects
        
        for i in range(uol):
            # Vary unit sizes slightly for realism
            if i < uol - 1:  # Not the last unit
                if base_ects_per_unit <= 1.0:
                    # For small ECTS, keep units roughly equal
                    unit_ects = round(base_ects_per_unit, 1)
                else:
                    # For larger ECTS, add some variation
                    variation = 0.1 if i % 2 == 0 else -0.1
                    unit_ects = round(base_ects_per_unit + variation, 1)
                    
                # Ensure we don't exceed remaining ECTS
                unit_ects = min(unit_ects, remaining_ects - 0.1 * (uol - i - 1))
            else:
                # Last unit gets remaining ECTS
                unit_ects = round(remaining_ects, 1)
            
            # Create the learning unit
            unit = self._create_learning_unit(i + 1, unit_ects, uol, role_id, topic)
            learning_units.append(unit)
            remaining_ects -= unit_ects
            
            print(f"   Unit {i+1}: {unit_ects} ECTS - {unit['progression_level']}")
        
        return learning_units

    def _create_learning_unit(self, unit_number: int, ects: float, total_units: int, role_id: str, topic: str) -> Dict[str, Any]:
        """Create a single learning unit with industry-focused competencies"""
        
        # Determine progression level based on unit position
        progression_index = min(unit_number - 1, len(self.competency_progression_types) - 1)
        progression_type = self.competency_progression_types[progression_index]
        
        # Determine delivery approach based on ECTS size
        delivery_approach = self._determine_delivery_approach(ects)
        
        learning_unit = {
            'unit_id': f"UNIT_{role_id}_{unit_number}",
            'unit_number': unit_number,
            'progression_level': progression_type,
            'ects': ects,
            'estimated_hours': f"{int(ects * 25)}-{int(ects * 30)} hours",
            'delivery_approach': delivery_approach,
            'assessment_method': self._determine_assessment_method(ects, progression_type),
            'prerequisite_units': list(range(1, unit_number)) if unit_number > 1 else [],
            'stackable': True,
            'industry_ready': True
        }
        
        return learning_unit

    def _determine_delivery_approach(self, ects: float) -> str:
        """Determine delivery approach based on ECTS"""
        
        if ects <= 0.5:
            return "Focused micro-learning sessions with immediate practice"
        elif ects <= 1.0:
            return "Short-form learning with hands-on exercises"
        elif ects <= 2.0:
            return "Workshop-style learning with project components"
        else:
            return "Extended learning with comprehensive project work"

    def _determine_assessment_method(self, ects: float, progression_type: str) -> str:
        """Determine appropriate assessment method"""
        
        if ects <= 0.5:
            return "Practical demonstration (15-30 minutes)"
        elif ects <= 1.0:
            return "Skills assessment with portfolio evidence"
        elif progression_type in ["Mastery", "Leadership"]:
            return "Project presentation and peer evaluation"
        else:
            return "Competency-based assessment with workplace application"

    def create_industry_skills_matrix(self, learning_units: List[Dict[str, Any]], role_id: str) -> Dict[str, Any]:
        """Create skills matrix for Mateja to show industry members what they need - FIXED"""
        
        skills_matrix = {
            'role_id': role_id,
            'total_units': len(learning_units),
            'total_ects': sum(unit['ects'] for unit in learning_units),
            'competency_breakdown': [],
            'stackable_structure': {},
            'gap_analysis_ready': True
        }
        
        # Create competency breakdown for each unit - FIXED field names
        for unit in learning_units:
            # Use unit_title if available, otherwise use progression_level
            competency_title = unit.get('unit_title', f"{unit.get('progression_level', 'Professional')} Skills")
            
            competency_item = {
                'unit_number': unit['unit_number'],
                'competency_title': competency_title,
                'ects_investment': unit['ects'],
                'time_commitment': unit['estimated_hours'],
                'business_value': f"Enables {competency_title.lower()} in professional practice",
                'prerequisite_check': len(unit['prerequisite_units']) == 0,
                'standalone_value': unit['ects'] >= 0.5  # Can be taken independently if >= 0.5 ECTS
            }
            skills_matrix['competency_breakdown'].append(competency_item)
        
        # Create stackable structure - FIXED field names
        skills_matrix['stackable_structure'] = {
            'foundation_units': [u for u in learning_units if u['progression_level'] in ['Foundation', 'Development']],
            'advanced_units': [u for u in learning_units if u['progression_level'] in ['Application', 'Integration']],
            'leadership_units': [u for u in learning_units if u['progression_level'] in ['Mastery', 'Leadership']],
            'recommended_sequences': self._generate_learning_sequences(learning_units)
        }
        
        return skills_matrix

    def _generate_learning_sequences(self, learning_units: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommended learning sequences for different learner types"""
        
        return [
            {
                'sequence_name': 'Complete Pathway',
                'description': 'Full competency development from foundation to mastery',
                'units': [unit['unit_number'] for unit in learning_units],
                'total_ects': sum(unit['ects'] for unit in learning_units)
            },
            {
                'sequence_name': 'Foundation Only',
                'description': 'Essential competencies for immediate workplace application',
                'units': [unit['unit_number'] for unit in learning_units if unit['progression_level'] in ['Foundation', 'Development']],
                'total_ects': sum(unit['ects'] for unit in learning_units if unit['progression_level'] in ['Foundation', 'Development'])
            },
            {
                'sequence_name': 'Advanced Practice',
                'description': 'For professionals with existing foundation knowledge',
                'units': [unit['unit_number'] for unit in learning_units if unit['progression_level'] in ['Application', 'Integration', 'Mastery']],
                'total_ects': sum(unit['ects'] for unit in learning_units if unit['progression_level'] in ['Application', 'Integration', 'Mastery'])
            }
        ]
    
    def distribute_ects_across_uol_enhanced(self, total_ects: float, uol: int, role_id: str, 
                                          topic: str, delivery_mode: str = 'standard') -> List[Dict[str, Any]]:
        """Enhanced UOL distribution with detailed time and learning descriptions"""
        
        # Get base distribution
        base_units = self.distribute_ects_across_uol(total_ects, uol, role_id, topic)
        
        # If unit descriptor available, enhance with detailed descriptions
        if self.unit_descriptor:
            enhanced_units = []
            
            for i, unit in enumerate(base_units):
                # Get detailed unit description
                unit_description = self.unit_descriptor.describe_learning_unit_structure(
                    unit['unit_number'],
                    unit['ects'], 
                    uol,
                    topic,
                    delivery_mode
                )
                
                # Merge base unit with enhanced description
                enhanced_unit = {
                    **unit,
                    'detailed_description': unit_description,
                    'duration_breakdown': unit_description['duration'],
                    'learning_objectives': unit_description['learning_objectives'],
                    'weekly_schedule': unit_description['weekly_breakdown'],
                    'assessment_schedule': unit_description['assessment_schedule'],
                    'position_in_curriculum': unit_description['unit_position']
                }
                
                enhanced_units.append(enhanced_unit)
            
            return enhanced_units
        else:
            # Return base units if no descriptor available
            print("⚠️  Using basic unit descriptions (LearningUnitDescriptor not available)")
            return base_units
    
    def generate_curriculum_time_summary(self, units: List[Dict[str, Any]], total_ects: float) -> Dict[str, Any]:
        """Generate comprehensive time and structure summary"""
        
        if self.unit_descriptor:
            return self.unit_descriptor.generate_curriculum_overview(units, total_ects)
        else:
            # Basic fallback summary
            return {
                'total_ects': total_ects,
                'total_units': len(units),
                'estimated_hours': f"{int(total_ects * 25)}-{int(total_ects * 30)} hours",
                'completion_estimate': f"{math.ceil(total_ects / 5)} weeks"
            }