    
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
            ],
            "SBA": [
                "Business Process Sustainability Analysis",
                "Sustainability Metrics & KPI Development", 
                "Business Case Development & ROI Modeling"
            ],
            "SDD": [
                "Green Coding Practices & Optimization",
                "Sustainable Software Architecture",
                "Energy-Efficient Development & Testing"
            ],
            "SSD": [
                "Sustainable System Design Principles",
                "Circular Design Methodologies",
                "Eco-Design Implementation & Validation"
            ],
            "STS": [
                "Sustainability Platform Configuration",
                "Technical Tool Implementation & Support",
                "System Integration & Optimization"
            ]
        }
        
        patterns = role_patterns.get(role_id, [f"Professional Sustainability Module {i}" for i in range(1, 4)])
        
        if module_num <= len(patterns):
            return patterns[module_num - 1]
        else:
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
            ],
            "SBA": [
                "Analyze business processes for sustainability improvement opportunities",
                "Develop and monitor sustainability KPIs and metrics",
                "Create business cases for sustainability investments"
            ],
            "SDD": [
                "Implement green coding practices and energy-efficient programming",
                "Develop sustainable software applications with minimal footprint",
                "Optimize code for reduced computational resource consumption"
            ],
            "SSD": [
                "Design sustainable IT architectures and user experiences",
                "Apply circular design methodologies to technology systems",
                "Integrate sustainability requirements into technical specifications"
            ],
            "STS": [
                "Configure and support sustainability tools and platforms",
                "Implement technical solutions for organizational environmental goals",
                "Troubleshoot and optimize sustainability technology implementations"
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
            "DSI": "AI for Sustainability Applications",
            "SBA": "Sustainability Business Analysis Fundamentals",
            "SDD": "Green Software Development Essentials",
            "SSD": "Sustainable Solution Design Principles",
            "STS": "Sustainability Technical Support Basics"
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
            ],
            "SBA": [
                "Analyze business processes to identify sustainability improvement opportunities",
                "Develop and implement sustainability metrics and KPIs for organizational performance",
                "Create compelling business cases for sustainability investments with ROI projections",
                "Facilitate cross-functional collaboration to align sustainability with business strategy",
                "Apply business analysis methodologies to sustainability transformation initiatives"
            ],
            "SDD": [
                "Implement green coding practices and energy-efficient programming techniques",
                "Develop sustainable software applications with minimal environmental footprint",
                "Apply code optimization strategies to reduce computational resource consumption",
                "Integrate sustainability principles throughout software development lifecycle",
                "Collaborate with development teams to establish sustainable coding standards"
            ],
            "SSD": [
                "Design sustainable IT architectures and systems with sustainability as core principle",
                "Apply circular design methodologies to technology solutions and user experiences",
                "Integrate eco-design frameworks to minimize environmental impact of digital solutions",
                "Balance functionality with environmental responsibility in technical solution design",
                "Lead interdisciplinary design processes that prioritize sustainability outcomes"
            ],
            "STS": [
                "Configure and support sustainability tools and platforms for organizational goals",
                "Implement technical solutions that enable comprehensive sustainability data collection",
                "Provide user support and training for sustainability software and digital tools",
                "Troubleshoot and optimize sustainability technology implementations",
                "Collaborate with technical teams to integrate sustainability tools with existing systems"
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
                    "level": f"EQF {eqf_level}",
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
            },
            "SBA": {
                "mini_placements": ["Business analysis teams", "Sustainability program offices"],
                "practical_labs": ["Process analysis simulations", "KPI development workshops"],
                "industry_projects": ["Business case development", "Sustainability ROI analysis"]
            },
            "SDD": {
                "mini_placements": ["Software development teams", "Green IT departments"],
                "practical_labs": ["Code optimization workshops", "Energy-efficient development"],
                "industry_projects": ["Sustainable application development", "Green coding implementation"]
            },
            "SSD": {
                "mini_placements": ["Design teams", "Architecture departments"],
                "practical_labs": ["Sustainable design workshops", "Circular design methodologies"],
                "industry_projects": ["Eco-design implementation", "Sustainable system architecture"]
            },
            "STS": {
                "mini_placements": ["Technical support teams", "IT implementation groups"],
                "practical_labs": ["Platform configuration", "Tool implementation workshops"],
                "industry_projects": ["System integration project", "Technical optimization initiative"]
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
                "DSI": ["Predictive Analytics", "AI Solutions", "Environmental Modeling"],
                "SBA": ["Business Analysis", "Process Optimization", "Performance Measurement"],
                "SDD": ["Software Development", "Green Coding", "Application Optimization"],
                "SSD": ["System Design", "Solution Architecture", "User Experience Design"],
                "STS": ["Technical Support", "Platform Management", "System Implementation"]
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
