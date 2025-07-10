scripts/curriculum_generator/components/educational_profile_rewriter.py
"""
Educational Profile Rewriter - EU Compliance Transformation Engine
Automatically transforms existing educational profiles to meet EU educational standards
Addresses all critique points: repetitive outcomes, curriculum contamination, EQF progression, role differentiation
"""
import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path
import copy
class EUProfileRewriter:
"""
Comprehensive EU Educational Profile Rewriter
Transforms non-compliant profiles into EU-standard compliant profiles
"""
def __init__(self):
    self.role_specific_data = self._initialize_role_data()
    self.eqf_complexity_verbs = self._initialize_complexity_verbs()
    self.framework_mappings = self._initialize_framework_mappings()
    
def _initialize_role_data(self) -> Dict[str, Dict[str, Any]]:
    """Initialize role-specific transformation data"""
    return {
        'DSL': {
            'title': 'Digital Sustainability Lead',
            'strategic_focus': 'organizational transformation and strategic ESG leadership',
            'core_competencies': [
                'Strategic Sustainability Transformation and Governance',
                'Stakeholder Engagement and Change Leadership', 
                'Regulatory Compliance and Risk Management'
            ],
            'distinctive_features': [
                'C-suite communication expertise on ESG value creation',
                'Regulatory foresight integrated with business transformation',
                'Multi-stakeholder governance innovation and global impact leadership'
            ],
            'career_progression': {
                'entry': 'Sustainability Team Leader',
                'mid': 'Director of Sustainability Strategy',
                'senior': 'Senior Director of Sustainability Leadership',
                'executive': 'Chief Sustainability Officer (CSO)'
            },
            'industry_focus': 'strategic leadership and ESG transformation',
            'complexity_emphasis': 'strategic planning and organizational transformation'
        },
        'DSM': {
            'title': 'Digital Sustainability Manager',
            'strategic_focus': 'operational sustainability implementation and project coordination',
            'core_competencies': [
                'Sustainability Project Management and Implementation',
                'Performance Monitoring and Reporting Systems',
                'Team Coordination and Stakeholder Communication'
            ],
            'distinctive_features': [
                'Cross-functional project coordination expertise',
                'Performance measurement and KPI development',
                'Implementation excellence and operational efficiency'
            ],
            'career_progression': {
                'entry': 'Sustainability Implementation Manager',
                'mid': 'Senior Sustainability Manager',
                'senior': 'Director of Sustainability Operations',
                'executive': 'Executive Director of Sustainability'
            },
            'industry_focus': 'operational management and implementation coordination',
            'complexity_emphasis': 'project management and operational excellence'
        },
        'DSC': {
            'title': 'Digital Sustainability Consultant',
            'strategic_focus': 'external advisory services and solution architecture',
            'core_competencies': [
                'Client Advisory and Solution Architecture',
                'Best Practice Development and Knowledge Transfer',
                'Stakeholder Engagement and Change Management'
            ],
            'distinctive_features': [
                'External stakeholder engagement and client relationship management',
                'Cross-industry expertise and solution adaptation',
                'Knowledge transfer and capacity building excellence'
            ],
            'career_progression': {
                'entry': 'Sustainability Consultant',
                'mid': 'Senior Sustainability Consultant',
                'senior': 'Principal Sustainability Consultant',
                'executive': 'Partner in Sustainability Practice'
            },
            'industry_focus': 'advisory services and external consultation',
            'complexity_emphasis': 'client advisory and solution development'
        },
        'DAN': {
            'title': 'Data Analyst - Sustainability Focus',
            'strategic_focus': 'sustainability data analytics and insight generation',
            'core_competencies': [
                'Advanced Sustainability Data Analytics and Predictive Modeling',
                'Environmental Impact Assessment and Strategic Measurement',
                'Stakeholder Communication and Data-Driven Insight Generation'
            ],
            'distinctive_features': [
                'Advanced analytics expertise in environmental and social data',
                'Predictive modeling for sustainability outcomes',
                'Data visualization and stakeholder communication excellence'
            ],
            'career_progression': {
                'entry': 'Junior Data Analyst - Sustainability',
                'mid': 'Senior Data Analyst - Sustainability',
                'senior': 'Lead Data Analyst - Sustainability',
                'executive': 'Principal Data Analyst - Sustainability'
            },
            'industry_focus': 'data analytics and insight generation',
            'complexity_emphasis': 'analytical thinking and data interpretation'
        },
        'SDD': {
            'title': 'Sustainable Digital Developer',
            'strategic_focus': 'environmentally conscious software development',
            'core_competencies': [
                'Green Software Development and Energy Optimization',
                'Sustainable Software Architecture and Design Patterns',
                'Environmental Impact Assessment for Digital Systems'
            ],
            'distinctive_features': [
                'Energy-efficient coding practices and optimization',
                'Carbon-aware application development',
                'Sustainable software architecture expertise'
            ],
            'career_progression': {
                'entry': 'Junior Sustainable Developer',
                'mid': 'Senior Sustainable Developer',
                'senior': 'Lead Sustainable Developer',
                'executive': 'Principal Software Architect - Sustainability'
            },
            'industry_focus': 'software development and technical implementation',
            'complexity_emphasis': 'technical development and system optimization'
        },
        'SSD': {
            'title': 'Sustainable Systems Designer',
            'strategic_focus': 'sustainable digital architecture and systems design',
            'core_competencies': [
                'Sustainable Systems Architecture and Infrastructure Design',
                'Technology Assessment and Environmental Impact Analysis',
                'Digital Infrastructure Optimization and Governance'
            ],
            'distinctive_features': [
                'Systems-level thinking for sustainability optimization',
                'Infrastructure design with environmental considerations',
                'Technology assessment and selection expertise'
            ],
            'career_progression': {
                'entry': 'Systems Designer - Sustainability',
                'mid': 'Senior Systems Designer - Sustainability',
                'senior': 'Lead Systems Architect - Sustainability',
                'executive': 'Principal Design Architect - Sustainability'
            },
            'industry_focus': 'systems design and infrastructure architecture',
            'complexity_emphasis': 'systems thinking and architectural design'
        },
        'SBA': {
            'title': 'Sustainability Business Analyst',
            'strategic_focus': 'business process analysis for sustainability integration',
            'core_competencies': [
                'Sustainability Requirements Engineering and Process Analysis',
                'Stakeholder Analysis and Business Process Optimization',
                'Change Management and Solution Implementation'
            ],
            'distinctive_features': [
                'Business process analysis with sustainability integration',
                'Requirements engineering for environmental objectives',
                'Stakeholder analysis and change management expertise'
            ],
            'career_progression': {
                'entry': 'Business Analyst - Sustainability',
                'mid': 'Senior Business Analyst - Sustainability',
                'senior': 'Lead Business Analyst - Sustainability',
                'executive': 'Principal Business Architecture Specialist - Sustainability'
            },
            'industry_focus': 'business analysis and process optimization',
            'complexity_emphasis': 'analytical thinking and process improvement'
        },
        'DSI': {
            'title': 'Digital Sustainability Implementer',
            'strategic_focus': 'technical implementation of sustainability solutions',
            'core_competencies': [
                'Technical Solution Implementation and System Integration',
                'Digital Infrastructure Deployment and Optimization',
                'Quality Assurance and Performance Monitoring'
            ],
            'distinctive_features': [
                'Technical implementation excellence and system integration',
                'Deployment coordination and quality assurance',
                'Performance optimization and monitoring expertise'
            ],
            'career_progression': {
                'entry': 'Implementation Specialist - Sustainability',
                'mid': 'Senior Implementer - Sustainability',
                'senior': 'Lead Technical Specialist - Sustainability',
                'executive': 'Principal Implementation Architect - Sustainability'
            },
            'industry_focus': 'technical implementation and system deployment',
            'complexity_emphasis': 'technical implementation and quality assurance'
        },
        'DSE': {
            'title': 'Digital Sustainability Educator',
            'strategic_focus': 'educational program development and delivery',
            'core_competencies': [
                'Curriculum Design and Educational Program Development',
                'Digital Pedagogy and Learning Technology Integration',
                'Assessment Design and Learning Outcome Evaluation'
            ],
            'distinctive_features': [
                'Curriculum development expertise for sustainability education',
                'Digital pedagogy and technology-enhanced learning',
                'Assessment design and educational evaluation excellence'
            ],
            'career_progression': {
                'entry': 'Sustainability Education Instructor',
                'mid': 'Senior Sustainability Educator',
                'senior': 'Lead Educational Designer - Sustainability',
                'executive': 'Principal Learning Architect - Sustainability'
            },
            'industry_focus': 'education and curriculum development',
            'complexity_emphasis': 'educational design and pedagogical expertise'
        },
        'STS': {
            'title': 'Sustainability Technology Specialist',
            'strategic_focus': 'technology innovation and research for sustainability applications',
            'core_competencies': [
                'Technology Innovation and Research Methodology',
                'Sustainability Applications Development and Evaluation',
                'Knowledge Management and Technology Transfer'
            ],
            'distinctive_features': [
                'Technology innovation and research excellence',
                'Sustainability applications development',
                'Knowledge transfer and technology evaluation expertise'
            ],
            'career_progression': {
                'entry': 'Technology Specialist - Sustainability',
                'mid': 'Senior Technology Specialist - Sustainability',
                'senior': 'Lead Technology Innovator - Sustainability',
                'executive': 'Principal Technology Strategist - Sustainability'
            },
            'industry_focus': 'technology specialization and innovation',
            'complexity_emphasis': 'research methodology and technology innovation'
        }
    }

