#!/usr/bin/env python3
# scripts/curriculum_generator/components/enhanced_curriculum_builder.py
"""
ENHANCED Curriculum Builder - Phase 1: Rich Content Integration
Addresses critical gaps: extended descriptions, varied language, rich topics
Eliminates repetitive "Focused learning" patterns with educational richness
"""

import random
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Import existing builders for base functionality
from scripts.curriculum_generator.components.curriculum_builder_micro_integrated import MicroIntegratedCurriculumBuilder
from scripts.curriculum_generator.domain.educational_profiles import EnhancedEducationalProfilesManager

class EnhancedCurriculumBuilder:
    """Enhanced curriculum builder with rich content integration and varied language patterns"""
    
    def __init__(self, modules: List[Dict[str, Any]], project_root: Path, role_definitions: Dict[str, Any]):
        self.modules = modules
        self.project_root = project_root
        self.role_definitions = role_definitions
        self.base_builder = MicroIntegratedCurriculumBuilder(modules, project_root, role_definitions)
        self.profile_manager = EnhancedEducationalProfilesManager(project_root)
        
        # Rich content integration patterns
        self.description_patterns = [
            "In-depth exploration of {topic} with practical applications in {context}",
            "Comprehensive study covering {topic} through {approach} methodology",
            "Advanced investigation into {topic} with real-world {context} scenarios", 
            "Specialized training in {topic} designed for {context} professionals",
            "Intensive learning experience examining {topic} within {context} frameworks",
            "Professional development module exploring {topic} through {context} lens",
            "Hands-on learning journey through {topic} with emphasis on {context} applications",
            "Strategic deep-dive into {topic} for effective {context} implementation"
        ]
        
        self.context_variations = {
            'Data': ['data-driven sustainability', 'environmental analytics', 'sustainability metrics'],
            'Management': ['organizational sustainability', 'strategic planning', 'change leadership'],
            'Technology': ['digital innovation', 'sustainable technology', 'green computing'],
            'General': ['holistic sustainability', 'interdisciplinary approaches', 'systems thinking'],
            'Policy': ['regulatory compliance', 'policy frameworks', 'governance structures']
        }
        
        print(f"🌟 Enhanced Curriculum Builder initialized")
        print(f"   ✅ Rich content patterns: {len(self.description_patterns)} variations")
        print(f"   ✅ Context variations: {sum(len(v) for v in self.context_variations.values())} contexts")
    
    def build_curriculum_with_semesters(
        self,
        role_id: str,
        role_name: str,
        topic: Optional[str],
        eqf_level: int,
        target_ects: float,
        role_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build enhanced curriculum with rich content integration"""
        
        print(f"\n🌟 Building ENHANCED curriculum with rich content")
        print(f"   Role: {role_id} | Topic: {topic} | ECTS: {target_ects}")
        
        # Step 1: Get educational profile for content foundation
        educational_profile = self.profile_manager.generate_comprehensive_profile(role_id, eqf_level)
        
        # Step 2: Generate base curriculum structure
        base_curriculum = self.base_builder.build_curriculum_with_semesters(
            role_id=role_id,
            role_name=role_name,
            topic=topic,
            eqf_level=eqf_level,
            target_ects=target_ects,
            role_info=role_info
        )
        
        if not base_curriculum:
            print("❌ Base curriculum generation failed!")
            return None
        
        # Step 3: Enhance with rich content integration
        enhanced_curriculum = self._enhance_curriculum_content(
            base_curriculum, educational_profile, topic, role_info
        )
        
        # Step 4: Update metadata
        enhanced_curriculum['metadata']['builder_version'] = 'Enhanced_v1.0'
        enhanced_curriculum['metadata']['content_enhancement'] = 'Rich content integration applied'
        enhanced_curriculum['metadata']['language_patterns'] = 'Varied patterns (no repetition)'
        enhanced_curriculum['metadata']['educational_profile_integrated'] = True
        enhanced_curriculum['metadata']['extended_descriptions_used'] = True
        
        print(f"🌟 Enhanced curriculum built successfully!")
        print(f"   ✅ Rich content applied to all modules/units")
        print(f"   ✅ Language variation patterns implemented")
        print(f"   ✅ Educational profile integration completed")
        
        return enhanced_curriculum
    
    def _enhance_curriculum_content(
        self, 
        curriculum: Dict[str, Any], 
        educational_profile: Dict[str, Any],
        topic: Optional[str],
        role_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply rich content enhancement to curriculum"""
        
        curriculum_type = curriculum.get('curriculum_type', 'micro_course')
        
        # Enhance based on curriculum type
        if curriculum_type == 'micro_course':
            curriculum = self._enhance_micro_course_content(curriculum, educational_profile, topic)
        elif curriculum_type == 'short_course':
            curriculum = self._enhance_short_course_content(curriculum, educational_profile, topic)
        else:
            curriculum = self._enhance_standard_course_content(curriculum, educational_profile, topic)
        
        # Add educational profile integration
        curriculum['educational_profile'] = educational_profile
        curriculum['profile_based_enhancements'] = self._generate_profile_based_enhancements(educational_profile)
        
        return curriculum
    
    def _enhance_micro_course_content(
        self, 
        curriculum: Dict[str, Any], 
        educational_profile: Dict[str, Any],
        topic: Optional[str]
    ) -> Dict[str, Any]:
        """Enhance micro-course with rich content from extended descriptions"""
        
        micro_units = curriculum.get('micro_units', [])
        enhanced_units = []
        
        for unit in micro_units:
            # Find source module for extended description
            source_module = self._find_source_module(unit.get('source_module_id'))
            if source_module:
                enhanced_unit = self._enhance_micro_unit_with_rich_content(unit, source_module, topic)
            else:
                enhanced_unit = self._enhance_micro_unit_fallback(unit, topic)
            
            enhanced_units.append(enhanced_unit)
        
        curriculum['micro_units'] = enhanced_units
        
        # Add curriculum-level enhancements
        curriculum['rich_content_summary'] = self._generate_rich_content_summary(enhanced_units)
        curriculum['learning_approach_description'] = self._generate_learning_approach_description(enhanced_units, topic)
        
        return curriculum
    
    def _enhance_micro_unit_with_rich_content(
        self, 
        unit: Dict[str, Any], 
        source_module: Dict[str, Any],
        topic: Optional[str]
    ) -> Dict[str, Any]:
        """Enhance micro unit with rich content from source module"""
        
        # Get extended description and extract relevant portion
        extended_desc = source_module.get('extended_description', '')
        unit_topic = unit.get('unit_topic', unit.get('title', ''))
        
        # Debug logging
        print(f"   🔧 Enhancing unit: {unit_topic} from module: {source_module.get('name', 'Unknown')}")
        
        # Generate rich description using extended content
        enhanced_description = self._extract_relevant_content(extended_desc, unit_topic, topic)
        
        # Apply varied language pattern
        thematic_area = source_module.get('thematic_area', 'General')
        context_options = self.context_variations.get(thematic_area, self.context_variations['General'])
        selected_context = random.choice(context_options)
        
        pattern = random.choice(self.description_patterns)
        varied_description = pattern.format(
            topic=unit_topic,
            context=selected_context,
            approach="evidence-based"
        )
        
        # Combine rich content with varied pattern
        full_description = f"{varied_description}. {enhanced_description}"
        
        # Enhanced unit structure with error handling
        enhanced_unit = unit.copy()
        try:
            enhanced_learning_outcomes = self._enhance_learning_outcomes(source_module, unit_topic)
        except Exception as e:
            print(f"   ⚠️ Warning: Learning outcomes enhancement failed for {unit_topic}: {e}")
            enhanced_learning_outcomes = {
                'knowledge_outcome': f"Understand key principles and concepts related to {unit_topic}",
                'understanding_outcome': f"Explain the application and significance of {unit_topic} in sustainability contexts",
                'skills_outcome': f"Apply {unit_topic} methodologies to solve practical sustainability challenges",
                'competency_level': 'Professional application level',
                'assessment_alignment': 'Outcomes-based assessment with practical demonstration'
            }
        
        enhanced_unit.update({
            'enhanced_description': full_description,
            'rich_topics': source_module.get('topics', [])[:5],  # Top 5 relevant topics
            'learning_approach': self._generate_learning_approach(source_module),
            'practical_applications': self._extract_practical_applications(extended_desc),
            'extended_learning_outcomes': enhanced_learning_outcomes,
            'content_depth_level': 'comprehensive',
            'source_module_name': source_module.get('name', 'Unknown'),
            'thematic_context': selected_context
        })
        
        return enhanced_unit
    
    def _enhance_micro_unit_fallback(self, unit: Dict[str, Any], topic: Optional[str]) -> Dict[str, Any]:
        """Fallback enhancement for units without source modules"""
        
        unit_topic = unit.get('unit_topic', unit.get('title', ''))
        
        # Generate description with variation
        pattern = random.choice(self.description_patterns)
        context = random.choice(self.context_variations['General'])
        
        enhanced_description = pattern.format(
            topic=unit_topic,
            context=context,
            approach="integrated"
        )
        
        enhanced_unit = unit.copy()
        enhanced_unit.update({
            'enhanced_description': enhanced_description,
            'rich_topics': [f"{unit_topic} fundamentals", f"{unit_topic} applications", f"{unit_topic} best practices"],
            'learning_approach': 'Interactive and practical methodology',
            'practical_applications': f"Real-world applications of {unit_topic} in professional contexts",
            'content_depth_level': 'foundational',
            'thematic_context': context
        })
        
        return enhanced_unit
    
    def _find_source_module(self, module_id: Optional[str]) -> Optional[Dict[str, Any]]:
        """Find source module by ID"""
        if not module_id:
            return None
        
        for module in self.modules:
            if module.get('id') == module_id:
                return module
        return None
    
    def _extract_relevant_content(self, extended_desc: str, unit_topic: str, main_topic: Optional[str]) -> str:
        """Extract relevant portion from extended description"""
        if not extended_desc:
            return f"Comprehensive coverage of {unit_topic} with practical implementation strategies."
        
        # Split into sentences and find most relevant ones
        sentences = [s.strip() for s in extended_desc.split('.') if s.strip()]
        
        # Simple relevance scoring based on keyword matching
        unit_keywords = unit_topic.lower().split()
        main_keywords = main_topic.lower().split() if main_topic else []
        all_keywords = unit_keywords + main_keywords
        
        scored_sentences = []
        for sentence in sentences:
            score = sum(1 for keyword in all_keywords if keyword in sentence.lower())
            if score > 0 or len(scored_sentences) < 2:  # Ensure at least 2 sentences
                scored_sentences.append((sentence, score))
        
        # Sort by relevance and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        selected_sentences = [s[0] for s in scored_sentences[:3]]
        
        return '. '.join(selected_sentences) + '.'
    
    def _generate_learning_approach(self, module: Dict[str, Any]) -> str:
        """Generate learning approach description"""
        delivery_methods = module.get('delivery_methods', [])
        module_types = module.get('module_type', [])
        is_work_based = module.get('is_work_based', False)
        
        approaches = []
        if 'classroom' in delivery_methods:
            approaches.append('interactive classroom sessions')
        if 'online' in delivery_methods:
            approaches.append('digital learning platforms')
        if 'blended' in delivery_methods:
            approaches.append('hybrid learning methodology')
        if 'practical' in module_types:
            approaches.append('hands-on practical exercises')
        if 'theoretical' in module_types:
            approaches.append('conceptual framework development')
        if is_work_based:
            approaches.append('workplace application projects')
        
        if not approaches:
            approaches = ['comprehensive learning methodology']
        
        return f"Delivered through {', '.join(approaches[:-1])} and {approaches[-1]}" if len(approaches) > 1 else f"Delivered through {approaches[0]}"
    
    def _extract_practical_applications(self, extended_desc: str) -> str:
        """Extract practical applications from extended description"""
        if not extended_desc:
            return "Professional application in real-world sustainability contexts"
        
        # Look for sentences containing application-related keywords
        application_keywords = ['apply', 'implement', 'use', 'practice', 'workplace', 'organization', 'project']
        sentences = [s.strip() for s in extended_desc.split('.') if s.strip()]
        
        application_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in application_keywords):
                application_sentences.append(sentence)
        
        if application_sentences:
            return '. '.join(application_sentences[:2]) + '.'
        else:
            return "Practical implementation strategies for professional sustainability initiatives"
    
    def _enhance_learning_outcomes(self, module: Dict[str, Any], unit_topic: str) -> Dict[str, Any]:
        """Enhance learning outcomes with rich detail - handles both dict and list formats"""
        base_outcomes = module.get('learning_outcomes', {})
        
        # Handle different learning outcomes formats
        if isinstance(base_outcomes, dict):
            # Dictionary format: {'knowledge': '...', 'understanding': '...', 'skills': '...'}
            knowledge_outcome = base_outcomes.get('knowledge', f"Understand key principles and concepts related to {unit_topic}")
            understanding_outcome = base_outcomes.get('understanding', f"Explain the application and significance of {unit_topic} in sustainability contexts")
            skills_outcome = base_outcomes.get('skills', f"Apply {unit_topic} methodologies to solve practical sustainability challenges")
        elif isinstance(base_outcomes, list):
            # List format: ['outcome1', 'outcome2', 'outcome3']
            knowledge_outcome = base_outcomes[0] if len(base_outcomes) > 0 else f"Understand key principles and concepts related to {unit_topic}"
            understanding_outcome = base_outcomes[1] if len(base_outcomes) > 1 else f"Explain the application and significance of {unit_topic} in sustainability contexts"
            skills_outcome = base_outcomes[2] if len(base_outcomes) > 2 else f"Apply {unit_topic} methodologies to solve practical sustainability challenges"
        else:
            # Fallback for other formats
            knowledge_outcome = f"Understand key principles and concepts related to {unit_topic}"
            understanding_outcome = f"Explain the application and significance of {unit_topic} in sustainability contexts"
            skills_outcome = f"Apply {unit_topic} methodologies to solve practical sustainability challenges"
        
        enhanced_outcomes = {
            'knowledge_outcome': knowledge_outcome,
            'understanding_outcome': understanding_outcome,
            'skills_outcome': skills_outcome,
            'competency_level': 'Professional application level',
            'assessment_alignment': 'Outcomes-based assessment with practical demonstration'
        }
        
        return enhanced_outcomes
    
    def _generate_rich_content_summary(self, enhanced_units: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of rich content features"""
        total_topics = sum(len(unit.get('rich_topics', [])) for unit in enhanced_units)
        content_depths = [unit.get('content_depth_level', 'standard') for unit in enhanced_units]
        thematic_contexts = list(set(unit.get('thematic_context', 'general') for unit in enhanced_units))
        
        return {
            'total_rich_topics_covered': total_topics,
            'content_depth_distribution': {depth: content_depths.count(depth) for depth in set(content_depths)},
            'thematic_contexts_integrated': thematic_contexts,
            'enhanced_descriptions_count': len(enhanced_units),
            'language_variation_applied': True
        }
    
    def _generate_learning_approach_description(self, enhanced_units: List[Dict[str, Any]], topic: Optional[str]) -> str:
        """Generate overall learning approach description"""
        
        approaches = set()
        for unit in enhanced_units:
            approach = unit.get('learning_approach', '')
            if approach:
                approaches.add(approach)
        
        if topic:
            focus_statement = f"with specialized focus on {topic}"
        else:
            focus_statement = "with comprehensive sustainability integration"
        
        return f"Multi-modal learning experience {focus_statement}, incorporating {len(approaches)} distinct pedagogical approaches for maximum engagement and practical application."
    
    def _enhance_short_course_content(self, curriculum: Dict[str, Any], educational_profile: Dict[str, Any], topic: Optional[str]) -> Dict[str, Any]:
        """Enhance short course content (combination of modules and micro-units)"""
        
        # Enhance both regular modules and micro-units
        if 'modules' in curriculum:
            curriculum['modules'] = [self._enhance_regular_module(mod, topic) for mod in curriculum['modules']]
        
        if 'micro_units' in curriculum:
            curriculum = self._enhance_micro_course_content(curriculum, educational_profile, topic)
        
        return curriculum
    
    def _enhance_standard_course_content(self, curriculum: Dict[str, Any], educational_profile: Dict[str, Any], topic: Optional[str]) -> Dict[str, Any]:
        """Enhance standard course content"""
        
        if 'modules' in curriculum:
            curriculum['modules'] = [self._enhance_regular_module(mod, topic) for mod in curriculum['modules']]
        
        # Add semester-level enhancements
        if 'semester_breakdown' in curriculum:
            curriculum['semester_breakdown'] = self._enhance_semester_breakdown(curriculum['semester_breakdown'], topic)
        
        return curriculum
    
    def _enhance_regular_module(self, module: Dict[str, Any], topic: Optional[str]) -> Dict[str, Any]:
        """Enhance regular module with rich content"""
        
        # Find full module data
        module_id = module.get('id')
        full_module = self._find_source_module(module_id)
        
        if full_module:
            extended_desc = full_module.get('extended_description', '')
            enhanced_module = module.copy()
            
            # Safely handle learning outcomes (could be dict or list)
            learning_outcomes = full_module.get('learning_outcomes', {})
            if isinstance(learning_outcomes, (dict, list)):
                enhanced_learning_outcomes = learning_outcomes
            else:
                enhanced_learning_outcomes = {}
            
            enhanced_module.update({
                'extended_description': extended_desc,
                'rich_topics': full_module.get('topics', []),
                'enhanced_learning_outcomes': enhanced_learning_outcomes,
                'delivery_approach': self._generate_learning_approach(full_module),
                'content_richness': 'comprehensive'
            })
        else:
            enhanced_module = module
        
        return enhanced_module
    
    def _enhance_semester_breakdown(self, semester_breakdown: List[Dict[str, Any]], topic: Optional[str]) -> List[Dict[str, Any]]:
        """Enhance semester breakdown with rich content"""
        
        enhanced_semesters = []
        for semester in semester_breakdown:
            enhanced_semester = semester.copy()
            
            # Enhance semester objectives
            if topic:
                enhanced_semester['enhanced_objectives'] = [
                    f"Apply {topic} principles to practical sustainability challenges",
                    f"Develop professional competency in {topic} implementation",
                    f"Integrate {topic} methodologies with sustainability frameworks"
                ]
            
            enhanced_semesters.append(enhanced_semester)
        
        return enhanced_semesters
    
    def _generate_profile_based_enhancements(self, educational_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhancements based on educational profile"""
        
        competencies = educational_profile.get('enhanced_competencies', [])
        career_progression = educational_profile.get('realistic_career_progression', {})
        
        return {
            'competency_integration': f"Curriculum aligned with {len(competencies)} professional competencies",
            'career_pathway_alignment': bool(career_progression),
            'industry_relevance': educational_profile.get('industry_sectors', []),
            'profile_based_customization': True
        }