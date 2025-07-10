scripts/curriculum_generator/components/educational_profile_improver.py
"""
Educational Profile Improver - Straightforward EU Compliance Fix
Directly addresses critique points: repetitive outcomes, curriculum contamination, role differentiation
"""
import json
import re
from typing import Dict, List, Any
class EducationalProfileImprover:
"""
Straightforward profile improvement to achieve EU compliance
"""
def __init__(self):
    self.role_learning_outcomes = {
        'DSL': {
            7: [
                "Synthesize complex sustainability challenges into strategic frameworks that align ESG objectives with business performance and stakeholder value creation",
                "Evaluate and transform organizational systems to embed sustainability principles into core operations, ensuring regulatory compliance and competitive advantage", 
                "Design stakeholder engagement strategies that build consensus around sustainability initiatives while managing conflicting priorities in complex ecosystems"
            ],
            8: [
                "Innovate transformation methodologies that establish new organizational paradigms for sustainability leadership and strategic value creation",
                "Lead multi-stakeholder ecosystems through visionary sustainability governance that creates systemic change across industry boundaries",
                "Establish thought leadership that shapes regulatory development and influences global sustainability standards through strategic innovation"
            ]
        },
        'DSM': {
            6: [
                "Integrate sustainability implementation initiatives that deliver measurable environmental outcomes while maintaining operational efficiency and stakeholder satisfaction",
                "Synthesize environmental management systems with digital tools to optimize monitoring, reporting, and continuous improvement processes",
                "Coordinate cross-functional teams to achieve sustainability objectives while addressing diverse organizational requirements and constraints"
            ],
            7: [
                "Innovate implementation frameworks that embed sustainability practices into organizational operations and establish new performance standards",
                "Lead transformation initiatives that accelerate sustainability adoption across complex organizational systems and stakeholder networks", 
                "Establish governance mechanisms that ensure sustained environmental impact while building organizational capabilities for continuous improvement"
            ]
        },
        'DSC': {
            6: [
                "Synthesize comprehensive sustainability assessments that identify strategic opportunities and provide actionable recommendations for organizational transformation",
                "Evaluate complex regulatory environments to provide expert guidance for environmental compliance and risk management strategies",
                "Design client engagement processes that build trusted advisory relationships and deliver measurable value through strategic consulting"
            ],
            7: [
                "Innovate consulting methodologies that establish new benchmarks for sustainability advisory services and client transformation outcomes",
                "Lead comprehensive organizational transformations requiring coordination of diverse stakeholder groups and complex change management",
                "Establish thought leadership in sustainability consulting that influences industry best practices and regulatory development"
            ]
        },
        'DAN': {
            6: [
                "Synthesize complex environmental datasets to identify strategic sustainability opportunities and quantify organizational impact across multiple metrics",
                "Evaluate data collection methodologies for sustainability metrics, ensuring compliance with reporting frameworks while maintaining analytical rigor",
                "Design predictive analytics models that forecast environmental risks and opportunities, enabling proactive organizational responses"
            ],
            7: [
                "Innovate analytical frameworks that integrate sustainability performance with financial metrics to support evidence-based ESG strategy development",
                "Lead cross-functional analytics initiatives that transform environmental data into strategic insights for executive decision-making",
                "Establish data governance standards for sustainability analytics that ensure ethical information use and organizational learning"
            ]
        },
        'DSE': {
            6: [
                "Design energy-efficient data processing architectures that minimize environmental impact while ensuring performance and scalability requirements",
                "Implement automated sustainability data pipelines with robust quality assurance and regulatory compliance validation processes",
                "Evaluate infrastructure resource consumption through measurable carbon footprint reduction and optimization strategies"
            ],
            7: [
                "Innovate sustainable infrastructure solutions that establish new organizational standards for green IT and carbon-aware computing",
                "Lead technical teams implementing carbon-aware computing strategies based on renewable energy availability and demand optimization",
                "Establish enterprise-wide sustainable technology governance frameworks that influence organizational environmental strategy"
            ]
        },
        'DSI': {
            7: [
                "Synthesize advanced predictive models that address complex environmental challenges through rigorous scientific methodology and innovation",
                "Evaluate diverse environmental datasets to support evidence-based policy development at organizational and societal levels",
                "Design analytical frameworks that advance scientific understanding of sustainability systems and environmental interactions"
            ],
            8: [
                "Innovate breakthrough analytical methodologies that establish new scientific standards for sustainability research and application",
                "Lead multidisciplinary research initiatives combining technical expertise with domain knowledge for sustainability challenges",
                "Establish thought leadership in sustainability data science that influences academic standards and industry innovation"
            ]
        },
        'SBA': {
            6: [
                "Synthesize business processes with sustainability requirements to identify strategic opportunities that create environmental and financial value",
                "Evaluate organizational performance against sustainability benchmarks while developing comprehensive measurement and improvement frameworks",
                "Design evidence-based business cases that demonstrate value proposition of sustainability investments and strategic initiatives"
            ],
            7: [
                "Innovate analytical frameworks that reveal strategic connections between sustainability performance and business value creation",
                "Lead cross-functional analytical initiatives that transform organizational understanding of sustainability opportunities and risks",
                "Establish performance measurement systems that integrate sustainability indicators with business intelligence and strategic planning"
            ]
        },
        'SDD': {
            5: [
                "Apply energy-efficient coding practices to create applications that demonstrably reduce environmental impact while maintaining functionality",
                "Use sustainable architecture patterns to develop scalable solutions that optimize resource consumption and performance",
                "Support development teams while contributing to sustainable development community practices and knowledge sharing"
            ],
            6: [
                "Innovate software solutions that integrate environmental impact measurement throughout development lifecycles and operational deployment",
                "Lead development initiatives that establish organizational standards for sustainable software engineering and green coding practices",
                "Establish development methodologies that advance sustainable software engineering through open-source contributions and industry influence"
            ]
        },
        'SSD': {
            6: [
                "Synthesize innovative technology solutions that apply circular economy principles and systems thinking to create regenerative outcomes",
                "Evaluate life cycle assessment methodologies and integrate them into design processes while balancing functionality and environmental impact",
                "Facilitate collaborative design processes that engage diverse stakeholders in sustainable innovation and solution development"
            ],
            7: [
                "Innovate design methodologies that establish new standards for regenerative technology solutions and environmental restoration outcomes",
                "Lead organizational transformation in sustainable design practices while building capabilities for continuous environmental innovation",
                "Establish thought leadership in regenerative design that influences industry best practices and sustainable solution development"
            ]
        },
        'STS': {
            4: [
                "Apply sustainability technology platform configuration procedures to support environmental monitoring and reporting requirements",
                "Use technical support processes that enable effective user adoption while maintaining system security and performance standards",
                "Support technical teams in deploying environmental monitoring solutions that meet organizational quality and documentation requirements"
            ],
            5: [
                "Coordinate technical solutions that optimize sustainability platform performance while ensuring data integrity across organizational environments",
                "Develop user training initiatives that build organizational capabilities in sustainability technologies and system utilization",
                "Create technical approaches that improve platform effectiveness while establishing best practices for environmental technology implementation"
            ]
        }
    }
    
    self.standard_structure_fields = [
        'id', 'profile_name', 'role_description', 'core_competency_areas',
        'learning_outcomes_by_eqf', 'framework_alignment', 'career_progression',
        'entry_requirements_by_eqf', 'assessment_philosophy', 'industry_application',
        'distinctive_features'
    ]

