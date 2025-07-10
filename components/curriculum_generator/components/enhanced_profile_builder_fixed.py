#!/usr/bin/env python3
# scripts/curriculum_generator/components/enhanced_profile_builder_fixed.py
"""
FIXED Enhanced Educational Profile Builder - Uses Rich JSON Data
Integrates rich educational profiles JSON with enhanced curriculum generation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path

class FixedEnhancedEducationalProfileBuilder:
    """FIXED: Enhanced profile builder that ACTUALLY uses the rich JSON data"""

    def __init__(self, role_definitions: Dict[str, Any], project_root: Path):
        self.role_definitions = role_definitions
        self.project_root = project_root
        
        # FIXED: Load rich educational profiles from JSON
        self.rich_profiles = self._load_rich_educational_profiles()
        
        print(f"🎯 FIXED Enhanced Educational Profile Builder initialized")
        print(f"   - Role definitions: {len(role_definitions)}")
        print(f"   - Rich profiles loaded: {len(self.rich_profiles)}")

    def _load_rich_educational_profiles(self) -> Dict[str, Dict[str, Any]]:
        """FIXED: Load rich educational profiles from JSON file"""
        
        profiles_file = self.project_root / "input" / "educational_profiles" / "educational_profiles.json"
        
        try:
            with open(profiles_file, 'r', encoding='utf-8') as f:
                profiles_list = json.load(f)
            
            # Convert to dictionary for easy lookup
            profiles_dict = {profile['id']: profile for profile in profiles_list}
            
            print(f"✅ RICH profile data loaded:")
            for profile_id, profile in profiles_dict.items():
                enhanced_comps = len(profile.get('enhanced_competencies', []))
                print(f"   - {profile_id}: {enhanced_comps} enhanced competencies")
            
            return profiles_dict
            
        except FileNotFoundError:
            print(f"⚠️ Rich profiles file not found: {profiles_file}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing rich profiles JSON: {e}")
            return {}

    def build_rich_educational_profile(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """FIXED: Build profile using rich JSON data + enhanced generation"""
        
        print(f"\n🏗️ FIXED: Building RICH educational profile for {role_name} ({role_id})")
        
        # FIXED: Get rich profile data from JSON
        rich_profile_data = self.rich_profiles.get(role_id, {})
        
        if rich_profile_data:
            print(f"✅ RICH profile data loaded:")
            enhanced_competencies = rich_profile_data.get('enhanced_competencies', [])
            print(f"   Enhanced competencies: {len(enhanced_competencies)}")
            
            # FIXED: Use JSON data as primary source
            profile = self._build_from_rich_json_data(
                rich_profile_data, role_id, role_name, topic, eqf_level, target_ects, role_info
            )
        else:
            print(f"⚠️ Using fallback profile loader for missing data...")
            # Fallback to generated data if JSON not available
            profile = self._build_fallback_profile(
                role_id, role_name, topic, eqf_level, target_ects, role_info
            )
        
        print(f"✅ FIXED: Educational profile built successfully!")
        print(f"   Profile type: {profile.get('profile_type', 'unknown')}")
        print(f"   Rich sections included:")
        print(f"     - Enhanced competencies: {'✅' if profile.get('enhanced_competencies') else '❌'}")
        print(f"     - Modular structure: {'✅' if profile.get('modular_structure') else '❌'}")
        print(f"     - Career progression: {'✅' if profile.get('realistic_career_progression') else '❌'}")
        
        return profile

    def _build_from_rich_json_data(
        self,
        rich_data: Dict[str, Any],
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build profile using rich JSON data as primary source"""
        
        # Generate enhanced metadata
        profile_metadata = self._generate_enhanced_metadata(
            role_id, role_name, topic, eqf_level, target_ects
        )
        
        # FIXED: Use JSON enhanced competencies directly
        json_competencies = rich_data.get('enhanced_competencies', [])
        enhanced_competencies = self._adapt_json_competencies_for_topic(
            json_competencies, topic, eqf_level
        )
        
        # Generate additional profile sections
        programme_outcomes = self._extract_programme_outcomes_from_competencies(enhanced_competencies)
        career_progression = self._generate_career_progression_enhanced(role_id, eqf_level, role_info)
        modular_structure = self._generate_modular_structure_from_competencies(
            enhanced_competencies, target_ects, eqf_level
        )
        
        # Additional rich profile sections
        assessment_methods = self._extract_assessment_methods_from_competencies(enhanced_competencies)
        entry_requirements = self._generate_entry_requirements_enhanced(role_id, eqf_level, topic)
        professional_recognition = self._generate_professional_recognition_enhanced(role_id, role_info)
        role_context = self._extract_role_context_enhanced(role_info)
        
        # Compile comprehensive profile
        rich_profile = {
            **profile_metadata,
            'enhanced_competencies': enhanced_competencies,
            'sustainability_competencies': enhanced_competencies,  # Alias for compatibility
            'learning_outcomes_programme': programme_outcomes,
            'realistic_career_progression': career_progression,
            'modular_structure': modular_structure,
            'assessment_methods': assessment_methods,
            'entry_requirements': entry_requirements,
            'professional_recognition': professional_recognition,
            'role_context': role_context,
            'competency_requirements': self._generate_competency_requirements_from_json(enhanced_competencies),
            
            # T3.2/T3.4 Compliance metadata
            't3_compliance': self._generate_t3_compliance_metadata(enhanced_competencies, target_ects),
            'micro_credentials': self._generate_micro_credentials_framework(enhanced_competencies),
            'learning_pathways': self._generate_learning_pathways_from_competencies(enhanced_competencies, target_ects)
        }
        
        return rich_profile

    def _adapt_json_competencies_for_topic(
        self, json_competencies: List[Dict], topic: str, eqf_level: int
    ) -> List[Dict[str, Any]]:
        """Adapt JSON competencies for specific topic and EQF level"""
        
        adapted_competencies = []
        
        for comp in json_competencies:
            # Keep original rich structure from JSON
            adapted_comp = {
                'competency_name': comp.get('competency_name', 'Unknown Competency'),
                'competency_level': comp.get('competency_level', 'Proficient'),
                'competency_category': 'Professional',  # Default category
                'eqf_alignment': comp.get('eqf_alignment', f'Level {eqf_level}'),
                'learning_outcomes': comp.get('learning_outcomes', []),
                'framework_mappings': comp.get('framework_mappings', {}),
                'assessment_methods': self._extract_assessment_methods_from_comp(comp),
                'module_requirements': self._extract_module_requirements_from_outcomes(
                    comp.get('learning_outcomes', [])
                )
            }
            
            # Add topic adaptation if relevant
            if topic and topic.lower() not in adapted_comp['competency_name'].lower():
                adapted_comp['topic_relevance'] = self._assess_topic_relevance(comp, topic)
                adapted_comp['topic_adaptation'] = self._suggest_topic_adaptation(comp, topic)
            
            adapted_competencies.append(adapted_comp)
        
        print(f"   ✅ Adapted {len(adapted_competencies)} JSON competencies for {topic}")
        return adapted_competencies

    def _extract_programme_outcomes_from_competencies(self, competencies: List[Dict]) -> List[str]:
        """Extract programme-level learning outcomes from competency data"""
        
        programme_outcomes = []
        
        # Extract high-level outcomes from each competency
        for comp in competencies:
            learning_outcomes = comp.get('learning_outcomes', [])
            if learning_outcomes:
                # Take the most comprehensive outcome from each competency for programme level
                programme_outcomes.append(learning_outcomes[0])
        
        # Add programme-level synthesis outcomes
        programme_outcomes.extend([
            "Integrate sustainability principles across professional practice",
            "Demonstrate critical thinking in complex sustainability challenges",
            "Communicate effectively with diverse stakeholders on sustainability issues",
            "Apply evidence-based approaches to sustainability problem-solving"
        ])
        
        return programme_outcomes[:8]  # Limit to reasonable number

    def _generate_modular_structure_from_competencies(
        self, competencies: List[Dict], target_ects: int, eqf_level: int
    ) -> Dict[str, Any]:
        """Generate modular structure based on actual competency requirements"""
        
        # Calculate modules needed for competencies
        competency_modules = {}
        total_estimated_modules = 0
        
        for comp in competencies:
            comp_name = comp['competency_name']
            learning_outcomes = comp.get('learning_outcomes', [])
            
            # Estimate modules needed (roughly 1 module per 2-3 learning outcomes)
            estimated_modules = max(1, len(learning_outcomes) // 2)
            competency_modules[comp_name] = estimated_modules
            total_estimated_modules += estimated_modules
        
        # Ensure reasonable total (8-16 modules for most programmes)
        recommended_modules = min(16, max(8, total_estimated_modules))
        
        return {
            'total_modules': recommended_modules,
            'target_ects': target_ects,
            'ects_per_module': target_ects // recommended_modules if recommended_modules > 0 else 5,
            'semesters': max(1, target_ects // 30),  # Assume 30 ECTS per semester
            'competency_module_mapping': competency_modules,
            'flexibility_options': {
                'core_modules': recommended_modules // 2,
                'elective_modules': recommended_modules - (recommended_modules // 2),
                'pathway_options': ['Generalist', 'Specialist', 'Research-focused']
            },
            'learning_sequence': self._generate_learning_sequence(competencies)
        }

    def _generate_t3_compliance_metadata(self, competencies: List[Dict], target_ects: int) -> Dict[str, Any]:
        """Generate T3.2/T3.4 compliance metadata"""
        
        return {
            'eqf_referenced': True,
            'ects_compliant': True,
            'learning_outcomes_defined': len(competencies) > 0,
            'competency_based': True,
            'modular_design': True,
            'micro_credentials_enabled': True,
            'work_based_learning': self._assess_work_based_learning(competencies),
            'quality_assurance': {
                'framework_aligned': True,
                'assessment_criteria_defined': True,
                'recognition_pathways': True
            },
            'stackable_credentials': True,
            'flexible_pathways': True
        }

    def _generate_micro_credentials_framework(self, competencies: List[Dict]) -> Dict[str, Any]:
        """Generate micro-credentials framework from competencies"""
        
        micro_credentials = []
        
        for comp in competencies:
            comp_name = comp['competency_name']
            learning_outcomes = comp.get('learning_outcomes', [])
            
            # Each competency can be a micro-credential
            micro_credential = {
                'credential_name': f"Micro-Credential: {comp_name}",
                'ects_value': len(learning_outcomes),  # Rough estimate
                'learning_outcomes': learning_outcomes[:3],  # Top 3 outcomes
                'assessment_methods': comp.get('assessment_methods', ['Portfolio', 'Assessment']),
                'stackable_with': [other_comp['competency_name'] for other_comp in competencies if other_comp != comp],
                'recognition_level': 'Professional'
            }
            
            micro_credentials.append(micro_credential)
        
        return {
            'available_micro_credentials': micro_credentials,
            'stacking_rules': {
                'minimum_credits': 3,
                'maximum_credits': 15,
                'prerequisite_checking': True
            },
            'recognition_framework': {
                'digital_badges': True,
                'blockchain_verified': True,
                'industry_recognized': True
            }
        }

    def _generate_learning_pathways_from_competencies(
        self, competencies: List[Dict], target_ects: int
    ) -> Dict[str, Any]:
        """Generate flexible learning pathways based on competencies"""
        
        # Group competencies by type/category
        technical_comps = [c for c in competencies if 'technical' in c.get('competency_name', '').lower() or 'data' in c.get('competency_name', '').lower()]
        management_comps = [c for c in competencies if 'management' in c.get('competency_name', '').lower() or 'leadership' in c.get('competency_name', '').lower()]
        communication_comps = [c for c in competencies if 'communication' in c.get('competency_name', '').lower() or 'stakeholder' in c.get('competency_name', '').lower()]
        
        pathways = {
            'technical_specialist': {
                'name': 'Technical Specialist Pathway',
                'focus': 'Deep technical competencies',
                'competencies': [c['competency_name'] for c in technical_comps],
                'ects_allocation': target_ects * 0.7,  # 70% technical
                'duration': '2-3 semesters'
            },
            'management_track': {
                'name': 'Management Track Pathway', 
                'focus': 'Leadership and management competencies',
                'competencies': [c['competency_name'] for c in management_comps],
                'ects_allocation': target_ects * 0.6,  # 60% management
                'duration': '2-3 semesters'
            },
            'generalist': {
                'name': 'Generalist Pathway',
                'focus': 'Balanced competency development',
                'competencies': [c['competency_name'] for c in competencies[:6]],  # Balanced selection
                'ects_allocation': target_ects,
                'duration': '3-4 semesters'
            }
        }
        
        return {
            'available_pathways': pathways,
            'pathway_flexibility': 85,  # High flexibility score
            'customization_options': ['Self-paced', 'Accelerated', 'Part-time'],
            'entry_points': ['Beginner', 'Intermediate', 'Advanced']
        }

    # Helper methods
    def _extract_assessment_methods_from_competencies(self, competencies: List[Dict]) -> List[str]:
        """Extract unique assessment methods from all competencies"""
        methods = set()
        
        for comp in competencies:
            # Extract from learning outcomes (infer assessment methods)
            outcomes = comp.get('learning_outcomes', [])
            for outcome in outcomes:
                if 'design' in outcome.lower() or 'develop' in outcome.lower():
                    methods.add('Portfolio')
                    methods.add('Project work')
                elif 'analyze' in outcome.lower() or 'evaluate' in outcome.lower():
                    methods.add('Case study analysis')
                    methods.add('Report writing')
                elif 'implement' in outcome.lower() or 'configure' in outcome.lower():
                    methods.add('Practical assessment')
                    methods.add('Technical demonstration')
        
        # Add standard methods
        methods.update(['Competency assessment', 'Peer evaluation', 'Professional presentation'])
        
        return list(methods)

    def _extract_assessment_methods_from_comp(self, comp: Dict) -> List[str]:
        """Extract assessment methods for individual competency"""
        methods = ['Portfolio', 'Competency assessment']
        
        outcomes = comp.get('learning_outcomes', [])
        for outcome in outcomes:
            if 'design' in outcome.lower():
                methods.append('Design portfolio')
            elif 'analyze' in outcome.lower():
                methods.append('Data analysis project')
            elif 'implement' in outcome.lower():
                methods.append('Practical project')
        
        return list(set(methods))

    def _extract_module_requirements_from_outcomes(self, learning_outcomes: List[str]) -> List[str]:
        """Extract module requirements from learning outcomes"""
        requirements = []
        
        for outcome in learning_outcomes:
            outcome_lower = outcome.lower()
            if 'statistical' in outcome_lower or 'data' in outcome_lower:
                requirements.extend(['Statistics', 'Data analysis'])
            elif 'machine learning' in outcome_lower or 'ai' in outcome_lower:
                requirements.extend(['Machine learning', 'AI fundamentals'])
            elif 'dashboard' in outcome_lower or 'visualization' in outcome_lower:
                requirements.extend(['Data visualization', 'Business intelligence'])
            elif 'sustainability' in outcome_lower or 'environmental' in outcome_lower:
                requirements.extend(['Sustainability principles', 'Environmental management'])
        
        return list(set(requirements))

    def _assess_topic_relevance(self, comp: Dict, topic: str) -> float:
        """Assess how relevant a competency is to the topic"""
        comp_text = f"{comp.get('competency_name', '')} {' '.join(comp.get('learning_outcomes', []))}"
        topic_words = topic.lower().split()
        
        relevance_score = 0
        for word in topic_words:
            if word in comp_text.lower():
                relevance_score += 1
        
        return min(1.0, relevance_score / len(topic_words))

    def _suggest_topic_adaptation(self, comp: Dict, topic: str) -> str:
        """Suggest how to adapt competency for specific topic"""
        return f"Apply {comp.get('competency_name', 'competency')} specifically to {topic} contexts"

    def _assess_work_based_learning(self, competencies: List[Dict]) -> bool:
        """Assess if competencies include work-based learning elements"""
        for comp in competencies:
            outcomes = comp.get('learning_outcomes', [])
            for outcome in outcomes:
                if 'implement' in outcome.lower() or 'configure' in outcome.lower() or 'apply' in outcome.lower():
                    return True
        return False

    def _generate_learning_sequence(self, competencies: List[Dict]) -> List[str]:
        """Generate logical learning sequence for competencies"""
        # Simple heuristic: foundational -> technical -> applied
        foundational = []
        technical = []
        applied = []
        
        for comp in competencies:
            comp_name = comp['competency_name']
            if 'understanding' in comp_name.lower() or 'principles' in comp_name.lower():
                foundational.append(comp_name)
            elif 'advanced' in comp_name.lower() or 'analytics' in comp_name.lower():
                technical.append(comp_name)
            else:
                applied.append(comp_name)
        
        return foundational + technical + applied

    def _build_fallback_profile(self, role_id: str, role_name: str, topic: str, eqf_level: int, target_ects: int, role_info: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback profile builder if JSON data not available"""
        
        return {
            'profile_id': f"FALLBACK_{role_id}_{eqf_level}",
            'role_id': role_id,
            'role_name': role_name,
            'profile_type': 'fallback_generated',
            'enhanced_competencies': [],
            'learning_outcomes_programme': [f"Complete {role_name} programme successfully"],
            'realistic_career_progression': {},
            'modular_structure': {'total_modules': 12, 'target_ects': target_ects}
        }

    def _generate_enhanced_metadata(self, role_id: str, role_name: str, topic: str, eqf_level: int, target_ects: int) -> Dict[str, Any]:
        """Generate enhanced profile metadata"""
        
        return {
            'profile_id': f"EP_{role_id}_{eqf_level}_{datetime.now().strftime('%Y%m%d')}",
            'role_id': role_id,
            'role_name': role_name,
            'profile_title': f"{role_name} Educational Profile",
            'profile_type': 'enhanced_standard',
            'creation_date': datetime.now().isoformat(),
            'version': '3.2_json_integrated',
            'target_eqf_level': eqf_level,
            'target_ects': target_ects,
            'topic_focus': topic,
            'generation_mode': 'json_data_driven',
            'compliance_level': 'T3.2_T3.4_compliant'
        }

    def _generate_competency_requirements_from_json(self, competencies: List[Dict]) -> Dict[str, Any]:
        """Generate module requirements from JSON competency data"""
        
        requirements = {
            'required_topics': [],
            'required_thematic_areas': [],
            'competency_module_mapping': {},
            'assessment_requirements': [],
            'minimum_ects_per_category': {}
        }
        
        for comp in competencies:
            comp_name = comp['competency_name']
            
            # Extract required topics from learning outcomes
            module_reqs = comp.get('module_requirements', [])
            requirements['required_topics'].extend(module_reqs)
            
            # Map competency to requirements
            requirements['competency_module_mapping'][comp_name] = {
                'required_modules': module_reqs,
                'assessment_methods': comp.get('assessment_methods', []),
                'learning_outcomes': comp.get('learning_outcomes', [])
            }
            
            # Extract assessment requirements
            assessment_methods = comp.get('assessment_methods', [])
            requirements['assessment_requirements'].extend(assessment_methods)
        
        # Remove duplicates
        requirements['required_topics'] = list(set(requirements['required_topics']))
        requirements['assessment_requirements'] = list(set(requirements['assessment_requirements']))
        
        return requirements

    # Additional helper methods for enhanced functionality
    def _generate_career_progression_enhanced(self, role_id: str, eqf_level: int, role_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced career progression with realistic data"""
        
        base_salary = {'DAN': 45000, 'SSD': 50000}.get(role_id, 45000)
        
        progression = {
            'immediate': {
                'timeframe': '0-2 years',
                'salary_range': f'€{base_salary:,} - €{base_salary + 15000:,}',
                'roles': [f'Junior {role_info.get("name", "Professional")}', 'Sustainability Analyst', 'Data Specialist']
            },
            'short_term': {
                'timeframe': '2-5 years', 
                'salary_range': f'€{base_salary + 15000:,} - €{base_salary + 35000:,}',
                'roles': [f'Senior {role_info.get("name", "Professional")}', 'Team Lead', 'Sustainability Manager']
            },
            'long_term': {
                'timeframe': '5+ years',
                'salary_range': f'€{base_salary + 35000:,} - €{base_salary + 60000:,}',
                'roles': ['Director', 'Chief Sustainability Officer', 'Practice Leader']
            }
        }
        
        return progression

    def _generate_entry_requirements_enhanced(self, role_id: str, eqf_level: int, topic: str) -> Dict[str, str]:
        """Generate enhanced entry requirements"""
        
        requirements = {}
        
        if eqf_level >= 7:
            requirements['academic'] = "Bachelor's degree with honours (2:1 or equivalent) in relevant field"
            requirements['professional'] = "Minimum 2-3 years relevant professional experience"
            requirements['english'] = "IELTS 6.5 or equivalent (for non-native speakers)"
        else:
            requirements['academic'] = "Bachelor's degree or equivalent professional qualification"
            requirements['professional'] = "Some relevant experience preferred but not essential"
            requirements['english'] = "IELTS 6.0 or equivalent (for non-native speakers)"
        
        requirements['technical'] = f"Basic understanding of {topic} and sustainability principles"
        requirements['digital'] = "Proficiency with digital tools and online learning platforms"
        requirements['motivation'] = "Demonstrated interest in sustainable development"
        
        return requirements

    def _generate_professional_recognition_enhanced(self, role_id: str, role_info: Dict) -> Dict[str, Any]:
        """Generate enhanced professional recognition framework"""
        
        return {
            'professional_bodies': [
                'Institute for Sustainable Business',
                'Digital Sustainability Network',
                f'{role_id} Professional Association'
            ],
            'certification_pathways': [
                'Certified Digital Sustainability Professional (CDSP)',
                f'Advanced {role_info.get("name", "Professional")} Certification',
                'Micro-credentials in Sustainability Leadership'
            ],
            'cpd_requirements': {
                'annual_hours': 30,
                'certification_maintenance': '60 hours every 3 years',
                'conference_participation': 'Annual professional development conference',
                'professional_networking': 'Active participation in professional communities',
                'reflection_practice': 'Annual reflective practice portfolio'
            },
            'accreditation': {
                'eu_recognition': True,
                'international_recognition': True,
                'industry_partnerships': True
            },
            'quality_assurance': {
                'external_review': 'Annual',
                'student_feedback': 'Continuous',
                'employer_feedback': 'Bi-annual',
                'industry_advisory': 'Quarterly board meetings'
            }
        }

    def _extract_role_context_enhanced(self, role_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract enhanced role context information"""
        
        return {
            'main_area': role_info.get('main_area', 'Digital Sustainability'),
            'industry_sectors': role_info.get('industry_sectors', [
                'Technology', 'Consulting', 'Public Sector', 'NGOs', 'Research'
            ]),
            'career_pathways': role_info.get('career_pathways', [
                'Technical specialist', 'Management track', 'Consulting', 'Research and development'
            ]),
            'typical_employers': role_info.get('typical_employers', [
                'Technology companies', 'Sustainability consultancies', 'Government agencies',
                'International organizations', 'Research institutions'
            ]),
            'geographic_opportunities': [
                'Europe', 'North America', 'Asia-Pacific', 'Remote/Global'
            ],
            'employment_types': [
                'Full-time permanent', 'Contract/Freelance', 'Part-time', 'Remote work'
            ]
        }
