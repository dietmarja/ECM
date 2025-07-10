# scripts/curriculum_generator/domain/role_manager.py
"""
Enhanced Role Manager with T3.2 & T3.4 compliance.
Manages professional roles and generates educational profiles.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class RoleManager:
    """Enhanced role manager for T3.2/T3.4 compliance"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.roles = {}
        self.role_types = {
            'RIC': 'Role in Context',
            'RIP': 'Role in Practice', 
            'RIS': 'Role in Strategy'
        }
        self._load_roles()
    
    def _load_roles(self):
        """Load roles from roles.json"""
        roles_file = self.project_root / "input" / "roles" / "roles.json"
        
        try:
            with open(roles_file, 'r', encoding='utf-8') as f:
                roles_data = json.load(f)
            
            for role in roles_data:
                self.roles[role['id']] = role
                
            print(f"✅ Loaded {len(self.roles)} role definitions")
            
        except FileNotFoundError:
            print(f"⚠️  Roles file not found: {roles_file}")
            self.roles = {}
        except Exception as e:
            print(f"❌ Error loading roles: {e}")
            self.roles = {}
    
    def get_role(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Get role definition by ID"""
        return self.roles.get(role_id)
    
    def get_all_roles(self) -> Dict[str, Dict[str, Any]]:
        """Get all role definitions"""
        return self.roles
    
    def validate_role_id(self, role_id: str) -> bool:
        """Validate if role ID exists"""
        return role_id in self.roles
    
    def get_role_description(self, role_id: str) -> str:
        """Get formatted role description"""
        role = self.get_role(role_id)
        if role:
            return f"{role['name']} - {role['description']}"
        return f"Unknown role: {role_id}"
    
    def get_default_ects_for_role(self, role_id: str, eqf_level: int) -> int:
        """Get default ECTS for role at specific EQF level"""
        role = self.get_role(role_id)
        if not role:
            return 60
        
        default_ects = role.get('default_ects', {})
        if isinstance(default_ects, dict):
            return default_ects.get(str(eqf_level), 60)
        return default_ects if isinstance(default_ects, int) else 60
    
    def get_roles_for_eqf_level(self, eqf_level: int) -> List[Dict[str, Any]]:
        """Get roles compatible with EQF level"""
        compatible_roles = []
        
        for role in self.roles.values():
            if eqf_level in role.get('eqf_levels', []):
                compatible_roles.append(role)
        
        return compatible_roles
    
    def supports_work_based_learning(self, role_id: str, eqf_level: int) -> bool:
        """Check if role supports work-based learning at EQF level"""
        role = self.get_role(role_id)
        if not role:
            return False
        
        wbl_components = role.get('work_based_components', {})
        return wbl_components.get(str(eqf_level), False)
    
    def is_dual_principle_applicable(self, role_id: str) -> bool:
        """Check if dual principle is applicable for role"""
        role = self.get_role(role_id)
        if not role:
            return False
        
        return role.get('dual_principle_applicable', False)
    
    def get_role_module_relevance(self, role_id: str, module_id: str) -> int:
        """Get module relevance score for role (0-100)"""
        role = self.get_role(role_id)
        if not role:
            return 0
        
        related_modules = role.get('related_modules', {})
        return related_modules.get(module_id, 0)