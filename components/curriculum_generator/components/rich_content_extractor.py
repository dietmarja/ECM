#!/usr/bin/env python3
# scripts/curriculum_generator/components/rich_content_extractor.py
"""
Rich Content Extractor - Utilizes detailed module data from modules_v5.json
Generates specific, differentiated content instead of generic outcomes
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import re

class RichContentExtractor:
    """Extracts rich, specific content from module database"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.module_database = self._load_full_module_database()
        self.framework_mappings = self._initialize_framework_mappings()
        
    def _load_full_module_database(self) -> List[Dict]:
        """Load complete module database with all rich content"""
        module_paths = [
            self.project_root / "input" / "modules" / "modules_v5.json"
        ]
        
        for path in module_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        modules = json.load(f)
                        print(f"✅ Loaded FULL module database: {len(modules)} modules with rich content")
                        return modules
                except Exception as e:
                    print(f"⚠️  Error loading {path}: {e}")
                    continue
        
        print("⚠️  Full module database not found, content will be limited")
        return []
    
    def _initialize_framework_mappings(self) -> Dict[str, Dict]:
        """Initialize framework mapping templates"""
        return {
            "e-CF": {
                "A": "Plan", "B": "Build", "C": "Run", "D": "Enable", "E": "Manage"
            },
            "DigComp": {
                "1": "Information and data literacy",
                "2": "Communication and collaboration", 
                "3": "Digital content creation",
                "4": "Safety",
                "5": "Problem solving"
            },
            "GreenComp": {
                "1": "Embodying sustainability values",
                "2": "Embracing complexity in sustainability",
                "3": "Envisioning sustainable futures", 
                "4": "Acting for sustainability"
            }
        }
    
    def extract_specific_learning_outcomes(self, modules: List[Dict], role_id: str, 
                                         progression_level: str, eqf_level: int) -> List[str]:
        """Extract specific, rich learning outcomes from module data"""
        specific_outcomes = []
        
        for module in modules:
            module_outcomes = self._extract_module_specific_outcomes(module, role_id, progression_level, eqf_level)
            specific_outcomes.extend(module_outcomes)
        
        # Remove duplicates while preserving order and specificity
        unique_outcomes = []
        seen_concepts = set()
        
        for outcome in specific_outcomes:
            # Extract key concepts to avoid semantic duplicates
            key_concepts = self._extract_key_concepts(outcome)
            concept_signature = frozenset(key_concepts)
            
            if concept_signature not in seen_concepts:
                unique_outcomes.append(outcome)
                seen_concepts.add(concept_signature)
        
        return unique_outcomes[:8]  # Limit to 8 most specific outcomes
    
    def _extract_module_specific_outcomes(self, module: Dict, role_id: str, 
                                        progression_level: str, eqf_level: int) -> List[str]:
        """Extract and adapt specific outcomes from a single module"""
        outcomes = []
        module_name = module.get('name', '')
        module_id = module.get('id', '')
        
        # Extract direct learning outcomes
        learning_outcomes = module.get('learning_outcomes', {})
        
        # Process knowledge outcomes
        if 'knowledge' in learning_outcomes:
            knowledge = learning_outcomes['knowledge']
            adapted_knowledge = self._adapt_outcome_to_role(knowledge, role_id, progression_level, eqf_level, 'knowledge')
            outcomes.append(f"📚 {adapted_knowledge}")
        
        # Process skills outcomes  
        if 'skills' in learning_outcomes:
            skills = learning_outcomes['skills']
            adapted_skills = self._adapt_outcome_to_role(skills, role_id, progression_level, eqf_level, 'skills')
            outcomes.append(f"🛠️ {adapted_skills}")
        
        # Process understanding/competence outcomes
        if 'understanding' in learning_outcomes:
            understanding = learning_outcomes['understanding']
            adapted_understanding = self._adapt_outcome_to_role(understanding, role_id, progression_level, eqf_level, 'competence')
            outcomes.append(f"🎯 {adapted_understanding}")
        
        # Extract from module description for additional context
        description = module.get('description', '') or module.get('extended_description', '')
        if description:
            context_outcome = self._generate_contextual_outcome(description, module_name, role_id, progression_level)
            if context_outcome:
                outcomes.append(f"🔧 {context_outcome}")
        
        # Add assessment-specific outcomes
        assessment_methods = module.get('assessment_methods', [])
        if assessment_methods:
            assessment_outcome = self._generate_assessment_outcome(assessment_methods, module_name, role_id, eqf_level)
            outcomes.append(f"📊 {assessment_outcome}")
        
        return outcomes
    
    def _adapt_outcome_to_role(self, base_outcome: str, role_id: str, progression_level: str, 
                              eqf_level: int, outcome_type: str) -> str:
        """Adapt generic outcome to specific role context"""
        
        # EQF level action verbs
        eqf_verbs = {
            4: {"knowledge": "recall and explain", "skills": "apply and demonstrate", "competence": "work independently with"},
            5: {"knowledge": "analyze and evaluate", "skills": "implement and optimize", "competence": "manage and coordinate"},
            6: {"knowledge": "synthesize and design", "skills": "develop and innovate", "competence": "lead and integrate"},
            7: {"knowledge": "create and pioneer", "skills": "transform and architect", "competence": "strategize and influence"},
            8: {"knowledge": "research and theorize", "skills": "revolutionize and advance", "competence": "pioneer and establish"}
        }
        
        verb_set = eqf_verbs.get(eqf_level, eqf_verbs[6])
        action_verb = verb_set.get(outcome_type, "apply")
        
        # Role-specific contexts
        role_contexts = {
            "DAN": "data analysis and visualization contexts",
            "DSE": "data engineering and infrastructure environments", 
            "DSL": "strategic leadership and organizational transformation scenarios",
            "DSM": "program management and operational sustainability initiatives",
            "DSC": "consulting and advisory service delivery",
            "DSI": "data science and predictive modeling applications",
            "SBA": "business analysis and process optimization frameworks",
            "SDD": "software development and green coding practices",
            "SSD": "systems design and sustainable architecture solutions",
            "STS": "technical implementation and platform management"
        }
        
        context = role_contexts.get(role_id, "professional sustainability contexts")
        
        # Clean and enhance the base outcome
        cleaned_outcome = re.sub(r'^(understand|learn|know|apply)\s+', '', base_outcome.lower())
        cleaned_outcome = re.sub(r'\s+', ' ', cleaned_outcome).strip()
        
        return f"The learner will be able to {action_verb} {cleaned_outcome} within {context}, demonstrating {progression_level.lower()}-level professional competency"
    
    def _extract_key_concepts(self, outcome: str) -> Set[str]:
        """Extract key concepts from learning outcome to avoid duplicates"""
        # Remove common words and extract domain concepts
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'be', 'able', 'will', 'learner'}
        words = re.findall(r'\b[a-zA-Z]{4,}\b', outcome.lower())
        return {word for word in words if word not in stop_words}
    
    def _generate_contextual_outcome(self, description: str, module_name: str, 
                                   role_id: str, progression_level: str) -> Optional[str]:
        """Generate contextual learning outcome from module description"""
        if len(description) < 50:
            return None
        
        # Extract key phrases from description
        key_phrases = re.findall(r'\b(?:implement|develop|design|analyze|evaluate|manage|optimize|integrate)\s+[a-zA-Z\s]{10,50}', description.lower())
        
        if key_phrases:
            selected_phrase = key_phrases[0].strip()
            return f"The learner will be able to {selected_phrase} as demonstrated through the {module_name} module application in {progression_level.lower()}-level professional practice"
        
        return None
    
    def _generate_assessment_outcome(self, assessment_methods: List[str], module_name: str, 
                                   role_id: str, eqf_level: int) -> str:
        """Generate assessment-specific learning outcome"""
        if not assessment_methods:
            return "The learner will be able to demonstrate competency through appropriate assessment methods"
        
        primary_method = assessment_methods[0]
        method_descriptions = {
            "practical_assignment": "hands-on practical assignments",
            "case_study": "real-world case study analysis",
            "industry_project": "authentic industry project execution",
            "work_based_assessment": "workplace-based competency demonstration",
            "research_project": "independent research and investigation",
            "presentation": "professional presentation and communication",
            "portfolio": "comprehensive portfolio development",
            "simulation": "simulated professional environment assessment"
        }
        
        method_desc = method_descriptions.get(primary_method, "professional assessment methods")
        
        return f"The learner will be able to demonstrate mastery of {module_name} competencies through {method_desc}, meeting EQF Level {eqf_level} performance standards"
    
    def extract_detailed_module_descriptions(self, modules: List[Dict], role_id: str) -> List[Dict]:
        """Extract detailed, role-specific module descriptions"""
        detailed_modules = []
        
        for module in modules:
            detailed_module = self._create_detailed_module_description(module, role_id)
            detailed_modules.append(detailed_module)
        
        return detailed_modules
    
    def _create_detailed_module_description(self, module: Dict, role_id: str) -> Dict:
        """Create comprehensive module description with rich metadata"""
        
        module_id = module.get('id', '')
        module_name = module.get('name', '')
        base_description = module.get('description', '') or module.get('extended_description', '')
        
        # Extract framework mappings
        framework_mappings = self._extract_framework_mappings(module)
        
        # Generate role-specific content focus
        role_focus = self._generate_role_specific_focus(module, role_id)
        
        # Extract work-based learning elements
        wbl_elements = self._extract_work_based_elements(module, role_id)
        
        # Generate detailed prerequisites and progression
        prerequisites = self._extract_prerequisites(module)
        progression_pathways = self._generate_progression_pathways(module, role_id)
        
        return {
            "module_id": module_id,
            "module_name": module_name,
            "rich_description": f"{base_description} {role_focus}",
            "specific_topics": self._extract_specific_topics(module),
            "learning_methods": self._extract_learning_methods(module, role_id),
            "assessment_details": self._extract_assessment_details(module),
            "framework_mappings": framework_mappings,
            "work_based_elements": wbl_elements,
            "prerequisites": prerequisites,
            "progression_pathways": progression_pathways,
            "industry_relevance": self._extract_industry_relevance(module),
            "practical_applications": self._extract_practical_applications(module, role_id)
        }
    
    def _extract_framework_mappings(self, module: Dict) -> Dict:
        """Extract or generate framework mappings for the module"""
        mappings = {}
        
        # Check for existing mappings in module data
        if 'framework_mappings' in module:
            mappings = module['framework_mappings']
        else:
            # Generate based on module content
            module_content = f"{module.get('name', '')} {module.get('description', '')}"
            
            # e-CF mapping based on content analysis
            if any(term in module_content.lower() for term in ['strategy', 'plan', 'design']):
                mappings['e-CF'] = ['A.1', 'A.4', 'A.6']  # Plan category
            elif any(term in module_content.lower() for term in ['develop', 'implement', 'build']):
                mappings['e-CF'] = ['B.1', 'B.3', 'B.5']  # Build category
            elif any(term in module_content.lower() for term in ['manage', 'operate', 'maintain']):
                mappings['e-CF'] = ['C.1', 'C.2', 'C.4']  # Run category
            
            # DigComp mapping
            if any(term in module_content.lower() for term in ['data', 'information', 'analysis']):
                mappings['DigComp'] = ['1.1', '1.2', '1.3']
            elif any(term in module_content.lower() for term in ['collaboration', 'communication']):
                mappings['DigComp'] = ['2.1', '2.2', '2.4']
            
            # GreenComp mapping
            if any(term in module_content.lower() for term in ['sustainability', 'environmental', 'green']):
                mappings['GreenComp'] = ['1.1', '4.1', '4.3']
        
        return mappings
    
    def _generate_role_specific_focus(self, module: Dict, role_id: str) -> str:
        """Generate role-specific focus statement for the module"""
        role_focuses = {
            "DAN": "This module emphasizes data visualization, statistical analysis, and ESG reporting dashboard creation for sustainability analysts.",
            "DSE": "This module focuses on sustainable data architecture, green computing practices, and energy-efficient data pipeline implementation.",
            "DSL": "This module develops strategic thinking, organizational transformation capabilities, and executive-level sustainability leadership skills.",
            "DSM": "This module builds program management expertise, cross-functional coordination abilities, and operational sustainability implementation skills.",
            "DSC": "This module enhances consulting methodologies, client engagement strategies, and advisory service delivery for sustainability transformation.",
            "DSI": "This module advances machine learning applications, predictive modeling techniques, and AI-driven sustainability solution development.",
            "SBA": "This module strengthens business process analysis, sustainability ROI evaluation, and organizational change management capabilities.",
            "SDD": "This module deepens green coding practices, sustainable software architecture, and energy-efficient application development skills.",
            "SSD": "This module expands systems thinking, sustainable design principles, and circular economy solution architecture expertise.",
            "STS": "This module builds technical implementation skills, platform management capabilities, and sustainability technology deployment expertise."
        }
        
        return role_focuses.get(role_id, "This module develops professional competencies relevant to sustainability practice.")
    
    def _extract_work_based_elements(self, module: Dict, role_id: str) -> List[str]:
        """Extract work-based learning elements"""
        wbl_elements = []
        
        # Check module data for WBL indicators
        if module.get('work_based_learning', False):
            wbl_elements.append("Workplace-based competency assessment")
            wbl_elements.append("Real organizational project implementation")
        
        # Generate role-specific WBL elements
        role_wbl = {
            "DAN": ["ESG dashboard development for real organization", "Sustainability data analysis project with industry partner"],
            "DSE": ["Green data infrastructure implementation project", "Energy efficiency optimization in live systems"],
            "DSL": ["Strategic sustainability transformation leadership in organization", "C-suite stakeholder engagement project"],
            "DSM": ["Cross-functional sustainability program management", "Operational sustainability KPI implementation"],
            "DSC": ["Client organization sustainability assessment", "Advisory service delivery project"],
            "DSI": ["Predictive sustainability model development for industry", "AI solution implementation in organizational context"]
        }
        
        wbl_elements.extend(role_wbl.get(role_id, ["Professional practice application project"]))
        
        return wbl_elements
    
    def _extract_specific_topics(self, module: Dict) -> List[str]:
        """Extract specific topics covered in the module"""
        topics = []
        
        # Extract from module topics if available
        if 'topics' in module:
            topics = module['topics']
        elif 'content_topics' in module:
            topics = module['content_topics']
        else:
            # Generate from module name and description
            module_text = f"{module.get('name', '')} {module.get('description', '')}"
            
            # Extract key concepts as topics
            concepts = re.findall(r'\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', module_text)
            topics = list(set(concepts))[:8]  # Limit to 8 topics
        
        return topics
    
    def _extract_learning_methods(self, module: Dict, role_id: str) -> List[str]:
        """Extract specific learning methods for the module"""
        methods = []
        
        if 'learning_methods' in module:
            methods = module['learning_methods']
        else:
            # Generate role-appropriate methods
            base_methods = ["Interactive workshops", "Case study analysis", "Practical exercises"]
            
            role_methods = {
                "DAN": ["Data visualization labs", "Statistical analysis workshops", "Dashboard creation sessions"],
                "DSE": ["Infrastructure design workshops", "Hands-on architecture labs", "System optimization exercises"],
                "DSL": ["Strategic planning sessions", "Leadership simulations", "Stakeholder engagement workshops"],
                "DSM": ["Project management labs", "Cross-functional team exercises", "Program coordination simulations"],
                "DSC": ["Client consultation simulations", "Advisory methodology workshops", "Presentation skills labs"],
                "DSI": ["Machine learning workshops", "Model development labs", "AI implementation exercises"]
            }
            
            methods = base_methods + role_methods.get(role_id, [])
        
        return methods
    
    def _extract_assessment_details(self, module: Dict) -> Dict:
        """Extract detailed assessment information"""
        assessment_methods = module.get('assessment_methods', [])
        
        return {
            "methods": assessment_methods,
            "weighting": self._generate_assessment_weighting(assessment_methods),
            "criteria": self._generate_assessment_criteria(module),
            "pass_threshold": "70% overall with minimum 60% in each component"
        }
    
    def _generate_assessment_weighting(self, methods: List[str]) -> Dict:
        """Generate assessment weighting distribution"""
        if not methods:
            return {"coursework": 100}
        
        weightings = {}
        weight_per_method = 100 // len(methods)
        remainder = 100 % len(methods)
        
        for i, method in enumerate(methods):
            weight = weight_per_method + (1 if i < remainder else 0)
            weightings[method] = weight
        
        return weightings
    
    def _generate_assessment_criteria(self, module: Dict) -> List[str]:
        """Generate specific assessment criteria"""
        criteria = [
            "Technical accuracy and professional competency demonstration",
            "Application of theoretical knowledge to practical scenarios",
            "Quality of analysis and problem-solving approach",
            "Professional communication and presentation skills"
        ]
        
        # Add module-specific criteria
        module_name = module.get('name', '').lower()
        if 'data' in module_name:
            criteria.append("Data handling and visualization quality")
        if 'management' in module_name:
            criteria.append("Strategic thinking and leadership capability")
        if 'technical' in module_name or 'engineering' in module_name:
            criteria.append("Technical implementation and optimization skills")
        
        return criteria
    
    def _extract_prerequisites(self, module: Dict) -> List[str]:
        """Extract module prerequisites"""
        prerequisites = module.get('prerequisites', [])
        
        if not prerequisites:
            # Generate based on EQF level and content
            eqf_level = module.get('eqf_level', 6)
            if eqf_level >= 7:
                prerequisites = ["Bachelor's degree or equivalent professional experience", "Foundational sustainability knowledge"]
            elif eqf_level >= 6:
                prerequisites = ["Diploma/certificate level qualification or relevant work experience"]
            else:
                prerequisites = ["Basic digital literacy", "Interest in sustainability topics"]
        
        return prerequisites
    
    def _generate_progression_pathways(self, module: Dict, role_id: str) -> Dict:
        """Generate progression pathways from this module"""
        return {
            "prerequisites_for": f"Advanced {role_id} specialization modules",
            "stacks_with": f"Other {role_id} professional development modules",
            "leads_to": f"{role_id} certification pathway completion",
            "micro_credential": f"{module.get('name', 'Module')} Digital Badge"
        }
    
    def _extract_industry_relevance(self, module: Dict) -> List[str]:
        """Extract industry relevance and applications"""
        relevance = module.get('industry_applications', [])
        
        if not relevance:
            # Generate based on module content
            module_content = f"{module.get('name', '')} {module.get('description', '')}"
            
            base_industries = ["Technology", "Finance", "Manufacturing", "Consulting", "Public Sector"]
            if 'esg' in module_content.lower():
                relevance.extend(["ESG Reporting", "Regulatory Compliance", "Investment Management"])
            if 'data' in module_content.lower():
                relevance.extend(["Data Analytics", "Business Intelligence", "Digital Transformation"])
        
        return relevance[:6]  # Limit to 6 most relevant
    
    def _extract_practical_applications(self, module: Dict, role_id: str) -> List[str]:
        """Extract practical applications specific to role"""
        applications = []
        
        role_applications = {
            "DAN": ["ESG dashboard creation", "Sustainability metrics analysis", "Data-driven reporting"],
            "DSE": ["Green data pipeline design", "Energy-efficient architecture", "Sustainable infrastructure"],
            "DSL": ["Strategy development", "Transformation leadership", "Stakeholder engagement"],
            "DSM": ["Program implementation", "Team coordination", "Performance monitoring"],
            "DSC": ["Client assessment", "Advisory delivery", "Solution recommendation"],
            "DSI": ["Predictive modeling", "AI solution development", "Data science applications"]
        }
        
        base_apps = role_applications.get(role_id, ["Professional practice application"])
        module_name = module.get('name', '').lower()
        
        # Enhance with module-specific applications
        if 'reporting' in module_name:
            applications.append("Automated sustainability reporting system development")
        if 'compliance' in module_name:
            applications.append("Regulatory compliance framework implementation")
        if 'assessment' in module_name:
            applications.append("Sustainability impact assessment methodology")
        
        return base_apps + applications
    
    def generate_framework_compliance_summary(self, modules: List[Dict]) -> Dict:
        """Generate comprehensive framework compliance summary"""
        
        all_mappings = {}
        for module in modules:
            module_mappings = self._extract_framework_mappings(module)
            for framework, competencies in module_mappings.items():
                if framework not in all_mappings:
                    all_mappings[framework] = set()
                all_mappings[framework].update(competencies)
        
        return {
            "framework_coverage": {
                framework: {
                    "competencies_covered": len(competencies),
                    "specific_competencies": list(competencies)
                }
                for framework, competencies in all_mappings.items()
            },
            "compliance_percentage": {
                framework: min(100, (len(competencies) / 10) * 100)  # Assume 10 key competencies per framework
                for framework, competencies in all_mappings.items()
            },
            "cross_recognition_readiness": len(all_mappings) >= 2  # Ready if mapped to 2+ frameworks
        }