def improve_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Improve a single profile to meet EU standards
    """
    profile_id = profile.get('id', 'UNKNOWN')
    
    improved_profile = {
        'id': profile_id,
        'profile_name': profile.get('profile_name', f"{profile_id} Educational Profile"),
        'role_description': self._improve_role_description(profile),
        'core_competency_areas': self._standardize_competency_areas(profile),
        'learning_outcomes_by_eqf': self._improve_learning_outcomes(profile, profile_id),
        'framework_alignment': self._improve_framework_alignment(profile),
        'career_progression': self._improve_career_progression(profile),
        'entry_requirements_by_eqf': self._standardize_entry_requirements(profile),
        'assessment_philosophy': self._improve_assessment_philosophy(profile),
        'industry_application': profile.get('industry_application', []),
        'distinctive_features': profile.get('distinctive_features', [])
    }
    
    return improved_profile

def _improve_role_description(self, profile: Dict[str, Any]) -> str:
    """
    Improve role description by removing curriculum contamination
    """
    description = profile.get('role_description', '')
    
    # Remove curriculum-level details
    contamination_patterns = [
        r'at eqf level \d+,',
        r'75 ects',
        r'semester',
        r'module \d+',
        r'written exam',
        r'coursework'
    ]
    
    cleaned_description = description
    for pattern in contamination_patterns:
        cleaned_description = re.sub(pattern, '', cleaned_description, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    cleaned_description = re.sub(r'\s+', ' ', cleaned_description).strip()
    
    return cleaned_description

def _standardize_competency_areas(self, profile: Dict[str, Any]) -> List[str]:
    """
    Standardize core competency areas
    """
    # Check multiple possible field names
    competencies = (
        profile.get('core_competency_areas') or 
        profile.get('distinctive_competencies') or
        []
    )
    
    if not competencies:
        # Provide default based on profile type
        profile_id = profile.get('id', '')
        defaults = {
            'DSL': ['Strategic Sustainability Leadership', 'Organizational Transformation', 'Stakeholder Engagement'],
            'DSM': ['Sustainability Implementation', 'Performance Management', 'Team Leadership'],
            'DSC': ['Sustainability Advisory', 'Client Relationship Management', 'Strategic Consulting'],
            'DAN': ['Sustainability Data Analytics', 'Environmental Impact Assessment', 'Strategic Insights'],
            'DSE': ['Sustainable Infrastructure', 'Green Computing', 'Technical Leadership'],
            'DSI': ['Sustainability Data Science', 'Environmental Research', 'Scientific Innovation'],
            'SBA': ['Business Analysis', 'Sustainability Integration', 'Performance Measurement'],
            'SDD': ['Green Software Development', 'Sustainable Architecture', 'Environmental Technology'],
            'SSD': ['Sustainable Solution Design', 'Regenerative Innovation', 'Circular Economy'],
            'STS': ['Technical Support', 'Platform Configuration', 'User Enablement']
        }
        competencies = defaults.get(profile_id, ['Digital Sustainability', 'Professional Excellence', 'Strategic Impact'])
    
    return competencies[:3]  # Limit to 3 core competencies

def _improve_learning_outcomes(self, profile: Dict[str, Any], profile_id: str) -> Dict[str, List[str]]:
    """
    Replace repetitive learning outcomes with integrated, role-specific ones
    """
    if profile_id in self.role_learning_outcomes:
        return {str(k): v for k, v in self.role_learning_outcomes[profile_id].items()}
    
    # Keep existing if already good
    existing_outcomes = profile.get('learning_outcomes_by_eqf', {})
    if existing_outcomes and not self._has_repetitive_outcomes(existing_outcomes):
        return existing_outcomes
    
    # Provide improved defaults
    return {
        "6": [
            f"Synthesize complex sustainability concepts into practical applications for {profile_id.lower()} contexts",
            f"Evaluate environmental and social impacts to develop strategic recommendations",
            f"Design sustainable solutions that integrate technical excellence with environmental responsibility"
        ]
    }

def _has_repetitive_outcomes(self, outcomes: Dict[str, Any]) -> bool:
    """
    Check if outcomes are repetitive
    """
    all_outcomes = []
    for level_outcomes in outcomes.values():
        if isinstance(level_outcomes, list):
            all_outcomes.extend(level_outcomes)
    
    # Check for repetitive patterns
    template_patterns = [
        "apply .* principles to address.*challenges",
        "the learner will be able to apply"
    ]
    
    repetitive_count = 0
    for outcome in all_outcomes:
        if any(re.search(pattern, outcome.lower()) for pattern in template_patterns):
            repetitive_count += 1
    
    return repetitive_count > len(all_outcomes) * 0.5

def _improve_framework_alignment(self, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Improve framework alignment with specific mappings
    """
    existing = profile.get('framework_alignment', {})
    
    # Ensure proper structure
    improved = {
        'eqf_focus': existing.get('eqf_focus', 'Strategic capability with autonomous responsibility'),
        'key_frameworks': existing.get('key_frameworks', ['e-CF', 'DigComp', 'GreenComp']),
        'competency_emphasis': existing.get('competency_emphasis', 'Professional excellence in sustainability')
    }
    
    return improved

