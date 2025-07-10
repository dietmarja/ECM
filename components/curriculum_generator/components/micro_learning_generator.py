#!/usr/bin/env python3
# scripts/curriculum_generator/components/micro_learning_generator.py
"""
Micro-Learning Unit Generator
Breaks down standard modules into micro-learning units with fractional ECTS
Supports 0.1 ECTS to 5 ECTS learning units for short courses and micro-credentials
"""

from typing import Dict, Any, List, Optional
import json
import math

class MicroLearningGenerator:
    """Generates micro-learning units from standard modules"""
    
    def __init__(self):
        self.micro_ects_options = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
        self.learning_unit_types = {
            'concept': {'min_ects': 0.1, 'max_ects': 0.5, 'duration_hours': '1-5 hours'},
            'skill': {'min_ects': 0.5, 'max_ects': 2.0, 'duration_hours': '5-20 hours'},
            'application': {'min_ects': 1.0, 'max_ects': 3.0, 'duration_hours': '10-30 hours'},
            'project': {'min_ects': 2.0, 'max_ects': 5.0, 'duration_hours': '20-50 hours'}
        }
        
        print(f"🔬 Micro-Learning Generator initialized")
        print(f"   Supported ECTS range: {min(self.micro_ects_options)} - {max(self.micro_ects_options)}")
    
    def generate_micro_units_from_modules(
        self, 
        modules: List[Dict[str, Any]], 
        target_micro_ects: float,
        learning_focus: str = "general"
    ) -> List[Dict[str, Any]]:
        """Generate micro-learning units from standard modules"""
        
        print(f"\n🔬 Generating micro-learning units:")
        print(f"   Target ECTS: {target_micro_ects}")
        print(f"   Learning focus: {learning_focus}")
        print(f"   Source modules: {len(modules)}")
        
        micro_units = []
        accumulated_ects = 0.0
        
        for module in modules:
            if accumulated_ects >= target_micro_ects:
                break
                
            module_micro_units = self._break_module_into_micro_units(
                module, target_micro_ects - accumulated_ects, learning_focus
            )
            
            for unit in module_micro_units:
                if accumulated_ects + unit['ects'] <= target_micro_ects * 1.1:  # 10% tolerance
                    micro_units.append(unit)
                    accumulated_ects += unit['ects']
                    print(f"     ✅ {unit['title']} ({unit['ects']} ECTS)")
                    
                    if accumulated_ects >= target_micro_ects:
                        break
        
        print(f"   📊 Generated {len(micro_units)} micro-units, total: {accumulated_ects} ECTS")
        return micro_units
    
    def _break_module_into_micro_units(
        self, 
        module: Dict[str, Any], 
        remaining_ects: float,
        focus: str
    ) -> List[Dict[str, Any]]:
        """Break a single module into micro-learning units"""
        
        module_ects = module.get('ects', 5)
        module_title = module.get('title', 'Unknown Module')
        module_topics = module.get('topics', [])
        learning_outcomes = module.get('learning_outcomes', [])
        
        micro_units = []
        
        # Strategy 1: Topic-based micro-units
        if module_topics and len(module_topics) > 1:
            micro_units.extend(self._create_topic_based_micro_units(
                module, module_topics, remaining_ects, focus
            ))
        
        # Strategy 2: Learning outcome-based micro-units  
        elif learning_outcomes and len(learning_outcomes) > 2:
            micro_units.extend(self._create_outcome_based_micro_units(
                module, learning_outcomes, remaining_ects, focus
            ))
        
        # Strategy 3: Conceptual breakdown
        else:
            micro_units.extend(self._create_conceptual_micro_units(
                module, remaining_ects, focus
            ))
        
        return micro_units
    
    def _create_topic_based_micro_units(
        self, 
        module: Dict[str, Any], 
        topics: List[str], 
        remaining_ects: float,
        focus: str
    ) -> List[Dict[str, Any]]:
        """Create micro-units based on module topics"""
        
        module_title = module.get('title', 'Unknown Module')
        module_ects = module.get('ects', 5)
        
        micro_units = []
        topics_to_use = topics[:min(len(topics), int(remaining_ects * 4))]  # Reasonable limit
        
        for i, topic in enumerate(topics_to_use):
            if sum(unit['ects'] for unit in micro_units) >= remaining_ects:
                break
                
            # Determine micro-unit type and ECTS
            unit_type = self._determine_unit_type(topic, focus)
            unit_ects = self._calculate_micro_ects(unit_type, remaining_ects, len(topics_to_use) - i)
            
            micro_unit = {
                'title': f"{topic} (Micro-Unit)",
                'parent_module': module_title,
                'ects': unit_ects,
                'unit_type': unit_type,
                'duration_hours': self.learning_unit_types[unit_type]['duration_hours'],
                'description': f"Focused learning on {topic} from {module_title}",
                'learning_outcomes': self._generate_micro_learning_outcomes(topic, unit_type),
                'assessment_method': self._determine_micro_assessment(unit_type),
                'topics': [topic],
                'delivery_methods': ['online', 'self-paced'],
                'thematic_area': module.get('thematic_area', 'General'),
                'micro_credential_eligible': True,
                'prerequisite_units': micro_units[-1]['title'] if micro_units else None,
                'difficulty_level': self._assess_topic_difficulty(topic),
                'eqf_level': module.get('eqf_level', 6)
            }
            
            micro_units.append(micro_unit)
        
        return micro_units
    
    def _create_outcome_based_micro_units(
        self, 
        module: Dict[str, Any], 
        outcomes: List[str], 
        remaining_ects: float,
        focus: str
    ) -> List[Dict[str, Any]]:
        """Create micro-units based on learning outcomes"""
        
        module_title = module.get('title', 'Unknown Module')
        micro_units = []
        
        # Group outcomes into logical micro-units (2-3 outcomes per unit)
        outcome_groups = [outcomes[i:i+2] for i in range(0, len(outcomes), 2)]
        
        for i, outcome_group in enumerate(outcome_groups):
            if sum(unit['ects'] for unit in micro_units) >= remaining_ects:
                break
            
            # Determine unit characteristics
            primary_outcome = outcome_group[0]
            unit_type = self._determine_unit_type_from_outcome(primary_outcome)
            unit_ects = self._calculate_micro_ects(unit_type, remaining_ects, len(outcome_groups) - i)
            
            micro_unit = {
                'title': f"{module_title} - Unit {i+1}",
                'parent_module': module_title,
                'ects': unit_ects,
                'unit_type': unit_type,
                'duration_hours': self.learning_unit_types[unit_type]['duration_hours'],
                'description': f"Learning unit focused on: {primary_outcome}",
                'learning_outcomes': outcome_group,
                'assessment_method': self._determine_micro_assessment(unit_type),
                'topics': self._extract_topics_from_outcomes(outcome_group),
                'delivery_methods': ['online', 'self-paced'],
                'thematic_area': module.get('thematic_area', 'General'),
                'micro_credential_eligible': True,
                'difficulty_level': self._assess_outcome_difficulty(primary_outcome),
                'eqf_level': module.get('eqf_level', 6)
            }
            
            micro_units.append(micro_unit)
        
        return micro_units
    
    def _create_conceptual_micro_units(
        self, 
        module: Dict[str, Any], 
        remaining_ects: float,
        focus: str
    ) -> List[Dict[str, Any]]:
        """Create conceptual micro-units when topics/outcomes are limited"""
        
        module_title = module.get('title', 'Unknown Module')
        module_description = module.get('description', '')
        
        # Create 3-4 conceptual units per module
        conceptual_units = [
            {'name': 'Fundamentals', 'type': 'concept', 'focus': 'Core concepts and principles'},
            {'name': 'Methods & Tools', 'type': 'skill', 'focus': 'Practical methods and tools'},
            {'name': 'Application', 'type': 'application', 'focus': 'Real-world application'},
            {'name': 'Synthesis', 'type': 'project', 'focus': 'Integration and synthesis'}
        ]
        
        micro_units = []
        for i, concept in enumerate(conceptual_units):
            if sum(unit['ects'] for unit in micro_units) >= remaining_ects:
                break
            
            unit_ects = self._calculate_micro_ects(concept['type'], remaining_ects, len(conceptual_units) - i)
            
            micro_unit = {
                'title': f"{module_title}: {concept['name']}",
                'parent_module': module_title,
                'ects': unit_ects,
                'unit_type': concept['type'],
                'duration_hours': self.learning_unit_types[concept['type']]['duration_hours'],
                'description': f"{concept['focus']} related to {module_title}",
                'learning_outcomes': [f"Understand {concept['focus'].lower()} in {module_title.lower()}"],
                'assessment_method': self._determine_micro_assessment(concept['type']),
                'topics': [concept['name']],
                'delivery_methods': ['online', 'self-paced'],
                'thematic_area': module.get('thematic_area', 'General'),
                'micro_credential_eligible': True,
                'difficulty_level': 'intermediate',
                'eqf_level': module.get('eqf_level', 6)
            }
            
            micro_units.append(micro_unit)
        
        return micro_units
    
    def _determine_unit_type(self, topic: str, focus: str) -> str:
        """Determine the type of micro-learning unit based on topic"""
        
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['introduction', 'overview', 'principles', 'fundamentals']):
            return 'concept'
        elif any(word in topic_lower for word in ['implementation', 'project', 'case study', 'integration']):
            return 'project'
        elif any(word in topic_lower for word in ['tools', 'methods', 'techniques', 'skills']):
            return 'skill'
        else:
            return 'application'
    
    def _determine_unit_type_from_outcome(self, outcome: str) -> str:
        """Determine unit type from learning outcome"""
        
        outcome_lower = outcome.lower()
        
        if any(word in outcome_lower for word in ['understand', 'explain', 'describe', 'define']):
            return 'concept'
        elif any(word in outcome_lower for word in ['apply', 'use', 'implement', 'demonstrate']):
            return 'skill'
        elif any(word in outcome_lower for word in ['analyze', 'evaluate', 'create', 'design']):
            return 'application'
        elif any(word in outcome_lower for word in ['integrate', 'synthesize', 'develop', 'build']):
            return 'project'
        else:
            return 'skill'
    
    def _calculate_micro_ects(self, unit_type: str, remaining_ects: float, units_remaining: int) -> float:
        """Calculate appropriate ECTS for micro-unit"""
        
        type_config = self.learning_unit_types[unit_type]
        min_ects = type_config['min_ects']
        max_ects = type_config['max_ects']
        
        # Calculate target ECTS based on remaining budget and units
        if units_remaining > 0:
            target_ects = remaining_ects / units_remaining
        else:
            target_ects = remaining_ects
        
        # Constrain to type limits
        target_ects = max(min_ects, min(max_ects, target_ects))
        
        # Round to nearest valid micro-ECTS value
        closest_ects = min(self.micro_ects_options, key=lambda x: abs(x - target_ects))
        
        return closest_ects
    
    def _generate_micro_learning_outcomes(self, topic: str, unit_type: str) -> List[str]:
        """Generate learning outcomes for micro-unit"""
        
        outcome_templates = {
            'concept': [
                f"Understand the core concepts of {topic}",
                f"Explain the principles underlying {topic}"
            ],
            'skill': [
                f"Apply {topic} techniques in practical contexts",
                f"Demonstrate proficiency with {topic} tools"
            ],
            'application': [
                f"Analyze real-world {topic} scenarios",
                f"Evaluate {topic} solutions and approaches"
            ],
            'project': [
                f"Design and implement {topic} projects",
                f"Integrate {topic} with other sustainability practices"
            ]
        }
        
        return outcome_templates.get(unit_type, [f"Learn about {topic}"])
    
    def _determine_micro_assessment(self, unit_type: str) -> str:
        """Determine assessment method for micro-unit"""
        
        assessment_map = {
            'concept': 'Knowledge check quiz',
            'skill': 'Practical exercise',
            'application': 'Case study analysis', 
            'project': 'Mini-project submission'
        }
        
        return assessment_map.get(unit_type, 'Competency assessment')
    
    def _extract_topics_from_outcomes(self, outcomes: List[str]) -> List[str]:
        """Extract topic keywords from learning outcomes"""
        
        topics = []
        for outcome in outcomes:
            # Simple keyword extraction (can be enhanced)
            words = outcome.split()
            for word in words:
                if len(word) > 4 and word.lower() not in ['understand', 'apply', 'analyze', 'evaluate']:
                    topics.append(word.strip('.,!?'))
        
        return list(set(topics))[:3]  # Limit to 3 topics
    
    def _assess_topic_difficulty(self, topic: str) -> str:
        """Assess difficulty level of topic"""
        
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['advanced', 'complex', 'expert', 'sophisticated']):
            return 'advanced'
        elif any(word in topic_lower for word in ['basic', 'introduction', 'fundamentals', 'overview']):
            return 'beginner'
        else:
            return 'intermediate'
    
    def _assess_outcome_difficulty(self, outcome: str) -> str:
        """Assess difficulty level from learning outcome"""
        
        outcome_lower = outcome.lower()
        
        if any(word in outcome_lower for word in ['create', 'design', 'synthesize', 'evaluate']):
            return 'advanced'
        elif any(word in outcome_lower for word in ['understand', 'describe', 'explain']):
            return 'beginner'
        else:
            return 'intermediate'
    
    def create_micro_credential_pathway(self, micro_units: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create micro-credential pathway from micro-units"""
        
        total_ects = sum(unit['ects'] for unit in micro_units)
        
        pathway = {
            'pathway_id': f"MICRO_PATHWAY_{len(micro_units)}units_{total_ects}ects",
            'pathway_name': f"Micro-Learning Pathway ({total_ects} ECTS)",
            'total_ects': total_ects,
            'total_units': len(micro_units),
            'estimated_duration': f"{int(total_ects * 10)}-{int(total_ects * 15)} hours",
            'difficulty_progression': self._analyze_difficulty_progression(micro_units),
            'micro_units': micro_units,
            'completion_criteria': {
                'minimum_units': math.ceil(len(micro_units) * 0.8),  # 80% completion
                'assessment_pass_rate': '70%',
                'time_limit': f"{int(total_ects * 20)} hours maximum"
            },
            'micro_credentials_available': [
                {
                    'credential_name': f"Micro-Credential: {unit['title']}",
                    'ects_value': unit['ects'],
                    'unit_type': unit['unit_type']
                }
                for unit in micro_units
            ],
            'stackable_with': 'Other micro-learning pathways',
            'recognition_level': 'Professional micro-credential'
        }
        
        return pathway
    
    def _analyze_difficulty_progression(self, micro_units: List[Dict[str, Any]]) -> str:
        """Analyze difficulty progression across micro-units"""
        
        difficulty_levels = [unit.get('difficulty_level', 'intermediate') for unit in micro_units]
        
        if difficulty_levels[0] == 'beginner' and difficulty_levels[-1] == 'advanced':
            return 'Progressive (Beginner → Advanced)'
        elif all(level == 'beginner' for level in difficulty_levels):
            return 'Beginner level throughout'
        elif all(level == 'advanced' for level in difficulty_levels):
            return 'Advanced level throughout'
        else:
            return 'Mixed difficulty levels'

    def generate_short_course_from_micro_units(
        self, 
        micro_units: List[Dict[str, Any]], 
        course_title: str,
        target_ects: float
    ) -> Dict[str, Any]:
        """Generate a complete short course from micro-units"""
        
        # Select micro-units that fit the target ECTS
        selected_units = []
        accumulated_ects = 0.0
        
        for unit in micro_units:
            if accumulated_ects + unit['ects'] <= target_ects * 1.1:  # 10% tolerance
                selected_units.append(unit)
                accumulated_ects += unit['ects']
                
                if accumulated_ects >= target_ects:
                    break
        
        short_course = {
            'course_id': f"SHORT_COURSE_{len(selected_units)}units_{accumulated_ects}ects",
            'course_title': course_title,
            'course_type': 'short_course',
            'total_ects': accumulated_ects,
            'total_units': len(selected_units),
            'micro_units': selected_units,
            'estimated_duration': f"{int(accumulated_ects * 8)}-{int(accumulated_ects * 12)} hours",
            'delivery_mode': 'Online self-paced with live sessions',
            'assessment_strategy': 'Continuous micro-assessments',
            'completion_certificate': f"Certificate in {course_title}",
            'micro_credentials_included': True,
            'stackable_towards': 'Full programme credentials',
            'entry_requirements': 'Open access',
            'target_audience': 'Professionals seeking focused upskilling',
            'course_structure': self._organize_units_into_modules(selected_units)
        }
        
        return short_course
    
    def _organize_units_into_modules(self, micro_units: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Organize micro-units into logical modules for course structure"""
        
        # Group units by type
        modules = {}
        for unit in micro_units:
            unit_type = unit['unit_type']
            if unit_type not in modules:
                modules[unit_type] = []
            modules[unit_type].append(unit)
        
        structured_modules = {}
        module_number = 1
        
        for unit_type, units in modules.items():
            total_ects = sum(unit['ects'] for unit in units)
            
            structured_modules[f"Module {module_number}"] = {
                'module_name': f"{unit_type.title()} Module",
                'focus_area': unit_type,
                'units': units,
                'total_ects': total_ects,
                'estimated_hours': f"{int(total_ects * 10)}-{int(total_ects * 15)}"
            }
            
            module_number += 1
        
        return structured_modules