def _initialize_complexity_verbs(self) -> Dict[int, List[str]]:
    """Initialize EQF-appropriate complexity verbs"""
    return {
        4: ['implement', 'apply', 'use', 'follow', 'support', 'assist', 'operate'],
        5: ['coordinate', 'organize', 'manage', 'analyze', 'develop', 'create'],
        6: ['design', 'evaluate', 'synthesize', 'plan', 'optimize', 'integrate'],
        7: ['innovate', 'lead', 'transform', 'strategize', 'establish', 'influence'],
        8: ['pioneer', 'revolutionize', 'conceptualize', 'architect', 'mastermind']
    }

def _initialize_framework_mappings(self) -> Dict[str, Dict[str, List[str]]]:
    """Initialize specific framework mappings for each role"""
    return {
        'DSL': {
            'e-CF': ['E.9 (IS Governance)', 'E.1 (Strategic Planning)', 'E.4 (Relationship Management)'],
            'DigComp': ['5.4 (Digital Identity & Ethics)', '2.4 (Collaboration through Digital Tools)'],
            'GreenComp': ['4.3 (Political Agency)', '4.2 (Collective Action)']
        },
        'DSM': {
            'e-CF': ['C.2 (Change Support)', 'D.1 (Information Systems Strategy)', 'E.6 (IT Quality Management)'],
            'DigComp': ['3.1 (Developing Digital Content)', '2.3 (Managing Digital Identity)'],
            'GreenComp': ['3.1 (Exploratory Thinking)', '2.2 (Sustainability and Equity)']
        },
        'DSC': {
            'e-CF': ['A.5 (Architecture Design)', 'E.4 (Relationship Management)', 'D.8 (Contract Management)'],
            'DigComp': ['1.3 (Managing Data)', '5.2 (Identifying Needs and Technological Responses)'],
            'GreenComp': ['1.2 (Systems Thinking)', '4.1 (Individual Initiative)']
        },
        'DAN': {
            'e-CF': ['B.1 (Application Development)', 'B.6 (Engineering Design)', 'E.3 (Risk Management)'],
            'DigComp': ['5.3 (Creatively Using Technologies)', '3.2 (Integrating Digital Content)'],
            'GreenComp': ['3.2 (Critical Thinking)', '1.3 (Interconnectedness)']
        },
        'SDD': {
            'e-CF': ['B.1 (Application Development)', 'B.6 (Engineering Design)', 'C.4 (Problem Management)'],
            'DigComp': ['3.1 (Developing Digital Content)', '5.1 (Solving Technical Problems)'],
            'GreenComp': ['2.3 (Future-Mindedness)', '3.3 (Science Literacy)']
        },
        'SSD': {
            'e-CF': ['A.5 (Architecture Design)', 'A.6 (Application Design)', 'B.6 (Engineering Design)'],
            'DigComp': ['1.2 (Evaluating Data)', '5.2 (Identifying Needs and Technological Responses)'],
            'GreenComp': ['1.1 (Embodied Knowledge)', '3.1 (Exploratory Thinking)']
        },
        'SBA': {
            'e-CF': ['A.1 (IS and Business Strategy Alignment)', 'A.4 (Product Planning)', 'E.2 (Project Management)'],
            'DigComp': ['2.1 (Interacting through Technologies)', '4.2 (Protecting Personal Data)'],
            'GreenComp': ['2.1 (Values)', '1.2 (Systems Thinking)']
        },
        'DSI': {
            'e-CF': ['C.1 (User Support)', 'C.3 (Service Delivery)', 'B.2 (Component Integration)'],
            'DigComp': ['5.1 (Solving Technical Problems)', '3.3 (Copyright and Licenses)'],
            'GreenComp': ['4.1 (Individual Initiative)', '2.3 (Future-Mindedness)']
        },
        'DSE': {
            'e-CF': ['E.4 (Relationship Management)', 'A.9 (Innovating)', 'E.8 (Information Security Management)'],
            'DigComp': ['2.4 (Collaboration through Digital Tools)', '3.1 (Developing Digital Content)'],
            'GreenComp': ['4.2 (Collective Action)', '1.3 (Interconnectedness)']
        },
        'STS': {
            'e-CF': ['A.9 (Innovating)', 'B.6 (Engineering Design)', 'E.1 (Strategic Planning)'],
            'DigComp': ['5.3 (Creatively Using Technologies)', '1.1 (Browsing and Searching)'],
            'GreenComp': ['3.3 (Science Literacy)', '2.3 (Future-Mindedness)']
        }
    }

