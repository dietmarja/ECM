"""
Module selection logic for curriculum generation.
Selects optimal modules based on topic relevance, EQF level, role requirements, and ECTS constraints.
"""

from typing import Dict, List, Any, Tuple
import math


class ModuleSelector:
    """Handles module selection for curriculum generation"""
    
    def __init__(self, domain_knowledge, role_manager=None):
        self.domain_knowledge = domain_knowledge
        self.role_manager = role_manager
        
    def select_modules_for_topic(
        self, 
        topic: str, 
        eqf_level: int, 
        target_ects: int, 
        modules: List[Dict[str, Any]],
        role_id: str = None
    ) -> List[Dict[str, Any]]:
        """Select optimal modules for a topic, EQF level, role, and ECTS target"""
        
        print(f"🎯 Selecting modules for topic: {topic} (EQF {eqf_level}, {target_ects} ECTS, Role: {role_id})")
        
        # Initialize empty result in case of errors
        selected_modules = []
        
        try:
            # Filter modules by EQF level compatibility
            compatible_modules = self._filter_by_eqf_level(modules, eqf_level)
            print(f"📊 {len(compatible_modules)} modules compatible with EQF {eqf_level}")
            
            if not compatible_modules:
                print("⚠️  No compatible modules found")
                return selected_modules
            
            # Score modules by relevance to topic and role
            scored_modules = self._score_modules_by_relevance(compatible_modules, topic, role_id)
            
            if not scored_modules:
                print("⚠️  No modules could be scored")
                return selected_modules
            
            # Sort by relevance score (descending)
            scored_modules.sort(key=lambda x: x.get('total_relevance_score', 0), reverse=True)
            
            # Select optimal combination to meet ECTS target
            selected_modules = self._select_optimal_combination(scored_modules, target_ects)
            
            print(f"✅ Selected {len(selected_modules)} modules totaling {sum(m.get('ects', 5) for m in selected_modules)} ECTS")
            
        except Exception as e:
            print(f"❌ Error in module selection: {e}")
            # Return empty list rather than crashing
            selected_modules = []
        
        return selected_modules
        
    def _filter_by_eqf_level(self, modules: List[Dict[str, Any]], target_eqf: int) -> List[Dict[str, Any]]:
        """Filter modules compatible with target EQF level"""
        compatible = []
        
        for module in modules:
            if not isinstance(module, dict):
                continue
                
            module_eqf = module.get('eqf_level', 6)
            
            # Allow modules at target level or one level below/above
            if target_eqf - 1 <= module_eqf <= target_eqf + 1:
                compatible.append(module)
                
        return compatible
        
    def _score_modules_by_relevance(
        self, 
        modules: List[Dict[str, Any]], 
        topic: str,
        role_id: str = None
    ) -> List[Dict[str, Any]]:
        """Score modules by relevance to topic and role"""
        scored_modules = []
        
        for module in modules:
            if not isinstance(module, dict):
                continue
                
            try:
                # Calculate topic relevance score
                topic_relevance = self.domain_knowledge.score_module_relevance(module, topic)
                
                # Calculate role relevance score from module's role_relevance field
                role_relevance = 0
                if role_id and 'role_relevance' in module:
                    role_relevance_dict = module['role_relevance']
                    if isinstance(role_relevance_dict, dict) and role_id in role_relevance_dict:
                        role_relevance = role_relevance_dict[role_id] / 10.0  # Scale to 0-10
                
                # Combine topic and role scores (weighted)
                total_relevance = (topic_relevance * 0.6) + (role_relevance * 0.4)
                
                # Create scored module
                scored_module = module.copy()
                scored_module['topic_relevance_score'] = topic_relevance
                scored_module['role_relevance_score'] = role_relevance
                scored_module['total_relevance_score'] = total_relevance
                
                scored_modules.append(scored_module)
                
            except Exception as e:
                print(f"⚠️  Error scoring module {module.get('title', 'Unknown')}: {e}")
                continue
            
        return scored_modules
        
    def _select_optimal_combination(
        self, 
        scored_modules: List[Dict[str, Any]], 
        target_ects: int
    ) -> List[Dict[str, Any]]:
        """Select optimal combination of modules to meet ECTS target"""
        
        selected = []
        current_ects = 0
        used_indices = set()
        
        if not scored_modules:
            return selected
        
        # First pass: Select high-relevance modules
        for i, module in enumerate(scored_modules):
            if i in used_indices:
                continue
                
            module_ects = module.get('ects', 5)
            
            # If adding this module doesn't exceed target significantly
            if current_ects + module_ects <= target_ects * 1.1:
                selected.append(module)
                current_ects += module_ects
                used_indices.add(i)
                
                if current_ects >= target_ects * 0.9:
                    break
                    
        # Second pass: Fill remaining ECTS if needed
        if current_ects < target_ects * 0.8:
            remaining_ects = target_ects - current_ects
            
            for i, module in enumerate(scored_modules):
                if i in used_indices:
                    continue
                    
                module_ects = module.get('ects', 5)
                
                if module_ects <= remaining_ects * 1.2:
                    selected.append(module)
                    current_ects += module_ects
                    used_indices.add(i)
                    remaining_ects = target_ects - current_ects
                    
                    if remaining_ects <= 5:  # Close enough
                        break
                        
        # Ensure minimum number of modules - FIX: Use 'selected' not 'selected_modules'
        min_modules = max(3, target_ects // 10)
        if len(selected) < min_modules:
            for i, module in enumerate(scored_modules):
                if i in used_indices:
                    continue
                    
                if len(selected) >= min_modules:
                    break
                    
                selected.append(module)
                used_indices.add(i)
                
        return selected
        
    def analyze_module_coverage(
        self, 
        selected_modules: List[Dict[str, Any]], 
        topic: str
    ) -> Dict[str, Any]:
        """Analyze coverage of selected modules"""
        
        if not selected_modules:
            return {
                'total_modules': 0,
                'total_ects': 0,
                'average_topic_relevance_score': 0,
                'average_role_relevance_score': 0,
                'average_relevance_score': 0,
                'eqf_level_distribution': {},
                'keyword_coverage_percentage': 0,
                'covered_keywords': [],
                'missing_keywords': []
            }
        
        total_ects = sum(module.get('ects', 5) for module in selected_modules)
        
        # Calculate average relevance scores
        topic_scores = [module.get('topic_relevance_score', 0) for module in selected_modules]
        role_scores = [module.get('role_relevance_score', 0) for module in selected_modules]
        total_scores = [module.get('total_relevance_score', 0) for module in selected_modules]
        
        avg_topic_relevance = sum(topic_scores) / len(topic_scores) if topic_scores else 0
        avg_role_relevance = sum(role_scores) / len(role_scores) if role_scores else 0
        avg_total_relevance = sum(total_scores) / len(total_scores) if total_scores else 0
        
        # Analyze EQF level distribution
        eqf_levels = [module.get('eqf_level', 6) for module in selected_modules]
        eqf_distribution = {}
        for level in eqf_levels:
            eqf_distribution[level] = eqf_distribution.get(level, 0) + 1
            
        # Analyze topic coverage
        topic_keywords = set(self.domain_knowledge.get_topic_keywords(topic))
        covered_keywords = set()
        
        for module in selected_modules:
            module_keywords = module.get('keywords', [])
            if isinstance(module_keywords, str):
                module_keywords = [kw.strip() for kw in module_keywords.split(',')]
            for keyword in module_keywords:
                if keyword.lower() in [tk.lower() for tk in topic_keywords]:
                    covered_keywords.add(keyword.lower())
                    
        keyword_coverage = len(covered_keywords) / len(topic_keywords) if topic_keywords else 0
        
        return {
            'total_modules': len(selected_modules),
            'total_ects': total_ects,
            'average_topic_relevance_score': avg_topic_relevance,
            'average_role_relevance_score': avg_role_relevance,
            'average_relevance_score': avg_total_relevance,
            'eqf_level_distribution': eqf_distribution,
            'keyword_coverage_percentage': keyword_coverage * 100,
            'covered_keywords': list(covered_keywords),
            'missing_keywords': [kw for kw in topic_keywords if kw.lower() not in covered_keywords]
        }
        
    def get_prerequisite_chain(self, modules: List[Dict[str, Any]]) -> List[str]:
        """Analyze prerequisite relationships between modules"""
        prerequisites = []
        
        for module in modules:
            if not isinstance(module, dict):
                continue
                
            module_prereqs = module.get('prerequisites', [])
            if isinstance(module_prereqs, str):
                module_prereqs = [module_prereqs]
                
            for prereq in module_prereqs:
                if prereq and prereq not in prerequisites:
                    prerequisites.append(prereq)
                    
        return prerequisites
        
    def suggest_additional_modules(
        self, 
        selected_modules: List[Dict[str, Any]], 
        all_modules: List[Dict[str, Any]], 
        topic: str,
        role_id: str = None,
        max_suggestions: int = 5
    ) -> List[Dict[str, Any]]:
        """Suggest additional modules that complement the selection"""
        
        if not selected_modules or not all_modules:
            return []
            
        selected_titles = {module.get('title', '') for module in selected_modules}
        
        # Get related topics
        related_topics = self.domain_knowledge.get_related_topics(topic)
        
        # Get role skills for additional context
        role_skills = []
        if self.role_manager and role_id:
            try:
                role_skills = self.role_manager.get_role_skills(role_id)
            except:
                role_skills = []
        
        suggestions = []
        
        for module in all_modules:
            if not isinstance(module, dict):
                continue
                
            if module.get('title', '') in selected_titles:
                continue
                
            try:
                # Check if module covers related topics
                relevance_to_related = 0
                for related_topic in related_topics:
                    relevance_to_related += self.domain_knowledge.score_module_relevance(module, related_topic)
                
                # Check if module aligns with role skills
                role_skill_relevance = 0
                if role_skills:
                    module_text = (module.get('title', '') + ' ' + 
                                 module.get('description', '') + ' ' +
                                 ' '.join(module.get('keywords', []))).lower()
                    
                    for skill in role_skills:
                        skill_words = str(skill).replace('_', ' ').split()
                        skill_matches = sum(1 for word in skill_words if word in module_text)
                        role_skill_relevance += skill_matches
                    
                total_relevance = relevance_to_related + role_skill_relevance
                
                if total_relevance > 0:
                    suggestion = module.copy()
                    suggestion['relevance_score'] = total_relevance
                    suggestion['reason'] = f"Complements {topic} and aligns with role requirements"
                    suggestions.append(suggestion)
                    
            except Exception as e:
                print(f"⚠️  Error processing suggestion for {module.get('title', 'Unknown')}: {e}")
                continue
                
        # Sort by relevance and return top suggestions
        suggestions.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return suggestions[:max_suggestions]
