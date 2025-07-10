# scripts/curriculum_generator/components/competency_module_selector.py
"""
Competency-Based Module Selector - Enhanced Module Selection
Integrates competency requirements from educational profiles into module selection
Supports both Profile-First and Plan B (direct) curriculum generation modes
"""

from typing import Dict, List, Any, Tuple, Optional, Set
import math
from scripts.curriculum_generator.components.topic_scorer import ConsolidatedTopicScorer


class CompetencyModuleSelector:
    """Enhanced module selector with competency-based selection support"""

    def __init__(self, modules: List[Dict[str, Any]], domain_knowledge=None):
        self.modules = modules
        self.modules_dict = {m.get('id', ''): m for m in modules}
        self.domain_knowledge = domain_knowledge
        self.topic_scorer = ConsolidatedTopicScorer()
        self.topic_scorer.debug_mode = False
        
        print("🎯 CompetencyModuleSelector initialized with competency-driven capabilities")

    def select_modules_competency_driven(
        self,
        competency_requirements: Dict[str, Any],
        role_id: str,
        topic: str,
        target_ects: int,
        eqf_level: int = 6
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        PRIMARY MODE: Select modules based on competency requirements from educational profile
        """
        
        print(f"🌱 COMPETENCY-DRIVEN: Module selection for {role_id}")
        print(f"   Topic: {topic}")
        print(f"   Competency requirements: {len(competency_requirements.get('competency_module_mapping', {}))}")
        
        # Extract competency requirements
        required_topics = competency_requirements.get('required_topics', [])
        required_thematic_areas = competency_requirements.get('required_thematic_areas', [])
        competency_mapping = competency_requirements.get('competency_module_mapping', {})
        assessment_requirements = competency_requirements.get('assessment_requirements', [])
        min_ects_per_category = competency_requirements.get('minimum_ects_per_category', {})
        
        print(f"   Required topics: {len(required_topics)}")
        print(f"   Competency mappings: {len(competency_mapping)}")
        
        # Phase 1: Select modules for competency requirements
        competency_modules = self._select_modules_for_competencies(
            competency_mapping, required_topics, eqf_level
        )
        
        # Phase 2: Fill remaining ECTS with topic-relevant modules
        remaining_ects = target_ects - sum(m.get('ects', 5) for m in competency_modules)
        topic_modules = []
        
        if remaining_ects > 0:
            topic_modules = self._select_topic_modules_to_fill(
                competency_modules, topic, role_id, remaining_ects, eqf_level
            )
        
        # Combine and validate
        selected_modules = competency_modules + topic_modules
        
        # Ensure minimum module count and ECTS
        selected_modules = self._ensure_minimum_requirements(
            selected_modules, target_ects, eqf_level, role_id, topic
        )
        
        # Generate selection metadata
        selection_metadata = self._generate_competency_selection_metadata(
            selected_modules, competency_requirements, target_ects
        )
        
        actual_ects = sum(m.get('ects', 5) for m in selected_modules)
        print(f"✅ COMPETENCY-DRIVEN: Selected {len(selected_modules)} modules, {actual_ects} ECTS")
        print(f"   Competency modules: {len(competency_modules)}")
        print(f"   Topic fill modules: {len(topic_modules)}")
        
        return selected_modules, selection_metadata

    def select_modules_direct_mode(
        self,
        role_id: str,
        topic: str,
        target_ects: int,
        eqf_level: int = 6
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        PLAN B MODE: Direct module selection without competency requirements (backward compatible)
        """
        
        print(f"📚 PLAN B MODE: Direct module selection for {role_id}")
        print(f"   Topic: {topic}")
        
        # Use enhanced topic scoring and role relevance
        scored_modules = []
        for module in self.modules:
            # Topic relevance score
            topic_score, topic_debug = self.topic_scorer.score_module_topic_relevance(
                module, topic, f"{role_id}_{module.get('id', 'unknown')}"
            )
            
            # Role relevance score from module's role_relevance field
            role_relevance = 0
            if 'role_relevance' in module:
                role_relevance_dict = module['role_relevance']
                if isinstance(role_relevance_dict, dict) and role_id in role_relevance_dict:
                    role_relevance = role_relevance_dict[role_id]
            
            # EQF compatibility score
            module_eqf = module.get('eqf_level', 6)
            eqf_score = max(0, 100 - abs(module_eqf - eqf_level) * 15)
            
            # Combined score (weighted)
            overall_score = (topic_score * 0.4) + (role_relevance * 0.4) + (eqf_score * 0.2)
            
            if overall_score > 0:
                scored_modules.append((module, overall_score, topic_score, role_relevance))
        
        # Sort by overall score
        scored_modules.sort(key=lambda x: x[1], reverse=True)
        
        # Select optimal combination
        selected_modules = []
        current_ects = 0
        
        for module, overall_score, topic_score, role_relevance in scored_modules:
            if current_ects < target_ects:
                module_ects = module.get('ects', 5)
                if current_ects + module_ects <= target_ects * 1.1:  # Allow 10% overage
                    selected_modules.append(module)
                    current_ects += module_ects
        
        # Ensure minimum modules
        min_modules = max(6, target_ects // 15)
        if len(selected_modules) < min_modules:
            for module, score, topic_score, role_relevance in scored_modules:
                if module not in selected_modules and len(selected_modules) < min_modules:
                    selected_modules.append(module)
        
        # Generate selection metadata
        selection_metadata = self._generate_direct_selection_metadata(
            selected_modules, target_ects, topic
        )
        
        actual_ects = sum(m.get('ects', 5) for m in selected_modules)
        print(f"✅ PLAN B MODE: Selected {len(selected_modules)} modules, {actual_ects} ECTS")
        
        return selected_modules, selection_metadata

    def _select_modules_for_competencies(
        self,
        competency_mapping: Dict[str, Any],
        required_topics: List[str],
        eqf_level: int
    ) -> List[Dict[str, Any]]:
        """Select modules that fulfill specific competency requirements"""
        
        competency_modules = []
        used_module_ids = set()
        
        # Process each competency's module requirements
        for competency_name, comp_data in competency_mapping.items():
            comp_required_modules = comp_data.get('required_modules', [])
            comp_outcomes = comp_data.get('learning_outcomes', [])
            
            # Find modules matching competency requirements
            for req_topic in comp_required_modules:
                best_module = self._find_best_module_for_requirement(
                    req_topic, eqf_level, used_module_ids
                )
                
                if best_module:
                    competency_modules.append(best_module)
                    used_module_ids.add(best_module.get('id', ''))
        
        # Additional topic-based requirements
        for req_topic in required_topics:
            if req_topic not in [m.get('name', '') for m in competency_modules]:
                best_module = self._find_best_module_for_requirement(
                    req_topic, eqf_level, used_module_ids
                )
                
                if best_module:
                    competency_modules.append(best_module)
                    used_module_ids.add(best_module.get('id', ''))
        
        print(f"   🌱 Selected {len(competency_modules)} competency-specific modules")
        return competency_modules

    def _find_best_module_for_requirement(
        self,
        requirement: str,
        eqf_level: int,
        used_module_ids: Set[str]
    ) -> Optional[Dict[str, Any]]:
        """Find the best module matching a specific requirement"""
        
        requirement_lower = requirement.lower()
        best_module = None
        best_score = 0
        
        for module in self.modules:
            if module.get('id', '') in used_module_ids:
                continue
            
            # Check EQF compatibility
            module_eqf = module.get('eqf_level', 6)
            if abs(module_eqf - eqf_level) > 1:
                continue
            
            # Score module relevance to requirement
            score = 0
            module_name = module.get('name', '').lower()
            module_desc = module.get('description', '').lower()
            module_topics = module.get('topics', [])
            module_skills = module.get('skills', [])
            
            # Direct name matching
            if requirement_lower in module_name:
                score += 50
            
            # Description matching
            if requirement_lower in module_desc:
                score += 30
            
            # Topics matching
            for topic in module_topics:
                if requirement_lower in str(topic).lower():
                    score += 40
            
            # Skills matching
            for skill in module_skills:
                if requirement_lower in str(skill).lower():
                    score += 35
            
            # Keyword matching (fuzzy)
            req_words = requirement_lower.split()
            for word in req_words:
                if len(word) > 2:
                    if word in module_name:
                        score += 15
                    if word in module_desc:
                        score += 10
            
            if score > best_score:
                best_score = score
                best_module = module
        
        return best_module

    def _select_topic_modules_to_fill(
        self,
        existing_modules: List[Dict[str, Any]],
        topic: str,
        role_id: str,
        remaining_ects: int,
        eqf_level: int
    ) -> List[Dict[str, Any]]:
        """Select additional topic-relevant modules to fill remaining ECTS"""
        
        existing_ids = {m.get('id', '') for m in existing_modules}
        topic_modules = []
        current_ects = 0
        
        # Score remaining modules by topic relevance
        scored_modules = []
        for module in self.modules:
            if module.get('id', '') in existing_ids:
                continue
            
            # Check EQF compatibility
            module_eqf = module.get('eqf_level', 6)
            if abs(module_eqf - eqf_level) > 1:
                continue
            
            # Topic relevance score
            topic_score, _ = self.topic_scorer.score_module_topic_relevance(module, topic)
            
            # Role relevance score
            role_relevance = 0
            if 'role_relevance' in module:
                role_relevance_dict = module['role_relevance']
                if isinstance(role_relevance_dict, dict) and role_id in role_relevance_dict:
                    role_relevance = role_relevance_dict[role_id]
            
            combined_score = (topic_score * 0.6) + (role_relevance * 0.4)
            
            if combined_score > 10:  # Minimum relevance threshold
                scored_modules.append((module, combined_score))
        
        # Sort by relevance and select
        scored_modules.sort(key=lambda x: x[1], reverse=True)
        
        for module, score in scored_modules:
            if current_ects >= remaining_ects:
                break
            
            module_ects = module.get('ects', 5)
            if current_ects + module_ects <= remaining_ects * 1.2:  # Allow slight overage
                topic_modules.append(module)
                current_ects += module_ects
        
        print(f"   📚 Selected {len(topic_modules)} topic-fill modules ({current_ects} ECTS)")
        return topic_modules

    def _ensure_minimum_requirements(
        self,
        selected_modules: List[Dict[str, Any]],
        target_ects: int,
        eqf_level: int,
        role_id: str,
        topic: str
    ) -> List[Dict[str, Any]]:
        """Ensure minimum module count and ECTS requirements are met"""
        
        current_ects = sum(m.get('ects', 5) for m in selected_modules)
        min_modules = max(6, target_ects // 15)
        existing_ids = {m.get('id', '') for m in selected_modules}
        
        # Add more modules if below minimums
        if len(selected_modules) < min_modules or current_ects < target_ects * 0.8:
            additional_modules = []
            
            for module in self.modules:
                if module.get('id', '') in existing_ids:
                    continue
                
                module_eqf = module.get('eqf_level', 6)
                if abs(module_eqf - eqf_level) > 1:
                    continue
                
                # Check if we need more modules or ECTS
                need_more_modules = len(selected_modules) + len(additional_modules) < min_modules
                need_more_ects = current_ects + sum(m.get('ects', 5) for m in additional_modules) < target_ects * 0.9
                
                if need_more_modules or need_more_ects:
                    additional_modules.append(module)
                    
                    if len(selected_modules) + len(additional_modules) >= min_modules and \
                       current_ects + sum(m.get('ects', 5) for m in additional_modules) >= target_ects * 0.9:
                        break
            
            selected_modules.extend(additional_modules)
            print(f"   📈 Added {len(additional_modules)} modules to meet minimum requirements")
        
        return selected_modules

    def _generate_competency_selection_metadata(
        self,
        selected_modules: List[Dict[str, Any]],
        competency_requirements: Dict[str, Any],
        target_ects: int
    ) -> Dict[str, Any]:
        """Generate metadata for competency-driven selection"""
        
        actual_ects = sum(m.get('ects', 5) for m in selected_modules)
        required_topics = competency_requirements.get('required_topics', [])
        competency_mapping = competency_requirements.get('competency_module_mapping', {})
        
        # Analyze competency coverage
        covered_topics = []
        for module in selected_modules:
            module_name = module.get('name', '').lower()
            module_topics = module.get('topics', [])
            
            for req_topic in required_topics:
                if req_topic.lower() in module_name or \
                   any(req_topic.lower() in str(topic).lower() for topic in module_topics):
                    covered_topics.append(req_topic)
        
        covered_topics = list(set(covered_topics))
        
        return {
            'selection_mode': 'competency_driven',
            'total_modules': len(selected_modules),
            'total_ects': actual_ects,
            'target_ects': target_ects,
            'ects_efficiency': min((actual_ects / target_ects) * 100, 100) if target_ects > 0 else 100,
            'competency_requirements': {
                'total_competencies': len(competency_mapping),
                'required_topics': len(required_topics),
                'covered_topics': len(covered_topics),
                'topic_coverage_percentage': (len(covered_topics) / len(required_topics)) * 100 if required_topics else 100
            },
            'module_distribution': {
                'competency_modules': len([m for m in selected_modules if self._is_competency_module(m, required_topics)]),
                'topic_fill_modules': len([m for m in selected_modules if not self._is_competency_module(m, required_topics)])
            }
        }

    def _generate_direct_selection_metadata(
        self,
        selected_modules: List[Dict[str, Any]],
        target_ects: int,
        topic: str
    ) -> Dict[str, Any]:
        """Generate metadata for direct selection (Plan B mode)"""
        
        actual_ects = sum(m.get('ects', 5) for m in selected_modules)
        
        # Calculate average topic relevance
        total_topic_score = 0
        scored_modules = 0
        
        for module in selected_modules:
            topic_score, _ = self.topic_scorer.score_module_topic_relevance(module, topic)
            total_topic_score += topic_score
            scored_modules += 1
        
        avg_topic_relevance = total_topic_score / scored_modules if scored_modules > 0 else 0
        
        return {
            'selection_mode': 'direct_topic_role',
            'total_modules': len(selected_modules),
            'total_ects': actual_ects,
            'target_ects': target_ects,
            'ects_efficiency': min((actual_ects / target_ects) * 100, 100) if target_ects > 0 else 100,
            'topic_analysis': {
                'target_topic': topic,
                'average_topic_relevance': avg_topic_relevance,
                'high_relevance_modules': len([m for m in selected_modules 
                                             if self.topic_scorer.score_module_topic_relevance(m, topic)[0] > 60])
            },
            'quality_indicators': {
                'topic_coverage': 'high' if avg_topic_relevance > 50 else 'medium' if avg_topic_relevance > 30 else 'low',
                'module_diversity': len(set(m.get('thematic_area', 'general') for m in selected_modules))
            }
        }

    def _is_competency_module(self, module: Dict[str, Any], required_topics: List[str]) -> bool:
        """Check if module was selected for competency requirements"""
        module_name = module.get('name', '').lower()
        module_topics = module.get('topics', [])
        
        for req_topic in required_topics:
            if req_topic.lower() in module_name or \
               any(req_topic.lower() in str(topic).lower() for topic in module_topics):
                return True
        
        return False

    # Backward compatibility methods
    def select_modules_for_role_and_topic(self, role_id: str, topic: str, target_ects: int, eqf_level: int = 6) -> List[Dict[str, Any]]:
        """Backward compatibility method - uses direct mode"""
        selected_modules, _ = self.select_modules_direct_mode(role_id, topic, target_ects, eqf_level)
        return selected_modules