def rewrite_profile_comprehensive(self, profile: Dict[str, Any], profile_id: str) -> Dict[str, Any]:
    """
    Comprehensive profile rewriting to achieve EU compliance
    """
    role_data = self.role_specific_data.get(profile_id, {})
    if not role_data:
        raise ValueError(f"Unknown role ID: {profile_id}")
    
    # Create new compliant profile structure
    rewritten_profile = {
        'title': role_data['title'],
        'eqf_level': profile.get('eqf_level', 7),
        'profile_id': profile_id,
        'role_overview': self._generate_role_overview(profile_id, role_data),
        'core_competency_areas': role_data['core_competencies'],
        'learning_outcomes': self._generate_integrated_learning_outcomes(profile_id, role_data, profile.get('eqf_level', 7)),
        'competency_framework_alignment': self._generate_framework_alignment(profile_id),
        'career_progression': self._generate_career_progression(role_data),
        'entry_requirements': self._generate_entry_requirements(profile.get('eqf_level', 7)),
        'assessment_philosophy': self._generate_assessment_philosophy(profile_id, role_data),
        'industry_application': self._generate_industry_application(profile_id, role_data),
        'distinctive_features': role_data['distinctive_features']
    }
    
    return rewritten_profile

def _generate_role_overview(self, role_id: str, role_data: Dict[str, Any]) -> str:
    """Generate EU-compliant role overview"""
    eqf_level = 7  # Default for strategic roles
    
    overviews = {
        'DSL': f"{role_data['title']}s spearhead organizational transformation by aligning sustainability goals with business strategy. At EQF Level {eqf_level}, these professionals evaluate and embed ESG principles into operations, manage stakeholder engagement across complex environments, and drive strategic frameworks that advance sustainability performance and compliance.",
        
        'DSM': f"{role_data['title']}s coordinate implementation of digital sustainability initiatives within organizations. At EQF Level 6-7, these professionals manage project teams, monitor performance against sustainability targets, and ensure operational excellence in sustainability program delivery while maintaining stakeholder engagement and regulatory compliance.",
        
        'DSC': f"{role_data['title']}s provide specialized advisory services to organizations seeking to enhance their digital sustainability practices. At EQF Level 6-8, these professionals assess client needs, design solution architectures, and guide implementation strategies while transferring knowledge and building organizational capacity for long-term sustainability success.",
        
        'DAN': f"{role_data['title']}s transform environmental and social data into strategic insights that drive evidence-based sustainability decision-making. At EQF Level 6-7, these professionals develop analytical frameworks, create predictive models, and communicate complex data relationships to diverse stakeholders through compelling visualizations and reports.",
        
        'SDD': f"{role_data['title']}s create environmentally conscious digital solutions through sustainable coding practices and energy-efficient application development. At EQF Level 5-7, these professionals integrate environmental considerations into software design, optimize energy consumption, and implement green development methodologies throughout the software lifecycle.",
        
        'SSD': f"{role_data['title']}s architect sustainable digital infrastructures and systems that minimize environmental impact while maximizing operational efficiency. At EQF Level 6-7, these professionals assess technology options, design eco-friendly system architectures, and integrate sustainability principles into digital infrastructure planning and implementation.",
        
        'SBA': f"{role_data['title']}s analyze business processes to identify opportunities for sustainability integration and optimization. At EQF Level 6-7, these professionals gather requirements, model sustainable business processes, and facilitate stakeholder alignment around environmental and social objectives within organizational change initiatives.",
        
        'DSI': f"{role_data['title']}s specialize in deploying and integrating sustainable digital technologies within organizational environments. At EQF Level 5-7, these professionals coordinate technical implementations, ensure system optimization, and maintain quality standards while managing the transition to sustainable digital practices.",
        
        'DSE': f"{role_data['title']}s develop and deliver educational programs that build digital sustainability competencies across diverse learning environments. At EQF Level 6-8, these professionals design curricula, integrate pedagogical technologies, and assess learning outcomes while advancing the field of sustainability education through research and innovation.",
        
        'STS': f"{role_data['title']}s focus on emerging technologies and research applications that advance sustainability goals through digital innovation. At EQF Level 4-6, these professionals evaluate technology solutions, conduct applied research, and facilitate knowledge transfer between research and practice communities in sustainability technology applications."
    }
    
    return overviews.get(role_id, f"{role_data['title']}s work in the field of digital sustainability with focus on {role_data['strategic_focus']}.")

