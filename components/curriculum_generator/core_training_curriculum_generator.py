# scripts/curriculum_generator/core_training_curriculum_generator.py
"""
Digital Sustainability Skills Core Training Curriculum Generator
Facilitates rapid upskilling/reskilling of different target groups into occupational profiles
Covers EQF levels 3-8 and focuses on high demand Digital Sustainability roles
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import existing components
from scripts.curriculum_generator.core.data_loader import DataLoader
from scripts.curriculum_generator.components.qualification_pathway_generator import generate_qualification_pathway_section
from scripts.curriculum_generator.domain.role_manager import RoleManager
from scripts.curriculum_generator.components.uol_learning_manager import UOLLearningManager
from scripts.curriculum_generator.components.general_industry_content_generator import GeneralIndustryContentGenerator
from scripts.curriculum_generator.core.ep_curriculum_integrator import EPCurriculumIntegrator

class CoreTrainingCurriculumGenerator:
    """Generates Digital Sustainability Skills Core Training Curricula for rapid upskilling/reskilling"""
    
    def __init__(self):
        # High demand Digital Sustainability roles for rapid training
        self.high_demand_roles = {
            "DAN": {"priority": "high", "demand_level": "critical", "timeframe": "immediate"},
            "DSM": {"priority": "critical", "demand_level": "high", "timeframe": "immediate"}, 
            "DSE": {"priority": "high", "demand_level": "high", "timeframe": "short-term"},
            "SDD": {"priority": "high", "demand_level": "critical", "timeframe": "immediate"},
            "DSC": {"priority": "medium", "demand_level": "high", "timeframe": "medium-term"},
            "SSD": {"priority": "high", "demand_level": "medium", "timeframe": "short-term"},
            "DSI": {"priority": "critical", "demand_level": "high", "timeframe": "short-term"},
            "DSL": {"priority": "critical", "demand_level": "critical", "timeframe": "immediate"},
            "STS": {"priority": "medium", "demand_level": "medium", "timeframe": "medium-term"}
        }
        
        # Target groups for reskilling
        self.target_groups = {
            "company_staff": {
                "description": "Existing company employees needing sustainability skills",
                "typical_background": "Various professional backgrounds, some digital literacy",
                "learning_pace": "accelerated", 
                "preferred_delivery": "in_company",
                "time_availability": "part_time",
                "focus": "practical_application"
            },
            "management": {
                "description": "Management and leadership roles requiring sustainability oversight",
                "typical_background": "Management experience, strategic thinking skills",
                "learning_pace": "intensive",
                "preferred_delivery": "executive_format",
                "time_availability": "limited_blocks",
                "focus": "strategic_implementation"
            },
            "technical_professionals": {
                "description": "IT, engineering, and technical staff expanding into sustainability",
                "typical_background": "Strong technical skills, analytical mindset",
                "learning_pace": "standard",
                "preferred_delivery": "blended",
                "time_availability": "flexible",
                "focus": "technical_integration"
            },
            "career_changers": {
                "description": "Professionals transitioning from other sectors into sustainability",
                "typical_background": "Professional experience, varying technical backgrounds",
                "learning_pace": "comprehensive", 
                "preferred_delivery": "full_time",
                "time_availability": "full_time",
                "focus": "foundation_to_advanced"
            },
            "graduates": {
                "description": "Recent graduates entering digital sustainability careers",
                "typical_background": "Academic foundation, limited professional experience",
                "learning_pace": "structured",
                "preferred_delivery": "academic_style",
                "time_availability": "full_time",
                "focus": "skill_building"
            }
        }
        
        # EQF 3 descriptors (adding support for EQF 3)
        self.eqf_3_descriptors = {
            "knowledge": "Knowledge of facts, principles, processes and general concepts, in a field of work or study",
            "skills": "A range of cognitive and practical skills required to accomplish tasks and solve problems by selecting and applying basic methods, tools, materials and information",
            "competence": "Take responsibility for completion of tasks in work or study; adapt own behaviour to circumstances in solving problems"
        }
        
        # Core curriculum structures by target group
        self.core_structures = {
            "rapid_upskilling": {
                "duration_weeks": "4-8 weeks",
                "intensity": "high",
                "ects_range": "5-15 ECTS",
                "focus": "immediate_application",
                "delivery": "intensive_blocks"
            },
            "comprehensive_reskilling": {
                "duration_weeks": "12-24 weeks", 
                "intensity": "medium",
                "ects_range": "15-45 ECTS",
                "focus": "career_transition",
                "delivery": "structured_programme"
            },
            "leadership_preparation": {
                "duration_weeks": "6-12 weeks",
                "intensity": "high",
                "ects_range": "10-30 ECTS", 
                "focus": "strategic_leadership",
                "delivery": "executive_format"
            }
        }
    
    def generate_core_training_curriculum(self, role: str, eqf_level: int, target_group: str, 
                                        training_type: str = "rapid_upskilling") -> Dict[str, Any]:
        """Generate core training curriculum for specific target group and training type"""
        
        # Validate inputs
        if role not in self.high_demand_roles:
            raise ValueError(f"Role {role} not in high demand roles for core training")
        
        if target_group not in self.target_groups:
            raise ValueError(f"Target group {target_group} not supported")
        
        if training_type not in self.core_structures:
            raise ValueError(f"Training type {training_type} not supported")
        
        # Get target group and training structure info
        target_info = self.target_groups[target_group]
        training_structure = self.core_structures[training_type]
        role_demand = self.high_demand_roles[role]
        
        # Determine ECTS based on training type and target group
        ects_ranges = {
            "rapid_upskilling": {"min": 5, "max": 15},
            "comprehensive_reskilling": {"min": 15, "max": 45}, 
            "leadership_preparation": {"min": 10, "max": 30}
        }
        
        # Select ECTS based on EQF level and training type
        ects_range = ects_ranges[training_type]
        if eqf_level <= 4:
            target_ects = ects_range["min"]
        elif eqf_level >= 7:
            target_ects = ects_range["max"]
        else:
            target_ects = (ects_range["min"] + ects_range["max"]) / 2
        
        # Determine UOL based on ECTS and training type
        if training_type == "rapid_upskilling":
            uol = max(2, min(4, int(target_ects / 3)))  # 2-4 units for rapid training
        elif training_type == "leadership_preparation":
            uol = max(3, min(6, int(target_ects / 4)))  # 3-6 units for leadership
        else:
            uol = max(4, min(8, int(target_ects / 5)))  # 4-8 units for comprehensive
        
        # Generate core curriculum structure
        core_curriculum = {
            "curriculum_type": "Digital Sustainability Skills Core Training Curriculum",
            "metadata": {
                "role": role,
                "role_demand_info": role_demand,
                "eqf_level": eqf_level,
                "target_group": target_group,
                "target_group_info": target_info,
                "training_type": training_type,
                "training_structure": training_structure,
                "target_ects": target_ects,
                "units_of_learning": uol,
                "generation_date": datetime.now().isoformat(),
                "curriculum_focus": "rapid_upskilling_reskilling",
                "delivery_optimization": target_info["preferred_delivery"]
            },
            
            "programme_overview": {
                "title": f"Digital Sustainability Skills Core Training - {role} for {target_group.replace('_', ' ').title()}",
                "description": f"Intensive {training_type.replace('_', ' ')} programme designed for {target_info['description'].lower()}. This {target_ects} ECTS core curriculum facilitates rapid transition into high-demand {role} roles.",
                "key_features": [
                    f"🎯 **High-Demand Role Focus**: {role} is classified as {role_demand['priority']} priority with {role_demand['demand_level']} market demand",
                    f"👥 **Target Group Optimized**: Specifically designed for {target_info['description'].lower()}",
                    f"⚡ **Rapid Implementation**: {training_structure['duration_weeks']} intensive programme with {training_structure['focus'].replace('_', ' ')} focus",
                    f"💼 **Workplace Integration**: {target_info['preferred_delivery'].replace('_', ' ')} delivery optimized for {target_info['time_availability']} schedules",
                    "🏆 **Industry Recognition**: Meets European qualification standards for immediate employability",
                    "📈 **Career Acceleration**: Direct pathway to high-demand sustainability roles"
                ]
            },
            
            "rapid_deployment_features": {
                "accelerated_learning": {
                    "intensive_delivery": f"{training_structure['intensity']} intensity with concentrated learning blocks",
                    "practical_focus": "70% hands-on application, 30% theoretical foundation",
                    "immediate_application": "Skills applicable in workplace within 2 weeks of training start",
                    "mentor_support": "Industry mentor assigned for each participant"
                },
                "company_integration": {
                    "workplace_projects": "Real company sustainability challenges as learning vehicles",
                    "team_cohorts": "Department-based learning cohorts for organizational alignment",
                    "management_engagement": "Regular progress updates and strategic alignment sessions",
                    "roi_tracking": "Measurable impact assessment and return on investment metrics"
                },
                "flexible_pathways": {
                    "modular_entry": "Entry points every 4 weeks for continuous onboarding",
                    "prior_learning": "Recognition of existing skills to accelerate progression",
                    "customization": "Programme adaptation to specific organizational needs",
                    "scaling": "Cohort sizes from 5-50 participants with maintained quality"
                }
            }
        }
        
        return core_curriculum
    
    def create_eqf_3_support(self) -> Dict[str, Any]:
        """Add EQF Level 3 support for core training curricula"""
        
        return {
            "eqf_level": 3,
            "descriptors": self.eqf_3_descriptors,
            "target_roles": ["DAN", "SDD"],  # Entry-level focus
            "typical_ects": "5-15 ECTS",
            "duration": "4-12 weeks",
            "entry_requirements": {
                "education": "Lower secondary education completion",
                "experience": "No prior professional experience required",
                "skills": "Basic digital literacy and willingness to learn"
            },
            "learning_outcomes_focus": [
                "Basic sustainability concepts and terminology",
                "Fundamental digital tools for sustainability tasks",
                "Entry-level workplace application skills",
                "Professional communication in sustainability contexts"
            ],
            "career_progression": "Pathway to EQF Level 4-5 roles with experience"
        }
    
    def create_target_group_specific_content(self, target_group: str, role: str) -> Dict[str, Any]:
        """Generate content specific to target group needs"""
        
        target_info = self.target_groups[target_group]
        
        if target_group == "company_staff":
            return {
                "learning_approach": "Problem-based learning using actual company challenges",
                "assessment_methods": [
                    "Workplace project completion",
                    "Peer assessment within department teams", 
                    "Manager evaluation of skill application",
                    "Self-reflection on learning integration"
                ],
                "delivery_schedule": "2-3 hours per week over 8-16 weeks, with monthly intensive days",
                "support_structure": "Internal mentors, external expert sessions, peer learning groups"
            }
        
        elif target_group == "management":
            return {
                "learning_approach": "Strategic case studies and leadership scenarios",
                "assessment_methods": [
                    "Strategic sustainability plan development",
                    "Board-level presentation preparation",
                    "Change management initiative design",
                    "ROI and impact measurement frameworks"
                ],
                "delivery_schedule": "Quarterly 2-3 day intensive blocks over 6-12 months",
                "support_structure": "Executive coaching, peer networking, expert advisory sessions"
            }
        
        elif target_group == "technical_professionals":
            return {
                "learning_approach": "Technical deep-dives with hands-on system implementation",
                "assessment_methods": [
                    "Technical system design and implementation",
                    "Code review and optimization projects",
                    "Integration testing and deployment",
                    "Technical documentation and knowledge transfer"
                ],
                "delivery_schedule": "Flexible online modules with monthly practical workshops",
                "support_structure": "Technical mentors, online labs, peer programming sessions"
            }
        
        elif target_group == "career_changers":
            return {
                "learning_approach": "Comprehensive foundation building with accelerated practical application",
                "assessment_methods": [
                    "Portfolio development across multiple competency areas",
                    "Industry project completion",
                    "Professional network development",
                    "Job readiness assessment and interview preparation"
                ],
                "delivery_schedule": "Full-time 12-24 week programme with structured progression",
                "support_structure": "Career counseling, industry placement support, alumni network"
            }
        
        else:  # graduates
            return {
                "learning_approach": "Structured academic progression with industry integration",
                "assessment_methods": [
                    "Academic assignments with industry relevance",
                    "Group projects with real company partners",
                    "Individual research and innovation projects",
                    "Professional competency examinations"
                ],
                "delivery_schedule": "Semester-based delivery with summer intensive options",
                "support_structure": "Academic supervision, industry guest lecturers, career services"
            }

def generate_comprehensive_core_curriculum(role: str, eqf_level: int, target_group: str, 
                                         training_type: str = "rapid_upskilling") -> Dict[str, Any]:
    """Generate comprehensive core training curriculum"""
    
    generator = CoreTrainingCurriculumGenerator()
    
    # Generate base core curriculum
    core_curriculum = generator.generate_core_training_curriculum(role, eqf_level, target_group, training_type)
    
    # Add target group specific content
    target_specific = generator.create_target_group_specific_content(target_group, role)
    core_curriculum["target_group_specific"] = target_specific
    
    # Add EQF 3 support if needed
    if eqf_level == 3:
        eqf_3_support = generator.create_eqf_3_support()
        core_curriculum["eqf_3_support"] = eqf_3_support
    
    # Generate actual learning units using existing system
    role_manager = RoleManager(project_root)
    uol_manager = UOLLearningManager()
    content_generator = GeneralIndustryContentGenerator()
    
    role_info = role_manager.get_role(role)
    if not role_info:
        raise ValueError(f"Role {role} not found")
    
    # Generate learning units optimized for rapid training
    target_ects = core_curriculum["metadata"]["target_ects"]
    uol = core_curriculum["metadata"]["units_of_learning"]
    
    base_units = uol_manager.distribute_ects_across_uol(
        total_ects=target_ects,
        uol=uol,
        role_id=role,
        topic=f"Core Training for {target_group.replace('_', ' ').title()}"
    )
    
    # Enhance units for rapid deployment
    enhanced_units = []
    for unit in base_units:
        # Generate accelerated unit title
        unit_title = f"Rapid {unit['progression_level']}: {role} Core Skills {unit['unit_number']}"
        
        # Create accelerated learning outcomes
        accelerated_outcomes = [
            f"Rapidly acquire {unit['progression_level'].lower()} level competencies in {role_info['name']} role",
            f"Immediately apply {unit['progression_level'].lower()} skills in workplace context",
            f"Demonstrate proficiency through practical project completion"
        ]
        
        enhanced_unit = {
            **unit,
            "unit_title": unit_title,
            "specific_learning_outcomes": accelerated_outcomes,
            "delivery_optimization": "rapid_deployment",
            "workplace_integration": True,
            "mentor_support": True,
            "immediate_application": True
        }
        enhanced_units.append(enhanced_unit)
    
    core_curriculum["learning_units"] = enhanced_units
    
    return core_curriculum

def generate_html_core_curriculum(curriculum_data: Dict[str, Any]) -> str:
    # Generate qualification pathway
    qualification_pathway_html = generate_qualification_pathway_section(
        course_ects=curriculum_data.get("metadata", {}).get("target_ects", 10.0),
        role=curriculum_data.get("metadata", {}).get("role", "DSM"),
        eqf_level=curriculum_data.get("metadata", {}).get("eqf_level", 6),
        target_group=curriculum_data.get("metadata", {}).get("target_group", "company_staff")
    )

        """Generate HTML for core training curriculum"""
    
    metadata = curriculum_data.get("metadata", {})
    programme_overview = curriculum_data.get("programme_overview", {})
    rapid_deployment = curriculum_data.get("rapid_deployment_features", {})
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Sustainability Skills Core Training Curriculum</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f8f9fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; box-shadow: 0 0 30px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #d32f2f 0%, #f57c00 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.2em; margin: 0 0 10px 0; }}
        .core-badge {{ background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 10px 0; font-weight: bold; }}
        .section {{ padding: 40px; border-bottom: 1px solid #eee; }}
        .section h2 {{ color: #d32f2f; font-size: 1.8em; margin-bottom: 20px; border-bottom: 2px solid #f57c00; padding-bottom: 10px; }}
        .highlight {{ background: linear-gradient(135deg, #d32f2f22 0%, #f57c0011 100%); padding: 25px; border-radius: 10px; margin: 20px 0; border: 1px solid #d32f2f44; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #f57c00; }}
        .rapid-feature {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border: 2px solid #d32f2f44; }}
        .demand-indicator {{ background: #d32f2f; color: white; padding: 5px 15px; border-radius: 15px; font-size: 0.9em; display: inline-block; margin: 5px; }}
        ul {{ margin-left: 20px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>Digital Sustainability Skills Core Training Curriculum</h1>
            <div class="core-badge">RAPID UPSKILLING & RESKILLING PROGRAMME</div>
            <p style="font-size: 1.1em; margin: 15px 0;">
                {metadata.get('role', 'Professional')} • EQF Level {metadata.get('eqf_level', 6)} • 
                {metadata.get('target_ects', 0)} ECTS • {metadata.get('units_of_learning', 0)} Learning Units
            </p>
            <p>Target Group: {metadata.get('target_group', '').replace('_', ' ').title()} • 
               Training Type: {metadata.get('training_type', '').replace('_', ' ').title()}</p>
        </header>
        
        <section class="section">
            <h2>🎯 Programme Overview</h2>
            <div class="highlight">
                <h3>{programme_overview.get('title', 'Core Training Programme')}</h3>
                <p style="font-size: 1.1em;">{programme_overview.get('description', '')}</p>
            </div>
            
            <h3>High-Demand Role Information</h3>
            <div style="margin: 20px 0;">
"""
    
    role_demand = metadata.get("role_demand_info", {})
    html += f"""                <span class="demand-indicator">Priority: {role_demand.get('priority', 'high').title()}</span>
                <span class="demand-indicator">Market Demand: {role_demand.get('demand_level', 'high').title()}</span>
                <span class="demand-indicator">Timeframe: {role_demand.get('timeframe', 'immediate').title()}</span>
            </div>
            
            <h3>Key Features</h3>
            <div class="grid">
"""
    
    for feature in programme_overview.get("key_features", []):
        html += f'                <div class="card">{feature}</div>\n'
    
    html += """            </div>
        </section>
        
        <section class="section">
            <h2>⚡ Rapid Deployment Features</h2>
"""
    
    for feature_category, features in rapid_deployment.items():
        html += f"""            <div class="rapid-feature">
                <h3>{feature_category.replace('_', ' ').title()}</h3>
"""
        for feature_name, feature_desc in features.items():
            html += f"""                <p><strong>{feature_name.replace('_', ' ').title()}:</strong> {feature_desc}</p>
"""
        html += "            </div>\n"
    
    # Add target group specific information
    target_specific = curriculum_data.get("target_group_specific", {})
    if target_specific:
        html += f"""
        <section class="section">
            <h2>👥 Target Group Optimization</h2>
            <div class="grid">
                <div class="card">
                    <h4>Learning Approach</h4>
                    <p>{target_specific.get('learning_approach', '')}</p>
                </div>
                <div class="card">
                    <h4>Delivery Schedule</h4>
                    <p>{target_specific.get('delivery_schedule', '')}</p>
                </div>
            </div>
            
            <h3>Assessment Methods</h3>
            <ul>
"""
        for method in target_specific.get("assessment_methods", []):
            html += f"                <li>{method}</li>\n"
        
        html += f"""            </ul>
            
            <div class="highlight">
                <h4>Support Structure</h4>
                <p>{target_specific.get('support_structure', '')}</p>
            </div>
        </section>
"""
    
    # Add learning units
    learning_units = curriculum_data.get("learning_units", [])
    if learning_units:
        html += """
        <section class="section">
            <h2>🧱 Core Learning Units</h2>
"""
        for unit in learning_units:
            html += f"""            <div class="card" style="margin: 15px 0;">
                <h4>{unit.get('unit_title', f"Unit {unit.get('unit_number', 1)}")}</h4>
                <p><strong>Level:</strong> {unit.get('progression_level', 'Development')} | 
                   <strong>ECTS:</strong> {unit.get('ects', 0)} | 
                   <strong>Focus:</strong> Rapid deployment with immediate application</p>
                <ul>
"""
            for outcome in unit.get('specific_learning_outcomes', []):
                html += f"                    <li>{outcome}</li>\n"
            
            html += """                </ul>
            </div>
"""
        
        html += """        </section>
"""
    
    html += f"""
        <!-- QUALIFICATION PATHWAY SECTION -->
        {qualification_pathway_html}
        
                <footer style="background: #d32f2f; color: white; padding: 30px; text-align: center;">
            <h3>🚀 Digital Sustainability Skills Core Training Curriculum</h3>
            <p>Facilitating Rapid Upskilling & Reskilling for High-Demand Roles</p>
            <p style="margin-top: 15px; opacity: 0.8;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 
                EQF Levels 3-8 Supported | Industry-Ready Deployment
            </p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Main CLI for Core Training Curriculum Generator"""
    parser = argparse.ArgumentParser(
        description='Digital Sustainability Skills Core Training Curriculum Generator'
    )
    
    # Core arguments
    parser.add_argument('--role', help='Professional role (DAN, DSM, DSE, etc.)')
    parser.add_argument('--eqf-level', type=int, choices=[3,4,5,6,7,8], help='EQF level (3-8)')
    parser.add_argument('--target-group', choices=['company_staff', 'management', 'technical_professionals', 'career_changers', 'graduates'], 
                       help='Target group for reskilling')
    parser.add_argument('--training-type', choices=['rapid_upskilling', 'comprehensive_reskilling', 'leadership_preparation'],
                       default='rapid_upskilling', help='Type of training programme')
    
    # Optional arguments
    parser.add_argument('--list-options', action='store_true', help='List available options')
    parser.add_argument('--output-dir', default='output/core_training_curricula', help='Output directory')
    parser.add_argument('--output-json', action='store_true', help='Generate JSON output')
    
    args = parser.parse_args()
    
    try:
        print("🚀 Digital Sustainability Skills Core Training Curriculum Generator")
        print("=" * 80)
        print("   📚 Facilitating rapid upskilling/reskilling of different target groups")
        print("   🎯 EQF levels 3-8 supported")
        print("   💼 Focus on high demand Digital Sustainability roles")
        print("   🏢 Company staff and management reskilling optimization")
        print(f"   🎯 Generation timestamp: {datetime.now().isoformat()}")
        
        if args.list_options:
            generator = CoreTrainingCurriculumGenerator()
            
            print("\n📋 Available Options:")
            print("\n🎯 High Demand Roles:")
            for role, info in generator.high_demand_roles.items():
                print(f"   {role}: {info['priority']} priority, {info['demand_level']} demand, {info['timeframe']} timeframe")
            
            print("\n👥 Target Groups:")
            for group, info in generator.target_groups.items():
                print(f"   {group}: {info['description']}")
            
            print("\n📚 Training Types:")
            for training_type, info in generator.core_structures.items():
                print(f"   {training_type}: {info['duration_weeks']}, {info['ects_range']}")
            
            print("\n📊 EQF Levels: 3, 4, 5, 6, 7, 8 (Level 3 newly supported for core training)")
            return
        
        # Validate required arguments
        if not args.role or not args.eqf_level or not args.target_group:
            parser.error("--role, --eqf-level, and --target-group are required")
        
        print(f"\n📊 Generating Core Training Curriculum:")
        print(f"   Role: {args.role}")
        print(f"   EQF Level: {args.eqf_level}")
        print(f"   Target Group: {args.target_group}")
        print(f"   Training Type: {args.training_type}")
        
        # Generate core training curriculum
        core_curriculum = generate_comprehensive_core_curriculum(
            args.role, args.eqf_level, args.target_group, args.training_type
        )
        
        print(f"\n✅ Core curriculum generated:")
        print(f"   ECTS: {core_curriculum['metadata']['target_ects']}")
        print(f"   Units: {core_curriculum['metadata']['units_of_learning']}")
        print(f"   Duration: {core_curriculum['metadata']['training_structure']['duration_weeks']}")
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename_base = f"CORE_TRAINING_{args.role}_EQF{args.eqf_level}_{args.target_group}_{args.training_type}_{timestamp}"
        
        # Save JSON
        if args.output_json:
            json_file = output_dir / f"{filename_base}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(core_curriculum, f, indent=2, ensure_ascii=False)
            print(f"   ✅ JSON saved: {json_file}")
        
        # Generate HTML
        html_content = generate_html_core_curriculum(core_curriculum)
        html_file = output_dir / f"{filename_base}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✅ HTML saved: {html_file}")
        
        print(f"\n🎉 Core Training Curriculum generation completed!")
        print(f"   🎯 Ready for rapid deployment and upskilling/reskilling")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
