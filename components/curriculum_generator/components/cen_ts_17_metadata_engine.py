# scripts/curriculum_generator/components/cen_ts_17_metadata_engine.py
"""
CEN/TS 17699:2022 Machine-Readable Metadata Engine
Addresses interoperability gaps: semantic web vocabularies, structured metadata, URI links
Generates RDF/XML/JSON-LD exportable structures for EU-wide database compatibility
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

class CenTS17MetadataEngine:
    """Generates CEN/TS 17699:2022 compliant machine-readable metadata"""
    
    def __init__(self):
        # Semantic web vocabulary base URIs
        self.vocab_uris = {
            'esco': 'http://data.europa.eu/esco/',
            'ecf': 'http://www.ecompetences.eu/ecf/',
            'digcomp': 'https://ec.europa.eu/jrc/en/digcomp/',
            'greencomp': 'https://ec.europa.eu/jrc/en/greencomp/',
            'eqf': 'https://ec.europa.eu/ploteus/eqf/',
            'ects': 'https://ec.europa.eu/education/ects/',
            'dscg': 'https://digital4sustainability.eu/profiles/'
        }
        
        # EQF level descriptors with URIs
        self.eqf_descriptors = {
            4: {
                'uri': f"{self.vocab_uris['eqf']}level/4",
                'knowledge': 'factual and theoretical knowledge in broad contexts',
                'skills': 'cognitive and practical skills required to solve specific problems',
                'responsibility': 'self-management within guidelines'
            },
            5: {
                'uri': f"{self.vocab_uris['eqf']}level/5", 
                'knowledge': 'comprehensive, specialised, factual and theoretical knowledge',
                'skills': 'comprehensive cognitive and practical skills',
                'responsibility': 'management and supervision in contexts of work or study'
            },
            6: {
                'uri': f"{self.vocab_uris['eqf']}level/6",
                'knowledge': 'advanced knowledge involving critical understanding',
                'skills': 'advanced skills demonstrating mastery and innovation',
                'responsibility': 'management of complex technical or professional activities'
            },
            7: {
                'uri': f"{self.vocab_uris['eqf']}level/7",
                'knowledge': 'highly specialised knowledge at the forefront of knowledge',
                'skills': 'specialised problem-solving skills in research and innovation',
                'responsibility': 'management and transformation of complex contexts'
            },
            8: {
                'uri': f"{self.vocab_uris['eqf']}level/8",
                'knowledge': 'knowledge at the most advanced frontier',
                'skills': 'most advanced skills to synthesize and evaluate',
                'responsibility': 'authority, innovation, autonomy, and integrity'
            }
        }
        
        # Framework competency URI mappings
        self.framework_uris = {
            'e_cf': {
                'E.1': f"{self.vocab_uris['ecf']}competence/E.1",
                'E.4': f"{self.vocab_uris['ecf']}competence/E.4", 
                'E.9': f"{self.vocab_uris['ecf']}competence/E.9",
                'A.3': f"{self.vocab_uris['ecf']}competence/A.3",
                'B.1': f"{self.vocab_uris['ecf']}competence/B.1",
                'B.6': f"{self.vocab_uris['ecf']}competence/B.6",
                'D.10': f"{self.vocab_uris['ecf']}competence/D.10"
            },
            'digcomp': {
                '5.4': f"{self.vocab_uris['digcomp']}competence/5.4",
                '2.4': f"{self.vocab_uris['digcomp']}competence/2.4",
                '3.1': f"{self.vocab_uris['digcomp']}competence/3.1",
                '5.2': f"{self.vocab_uris['digcomp']}competence/5.2"
            },
            'greencomp': {
                '4.3': f"{self.vocab_uris['greencomp']}competence/4.3",
                '4.2': f"{self.vocab_uris['greencomp']}competence/4.2",
                '3.4': f"{self.vocab_uris['greencomp']}competence/3.4",
                '1.3': f"{self.vocab_uris['greencomp']}competence/1.3"
            }
        }
    
    def generate_machine_readable_metadata(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete machine-readable metadata structure per CEN/TS 17699:2022"""
        
        role_def = profile_data.get('role_definition', {})
        metadata = profile_data.get('metadata', {})
        
        # Generate profile UUID and version info
        profile_uuid = str(uuid.uuid4())
        current_date = datetime.now()
        valid_until = current_date + timedelta(days=1095)  # 3 years validity
        
        machine_metadata = {
            # Core identification metadata
            '@context': {
                '@vocab': 'https://www.w3.org/ns/org#',
                'dct': 'http://purl.org/dc/terms/',
                'skos': 'http://www.w3.org/2004/02/skos/core#',
                'esco': self.vocab_uris['esco'],
                'ecf': self.vocab_uris['ecf'],
                'eqf': self.vocab_uris['eqf']
            },
            '@type': 'EducationalProfile',
            '@id': f"{self.vocab_uris['dscg']}{role_def.get('id', 'ROLE')}",
            
            # Profile versioning and validity
            'dct:identifier': profile_uuid,
            'dct:version': '1.0.0',
            'dct:issued': current_date.isoformat(),
            'dct:valid': valid_until.isoformat(),
            'dct:modified': current_date.isoformat(),
            
            # Profile core metadata
            'profileId': role_def.get('id', 'ROLE'),
            'title': role_def.get('name', 'Professional'),
            'description': role_def.get('description', 'Professional role'),
            'language': 'en',
            'targetCountry': ['EU'],
            
            # EQF level with semantic URI
            'eqfLevel': {
                '@type': 'EQFLevel',
                '@id': self.eqf_descriptors[metadata.get('eqf_level', 6)]['uri'],
                'level': metadata.get('eqf_level', 6),
                'description': self.eqf_descriptors[metadata.get('eqf_level', 6)]
            },
            
            # Learning outcomes with UUIDs and semantic anchors
            'learningOutcomes': self._generate_learning_outcome_metadata(profile_data),
            
            # Competency framework mappings with URIs
            'competencyFrameworkAlignment': self._generate_framework_metadata(profile_data),
            
            # Career progression with structured metadata
            'careerProgression': self._generate_career_metadata(profile_data),
            
            # CPD requirements as structured metadata
            'continuingProfessionalDevelopment': self._generate_cpd_metadata(profile_data),
            
            # Industry application with ESCO sector codes
            'industryApplication': self._generate_industry_metadata(profile_data),
            
            # Modularization metadata for learning units
            'modularizationStructure': self._generate_modular_metadata(profile_data),
            
            # Learning opportunity cross-reference
            'learningOpportunitySpecification': self._generate_learning_opportunity_bridge(profile_data),
            
            # Assessment metadata
            'assessmentSpecification': self._generate_assessment_metadata(profile_data)
        }
        
        return machine_metadata
    
    def _generate_learning_outcome_metadata(self, profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate learning outcomes with UUIDs and semantic anchors"""
        
        competencies = profile_data.get('enhanced_competencies', {})
        learning_outcomes = competencies.get('learning_outcomes', [])
        
        structured_outcomes = []
        for i, outcome in enumerate(learning_outcomes, 1):
            outcome_uuid = str(uuid.uuid4())
            structured_outcomes.append({
                '@type': 'LearningOutcome',
                '@id': f"{self.vocab_uris['dscg']}outcome/{outcome_uuid}",
                'outcomeId': f"LO_{i:02d}",
                'description': outcome,
                'eqfAlignment': {
                    '@id': self.eqf_descriptors[profile_data.get('metadata', {}).get('eqf_level', 6)]['uri'],
                    'level': profile_data.get('metadata', {}).get('eqf_level', 6)
                },
                'bloomsTaxonomyLevel': self._extract_blooms_level(outcome),
                'learningDomain': self._classify_learning_domain(outcome)
            })
        
        return structured_outcomes
    
    def _generate_framework_metadata(self, profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate framework mappings with semantic web URIs"""
        
        competencies = profile_data.get('enhanced_competencies', {})
        framework_mappings = competencies.get('framework_mappings', {})
        role_id = profile_data.get('role_definition', {}).get('id', 'ROLE')
        
        # Get role-specific framework mappings if none exist
        if not framework_mappings:
            framework_mappings = self._get_role_specific_framework_mappings(role_id)
        
        structured_frameworks = []
        
        for framework, codes in framework_mappings.items():
            if framework in self.framework_uris and codes:
                for code in codes:
                    if code in self.framework_uris[framework]:
                        structured_frameworks.append({
                            '@type': 'CompetencyFrameworkAlignment',
                            'framework': framework.upper().replace('_', '-'),
                            'competencyCode': code,
                            'competencyURI': self.framework_uris[framework][code],
                            'proficiencyLevel': self._determine_proficiency_level(framework, code, profile_data.get('metadata', {}).get('eqf_level', 6)),
                            'alignmentType': 'core'
                        })
        
        return structured_frameworks
    
    def _generate_career_metadata(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate career progression with structured metadata"""
        
        career_prog = profile_data.get('realistic_career_progression', {})
        role_id = profile_data.get('role_definition', {}).get('id', 'ROLE')
        
        # Generate complete career progression if missing
        if not career_prog or not career_prog.get('progression_roles'):
            career_prog = self._generate_complete_career_progression(role_id)
        
        structured_career = {
            '@type': 'CareerProgression',
            'entryLevel': {
                '@type': 'CareerLevel',
                'levelId': 'entry',
                'title': career_prog.get('entry_level', {}).get('title', 'Professional'),
                'eqfLevel': profile_data.get('metadata', {}).get('eqf_level', 6),
                'experienceRequired': '0-2 years',
                'salaryRange': career_prog.get('entry_level', {}).get('salary_range_eur', {})
            },
            'progressionPath': []
        }
        
        progression_roles = career_prog.get('progression_roles', [])
        for i, role in enumerate(progression_roles, 1):
            if isinstance(role, dict):
                structured_career['progressionPath'].append({
                    '@type': 'CareerLevel',
                    'levelId': f'level_{i}',
                    'title': role.get('title', f'Senior Professional {i}'),
                    'eqfLevel': min(profile_data.get('metadata', {}).get('eqf_level', 6) + i, 8),
                    'yearsToAchieve': role.get('years_to_achieve', '3-5 years'),
                    'salaryIncrease': role.get('salary_increase_percent', '30-50%')
                })
        
        return structured_career
    
    def _generate_cpd_metadata(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CPD requirements as structured metadata"""
        
        cpd = profile_data.get('cpd_requirements', {})
        
        structured_cpd = {
            '@type': 'ContinuingProfessionalDevelopment',
            'maintenanceRequirements': {
                '@type': 'MaintenanceRequirement',
                'renewalPeriod': f"P{cpd.get('certification_maintenance', {}).get('renewal_period_years', 3)}Y",
                'requiredHours': cpd.get('certification_maintenance', {}).get('cpd_hours_required', 40),
                'validationMethod': 'portfolio-based',
                'recognizedProviders': ['accredited_institutions', 'professional_bodies']
            },
            'microCredentials': {
                '@type': 'MicroCredentialRecognition',
                'maximumECTS': cpd.get('micro_learning_opportunities', {}).get('maximum_recognition', 10),
                'stackableCredits': True,
                'recognitionFramework': 'ECTS'
            }
        }
        
        return structured_cpd
    
    def _generate_industry_metadata(self, profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate industry applications with ESCO sector codes"""
        
        employers = profile_data.get('typical_employers', {})
        industry_app = profile_data.get('industry_application', [])
        
        # ESCO sector mappings (simplified - would need full ESCO database integration)
        esco_sectors = {
            'technology': 'http://data.europa.eu/esco/isco/C25',
            'financial': 'http://data.europa.eu/esco/isco/C64',
            'consulting': 'http://data.europa.eu/esco/isco/C70',
            'government': 'http://data.europa.eu/esco/isco/C84',
            'manufacturing': 'http://data.europa.eu/esco/isco/C25'
        }
        
        structured_industries = []
        primary_sectors = employers.get('primary_sectors', industry_app)
        
        for sector in primary_sectors[:5]:  # Limit to top 5
            sector_key = self._classify_sector(sector)
            structured_industries.append({
                '@type': 'IndustryApplication',
                'sectorName': sector,
                'escoSectorCode': esco_sectors.get(sector_key, esco_sectors['technology']),
                'applicabilityLevel': 'high',
                'typicalRoles': [profile_data.get('role_definition', {}).get('name', 'Professional')]
            })
        
        return structured_industries
    
    def _generate_modular_metadata(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate modularization metadata for learning units"""
        
        return {
            '@type': 'ModularStructure',
            'unitOfLearning': {
                'recommendedECTS': 30,
                'minimumECTS': 15,
                'maximumECTS': 60,
                'modularityLevel': 'high',
                'stackabilitySupported': True
            },
            'creditTransferSupport': {
                'ectsCompatible': True,
                'regionalRecognition': ['EU', 'EHEA'],
                'qualificationLevel': profile_data.get('metadata', {}).get('eqf_level', 6)
            }
        }
    
    def _generate_learning_opportunity_bridge(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning opportunity specification bridge"""
        
        role_id = profile_data.get('role_definition', {}).get('id', 'ROLE')
        
        return {
            '@type': 'LearningOpportunitySpecification',
            '@id': f"{self.vocab_uris['dscg']}curriculum/{role_id}",
            'relatedProfile': f"{self.vocab_uris['dscg']}{role_id}",
            'implementationGuidelines': {
                'deliveryModes': ['classroom', 'online', 'blended', 'work-based'],
                'assessmentMethods': ['portfolio', 'project', 'competency-demonstration'],
                'qualityAssurance': 'external-validation'
            },
            'curriculumMetadata': {
                'modular': True,
                'flexible': True,
                'outcomesBased': True
            }
        }
    
    def _generate_assessment_metadata(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate assessment specification metadata"""
        
        eqf_level = profile_data.get('metadata', {}).get('eqf_level', 6)
        
        return {
            '@type': 'AssessmentSpecification',
            'assessmentApproach': 'competency-based',
            'assessmentMethods': {
                'primary': ['portfolio', 'project-based', 'competency-demonstration'],
                'supplementary': ['peer-review', 'self-assessment', 'workplace-observation']
            },
            'eqfAlignedCriteria': {
                'knowledge': f"Demonstrates {self.eqf_descriptors[eqf_level]['knowledge']}",
                'skills': f"Exhibits {self.eqf_descriptors[eqf_level]['skills']}",
                'responsibility': f"Shows {self.eqf_descriptors[eqf_level]['responsibility']}"
            },
            'qualityAssurance': {
                'externalValidation': True,
                'peerReview': True,
                'stakeholderFeedback': True
            }
        }
    
    # Helper methods
    def _extract_blooms_level(self, outcome: str) -> str:
        """Extract Bloom's taxonomy level from learning outcome"""
        outcome_lower = outcome.lower()
        if any(verb in outcome_lower for verb in ['synthesize', 'evaluate', 'create', 'innovate']):
            return 'create'
        elif any(verb in outcome_lower for verb in ['analyze', 'compare', 'categorize']):
            return 'analyze'
        elif any(verb in outcome_lower for verb in ['apply', 'implement', 'demonstrate']):
            return 'apply'
        else:
            return 'understand'
    
    def _classify_learning_domain(self, outcome: str) -> str:
        """Classify learning outcome domain"""
        outcome_lower = outcome.lower()
        if any(word in outcome_lower for word in ['lead', 'manage', 'coordinate']):
            return 'cognitive-strategic'
        elif any(word in outcome_lower for word in ['design', 'develop', 'implement']):
            return 'cognitive-procedural'
        else:
            return 'cognitive-factual'
    
    def _get_role_specific_framework_mappings(self, role_id: str) -> Dict[str, List[str]]:
        """Get role-specific framework mappings"""
        mappings = {
            'DSL': {'e_cf': ['E.1', 'E.4', 'E.9'], 'digcomp': ['5.4', '2.4'], 'greencomp': ['4.3', '4.2']},
            'DSM': {'e_cf': ['A.3', 'D.10'], 'digcomp': ['2.2', '3.4'], 'greencomp': ['2.2', '3.2']},
            'DAN': {'e_cf': ['B.1', 'B.6'], 'digcomp': ['3.1', '5.2'], 'greencomp': ['1.3', '2.3']},
            'SDD': {'e_cf': ['B.1', 'B.4'], 'digcomp': ['3.2', '5.1'], 'greencomp': ['2.1', '3.3']}
        }
        return mappings.get(role_id, {'e_cf': ['B.1'], 'digcomp': ['3.1'], 'greencomp': ['1.1']})
    
    def _determine_proficiency_level(self, framework: str, code: str, eqf_level: int) -> str:
        """Determine proficiency level based on EQF level"""
        if eqf_level >= 7:
            return 'expert'
        elif eqf_level >= 6:
            return 'proficient'
        elif eqf_level >= 5:
            return 'competent'
        else:
            return 'basic'
    
    def _generate_complete_career_progression(self, role_id: str) -> Dict[str, Any]:
        """Generate complete career progression when missing"""
        progressions = {
            'DSL': {
                'entry_level': {'title': 'Sustainability Strategy Coordinator'},
                'progression_roles': [
                    {'title': 'Senior Sustainability Leader', 'years_to_achieve': '3-5 years'},
                    {'title': 'Director of Sustainability Strategy', 'years_to_achieve': '5-8 years'}, 
                    {'title': 'Chief Sustainability Officer', 'years_to_achieve': '8-12 years'}
                ]
            }
        }
        return progressions.get(role_id, {
            'entry_level': {'title': 'Professional'},
            'progression_roles': [{'title': 'Senior Professional', 'years_to_achieve': '3-5 years'}]
        })
    
    def _classify_sector(self, sector_description: str) -> str:
        """Classify sector for ESCO mapping"""
        sector_lower = sector_description.lower()
        if any(word in sector_lower for word in ['technology', 'software', 'digital']):
            return 'technology'
        elif any(word in sector_lower for word in ['financial', 'investment', 'banking']):
            return 'financial'
        elif any(word in sector_lower for word in ['consulting', 'advisory']):
            return 'consulting'
        elif any(word in sector_lower for word in ['government', 'public', 'agency']):
            return 'government'
        else:
            return 'technology'
    
    def export_as_json_ld(self, metadata: Dict[str, Any], output_path: Path) -> Path:
        """Export metadata as JSON-LD"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        return output_path
    
    def export_as_rdf_xml(self, metadata: Dict[str, Any], output_path: Path) -> Path:
        """Export metadata as RDF/XML (simplified)"""
        # This would require an RDF library like rdflib for full implementation
        # For now, create XML structure manually
        xml_content = self._convert_to_rdf_xml(metadata)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        return output_path
    
    def _convert_to_rdf_xml(self, metadata: Dict[str, Any]) -> str:
        """Convert metadata to RDF/XML format"""
        # Simplified RDF/XML generation
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dct="http://purl.org/dc/terms/"
         xmlns:esco="{self.vocab_uris['esco']}"
         xmlns:eqf="{self.vocab_uris['eqf']}">
  
  <rdf:Description rdf:about="{metadata.get('@id', '')}">
    <rdf:type rdf:resource="{metadata.get('@type', '')}"/>
    <dct:title>{metadata.get('title', '')}</dct:title>
    <dct:identifier>{metadata.get('dct:identifier', '')}</dct:identifier>
    <dct:version>{metadata.get('dct:version', '')}</dct:version>
    <dct:issued>{metadata.get('dct:issued', '')}</dct:issued>
    <dct:valid>{metadata.get('dct:valid', '')}</dct:valid>
  </rdf:Description>
  
</rdf:RDF>"""

