#!/usr/bin/env python3
# scripts/curriculum_generator/content_specificity_engine.py

"""
Content Specificity Engine - Fixed Module Database Path
Addresses D2.1 curriculum generation problems with corrected module mappings
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import logging

class ContentSpecificityEngine:
    """Enhanced content specificity engine with corrected module references"""
    
    def __init__(self, modules_path: str = None):
        # Use absolute path resolution
        if modules_path is None:
            project_root = Path(__file__).parent.parent.parent
            self.modules_path = project_root / "input" / "modules" / "modules_v5.json"
        else:
            self.modules_path = Path(modules_path)
        
        self.modules = self._load_modules()
        self.role_preferences = self._initialize_role_preferences()
        self.d21_priority_modules = self._initialize_d21_modules()
        
    def _load_modules(self) -> List[Dict]:
        """Load module database with proper path resolution"""
        try:
            if self.modules_path.exists():
                with open(self.modules_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ Loaded {len(data)} modules from {self.modules_path}")
                return data
            else:
                print(f"❌ Module database not found at {self.modules_path}")
                return []
        except Exception as e:
            print(f"⚠️  Error loading modules: {e}")
            return []
    
    def _initialize_role_preferences(self) -> Dict[str, List[str]]:
        """Initialize content preferences for each role"""
        return {
            "DSL": ["management", "esg_reporting", "regulatory"],
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
    
    def _initialize_d21_modules(self) -> Dict[str, List[str]]:
        """Initialize D2.1 priority modules with CORRECTED IDs"""
        return {
            "esg_reporting": ["M44", "M45", "M46"],  # Fixed: M66->M44, M67->M45, M68->M46
            "regulatory_compliance": ["M45", "M46", "M22"],  # Fixed: Uses existing modules
            "technical_implementation": ["M5", "M16", "M21"],  # Uses existing tech modules
            "data_analytics": ["M3", "M4", "M11"],  # Uses existing data modules
            "management_leadership": ["M8", "M2", "M28"],  # Uses existing mgmt modules
            "business_analysis": ["M51", "M19", "M24"]  # Uses existing analysis modules
        }
    
    def enhance_curriculum(self, curriculum: Dict, role: str, modules_used: List[Dict]) -> Dict:
        """Enhanced curriculum with content specificity engine"""
        print(f"🚀 Enhancing curriculum with specific content for {role}")
        print(f"   📦 Using {len(modules_used)} modules for content extraction")
        
        # Extract specific content based on modules
        specific_outcomes = self._extract_specific_learning_outcomes(role, curriculum, modules_used)
        specific_descriptions = self._extract_specific_content_descriptions(role, modules_used)
        specific_assessments = self._extract_specific_assessment_methods(role, curriculum, modules_used)
        
        # Analyze D2.1 gap coverage
        d21_coverage = self._analyze_d21_gap_coverage(role, modules_used)
        
        # Update curriculum with specific content
        curriculum = self._integrate_specific_content(
            curriculum, specific_outcomes, specific_descriptions, specific_assessments
        )
        
        # Add content specificity metrics
        curriculum["content_specificity"] = {
            "d21_gap_coverage_score": d21_coverage,
            "modules_used_count": len(modules_used),
            "content_extraction_success": len(specific_descriptions) > 0
        }
        
        print("✅ Content specificity enhancement complete")
        print(f"   📊 D2.1 gap coverage score: {d21_coverage}%")
        
        content_warnings = 0
        if len(specific_descriptions) < max(3, len(modules_used) * 0.5):
            content_warnings += 1
            print(f"⚠️  Content warnings issued: {content_warnings}")
        else:
            print(f"   ⚠️  Content warnings issued: {content_warnings}")
        
        return curriculum
    
    def _extract_specific_learning_outcomes(self, role: str, curriculum: Dict, modules_used: List[Dict]) -> List[str]:
        """Extract specific learning outcomes from modules"""
        eqf_level = curriculum.get("programme_specification", {}).get("eqf_level", 6)
        target_audience = curriculum.get("programme_specification", {}).get("target_audience", "students_job_seekers")
        
        print(f"🔍 Extracting specific learning outcomes for {role} (EQF {eqf_level}) - {target_audience}")
        
        outcomes = []
        for module in modules_used:
            if "learning_outcomes" in module:
                # Extract knowledge, understanding, skills outcomes
                for outcome_type, outcome_text in module["learning_outcomes"].items():
                    if outcome_text:
                        outcomes.append(f"Learner will be able to {outcome_text.lower()}")
        
        return outcomes[:10]  # Limit to top 10 outcomes
    
    def _extract_specific_content_descriptions(self, role: str, modules_used: List[Dict]) -> List[str]:
        """Extract specific content descriptions from modules"""
        print(f"📝 Extracting specific content descriptions for {role}")
        
        descriptions = []
        for module in modules_used:
            if "extended_description" in module and module["extended_description"]:
                descriptions.append(module["extended_description"])
            elif "description" in module and module["description"]:
                descriptions.append(module["description"])
        
        if len(descriptions) < max(3, len(modules_used) * 0.5):
            print(f"⚠️  CONTENT SPECIFICITY WARNING: Only {len(descriptions)} modules provided specific descriptions")
            self._generate_content_fallback_warning(role, len(modules_used))
        
        return descriptions
    
    def _generate_content_fallback_warning(self, role: str, modules_count: int):
        """Generate content improvement recommendations with CORRECTED module IDs"""
        print(f"⚠️  CONTENT FALLBACK WARNING ({role} - content_descriptions):")
        
        # Use role preferences to suggest existing modules
        preferences = self.role_preferences.get(role, [])
        
        for preference in preferences[:3]:  # Top 3 preferences
            if preference in self.d21_priority_modules:
                module_list = ", ".join(self.d21_priority_modules[preference])
                category_name = preference.replace("_", " ").title()
                
                if preference == "esg_reporting":
                    print(f"   📋 Add {preference} modules: {module_list} - ESG reporting and compliance modules for D2.1 priority gap")
                elif preference == "regulatory_compliance":
                    print(f"   📋 Add {preference} modules: {module_list} - Regulatory compliance depth modules for D2.1 priority gap")
                elif preference == "technical_implementation":
                    print(f"   📋 Add {preference} modules: {module_list} - Technical implementation granularity modules for D2.1 priority gap")
                else:
                    print(f"   📋 Add {preference} modules: {module_list} - {category_name} modules")
        
        print(f"   📋 SOLUTION: Expand module extended_description fields with technical detail")
        print(f"   📋 PRIORITY: Add regulatory compliance modules (M45, M46) for depth")
    
    def _extract_specific_assessment_methods(self, role: str, curriculum: Dict, modules_used: List[Dict]) -> List[str]:
        """Extract specific assessment methods from modules"""
        target_audience = curriculum.get("programme_specification", {}).get("target_audience", "students_job_seekers")
        print(f"📊 Extracting specific assessment methods for {role} - {target_audience}")
        
        assessments = []
        for module in modules_used:
            # Generate assessments based on module characteristics
            if module.get("is_work_based", False):
                assessments.append("Work-based project implementation")
            if module.get("module_type") == ["practical"]:
                assessments.append("Practical skills demonstration")
            if "data" in module.get("thematic_area", "").lower():
                assessments.append("Data analysis portfolio")
            if "management" in module.get("thematic_area", "").lower():
                assessments.append("Management case study")
        
        return list(set(assessments))[:5]  # Unique assessments, max 5
    
    def _analyze_d21_gap_coverage(self, role: str, modules_used: List[Dict]) -> float:
        """Analyze D2.1 gap coverage with corrected module references"""
        print(f"🔍 Analyzing D2.1 gap coverage for {role}")
        
        module_ids = [m.get("id", "") for m in modules_used]
        
        # D2.1 priority areas with corrected module IDs
        d21_gaps = {
            "esg_centrality": ["M44"],  # ESG Reporting (was M66)
            "regulatory_depth": ["M45", "M46"],  # Policy & RegTech (was M67, M68)
            "technical_granularity": ["M5", "M16", "M21"],  # Technical modules
            "assessment_specificity": ["M8"],  # Work-based module
            "industry_specialization": ["M51", "M19"]  # Business analysis
        }
        
        coverage_count = 0
        total_gaps = len(d21_gaps)
        
        for gap_area, required_modules in d21_gaps.items():
            if any(mod_id in module_ids for mod_id in required_modules):
                coverage_count += 1
        
        coverage_percentage = (coverage_count / total_gaps) * 100
        return round(coverage_percentage, 1)
    
    def _integrate_specific_content(self, curriculum: Dict, outcomes: List[str], 
                                  descriptions: List[str], assessments: List[str]) -> Dict:
        """Integrate specific content into curriculum structure"""
        
        # Enhance learning outcomes with module-specific content
        if outcomes and "section_2_learning_outcomes" in curriculum:
            curriculum["section_2_learning_outcomes"]["enhanced_outcomes"] = outcomes
        
        # Enhance programme description with module content
        if descriptions and "section_1_programme_description" in curriculum:
            curriculum["section_1_programme_description"]["module_based_content"] = descriptions
        
        # Enhance assessment methods with module-specific approaches
        if assessments and "section_7_assessment_methods" in curriculum:
            curriculum["section_7_assessment_methods"]["module_derived_methods"] = assessments
        
        return curriculum
    
    def validate_module_selection(self, selected_modules: List[Dict], target_count: int) -> Tuple[bool, List[str]]:
        """Validate module selection and provide improvement recommendations"""
        warnings = []
        
        # IMPROVED: Less conservative module count validation
        minimum_modules = max(2, min(target_count, 4))  # At least 2, but more reasonable max
        
        if len(selected_modules) < minimum_modules:
            warnings.append("CRITICAL: Very low module count may result in generic content")
            warnings.append(f"RECOMMENDATION: Increase to at least {minimum_modules} modules")
        
        # Check for D2.1 priority coverage
        module_ids = [m.get("id", "") for m in selected_modules]
        
        # Check ESG coverage with corrected IDs
        esg_modules = ["M44", "M45", "M46"]  # Corrected from M66, M67, M68
        if not any(mod_id in module_ids for mod_id in esg_modules):
            warnings.append("D2.1 GAP: Add ESG/regulatory modules (M44, M45, M46) for centrality")
        
        # Check technical coverage
        tech_modules = ["M5", "M16", "M21"]
        if not any(mod_id in module_ids for mod_id in tech_modules):
            warnings.append("D2.1 GAP: Add technical modules (M5, M16, M21) for skills granularity")
        
        is_valid = len(warnings) == 0
        return is_valid, warnings
    
    def get_role_specific_recommendations(self, role: str, current_modules: List[str]) -> List[str]:
        """Get role-specific module recommendations with corrected IDs"""
        preferences = self.role_preferences.get(role, [])
        recommendations = []
        
        for preference in preferences:
            if preference in self.d21_priority_modules:
                available_modules = self.d21_priority_modules[preference]
                # Suggest modules not already selected
                new_modules = [m for m in available_modules if m not in current_modules]
                recommendations.extend(new_modules[:2])  # Max 2 per category
        
        return recommendations[:5]  # Max 5 total recommendations
