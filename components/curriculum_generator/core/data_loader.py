"""
Data loading and validation for curriculum generation.
Handles loading of modules, standards, and configuration files.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class DataLoader:
    """Handles loading and validation of data files"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def load_modules(self, modules_file: str) -> List[Dict[str, Any]]:
        """Load modules from JSON file"""
        file_path = self.project_root / modules_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"Modules file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle different JSON structures
            if isinstance(data, list):
                modules = data
            elif isinstance(data, dict):
                if 'modules' in data:
                    modules = data['modules']
                elif 'data' in data:
                    modules = data['data']
                else:
                    # Assume the dict values are modules
                    modules = list(data.values())
            else:
                raise ValueError("Invalid modules file format")
                
            print(f"📊 Loaded {len(modules)} modules from {modules_file}")
            return self._validate_modules(modules)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in modules file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading modules: {e}")
            
    def _validate_modules(self, modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate module structure and add missing fields"""
        validated_modules = []
        
        for i, module in enumerate(modules):
            if not isinstance(module, dict):
                print(f"⚠️  Skipping invalid module at index {i}: not a dictionary")
                continue
            
            # Check for title field (could be 'title' or 'name')
            title = module.get('title') or module.get('name')
            if not title:
                print(f"⚠️  Skipping module at index {i}: missing 'title' or 'name' field")
                continue
            
            # Ensure required fields exist with defaults
            validated_module = {
                'title': title,  # Standardize to 'title'
                'name': title,   # Keep original 'name' for compatibility
                'id': module.get('id', f'M{i+1}'),
                'description': module.get('description', ''),
                'extended_description': module.get('extended_description', ''),
                'keywords': module.get('keywords', module.get('skills', [])),
                'learning_outcomes': module.get('learning_outcomes', {}),
                'ects': module.get('ects_points', module.get('ects', 5)),
                'eqf_level': module.get('eqf_level', 6),
                'duration_weeks': module.get('duration_weeks', 1),
                'prerequisites': module.get('prerequisites', []),
                'assessment_methods': module.get('assessment_methods', []),
                'competencies': module.get('competencies', {}),
                'topics': module.get('topics', []),
                'complexity': module.get('complexity', 'intermediate'),
                'thematic_area': module.get('thematic_area', 'General'),
                'delivery_methods': module.get('delivery_methods', ['online']),
                'module_type': module.get('module_type', ['theoretical']),
                'skills': module.get('skills', []),
                'role_relevance': module.get('role_relevance', {}),
                'is_work_based': module.get('is_work_based', False),
                'micro_credentials': module.get('micro_credentials', {}),
                'institutional_framework': module.get('institutional_framework', {}),
                'quality_assurance': module.get('quality_assurance', {})
            }
            
            # Normalize keywords to list of strings
            if isinstance(validated_module['keywords'], str):
                validated_module['keywords'] = [
                    kw.strip() for kw in validated_module['keywords'].split(',') if kw.strip()
                ]
            
            # Ensure keywords is a list
            if not isinstance(validated_module['keywords'], list):
                validated_module['keywords'] = []
                
            # Add skills to keywords for better matching
            skills = validated_module.get('skills', [])
            if isinstance(skills, list):
                validated_module['keywords'].extend(skills)
            
            # Normalize learning outcomes
            learning_outcomes = validated_module['learning_outcomes']
            if isinstance(learning_outcomes, dict):
                # Convert dict format to list
                outcomes_list = []
                for key, value in learning_outcomes.items():
                    if value:
                        outcomes_list.append(f"{key.title()}: {value}")
                validated_module['learning_outcomes'] = outcomes_list
            elif isinstance(learning_outcomes, str):
                validated_module['learning_outcomes'] = [learning_outcomes]
            elif not isinstance(learning_outcomes, list):
                validated_module['learning_outcomes'] = []
            
            validated_modules.append(validated_module)
            
        print(f"✅ Validated {len(validated_modules)} modules")
        return validated_modules
        
    def load_standards(self, standards_file: str) -> Dict[str, Any]:
        """Load educational standards"""
        file_path = self.project_root / standards_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"Standards file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in standards file: {e}")
            
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration file"""
        file_path = self.project_root / config_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
            
    def save_json(self, data: Dict[str, Any], file_path: str) -> None:
        """Save data to JSON file"""
        full_path = self.project_root / file_path
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error saving JSON file: {e}")