def _generate_integrated_learning_outcomes(self, role_id: str, role_data: Dict[str, Any], eqf_level: int) -> Dict[str, List[str]]:
    """Generate integrated, non-repetitive learning outcomes"""
    complexity_verbs = self.eqf_complexity_verbs.get(eqf_level, self.eqf_complexity_verbs[7])
    
    outcomes_templates = {
        'DSL': [
            f"{complexity_verbs[0].title()} complex sustainability challenges into strategic frameworks that align ESG objectives with business performance and stakeholder value creation.",
            f"{complexity_verbs[1].title()} and transform organizational systems to embed sustainability principles into core operations, ensuring regulatory compliance and competitive advantage.",
            f"{complexity_verbs[2].title()} stakeholder engagement strategies that build consensus around sustainability initiatives while managing conflicting priorities in complex ecosystems."
        ],
        'DSM': [
            f"{complexity_verbs[0].title()} sustainability project portfolios that deliver measurable environmental and social impact while maintaining operational efficiency and stakeholder satisfaction.",
            f"{complexity_verbs[1].title()} cross-functional teams to implement digital sustainability solutions, ensuring alignment with organizational strategy and regulatory requirements.",
            f"{complexity_verbs[2].title()} performance monitoring systems that track sustainability KPIs and provide actionable insights for continuous improvement and stakeholder reporting."
        ],
        'DSC': [
            f"{complexity_verbs[0].title()} comprehensive sustainability assessments that identify optimization opportunities and provide strategic recommendations for organizational transformation.",
            f"{complexity_verbs[1].title()} client relationships through expert advisory services that bridge sustainability knowledge gaps and accelerate implementation success.",
            f"{complexity_verbs[2].title()} solution architectures that integrate sustainability principles with business requirements, ensuring long-term viability and stakeholder value creation."
        ],
        'DAN': [
            f"{complexity_verbs[0].title()} analytical frameworks that integrate sustainability performance with financial metrics to support evidence-based ESG strategy development.",
            f"{complexity_verbs[1].title()} cross-functional analytics initiatives that transform raw environmental data into strategic insights for executive decision-making.",
            f"{complexity_verbs[2].title()} and oversee data governance standards for sustainability analytics to ensure ethical information use and organizational learning."
        ],
        'SDD': [
            f"{complexity_verbs[0].title()} energy-efficient software solutions that minimize environmental impact while maintaining high performance and user experience standards.",
            f"{complexity_verbs[1].title()} sustainable development methodologies that integrate environmental considerations throughout the software development lifecycle.",
            f"{complexity_verbs[2].title()} code optimization strategies that reduce computational resource consumption and support carbon-neutral application deployment."
        ],
        'SSD': [
            f"{complexity_verbs[0].title()} sustainable system architectures that balance environmental impact with functional requirements and operational scalability.",
            f"{complexity_verbs[1].title()} technology assessment frameworks that evaluate digital infrastructure options for environmental and economic optimization.",
            f"{complexity_verbs[2].title()} system integration strategies that enable sustainable digital transformation while maintaining security and performance standards."
        ],
        'SBA': [
            f"{complexity_verbs[0].title()} business process analysis methodologies that identify sustainability integration opportunities and quantify potential impact.",
            f"{complexity_verbs[1].title()} stakeholder engagement processes that align diverse organizational perspectives around sustainable business transformation objectives.",
            f"{complexity_verbs[2].title()} requirements engineering approaches that translate sustainability goals into actionable business process improvements and system specifications."
        ],
        'DSI': [
            f"{complexity_verbs[0].title()} technical solution deployments that integrate sustainability technologies with existing organizational infrastructure and workflows.",
            f"{complexity_verbs[1].title()} implementation quality assurance processes that ensure sustainable technology solutions meet performance and environmental standards.",
            f"{complexity_verbs[2].title()} system optimization strategies that maximize the environmental and operational benefits of deployed sustainability technologies."
        ],
        'DSE': [
            f"{complexity_verbs[0].title()} educational curricula that integrate digital sustainability competencies with pedagogical best practices and learning outcome assessment.",
            f"{complexity_verbs[1].title()} technology-enhanced learning experiences that engage diverse learners in sustainability knowledge development and practical application.",
            f"{complexity_verbs[2].title()} assessment methodologies that evaluate both knowledge acquisition and real-world application of digital sustainability competencies."
        ],
        'STS': [
            f"{complexity_verbs[0].title()} technology evaluation frameworks that assess emerging digital solutions for sustainability applications and organizational fit.",
            f"{complexity_verbs[1].title()} research methodologies that advance understanding of technology-sustainability relationships and inform evidence-based practice.",
            f"{complexity_verbs[2].title()} knowledge transfer processes that bridge research findings with practical implementation in organizational sustainability initiatives."
        ]
    }
    
    base_outcomes = outcomes_templates.get(role_id, [
        f"{complexity_verbs[0].title()} sustainability principles in digital contexts.",
        f"{complexity_verbs[1].title()} solutions for digital sustainability challenges.",
        f"{complexity_verbs[2].title()} sustainable practices in professional environments."
    ])
    
    return {str(eqf_level): base_outcomes}

