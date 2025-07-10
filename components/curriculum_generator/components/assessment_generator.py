"""
Assessment strategy generator component.
Creates comprehensive assessment strategies aligned with learning outcomes and EQF levels.
"""

from typing import Dict, List, Any, Optional
import math


class AssessmentGenerator:
    """Generates comprehensive assessment strategies"""
    
    def __init__(self, domain_knowledge):
        self.domain_knowledge = domain_knowledge
        
    def generate_assessment_strategy(
        self,
        topic: str,
        eqf_level: int,
        selected_modules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate comprehensive assessment strategy"""
        
        print(f"📝 Generating assessment strategy for EQF {eqf_level}")
        
        # Generate different assessment components
        strategy = {
            "overall_strategy": self._generate_overall_strategy(topic, eqf_level),
            "module_assessments": self._generate_module_assessments(selected_modules, eqf_level, topic),
            "summative_assessment": self._generate_summative_assessment(topic, eqf_level, selected_modules),
            "formative_assessment": self._generate_formative_assessment(eqf_level),
            "competency_assessment": self._generate_competency_assessment(topic, eqf_level),
            "quality_assurance": self._generate_quality_assurance_framework(eqf_level),
            "grading_framework": self._generate_grading_framework(eqf_level),
            "assessment_calendar": self._generate_assessment_calendar(selected_modules)
        }
        
        print(f"✅ Assessment strategy generated with {len(strategy['module_assessments'])} module assessments")
        return strategy
        
    def _generate_overall_strategy(self, topic: str, eqf_level: int) -> Dict[str, Any]:
        """Generate overall assessment strategy"""
        
        # Get topic-appropriate assessment methods
        preferred_methods = self.domain_knowledge.get_assessment_methods_for_topic(topic, eqf_level)
        
        strategy = {
            "assessment_philosophy": self._get_assessment_philosophy(eqf_level),
            "primary_methods": preferred_methods,
            "balance_ratios": self._get_assessment_balance(eqf_level),
            "learning_outcome_alignment": self._describe_outcome_alignment(eqf_level),
            "feedback_strategy": self._get_feedback_strategy(eqf_level),
            "authentic_assessment": self._describe_authentic_assessment(topic, eqf_level)
        }
        
        return strategy
        
    def _get_assessment_philosophy(self, eqf_level: int) -> str:
        """Get assessment philosophy for EQF level"""
        
        philosophies = {
            5: "Competency-based assessment focusing on practical skills demonstration and workplace readiness",
            6: "Balanced assessment combining theoretical understanding with practical application and critical thinking",
            7: "Advanced assessment emphasizing analysis, synthesis, and independent research capabilities",
            8: "Research-focused assessment promoting original contribution and scholarly excellence"
        }
        
        return philosophies.get(eqf_level, philosophies[6])
        
    def _get_assessment_balance(self, eqf_level: int) -> Dict[str, int]:
        """Get recommended assessment balance percentages"""
        
        balances = {
            5: {"practical": 60, "written": 25, "project": 15},
            6: {"practical": 40, "written": 35, "project": 25},
            7: {"practical": 25, "written": 30, "project": 45},
            8: {"practical": 15, "written": 20, "project": 65}
        }
        
        return balances.get(eqf_level, balances[6])
        
    def _describe_outcome_alignment(self, eqf_level: int) -> str:
        """Describe how assessments align with learning outcomes"""
        
        alignments = {
            5: "Assessments directly measure competency achievement and workplace performance indicators",
            6: "Assessments evaluate understanding, application, and analysis across cognitive domains",
            7: "Assessments measure advanced analytical skills, research competency, and professional judgment", 
            8: "Assessments evaluate original research, scholarly contribution, and field advancement"
        }
        
        return alignments.get(eqf_level, alignments[6])
        
    def _get_feedback_strategy(self, eqf_level: int) -> Dict[str, Any]:
        """Get feedback strategy for EQF level"""
        
        base_strategy = {
            "frequency": "regular",
            "types": ["formative", "summative"],
            "delivery_methods": ["written", "verbal", "peer"],
            "turnaround_time": "within 2 weeks"
        }
        
        if eqf_level >= 7:
            base_strategy.update({
                "peer_review": True,
                "self_assessment": True,
                "expert_feedback": True,
                "reflective_components": True
            })
        else:
            base_strategy.update({
                "peer_review": False,
                "instructor_focused": True,
                "clear_criteria": True,
                "improvement_focused": True
            })
            
        return base_strategy
        
    def _describe_authentic_assessment(self, topic: str, eqf_level: int) -> Dict[str, Any]:
        """Describe authentic assessment approaches"""
        
        # Get industry context
        industries = self.domain_knowledge.get_industry_relevance(topic)
        
        authentic = {
            "real_world_contexts": [],
            "industry_connections": industries,
            "professional_scenarios": [],
            "practical_applications": []
        }
        
        # Topic-specific authentic assessments
        if "software" in topic.lower():
            authentic["real_world_contexts"].extend([
                "Actual software development projects",
                "Code review and optimization challenges",
                "System architecture design tasks"
            ])
        elif "carbon" in topic.lower() or "measurement" in topic.lower():
            authentic["real_world_contexts"].extend([
                "Real organization carbon audits", 
                "Live data analysis projects",
                "Policy recommendation development"
            ])
        else:
            authentic["real_world_contexts"].extend([
                "Industry case studies",
                "Consulting project simulations",
                "Professional practice scenarios"
            ])
            
        # EQF-specific scenarios
        if eqf_level >= 7:
            authentic["professional_scenarios"].extend([
                "Strategic decision-making simulations",
                "Research project leadership",
                "Policy development initiatives"
            ])
        else:
            authentic["professional_scenarios"].extend([
                "Team project participation",
                "Problem-solving challenges",
                "Implementation tasks"
            ])
            
        return authentic
        
    def _generate_module_assessments(
        self, 
        modules: List[Dict[str, Any]], 
        eqf_level: int, 
        topic: str
    ) -> List[Dict[str, Any]]:
        """Generate assessments for individual modules"""
        
        module_assessments = []
        
        for module in modules:
            # Determine appropriate assessment methods for this module
            module_methods = self._select_module_assessment_methods(module, eqf_level, topic)
            
            # Calculate assessment weighting
            weightings = self._calculate_assessment_weightings(module_methods, eqf_level)
            
            # Generate specific assessment tasks
            assessment_tasks = self._generate_assessment_tasks(module, module_methods, topic)
            
            module_assessment = {
                "module_title": module.get('title', 'Untitled Module'),
                "module_ects": module.get('ects', 5),
                "assessment_methods": module_methods,
                "assessment_weightings": weightings,
                "assessment_tasks": assessment_tasks,
                "learning_outcomes_assessed": self._identify_assessed_outcomes(module, module_methods),
                "assessment_criteria": self._generate_assessment_criteria(module, eqf_level),
                "submission_schedule": self._generate_submission_schedule(module, module_methods)
            }
            
            module_assessments.append(module_assessment)
            
        return module_assessments
        
    def _select_module_assessment_methods(
        self, 
        module: Dict[str, Any], 
        eqf_level: int, 
        topic: str
    ) -> List[str]:
        """Select appropriate assessment methods for a module"""
        
        methods = []
        
        # Get base methods for topic and EQF level
        base_methods = self.domain_knowledge.get_assessment_methods_for_topic(topic, eqf_level)
        
        # Analyze module characteristics
        title_lower = module.get('title', '').lower()
        keywords = [kw.lower() for kw in module.get('keywords', [])]
        
        # Select methods based on module type
        if any(word in title_lower for word in ['practical', 'lab', 'workshop', 'implementation']):
            methods.extend(['practical_assignment', 'skills_demonstration', 'portfolio'])
        elif any(word in title_lower for word in ['project', 'capstone', 'dissertation']):
            methods.extend(['project_work', 'presentation', 'report'])
        elif any(word in title_lower for word in ['analysis', 'research', 'study']):
            methods.extend(['research_project', 'case_study', 'written_exam'])
        else:
            # Use default methods from domain knowledge
            methods.extend(base_methods[:2])
            
        # Ensure variety and appropriateness
        if len(methods) < 2:
            methods.append('written_exam')
        if len(methods) > 3:
            methods = methods[:3]
            
        return list(set(methods))  # Remove duplicates
        
    def _calculate_assessment_weightings(
        self, 
        methods: List[str], 
        eqf_level: int
    ) -> Dict[str, int]:
        """Calculate percentage weightings for assessment methods"""
        
        # Base weightings by method type
        base_weights = {
            'written_exam': 30,
            'practical_assignment': 40,
            'project_work': 50,
            'case_study': 35,
            'presentation': 20,
            'portfolio': 45,
            'research_project': 60,
            'skills_demonstration': 35,
            'report': 40,
            'peer_review': 15
        }
        
        # Adjust based on EQF level
        if eqf_level >= 7:
            # Increase project and research weights
            base_weights['project_work'] = 60
            base_weights['research_project'] = 70
            base_weights['written_exam'] = 20
        elif eqf_level == 5:
            # Increase practical weights
            base_weights['practical_assignment'] = 50
            base_weights['skills_demonstration'] = 45
            base_weights['written_exam'] = 25
            
        # Calculate proportional weights
        total_base = sum(base_weights.get(method, 30) for method in methods)
        weightings = {}
        
        for method in methods:
            weight = base_weights.get(method, 30)
            percentage = round((weight / total_base) * 100)
            weightings[method] = percentage
            
        # Ensure total is 100%
        total = sum(weightings.values())
        if total != 100:
            # Adjust largest component
            largest_method = max(weightings.keys(), key=lambda k: weightings[k])
            weightings[largest_method] += 100 - total
            
        return weightings
        
    def _generate_assessment_tasks(
        self, 
        module: Dict[str, Any], 
        methods: List[str], 
        topic: str
    ) -> List[Dict[str, Any]]:
        """Generate specific assessment tasks"""
        
        tasks = []
        
        for method in methods:
            task = {
                "method": method,
                "title": self._generate_task_title(module, method),
                "description": self._generate_task_description(module, method, topic),
                "deliverables": self._get_task_deliverables(method),
                "evaluation_criteria": self._get_evaluation_criteria(method),
                "estimated_hours": self._estimate_task_hours(method, module.get('ects', 5))
            }
            tasks.append(task)
            
        return tasks
        
    def _generate_task_title(self, module: Dict[str, Any], method: str) -> str:
        """Generate title for assessment task"""
        
        module_title = module.get('title', 'Module')
        
        titles = {
            'written_exam': f"{module_title} - Comprehensive Examination",
            'practical_assignment': f"{module_title} - Practical Implementation Task",
            'project_work': f"{module_title} - Applied Project",
            'case_study': f"{module_title} - Case Study Analysis",
            'presentation': f"{module_title} - Professional Presentation",
            'portfolio': f"{module_title} - Learning Portfolio",
            'research_project': f"{module_title} - Research Investigation",
            'skills_demonstration': f"{module_title} - Competency Demonstration",
            'report': f"{module_title} - Technical Report"
        }
        
        return titles.get(method, f"{module_title} - Assessment Task")
        
    def _generate_task_description(
        self, 
        module: Dict[str, Any], 
        method: str, 
        topic: str
    ) -> str:
        """Generate description for assessment task"""
        
        module_title = module.get('title', '')
        
        descriptions = {
            'written_exam': f"Comprehensive examination testing theoretical knowledge and practical application of {module_title} concepts",
            'practical_assignment': f"Hands-on implementation task requiring application of {module_title} principles to solve real-world problems",
            'project_work': f"Independent project demonstrating mastery of {module_title} concepts through practical implementation",
            'case_study': f"Analysis of real-world scenario applying {module_title} methodologies and frameworks",
            'presentation': f"Professional presentation communicating key insights and applications from {module_title}",
            'portfolio': f"Curated collection of work demonstrating learning progression and competency development in {module_title}",
            'research_project': f"Independent research investigation exploring advanced aspects of {module_title}",
            'skills_demonstration': f"Practical demonstration of key competencies and skills developed through {module_title}",
            'report': f"Technical report analyzing and documenting findings from {module_title} investigations"
        }
        
        return descriptions.get(method, f"Assessment task for {module_title}")
        
    def _get_task_deliverables(self, method: str) -> List[str]:
        """Get deliverables for assessment method"""
        
        deliverables = {
            'written_exam': ["Completed exam paper"],
            'practical_assignment': ["Working solution", "Implementation documentation", "Reflection report"],
            'project_work': ["Project deliverables", "Technical documentation", "Presentation slides"],
            'case_study': ["Case study analysis report", "Recommendations document"],
            'presentation': ["Presentation slides", "Supporting materials", "Q&A responses"],
            'portfolio': ["Portfolio document", "Evidence artifacts", "Reflection essays"],
            'research_project': ["Research report", "Literature review", "Methodology documentation"],
            'skills_demonstration': ["Demonstration video/live performance", "Skills checklist", "Self-assessment"],
            'report': ["Technical report", "Executive summary", "Data/evidence appendix"]
        }
        
        return deliverables.get(method, ["Assessment submission"])
        
    def _get_evaluation_criteria(self, method: str) -> List[str]:
        """Get evaluation criteria for assessment method"""
        
        criteria = {
            'written_exam': ["Knowledge accuracy", "Conceptual understanding", "Application ability"],
            'practical_assignment': ["Technical competency", "Problem-solving approach", "Solution quality"],
            'project_work': ["Project scope and complexity", "Implementation quality", "Innovation and creativity"],
            'case_study': ["Analytical depth", "Evidence evaluation", "Recommendation quality"],
            'presentation': ["Content clarity", "Communication skills", "Professional delivery"],
            'portfolio': ["Learning evidence", "Reflection quality", "Professional development"],
            'research_project': ["Research rigor", "Originality", "Scholarly contribution"],
            'skills_demonstration': ["Competency demonstration", "Professional standards", "Practical application"],
            'report': ["Technical accuracy", "Communication clarity", "Professional standards"]
        }
        
        return criteria.get(method, ["Quality", "Completeness", "Professional standards"])
        
    def _estimate_task_hours(self, method: str, module_ects: int) -> int:
        """Estimate hours required for assessment task"""
        
        total_hours = module_ects * 25  # Standard ECTS conversion
        
        # Percentage of total module hours typically spent on assessment
        assessment_percentages = {
            'written_exam': 0.1,  # 10% for exam preparation and taking
            'practical_assignment': 0.3,  # 30% for hands-on work
            'project_work': 0.5,  # 50% for major projects
            'case_study': 0.25,  # 25% for analysis work
            'presentation': 0.15,  # 15% for preparation and delivery
            'portfolio': 0.2,  # 20% for compilation and reflection
            'research_project': 0.6,  # 60% for research projects
            'skills_demonstration': 0.2,  # 20% for preparation and demonstration
            'report': 0.3  # 30% for report writing
        }
        
        percentage = assessment_percentages.get(method, 0.25)
        return round(total_hours * percentage)
        
    def _identify_assessed_outcomes(
        self, 
        module: Dict[str, Any], 
        methods: List[str]
    ) -> List[str]:
        """Identify which learning outcomes are assessed"""
        
        module_outcomes = module.get('learning_outcomes', [])
        if isinstance(module_outcomes, str):
            module_outcomes = [module_outcomes]
            
        # If no specific outcomes, generate generic ones
        if not module_outcomes:
            module_title = module.get('title', '')
            module_outcomes = [
                f"Demonstrate understanding of {module_title} concepts",
                f"Apply {module_title} principles in practical contexts",
                f"Evaluate and analyze {module_title} applications"
            ]
            
        return module_outcomes[:5]  # Limit to 5 key outcomes
        
    def _generate_assessment_criteria(self, module: Dict[str, Any], eqf_level: int) -> Dict[str, Any]:
        """Generate detailed assessment criteria"""
        
        criteria = {
            "grading_scale": self._get_grading_scale(eqf_level),
            "pass_requirements": self._get_pass_requirements(eqf_level),
            "excellence_indicators": self._get_excellence_indicators(eqf_level),
            "rubric_categories": self._get_rubric_categories(module, eqf_level)
        }
        
        return criteria
        
    def _get_grading_scale(self, eqf_level: int) -> Dict[str, Any]:
        """Get appropriate grading scale"""
        
        if eqf_level >= 7:
            return {
                "scale_type": "letter_grade",
                "grades": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"],
                "pass_threshold": "C",
                "distinction_threshold": "A-"
            }
        else:
            return {
                "scale_type": "percentage",
                "range": "0-100",
                "pass_threshold": 50,
                "distinction_threshold": 85
            }
            
    def _get_pass_requirements(self, eqf_level: int) -> List[str]:
        """Get pass requirements for EQF level"""
        
        requirements = {
            5: [
                "Demonstrate basic competency in all learning outcomes",
                "Complete all required assessments", 
                "Achieve minimum 50% overall score"
            ],
            6: [
                "Demonstrate understanding and application of concepts",
                "Complete all assessments to satisfactory standard",
                "Achieve minimum 50% in each major assessment"
            ],
            7: [
                "Demonstrate advanced understanding and critical analysis",
                "Show evidence of independent learning and research",
                "Achieve minimum C grade in all assessments"
            ],
            8: [
                "Demonstrate original contribution and scholarly excellence",
                "Show evidence of advanced research capabilities",
                "Achieve minimum B grade in all major components"
            ]
        }
        
        return requirements.get(eqf_level, requirements[6])
        
    def _get_excellence_indicators(self, eqf_level: int) -> List[str]:
        """Get indicators of excellent performance"""
        
        indicators = {
            5: [
                "Exceptional practical skills demonstration",
                "Innovation in problem-solving approaches",
                "Leadership in group activities"
            ],
            6: [
                "Deep conceptual understanding",
                "Creative application of knowledge",
                "High-quality communication and presentation"
            ],
            7: [
                "Original analysis and insights",
                "Advanced research and critical thinking",
                "Professional-level output quality"
            ],
            8: [
                "Significant original contribution",
                "Exceptional scholarly rigor",
                "International publication quality"
            ]
        }
        
        return indicators.get(eqf_level, indicators[6])
        
    def _get_rubric_categories(self, module: Dict[str, Any], eqf_level: int) -> List[str]:
        """Get rubric categories for assessment"""
        
        base_categories = [
            "Knowledge and Understanding",
            "Application and Analysis", 
            "Communication and Presentation",
            "Professional Standards"
        ]
        
        if eqf_level >= 7:
            base_categories.extend([
                "Critical Thinking and Evaluation",
                "Research and Investigation"
            ])
            
        if eqf_level >= 8:
            base_categories.extend([
                "Original Contribution",
                "Scholarly Excellence"
            ])
            
        return base_categories
        
    def _generate_submission_schedule(
        self, 
        module: Dict[str, Any], 
        methods: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate submission schedule for assessments"""
        
        duration_weeks = module.get('duration_weeks', 12)
        schedule = []
        
        # Distribute assessments across module duration
        for i, method in enumerate(methods):
            # Calculate submission week based on method type and sequence
            if method == 'written_exam':
                week = duration_weeks  # Exams typically at end
            elif method in ['practical_assignment', 'skills_demonstration']:
                week = max(3, duration_weeks // 2)  # Mid-module
            elif method in ['project_work', 'research_project']:
                week = duration_weeks - 1  # Near end for major work
            else:
                week = min(duration_weeks, 3 + i * 3)  # Spaced throughout
                
            schedule.append({
                "assessment_method": method,
                "submission_week": week,
                "preparation_time": f"{week-2} weeks" if week > 2 else "2 weeks",
                "feedback_timeline": "2 weeks post-submission"
            })
            
        return sorted(schedule, key=lambda x: x['submission_week'])
        
    def _generate_summative_assessment(
        self, 
        topic: str, 
        eqf_level: int, 
        modules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summative assessment for entire curriculum"""
        
        total_ects = sum(module.get('ects', 5) for module in modules)
        
        if eqf_level >= 7 and total_ects >= 45:
            # Major capstone requirement
            summative = {
                "type": "capstone_project",
                "title": f"Capstone Project in {topic}",
                "description": f"Comprehensive project integrating learning across all {topic} modules",
                "ects_weight": min(15, total_ects // 4),
                "duration": "final semester",
                "deliverables": [
                    "Major project deliverable",
                    "Technical documentation",
                    "Professional presentation",
                    "Reflective analysis"
                ],
                "assessment_criteria": [
                    "Integration of module learning",
                    "Professional application",
                    "Innovation and creativity",
                    "Communication excellence"
                ]
            }
        else:
            # Integrative assessment
            summative = {
                "type": "integrative_assessment",
                "title": f"Integrated Assessment in {topic}",
                "description": f"Assessment demonstrating integration of {topic} knowledge and skills",
                "format": "portfolio_plus_presentation",
                "components": [
                    "Learning portfolio compilation",
                    "Reflective synthesis essay",
                    "Professional presentation"
                ],
                "assessment_focus": [
                    "Knowledge integration",
                    "Competency demonstration",
                    "Professional readiness"
                ]
            }
            
        return summative
        
    def _generate_formative_assessment(self, eqf_level: int) -> Dict[str, Any]:
        """Generate formative assessment strategy"""
        
        return {
            "frequency": "weekly" if eqf_level <= 6 else "bi-weekly",
            "methods": [
                "Self-assessment questionnaires",
                "Peer feedback sessions",
                "Progress check-ins",
                "Draft submissions",
                "Discussion participation"
            ],
            "feedback_mechanisms": [
                "Immediate automated feedback",
                "Instructor comments",
                "Peer review",
                "Self-reflection prompts"
            ],
            "purpose": [
                "Monitor learning progress",
                "Identify areas for improvement",
                "Build metacognitive skills",
                "Enhance learning experience"
            ]
        }
        
    def _generate_competency_assessment(self, topic: str, eqf_level: int) -> Dict[str, Any]:
        """Generate competency-based assessment framework"""
        
        competencies = self.domain_knowledge.get_all_competency_mappings(topic)
        
        return {
            "competency_frameworks": list(competencies.keys()) if competencies else ["Custom"],
            "assessment_approach": "evidence_based",
            "competency_levels": self._get_competency_levels(eqf_level),
            "evidence_requirements": self._get_evidence_requirements(eqf_level),
            "competency_mapping": competencies,
            "progression_tracking": {
                "method": "portfolio_based",
                "frequency": "continuous",
                "milestones": self._get_competency_milestones(eqf_level)
            }
        }
        
    def _get_competency_levels(self, eqf_level: int) -> List[str]:
        """Get competency levels for EQF level"""
        
        levels = {
            5: ["Developing", "Competent", "Proficient"],
            6: ["Developing", "Competent", "Proficient", "Advanced"],
            7: ["Competent", "Proficient", "Advanced", "Expert"],
            8: ["Proficient", "Advanced", "Expert", "Leading"]
        }
        
        return levels.get(eqf_level, levels[6])
        
    def _get_evidence_requirements(self, eqf_level: int) -> List[str]:
        """Get evidence requirements for competency assessment"""
        
        requirements = {
            5: [
                "Direct observation of performance",
                "Work samples and artifacts",
                "Supervisor/peer testimonials"
            ],
            6: [
                "Portfolio of work samples", 
                "Reflective documentation",
                "Performance evaluations",
                "Project outcomes"
            ],
            7: [
                "Research and analysis outputs",
                "Leadership evidence",
                "Professional contributions",
                "Peer recognition"
            ],
            8: [
                "Original research contributions",
                "Scholarly publications",
                "Expert recognition",
                "Field advancement evidence"
            ]
        }
        
        return requirements.get(eqf_level, requirements[6])
        
    def _get_competency_milestones(self, eqf_level: int) -> List[str]:
        """Get competency development milestones"""
        
        milestones = {
            5: ["Basic competency achieved", "Workplace readiness demonstrated"],
            6: ["Professional competency achieved", "Independent practice capability"],
            7: ["Advanced competency achieved", "Leadership capability demonstrated"],
            8: ["Expert competency achieved", "Field contribution demonstrated"]
        }
        
        return milestones.get(eqf_level, milestones[6])
        
    def _generate_quality_assurance_framework(self, eqf_level: int) -> Dict[str, Any]:
        """Generate quality assurance framework"""
        
        return {
            "moderation_process": {
                "internal_moderation": True,
                "external_moderation": eqf_level >= 7,
                "peer_review": eqf_level >= 6,
                "industry_input": eqf_level >= 6
            },
            "standardization_measures": [
                "Assessment rubrics",
                "Marking guidelines", 
                "Exemplar materials",
                "Calibration exercises"
            ],
            "review_cycles": {
                "annual_review": True,
                "continuous_improvement": True,
                "stakeholder_feedback": True
            },
            "compliance_standards": self._get_compliance_standards(eqf_level)
        }
        
    def _get_compliance_standards(self, eqf_level: int) -> List[str]:
        """Get compliance standards for EQF level"""
        
        standards = [
            "EQF Level Descriptors",
            "ECTS Guidelines",
            "Quality Assurance Standards"
        ]
        
        if eqf_level >= 6:
            standards.extend([
                "Professional Body Requirements",
                "Industry Standards"
            ])
            
        if eqf_level >= 7:
            standards.extend([
                "Research Ethics Guidelines",
                "Academic Integrity Standards"
            ])
            
        return standards
        
    def _generate_grading_framework(self, eqf_level: int) -> Dict[str, Any]:
        """Generate grading framework"""
        
        framework = {
            "grading_philosophy": self._get_grading_philosophy(eqf_level),
            "grade_boundaries": self._get_grade_boundaries(eqf_level),
            "grade_descriptors": self._get_grade_descriptors(eqf_level),
            "aggregation_method": self._get_aggregation_method(eqf_level),
            "special_considerations": self._get_special_considerations()
        }
        
        return framework
        
    def _get_grading_philosophy(self, eqf_level: int) -> str:
        """Get grading philosophy for EQF level"""
        
        philosophies = {
            5: "Competency-based grading focusing on workplace readiness and practical skills demonstration",
            6: "Criterion-referenced grading measuring achievement against defined learning outcomes",
            7: "Advanced criterion-referenced grading with emphasis on critical thinking and research skills",
            8: "Scholarly grading standards reflecting research excellence and original contribution"
        }
        
        return philosophies.get(eqf_level, philosophies[6])
        
    def _get_grade_boundaries(self, eqf_level: int) -> Dict[str, Any]:
        """Get grade boundaries for EQF level"""
        
        if eqf_level >= 7:
            return {
                "A+": "95-100%",
                "A": "85-94%", 
                "A-": "80-84%",
                "B+": "75-79%",
                "B": "70-74%",
                "B-": "65-69%",
                "C+": "60-64%",
                "C": "50-59%",
                "F": "0-49%"
            }
        else:
            return {
                "Distinction": "85-100%",
                "Merit": "70-84%",
                "Pass": "50-69%",
                "Fail": "0-49%"
            }
            
    def _get_grade_descriptors(self, eqf_level: int) -> Dict[str, str]:
        """Get grade descriptors"""
        
        if eqf_level >= 7:
            return {
                "A": "Exceptional achievement demonstrating mastery and original thinking",
                "B": "Good achievement demonstrating solid understanding and application",
                "C": "Satisfactory achievement meeting minimum learning outcome requirements",
                "F": "Inadequate achievement failing to meet minimum requirements"
            }
        else:
            return {
                "Distinction": "Exceptional work demonstrating mastery of subject matter",
                "Merit": "Good quality work demonstrating solid understanding",
                "Pass": "Satisfactory work meeting minimum learning requirements",
                "Fail": "Work that does not meet minimum learning requirements"
            }
            
    def _get_aggregation_method(self, eqf_level: int) -> Dict[str, Any]:
        """Get grade aggregation method"""
        
        return {
            "method": "weighted_average",
            "module_weighting": "ects_based",
            "minimum_requirements": [
                "Pass all core modules",
                "Achieve overall average above pass threshold"
            ],
            "compensation_rules": eqf_level < 7,  # Allow compensation for lower levels
            "progression_requirements": self._get_progression_requirements(eqf_level)
        }
        
    def _get_progression_requirements(self, eqf_level: int) -> List[str]:
        """Get progression requirements"""
        
        requirements = [
            "Complete all required modules",
            "Achieve minimum ECTS credits"
        ]
        
        if eqf_level >= 6:
            requirements.append("Demonstrate competency in all learning outcomes")
            
        if eqf_level >= 7:
            requirements.extend([
                "Complete research component successfully",
                "Demonstrate independent learning capability"
            ])
            
        return requirements
        
    def _get_special_considerations(self) -> List[str]:
        """Get special considerations for grading"""
        
        return [
            "Reasonable adjustments for students with disabilities",
            "Extensions for extenuating circumstances",
            "Alternative assessment formats when appropriate",
            "Recognition of prior learning where applicable",
            "Support for non-native speakers"
        ]
        
    def _generate_assessment_calendar(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate assessment calendar"""
        
        total_weeks = max([m.get('duration_weeks', 12) for m in modules])
        calendar = {
            "total_duration_weeks": total_weeks,
            "assessment_periods": [],
            "submission_deadlines": [],
            "feedback_schedule": [],
            "exam_periods": []
        }
        
        # Generate assessment periods
        num_periods = math.ceil(total_weeks / 6)  # 6-week assessment periods
        
        for period in range(num_periods):
            start_week = period * 6 + 1
            end_week = min((period + 1) * 6, total_weeks)
            
            calendar["assessment_periods"].append({
                "period": period + 1,
                "weeks": f"{start_week}-{end_week}",
                "focus": "Continuous assessment and formative feedback",
                "major_submissions": end_week == total_weeks
            })
            
        # Generate submission deadlines
        for i, module in enumerate(modules):
            module_duration = module.get('duration_weeks', 12)
            deadline_week = min(module_duration - 1, total_weeks - 1)
            
            calendar["submission_deadlines"].append({
                "module": module.get('title', 'Untitled Module'),
                "submission_week": deadline_week,
                "assessment_type": "Module completion",
                "buffer_time": "1 week before module end"
            })
            
        # Generate feedback schedule
        for week in range(2, total_weeks + 1, 2):  # Bi-weekly feedback
            calendar["feedback_schedule"].append({
                "week": week,
                "type": "Formative feedback",
                "method": "Online feedback or tutorial"
            })
            
        # Generate exam periods
        if total_weeks >= 12:
            calendar["exam_periods"].extend([
                {
                    "period": "Mid-term",
                    "week": total_weeks // 2,
                    "type": "Formative assessment"
                },
                {
                    "period": "Final", 
                    "week": total_weeks,
                    "type": "Summative assessment"
                }
            ])
        else:
            calendar["exam_periods"].append({
                "period": "Final",
                "week": total_weeks,
                "type": "Summative assessment"
            })
            
        return calendar
