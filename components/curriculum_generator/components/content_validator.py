#!/usr/bin/env python3
# scripts/curriculum_generator/components/content_validator.py
"""
Content Validator - Stops system when generic content is detected
Forces use of rich module database content
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

class ContentValidator:
    """Validates curriculum content and stops on generic fallbacks"""
    
    def __init__(self):
        self.module_database = self._load_module_database()
        self.generic_patterns = [
            'Foundation Module',
            'Application Module', 
            'Integration Module',
            'Core sustainability concepts',
            'Practical applications',
            'Integrated competencies',
            'Foundation Certificate',
            'Application Certificate',
            'Integration Certificate'
        ]
        
    def _load_module_database(self) -> Dict:
        """Load the rich module database"""
        module_paths = [
            "DSCG/input/modules/modules_v5.json",
            "input/modules/modules_v5.json", 
            "data/modules/modules_v5_full.json"
        ]
        
        for path in module_paths:
            if Path(path).exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                    # Handle both list and dict formats
                    if isinstance(data, list):
                        # Convert list to dict using id as key
                        modules = {}
                        for module in data:
                            if isinstance(module, dict) and "id" in module:
                                modules[module["id"]] = module
                        print(f"✅ Loaded {len(modules)} modules from {path} (list format)")
                        return modules
                    elif isinstance(data, dict):
                        print(f"✅ Loaded {len(data)} modules from {path} (dict format)")
                        return data
                    else:
                        print(f"⚠️ Unknown format in {path}")
                        continue
                        
                except Exception as e:
                    print(f"⚠️ Error loading {path}: {e}")
                    continue
        
        print("❌ CRITICAL: No module database found!")
        return {}
    
    def validate_curriculum_content(self, curriculum_text: str, role_id: str, 
                                  selected_modules: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate curriculum content and detect generic fallbacks"""
        
        print(f"\n🔍 VALIDATING CURRICULUM CONTENT FOR {role_id}")
        print("=" * 60)
        
        errors = []
        
        # Check 1: Generic content detection
        generic_found = []
        for pattern in self.generic_patterns:
            if pattern in curriculum_text:
                generic_found.append(pattern)
        
        if generic_found:
            errors.append(f"GENERIC CONTENT DETECTED: {', '.join(generic_found)}")
            print(f"❌ STOP: Generic content found: {generic_found}")
        
        # Check 2: Required sections validation
        required_sections = [
            '1. 🎯 Programme Learning Outcomes',
            '2. 📚 Modular Structure', 
            '3. 📝 Assessment Strategy',
            '4. 🌐 Framework Mapping',
            '5. 🧩 Stackability & Micro-Credentialing',
            '6. 🧪 Work-Based Integration',
            '7. 👥 Target Audiences',
            '8. 🛠 Support & QA'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in curriculum_text:
                missing_sections.append(section)
        
        if missing_sections:
            errors.append(f"MISSING SECTIONS: {', '.join(missing_sections)}")
            print(f"❌ STOP: Missing sections: {missing_sections}")
        
        # Check 3: Role-specific content validation
        role_specific_content = {
            'DAN': ['ESG Data Standards', 'Sustainability Data Practices', 'Reporting & Communication'],
            'DSE': ['Green Data Architecture', 'Sustainable Data Pipeline', 'Energy-Efficient'],
            'DSL': ['Strategic Sustainability Leadership', 'Organizational Transformation', 'Executive Stakeholder'],
            'DSM': ['Sustainability Program Management', 'Cross-Functional', 'Performance Monitoring'],
            'DSC': ['Sustainability Assessment', 'Client Engagement', 'Strategic Sustainability Solution'],
            'DSI': ['AI & Machine Learning', 'Predictive Sustainability', 'Data Science Applications'],
            'SBA': ['Business Process Sustainability', 'Sustainability Metrics', 'Business Case Development'],
            'SDD': ['Green Coding Practices', 'Sustainable Software Architecture', 'Energy-Efficient Development'],
            'SSD': ['Sustainable System Design', 'Circular Design Methodologies', 'Eco-Design Implementation'],
            'STS': ['Sustainability Platform Configuration', 'Technical Tool Implementation', 'System Integration']
        }
        
        expected_content = role_specific_content.get(role_id, [])
        found_content = []
        for content in expected_content:
            if content in curriculum_text:
                found_content.append(content)
        
        if len(found_content) < len(expected_content) / 2:  # Less than 50% found
            errors.append(f"INSUFFICIENT ROLE-SPECIFIC CONTENT: Expected {expected_content}, found {found_content}")
            print(f"❌ STOP: Missing role-specific content for {role_id}")
        
        # Check 4: Module database usage validation
        if not self.module_database:
            errors.append("MODULE DATABASE NOT LOADED")
            print("❌ STOP: Module database not available")
        elif not selected_modules:
            errors.append("NO MODULES SELECTED FROM DATABASE")
            print("❌ STOP: No modules selected from rich database")
        else:
            # Check if selected modules are being used
            module_names_in_text = 0
            for module in selected_modules:
                module_name = module.get('name', '')
                if module_name and module_name in curriculum_text:
                    module_names_in_text += 1
            
            if module_names_in_text == 0:
                errors.append("SELECTED MODULES NOT USED IN CURRICULUM TEXT")
                print(f"❌ STOP: {len(selected_modules)} modules selected but none used in text")
        
        # Summary
        if errors:
            print(f"\n❌ VALIDATION FAILED - {len(errors)} CRITICAL ERRORS:")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
            
            print(f"\n🔧 REQUIRED FIXES:")
            print(f"   • Use rich content from {len(self.module_database)} modules in database")
            print(f"   • Generate role-specific modules for {role_id}")
            print(f"   • Include all 8 required sections")
            print(f"   • Eliminate generic fallback content")
            
            return False, errors
        else:
            print("✅ CONTENT VALIDATION PASSED")
            return True, []
    
    def get_role_specific_modules(self, role_id: str, num_modules: int = 3) -> List[Dict]:
        """Get actual role-specific modules from database"""
        
        if not self.module_database:
            print("❌ Cannot get modules - database not loaded")
            return []
        
        # Find modules relevant to the role
        relevant_modules = []
        
        # Load roles.json to get role preferences
        try:
            with open('roles.json', 'r') as f:
                roles_data = {role['id']: role for role in json.load(f)}
            
            role_info = roles_data.get(role_id, {})
            related_modules = role_info.get('related_modules', {})
            
            # Get modules with high relevance scores
            for module_id, relevance in related_modules.items():
                if module_id in self.module_database and relevance >= 80:
                    module = self.module_database[module_id].copy()
                    module['relevance_score'] = relevance
                    relevant_modules.append(module)
            
            # Sort by relevance and take top modules
            relevant_modules.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            selected = relevant_modules[:num_modules]
            
            print(f"✅ Selected {len(selected)} high-relevance modules for {role_id}")
            for module in selected:
                print(f"   • {module.get('name', 'Unknown')} (relevance: {module.get('relevance_score', 0)}%)")
            
            return selected
            
        except Exception as e:
            print(f"❌ Error selecting modules: {e}")
            return []
    
    def explain_generic_fallback(self, curriculum_text: str, role_id: str) -> str:
        """Explain why system fell back to generic content"""
        
        explanations = []
        
        # Check what went wrong
        if any(pattern in curriculum_text for pattern in self.generic_patterns):
            explanations.append("⚠️ GENERIC CONTENT FALLBACK DETECTED")
            explanations.append("")
            
            explanations.append("ROOT CAUSES:")
            
            if not self.module_database:
                explanations.append("❌ Module database (modules_v5.json) not loaded")
                explanations.append("   → Check file exists at: DSCG/input/modules/modules_v5.json")
            
            try:
                with open('roles.json', 'r') as f:
                    roles_data = json.load(f)
                    role_info = next((r for r in roles_data if r['id'] == role_id), None)
                    
                    if not role_info:
                        explanations.append(f"❌ Role {role_id} not found in roles.json")
                    elif not role_info.get('related_modules'):
                        explanations.append(f"❌ No related_modules defined for {role_id}")
                    else:
                        explanations.append(f"✅ Role {role_id} has {len(role_info['related_modules'])} related modules")
                        
            except Exception as e:
                explanations.append(f"❌ Error loading roles.json: {e}")
            
            explanations.append("")
            explanations.append("SOLUTION:")
            explanations.append("1. Ensure modules_v5.json is loaded with rich content")
            explanations.append("2. Use module selector to pick relevant modules")
            explanations.append("3. Generate role-specific module names and content")
            explanations.append("4. Include all 8 curriculum sections")
        
        return "\n".join(explanations)