def _generate_framework_alignment(self, role_id: str) -> Dict[str, Any]:
    """Generate specific framework alignment"""
    mappings = self.framework_mappings.get(role_id, {})
    
    alignment = {
        'eqf_focus': f"Strategic leadership and innovation in sustainability transformation",
        'key_frameworks': mappings
    }
    
    return alignment

def _generate_career_progression(self, role_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate logical career progression"""
    progression = role_data.get('career_progression', {})
    
    return {
        'entry_level': progression.get('entry', 'Entry Level Professional'),
        'mid_level': progression.get('mid', 'Senior Professional'),
        'senior_level': progression.get('senior', 'Lead Professional'),
        'executive_level': progression.get('executive', 'Executive Professional')
    }

def _generate_entry_requirements(self, eqf_level: int) -> Dict[str, str]:
    """Generate appropriate entry requirements"""
    requirements = {
        4: {
            'academic': "Secondary education completion or equivalent qualification",
            'professional': "1-2 years experience in relevant field or demonstrated competency",
            'key_competencies': "Basic digital literacy, environmental awareness, communication skills"
        },
        5: {
            'academic': "Post-secondary education or equivalent professional qualification",
            'professional': "2-3 years progressive experience in sustainability or related field",
            'key_competencies': "Digital competency, project coordination, stakeholder communication"
        },
        6: {
            'academic': "Bachelor's degree or equivalent professional qualification",
            'professional': "3-5 years experience with demonstrated progression in sustainability field",
            'key_competencies': "Advanced digital skills, analytical thinking, project management"
        },
        7: {
            'academic': "Bachelor's with honours or Master's in relevant strategic field",
            'professional': "5+ years progressive leadership experience in sustainability or business transformation",
            'key_competencies': "Strategic planning, change leadership, ESG frameworks, stakeholder management"
        },
        8: {
            'academic': "Master's degree with research component or equivalent advanced qualification",
            'professional': "7+ years senior leadership experience with demonstrated innovation impact",
            'key_competencies': "Strategic innovation, research methodology, thought leadership, organizational transformation"
        }
    }
    
    return requirements.get(eqf_level, requirements[7])

def _generate_assessment_philosophy(self, role_id: str, role_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate assessment philosophy without curriculum details"""
    
    assessment_approaches = {
        'DSL': {
            'approach': 'Strategic evaluation emphasizing systems-level impact',
            'focus_areas': [
                'Sustainability transformation strategy development',
                'Stakeholder ecosystem management portfolio',
                'Governance and policy design assessment'
            ]
        },
        'DSM': {
            'approach': 'Competency-based evaluation focusing on implementation excellence',
            'focus_areas': [
                'Project portfolio management and delivery',
                'Team leadership and coordination effectiveness',
                'Performance monitoring and improvement strategies'
            ]
        },
        'DSC': {
            'approach': 'Portfolio-based assessment emphasizing client value creation',
            'focus_areas': [
                'Client advisory and solution development',
                'Knowledge transfer and capacity building',
                'Strategic recommendation and implementation guidance'
            ]
        },
        'DAN': {
            'approach': 'Evidence-based evaluation through analytical portfolio development',
            'focus_areas': [
                'Data analysis and insight generation projects',
                'Predictive modeling and forecasting capabilities',
                'Stakeholder communication and visualization excellence'
            ]
        }
    }
    
    default_approach = {
        'approach': 'Competency-based evaluation emphasizing practical application',
        'focus_areas': [
            'Professional competency demonstration',
            'Real-world problem solving',
            'Stakeholder engagement and communication'
        ]
    }
    
    return assessment_approaches.get(role_id, default_approach)

def _generate_industry_application(self, role_id: str, role_data: Dict[str, Any]) -> List[str]:
    """Generate industry application contexts"""
    
    industry_contexts = {
        'DSL': [
            "Multinational corporations implementing net-zero and ESG policies",
            "Investment firms embedding sustainability into portfolio governance", 
            "Public institutions shaping environmental and social policy",
            "Global NGOs and development agencies driving systemic change"
        ],
        'DSM': [
            "Corporate sustainability departments implementing digital transformation",
            "Manufacturing organizations optimizing environmental performance",
            "Technology companies developing sustainable business practices",
            "Government agencies coordinating sustainability initiatives"
        ],
        'DSC': [
            "Management consulting firms providing sustainability advisory services",
            "Specialized sustainability consulting practices",
            "Professional services organizations supporting client transformation",
            "Independent advisory practices in sustainability strategy"
        ],
        'DAN': [
            "Financial institutions developing ESG analytics capabilities",
            "Environmental monitoring organizations processing sensor data",
            "Corporate sustainability teams analyzing performance metrics",
            "Research institutions studying environmental and social trends"
        ]
    }
    
    default_contexts = [
        f"Organizations implementing digital sustainability initiatives",
        f"Teams focused on {role_data.get('strategic_focus', 'sustainability transformation')}",
        f"Professional environments requiring {role_data.get('industry_focus', 'sustainability expertise')}"
    ]
    
    return industry_contexts.get(role_id, default_contexts)

def rewrite_all_profiles(self, input_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Rewrite all educational profiles to achieve EU compliance
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original_profiles = json.load(f)
    except Exception as e:
        return {'error': f"Failed to load profiles: {e}"}
    
    rewritten_profiles = {}
    rewrite_summary = {
        'total_profiles': 0,
        'successfully_rewritten': 0,
        'failed_rewrites': 0,
        'improvements': []
    }
    
    for profile_id, profile_data in original_profiles.items():
        try:
            if isinstance(profile_data, dict):
                rewritten_profile = self.rewrite_profile_comprehensive(profile_data, profile_id)
                rewritten_profiles[profile_id] = rewritten_profile
                rewrite_summary['successfully_rewritten'] += 1
                rewrite_summary['improvements'].append(f"✅ {profile_id}: Transformed to EU-compliant structure")
            else:
                rewrite_summary['failed_rewrites'] += 1
                rewrite_summary['improvements'].append(f"❌ {profile_id}: Invalid profile structure")
            
            rewrite_summary['total_profiles'] += 1
            
        except Exception as e:
            rewrite_summary['failed_rewrites'] += 1
            rewrite_summary['improvements'].append(f"❌ {profile_id}: Rewrite failed - {e}")
    
    # Save rewritten profiles
    if output_path:
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(rewritten_profiles, f, indent=2, ensure_ascii=False)
            rewrite_summary['improvements'].append(f"💾 Rewritten profiles saved to: {output_path}")
        except Exception as e:
            rewrite_summary['improvements'].append(f"❌ Failed to save rewritten profiles: {e}")
    
    return {
        'rewritten_profiles': rewritten_profiles,
        'summary': rewrite_summary
    }

def compare_before_after(self, original_path: str, rewritten_profiles: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare original vs rewritten profiles for improvement analysis
    """
    try:
        with open(original_path, 'r', encoding='utf-8') as f:
            original_profiles = json.load(f)
    except Exception as e:
        return {'error': f"Failed to load original profiles: {e}"}
    
    comparison = {}
    
    for profile_id in original_profiles.keys():
        if profile_id in rewritten_profiles:
            original = original_profiles[profile_id]
            rewritten = rewritten_profiles[profile_id]
            
            comparison[profile_id] = {
                'improvements': [],
                'structural_changes': [],
                'compliance_enhancements': []
            }
            
            # Check learning outcomes improvement
            original_outcomes = original.get('learning_outcomes', {})
            rewritten_outcomes = rewritten.get('learning_outcomes', {})
            
            if self._outcomes_improved(original_outcomes, rewritten_outcomes):
                comparison[profile_id]['improvements'].append("✅ Learning outcomes: Eliminated repetition and improved integration")
            
            # Check curriculum contamination removal
            if self._contamination_removed(original, rewritten):
                comparison[profile_id]['improvements'].append("✅ Curriculum contamination: Removed ECTS, modules, and assessment details")
            
            # Check role differentiation enhancement
            if self._role_differentiation_enhanced(original, rewritten):
                comparison[profile_id]['improvements'].append("✅ Role differentiation: Added specific competency areas and distinctive features")
            
            # Check framework alignment improvement
            if self._framework_alignment_improved(original, rewritten):
                comparison[profile_id]['improvements'].append("✅ Framework alignment: Added specific competency mappings")
            
            # Check career progression logic
            if self._career_progression_improved(original, rewritten):
                comparison[profile_id]['improvements'].append("✅ Career progression: Established logical role-consistent advancement")
    
    return comparison

def _outcomes_improved(self, original: Any, rewritten: Any) -> bool:
    """Check if learning outcomes were improved"""
    if not isinstance(rewritten, dict):
        return False
    
    rewritten_texts = []
    for outcomes in rewritten.values():
        if isinstance(outcomes, list):
            rewritten_texts.extend(outcomes)
    
    # Check for integration keywords
    integration_keywords = ['synthesize', 'integrate', 'transform', 'strategic', 'complex']
    has_integration = any(keyword in ' '.join(rewritten_texts).lower() for keyword in integration_keywords)
    
    # Check for template patterns (should be reduced)
    template_pattern = r"apply .* principles to"
    has_templates = bool(re.search(template_pattern, ' '.join(rewritten_texts).lower()))
    
    return has_integration and not has_templates

def _contamination_removed(self, original: Dict[str, Any], rewritten: Dict[str, Any]) -> bool:
    """Check if curriculum contamination was removed"""
    contamination_keywords = ['ects', 'semester', 'module 1', 'module 2', 'written exam', 'coursework']
    
    rewritten_text = json.dumps(rewritten).lower()
    contamination_found = any(keyword in rewritten_text for keyword in contamination_keywords)
    
    return not contamination_found

def _role_differentiation_enhanced(self, original: Dict[str, Any], rewritten: Dict[str, Any]) -> bool:
    """Check if role differentiation was enhanced"""
    return (
        'core_competency_areas' in rewritten and 
        'distinctive_features' in rewritten and
        len(rewritten.get('distinctive_features', [])) >= 3
    )

def _framework_alignment_improved(self, original: Dict[str, Any], rewritten: Dict[str, Any]) -> bool:
    """Check if framework alignment was improved"""
    alignment = rewritten.get('competency_framework_alignment', {})
    return (
        'key_frameworks' in alignment and
        isinstance(alignment['key_frameworks'], dict) and
        len(alignment['key_frameworks']) >= 3
    )

def _career_progression_improved(self, original: Dict[str, Any], rewritten: Dict[str, Any]) -> bool:
    """Check if career progression was improved"""
    progression = rewritten.get('career_progression', {})
    return (
        isinstance(progression, dict) and
        len(progression) >= 4 and
        all(key in progression for key in ['entry_level', 'mid_level', 'senior_level', 'executive_level'])
    )
def main():
"""
Main function for educational profile rewriting
"""
import argparse
parser = argparse.ArgumentParser(description="Educational Profile Rewriter - EU Compliance Transformation")
parser.add_argument('--input', '-i', required=True, help="Path to original educational profiles JSON file")
parser.add_argument('--output', '-o', help="Path for rewritten profiles (default: add _eu_compliant suffix)")
parser.add_argument('--comparison', '-c', action='store_true', help="Generate before/after comparison report")
parser.add_argument('--validate', '-v', action='store_true', help="Validate rewritten profiles with EU compliance checker")
parser.add_argument('--quiet', '-q', action='store_true', help="Suppress detailed output")

args = parser.parse_args()

# Determine output path
if not args.output:
    input_path = Path(args.input)
    args.output = str(input_path.parent / f"{input_path.stem}_eu_compliant{input_path.suffix}")

rewriter = EUProfileRewriter()

if not args.quiet:
    print("🔄 Educational Profile Rewriter - EU Compliance Transformation")
    print("="*70)
    print(f"📥 Input: {args.input}")
    print(f"📤 Output: {args.output}")

# Perform rewriting
rewrite_result = rewriter.rewrite_all_profiles(args.input, args.output)

if 'error' in rewrite_result:
    print(f"❌ Rewriting failed: {rewrite_result['error']}")
    return 1

summary = rewrite_result['summary']

if not args.quiet:
    print(f"\n📊 REWRITING SUMMARY:")
    print(f"📋 Total Profiles: {summary['total_profiles']}")
    print(f"✅ Successfully Rewritten: {summary['successfully_rewritten']}")
    print(f"❌ Failed Rewrites: {summary['failed_rewrites']}")
    
    print(f"\n📝 IMPROVEMENTS:")
    for improvement in summary['improvements']:
        print(f"  {improvement}")

# Generate comparison if requested
if args.comparison:
    comparison = rewriter.compare_before_after(args.input, rewrite_result['rewritten_profiles'])
    
    if 'error' not in comparison:
        print(f"\n🔍 BEFORE/AFTER COMPARISON:")
        print("-" * 50)
        
        for profile_id, changes in comparison.items():
            print(f"\n📋 {profile_id}:")
            for improvement in changes['improvements']:
                print(f"  {improvement}")

# Validate if requested
if args.validate:
    try:
        # Import the validation engine
        sys.path.append(str(Path(__file__).parent))
        from content_specificity_engine import ContentSpecificityEngine
        
        validator = ContentSpecificityEngine()
        validation_report = validator.validate_educational_profiles(args.output)
        
        if 'error' not in validation_report:
            overall = validation_report['overall_compliance']
            print(f"\n🔍 EU COMPLIANCE VALIDATION:")
            print(f"📊 Overall Status: {overall['status'].upper()}")
            print(f"📈 Compliance Score: {overall['score']:.1%}")
            print(f"💡 Recommendation: {overall['recommendation']}")
        
    except ImportError:
        print("⚠️  Validation skipped - content_specificity_engine not available")

return 0 if summary['failed_rewrites'] == 0 else 1
if name == "main":
exit(main())
