# scripts/curriculum_generator/components/educational_profile_config_manager.py
"""
Educational Profile Configuration Manager
Handles terminology, section sequencing, and subsection toggling for educational profiles
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class EducationalProfileConfigManager:
    """Manages educational profile configuration settings"""
    
    def __init__(self, project_root: str = None):
        """Initialize the configuration manager"""
        self.project_root = project_root or os.getcwd()
        self.config = self._load_config()
        self.terminology = self.config.get("terminology", {})
        self.section_config = self.config.get("section_configuration", {})
        self.subsection_config = self.config.get("subsection_configuration", {})
        self.display_settings = self.config.get("display_settings", {})
        self.compliance_settings = self.config.get("compliance_settings", {})
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        config_paths = [
            os.path.join(self.project_root, "scripts", "curriculum_generator", "config", "educational_profile_config.json"),
            os.path.join(self.project_root, "config", "educational_profile_config.json"),
            "scripts/curriculum_generator/config/educational_profile_config.json",
            "config/educational_profile_config.json"
        ]
        
        for config_path in config_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        print(f"✅ Educational profile config loaded from: {config_path}")
                        return config
            except Exception as e:
                print(f"⚠️  Failed to load config from {config_path}: {e}")
                continue
        
        print("⚠️  No config file found, using default settings")
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Provide default configuration if file not found"""
        return {
            "terminology": {
                "competencies_and_learning_outcomes": "Competences",
                "what_you_learn": "Target Learning Outcomes"
            },
            "section_configuration": {
                "enabled_sections": {},
                "section_sequence": []
            },
            "subsection_configuration": {},
            "display_settings": {
                "show_section_numbers": True,
                "use_emoji_icons": True
            },
            "compliance_settings": {
                "enforce_t32_sections": True,
                "enforce_t34_sections": True
            }
        }
    
    def replace_terminology(self, text: str) -> str:
        """Replace terminology in text according to configuration"""
        if not text:
            return text
        
        # Apply terminology replacements
        for old_term, new_term in self.terminology.items():
            # Handle specific phrases with emoji
            if old_term == "what_you_learn":
                text = text.replace("🎯 What You'll Learn", new_term)
                text = text.replace("What You'll Learn", new_term)
            elif old_term == "competencies_and_learning_outcomes":
                text = text.replace("Competencies & Learning Outcomes", new_term)
                text = text.replace("Competencies and Learning Outcomes", new_term)
            else:
                # Case-insensitive replacement for other terms
                import re
                pattern = re.compile(re.escape(old_term), re.IGNORECASE)
                text = pattern.sub(new_term, text)
        
        return text
    
    def is_section_enabled(self, section_name: str) -> bool:
        """Check if a section is enabled"""
        enabled_sections = self.section_config.get("enabled_sections", {})
        return enabled_sections.get(section_name, True)  # Default to enabled
    
    def is_subsection_enabled(self, section_name: str, subsection_name: str) -> bool:
        """Check if a subsection is enabled"""
        section_subsections = self.subsection_config.get(section_name, {})
        enabled_subsections = section_subsections.get("enabled_subsections", {})
        return enabled_subsections.get(subsection_name, True)  # Default to enabled
    
    def get_section_sequence(self) -> List[str]:
        """Get the configured section sequence"""
        return self.section_config.get("section_sequence", [])
    
    def get_subsection_sequence(self, section_name: str) -> List[str]:
        """Get the configured subsection sequence for a given section"""
        section_subsections = self.subsection_config.get(section_name, {})
        return section_subsections.get("subsection_sequence", [])
    
    def filter_sections_by_config(self, sections_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Filter sections dictionary based on configuration"""
        filtered_sections = {}
        
        # Get the configured sequence
        section_sequence = self.get_section_sequence()
        
        # If no sequence configured, use original order
        if not section_sequence:
            section_sequence = list(sections_dict.keys())
        
        # Add sections in configured order if they exist and are enabled
        for section_name in section_sequence:
            if section_name in sections_dict and self.is_section_enabled(section_name):
                # Filter subsections within each section
                section_data = sections_dict[section_name]
                if isinstance(section_data, dict):
                    filtered_section_data = self.filter_subsections_by_config(section_name, section_data)
                    filtered_sections[section_name] = filtered_section_data
                else:
                    filtered_sections[section_name] = section_data
        
        return filtered_sections
    
    def filter_subsections_by_config(self, section_name: str, section_data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter subsections within a section based on configuration"""
        filtered_data = {}
        
        # Get the configured subsection sequence
        subsection_sequence = self.get_subsection_sequence(section_name)
        
        # If no sequence configured, use original order
        if not subsection_sequence:
            subsection_sequence = list(section_data.keys())
        
        # Add subsections in configured order if they exist and are enabled
        for subsection_name in subsection_sequence:
            if (subsection_name in section_data and 
                self.is_subsection_enabled(section_name, subsection_name)):
                filtered_data[subsection_name] = section_data[subsection_name]
        
        return filtered_data
    
    def apply_display_formatting(self, section_title: str, section_number: int = None) -> str:
        """Apply display formatting to section titles"""
        formatted_title = self.replace_terminology(section_title)
        
        # Add section numbers if enabled
        if self.display_settings.get("show_section_numbers", True) and section_number:
            formatted_title = f"{section_number}. {formatted_title}"
        
        return formatted_title
    
    def get_compliance_requirements(self) -> Dict[str, bool]:
        """Get compliance requirements from configuration"""
        return {
            "t32_compliance": self.compliance_settings.get("enforce_t32_sections", True),
            "t34_compliance": self.compliance_settings.get("enforce_t34_sections", True),
            "audience_differentiation": self.compliance_settings.get("require_audience_differentiation", True),
            "tuning_methodology": self.compliance_settings.get("require_tuning_methodology", True)
        }
    
    def validate_curriculum_sections(self, curriculum_sections: Dict[str, Any]) -> List[str]:
        """Validate curriculum sections against configuration requirements"""
        warnings = []
        compliance = self.get_compliance_requirements()
        
        # Check T3.2 compliance requirements
        if compliance["t32_compliance"]:
            required_t32_sections = ["target_learning_outcomes", "delivery_methodologies", "course_organization"]
            for section in required_t32_sections:
                if section not in curriculum_sections:
                    warnings.append(f"T3.2 COMPLIANCE: Missing required section '{section}'")
        
        # Check T3.4 compliance requirements  
        if compliance["t34_compliance"]:
            required_t34_sections = ["qualification_recognition", "assessment_methods"]
            for section in required_t34_sections:
                if section not in curriculum_sections:
                    warnings.append(f"T3.4 COMPLIANCE: Missing required section '{section}'")
        
        # Check audience differentiation
        if compliance["audience_differentiation"]:
            target_outcomes = curriculum_sections.get("target_learning_outcomes", {})
            if "differentiation_evidence" not in target_outcomes:
                warnings.append("AUDIENCE DIFFERENTIATION: Missing differentiation evidence")
        
        return warnings
    
    def update_configuration(self, config_updates: Dict[str, Any]) -> bool:
        """Update configuration settings"""
        try:
            # Deep merge the updates into current config
            def deep_merge(base_dict, update_dict):
                for key, value in update_dict.items():
                    if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                        deep_merge(base_dict[key], value)
                    else:
                        base_dict[key] = value
            
            deep_merge(self.config, config_updates)
            
            # Reload instance variables
            self.terminology = self.config.get("terminology", {})
            self.section_config = self.config.get("section_configuration", {})
            self.subsection_config = self.config.get("subsection_configuration", {})
            self.display_settings = self.config.get("display_settings", {})
            self.compliance_settings = self.config.get("compliance_settings", {})
            
            return True
        except Exception as e:
            print(f"❌ Failed to update configuration: {e}")
            return False
    
    def export_config_summary(self) -> Dict[str, Any]:
        """Export a summary of current configuration settings"""
        return {
            "terminology_replacements": len(self.terminology),
            "enabled_sections": sum(1 for enabled in self.section_config.get("enabled_sections", {}).values() if enabled),
            "total_sections": len(self.section_config.get("enabled_sections", {})),
            "section_sequence_length": len(self.get_section_sequence()),
            "compliance_enforced": self.get_compliance_requirements(),
            "display_formatting": self.display_settings
        }
