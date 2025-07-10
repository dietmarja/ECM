# scripts/curriculum_generator/core/standards_manager.py
"""
EU standards compliance and management
Handles EQF, ECTS, ECVET and other EU framework requirements
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class StandardsManager:
    """Manages EU standards compliance and validation"""
    
    def __init__(self, standards_dir: str = "input/standards"):
        self.standards_dir = Path(standards_dir)
        self.standards = {}
        self.eqf_descriptors = self._initialize_eqf_descriptors()
        
        # Load standards if directory exists
        if self.standards_dir.exists():
            self._load_standards()
        else:
            logger.warning(f"Standards directory not found: {standards_dir}")
    
    def _initialize_eqf_descriptors(self) -> Dict:
        """Initialize EQF level descriptors"""
        return {
            4: {
                "knowledge": "Factual and theoretical knowledge in broad contexts",
                "skills": "Cognitive and practical skills for specific problems",
                "autonomy": "Self-management within predictable guidelines",
                "learning_hours_range": [120, 1800]
            },
            5: {
                "knowledge": "Comprehensive, specialised knowledge with boundary awareness",
                "skills": "Comprehensive skills for creative solutions to abstract problems",
                "autonomy": "Management and supervision in unpredictable contexts",
                "learning_hours_range": [300, 3000]
            },
            6: {
                "knowledge": "Advanced knowledge with critical understanding of theories",
                "skills": "Advanced skills with mastery and innovation for complex problems",
                "autonomy": "Complex technical/professional decision-making responsibility",
                "learning_hours_range": [900, 6000]
            },
            7: {
                "knowledge": "Highly specialised knowledge at forefront for original thinking",
                "skills": "Specialised problem-solving for research and innovation",
                "autonomy": "Transform complex, unpredictable contexts with new approaches",
                "learning_hours_range": [1500, 4500]
            },
            8: {
                "knowledge": "Knowledge at advanced frontier and interface between fields",
                "skills": "Most advanced techniques including synthesis and evaluation",
                "autonomy": "Substantial authority, innovation, autonomy and scholarly integrity",
                "learning_hours_range": [3000, 7500]
            }
        }
    
    def _load_standards(self):
        """Load EU standards from files"""
        standard_files = {
            'ects': 'standard_ects.json',
            'ecvet': 'standard_ecvet.json',
            'eqf': 'standard_eqf.json',
            'microcredentials': 'standard_microcredentials.json',
            'certification': 'standard_certification.json'
        }
        
        for standard_name, filename in standard_files.items():
            try:
                standard_path = self.standards_dir / filename
                if standard_path.exists():
                    with open(standard_path, 'r', encoding='utf-8') as f:
                        self.standards[standard_name] = json.load(f)
                        logger.info(f"Loaded {standard_name} standard")
                else:
                    logger.debug(f"Standard file not found: {filename}")
            except Exception as e:
                logger.warning(f"Error loading {standard_name} standard: {e}")
        
        logger.info(f"Loaded {len(self.standards)} EU standards")
    
    def enhance_with_standards(self, curriculum: Dict) -> Dict:
        """Enhance curriculum with EU standards compliance"""
        
        # Add EQF compliance
        eqf_level = curriculum.get('eqf_specification', {}).get('target_eqf_level', 6)
        curriculum['eqf_compliance'] = {
            'target_level': eqf_level,
            'descriptors': self.eqf_descriptors.get(eqf_level, {}),
            'validation_status': 'compliant'
        }
        
        # Add ECTS validation
        ects_spec = curriculum.get('ects_specification', {})
        curriculum['ects_compliance'] = {
            'allocated_ects': ects_spec.get('allocated_ects', 0),
            'target_ects': ects_spec.get('target_ects', 0),
            'efficiency': ects_spec.get('allocation_efficiency', 0),
            'validation_rules_applied': list(self.standards.get('ects', {}).get('validation_rules', []))
        }
        
        # Add certification framework
        curriculum['certification_framework'] = self._generate_certification_framework(curriculum)
        
        # Add micro-credentials support
        if 'microcredentials' in self.standards:
            curriculum['microcredentials_support'] = {
                'framework_compliance': 'EU Council Recommendation 2022/C 243/02',
                'stackability_supported': True,
                'digital_credentials': True
            }
        
        return curriculum
    
    def _generate_certification_framework(self, curriculum: Dict) -> Dict:
        """Generate certification framework information"""
        eqf_level = curriculum.get('eqf_specification', {}).get('target_eqf_level', 6)
        
        framework = {
            'qualification_type': self._get_qualification_type(eqf_level),
            'recognition_scope': 'EU-wide' if eqf_level >= 6 else 'National/Regional',
            'quality_assurance': {
                'internal_qa': True,
                'external_qa_required': eqf_level >= 6
            },
            'stackability': {
                'horizontal_stacking': True,
                'vertical_progression': True,
                'credit_transfer': True
            }
        }
        
        return framework
    
    def _get_qualification_type(self, eqf_level: int) -> str:
        """Determine qualification type based on EQF level"""
        if eqf_level <= 4:
            return 'Vocational Certificate'
        elif eqf_level == 5:
            return 'Advanced Vocational Certificate'
        elif eqf_level == 6:
            return 'Bachelor Level Qualification'
        elif eqf_level == 7:
            return 'Master Level Qualification'
        else:  # EQF 8
            return 'Doctoral Level Qualification'
    
    def validate_ects_allocation(self, target_ects: float, allocated_ects: float) -> Dict:
        """Validate ECTS allocation against standards"""
        efficiency = (allocated_ects / target_ects) * 100 if target_ects > 0 else 0
        
        validation = {
            'is_valid': True,
            'efficiency': efficiency,
            'warnings': [],
            'recommendations': []
        }
        
        if efficiency < 80:
            validation['warnings'].append('Low ECTS efficiency - consider adding more content')
        elif efficiency > 120:
            validation['warnings'].append('High ECTS allocation - consider reducing content')
        
        if efficiency < 70 or efficiency > 150:
            validation['is_valid'] = False
            validation['recommendations'].append('Significant ECTS mismatch - review curriculum scope')
        
        return validation
    
    def get_work_based_learning_requirements(self, eqf_level: int) -> float:
        """Get work-based learning percentage requirements for EQF level"""
        wbl_requirements = {
            4: 0.25,  # 25% for vocational levels
            5: 0.30,  # 30% for advanced vocational
            6: 0.20,  # 20% for bachelor level
            7: 0.15,  # 15% for master level
            8: 0.10   # 10% for doctoral level
        }
        return wbl_requirements.get(eqf_level, 0.20)
    
    def get_assessment_complexity_for_eqf(self, eqf_level: int) -> str:
        """Get appropriate assessment complexity for EQF level"""
        complexity_mapping = {
            4: 'structured',
            5: 'intermediate',
            6: 'advanced',
            7: 'expert',
            8: 'research'
        }
        return complexity_mapping.get(eqf_level, 'intermediate')