def _improve_career_progression(self, profile: Dict[str, Any]) -> Dict[str, str]:
    """
    Improve career progression with consistent structure
    """
    existing = profile.get('career_progression', {})
    
    if isinstance(existing, dict) and 'entry_level' in existing:
        return existing
    
    # Convert list to structured progression
    if isinstance(existing, list) and len(existing) >= 3:
        return {
            'entry_level': existing[0],
            'mid_level': existing[1] if len(existing) > 1 else 'Senior Professional',
            'senior_level': existing[2] if len(existing) > 2 else 'Lead Professional',
            'executive_level': existing[3] if len(existing) > 3 else 'Executive Professional'
        }
    
    # Provide defaults based on profile
    profile_id = profile.get('id', '')
    defaults = {
        'DSL': {
            'entry_level': 'Sustainability Team Leader',
            'mid_level': 'Director of Sustainability Strategy', 
            'senior_level': 'Senior Director of Sustainability',
            'executive_level': 'Chief Sustainability Officer'
        },
        'DSM': {
            'entry_level': 'Sustainability Implementation Manager',
            'mid_level': 'Senior Sustainability Manager',
            'senior_level': 'Director of Sustainability Operations', 
            'executive_level': 'Executive Director of Sustainability'
        }
    }
    
    return defaults.get(profile_id, {
        'entry_level': 'Entry Professional',
        'mid_level': 'Senior Professional',
        'senior_level': 'Lead Professional', 
        'executive_level': 'Executive Professional'
    })

