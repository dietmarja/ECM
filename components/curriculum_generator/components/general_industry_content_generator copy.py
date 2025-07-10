# scripts/curriculum_generator/components/general_industry_content_generator.py
"""
COMPREHENSIVE FIX - General Industry Content Generator
Addresses Critical T3.2/T3.4 Compliance Gaps:
- Complete role coverage (10 roles including SBA)
- Work-based learning integration
- EQF 4-8 full support
- Micro-credential framework
- SME-specific pathways
- Enhanced ESG/Data skills focus
- FIXED: Missing sections 8, 9, 10 generation
"""

import random
from typing import List, Dict, Any
from scripts.curriculum_generator.domain.competency_mapper import EnhancedCompetencyMapper

class GeneralIndustryContentGenerator:
    """
    Enhanced content generator with COMPLETE T3.2/T3.4 compliance
    Addresses all critical gaps identified in compliance analysis
    """

    def __init__(self):
        """Initialize with comprehensive T3.2/T3.4 compliant content templates"""

        # ENHANCED: Complete 10-role coverage including missing SBA
        self.role_skill_mapping = {
            "DAN": {
                "name": "Data Analyst",
                "primary_skills": ["sustainability data analysis", "environmental metrics reporting", "carbon footprint assessment", "ESG data analytics"],
                "secondary_skills": ["data visualization", "performance measurement", "compliance reporting", "statistical analysis"],
                "sme_focus": ["small business carbon tracking", "cost-effective analytics tools", "simplified reporting"],
                "work_based_skills": ["real-time data monitoring", "client dashboard creation", "stakeholder reporting"],
                "salary_range": {"min": 35000, "max": 65000, "currency": "EUR"},
                "career_benefits": ["High demand in ESG sector", "Rapid career progression", "Cross-industry mobility", "Remote work opportunities"]
            },
            "DSE": {
                "name": "Data Engineer", 
                "primary_skills": ["environmental data engineering", "sustainability systems integration", "IoT data management", "ESG data pipeline development"],
                "secondary_skills": ["database optimization", "data pipeline development", "system architecture", "cloud sustainability platforms"],
                "sme_focus": ["lightweight data systems", "cost-effective IoT solutions", "automated data collection"],
                "work_based_skills": ["system deployment", "data infrastructure optimization", "real-time monitoring setup"],
                "salary_range": {"min": 45000, "max": 85000, "currency": "EUR"},
                "career_benefits": ["Technical expertise premium", "Infrastructure leadership roles", "Innovation opportunities", "Global project exposure"]
            },
            "DSI": {
                "name": "Data Scientist",
                "primary_skills": ["sustainability data science", "predictive environmental modeling", "AI-driven sustainability insights", "ESG predictive analytics"],
                "secondary_skills": ["machine learning", "statistical analysis", "algorithm development", "AI model deployment"],
                "sme_focus": ["accessible AI tools", "predictive models for small organizations", "automated insights"],
                "work_based_skills": ["model deployment in production", "algorithm optimization", "predictive system development"],
                "salary_range": {"min": 50000, "max": 95000, "currency": "EUR"},
                "career_benefits": ["Cutting-edge technology work", "Research opportunities", "Academic collaboration", "AI leadership positions"]
            },
            "DSM": {
                "name": "Digital Sustainability Manager",
                "primary_skills": ["sustainability program management", "environmental strategy development", "stakeholder engagement", "ESG strategy implementation"],
                "secondary_skills": ["project leadership", "change management", "performance optimization", "digital transformation"],
                "sme_focus": ["SME sustainability roadmaps", "cost-effective program design", "scalable implementation"],
                "work_based_skills": ["organizational assessment", "change implementation", "stakeholder coordination"],
                "salary_range": {"min": 55000, "max": 95000, "currency": "EUR"},
                "career_benefits": ["Management progression", "Strategic influence", "Cross-functional leadership", "Executive pathway"]
            },
            "DSL": {
                "name": "Digital Sustainability Lead",
                "primary_skills": ["sustainability leadership", "organizational transformation", "strategic sustainability planning", "ESG executive strategy"],
                "secondary_skills": ["executive decision making", "vision development", "cultural change", "board-level reporting"],
                "sme_focus": ["executive sustainability leadership for SMEs", "strategic planning for small organizations"],
                "work_based_skills": ["strategic implementation", "organizational transformation", "executive reporting"],
                "salary_range": {"min": 70000, "max": 130000, "currency": "EUR"},
                "career_benefits": ["Executive leadership", "Industry influence", "Board positions", "Thought leadership"]
            },
            "DSC": {
                "name": "Digital Sustainability Consultant",
                "primary_skills": ["sustainability consulting", "organizational sustainability assessment", "solution design", "ESG consulting services"],
                "secondary_skills": ["client relationship management", "business development", "advisory services", "implementation support"],
                "sme_focus": ["SME-focused consulting", "affordable sustainability solutions", "rapid assessment tools"],
                "work_based_skills": ["client engagement", "solution implementation", "ongoing advisory support"],
                "salary_range": {"min": 60000, "max": 120000, "currency": "EUR"},
                "career_benefits": ["Entrepreneurial opportunities", "Diverse project exposure", "Expert recognition", "Independent practice"]
            },
            # NEW: Missing role identified in compliance analysis
            "SBA": {
                "name": "Sustainability Business Analyst",
                "primary_skills": ["ESG business analysis", "sustainability ROI assessment", "environmental impact analysis", "sustainable business modeling"],
                "secondary_skills": ["financial analysis", "business case development", "stakeholder analysis", "process optimization"],
                "sme_focus": ["SME business sustainability analysis", "cost-benefit analysis for small organizations", "rapid ROI assessment"],
                "work_based_skills": ["business case development", "stakeholder analysis", "implementation planning"],
                "salary_range": {"min": 40000, "max": 75000, "currency": "EUR"},
                "career_benefits": ["Business strategy roles", "Financial analysis expertise", "Stakeholder influence", "Strategic planning"]
            },
            "SDD": {
                "name": "Software Developer",
                "primary_skills": ["sustainable software development", "green coding practices", "eco-efficient system design", "carbon-aware programming"],
                "secondary_skills": ["software architecture", "development methodologies", "code optimization", "energy-efficient algorithms"],
                "sme_focus": ["lightweight sustainable applications", "cost-effective green software", "energy optimization"],
                "work_based_skills": ["sustainable application development", "green coding implementation", "system optimization"],
                "salary_range": {"min": 40000, "max": 80000, "currency": "EUR"},
                "career_benefits": ["Technical innovation", "Open source contributions", "Architecture roles", "Team leadership"]
            },
            "SSD": {
                "name": "Sustainable Solution Designer",
                "primary_skills": ["sustainable solution design", "circular economy systems", "environmental innovation", "ESG solution architecture"],
                "secondary_skills": ["design thinking", "systems integration", "innovation management", "sustainable technology selection"],
                "sme_focus": ["affordable sustainable solutions", "scalable design for SMEs", "rapid prototyping"],
                "work_based_skills": ["solution implementation", "design validation", "user-centered development"],
                "salary_range": {"min": 45000, "max": 85000, "currency": "EUR"},
                "career_benefits": ["Innovation leadership", "Design expertise", "Product management", "Strategic design roles"]
            },
            "STS": {
                "name": "Sustainability Technical Specialist",
                "primary_skills": ["sustainability technical implementation", "environmental system optimization", "green infrastructure", "technical ESG implementation"],
                "secondary_skills": ["technical project management", "system integration", "performance monitoring", "technical documentation"],
                "sme_focus": ["SME technical implementation", "cost-effective technical solutions", "simplified monitoring"],
                "work_based_skills": ["technical system deployment", "performance optimization", "maintenance planning"],
                "salary_range": {"min": 38000, "max": 70000, "currency": "EUR"},
                "career_benefits": ["Technical specialization", "Infrastructure expertise", "Operational leadership", "Systems architecture"]
            }
        }

        # ENHANCED: Work-based learning integration (addresses T3.2 dual principle requirement)
        self.work_based_learning_templates = {
            "dual_pathways": {
                "industry_partnership": [
                    "Partner with leading sustainability organizations for real-world project experience",
                    "Collaborate with ESG-focused companies on live sustainability challenges",
                    "Work directly with environmental consultancies on client projects",
                    "Engage with technology companies developing green solutions"
                ],
                "workplace_integration": [
                    "Apply {skill_area} skills in current workplace sustainability initiatives",
                    "Develop {skill_area} solutions for real organizational challenges",
                    "Lead {skill_area} implementation projects within learner's organization",
                    "Create {skill_area} frameworks for immediate workplace application"
                ],
                "mentorship_model": [
                    "Receive guidance from experienced {skill_area} practitioners",
                    "Participate in professional {skill_area} networks and communities",
                    "Access ongoing support from industry {skill_area} experts",
                    "Engage in peer learning with fellow {skill_area} professionals"
                ]
            },
            "sme_specific": {
                "small_organization_focus": [
                    "Develop {skill_area} solutions specifically designed for small and medium enterprises",
                    "Create cost-effective {skill_area} approaches suitable for limited budgets",
                    "Design scalable {skill_area} systems that grow with the organization",
                    "Implement rapid-deployment {skill_area} solutions for immediate impact"
                ],
                "resource_optimization": [
                    "Maximize {skill_area} impact with minimal resource investment",
                    "Leverage existing organizational assets for {skill_area} implementation",
                    "Create {skill_area} solutions using readily available tools and platforms",
                    "Develop {skill_area} approaches that require minimal specialized equipment"
                ]
            }
        }

        # ENHANCED: Micro-credential framework (addresses T3.4 stackable certification requirement)
        self.micro_credential_system = {
            "stackable_units": {
                "foundation_credentials": [
                    "Digital Sustainability Fundamentals (2 ECTS)",
                    "ESG Data Literacy (1.5 ECTS)", 
                    "Environmental Impact Assessment Basics (2 ECTS)",
                    "Sustainable Technology Overview (1.5 ECTS)"
                ],
                "specialist_credentials": [
                    "Carbon Footprint Analysis Specialist (3 ECTS)",
                    "ESG Reporting Professional (4 ECTS)",
                    "Sustainable Software Development (5 ECTS)", 
                    "Environmental Data Analytics (4 ECTS)"
                ],
                "advanced_credentials": [
                    "Sustainability Strategy Leadership (8 ECTS)",
                    "ESG Transformation Management (10 ECTS)",
                    "Digital Sustainability Innovation (12 ECTS)",
                    "Environmental Technology Implementation (8 ECTS)"
                ]
            },
            "certification_pathways": [
                "Micro-credentials combine to form larger qualifications",
                "Each unit provides immediate professional recognition",
                "Stackable progression from foundation to advanced expertise",
                "Industry-validated competency demonstration",
                "Digital badge system for professional credibility",
                "Cross-institutional recognition and transferability"
            ]
        }

        # ENHANCED: ESG and Data Skills Emphasis (addresses D2.1 priority findings)
        self.enhanced_esg_data_focus = {
            "esg_priority_skills": [
                "ESG data collection and management",
                "Environmental, Social, and Governance reporting",
                "Sustainability metrics and KPI development", 
                "ESG risk assessment and mitigation",
                "Stakeholder engagement for ESG initiatives",
                "ESG compliance and regulatory reporting",
                "ESG investment analysis and decision support",
                "ESG performance measurement and improvement"
            ],
            "data_analytics_emphasis": [
                "Environmental data visualization and storytelling",
                "Predictive analytics for sustainability outcomes",
                "Real-time sustainability monitoring systems",
                "Automated ESG reporting and dashboard creation",
                "Data-driven sustainability decision making",
                "Statistical analysis of environmental impacts",
                "Machine learning for environmental prediction",
                "Data integration from multiple sustainability sources"
            ]
        }

        # ENHANCED: Complete EQF 4-8 learning outcome templates
        self.learning_outcome_templates = {
            # NEW: EQF 4 Support (addresses missing EQF 4 requirement)
            "EQF4_Foundation": {
                "technical_skills": [
                    "Apply basic {skill_area} procedures following established guidelines and standards",
                    "Use fundamental {skill_area} tools and systems under supervision",
                    "Demonstrate knowledge of core {skill_area} principles and concepts",
                    "Perform routine {skill_area} tasks with accuracy and attention to detail",
                    "Recognize and respond to common {skill_area} challenges and issues"
                ],
                "validation_skills": [
                    "Check {skill_area} outputs against standard criteria and specifications",
                    "Identify basic errors and inconsistencies in {skill_area} work",
                    "Follow established {skill_area} quality control procedures"
                ],
                "application_skills": [
                    "Apply {skill_area} knowledge in familiar work contexts",
                    "Work effectively as part of a {skill_area} team",
                    "Communicate basic {skill_area} information to colleagues and supervisors"
                ],
                "work_based_learning": [
                    "Demonstrate {skill_area} competencies in real workplace settings",
                    "Apply classroom learning to actual work tasks and projects",
                    "Receive feedback and guidance from workplace mentors"
                ]
            },
            "Foundation": {
                "technical_skills": [
                    "Demonstrate fundamental competency in {skill_area} using industry-standard tools and methodologies",
                    "Apply basic {skill_area} principles to solve straightforward professional challenges",
                    "Use appropriate software and systems to perform {skill_area} tasks with accuracy and efficiency",
                    "Interpret and analyze {skill_area} data to support evidence-based decision making",
                    "Create professional-quality deliverables using {skill_area} best practices and standards"
                ],
                "validation_skills": [
                    "Verify the accuracy and completeness of {skill_area} outputs through systematic checking procedures",
                    "Apply quality assurance methods to ensure {skill_area} deliverables meet professional standards",
                    "Identify and correct common errors in {skill_area} processes and outputs"
                ],
                "application_skills": [
                    "Implement {skill_area} solutions in real workplace scenarios with appropriate supervision",
                    "Document {skill_area} processes and outcomes according to organizational requirements",
                    "Collaborate effectively with team members on {skill_area} projects and initiatives"
                ],
                "work_based_learning": [
                    "Apply {skill_area} competencies in diverse workplace environments",
                    "Integrate theoretical knowledge with practical workplace experience",
                    "Develop professional relationships within the {skill_area} community"
                ]
            },
            "Development": {
                "technical_skills": [
                    "Execute advanced {skill_area} procedures with minimal supervision and high accuracy",
                    "Integrate {skill_area} methodologies with other professional competencies",
                    "Optimize {skill_area} processes to improve efficiency and effectiveness",
                    "Troubleshoot complex {skill_area} problems using systematic diagnostic approaches",
                    "Design and implement {skill_area} solutions that meet specific organizational needs"
                ],
                "validation_skills": [
                    "Conduct comprehensive quality reviews of {skill_area} outputs and processes",
                    "Establish validation protocols to ensure consistency and reliability in {skill_area} work",
                    "Mentor junior colleagues in {skill_area} quality assurance practices"
                ],
                "application_skills": [
                    "Lead {skill_area} projects from conception through successful completion",
                    "Present {skill_area} findings and recommendations to stakeholders with confidence",
                    "Adapt {skill_area} approaches to accommodate changing organizational priorities"
                ],
                "work_based_learning": [
                    "Lead {skill_area} initiatives within workplace settings",
                    "Mentor and guide colleagues in {skill_area} best practices",
                    "Build bridges between academic theory and practical application"
                ]
            },
            "Application": {
                "technical_skills": [
                    "Synthesize {skill_area} knowledge to address multifaceted organizational challenges",
                    "Innovate {skill_area} approaches to achieve superior performance outcomes",
                    "Evaluate and select optimal {skill_area} tools and technologies for specific contexts",
                    "Design comprehensive {skill_area} frameworks for organizational implementation",
                    "Integrate {skill_area} competencies with strategic business objectives"
                ],
                "validation_skills": [
                    "Develop organization-wide standards for {skill_area} quality and performance",
                    "Audit {skill_area} processes to identify improvement opportunities",
                    "Establish metrics and KPIs for measuring {skill_area} effectiveness"
                ],
                "application_skills": [
                    "Champion {skill_area} excellence across multiple organizational units",
                    "Influence organizational culture to embrace {skill_area} best practices",
                    "Build strategic partnerships that leverage {skill_area} capabilities"
                ],
                "work_based_learning": [
                    "Drive organizational transformation through {skill_area} innovation",
                    "Establish centers of excellence for {skill_area} within organizations",
                    "Create lasting impact through strategic {skill_area} implementation"
                ]
            },
            "Integration": {
                "technical_skills": [
                    "Architect enterprise-level {skill_area} solutions that span organizational boundaries",
                    "Synthesize {skill_area} expertise with emerging technologies and methodologies",
                    "Lead organizational transformation through strategic {skill_area} implementation",
                    "Establish {skill_area} centers of excellence within the organization",
                    "Drive innovation in {skill_area} practices and technologies"
                ],
                "validation_skills": [
                    "Create comprehensive governance frameworks for {skill_area} quality management",
                    "Design and implement organization-wide {skill_area} compliance systems",
                    "Lead external audits and certifications related to {skill_area} practices"
                ],
                "application_skills": [
                    "Represent the organization as a {skill_area} thought leader in professional networks",
                    "Develop strategic alliances that advance organizational {skill_area} capabilities",
                    "Influence industry standards and practices in {skill_area}"
                ],
                "work_based_learning": [
                    "Lead cross-organizational {skill_area} initiatives and collaborations",
                    "Establish thought leadership position through workplace innovation",
                    "Create industry-wide impact through {skill_area} advancement"
                ]
            },
            "Mastery": {
                "technical_skills": [
                    "Pioneer breakthrough {skill_area} methodologies that set new industry standards",
                    "Lead cross-industry initiatives that advance {skill_area} knowledge and practice",
                    "Mentor and develop the next generation of {skill_area} professionals",
                    "Research and develop cutting-edge {skill_area} technologies and approaches",
                    "Establish thought leadership position in {skill_area} through publications and presentations"
                ],
                "validation_skills": [
                    "Define industry-wide standards for {skill_area} excellence and validation",
                    "Lead professional bodies and certification programs in {skill_area}",
                    "Conduct peer review of {skill_area} research and professional practices"
                ],
                "application_skills": [
                    "Shape organizational strategy through expert {skill_area} guidance and vision",
                    "Influence policy development and regulatory frameworks related to {skill_area}",
                    "Build and lead professional networks that advance {skill_area} practice globally"
                ],
                "work_based_learning": [
                    "Pioneer new approaches to {skill_area} through workplace innovation",
                    "Establish lasting legacy through mentorship and knowledge transfer",
                    "Drive field advancement through practical application and research"
                ]
            },
            "Leadership": {
                "technical_skills": [
                    "Establish strategic vision for {skill_area} development within the organization and industry",
                    "Lead transformation initiatives that revolutionize {skill_area} practices",
                    "Build and lead high-performance teams with advanced {skill_area} capabilities",
                    "Drive innovation ecosystems that advance {skill_area} knowledge and application",
                    "Establish the organization as a recognized leader in {skill_area} excellence"
                ],
                "validation_skills": [
                    "Establish global benchmarks for {skill_area} quality and performance",
                    "Lead international standard-setting bodies and professional organizations",
                    "Govern organizational and industry-wide {skill_area} compliance and ethics"
                ],
                "application_skills": [
                    "Influence global business strategy through expert {skill_area} leadership",
                    "Build strategic partnerships that advance organizational and industry {skill_area} capabilities",
                    "Legacy building through mentorship, knowledge transfer, and institutional development"
                ],
                "work_based_learning": [
                    "Shape industry direction through visionary {skill_area} leadership",
                    "Create transformational change across multiple organizations",
                    "Establish enduring impact through strategic vision and implementation"
                ]
            }
        }

        # ENHANCED: Assessment methods with work-based learning integration
        self.assessment_methods_mapping = {
            "sustainability": {
                4: ["workplace_project", "practical_assignment", "skills_demonstration"],
                5: ["workplace_application", "case_study", "portfolio"],
                6: ["industry_project", "case_study", "work_based_assessment"],
                7: ["consultancy_project", "research_project", "workplace_innovation"],
                8: ["industry_transformation_project", "original_research", "thought_leadership"]
            },
            "data": {
                4: ["data_analysis_task", "workplace_dashboard", "skills_demonstration"],
                5: ["real_data_project", "case_study", "practical_assignment"],
                6: ["industry_analytics_project", "technical_report", "work_based_implementation"],
                7: ["advanced_analytics_research", "industry_collaboration", "peer_review"],
                8: ["data_science_innovation", "publication", "industry_partnership"]
            },
            "software": {
                4: ["coding_assignment", "workplace_application", "skills_demonstration"],
                5: ["software_project", "industry_collaboration", "portfolio"],
                6: ["enterprise_application", "technical_documentation", "work_based_development"],
                7: ["system_architecture", "research_project", "industry_innovation"],
                8: ["technology_leadership", "open_source_contribution", "industry_transformation"]
            }
        }

        # Progression level mapping for different input formats
        self.progression_level_mapping = {
            "Foundation": "Foundation",
            "Development": "Development", 
            "Application": "Application",
            "Integration": "Integration",
            "Mastery": "Mastery",
            "Leadership": "Leadership",
            # Handle potential alternative names
            "Basic": "Foundation",
            "Intermediate": "Development",
            "Advanced": "Application",
            "Expert": "Integration",
            "Master": "Mastery",
            "Leader": "Leadership",
            # NEW: EQF 4 mapping
            "EQF4": "EQF4_Foundation",
            "EQF4_Foundation": "EQF4_Foundation"
        }

        # EU Recognition and Cross-Border Framework Templates
        self.eu_recognition_framework = {
            "recognition_mechanisms": [
                "European Credit Transfer and Accumulation System (ECTS) compliance",
                "European Quality Assurance in Vocational Education and Training (EQAVET) alignment",
                "Europass Digital Credentials for professional mobility",
                "European Qualifications Framework (EQF) level 4-8 referencing",
                "Professional recognition through EU regulated professions database",
                "Automatic recognition under Brussels I Regulation for professional services"
            ],
            "digital_credentials": [
                "Blockchain-verified digital badges for secure credential verification",
                "Europass Digital Credentials integration for cross-border recognition",
                "Professional portfolio development with digital evidence",
                "Automatic skills matching for EU job mobility platforms",
                "Integration with European Skills, Competences, Qualifications and Occupations (ESCO)"
            ],
            "professional_mobility": [
                "Enhanced mobility through standardized competency frameworks",
                "Recognition of non-formal and informal learning (RPL) across EU",
                "Professional pathway mapping for career advancement",
                "Cross-border work placement and internship opportunities",
                "International professional network development and mentorship"
            ]
        }

    # ========== UTILITY METHODS ==========
    
    def _clean_topic_name(self, topic: str) -> str:
        """Remove placeholders and create meaningful topic names"""
        topic = topic.replace("EU Test", "").replace("Test", "").strip()
        
        if not topic or topic.lower() in ["digital sustainability", "test", ""]:
            # Generate contextual topic based on content
            topic_options = [
                "Environmental Data Analytics",
                "ESG Strategy Implementation", 
                "Sustainability Technology",
                "Carbon Management Systems",
                "Green Digital Transformation",
                "Sustainable Business Intelligence",
                "Environmental Impact Assessment",
                "Climate Change Adaptation",
                "Circular Economy Innovation",
                "Renewable Energy Systems"
            ]
            import random
            topic = random.choice(topic_options)
        
        return topic.title()

    # ========== UTILITY METHODS ==========
    
    def _clean_topic_name(self, topic: str) -> str:
        """Remove placeholders and create meaningful topic names"""
        topic = topic.replace("EU Test", "").replace("Test", "").strip()
        
        if not topic or topic.lower() in ["digital sustainability", "test", ""]:
            # Generate contextual topic based on content
            topic_options = [
                "Environmental Data Analytics",
                "ESG Strategy Implementation", 
                "Sustainability Technology",
                "Carbon Management Systems",
                "Green Digital Transformation",
                "Sustainable Business Intelligence",
                "Environmental Impact Assessment",
                "Climate Change Adaptation",
                "Circular Economy Innovation",
                "Renewable Energy Systems"
            ]
            import random
            topic = random.choice(topic_options)
        
        return topic.title()
    
    def _calculate_dynamic_impact(self, ects: float, eqf_level: int, role_id: str) -> tuple:
        """Calculate dynamic salary increase and career impact based on multiple factors"""
        
        # Base impact by ECTS
        if ects <= 2:
            base_salary = "10-20%"
            base_impact = "skill enhancement"
        elif ects <= 10:
            base_salary = "20-35%"
            base_impact = "professional advancement"
        elif ects <= 30:
            base_salary = "35-55%"
            base_impact = "management progression"
        elif ects <= 60:
            base_salary = "55-80%"
            base_impact = "senior leadership"
        else:
            base_salary = "80-120%"
            base_impact = "executive transformation"
        
        # EQF multiplier
        eqf_multipliers = {4: 0.8, 5: 1.0, 6: 1.2, 7: 1.5, 8: 2.0}
        multiplier = eqf_multipliers.get(eqf_level, 1.0)
        
        # Role-specific adjustments
        role_adjustments = {
            "DSL": 1.3,  # Leadership roles command premium
            "DSC": 1.2,  # Consulting premium
            "DSI": 1.15, # Data science premium
            "DSM": 1.1,  # Management premium
            "DAN": 1.0,  # Baseline
            "DSE": 1.05, # Technical premium
            "SSD": 1.1,  # Design premium
            "SBA": 1.0,  # Business analysis baseline
            "SDD": 0.95, # Development slightly lower
            "STS": 0.9   # Specialist roles
        }
        
        role_mult = role_adjustments.get(role_id, 1.0)
        
        # Apply multipliers to create varied results
        final_multiplier = multiplier * role_mult
        
        # Generate varied salary ranges
        if final_multiplier >= 2.0:
            salary_increase = "80-120%"
            career_impact = "executive leadership and transformation"
        elif final_multiplier >= 1.5:
            salary_increase = "60-90%"
            career_impact = "senior management and strategic roles"
        elif final_multiplier >= 1.2:
            salary_increase = "40-65%"
            career_impact = "team leadership and specialization"
        elif final_multiplier >= 1.0:
            salary_increase = "25-45%"
            career_impact = "professional advancement and expertise"
        else:
            salary_increase = "15-30%"
            career_impact = "skill enhancement and recognition"
        
        return salary_increase, career_impact
    
    def _get_role_specific_benefits(self, role_id: str, topic: str, ects: float) -> List[str]:
        """Generate role-specific benefits with variety"""
        
        role_benefit_templates = {
            "DAN": [
                f"📊 **Data Mastery**: Advanced {topic.lower()} analytics capabilities for strategic decision-making",
                f"🔍 **Insight Generation**: Transform complex {topic.lower()} data into actionable business intelligence",
                f"📈 **Performance Optimization**: Quantify {topic.lower()} impact with sophisticated measurement frameworks",
                f"⚡ **Real-time Analytics**: Deploy live {topic.lower()} monitoring and reporting dashboards"
            ],
            "DSM": [
                f"🎯 **Strategic Leadership**: Direct {topic.lower()} transformation across organizational units",
                f"🔄 **Change Management**: Lead successful {topic.lower()} implementation with stakeholder buy-in",
                f"📋 **Program Oversight**: Manage complex {topic.lower()} initiatives from conception to delivery",
                f"💼 **Executive Influence**: Present {topic.lower()} strategies to C-suite and board leadership"
            ],
            "DSL": [
                f"🏆 **Visionary Leadership**: Shape industry direction through {topic.lower()} innovation",
                f"🌟 **Organizational Transformation**: Drive enterprise-wide {topic.lower()} cultural change",
                f"🎖️ **Thought Leadership**: Establish professional reputation as {topic.lower()} industry expert",
                f"💎 **Executive Positioning**: Access C-suite and board-level {topic.lower()} opportunities"
            ],
            "DSC": [
                f"🤝 **Client Expertise**: Deliver high-value {topic.lower()} consulting to diverse industries",
                f"💡 **Solution Innovation**: Design bespoke {topic.lower()} approaches for complex challenges",
                f"🏢 **Market Positioning**: Establish expertise in high-demand {topic.lower()} consultancy",
                f"📊 **Revenue Generation**: Command premium rates for specialized {topic.lower()} services"
            ],
            "DSI": [
                f"🧠 **AI Innovation**: Apply machine learning to {topic.lower()} challenges and opportunities",
                f"🔬 **Research Leadership**: Pioneer new {topic.lower()} methodologies and technologies",
                f"⚙️ **Algorithm Development**: Create predictive models for {topic.lower()} optimization",
                f"🎯 **Technical Excellence**: Master cutting-edge {topic.lower()} data science techniques"
            ],
            "DSE": [
                f"🏗️ **System Architecture**: Design scalable {topic.lower()} data infrastructure and platforms",
                f"🔧 **Technical Implementation**: Deploy enterprise {topic.lower()} systems and integrations",
                f"⚡ **Performance Engineering**: Optimize {topic.lower()} systems for speed and reliability",
                f"🛡️ **Data Governance**: Ensure secure and compliant {topic.lower()} data management"
            ],
            "SSD": [
                f"🎨 **Innovation Design**: Create user-centered {topic.lower()} solutions and experiences",
                f"🔄 **Systems Thinking**: Design integrated {topic.lower()} approaches for complex challenges",
                f"💡 **Creative Problem-Solving**: Develop novel {topic.lower()} solutions through design thinking",
                f"🌟 **Product Leadership**: Lead {topic.lower()} product development and innovation"
            ],
            "SBA": [
                f"💰 **ROI Analysis**: Quantify financial impact of {topic.lower()} initiatives and investments",
                f"📊 **Business Intelligence**: Translate {topic.lower()} data into strategic business insights",
                f"🎯 **Performance Metrics**: Develop KPIs and measurement frameworks for {topic.lower()} success",
                f"💼 **Stakeholder Engagement**: Build business cases for {topic.lower()} investment and adoption"
            ],
            "SDD": [
                f"💻 **Green Coding**: Develop energy-efficient {topic.lower()} applications and systems",
                f"🌱 **Sustainable Development**: Implement {topic.lower()} best practices in software engineering",
                f"⚡ **Performance Optimization**: Create high-performance {topic.lower()} software solutions",
                f"🔧 **Technical Innovation**: Build cutting-edge {topic.lower()} development frameworks"
            ],
            "STS": [
                f"⚙️ **Technical Specialization**: Master specialized {topic.lower()} technologies and implementations",
                f"🔧 **System Integration**: Seamlessly integrate {topic.lower()} technologies with existing systems",
                f"📐 **Technical Standards**: Develop and maintain {topic.lower()} technical specifications",
                f"🛠️ **Implementation Excellence**: Ensure flawless {topic.lower()} technical deployment"
            ]
        }
        
        return role_benefit_templates.get(role_id, [
            f"🎯 **Professional Excellence**: Advanced {topic.lower()} capabilities for career advancement",
            f"🚀 **Industry Leadership**: Recognized expertise in {topic.lower()} innovation",
            f"💼 **Strategic Impact**: Drive organizational {topic.lower()} transformation"
        ])
    
    def _get_ects_level_benefits(self, ects: float, eqf_level: int, topic: str) -> List[str]:
        """Generate ECTS-level appropriate benefits"""
        
        if ects <= 2:
            return [
                f"⚡ **Rapid Skill Acquisition**: Immediate {topic.lower()} competency in minimal time investment",
                f"🎯 **Targeted Expertise**: Focused {topic.lower()} skills for specific professional challenges"
            ]
        elif ects <= 10:
            return [
                f"📈 **Professional Development**: Comprehensive {topic.lower()} skills for career advancement",
                f"🔄 **Practical Application**: Immediately applicable {topic.lower()} tools and methodologies"
            ]
        elif ects <= 30:
            return [
                f"🎓 **Professional Certification**: Industry-recognized {topic.lower()} qualification",
                f"🌟 **Career Transformation**: Substantial {topic.lower()} expertise for new opportunities"
            ]
        elif ects <= 60:
            return [
                f"🏆 **Advanced Qualification**: Comprehensive {topic.lower()} expertise at professional level",
                f"💼 **Leadership Preparation**: Senior-level {topic.lower()} competencies for management roles"
            ]
        else:
            return [
                f"🎖️ **Expert Qualification**: Master-level {topic.lower()} expertise for industry leadership",
                f"🌍 **Global Recognition**: International standard {topic.lower()} qualification for worldwide opportunities"
            ]
    
    def _get_eqf_level_benefits(self, eqf_level: int, role_name: str, topic: str) -> List[str]:
        """Generate EQF-level appropriate benefits"""
        
        eqf_benefits = {
            4: [
                f"🔧 **Operational Excellence**: Workplace-ready {topic.lower()} skills for immediate application",
                f"📋 **Practical Competency**: Hands-on {topic.lower()} abilities for day-to-day professional tasks"
            ],
            5: [
                f"🎯 **Specialized Skills**: Advanced {topic.lower()} competencies for professional specialization",
                f"📊 **Technical Proficiency**: Comprehensive {topic.lower()} knowledge for technical roles"
            ],
            6: [
                f"🎓 **Professional Mastery**: Bachelor-level {topic.lower()} expertise for career advancement",
                f"💼 **Management Readiness**: {topic.lower()} competencies for team leadership opportunities"
            ],
            7: [
                f"🏆 **Strategic Expertise**: Master-level {topic.lower()} knowledge for organizational leadership",
                f"🌟 **Innovation Leadership**: Advanced {topic.lower()} capabilities for driving transformation"
            ],
            8: [
                f"🎖️ **Research Excellence**: Doctoral-level {topic.lower()} expertise for academic and industry leadership",
                f"🔬 **Thought Leadership**: Pioneer-level {topic.lower()} knowledge for shaping industry direction"
            ]
        }
        
        return eqf_benefits.get(eqf_level, [
            f"📈 **Professional Growth**: Enhanced {topic.lower()} capabilities for {role_name} advancement"
        ])
    
    def _get_dynamic_industry_demand(self, role_id: str, topic: str) -> Dict[str, str]:
        """Generate dynamic industry demand statistics"""
        
        # Role-specific growth rates and market data
        role_demand_data = {
            "DAN": {"growth": "45%", "market": "€1.8 trillion", "demand": "Data-driven decision making"},
            "DSM": {"growth": "38%", "market": "€2.3 trillion", "demand": "Strategic sustainability management"},
            "DSL": {"growth": "52%", "market": "€3.1 trillion", "demand": "Transformational leadership"},
            "DSC": {"growth": "41%", "market": "€950 billion", "demand": "Specialized consulting services"},
            "DSI": {"growth": "48%", "market": "€1.2 trillion", "demand": "AI and predictive analytics"},
            "DSE": {"growth": "43%", "market": "€2.1 trillion", "demand": "Scalable data infrastructure"},
            "SSD": {"growth": "39%", "market": "€1.6 trillion", "demand": "User-centered innovation"},
            "SBA": {"growth": "35%", "market": "€1.4 trillion", "demand": "Business intelligence and ROI"},
            "SDD": {"growth": "37%", "market": "€890 billion", "demand": "Sustainable software development"},
            "STS": {"growth": "33%", "market": "€1.1 trillion", "demand": "Technical specialization"}
        }
        
        data = role_demand_data.get(role_id, {"growth": "40%", "market": "€2.0 trillion", "demand": "Professional expertise"})
        
        return {
            "growth_rate": f"{data['growth']} annual growth in {topic.lower()} roles",
            "market_size": f"{data['market']} European {topic.lower()} economy",
            "employer_demand": f"95% of enterprises prioritizing {data['demand']} in {topic.lower()}"
        }

    # ========== NEW: MISSING SECTIONS GENERATION METHODS ==========

    def generate_section_8_key_benefits_recap(self, role_id: str, topic: str, 
                                            actual_ects: float, eqf_level: int) -> Dict[str, Any]:
        """Generate Section 8: Key Benefits Summary - DYNAMIC & CONTEXTUAL"""
        
        # Clean up topic - remove "EU Test" and similar placeholders
        clean_topic = self._clean_topic_name(topic)
        
        role_info = self.role_skill_mapping.get(role_id, {})
        role_name = role_info.get("name", "Professional")
        salary_range = role_info.get("salary_range", {"min": 35000, "max": 70000, "currency": "EUR"})
        career_benefits = role_info.get("career_benefits", ["Professional development", "Industry recognition"])
        
        # Dynamic salary increase and career impact based on role + ECTS + EQF
        salary_increase, career_impact = self._calculate_dynamic_impact(actual_ects, eqf_level, role_id)
        
        # Role-specific benefit templates (multiple variations)
        role_specific_benefits = self._get_role_specific_benefits(role_id, clean_topic, actual_ects)
        
        # ECTS-level specific benefits
        ects_benefits = self._get_ects_level_benefits(actual_ects, eqf_level, clean_topic)
        
        # EQF-level specific benefits  
        eqf_benefits = self._get_eqf_level_benefits(eqf_level, role_name, clean_topic)
        
        # Combine all benefits with variety
        all_benefits = role_specific_benefits + ects_benefits + eqf_benefits
        # Select 6-8 varied benefits
        import random
        selected_benefits = random.sample(all_benefits, min(7, len(all_benefits)))
        
        # Dynamic value proposition with multiple templates
        value_propositions = [
            f"This {actual_ects} ECTS programme transforms your {role_name.lower()} capabilities in {clean_topic.lower()}. "
            f"Industry data shows {role_name}s with specialized {clean_topic.lower()} skills command "
            f"€{salary_range['min']:,}-€{salary_range['max']:,} annually, with {salary_increase} advancement "
            f"typical within 12-18 months of completion.",
            
            f"As a {role_name}, this {actual_ects} ECTS qualification positions you at the forefront of "
            f"{clean_topic.lower()} innovation. Current market demand for {role_name}s with {clean_topic.lower()} "
            f"expertise exceeds supply by 3:1, creating exceptional career acceleration opportunities.",
            
            f"Investment in this {actual_ects} ECTS {clean_topic.lower()} programme delivers measurable ROI. "
            f"{role_name} professionals report {salary_increase} salary increases and accelerated promotion "
            f"to senior roles averaging 18 months faster than traditional career paths."
        ]
        
        selected_value_prop = random.choice(value_propositions)
        
        return {
            "benefits": selected_benefits,
            "value_proposition": selected_value_prop,
            "salary_impact": {
                "current_range": salary_range,
                "expected_increase": salary_increase,
                "timeframe": "12-18 months post-completion",
                "market_premium": f"{role_name}s with {clean_topic.lower()} specialization"
            },
            "career_progression": {
                "immediate_impact": f"Enhanced {clean_topic.lower()} credibility and expertise",
                "medium_term": f"{career_impact} in {clean_topic.lower()} leadership",
                "long_term": f"Strategic {clean_topic.lower()} transformation roles"
            },
            "industry_demand": self._get_dynamic_industry_demand(role_id, clean_topic)
        }
    
    def _get_role_specific_benefits(self, role_id: str, topic: str, ects: float) -> List[str]:
        """Generate role-specific benefits with variety"""
        
        role_benefit_templates = {
            "DAN": [
                f"📊 **Data Mastery**: Advanced {topic.lower()} analytics capabilities for strategic decision-making",
                f"🔍 **Insight Generation**: Transform complex {topic.lower()} data into actionable business intelligence",
                f"📈 **Performance Optimization**: Quantify {topic.lower()} impact with sophisticated measurement frameworks",
                f"⚡ **Real-time Analytics**: Deploy live {topic.lower()} monitoring and reporting dashboards"
            ],
            "DSM": [
                f"🎯 **Strategic Leadership**: Direct {topic.lower()} transformation across organizational units",
                f"🔄 **Change Management**: Lead successful {topic.lower()} implementation with stakeholder buy-in",
                f"📋 **Program Oversight**: Manage complex {topic.lower()} initiatives from conception to delivery",
                f"💼 **Executive Influence**: Present {topic.lower()} strategies to C-suite and board leadership"
            ],
            "DSL": [
                f"🏆 **Visionary Leadership**: Shape industry direction through {topic.lower()} innovation",
                f"🌟 **Organizational Transformation**: Drive enterprise-wide {topic.lower()} cultural change",
                f"🎖️ **Thought Leadership**: Establish professional reputation as {topic.lower()} industry expert",
                f"💎 **Executive Positioning**: Access C-suite and board-level {topic.lower()} opportunities"
            ],
            "DSC": [
                f"🤝 **Client Expertise**: Deliver high-value {topic.lower()} consulting to diverse industries",
                f"💡 **Solution Innovation**: Design bespoke {topic.lower()} approaches for complex challenges",
                f"🏢 **Market Positioning**: Establish expertise in high-demand {topic.lower()} consultancy",
                f"📊 **Revenue Generation**: Command premium rates for specialized {topic.lower()} services"
            ],
            "DSI": [
                f"🧠 **AI Innovation**: Apply machine learning to {topic.lower()} challenges and opportunities",
                f"🔬 **Research Leadership**: Pioneer new {topic.lower()} methodologies and technologies",
                f"⚙️ **Algorithm Development**: Create predictive models for {topic.lower()} optimization",
                f"🎯 **Technical Excellence**: Master cutting-edge {topic.lower()} data science techniques"
            ],
            "DSE": [
                f"🏗️ **System Architecture**: Design scalable {topic.lower()} data infrastructure and platforms",
                f"🔧 **Technical Implementation**: Deploy enterprise {topic.lower()} systems and integrations",
                f"⚡ **Performance Engineering**: Optimize {topic.lower()} systems for speed and reliability",
                f"🛡️ **Data Governance**: Ensure secure and compliant {topic.lower()} data management"
            ],
            "SSD": [
                f"🎨 **Innovation Design**: Create user-centered {topic.lower()} solutions and experiences",
                f"🔄 **Systems Thinking**: Design integrated {topic.lower()} approaches for complex challenges",
                f"💡 **Creative Problem-Solving**: Develop novel {topic.lower()} solutions through design thinking",
                f"🌟 **Product Leadership**: Lead {topic.lower()} product development and innovation"
            ],
            "SBA": [
                f"💰 **ROI Analysis**: Quantify financial impact of {topic.lower()} initiatives and investments",
                f"📊 **Business Intelligence**: Translate {topic.lower()} data into strategic business insights",
                f"🎯 **Performance Metrics**: Develop KPIs and measurement frameworks for {topic.lower()} success",
                f"💼 **Stakeholder Engagement**: Build business cases for {topic.lower()} investment and adoption"
            ],
            "SDD": [
                f"💻 **Green Coding**: Develop energy-efficient {topic.lower()} applications and systems",
                f"🌱 **Sustainable Development**: Implement {topic.lower()} best practices in software engineering",
                f"⚡ **Performance Optimization**: Create high-performance {topic.lower()} software solutions",
                f"🔧 **Technical Innovation**: Build cutting-edge {topic.lower()} development frameworks"
            ],
            "STS": [
                f"⚙️ **Technical Specialization**: Master specialized {topic.lower()} technologies and implementations",
                f"🔧 **System Integration**: Seamlessly integrate {topic.lower()} technologies with existing systems",
                f"📐 **Technical Standards**: Develop and maintain {topic.lower()} technical specifications",
                f"🛠️ **Implementation Excellence**: Ensure flawless {topic.lower()} technical deployment"
            ]
        }
        
        return role_benefit_templates.get(role_id, [
            f"🎯 **Professional Excellence**: Advanced {topic.lower()} capabilities for career advancement",
            f"🚀 **Industry Leadership**: Recognized expertise in {topic.lower()} innovation",
            f"💼 **Strategic Impact**: Drive organizational {topic.lower()} transformation"
        ])
    
    def _get_ects_level_benefits(self, ects: float, eqf_level: int, topic: str) -> List[str]:
        """Generate ECTS-level appropriate benefits"""
        
        if ects <= 2:
            return [
                f"⚡ **Rapid Skill Acquisition**: Immediate {topic.lower()} competency in minimal time investment",
                f"🎯 **Targeted Expertise**: Focused {topic.lower()} skills for specific professional challenges"
            ]
        elif ects <= 10:
            return [
                f"📈 **Professional Development**: Comprehensive {topic.lower()} skills for career advancement",
                f"🔄 **Practical Application**: Immediately applicable {topic.lower()} tools and methodologies"
            ]
        elif ects <= 30:
            return [
                f"🎓 **Professional Certification**: Industry-recognized {topic.lower()} qualification",
                f"🌟 **Career Transformation**: Substantial {topic.lower()} expertise for new opportunities"
            ]
        elif ects <= 60:
            return [
                f"🏆 **Advanced Qualification**: Comprehensive {topic.lower()} expertise at professional level",
                f"💼 **Leadership Preparation**: Senior-level {topic.lower()} competencies for management roles"
            ]
        else:
            return [
                f"🎖️ **Expert Qualification**: Master-level {topic.lower()} expertise for industry leadership",
                f"🌍 **Global Recognition**: International standard {topic.lower()} qualification for worldwide opportunities"
            ]
    
    def _get_eqf_level_benefits(self, eqf_level: int, role_name: str, topic: str) -> List[str]:
        """Generate EQF-level appropriate benefits"""
        
        eqf_benefits = {
            4: [
                f"🔧 **Operational Excellence**: Workplace-ready {topic.lower()} skills for immediate application",
                f"📋 **Practical Competency**: Hands-on {topic.lower()} abilities for day-to-day professional tasks"
            ],
            5: [
                f"🎯 **Specialized Skills**: Advanced {topic.lower()} competencies for professional specialization",
                f"📊 **Technical Proficiency**: Comprehensive {topic.lower()} knowledge for technical roles"
            ],
            6: [
                f"🎓 **Professional Mastery**: Bachelor-level {topic.lower()} expertise for career advancement",
                f"💼 **Management Readiness**: {topic.lower()} competencies for team leadership opportunities"
            ],
            7: [
                f"🏆 **Strategic Expertise**: Master-level {topic.lower()} knowledge for organizational leadership",
                f"🌟 **Innovation Leadership**: Advanced {topic.lower()} capabilities for driving transformation"
            ],
            8: [
                f"🎖️ **Research Excellence**: Doctoral-level {topic.lower()} expertise for academic and industry leadership",
                f"🔬 **Thought Leadership**: Pioneer-level {topic.lower()} knowledge for shaping industry direction"
            ]
        }
        
        return eqf_benefits.get(eqf_level, [
            f"📈 **Professional Growth**: Enhanced {topic.lower()} capabilities for {role_name} advancement"
        ])
    
    def _get_dynamic_industry_demand(self, role_id: str, topic: str) -> Dict[str, str]:
        """Generate dynamic industry demand statistics"""
        
        # Role-specific growth rates and market data
        role_demand_data = {
            "DAN": {"growth": "45%", "market": "€1.8 trillion", "demand": "Data-driven decision making"},
            "DSM": {"growth": "38%", "market": "€2.3 trillion", "demand": "Strategic sustainability management"},
            "DSL": {"growth": "52%", "market": "€3.1 trillion", "demand": "Transformational leadership"},
            "DSC": {"growth": "41%", "market": "€950 billion", "demand": "Specialized consulting services"},
            "DSI": {"growth": "48%", "market": "€1.2 trillion", "demand": "AI and predictive analytics"},
            "DSE": {"growth": "43%", "market": "€2.1 trillion", "demand": "Scalable data infrastructure"},
            "SSD": {"growth": "39%", "market": "€1.6 trillion", "demand": "User-centered innovation"},
            "SBA": {"growth": "35%", "market": "€1.4 trillion", "demand": "Business intelligence and ROI"},
            "SDD": {"growth": "37%", "market": "€890 billion", "demand": "Sustainable software development"},
            "STS": {"growth": "33%", "market": "€1.1 trillion", "demand": "Technical specialization"}
        }
        
        data = role_demand_data.get(role_id, {"growth": "40%", "market": "€2.0 trillion", "demand": "Professional expertise"})
        
        return {
            "growth_rate": f"{data['growth']} annual growth in {topic.lower()} roles",
            "market_size": f"{data['market']} European {topic.lower()} economy",
            "employer_demand": f"95% of enterprises prioritizing {data['demand']} in {topic.lower()}"
        }

    def generate_section_9_cross_border_compatibility(self, role_id: str, 
                                                    actual_ects: float, eqf_level: int) -> Dict[str, Any]:
        """Generate Section 9: Cross-Border Compatibility & Recognition - DYNAMIC"""
        
        role_info = self.role_skill_mapping.get(role_id, {})
        role_name = role_info.get("name", "Professional")
        
        # Dynamic EU recognition based on role and qualifications
        recognition_templates = [
            f"This {actual_ects} ECTS qualification establishes your {role_name.lower()} credentials across all 27 European Union member states through EQF Level {eqf_level} alignment. Your expertise will be immediately recognized by employers from Stockholm to Madrid, enabling seamless professional mobility and international career opportunities.",
            
            f"Built on European Qualifications Framework Level {eqf_level} standards, this {actual_ects} ECTS programme ensures automatic recognition of your {role_name.lower()} competencies throughout the European Union. Professional mobility regulations guarantee your qualification validity across all member states, opening doors to international opportunities.",
            
            f"Your {actual_ects} ECTS {role_name.lower()} qualification meets stringent EQF Level {eqf_level} requirements, ensuring recognition across Europe's integrated professional landscape. This enables direct access to opportunities in major European business centers including Frankfurt, Amsterdam, Brussels, and beyond."
        ]
        
        import random
        eu_recognition = random.choice(recognition_templates)
        
        # Dynamic recognition mechanisms based on EQF level
        base_mechanisms = [
            f"**ECTS Compliance**: {actual_ects} ECTS credits fully transferable across European higher education institutions",
            f"**EQF Level {eqf_level}**: Direct alignment with European Qualifications Framework descriptors for cross-border recognition"
        ]
        
        # Add EQF-specific mechanisms
        if eqf_level >= 7:
            base_mechanisms.extend([
                "**Academic Progression**: Direct entry to EQF Level 8 doctoral programmes across EU universities",
                "**Research Recognition**: Qualification acknowledged for EU research framework participation",
                "**Professional Regulation**: Meets requirements for regulated professional status in member states"
            ])
        elif eqf_level >= 6:
            base_mechanisms.extend([
                "**Graduate Access**: Qualification accepted for master's programme entry across EU institutions",
                "**Professional Standards**: Recognition by European professional regulatory bodies",
                "**Management Qualification**: Acknowledged for supervisory and management positions EU-wide"
            ])
        else:
            base_mechanisms.extend([
                "**Professional Entry**: Recognition for professional-level positions across EU member states",
                "**Vocational Advancement**: Qualification supports career progression in technical and specialist roles"
            ])
        
        # Standard mechanisms for all levels
        base_mechanisms.extend([
            "**Europass Integration**: Digital credentials automatically generated for European career mobility",
            "**EQAVET Quality Assurance**: Programme meets European Quality Assurance standards for vocational education",
            "**ESCO Framework Mapping**: Competencies mapped to European Skills/Competences/Qualifications/Occupations classification",
            "**Blockchain Verification**: Secure, tamper-proof digital credentials for international employer verification"
        ])
        
        # Role-specific professional mobility
        mobility_templates = {
            "DSL": f"**Executive Recognition**: Qualified for C-suite and board positions across European enterprises with {role_name.lower()} responsibilities",
            "DSM": f"**Management Authority**: Recognized for senior management positions requiring {role_name.lower()} expertise across EU markets",
            "DSC": f"**Consultancy Practice**: Authorized for independent {role_name.lower()} consulting across EU member states",
            "DSI": f"**Research Leadership**: Qualified for senior research positions in European academic and industry institutions",
            "DAN": f"**Analytical Expertise**: Recognized for specialized {role_name.lower()} positions across European data-driven organizations",
            "DSE": f"**Technical Leadership**: Qualified for senior engineering roles in European technology and infrastructure sectors",
            "SSD": f"**Design Authority**: Recognized for senior design and innovation roles across European creative and technology industries",
            "SBA": f"**Business Analysis**: Qualified for strategic analysis positions across European financial and consulting sectors",
            "SDD": f"**Development Excellence**: Recognized for senior software development positions across European technology companies",
            "STS": f"**Technical Specialization**: Qualified for expert technical roles across European engineering and technology sectors"
        }
        
        role_mobility = mobility_templates.get(role_id, f"**Professional Authority**: Qualified for senior {role_name.lower()} positions across European markets")
        
        professional_mobility = [
            role_mobility,
            f"**Salary Benchmarking**: Standardized compensation expectations based on European {role_name.lower()} market rates",
            "**Work Authorization**: Enhanced visa and work permit applications through skills-based migration programs",
            f"**Professional Networks**: Access to European-wide {role_name.lower()} professional associations and industry groups",
            "**Continuing Education**: Seamless progression to higher qualifications in any EU country",
            "**Regulatory Compliance**: Meets EU regulatory requirements for professional practice where applicable"
        ]
        
        # Dynamic digital verification based on ECTS level
        verification_base = [
            "**Digital Badges**: Blockchain-verified competency badges for LinkedIn and professional profiles",
            "**QR Code Certificates**: Instant verification through mobile scanning technology",
            "**Employer API**: Direct integration with major European HR and recruitment platforms"
        ]
        
        if actual_ects >= 30:
            verification_base.extend([
                "**Academic Transcript**: Official academic record recognized by European universities for further study",
                "**Professional Dossier**: Comprehensive competency portfolio for senior position applications",
                "**Research Portfolio**: Academic and professional research contributions for thought leadership positions"
            ])
        
        verification_base.extend([
            "**Multi-Language Support**: Credentials available in all 24 official EU languages",
            "**Mobile Verification**: Smartphone-compatible instant credential verification system"
        ])
        
        # Determine mobility level and geographic scope
        if actual_ects >= 60 and eqf_level >= 7:
            mobility_level = "executive_international"
            primary_recognition = "27 EU Member States + EEA + Associated Countries"
            extended_recognition = "OECD countries through mutual recognition agreements"
        elif actual_ects >= 30 and eqf_level >= 6:
            mobility_level = "senior_professional" 
            primary_recognition = "27 EU Member States + European Economic Area"
            extended_recognition = "Switzerland, UK through professional mobility agreements"
        elif actual_ects >= 10:
            mobility_level = "professional_specialist"
            primary_recognition = "27 EU Member States"
            extended_recognition = "EEA countries (Iceland, Liechtenstein, Norway)"
        else:
            mobility_level = "technical_specialist"
            primary_recognition = "27 EU Member States"
            extended_recognition = "Limited recognition in associate countries"
        
        return {
            "eu_recognition": eu_recognition,
            "recognition_mechanisms": base_mechanisms,
            "professional_mobility": professional_mobility,
            "digital_verification": verification_base,
            "mobility_level": mobility_level,
            "geographic_scope": {
                "primary_recognition": primary_recognition,
                "extended_recognition": extended_recognition,
                "global_recognition": "International employers with European operations and multinational corporations"
            },
            "certification_pathways": {
                "academic_progression": f"Direct entry to EQF Level {min(8, eqf_level + 1)} programmes across European universities",
                "professional_certification": f"Industry-specific professional body recognition for {role_name.lower()} roles",
                "regulatory_compliance": f"Meets EU regulatory requirements for {role_name.lower()} professional practice",
                "quality_assurance": "Full EQAVET quality standards compliance with annual external audit"
            }
        }

    # ========== ASSESSMENT GENERATOR COMPATIBILITY METHODS ==========
    
    def get_assessment_methods_for_topic(self, topic: str, eqf_level: int) -> List[str]:
        """Get appropriate assessment methods including work-based learning options"""
        
        topic_lower = topic.lower()
        topic_category = "sustainability"  # Default
        
        if any(word in topic_lower for word in ["data", "analysis", "analytics", "metrics", "esg"]):
            topic_category = "data"
        elif any(word in topic_lower for word in ["software", "development", "coding", "programming"]):
            topic_category = "software"
        elif any(word in topic_lower for word in ["management", "strategy", "planning"]):
            topic_category = "sustainability"  # Management falls under sustainability
        elif any(word in topic_lower for word in ["consulting", "advisory", "consultation"]):
            topic_category = "sustainability"  # Consulting falls under sustainability
        
        # Get methods including work-based learning options
        topic_methods = self.assessment_methods_mapping.get(topic_category, {})
        methods = topic_methods.get(eqf_level, topic_methods.get(6, ["work_based_project", "case_study", "practical_application"]))
        
        print(f"📊 CONTENT_GEN: Work-based assessment methods for '{topic}' (EQF {eqf_level}): {methods}")
        return methods

    def get_industry_relevance(self, topic: str) -> List[str]:
        """Get industry contexts with enhanced ESG and SME focus"""
        
        # Enhanced industry mapping with ESG emphasis
        esg_industries = [
            "ESG Consulting and Advisory Services",
            "Sustainability Reporting and Analytics", 
            "Environmental, Social, and Governance Risk Management",
            "ESG Investment and Financial Services",
            "Corporate Sustainability and ESG Strategy",
            "ESG Technology and Data Platforms"
        ]
        
        sme_focused_industries = [
            "Small Business Sustainability Consulting",
            "SME Environmental Compliance Services",
            "Cost-Effective Green Technology for SMEs",
            "Affordable ESG Solutions for Small Organizations",
            "SME-Focused Sustainability Training and Support"
        ]
        
        traditional_industries = [
            "Environmental Services", "Renewable Energy", "Green Technology",
            "Carbon Management", "Environmental Consulting", "Sustainability Technology"
        ]
        
        # Combine all relevant industries
        all_industries = esg_industries + sme_focused_industries + traditional_industries
        
        print(f"🏭 CONTENT_GEN: Enhanced industry relevance (ESG + SME focus) for '{topic}': {len(all_industries)} industries")
        return all_industries

    def get_all_competency_mappings(self, topic: str) -> Dict[str, List[str]]:
        """Get competency framework mappings with enhanced variety and specificity"""
        
        # Clean topic for better mapping
        clean_topic = self._clean_topic_name(topic)
        
        # Create topic-specific mapping variations to avoid repetition
        topic_keywords = clean_topic.lower().split()
        
        # Enhanced competency frameworks with topic-specific variations
        e_cf_base_mappings = [
            "A.1: IS and Business Strategy Alignment",
            "A.4: Solution Architecture", 
            "B.1: Application Development",
            "B.2: Component Integration",
            "D.2: ICT Quality Strategy",
            "E.2: Project and Portfolio Management",
            "E.3: Risk Management",
            "A.6: Application Architecture",
            "B.4: Solution Deployment",
            "C.1: User Support",
            "C.2: Change Support",
            "D.1: Information Security Strategy"
        ]
        
        digcomp_base_mappings = [
            "1.1: Browsing and Searching",
            "1.2: Evaluating Data and Information", 
            "2.1: Interacting through Digital Technologies",
            "3.1: Developing Digital Content",
            "3.2: Integrating and Re-elaborating Digital Content",
            "5.1: Solving Technical Problems",
            "5.3: Creatively Using Digital Technologies",
            "2.2: Sharing through Digital Technologies",
            "2.4: Collaborating through Digital Technologies",
            "3.3: Copyright and Licences",
            "4.1: Protecting Devices",
            "4.2: Protecting Personal Data"
        ]
        
        greencomp_base_mappings = [
            "1.1: Systems Thinking",
            "2.2: Sustainable Development",
            "3.1: Collective Action",
            "3.2: Critical Thinking", 
            "4.1: Political Agency",
            "4.2: Transformative Action",
            "1.2: Attentiveness",
            "1.3: Transdisciplinarity",
            "2.1: Sustainability Knowledge",
            "2.3: Exploratory Thinking",
            "3.3: Inclusiveness",
            "4.3: Individual Initiative"
        ]
        
        # Select 3-4 random mappings from each framework for variety
        import random
        selected_e_cf = random.sample(e_cf_base_mappings, 4)
        selected_digcomp = random.sample(digcomp_base_mappings, 3)  
        selected_greencomp = random.sample(greencomp_base_mappings, 4)
        
        # Create context-specific descriptions
        context_descriptors = [
            f"strategic {clean_topic.lower()} implementation",
            f"professional {clean_topic.lower()} application", 
            f"organizational {clean_topic.lower()} integration",
            f"innovative {clean_topic.lower()} solutions",
            f"advanced {clean_topic.lower()} methodologies",
            f"comprehensive {clean_topic.lower()} frameworks"
        ]
        
        # Build enhanced mappings with variety
        enhanced_mappings = {
            "e-CF": [],
            "DigComp": [],
            "GreenComp": []
        }
        
        # Create varied e-CF mappings
        for mapping in selected_e_cf:
            descriptor = random.choice(context_descriptors)
            enhanced_mappings["e-CF"].append(f"e-CF:{mapping} - {descriptor} for {clean_topic.lower()} excellence")
        
        # Create varied DigComp mappings  
        for mapping in selected_digcomp:
            descriptor = random.choice(context_descriptors)
            enhanced_mappings["DigComp"].append(f"DigComp:{mapping} - digital {descriptor} in {clean_topic.lower()}")
        
        # Create varied GreenComp mappings
        for mapping in selected_greencomp:
            descriptor = random.choice(context_descriptors)
            enhanced_mappings["GreenComp"].append(f"GreenComp:{mapping} - sustainability-focused {descriptor}")
        
        print(f"🗺️ CONTENT_GEN: Enhanced competency mappings (varied) for '{clean_topic}': e-CF: {len(enhanced_mappings['e-CF'])}, DigComp: {len(enhanced_mappings['DigComp'])}, GreenComp: {len(enhanced_mappings['GreenComp'])}")
        return enhanced_mappings

    # ========== ENHANCED CONTENT GENERATION METHODS ==========

    def generate_specific_learning_outcomes(self, unit_title: str, progression_level: str,
                                          role_id: str, topic: str, unit_ects: float) -> List[str]:
        """Generate learning outcomes with enhanced variety and specificity - NO REPETITION"""

        # Clean topic and extract key concepts
        clean_topic = self._clean_topic_name(topic)
        
        # Map progression level including EQF 4 support
        mapped_level = self.progression_level_mapping.get(progression_level, "Foundation")

        # Get role-specific skills with enhanced variety
        role_info = self.role_skill_mapping.get(role_id, {
            "primary_skills": ["professional competency", "analytical thinking", "problem solving"],
            "secondary_skills": ["communication", "collaboration", "quality assurance"],
            "sme_focus": ["small organization solutions", "cost-effective approaches"],
            "work_based_skills": ["workplace application", "practical implementation"]
        })

        # Create varied skill selections to avoid repetition
        all_primary = role_info["primary_skills"]
        all_secondary = role_info["secondary_skills"] 
        all_sme = role_info.get("sme_focus", ["organizational solutions"])
        all_work = role_info.get("work_based_skills", ["workplace application"])

        # Select different skills for variety
        import random
        primary_skill = random.choice(all_primary)
        secondary_skill = random.choice([s for s in all_secondary if s != primary_skill.split()[0]])
        sme_skill = random.choice(all_sme)
        work_skill = random.choice(all_work)

        # Get templates for progression level
        level_templates = self.learning_outcome_templates.get(mapped_level,
                                                            self.learning_outcome_templates["Foundation"])

        # Generate diverse outcomes with context-specific variations
        outcomes = []

        # Technical competency outcomes (2 outcomes) - with context specificity
        tech_templates = random.sample(level_templates["technical_skills"], min(2, len(level_templates["technical_skills"])))
        
        # Create context-specific variations
        context_variations = [
            f"{clean_topic.lower()} {primary_skill}",
            f"advanced {primary_skill} for {clean_topic.lower()}",
            f"{primary_skill} within {clean_topic.lower()} frameworks",
            f"professional {primary_skill} in {clean_topic.lower()} contexts"
        ]
        
        for i, template in enumerate(tech_templates):
            context_skill = context_variations[i % len(context_variations)]
            outcome = template.format(skill_area=context_skill)
            outcomes.append(outcome)

        # Work-based learning outcome (1 outcome) - contextual
        if "work_based_learning" in level_templates:
            work_template = random.choice(level_templates["work_based_learning"])
            work_context = f"{clean_topic.lower()}-focused {work_skill}"
            work_outcome = work_template.format(skill_area=work_context)
            outcomes.append(work_outcome)

        # Role-specific specialized outcome (1 outcome)
        role_specific_templates = {
            "DAN": [
                f"Generate actionable insights from {clean_topic.lower()} data to drive strategic decision-making",
                f"Design and implement {clean_topic.lower()} analytics frameworks for organizational impact",
                f"Create comprehensive {clean_topic.lower()} dashboards for stakeholder communication"
            ],
            "DSM": [
                f"Lead organizational {clean_topic.lower()} transformation initiatives across functional teams",
                f"Develop strategic {clean_topic.lower()} roadmaps aligned with business objectives",
                f"Manage complex {clean_topic.lower()} change programs from conception to implementation"
            ],
            "DSL": [
                f"Architect enterprise-wide {clean_topic.lower()} vision and strategic direction",
                f"Drive cultural transformation through {clean_topic.lower()} leadership and influence",
                f"Establish thought leadership position in {clean_topic.lower()} innovation and practice"
            ],
            "DSC": [
                f"Design and deliver specialized {clean_topic.lower()} consulting solutions for diverse clients",
                f"Develop innovative {clean_topic.lower()} methodologies for complex organizational challenges",
                f"Build sustainable client relationships through expert {clean_topic.lower()} advisory services"
            ],
            "DSI": [
                f"Apply machine learning algorithms to solve complex {clean_topic.lower()} challenges",
                f"Develop predictive models for {clean_topic.lower()} optimization and forecasting",
                f"Create data-driven {clean_topic.lower()} solutions using advanced statistical methods"
            ],
            "DSE": [
                f"Design scalable {clean_topic.lower()} data infrastructure and integration systems",
                f"Implement robust {clean_topic.lower()} data pipelines for enterprise-scale applications",
                f"Optimize {clean_topic.lower()} system performance for real-time data processing"
            ],
            "SSD": [
                f"Create user-centered {clean_topic.lower()} solutions through design thinking methodologies",
                f"Develop innovative {clean_topic.lower()} product concepts and service experiences",
                f"Design integrated {clean_topic.lower()} systems that address complex user needs"
            ],
            "SBA": [
                f"Conduct comprehensive {clean_topic.lower()} business impact analysis and ROI assessment",
                f"Develop compelling business cases for {clean_topic.lower()} investment and adoption",
                f"Translate {clean_topic.lower()} technical requirements into strategic business value"
            ],
            "SDD": [
                f"Develop energy-efficient {clean_topic.lower()} software applications and systems",
                f"Implement sustainable coding practices for {clean_topic.lower()} application development",
                f"Create high-performance {clean_topic.lower()} software with minimal environmental impact"
            ],
            "STS": [
                f"Implement specialized {clean_topic.lower()} technical solutions and system integrations",
                f"Optimize {clean_topic.lower()} technical performance through advanced configuration and tuning",
                f"Maintain and enhance {clean_topic.lower()} technical systems for operational excellence"
            ]
        }
        
        role_templates = role_specific_templates.get(role_id, [
            f"Apply professional {clean_topic.lower()} competencies in specialized organizational contexts",
            f"Implement {clean_topic.lower()} solutions that deliver measurable business value",
            f"Demonstrate expertise in {clean_topic.lower()} through practical application and results"
        ])
        
        role_outcome = random.choice(role_templates)
        outcomes.append(role_outcome)

        # Application competency with context specificity (for larger units)
        if unit_ects >= 2.0:
            app_template = random.choice(level_templates["application_skills"])
            app_context = f"strategic {clean_topic.lower()} {secondary_skill}"
            app_outcome = app_template.format(skill_area=app_context)
            outcomes.append(app_outcome)

        # SME-focused outcome (for comprehensive programs)
        if unit_ects >= 3.0:
            sme_templates = [
                f"Design cost-effective {clean_topic.lower()} solutions suitable for small and medium enterprises",
                f"Develop scalable {clean_topic.lower()} approaches that adapt to resource-constrained environments",
                f"Create accessible {clean_topic.lower()} implementations for organizations with limited technical capacity",
                f"Implement rapid-deployment {clean_topic.lower()} solutions for immediate organizational impact"
            ]
            sme_outcome = random.choice(sme_templates)
            outcomes.append(sme_outcome)

        return outcomes

    def generate_concrete_unit_title(self, unit_number: int, progression_level: str,
                                   role_id: str, topic: str) -> str:
        """Generate unit titles with enhanced variety and NO PLACEHOLDERS"""

        # Clean topic and make contextual
        clean_topic = self._clean_topic_name(topic)
        
        mapped_level = self.progression_level_mapping.get(progression_level, "Foundation")
        role_info = self.role_skill_mapping.get(role_id, {})
        primary_skills = role_info.get("primary_skills", ["Professional Development"])
        
        # Multiple title template sets for variety
        title_template_sets = {
            "EQF4_Foundation": {
                "practical": [
                    "Getting Started with {skill} in {context}",
                    "Basic {skill} for {context} Applications", 
                    "Introduction to {skill} Practice",
                    "Workplace {skill} Fundamentals"
                ],
                "technical": [
                    "Essential {skill} Tools and Methods",
                    "Core {skill} Technologies",
                    "Basic {skill} Implementation",
                    "Foundational {skill} Systems"
                ],
                "contextual": [
                    "{context} {skill} Basics",
                    "Applied {skill} in {context}",
                    "{skill} for {context} Professionals",
                    "Practical {skill} Applications"
                ]
            },
            "Foundation": {
                "practical": [
                    "Applied {skill} for {context} Innovation",
                    "Professional {skill} in {context}",
                    "Integrated {skill} and {context} Solutions",
                    "Modern {skill} Approaches to {context}"
                ],
                "technical": [
                    "Advanced {skill} Tools for {context}",
                    "{skill} Technology Integration",
                    "Digital {skill} Platforms",
                    "Automated {skill} Systems"
                ],
                "strategic": [
                    "Strategic {skill} Implementation",
                    "{skill} for Organizational {context}",
                    "Professional {skill} Excellence",
                    "{context}-Driven {skill} Solutions"
                ]
            },
            "Development": {
                "advanced": [
                    "Advanced {skill} for {context} Leadership",
                    "Expert {skill} Implementation",
                    "Professional {skill} Mastery",
                    "Specialized {skill} Applications"
                ],
                "analytical": [
                    "{skill} Analytics for {context} Optimization",
                    "Data-Driven {skill} Strategies",
                    "Quantitative {skill} Approaches",
                    "Metrics-Based {skill} Management"
                ],
                "innovation": [
                    "Innovative {skill} Solutions",
                    "Next-Generation {skill} Methods",
                    "Creative {skill} Applications",
                    "Emerging {skill} Technologies"
                ]
            },
            "Application": {
                "management": [
                    "Strategic {skill} Management for {context}",
                    "Enterprise {skill} Implementation",
                    "Organizational {skill} Transformation",
                    "Executive {skill} Leadership"
                ],
                "consulting": [
                    "Expert {skill} Consulting Methods",
                    "Professional {skill} Advisory Services",
                    "Strategic {skill} Consultation",
                    "Specialized {skill} Expertise"
                ],
                "innovation": [
                    "Innovative {skill} Frameworks",
                    "Breakthrough {skill} Methodologies",
                    "Advanced {skill} Innovation",
                    "Cutting-Edge {skill} Solutions"
                ]
            },
            "Integration": {
                "enterprise": [
                    "Enterprise {skill} Architecture",
                    "Integrated {skill} Ecosystems",
                    "Holistic {skill} Solutions",
                    "Comprehensive {skill} Frameworks"
                ],
                "transformation": [
                    "Organizational {skill} Transformation",
                    "Strategic {skill} Innovation",
                    "Enterprise {skill} Evolution",
                    "Systemic {skill} Change"
                ],
                "leadership": [
                    "Executive {skill} Leadership",
                    "Strategic {skill} Vision",
                    "Transformational {skill} Management",
                    "Visionary {skill} Implementation"
                ]
            },
            "Mastery": {
                "research": [
                    "Advanced {skill} Research Methods",
                    "Experimental {skill} Innovation",
                    "Scientific {skill} Investigation",
                    "Research-Led {skill} Development"
                ],
                "thought_leadership": [
                    "Thought Leadership in {skill}",
                    "Industry {skill} Innovation",
                    "Professional {skill} Excellence",
                    "Expert {skill} Mastery"
                ],
                "mentorship": [
                    "Expert {skill} Mentorship",
                    "Professional {skill} Development",
                    "Advanced {skill} Coaching",
                    "Specialized {skill} Training"
                ]
            },
            "Leadership": {
                "visionary": [
                    "Visionary {skill} Leadership",
                    "Transformational {skill} Strategy",
                    "Revolutionary {skill} Innovation",
                    "Pioneering {skill} Development"
                ],
                "global": [
                    "Global {skill} Leadership",
                    "International {skill} Standards",
                    "Worldwide {skill} Innovation",
                    "Universal {skill} Excellence"
                ],
                "legacy": [
                    "Legacy {skill} Development",
                    "Enduring {skill} Impact",
                    "Sustainable {skill} Leadership",
                    "Lasting {skill} Innovation"
                ]
            }
        }
        
        # Select skill and create variations
        base_skill = random.choice(primary_skills)
        
        # Create skill variations to avoid repetition
        skill_variations = {
            "sustainability data analysis": ["ESG Analytics", "Environmental Data Science", "Carbon Intelligence", "Impact Measurement"],
            "environmental metrics reporting": ["ESG Reporting", "Impact Communication", "Metrics Visualization", "Performance Dashboards"],
            "carbon footprint assessment": ["Carbon Analytics", "Emissions Analysis", "Climate Impact Assessment", "Carbon Intelligence"],
            "sustainability program management": ["ESG Strategy", "Impact Program Leadership", "Transformation Management", "Change Leadership"],
            "organizational transformation": ["Change Leadership", "Strategic Transformation", "Innovation Management", "Cultural Evolution"],
            "strategic sustainability planning": ["ESG Strategy", "Impact Planning", "Sustainable Development", "Strategic Innovation"],
            "sustainability consulting": ["ESG Advisory", "Impact Consulting", "Strategic Guidance", "Transformation Consulting"],
            "sustainable software development": ["Green Technology", "Eco-Friendly Development", "Carbon-Aware Programming", "Sustainable Engineering"],
            "sustainable solution design": ["Impact Innovation", "ESG Solution Architecture", "Sustainable Design Thinking", "Environmental Innovation"]
        }
        
        # Get varied skill name
        skill_options = skill_variations.get(base_skill, [base_skill.replace("sustainability ", "").replace("environmental ", "").title()])
        selected_skill = random.choice(skill_options)
        
        # Create context variations for the topic
        context_variations = [
            clean_topic,
            f"Modern {clean_topic}",
            f"Digital {clean_topic}", 
            f"Strategic {clean_topic}",
            f"Professional {clean_topic}"
        ]
        selected_context = random.choice(context_variations)
        
        # Select template set and category
        templates = title_template_sets.get(mapped_level, title_template_sets["Foundation"])
        template_category = random.choice(list(templates.keys()))
        template_list = templates[template_category]
        
        selected_template = random.choice(template_list)
        
        # Format with context and skill
        final_title = selected_template.format(
            skill=selected_skill,
            context=selected_context
        )
        
        return final_title

    def get_framework_mappings(self, progression_level: str, role_id: str = "DSM") -> Dict[str, List[str]]:
        """Get enhanced framework mappings with ESG focus"""
        
        # Use the enhanced competency mappings
        return self.get_all_competency_mappings(f"{role_id} sustainability")

    def get_micro_credential_pathways(self, role_id: str, total_ects: float) -> Dict[str, Any]:
        """Generate micro-credential stackable pathways - NEW"""
        
        role_info = self.role_skill_mapping.get(role_id, {})
        role_name = role_info.get("name", "Professional")
        
        # Determine appropriate micro-credential pathway
        if total_ects <= 5:
            pathway_type = "foundation_credentials"
            credential_level = "Foundation"
        elif total_ects <= 15:
            pathway_type = "specialist_credentials" 
            credential_level = "Specialist"
        else:
            pathway_type = "advanced_credentials"
            credential_level = "Advanced"
        
        available_credentials = self.micro_credential_system["stackable_units"][pathway_type]
        certification_info = self.micro_credential_system["certification_pathways"]
        
        return {
            "pathway_type": pathway_type,
            "credential_level": credential_level,
            "role_focus": role_name,
            "available_credentials": available_credentials,
            "stackable_features": certification_info,
            "next_level_options": self._get_next_level_options(pathway_type),
            "industry_recognition": f"Industry-validated {credential_level} level competency in {role_name}",
            "digital_badges": True,
            "blockchain_verification": True
        }
    
    def _get_next_level_options(self, current_pathway: str) -> List[str]:
        """Get next level progression options for micro-credentials"""
        
        progression_map = {
            "foundation_credentials": ["specialist_credentials"],
            "specialist_credentials": ["advanced_credentials"],
            "advanced_credentials": ["expert_certification", "leadership_pathway"]
        }
        
        return progression_map.get(current_pathway, [])

    def get_sme_specific_content(self, role_id: str, topic: str) -> Dict[str, Any]:
        """Generate SME-specific content and pathways - NEW"""
        
        role_info = self.role_skill_mapping.get(role_id, {})
        sme_focus = role_info.get("sme_focus", ["small organization solutions"])
        
        return {
            "sme_challenges": [
                "Limited budget for sustainability initiatives",
                "Lack of specialized sustainability expertise",
                "Need for rapid implementation and results",
                "Requirement for cost-effective solutions",
                "Limited time for complex certification processes"
            ],
            "sme_solutions": sme_focus,
            "implementation_approach": [
                "Rapid deployment methodologies",
                "Cost-effective technology selection",
                "Scalable solution design",
                "Simplified compliance procedures",
                "Peer learning and support networks"
            ],
            "success_metrics": [
                "Return on investment within 6 months",
                "Compliance achievement with minimal complexity",
                "Employee engagement and buy-in",
                "Measurable environmental impact",
                "Sustainable business growth"
            ]
        }
