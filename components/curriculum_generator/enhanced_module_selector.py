#!/usr/bin/env python3
# scripts/curriculum_generator/enhanced_module_selector.py

"""
Enhanced Module Selector - Fixed Conservative Selection Logic
Layer 1: Dynamic module selection based on ECTS requirements with improved algorithms
"""

import json
import os
import random
from typing import Dict, List, Tuple, Any, Optional
import logging

class EnhancedModuleSelector:
    """Enhanced module selector with improved logic for small curricula"""
    
    def __init__(self, modules_path: str = "input/modules/modules_v5.json"):
        self.modules_path = modules_path
        self.modules = self._load_modules()
        self.role_preferences = self._initialize_role_preferences()
        
    def _load_modules(self) -> List[Dict]:
        """Load module database"""
        try:
            if os.path.exists(self.modules_path):
                with open(self.modules_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Fallback to alternative paths
                fallback_paths = [
                    "input/modules/modules_v5.json"
                ]
                for path in fallback_paths:
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            return json.load(f)
                print(f"⚠️  enhanced_module_selector.py: Module database not found at {self.modules_path}")
                return []
        except Exception as e:
            print(f"⚠️  Error loading modules: {e}")
            return []
    
    def _initialize_role_preferences(self) -> Dict[str, List[str]]:
        """Initialize content preferences for each role"""
        return {
            "DSL": ["esg_reporting", "regulatory", "management"],
            "DSM": ["management", "regulatory", "esg_reporting"], 
            "DSC": ["business_analysis", "regulatory", "esg_reporting"],
            "SBA": ["business_analysis", "data_analytics", "esg_reporting"],
            "SDD": ["technical_implementation", "software_development"],
            "SSD": ["technical_implementation", "systems_design"],
            "DAN": ["data_analytics", "esg_reporting"],
            "DSI": ["technical_implementation", "data_analytics"],
            "DSE": ["technical_implementation", "data_analytics"],
            "STS": ["technical_implementation", "systems_design"]
        }
    
    def select_modules(self, role: str, topic: str, eqf_level: int, ects: float, 
                      uol_count: int, **kwargs) -> Tuple[List[Dict], float]:
        """Enhanced module selection with improved logic for small curricula"""
        
        print(f"🔍 Enhanced module selection for {role} | Topic: {topic} | EQF: {eqf_level} | ECTS: {ects}")
        
        # IMPROVED: More generous module count calculation
        target_modules = self._calculate_improved_module_count(ects, uol_count)
        print(f"   📊 Module count calculation: {ects} ECTS → {target_modules} modules (improved)")
        
        # Get content preferences for role
        preferences = self.role_preferences.get(role, ["general"])
        print(f"   📋 Content preferences: {', '.join(preferences)}")
        print(f"   🎯 Target modules: {target_modules}")
        
        # Filter and score modules
        candidate_modules = self._filter_and_score_modules(role, preferences, eqf_level, topic)
        
        # Select best modules
        selected_modules = self._select_best_modules(candidate_modules, target_modules, preferences)
        
        if not selected_modules:
            print("   ⚠️  No modules selected, using fallback selection")
            selected_modules = self._fallback_module_selection(eqf_level)
        
        # Calculate role alignment
        role_alignment = self._calculate_role_alignment(selected_modules, role)
        
        print(f"   ✅ Selected {len(selected_modules)} unique modules (target: {target_modules})")
        
        # Display selected modules with details
        for i, module in enumerate(selected_modules[:5], 1):
            categories = self._get_module_categories(module)
            score = module.get('selection_score', 0.0)
            print(f"   📦 {i}. {module.get('id', 'Unknown')}: {module.get('name', 'Unknown')} (Score: {score:.2f}, Categories: {categories})")
        
        # Generate warnings and recommendations
        warnings = self._generate_improved_warnings(selected_modules, target_modules, preferences)
        
        print(f"🔧 Enhanced curriculum with smart module selection:")
        print(f"   📦 {len(selected_modules)} unique modules selected")
        print(f"   🎯 Role alignment: {role_alignment:.1f}%")
        
        if warnings:
            print(f"   ⚠️  SELECTION WARNINGS:")
            for warning in warnings:
                print(f"      • {warning}")
        
        recommendations = self._generate_recommendations(selected_modules, preferences, role)
        if recommendations:
            print(f"   📋 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"      • {rec}")
        
        return selected_modules, {
            'role_alignment': role_alignment,
            'target_count': target_modules,
            'selection_success': len(selected_modules) > 0
        }
    
    def _calculate_improved_module_count(self, ects: float, uol_count: int) -> int:
        """Calculate module count with improved logic for small curricula"""
        
        # Base calculation: More generous for small ECTS
        if ects <= 1.0:
            base_count = 3  # Minimum 3 modules for very small curricula
        elif ects <= 2.5:
            base_count = 4  # 4 modules for small curricula
        elif ects <= 5.0:
            base_count = 5  # 5 modules for medium curricula
        else:
            base_count = max(4, int(ects / 5.0))  # Standard calculation for larger curricula
        
        # Adjust based on units of learning
        if uol_count >= 3:
            adjusted_count = max(base_count, uol_count)  # At least one module per unit
        else:
            adjusted_count = base_count
        
        # Ensure reasonable bounds
        final_count = max(3, min(adjusted_count, 15))  # Between 3-15 modules
        
        return final_count
    
    def _filter_and_score_modules(self, role: str, preferences: List[str], 
                                eqf_level: int, topic: str) -> List[Dict]:
        """Filter modules and assign relevance scores"""
        
        candidate_modules = []
        
        for module in self.modules:
            if not module.get('id') or not module.get('name'):
                continue
                
            # Calculate relevance score
            score = self._calculate_module_relevance(module, role, preferences, eqf_level, topic)
            
            if score > 0.3:  # Lower threshold to include more modules
                module_copy = module.copy()
                module_copy['selection_score'] = score
                candidate_modules.append(module_copy)
        
        # Sort by relevance score
        candidate_modules.sort(key=lambda x: x['selection_score'], reverse=True)
        
        return candidate_modules
    
    def _calculate_module_relevance(self, module: Dict, role: str, preferences: List[str], 
                                  eqf_level: int, topic: str) -> float:
        """Calculate module relevance score"""
        score = 0.0
        
        # Role relevance (if available)
        if 'role_relevance' in module and role in module['role_relevance']:
            score += module['role_relevance'][role] / 100.0 * 0.4
        else:
            score += 0.2  # Default score if no role relevance data
        
        # EQF level compatibility
        module_eqf = module.get('eqf_level', 6)
        if module_eqf == eqf_level:
            score += 0.3
        elif abs(module_eqf - eqf_level) == 1:
            score += 0.2
        else:
            score += 0.1
        
        # Content preference matching
        module_categories = self._get_module_categories(module)
        preference_match = len(set(preferences) & set(module_categories)) / max(len(preferences), 1)
        score += preference_match * 0.3
        
        return min(score, 1.0)
    
    def _get_module_categories(self, module: Dict) -> List[str]:
        """Extract categories from module based on thematic area and content"""
        categories = []
        
        thematic_area = module.get('thematic_area', '').lower()
        name = module.get('name', '').lower()
        description = module.get('description', '').lower()
        
        # Map thematic areas to categories
        if 'data' in thematic_area:
            categories.append('data_analytics')
        if 'management' in thematic_area:
            categories.append('management')
        if 'technical' in thematic_area:
            categories.append('technical_implementation')
        if 'software' in thematic_area:
            categories.append('software_development')
        if 'analysis' in thematic_area:
            categories.append('business_analysis')
        if 'ethics' in thematic_area or 'governance' in thematic_area:
            categories.append('regulatory')
        
        # Content-based categorization
        if any(term in name + description for term in ['esg', 'reporting', 'compliance']):
            categories.append('esg_reporting')
        if any(term in name + description for term in ['policy', 'regulation', 'legislation']):
            categories.append('regulatory')
        if any(term in name + description for term in ['data', 'analytics', 'visualization']):
            categories.append('data_analytics')
        if any(term in name + description for term in ['business', 'economic', 'finance']):
            categories.append('business_analysis')
        if any(term in name + description for term in ['software', 'development', 'coding']):
            categories.append('technical_implementation')
        
        return list(set(categories)) if categories else ['general']
    
    def _select_best_modules(self, candidates: List[Dict], target_count: int, 
                           preferences: List[str]) -> List[Dict]:
        """Select best modules ensuring diversity and preference coverage"""
        
        if not candidates:
            return []
        
        selected = []
        used_ids = set()
        
        # First pass: Select top modules for each preference
        for preference in preferences:
            pref_modules = [m for m in candidates 
                          if preference in self._get_module_categories(m) 
                          and m.get('id') not in used_ids]
            
            if pref_modules:
                selected.append(pref_modules[0])
                used_ids.add(pref_modules[0].get('id'))
                
                if len(selected) >= target_count:
                    break
        
        # Second pass: Fill remaining slots with highest scoring modules
        remaining_candidates = [m for m in candidates if m.get('id') not in used_ids]
        
        for module in remaining_candidates:
            if len(selected) >= target_count:
                break
            selected.append(module)
            used_ids.add(module.get('id'))
        
        return selected[:target_count]
    
    def _generate_improved_warnings(self, selected_modules: List[Dict], 
                                  target_count: int, preferences: List[str]) -> List[str]:
        """Generate improved warnings with better thresholds"""
        warnings = []
        
        # IMPROVED: Less aggressive warning thresholds
        if len(selected_modules) < 3:  # Only warn if less than 3 modules
            warnings.append("LOW: Module count may limit content specificity")
        
        # Check preference coverage
        selected_categories = set()
        for module in selected_modules:
            selected_categories.update(self._get_module_categories(module))
        
        missing_preferences = set(preferences) - selected_categories
        if len(missing_preferences) > 1:  # Allow one missing preference
            warnings.append(f"COVERAGE: Missing categories: {', '.join(missing_preferences)}")
        
        return warnings
    
    def _generate_recommendations(self, selected_modules: List[Dict], 
                                preferences: List[str], role: str) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        # Check for D2.1 gaps
        selected_categories = set()
        for module in selected_modules:
            selected_categories.update(self._get_module_categories(module))
        
        # ESG/Regulatory gap check
        if 'esg_reporting' not in selected_categories:
            recommendations.append("Add ESG reporting modules for D2.1 compliance centrality")
        
        # Technical gap check  
        if role in ['SDD', 'SSD', 'DSE'] and 'technical_implementation' not in selected_categories:
            recommendations.append("Add technical implementation modules for skills granularity")
        
        # Data analytics gap check
        if role in ['DAN', 'DSI'] and 'data_analytics' not in selected_categories:
            recommendations.append("Add data analytics modules for specialization depth")
        
        return recommendations
    
    def _calculate_role_alignment(self, modules: List[Dict], role: str) -> float:
        """Calculate role alignment percentage"""
        if not modules:
            return 0.0
        
        total_relevance = 0.0
        count = 0
        
        for module in modules:
            if 'role_relevance' in module and role in module['role_relevance']:
                total_relevance += module['role_relevance'][role]
                count += 1
            else:
                total_relevance += 50  # Default relevance if not specified
                count += 1
        
        return (total_relevance / count) if count > 0 else 50.0
    
    def _fallback_module_selection(self, eqf_level: int) -> List[Dict]:
        """Fallback selection when no modules match criteria"""
        fallback_modules = []
        
        # Select modules close to the target EQF level
        for module in self.modules:
            if not module.get('id'):
                continue
                
            module_eqf = module.get('eqf_level', 6)
            if abs(module_eqf - eqf_level) <= 1:
                fallback_modules.append(module)
                
            if len(fallback_modules) >= 3:
                break
        
        return fallback_modules