def _standardize_entry_requirements(self, profile: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """
    Standardize entry requirements structure
    """
    existing = profile.get('entry_requirements_by_eqf', {})
    
    if existing and isinstance(existing, dict):
        return existing
    
    # Provide standard structure
    return {
        "6": {
            "academic": "Bachelor's degree in relevant field with demonstrated capabilities",
            "professional": "3-4 years progressive experience in sustainability or related field",
            "core_competencies": "Professional competencies relevant to role requirements"
        },
        "7": {
            "academic": "Bachelor's with honours or Master's qualification in strategic field",
            "professional": "5+ years progressive leadership experience with demonstrated impact",
            "core_competencies": "Advanced professional competencies and leadership capabilities"
        }
    }

def _improve_assessment_philosophy(self, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Improve assessment philosophy without curriculum details
    """
    existing = profile.get('assessment_philosophy', {})
    
    if isinstance(existing, dict) and 'approach' in existing:
        # Remove any curriculum contamination from methods
        methods = existing.get('methods', [])
        clean_methods = [method for method in methods if not self._is_curriculum_detail(method)]
        
        return {
            'approach': existing.get('approach', 'Competency-based assessment'),
            'methods': clean_methods if clean_methods else ['Professional portfolio', 'Competency demonstration', 'Strategic project']
        }
    
    # Provide improved default
    return {
        'approach': 'Competency-based assessment emphasizing practical application',
        'methods': ['Professional portfolio', 'Competency demonstration', 'Strategic project']
    }

def _is_curriculum_detail(self, text: str) -> bool:
    """
    Check if text contains curriculum-level details
    """
    curriculum_keywords = ['ects', 'semester', 'exam', 'coursework', '% assessment', 'written', 'oral']
    return any(keyword in text.lower() for keyword in curriculum_keywords)

def improve_all_profiles(self, profiles_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Improve all profiles in the dataset
    """
    improved_profiles = []
    
    for profile in profiles_data:
        try:
            improved_profile = self.improve_profile(profile)
            improved_profiles.append(improved_profile)
            print(f"✅ Improved profile: {profile.get('id', 'Unknown')}")
        except Exception as e:
            print(f"❌ Failed to improve profile {profile.get('id', 'Unknown')}: {e}")
            improved_profiles.append(profile)  # Keep original if improvement fails
    
    return improved_profiles

def save_improved_profiles(self, input_path: str, output_path: str = None) -> str:
    """
    Load, improve, and save profiles
    """
    if not output_path:
        output_path = input_path.replace('.json', '_improved.json')
    
    # Load profiles
    with open(input_path, 'r', encoding='utf-8') as f:
        profiles_data = json.load(f)
    
    # Improve profiles
    improved_profiles = self.improve_all_profiles(profiles_data)
    
    # Save improved profiles
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(improved_profiles, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Improved profiles saved to: {output_path}")
    return output_path
def main():
"""
Main function for profile improvement
"""
import argparse
parser = argparse.ArgumentParser(description="Educational Profile Improver - Straightforward EU Compliance")
parser.add_argument('--input', '-i', required=True, help="Path to educational profiles JSON file")
parser.add_argument('--output', '-o', help="Output path (default: input_improved.json)")

args = parser.parse_args()

improver = EducationalProfileImprover()

print("🔧 Educational Profile Improver - EU Compliance Fix")
print("="*50)

try:
    output_path = improver.save_improved_profiles(args.input, args.output)
    print(f"\n✅ Profile improvement completed successfully!")
    print(f"📁 Improved profiles: {output_path}")
    return 0
except Exception as e:
    print(f"\n❌ Profile improvement failed: {e}")
    return 1
if name == "main":
exit(main())
