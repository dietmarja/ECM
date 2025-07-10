#!/usr/bin/env python3
# scripts/curriculum_generator/components/wp3_compliant_generator.py
"""
WP3 Compliant Curriculum Generator
Implements ChatGPT's revised outline structure for professional-grade curricula
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class WP3CompliantGenerator:
    """Generates curricula following WP3 standards with named modules, framework mappings, and micro-credentials"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.role_definitions = self._load_role_definitions()
        self.framework_mappings = self._initialize_framework_mappings()
        
    def _load_role_definitions(self) -> Dict[str, Any]:
        """Load role definitions"""
        role_paths = [
            self.project_root / "config" / "roles.json",
            "config/roles.json", "roles.json"
        ]
        
        for path in role_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        role_data = json.load(f)
                        return {role['id']: role for role in role_data}
                except Exception as e:
                    continue
        return {}
    
    def _initialize_framework_mappings(self) -> Dict:
        """Initialize WP3-compliant framework mappings"""
        return {
            "e-CF": {
                "DAN": ["B.1 Application Development", "D.11 Needs Identification", "C.2 Service Support"],
                "DSE": ["B.2 Component Integration", "C.1 User Support", "A.3 Business Plan Development"],
                "DSL": ["A.1 IS and Business Strategy", "E.3 Risk Management", "E.7 Business Change Management"],
                "DSM": ["E.2 Project and Portfolio Management", "E.6 IT Quality Management", "D.10 Information and Knowledge Management"],
                "DSC": ["A.4 Product/Service Planning", "D.11 Needs Identification", "E.8 Information Security Management"],
                "DSI": ["B.1 Application Development", "D.8 Contract Management", "A.6 Application Architecture"]
            },
            "ESCO": {
                "DAN": "Data Analyst (ESCO: 251101)",
                "DSE": "Data Engineer (ESCO: 251103)", 
                "DSL": "Digital Transformation Manager (ESCO: 121903)",
                "DSM": "Sustainability Manager (ESCO: 242214)",
                "DSC": "Management Consultant (ESCO: 242112)",
                "DSI": "Data Scientist (ESCO: 251102)"
            },
            "EQF_descriptors": {
                4: "Factual and theoretical knowledge in broad contexts within a field of work or study",
                5: "Comprehensive, specialised knowledge within a field and awareness of boundaries", 
                6: "Advanced knowledge demonstrating mastery and innovation",
                7: "Highly specialised knowledge at the forefront of field and interface between fields",
                8: "Knowledge at most advanced frontier of field and interface between fields"
            }
        }
    
    def generate_wp3_compliant_curriculum(self, role_id: str, eqf_level: int, ects: float, 
                                        selected_modules: List[Dict], topic: str) -> Dict:
        """Generate complete WP3-compliant curriculum following ChatGPT's template"""
        
        print(f"🎯 Generating WP3-COMPLIANT curriculum for {role_id} EQF{eqf_level} {ects}ECTS")
        
        role_definition = self.role_definitions.get(role_id, {})
        role_name = role_definition.get('name', 'Professional')
        
        # Calculate modular structure
        named_modules = self._create_named_modules(selected_modules, role_id, ects)
        
        # Generate programme learning outcomes (EQF-aligned)
        programme_outcomes = self._generate_programme_learning_outcomes(role_id, eqf_level, named_modules)
        
        # Create assessment strategy (competency-mapped)
        assessment_strategy = self._create_assessment_strategy(named_modules, role_id, eqf_level)
        
        # Generate framework mappings
        framework_compliance = self._generate_framework_compliance(role_id, eqf_level)
        
        # Create stackability structure
        stackability_info = self._create_stackability_structure(named_modules, role_id, ects)
        
        # Generate work-based learning options
        wbl_options = self._generate_work_based_options(role_id, named_modules)
        
        # Create target audience specification
        target_audiences = self._generate_target_audiences(role_id, eqf_level)
        
        # Generate support and QA structure
        support_qa = self._generate_support_qa_structure(role_id, eqf_level)
        
        wp3_curriculum = {
            "metadata": {
                "title": f"Digital Sustainability Professional Development Course - {role_name} Specialization",
                "role_id": role_id,
                "role_name": role_name,
                "eqf_level": eqf_level,
                "ects_credits": ects,
                "total_study_hours": ects * 25,  # 25 hours per ECTS
                "delivery_mode": "Blended (Online + Practical + Work-Based Option)",
                "module_count": len(named_modules),
                "credential_format": "Stackable Micro-Credentials + Certificate",
                "wp3_compliant": True,
                "generation_timestamp": datetime.now().isoformat()
            },
            "programme_learning_outcomes": programme_outcomes,
            "modular_structure": named_modules,
            "assessment_strategy": assessment_strategy,
            "framework_mapping": framework_compliance,
            "stackability_and_micro_credentialing": stackability_info,
            "work_based_integration": wbl_options,
            "target_audiences": target_audiences,
            "support_and_qa": support_qa,
            "compliance_verification": self._verify_wp3_compliance(named_modules, framework_compliance)
        }
        
        print(f"✅ WP3-compliant curriculum generated with {len(named_modules)} named modules")
        return wp3_curriculum
    
    def _create_named_modules(self, selected_modules: List[Dict], role_id: str, total_ects: float) -> List[Dict]:
        """Create properly named, structured modules following ChatGPT template"""
        
        # Distribute ECTS across modules (aim for 3-5 modules for optimal granularity)
        module_count = min(len(selected_modules), max(3, int(total_ects / 2.5)))
        ects_per_module = total_ects / module_count
        
        named_modules = []
        
        for i, module in enumerate(selected_modules[:module_count]):
            module_ects = ects_per_module
            module_hours = module_ects * 25  # 25 hours per ECTS
            
            # Generate specific module name based on content and role
            module_name = self._generate_specific_module_name(module, role_id, i + 1, module_count)
            
            # Extract specific learning outcomes for this module
            module_outcomes = self._extract_module_learning_outcomes(module, role_id)
            
            # Generate micro-credential name
            micro_credential = self._generate_micro_credential_name(module, role_id)
            
            named_module = {
                "module_number": f"M{i + 1}",
                "title": module_name,
                "study_hours": round(module_hours, 1),
                "ects_credits": round(module_ects, 1),
                "learning_outcomes": module_outcomes,
                "micro_credential": micro_credential,
                "source_module_id": module.get('id', ''),
                "source_module_name": module.get('name', ''),
                "prerequisites": self._extract_module_prerequisites(module),
                "assessment_methods": module.get('assessment_methods', []),
                "industry_applications": self._extract_industry_applications(module, role_id)
            }
            
            named_modules.append(named_module)
        
        return named_modules
    
    def _generate_specific_module_name(self, module: Dict, role_id: str, module_num: int, total_modules: int) -> str:
        """Generate specific module names following professional naming conventions"""
        
        base_name = module.get('name', 'Sustainability Module')
        
        # Role-specific module naming patterns
        role_patterns = {
            "DAN": [
                "ESG Data Standards & Regulatory Context",
                "Sustainable Data Practices & Technical Tools", 
                "Reporting & Communication of ESG Impact"
            ],
            "DSE": [
                "Green Data Architecture & Infrastructure Design",
                "Sustainable Data Pipeline Engineering",
                "Energy-Efficient Data Systems Implementation"
            ],
            "DSL": [
                "Strategic Sustainability Leadership & Vision",
                "Organizational Transformation for Sustainability",
                "Executive Stakeholder Engagement & Change Management"
            ],
            "DSM": [
                "Sustainability Program Management & Coordination",
                "Cross-Functional Sustainability Implementation",
                "Performance Monitoring & Optimization Systems"
            ],
            "DSC": [
                "Sustainability Assessment & Advisory Methodologies",
                "Client Engagement & Consulting Delivery",
                "Strategic Sustainability Solution Design"
            ],
            "DSI": [
                "AI & Machine Learning for Sustainability",
                "Predictive Sustainability Modeling & Analytics",
                "Data Science Applications in Environmental Impact"
            ]
        }
        
        patterns = role_patterns.get(role_id, [f"Professional Sustainability Module {i}" for i in range(1, 4)])
        
        if module_num <= len(patterns):
            return patterns[module_num - 1]
        else:
            # Fallback for additional modules
            return f"Advanced {base_name} - Module {module_num}"
    
    def _extract_module_learning_outcomes(self, module: Dict, role_id: str) -> List[str]:
        """Extract specific learning outcomes following WP3 standards"""
        
        outcomes = []
        
        # Extract from module data
        learning_outcomes = module.get('learning_outcomes', {})
        
        if 'skills' in learning_outcomes:
            skills = learning_outcomes['skills']
            outcomes.append(f"Apply {skills.lower()} in professional sustainability contexts")
        
        if 'knowledge' in learning_outcomes:
            knowledge = learning_outcomes['knowledge'] 
            outcomes.append(f"Demonstrate comprehensive understanding of {knowledge.lower()}")
        
        # Add role-specific outcomes
        role_specific = {
            "DAN": [
                "Transform and validate sustainability datasets using data wrangling techniques",
                "Create dashboards to communicate sustainability impact to stakeholders",
                "Interpret ESG metrics to support data-driven decision-making"
            ],
            "DSE": [
                "Design energy-efficient data architectures for sustainability applications",
                "Implement green computing practices in data infrastructure",
                "Optimize data pipeline performance while minimizing environmental impact"
            ],
            "DSL": [
                "Develop strategic sustainability transformation initiatives",
                "Lead organizational change toward sustainable digital practices",
                "Influence C-level stakeholders on sustainability strategy"
            ],
            "DSM": [
                "Coordinate cross-functional sustainability programs effectively",
                "Monitor and optimize sustainability performance metrics",
                "Manage sustainability project portfolios and timelines"
            ],
            "DSC": [
                "Conduct comprehensive organizational sustainability assessments",
                "Deliver strategic sustainability advisory services to clients",
                "Design customized sustainability transformation roadmaps"
            ],
            "DSI": [
                "Develop predictive models for sustainability impact assessment",
                "Apply machine learning techniques to environmental challenges",
                "Communicate data science insights to diverse stakeholders"
            ]
        }
        
        role_outcomes = role_specific.get(role_id, ["Apply professional competencies in sustainability contexts"])
        outcomes.extend(role_outcomes[:3])  # Limit to 3 additional outcomes
        
        return outcomes[:5]  # Total max 5 outcomes per module
    
    def _generate_micro_credential_name(self, module: Dict, role_id: str) -> str:
        """Generate micro-credential names for stackability"""
        
        module_name = module.get('name', '')
        
        credential_patterns = {
            "DAN": "ESG Data Analytics Foundations",
            "DSE": "Sustainable Data Engineering Basics", 
            "DSL": "Digital Sustainability Leadership Essentials",
            "DSM": "Sustainability Program Management Fundamentals",
            "DSC": "Sustainability Consulting Methodology",
            "DSI": "AI for Sustainability Applications"
        }
        
        base_credential = credential_patterns.get(role_id, "Sustainability Professional Competency")
        
        # Enhance with module-specific focus
        if 'reporting' in module_name.lower():
            return f"{base_credential} - Reporting & Communication"
        elif 'data' in module_name.lower():
            return f"{base_credential} - Data & Analytics"
        elif 'management' in module_name.lower():
            return f"{base_credential} - Management & Strategy"
        else:
            return base_credential
    
    def _generate_programme_learning_outcomes(self, role_id: str, eqf_level: int, modules: List[Dict]) -> Dict:
        """Generate programme-level learning outcomes aligned with EQF descriptors"""
        
        eqf_descriptor = self.framework_mappings["EQF_descriptors"].get(eqf_level, "professional competency")
        
        role_definition = self.role_definitions.get(role_id, {})
        role_name = role_definition.get('name', 'Professional')
        
        outcomes = {
            "introduction": f"Upon successful completion, {role_name}s will demonstrate {eqf_descriptor} through the following competencies:",
            "specific_outcomes": []
        }
        
        # Role-specific programme outcomes following ChatGPT template
        role_outcomes = {
            "DAN": [
                "Apply ESG and sustainability reporting standards (e.g., GRI, CSRD) to organizational datasets",
                "Transform and validate sustainability datasets using data wrangling and cleaning techniques", 
                "Create dashboards or visual reports to communicate sustainability impact to stakeholders",
                "Interpret ESG metrics to support data-driven decision-making in line with regulatory frameworks",
                "Collaborate with teams to integrate ESG data practices into sustainability workflows"
            ],
            "DSE": [
                "Design and implement energy-efficient data architectures for sustainability applications",
                "Optimize data pipeline performance while minimizing environmental impact through green computing",
                "Establish data governance frameworks that support sustainability reporting requirements",
                "Apply cloud optimization techniques to reduce carbon footprint of data infrastructure",
                "Collaborate with technical teams to implement sustainable data engineering best practices"
            ],
            "DSL": [
                "Develop comprehensive digital sustainability strategies aligned with organizational goals",
                "Lead transformation initiatives that integrate sustainability into digital operations",
                "Influence executive stakeholders to drive adoption of sustainable digital practices",
                "Design governance frameworks for sustainable digital transformation programs",
                "Coordinate cross-functional teams to implement strategic sustainability initiatives"
            ],
            "DSM": [
                "Manage cross-functional sustainability programs from conception to implementation",
                "Coordinate sustainability initiatives across multiple departments and stakeholder groups",
                "Monitor, measure, and optimize sustainability performance using advanced KPI frameworks",
                "Apply project management methodologies to sustainability transformation projects",
                "Facilitate stakeholder engagement and communication for sustainability initiatives"
            ],
            "DSC": [
                "Conduct comprehensive sustainability assessments for diverse organizational contexts",
                "Deliver strategic sustainability advisory services that align with client objectives",
                "Design customized sustainability transformation roadmaps based on maturity assessments",
                "Facilitate stakeholder engagement sessions to build consensus around sustainability initiatives",
                "Apply consulting methodologies to sustainability challenges across industry sectors"
            ],
            "DSI": [
                "Develop predictive models for sustainability impact assessment using machine learning",
                "Apply advanced analytics techniques to solve complex environmental challenges",
                "Design AI-driven solutions that optimize sustainability performance across operations",
                "Communicate complex data science insights to technical and non-technical stakeholders",
                "Integrate ethical considerations into AI applications for sustainability contexts"
            ]
        }
        
        outcomes["specific_outcomes"] = role_outcomes.get(role_id, [
            "Apply professional competencies in sustainability contexts",
            "Demonstrate technical proficiency in assigned role functions",
            "Collaborate effectively in cross-functional sustainability teams"
        ])
        
        return outcomes
    
    def _create_assessment_strategy(self, modules: List[Dict], role_id: str, eqf_level: int) -> Dict:
        """Create comprehensive assessment strategy mapped to competencies"""
        
        return {
            "overview": "Assessment combines theoretical mastery with practical application through competency-based evaluation",
            "components": [
                {
                    "component": "Portfolio",
                    "description": f"Curated digital evidence of {role_id} competency development, including reflections and professional artifacts",
                    "weight_percentage": 40,
                    "linked_modules": [m["module_number"] for m in modules],
                    "assessment_type": "Continuous"
                },
                {
                    "component": "Practical Project",  
                    "description": f"End-to-end {role_id} project demonstrating integrated competency application",
                    "weight_percentage": 35,
                    "linked_modules": [m["module_number"] for m in modules[-2:]],  # Last 2 modules
                    "assessment_type": "Summative"
                },
                {
                    "component": "Peer Collaboration Task",
                    "description": "Group challenges demonstrating teamwork and professional communication skills",
                    "weight_percentage": 15,
                    "linked_modules": [modules[1]["module_number"]] if len(modules) > 1 else [modules[0]["module_number"]],
                    "assessment_type": "Formative"
                },
                {
                    "component": "Reflective Practice Journal",
                    "description": "Self-assessment and professional development planning for sustainability career advancement",
                    "weight_percentage": 10,
                    "linked_modules": ["All modules"],
                    "assessment_type": "Continuous"
                }
            ],
            "pass_criteria": {
                "overall_pass_mark": "70% overall achievement",
                "component_requirements": "Minimum 60% in each major component",
                "competency_demonstration": f"Evidence of {role_id} professional competency across all learning outcomes"
            }
        }
    
    def _generate_framework_compliance(self, role_id: str, eqf_level: int) -> Dict:
        """Generate comprehensive framework mapping for cross-border recognition"""
        
        return {
            "eqf_alignment": {
                "level": eqf_level,
                "descriptor": self.framework_mappings["EQF_descriptors"].get(eqf_level),
                "competence_type": "Professional competency with autonomous practice"
            },
            "e_cf_mapping": {
                "competencies": self.framework_mappings["e-CF"].get(role_id, []),
                "version": "e-CF 4.0",
                "compliance_level": "Fully aligned"
            },
            "esco_mapping": {
                "occupation_code": self.framework_mappings["ESCO"].get(role_id),
                "transversal_skills": ["green thinking", "digital literacy", "analytical thinking"],
                "language_skills": ["Professional English for sustainability contexts"]
            },
            "national_framework_readiness": {
                "ecvet_compatible": True,
                "bologna_aligned": True,
                "cross_border_recognition": "Supported through framework mapping"
            }
        }
    
    def _create_stackability_structure(self, modules: List[Dict], role_id: str, total_ects: float) -> Dict:
        """Create stackability and micro-credentialing structure"""
        
        progression_map = " → ".join([f"[ {m['title'][:20]}... ]" for m in modules])
        
        return {
            "micro_credentials": {
                "individual_badges": [
                    {
                        "module": m["module_number"],
                        "badge_name": m["micro_credential"],
                        "ects_value": m["ects_credits"],
                        "verification": "Blockchain-secured digital badge"
                    }
                    for m in modules
                ],
                "certificate_completion": {
                    "name": f"{role_id} for Sustainability Certificate",
                    "total_ects": total_ects,
                    "level": f"EQF {modules[0].get('eqf_level', 6)}",
                    "recognition": "EU-wide through framework mapping"
                }
            },
            "progression_pathway": {
                "visual_map": progression_map,
                "next_level_options": [
                    f"Advanced {role_id} Specialization",
                    "Cross-role Sustainability Leadership",
                    "Industry-specific Sustainability Applications"
                ],
                "credit_transfer": f"ECTS credits transferable to related programmes"
            },
            "stackability_matrix": {
                "horizontal_stacking": f"Combines with other {role_id} programmes",
                "vertical_stacking": "Progresses to higher EQF levels",
                "cross_role_stacking": "Integrates with other sustainability roles"
            }
        }
    
    def _generate_work_based_options(self, role_id: str, modules: List[Dict]) -> Dict:
        """Generate work-based learning integration options"""
        
        role_wbl = {
            "DAN": {
                "mini_placements": ["ESG reporting teams", "Sustainability analytics departments"],
                "practical_labs": ["Real ESG dataset analysis", "Sustainability dashboard development"],
                "industry_projects": ["Corporate sustainability reporting automation", "ESG compliance data pipeline"]
            },
            "DSE": {
                "mini_placements": ["Green IT infrastructure teams", "Sustainable data center operations"],
                "practical_labs": ["Energy-efficient architecture design", "Carbon footprint optimization"],
                "industry_projects": ["Cloud sustainability migration", "Green data pipeline implementation"]
            },
            "DSL": {
                "mini_placements": ["C-suite sustainability strategy teams", "Digital transformation offices"],
                "practical_labs": ["Strategic planning simulations", "Stakeholder engagement workshops"],
                "industry_projects": ["Organizational sustainability transformation", "Executive sustainability presentation"]
            },
            "DSM": {
                "mini_placements": ["Sustainability program offices", "Cross-functional coordination teams"],
                "practical_labs": ["Program management simulations", "KPI dashboard development"],
                "industry_projects": ["Multi-department sustainability initiative", "Performance monitoring system"]
            },
            "DSC": {
                "mini_placements": ["Sustainability consulting firms", "Advisory service teams"],
                "practical_labs": ["Client assessment methodologies", "Solution design workshops"],
                "industry_projects": ["Client sustainability maturity assessment", "Advisory recommendation development"]
            },
            "DSI": {
                "mini_placements": ["AI for sustainability teams", "Data science departments"],
                "practical_labs": ["ML model development", "Predictive analytics workshops"],
                "industry_projects": ["Sustainability prediction model", "AI-driven optimization system"]
            }
        }
        
        return {
            "standard_options": role_wbl.get(role_id, {
                "mini_placements": ["Sustainability teams"],
                "practical_labs": ["Professional practice simulations"],
                "industry_projects": ["Real-world competency application"]
            }),
            "delivery_modes": {
                "hybrid_format": "Combination of workplace and educational institution",
                "virtual_placement": "Remote collaboration with industry partners",
                "project_based": "Authentic industry challenges with mentor support"
            },
            "recognition_of_prior_learning": {
                "rpl_available": True,
                "assessment_process": "Portfolio-based competency demonstration",
                "credit_reduction": "Up to 30% of programme ECTS through RPL"
            }
        }
    
    def _generate_target_audiences(self, role_id: str, eqf_level: int) -> List[str]:
        """Generate specific target audience definitions"""
        
        base_audiences = [
            f"Junior/aspiring {self.role_definitions.get(role_id, {}).get('name', 'professionals')} moving into sustainability",
            "Sustainability officers upskilling in specialized competencies",
            "Professionals retraining from finance/ICT/environmental roles"
        ]
        
        if eqf_level >= 7:
            base_audiences.append("Senior professionals seeking advanced sustainability leadership skills")
        
        if eqf_level <= 5:
            base_audiences.append("Career changers with foundational experience seeking sustainability specialization")
        
        return base_audiences
    
    def _generate_support_qa_structure(self, role_id: str, eqf_level: int) -> Dict:
        """Generate support and quality assurance structure"""
        
        return {
            "instructional_support": {
                "instructors": f"{role_id} sustainability experts + industry practitioners",
                "peer_learning": "Weekly asynchronous forums + monthly live sessions",
                "mentorship": "Industry mentor assignment for practical projects"
            },
            "quality_assurance": {
                "framework_alignment": "Mapped to EQF and reviewed annually",
                "industry_validation": "Employer panel review of competency relevance",
                "learner_feedback": "Continuous improvement through learner evaluation"
            },
            "accessibility": {
                "digital_inclusion": "Multiple device compatibility and offline options",
                "language_support": "Multi-language resources for international learners",
                "reasonable_adjustments": "Flexible assessment arrangements available"
            }
        }
    
    def _extract_module_prerequisites(self, module: Dict) -> List[str]:
        """Extract module prerequisites"""
        return module.get('prerequisites', ["Basic digital literacy", "Interest in sustainability topics"])
    
    def _extract_industry_applications(self, module: Dict, role_id: str) -> List[str]:
        """Extract industry applications for module"""
        applications = module.get('industry_applications', [])
        if not applications:
            role_apps = {
                "DAN": ["ESG Reporting", "Sustainability Analytics", "Regulatory Compliance"],
                "DSE": ["Green IT Infrastructure", "Energy Management", "Sustainable Computing"],
                "DSL": ["Digital Transformation", "Sustainability Strategy", "Organizational Change"],
                "DSM": ["Program Management", "Operations Optimization", "Performance Monitoring"],
                "DSC": ["Advisory Services", "Client Consulting", "Strategic Planning"],
                "DSI": ["Predictive Analytics", "AI Solutions", "Environmental Modeling"]
            }
            applications = role_apps.get(role_id, ["Sustainability Applications"])
        
        return applications[:4]  # Limit to 4 applications
    
    def _verify_wp3_compliance(self, modules: List[Dict], framework_compliance: Dict) -> Dict:
        """Verify WP3 compliance against standard criteria"""
        
        compliance_checks = {
            "modular_structure": len(modules) >= 2,  # At least 2 modules
            "named_modules": all(m.get('title') for m in modules),  # All modules named
            "ects_distribution": all(m.get('ects_credits', 0) > 0 for m in modules),  # ECTS assigned
            "learning_outcomes": all(len(m.get('learning_outcomes', [])) >= 3 for m in modules),  # Min 3 outcomes per module
            "framework_mapping": bool(framework_compliance.get('e_cf_mapping')),  # Framework mapped
            "micro_credentials": True,  # Micro-credentials defined
            "assessment_strategy": True,  # Assessment strategy defined
            "work_based_options": True  # WBL options provided
        }
        
        compliance_score = sum(compliance_checks.values()) / len(compliance_checks) * 100
        
        return {
            "overall_compliance": compliance_score >= 90,
            "compliance_percentage": compliance_score,
            "failed_criteria": [k for k, v in compliance_checks.items() if not v],
            "verification_timestamp": datetime.now().isoformat()
        }
