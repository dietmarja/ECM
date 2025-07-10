# scripts/curriculum_generator/components/t32_t34_compliance_manager.py
"""
T3.2/T3.4 Compliance Manager
Adds explicit learning outcomes, competency mapping, and framework alignment
Addresses gaps in ECVET/ECTS referencing and cross-recognition requirements
"""

from typing import Dict, List, Any, Optional
import json
from pathlib import Path

class T32T34ComplianceManager:
    """Manages T3.2/T3.4 compliance requirements"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.eqf_descriptors = self._load_eqf_descriptors()
        self.framework_mappings = self._load_framework_mappings()
        self.wp2_role_competencies = self._load_wp2_competencies()
        
        print(f"✅ T3.2/T3.4 Compliance Manager initialized")
        print(f"   📋 EQF descriptors: {len(self.eqf_descriptors)} levels")
        print(f"   🗺️ Framework mappings: {len(self.framework_mappings)} frameworks")
        print(f"   🎯 WP2 competencies: {len(self.wp2_role_competencies)} roles")

    def _load_eqf_descriptors(self) -> Dict[int, Dict[str, str]]:
        """Load EQF level descriptors for learning outcomes alignment"""
        return {
            4: {
                "knowledge": "Factual and theoretical knowledge in broad contexts within a field of work or study",
                "skills": "A range of cognitive and practical skills required to generate solutions to specific problems in a field of work or study",
                "responsibility": "Exercise self-management within the guidelines of work or study contexts that are usually predictable, but are subject to change"
            },
            5: {
                "knowledge": "Comprehensive, specialised, factual and theoretical knowledge within a field of work or study and an awareness of the boundaries of that knowledge",
                "skills": "A comprehensive range of cognitive and practical skills required to develop creative solutions to abstract problems",
                "responsibility": "Exercise management and supervision in contexts of work or study activities where there is unpredictable change"
            },
            6: {
                "knowledge": "Advanced knowledge of a field of work or study, involving a critical understanding of theories and principles",
                "skills": "Advanced skills, demonstrating mastery and innovation, required to solve complex and unpredictable problems in a specialised field of work or study",
                "responsibility": "Manage complex technical or professional activities or projects, taking responsibility for decision-making in unpredictable work or study contexts"
            },
            7: {
                "knowledge": "Highly specialised knowledge, some of which is at the forefront of knowledge in a field of work or study, as the basis for original thinking and/or research",
                "skills": "Specialised problem-solving skills required in research and/or innovation in order to develop new knowledge and procedures and to integrate knowledge from different fields",
                "responsibility": "Manage and transform work or study contexts that are complex, unpredictable and require new strategic approaches"
            },
            8: {
                "knowledge": "Knowledge at the most advanced frontier of a field of work or study and at the interface between fields",
                "skills": "The most advanced and specialised skills and techniques, including synthesis and evaluation, required to solve critical problems in research and/or innovation and to extend and redefine existing knowledge or professional practice",
                "responsibility": "Demonstrate substantial authority, innovation, autonomy, scholarly and professional integrity and sustained commitment to the development of new ideas or processes at the forefront of work or study contexts including research"
            }
        }

    def _load_framework_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Load framework mappings for competency alignment"""
        return {
            "e_cf": {
                "name": "European e-Competence Framework",
                "version": "3.0",
                "competencies": {
                    "A.1": "IS and Business Strategy Alignment",
                    "A.2": "Service Level Management", 
                    "A.3": "Business Plan Development",
                    "A.4": "Product/Service Planning",
                    "A.5": "Architecture Design",
                    "B.1": "Application Development",
                    "B.2": "Component Integration",
                    "B.3": "Testing",
                    "B.4": "Solution Deployment",
                    "B.5": "Documentation Production",
                    "C.1": "User Support",
                    "C.2": "Change Support",
                    "C.3": "Service Delivery",
                    "C.4": "Problem Management",
                    "D.1": "Information Security Strategy Development",
                    "D.2": "ICT Quality Strategy Development",
                    "D.3": "Education and Training Provision",
                    "D.4": "Purchasing",
                    "D.5": "Sales Development",
                    "D.6": "Channel Management",
                    "D.7": "Sales Management",
                    "D.8": "Contract Management",
                    "D.9": "Personnel Development",
                    "D.10": "Information and Knowledge Management",
                    "D.11": "Needs Identification",
                    "D.12": "Digital Marketing",
                    "E.1": "Forecast Development",
                    "E.2": "Project and Portfolio Management",
                    "E.3": "Risk Management",
                    "E.4": "Relationship Management",
                    "E.5": "Process Improvement",
                    "E.6": "ICT Quality Management",
                    "E.7": "Business Change Management",
                    "E.8": "Information Security Management",
                    "E.9": "IS Governance"
                }
            },
            "digcomp": {
                "name": "Digital Competence Framework for Citizens",
                "version": "2.2",
                "areas": {
                    "1": "Information and data literacy",
                    "2": "Communication and collaboration", 
                    "3": "Digital content creation",
                    "4": "Safety",
                    "5": "Problem solving"
                },
                "competencies": {
                    "1.1": "Browsing, searching and filtering data, information and digital content",
                    "1.2": "Evaluating data, information and digital content",
                    "1.3": "Managing data, information and digital content",
                    "2.1": "Interacting through digital technologies",
                    "2.2": "Sharing through digital technologies",
                    "2.3": "Engaging in citizenship through digital technologies",
                    "2.4": "Collaborating through digital technologies",
                    "2.5": "Netiquette",
                    "2.6": "Managing digital identity",
                    "3.1": "Developing digital content",
                    "3.2": "Integrating and re-elaborating digital content",
                    "3.3": "Copyright and licences",
                    "3.4": "Programming",
                    "4.1": "Protecting devices",
                    "4.2": "Protecting personal data and privacy",
                    "4.3": "Protecting health and well-being",
                    "4.4": "Protecting the environment",
                    "5.1": "Solving technical problems",
                    "5.2": "Identifying needs and technological responses",
                    "5.3": "Creatively using digital technologies",
                    "5.4": "Identifying digital competence gaps"
                }
            },
            "greencomp": {
                "name": "European sustainability competence framework",
                "version": "1.0",
                "areas": {
                    "1": "Embodying sustainability values",
                    "2": "Embracing complexity in sustainability",
                    "3": "Envisioning sustainable futures",
                    "4": "Acting for sustainability"
                },
                "competencies": {
                    "1.1": "Valuing sustainability",
                    "1.2": "Supporting fairness",
                    "1.3": "Promoting nature",
                    "2.1": "Systems thinking",
                    "2.2": "Critical thinking",
                    "2.3": "Problem framing",
                    "3.1": "Futures literacy",
                    "3.2": "Adaptability",
                    "3.3": "Exploratory thinking",
                    "4.1": "Political agency",
                    "4.2": "Collective action",
                    "4.3": "Individual initiative"
                }
            }
        }

    def _load_wp2_competencies(self) -> Dict[str, Dict[str, Any]]:
        """Load WP2 identified role competencies"""
        return {
            "DAN": {
                "role_name": "Data Analyst",
                "core_competencies": [
                    "Statistical analysis and data interpretation",
                    "Data visualization and dashboard creation",
                    "Environmental data analysis",
                    "Carbon footprint measurement",
                    "Evidence-based reporting",
                    "Stakeholder communication"
                ],
                "technical_skills": [
                    "Data analysis tools (Python, R, SQL)",
                    "Visualization software (Tableau, PowerBI)",
                    "Statistical methods and modeling",
                    "Database management",
                    "Report generation"
                ],
                "sustainability_focus": [
                    "Environmental data interpretation",
                    "Sustainability metrics analysis",
                    "Carbon accounting",
                    "Life cycle assessment data",
                    "ESG reporting"
                ]
            },
            "DSM": {
                "role_name": "Digital Sustainability Manager",
                "core_competencies": [
                    "Strategic sustainability planning",
                    "Digital transformation leadership",
                    "Change management",
                    "Stakeholder engagement",
                    "Performance monitoring",
                    "Team leadership"
                ],
                "technical_skills": [
                    "Project management tools",
                    "Strategy development frameworks",
                    "Performance measurement systems",
                    "Digital platform management",
                    "Communication technologies"
                ],
                "sustainability_focus": [
                    "Sustainable business model design",
                    "Digital sustainability frameworks",
                    "Green IT strategies",
                    "Circular economy principles",
                    "ESG integration"
                ]
            },
            "DSE": {
                "role_name": "Data Scientist (Sustainability)",
                "core_competencies": [
                    "Machine learning and AI",
                    "Predictive modeling",
                    "Big data analytics",
                    "Research methodology",
                    "Algorithm development"
                ],
                "technical_skills": [
                    "Python/R programming",
                    "Machine learning frameworks",
                    "Cloud computing platforms",
                    "Data engineering tools",
                    "API development"
                ],
                "sustainability_focus": [
                    "Environmental modeling",
                    "Climate data analysis",
                    "Sustainability prediction models",
                    "Resource optimization algorithms",
                    "Impact assessment tools"
                ]
            }
        }

    def generate_tuning_learning_outcomes(self, unit: Dict[str, Any], role_id: str, eqf_level: int) -> List[str]:
        """Generate Tuning-style learning outcomes ('The learner will be able to...')"""
        
        unit_name = unit.get('title', unit.get('name', 'Unit'))
        unit_topics = unit.get('topics', unit.get('rich_topics', []))
        unit_type = unit.get('unit_type', 'professional')
        
        # Get EQF descriptors for this level
        eqf_desc = self.eqf_descriptors.get(eqf_level, self.eqf_descriptors[6])
        
        # Generate outcomes based on EQF level and unit type
        outcomes = []
        
        # Knowledge outcomes
        if unit_topics:
            primary_topic = unit_topics[0]
            outcomes.append(f"The learner will be able to explain the fundamental concepts and principles of {primary_topic.lower()} within sustainability contexts")
            
            if len(unit_topics) > 1:
                secondary_topic = unit_topics[1]
                outcomes.append(f"The learner will be able to describe the relationship between {primary_topic.lower()} and {secondary_topic.lower()}")
        
        # Skills outcomes based on EQF level
        if eqf_level >= 6:
            outcomes.append(f"The learner will be able to apply advanced {unit_name.lower()} techniques to solve complex sustainability challenges")
            outcomes.append(f"The learner will be able to critically analyze {unit_name.lower()} solutions and recommend improvements")
        elif eqf_level >= 4:
            outcomes.append(f"The learner will be able to use {unit_name.lower()} methods to address specific sustainability problems")
            outcomes.append(f"The learner will be able to implement {unit_name.lower()} solutions in professional contexts")
        
        # Role-specific outcomes
        role_competencies = self.wp2_role_competencies.get(role_id, {})
        if role_competencies:
            core_comps = role_competencies.get('core_competencies', [])
            if core_comps:
                relevant_comp = next((comp for comp in core_comps if any(topic.lower() in comp.lower() for topic in unit_topics)), core_comps[0])
                outcomes.append(f"The learner will be able to demonstrate {relevant_comp.lower()} in professional {role_id} practice")
        
        # Responsibility/autonomy outcomes
        if eqf_level >= 7:
            outcomes.append(f"The learner will be able to lead {unit_name.lower()} initiatives and manage complex stakeholder relationships")
        elif eqf_level >= 6:
            outcomes.append(f"The learner will be able to take responsibility for {unit_name.lower()} decisions in unpredictable professional contexts")
        elif eqf_level >= 4:
            outcomes.append(f"The learner will be able to work independently on {unit_name.lower()} tasks within established guidelines")
        
        return outcomes[:5]  # Limit to 5 key outcomes

    def generate_competency_mapping(self, unit: Dict[str, Any], role_id: str) -> Dict[str, Any]:
        """Generate explicit competency mapping to frameworks and WP2 role framework"""
        
        unit_topics = unit.get('topics', unit.get('rich_topics', []))
        unit_name = unit.get('title', unit.get('name', 'Unit'))
        
        # Map to e-CF competencies
        ecf_mappings = []
        for topic in unit_topics[:3]:
            if 'data' in topic.lower() or 'analytic' in topic.lower():
                ecf_mappings.extend(['D.10', 'D.11'])  # Information Management, Needs Identification
            elif 'manage' in topic.lower() or 'strategy' in topic.lower():
                ecf_mappings.extend(['A.1', 'E.2'])  # Strategy Alignment, Project Management
            elif 'system' in topic.lower() or 'technical' in topic.lower():
                ecf_mappings.extend(['A.5', 'B.4'])  # Architecture Design, Solution Deployment
        
        # Remove duplicates and limit
        ecf_mappings = list(set(ecf_mappings))[:4]
        
        # Map to DigComp competencies
        digcomp_mappings = []
        for topic in unit_topics[:3]:
            if 'data' in topic.lower():
                digcomp_mappings.extend(['1.1', '1.2', '1.3'])  # Information and data literacy
            elif 'communication' in topic.lower() or 'collaboration' in topic.lower():
                digcomp_mappings.extend(['2.1', '2.4'])  # Communication and collaboration
            elif 'digital' in topic.lower() or 'technology' in topic.lower():
                digcomp_mappings.extend(['5.1', '5.2'])  # Problem solving
        
        digcomp_mappings = list(set(digcomp_mappings))[:4]
        
        # Map to GreenComp competencies
        greencomp_mappings = []
        if 'sustainability' in unit_name.lower() or any('sustain' in topic.lower() for topic in unit_topics):
            greencomp_mappings.extend(['1.1', '2.1', '4.3'])  # Valuing sustainability, Systems thinking, Individual initiative
        
        # Map to WP2 role competencies
        wp2_mappings = []
        role_data = self.wp2_role_competencies.get(role_id, {})
        if role_data:
            # Map to core competencies
            for comp in role_data.get('core_competencies', [])[:3]:
                if any(topic.lower() in comp.lower() for topic in unit_topics):
                    wp2_mappings.append({
                        'competency': comp,
                        'category': 'core_competency',
                        'alignment_strength': 'high'
                    })
            
            # Map to technical skills
            for skill in role_data.get('technical_skills', [])[:2]:
                if any(topic.lower() in skill.lower() for topic in unit_topics):
                    wp2_mappings.append({
                        'competency': skill,
                        'category': 'technical_skill',
                        'alignment_strength': 'medium'
                    })
        
        return {
            'unit_id': unit.get('id', 'unknown'),
            'unit_name': unit_name,
            'framework_mappings': {
                'e_cf': {
                    'mapped_competencies': [
                        {
                            'code': code,
                            'name': self.framework_mappings['e_cf']['competencies'].get(code, 'Unknown'),
                            'relevance': 'high' if i < 2 else 'medium'
                        }
                        for i, code in enumerate(ecf_mappings)
                    ]
                },
                'digcomp': {
                    'mapped_competencies': [
                        {
                            'code': code,
                            'name': self.framework_mappings['digcomp']['competencies'].get(code, 'Unknown'),
                            'relevance': 'high' if i < 2 else 'medium'
                        }
                        for i, code in enumerate(digcomp_mappings)
                    ]
                },
                'greencomp': {
                    'mapped_competencies': [
                        {
                            'code': code,
                            'name': self.framework_mappings['greencomp']['competencies'].get(code, 'Unknown'),
                            'relevance': 'high'
                        }
                        for code in greencomp_mappings
                    ]
                }
            },
            'wp2_role_mappings': wp2_mappings,
            'ecvet_ects_referencing': {
                'ects_value': unit.get('ects', unit.get('ects_points', 0)),
                'learning_outcomes_count': len(unit.get('learning_outcomes', [])),
                'assessment_methods': unit.get('assessment_method', 'Not specified'),
                'transferability': 'high' if len(ecf_mappings) > 2 else 'medium'
            }
        }

    def create_skills_matrix(self, curriculum: Dict[str, Any], role_id: str) -> Dict[str, Any]:
        """Create skills matrix showing mapping of micro-units to job-role skills"""
        
        content_key = 'modules' if 'modules' in curriculum else 'micro_units'
        content_units = curriculum.get(content_key, [])
        
        role_data = self.wp2_role_competencies.get(role_id, {})
        all_competencies = (
            role_data.get('core_competencies', []) + 
            role_data.get('technical_skills', []) + 
            role_data.get('sustainability_focus', [])
        )
        
        # Create matrix
        matrix = {
            'role_id': role_id,
            'role_name': role_data.get('role_name', f'{role_id} Professional'),
            'total_units': len(content_units),
            'total_competencies': len(all_competencies),
            'matrix_data': [],
            'coverage_analysis': {},
            'compliance_indicators': {}
        }
        
        # Build matrix data
        for unit in content_units:
            unit_name = unit.get('title', unit.get('name', 'Unit'))
            unit_topics = unit.get('topics', unit.get('rich_topics', []))
            
            unit_mapping = {
                'unit_name': unit_name,
                'unit_id': unit.get('id', 'unknown'),
                'ects': unit.get('ects', unit.get('ects_points', 0)),
                'competency_coverage': []
            }
            
            # Check coverage of each competency
            for comp in all_competencies:
                coverage_score = 0
                coverage_rationale = []
                
                # Check if unit topics relate to competency
                for topic in unit_topics:
                    if any(word in comp.lower() for word in topic.lower().split() if len(word) > 3):
                        coverage_score += 1
                        coverage_rationale.append(f"Topic '{topic}' relates to competency")
                
                # Check unit name relevance
                if any(word in comp.lower() for word in unit_name.lower().split() if len(word) > 3):
                    coverage_score += 1
                    coverage_rationale.append(f"Unit name relates to competency")
                
                # Determine coverage level
                if coverage_score >= 2:
                    coverage_level = 'high'
                elif coverage_score == 1:
                    coverage_level = 'medium'
                else:
                    coverage_level = 'low'
                
                unit_mapping['competency_coverage'].append({
                    'competency': comp,
                    'coverage_level': coverage_level,
                    'coverage_score': coverage_score,
                    'rationale': coverage_rationale
                })
            
            matrix['matrix_data'].append(unit_mapping)
        
        # Coverage analysis
        competency_coverage = {}
        for comp in all_competencies:
            high_coverage = sum(1 for unit in matrix['matrix_data'] 
                              for cov in unit['competency_coverage'] 
                              if cov['competency'] == comp and cov['coverage_level'] == 'high')
            medium_coverage = sum(1 for unit in matrix['matrix_data'] 
                                for cov in unit['competency_coverage'] 
                                if cov['competency'] == comp and cov['coverage_level'] == 'medium')
            
            competency_coverage[comp] = {
                'high_coverage_units': high_coverage,
                'medium_coverage_units': medium_coverage,
                'total_coverage_units': high_coverage + medium_coverage,
                'coverage_percentage': ((high_coverage * 2 + medium_coverage) / (len(content_units) * 2)) * 100
            }
        
        matrix['coverage_analysis'] = competency_coverage
        
        # Compliance indicators
        well_covered_competencies = sum(1 for comp_data in competency_coverage.values() 
                                      if comp_data['coverage_percentage'] >= 50)
        
        matrix['compliance_indicators'] = {
            'overall_coverage_score': (well_covered_competencies / len(all_competencies)) * 100,
            'well_covered_competencies': well_covered_competencies,
            'total_competencies': len(all_competencies),
            't32_compliance': well_covered_competencies >= len(all_competencies) * 0.7,  # 70% threshold
            't34_compliance': len(content_units) > 0 and all(unit.get('ects', 0) > 0 for unit in content_units),
            'ecvet_ready': True,
            'cross_recognition_ready': well_covered_competencies >= len(all_competencies) * 0.8  # 80% threshold
        }
        
        return matrix

    def enhance_curriculum_with_compliance(self, curriculum: Dict[str, Any], role_id: str) -> Dict[str, Any]:
        """Enhance curriculum with full T3.2/T3.4 compliance features"""
        
        print(f"\n🔧 Enhancing curriculum with T3.2/T3.4 compliance...")
        
        content_key = 'modules' if 'modules' in curriculum else 'micro_units'
        content_units = curriculum.get(content_key, [])
        eqf_level = curriculum.get('metadata', {}).get('eqf_level', 6)
        
        # Enhance each unit with compliance features
        enhanced_units = []
        for unit in content_units:
            enhanced_unit = unit.copy()
            
            # Add Tuning-style learning outcomes
            enhanced_unit['tuning_learning_outcomes'] = self.generate_tuning_learning_outcomes(unit, role_id, eqf_level)
            
            # Add competency mapping
            enhanced_unit['competency_mapping'] = self.generate_competency_mapping(unit, role_id)
            
            # Add ECVET/ECTS referencing
            enhanced_unit['ecvet_ects_reference'] = {
                'ects_value': unit.get('ects', unit.get('ects_points', 0)),
                'learning_outcomes_count': len(enhanced_unit['tuning_learning_outcomes']),
                'knowledge_outcomes': len([lo for lo in enhanced_unit['tuning_learning_outcomes'] if 'explain' in lo or 'describe' in lo]),
                'skills_outcomes': len([lo for lo in enhanced_unit['tuning_learning_outcomes'] if 'apply' in lo or 'use' in lo or 'demonstrate' in lo]),
                'competence_outcomes': len([lo for lo in enhanced_unit['tuning_learning_outcomes'] if 'manage' in lo or 'lead' in lo or 'responsibility' in lo]),
                'assessment_criteria': enhanced_unit.get('assessment_method', 'Competency-based assessment'),
                'transferability_level': 'high'
            }
            
            enhanced_units.append(enhanced_unit)
        
        # Update curriculum with enhanced units
        curriculum[content_key] = enhanced_units
        
        # Add skills matrix
        curriculum['wp2_skills_matrix'] = self.create_skills_matrix(curriculum, role_id)
        
        # Add compliance indicators
        curriculum['t32_t34_compliance'] = {
            'tuning_outcomes_present': all('tuning_learning_outcomes' in unit for unit in enhanced_units),
            'competency_mapping_present': all('competency_mapping' in unit for unit in enhanced_units),
            'framework_alignment': ['e-CF', 'DigComp', 'GreenComp'],
            'wp2_integration': True,
            'ecvet_ects_ready': all('ecvet_ects_reference' in unit for unit in enhanced_units),
            'cross_recognition_ready': curriculum['wp2_skills_matrix']['compliance_indicators']['cross_recognition_ready'],
            'compliance_score': curriculum['wp2_skills_matrix']['compliance_indicators']['overall_coverage_score']
        }
        
        print(f"✅ T3.2/T3.4 compliance enhancement complete")
        print(f"   📋 Tuning outcomes: {len(enhanced_units)} units enhanced")
        print(f"   🗺️ Competency mapping: Framework alignment added")
        print(f"   📊 Compliance score: {curriculum['t32_t34_compliance']['compliance_score']:.1f}%")
        
        return curriculum
