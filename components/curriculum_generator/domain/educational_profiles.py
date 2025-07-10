#!/usr/bin/env python3
# scripts/curriculum_generator/domain/educational_profiles.py
"""
Enhanced Educational Profiles Manager - T3.2/T3.4 Compliant
Generates comprehensive educational profiles with learner-focused information
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class EnhancedEducationalProfilesManager:
    """Manages creation of T3.2/T3.4 compliant educational profiles"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.roles_data = self._load_roles_data()
        
        # Framework mapping templates
        self.framework_mappings = {
            'e_cf': {
                4: ['A.7.1', 'A.7.2', 'B.4.1', 'B.4.2'],
                5: ['A.7.3', 'B.4.3', 'C.2.1', 'C.2.2'], 
                6: ['A.7.4', 'B.4.4', 'C.2.3', 'D.7.1'],
                7: ['A.7.5', 'B.4.5', 'C.2.4', 'D.7.2'],
                8: ['A.7.6', 'B.4.6', 'C.2.5', 'D.7.3']
            },
            'digcomp': {
                4: ['1.1.4', '2.1.4', '3.1.4', '4.1.4'],
                5: ['1.2.5', '2.2.5', '3.2.5', '4.2.5'],
                6: ['1.3.6', '2.3.6', '3.3.6', '4.3.6'],
                7: ['1.4.7', '2.4.7', '3.4.7', '4.4.7'],
                8: ['1.5.8', '2.5.8', '3.5.8', '4.5.8']
            },
            'greencomp': {
                4: ['GC1.1', 'GC2.1', 'GC3.1', 'GC4.1'],
                5: ['GC1.2', 'GC2.2', 'GC3.2', 'GC4.2'],
                6: ['GC1.3', 'GC2.3', 'GC3.3', 'GC4.3'],
                7: ['GC1.4', 'GC2.4', 'GC3.4', 'GC4.4'],
                8: ['GC1.5', 'GC2.5', 'GC3.5', 'GC4.5']
            }
        }
        
        # Salary data by role and EQF level (EUR annually)
        self.salary_ranges = {
            'DAN': {6: (35000, 55000), 7: (45000, 70000)},
            'DSE': {6: (40000, 65000), 7: (55000, 85000)},
            'DSM': {6: (45000, 70000), 7: (60000, 90000)},
            'DSL': {7: (70000, 110000), 8: (90000, 140000)},
            'DSC': {6: (50000, 75000), 7: (65000, 95000)},
            'DSI': {7: (60000, 95000), 8: (80000, 120000)},
            'SBA': {6: (38000, 58000), 7: (48000, 75000)},
            'SDD': {4: (25000, 40000), 5: (30000, 48000), 6: (40000, 60000)},
            'SSD': {6: (42000, 68000), 7: (55000, 82000)},
            'STS': {4: (22000, 35000), 5: (28000, 45000)}
        }
        
    def _load_roles_data(self) -> Dict[str, Any]:
        """Load roles configuration from JSON"""
        try:
            roles_file = self.project_root / 'input' / 'roles' / 'roles.json'
            with open(roles_file, 'r', encoding='utf-8') as f:
                roles_list = json.load(f)
            
            # Convert list to dict keyed by id
            return {role['id']: role for role in roles_list}
        except Exception as e:
            print(f"❌ Error loading roles data: {e}")
            return {}
    
    def generate_comprehensive_profile(self, role_id: str, eqf_level: int) -> Dict[str, Any]:
        """Generate complete T3.2/T3.4 compliant educational profile"""
        
        role_data = self.roles_data.get(role_id)
        if not role_data:
            raise ValueError(f"Role {role_id} not found")
        
        profile = {
            'metadata': {
                'role_id': role_id,
                'role_name': role_data['name'],
                'eqf_level': eqf_level,
                'generation_date': datetime.now().isoformat(),
              # 'compliance_version': 'T3.2_T3.4_v1.0',
                'profile_type': 'comprehensive_educational_profile'
            },
            
            # Core role information
            'role_definition': {
                'id': role_id,
                'name': role_data['name'],
                'description': role_data['description'],
                'main_area': role_data.get('main_area', 'Digital Sustainability'),
                'thematic_area': role_data.get('thematic_area', 'sustainability')
            },
            
            # NEW: Realistic career progression
            'realistic_career_progression': self._generate_career_progression(role_id, role_data, eqf_level),
            
            # NEW: Typical employers
            'typical_employers': self._generate_typical_employers(role_data),
            
            # NEW: Enhanced competencies with framework mapping
            'enhanced_competencies': self._generate_enhanced_competencies(role_data, eqf_level),
            
            # NEW: Detailed modular structure
            'modular_structure': self._generate_modular_structure(role_data, eqf_level),
            
            # NEW: Assessment methods
            'assessment_methods': self._generate_assessment_methods(role_data, eqf_level),
            
            # NEW: Entry requirements
            'entry_requirements': self._generate_entry_requirements(role_data, eqf_level),
            
            # NEW: CPD requirements
            'cpd_requirements': self._generate_cpd_requirements(role_data, eqf_level),
            
            # OPTIONAL: Industry sectors
            'industry_sectors': self._generate_industry_sectors(role_data)
        }
        
        return profile
    
    def _generate_career_progression(self, role_id: str, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate realistic career progression data"""
        
        # Get salary range for this role/level
        salary_data = self.salary_ranges.get(role_id, {})
        current_salary = salary_data.get(eqf_level, (30000, 50000))
        
        # Generate progression roles based on main area
        main_area = role_data.get('main_area', 'Other')
        progression_map = {
            'Data': ['Senior Data Analyst', 'Data Team Lead', 'Head of Data Analytics'],
            'Management': ['Senior Manager', 'Director', 'VP of Sustainability'],
            'Advisory': ['Senior Consultant', 'Principal Consultant', 'Practice Lead'],
            'Software Development': ['Senior Developer', 'Lead Developer', 'Technical Manager'],
            'Design': ['Senior Designer', 'Design Lead', 'Chief Design Officer'],
            'Technical Implementation': ['Technical Lead', 'System Architect', 'Technical Director']
        }
        
        roles = progression_map.get(main_area, ['Senior Professional', 'Team Lead', 'Department Head'])
        
        return {
            'entry_level': {
                'title': role_data['name'],
                'eqf_level': eqf_level,
                'salary_range_eur': {
                    'min': current_salary[0],
                    'max': current_salary[1]
                },
                'experience_required': '0-2 years'
            },
            'progression_roles': [
                {
                    'title': roles[0],
                    'years_to_achieve': '2-4',
                    'salary_increase_percent': '20-35',
                    'additional_skills_needed': ['Leadership', 'Project Management']
                },
                {
                    'title': roles[1], 
                    'years_to_achieve': '5-8',
                    'salary_increase_percent': '50-80',
                    'additional_skills_needed': ['Strategic Planning', 'Team Management', 'Budget Management']
                },
                {
                    'title': roles[2],
                    'years_to_achieve': '8-15',
                    'salary_increase_percent': '100-150',
                    'additional_skills_needed': ['Executive Leadership', 'Business Strategy', 'Stakeholder Management']
                }
            ],
            'growth_potential': 'High - Digital sustainability is rapidly expanding field',
            'mobility_options': [
                'Cross-industry movement (tech, manufacturing, finance)',
                'Consulting opportunities',
                'International assignments',
                'Academic/research positions'
            ]
        }
    
    def _generate_typical_employers(self, role_data: Dict) -> Dict[str, Any]:
        """Generate typical employer information"""
        
        main_area = role_data.get('main_area', 'Other')
        
        employer_map = {
            'Data': {
                'primary': ['Technology companies', 'Consulting firms', 'Financial services'],
                'secondary': ['Manufacturing', 'Energy companies', 'Government agencies'],
                'emerging': ['Sustainability startups', 'ESG rating agencies', 'Green finance firms']
            },
            'Management': {
                'primary': ['Large corporations', 'Consulting firms', 'Government organizations'],
                'secondary': ['NGOs', 'International organizations', 'Academic institutions'],
                'emerging': ['B-Corp companies', 'Sustainability consultancies', 'Impact investment firms']
            },
            'Advisory': {
                'primary': ['Management consulting', 'Sustainability consultancies', 'Professional services'],
                'secondary': ['Corporate sustainability departments', 'Government advisory roles'],
                'emerging': ['ESG consulting', 'Climate risk advisory', 'Circular economy consultants']
            }
        }
        
        employers = employer_map.get(main_area, {
            'primary': ['Technology companies', 'Consulting firms', 'Government agencies'],
            'secondary': ['Manufacturing', 'Financial services', 'Healthcare'],
            'emerging': ['Sustainability startups', 'Green tech companies', 'Impact organizations']
        })
        
        return {
            'primary_sectors': employers['primary'],
            'secondary_sectors': employers['secondary'],
            'emerging_opportunities': employers['emerging'],
            'company_sizes': {
                'startups': '10-50 employees',
                'sme': '50-500 employees', 
                'enterprise': '500+ employees',
                'preference_note': 'All sizes value digital sustainability expertise'
            },
            'geographic_demand': [
                'European Union (high regulatory focus)',
                'North America (corporate sustainability)',
                'Asia-Pacific (emerging regulations)',
                'Nordic countries (sustainability leaders)'
            ]
        }
    
    def _generate_enhanced_competencies(self, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate enhanced competencies with framework mappings"""
        
        core_skills = role_data.get('core_skills', [])
        
        # Generate Tuning-style learning outcomes
        learning_outcomes = []
        for skill in core_skills[:5]:  # Top 5 skills
            outcome = f"The learner will be able to apply {skill.replace('_', ' ')} principles to address digital sustainability challenges in professional contexts"
            learning_outcomes.append(outcome)
        
        return {
            'eqf_alignment': {
                'level': eqf_level,
                'descriptor': self._get_eqf_descriptor(eqf_level),
                'knowledge_skills_competence': self._get_eqf_details(eqf_level)
            },
            'learning_outcomes': learning_outcomes,
            'competency_name': f"Digital Sustainability Professional - {role_data['name']}",
            'framework_mappings': {
                'e_cf': self.framework_mappings['e_cf'][eqf_level],
                'digcomp': self.framework_mappings['digcomp'][eqf_level],
                'greencomp': self.framework_mappings['greencomp'][eqf_level]
            },
            'core_competencies': [
                {
                    'name': skill.replace('_', ' ').title(),
                    'description': f"Professional application of {skill.replace('_', ' ')} in sustainability contexts",
                    'proficiency_level': self._get_proficiency_level(eqf_level)
                }
                for skill in core_skills
            ]
        }
    
    def _generate_modular_structure(self, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate detailed modular structure"""
        
        default_ects = role_data.get('default_ects', {})
        total_ects = default_ects.get(str(eqf_level), default_ects.get(eqf_level, 60))
        
        # Calculate semesters based on ECTS
        if total_ects <= 30:
            semesters = 1
        elif total_ects <= 60:
            semesters = 2
        elif total_ects <= 90:
            semesters = 3
        else:
            semesters = 4
        
        # Generate module structure
        related_modules = role_data.get('related_modules', {})
        modules = []
        
        module_count = min(len(related_modules), 8)  # Max 8 modules
        ects_per_module = total_ects / module_count if module_count > 0 else 7.5
        
        for i, (module_id, relevance) in enumerate(list(related_modules.items())[:module_count]):
            modules.append({
                'module_id': module_id,
                'name': f"Digital Sustainability Module {i+1}",
                'ects': round(ects_per_module, 1),
                'semester': (i // 4) + 1,  # Distribute across semesters
                'relevance_score': relevance,
                'prerequisites': [f"M{i}"] if i > 0 else [],
                'delivery_mode': random.choice(['online', 'blended', 'classroom'])
            })
        
        return {
            'total_ects': total_ects,
            'duration_semesters': semesters,
            'modules': modules,
            'semesters': [
                {
                    'semester_number': i+1,
                    'ects': sum(m['ects'] for m in modules if m['semester'] == i+1),
                    'modules_count': len([m for m in modules if m['semester'] == i+1])
                }
                for i in range(semesters)
            ],
            'flexibility': {
                'part_time_available': True,
                'module_independence': 'High',
                'entry_points': ['September', 'January'] if semesters > 1 else ['Continuous']
            }
        }
    
    def _generate_assessment_methods(self, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate assessment methods based on role and level"""
        
        module_types = role_data.get('module_design', {}).get('module_types', ['theoretical', 'practical'])
        
        methods = []
        if 'theoretical' in module_types:
            methods.extend(['Written examination', 'Research project', 'Case study analysis'])
        if 'practical' in module_types:
            methods.extend(['Practical project', 'Portfolio development', 'Competency demonstration'])
        if 'work-based' in module_types:
            methods.extend(['Workplace assessment', 'Professional portfolio', 'Reflective journal'])
        
        return {
            'primary_methods': methods[:3],
            'secondary_methods': methods[3:] if len(methods) > 3 else [],
            'continuous_assessment': True,
            'final_assessment': 'Capstone project demonstrating integrated competencies',
            'practical_components': {
                'percentage': 60 if 'practical' in module_types else 40,
                'real_world_application': True,
                'industry_partnerships': role_data.get('dual_principle_applicable', False)
            },
            'recognition_methods': [
                'ECTS credit assignment',
                'Competency mapping',
                'Learning outcome verification',
                'Professional skill validation'
            ]
        }
    
    def _generate_entry_requirements(self, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate entry requirements based on EQF level"""
        
        requirements_map = {
            4: {
                'formal': 'Upper secondary education completion',
                'experience': 'No prior experience required',
                'digital_literacy': 'Basic computer skills'
            },
            5: {
                'formal': 'Upper secondary education or equivalent',
                'experience': '1-2 years relevant experience OR formal qualification',
                'digital_literacy': 'Intermediate digital skills'
            },
            6: {
                'formal': 'Bachelor\'s degree or equivalent professional experience',
                'experience': '2-3 years professional experience recommended',
                'digital_literacy': 'Good digital competencies'
            },
            7: {
                'formal': 'Bachelor\'s degree plus experience OR Master\'s degree',
                'experience': '3-5 years professional experience',
                'digital_literacy': 'Advanced digital competencies'
            },
            8: {
                'formal': 'Master\'s degree or extensive professional experience',
                'experience': '5+ years senior professional experience',
                'digital_literacy': 'Expert-level digital competencies'
            }
        }
        
        base_req = requirements_map[eqf_level]
        
        return {
            'formal_education': base_req['formal'],
            'professional_experience': base_req['experience'],
            'digital_competencies': base_req['digital_literacy'],
            'recommended_background': role_data.get('main_area', 'Any professional background'),
            'language_requirements': 'English proficiency (B2 level minimum)',
            'accessibility': {
                'prior_learning_recognition': True,
                'flexible_entry': True,
                'support_available': 'Academic and career guidance provided'
            },
            'suitability': {
                'career_changers': eqf_level <= 6,
                'new_graduates': eqf_level <= 7,
                'experienced_professionals': True
            }
        }
    
    def _generate_cpd_requirements(self, role_data: Dict, eqf_level: int) -> Dict[str, Any]:
        """Generate Continuing Professional Development requirements"""
        
        return {
            'certification_maintenance': {
                'renewal_period_years': 3,
                'cpd_hours_required': 40,
                'acceptable_activities': [
                    'Professional development courses',
                    'Conference attendance',
                    'Research publications',
                    'Mentoring activities',
                    'Industry projects'
                ]
            },
            'recommended_updates': [
                'Emerging sustainability regulations',
                'New digital technologies',
                'Industry best practices',
                'Framework updates (e-CF, DigComp, GreenComp)'
            ],
            'professional_networks': [
                'Digital Sustainability Professionals Association',
                'European Sustainability Network',
                'Industry-specific professional bodies'
            ],
            'micro_learning_opportunities': {
                'stackable_credentials': True,
                'minimum_ects': 0.5,
                'maximum_recognition': 10  # ECTS per renewal period
            }
        }
    
    def _generate_industry_sectors(self, role_data: Dict) -> List[str]:
        """Generate applicable industry sectors"""
        
        base_sectors = [
            'Information Technology',
            'Financial Services', 
            'Manufacturing',
            'Energy & Utilities',
            'Government & Public Sector'
        ]
        
        main_area = role_data.get('main_area', 'Other')
        if main_area == 'Data':
            base_sectors.extend(['Healthcare', 'Retail', 'Telecommunications'])
        elif main_area == 'Management':
            base_sectors.extend(['Consulting', 'Non-profit', 'Education'])
        elif main_area == 'Advisory':
            base_sectors.extend(['Legal Services', 'Real Estate', 'Transportation'])
        
        return base_sectors
    
    def _get_eqf_descriptor(self, level: int) -> str:
        """Get EQF level descriptor"""
        descriptors = {
            4: 'Factual and theoretical knowledge in broad contexts',
            5: 'Comprehensive, specialised, factual and theoretical knowledge',
            6: 'Advanced knowledge of a field of work or study', 
            7: 'Highly specialised knowledge, some at the forefront of knowledge',
            8: 'Knowledge at the most advanced frontier of a field of work or study'
        }
        return descriptors.get(level, 'Advanced professional knowledge')
    
    def _get_eqf_details(self, level: int) -> Dict[str, str]:
        """Get detailed EQF knowledge, skills, competence breakdown"""
        return {
            'knowledge': self._get_eqf_descriptor(level),
            'skills': f'Advanced professional skills required for EQF Level {level}',
            'competence': f'Full autonomy and responsibility appropriate for EQF Level {level}'
        }
    
    def _get_proficiency_level(self, eqf_level: int) -> str:
        """Map EQF level to proficiency description"""
        mapping = {
            4: 'Competent',
            5: 'Proficient', 
            6: 'Advanced',
            7: 'Expert',
            8: 'Master'
        }
        return mapping.get(eqf_level, 'Professional')

# Backward compatibility alias
EducationalProfileGenerator = EnhancedEducationalProfilesManager

# Additional helper function for legacy compatibility
def create_educational_profile_generator(project_root: Path) -> EnhancedEducationalProfilesManager:
    """Legacy compatibility function"""
    return EnhancedEducationalProfilesManager(project_root)
