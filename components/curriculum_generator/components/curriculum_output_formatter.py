#!/usr/bin/env python3
# scripts/curriculum_generator/components/curriculum_output_formatter.py
"""
Curriculum Output Formatter - Generates exact Example_Curriculum.txt format
"""

import json
from typing import Dict, List, Any

class CurriculumOutputFormatter:
    """Formats curriculum output to match Example_Curriculum.txt exactly"""
    
    def __init__(self):
        self.role_definitions = self._load_roles()
        
    def _load_roles(self) -> Dict:
        """Load role definitions"""
        try:
            with open('roles.json', 'r') as f:
                roles = json.load(f)
                return {role['id']: role for role in roles}
        except:
            return {}
    
    def format_curriculum_output(self, role_id: str, eqf_level: int, ects: float, 
                                uol: int, selected_modules: List[Dict]) -> str:
        """Generate curriculum output in exact Example_Curriculum.txt format"""
        
        role = self.role_definitions.get(role_id, {})
        role_name = role.get('name', 'Professional')
        total_hours = ects * 25
        
        # Generate the exact header format
        output = f"""Curriculum 
Digital Sustainability Professional Development Course
Specialization: {role_name}
EQF Level: {eqf_level}
ECTS: {ects} credits
Total Study Hours: {total_hours} hours
Delivery: Blended (Online + Practical + Work-Based Option)
Modules: {uol} Micro-Modules
Credential Format: Stackable Micro-Credentials + Certificate

1. 🎯 Programme Learning Outcomes (Aligned with EQF Level {eqf_level} Descriptors)
Upon successful completion, participants will be able to:

{self._generate_learning_outcomes(role_id, eqf_level)}

2. 📚 Modular Structure (Stackable, Granular, Mapped)
{self._generate_module_table(role_id, ects, uol)}

3. 📝 Assessment Strategy (Mapped to Competencies)
{self._generate_assessment_table(uol)}

4. 🌐 Framework Mapping
{self._generate_framework_mapping(role_id, eqf_level)}

5. 🧩 Stackability & Micro-Credentialing
{self._generate_stackability(role_id, uol, eqf_level)}

6. 🧪 Work-Based Integration Option
{self._generate_work_based(role_id)}

7. 👥 Target Audiences
{self._generate_target_audiences(role_id)}

8. 🛠 Support & QA
{self._generate_support_qa(role_id)}
"""
        return output
    
    def _generate_learning_outcomes(self, role_id: str, eqf_level: int) -> str:
        """Generate role-specific learning outcomes"""
        
        outcomes = {
            "DAN": [
                "Apply ESG and sustainability reporting standards (e.g., GRI, CSRD) to organizational datasets.",
                "Transform and validate sustainability datasets using data wrangling and cleaning techniques.",
                "Create dashboards or visual reports to communicate sustainability impact to stakeholders.",
                "Interpret ESG metrics to support data-driven decision-making in line with regulatory frameworks.",
                "Collaborate with teams to integrate ESG data practices into sustainability workflows."
            ],
            "DSE": [
                "Design and implement energy-efficient data architectures for sustainability applications.",
                "Optimize data pipeline performance while minimizing environmental impact through green computing.",
                "Establish data governance frameworks that support sustainability reporting requirements.",
                "Apply cloud optimization techniques to reduce carbon footprint of data infrastructure.",
                "Collaborate with technical teams to implement sustainable data engineering best practices."
            ],
            "DSC": [
                "Conduct comprehensive sustainability assessments for diverse organizational contexts.",
                "Deliver strategic sustainability advisory services that align with client objectives.",
                "Design customized sustainability transformation roadmaps based on maturity assessments.",
                "Facilitate stakeholder engagement sessions to build consensus around sustainability initiatives.",
                "Apply consulting methodologies to sustainability challenges across industry sectors."
            ],
            "DSL": [
                "Develop comprehensive digital sustainability strategies aligned with organizational goals.",
                "Lead transformation initiatives that integrate sustainability into digital operations.",
                "Influence executive stakeholders to drive adoption of sustainable digital practices.",
                "Design governance frameworks for sustainable digital transformation programs.",
                "Coordinate cross-functional teams to implement strategic sustainability initiatives."
            ],
            "DSM": [
                "Manage cross-functional sustainability programs from conception to implementation.",
                "Coordinate sustainability initiatives across multiple departments and stakeholder groups.",
                "Monitor, measure, and optimize sustainability performance using advanced KPI frameworks.",
                "Apply project management methodologies to sustainability transformation projects.",
                "Facilitate stakeholder engagement and communication for sustainability initiatives."
            ],
            "DSI": [
                "Develop predictive models for sustainability impact assessment using machine learning.",
                "Apply advanced analytics techniques to solve complex environmental challenges.",
                "Design AI-driven solutions that optimize sustainability performance across operations.",
                "Communicate complex data science insights to technical and non-technical stakeholders.",
                "Integrate ethical considerations into AI applications for sustainability contexts."
            ],
            "SBA": [
                "Analyze business processes to identify sustainability improvement opportunities.",
                "Develop and implement sustainability metrics and KPIs for organizational performance.",
                "Create compelling business cases for sustainability investments with ROI projections.",
                "Facilitate cross-functional collaboration to align sustainability with business strategy.",
                "Apply business analysis methodologies to sustainability transformation initiatives."
            ],
            "SDD": [
                "Implement green coding practices and energy-efficient programming techniques.",
                "Develop sustainable software applications with minimal environmental footprint.",
                "Apply code optimization strategies to reduce computational resource consumption.",
                "Integrate sustainability principles throughout software development lifecycle.",
                "Collaborate with development teams to establish sustainable coding standards."
            ],
            "SSD": [
                "Design sustainable IT architectures and systems with sustainability as core principle.",
                "Apply circular design methodologies to technology solutions and user experiences.",
                "Integrate eco-design frameworks to minimize environmental impact of digital solutions.",
                "Balance functionality with environmental responsibility in technical solution design.",
                "Lead interdisciplinary design processes that prioritize sustainability outcomes."
            ],
            "STS": [
                "Configure and support sustainability tools and platforms for organizational goals.",
                "Implement technical solutions that enable comprehensive sustainability data collection.",
                "Provide user support and training for sustainability software and digital tools.",
                "Troubleshoot and optimize sustainability technology implementations.",
                "Collaborate with technical teams to integrate sustainability tools with existing systems."
            ]
        }
        
        role_outcomes = outcomes.get(role_id, outcomes["DAN"])
        return "\n".join(role_outcomes)
    
    def _generate_module_table(self, role_id: str, total_ects: float, num_modules: int) -> str:
        """Generate module table exactly like Example_Curriculum.txt"""
        
        module_ects = round(total_ects / num_modules, 1)
        module_hours = round(module_ects * 25, 1)
        
        # Role-specific module names
        module_names = {
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
            "DSC": [
                "Sustainability Assessment & Advisory Methodologies",
                "Client Engagement & Consulting Delivery",
                "Strategic Sustainability Solution Design"
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
        
        # Micro-credential names
        credentials = {
            "DAN": "ESG Data Analytics Foundations",
            "DSE": "Sustainable Data Engineering Basics",
            "DSC": "Sustainability Consulting Methodology",
            "DSL": "Digital Sustainability Leadership Essentials",
            "DSM": "Sustainability Program Management Fundamentals",
            "DSI": "AI for Sustainability Applications",
            "SBA": "Sustainability Business Analysis Fundamentals",
            "SDD": "Green Software Development Essentials",
            "SSD": "Sustainable Solution Design Principles",
            "STS": "Sustainability Technical Support Basics"
        }
        
        names = module_names.get(role_id, module_names["DAN"])
        base_credential = credentials.get(role_id, "Sustainability Professional Competency")
        
        # Create the exact table format from Example_Curriculum.txt
        table = "Module Title\tHours\tECTS\tLearning Outcomes\tMicro-Credential\n"
        
        for i in range(num_modules):
            module_name = names[i] if i < len(names) else f"Advanced {role_id} Applications"
            outcomes = f"Develop comprehensive knowledge and skilled problem-solving in {module_name.lower()} for sustainability contexts"
            credential = f'"{base_credential} - Module {i+1}"'
            
            table += f"M{i+1}. {module_name}\t{module_hours}\t{module_ects}\t{outcomes}\t{credential}\n"
        
        return table
    
    def _generate_assessment_table(self, num_modules: int) -> str:
        """Generate assessment strategy table exactly like Example_Curriculum.txt"""
        
        modules_list = ", ".join([f"M{i+1}" for i in range(num_modules)])
        last_modules = ", ".join([f"M{i+1}" for i in range(max(1, num_modules-1), num_modules)])
        
        return f"""Component\tDescription\tWeight\tLinked Modules
Portfolio\tCurated digital evidence of sustainability tasks, reports, and reflections\t40%\t{modules_list}
Practical Project\tEnd-to-end sustainability task: analyze → implement → evaluate → reflect\t35%\t{last_modules}
Peer Collaboration Task\tGroup feedback on deliverables, joint problem-solving challenges\t15%\t{last_modules}
Reflective Journal\tSelf-assessment and goal-setting for sustainability career development\t10%\tAll"""
    
    def _generate_framework_mapping(self, role_id: str, eqf_level: int) -> str:
        """Generate framework mapping exactly like Example_Curriculum.txt"""
        
        eqf_descriptors = {
            4: "Competent, skilled professional able to work with guidance and some autonomy.",
            5: "Competent, skilled, problem-solving professional able to work independently and cooperatively.",
            6: "Advanced competent professional able to manage complex projects and lead others.",
            7: "Highly specialized professional able to innovate and lead organizational transformation.",
            8: "Expert professional at the cutting edge of knowledge and practice."
        }
        
        frameworks = {
            "DAN": ["e-CF 4.0 Competence B.1: Application Development", "e-CF 4.0 Competence D.11: Needs Identification", "e-CF 4.0 Competence C.2: Sustainability"],
            "DSE": ["e-CF 4.0 Competence B.2: Component Integration", "e-CF 4.0 Competence C.1: User Support", "e-CF 4.0 Competence A.3: Business Plan Development"],
            "DSC": ["e-CF 4.0 Competence A.4: Product/Service Planning", "e-CF 4.0 Competence D.11: Needs Identification", "e-CF 4.0 Competence E.8: Information Security Management"]
        }
        
        esco_mappings = {
            "DAN": 'Links to "Data Analyst (ESCO: 251101)"',
            "DSE": 'Links to "Data Engineer (ESCO: 251103)"',
            "DSC": 'Links to "Management Consultant (ESCO: 242112)"'
        }
        
        descriptor = eqf_descriptors.get(eqf_level, "Professional competency")
        framework_list = frameworks.get(role_id, frameworks["DAN"])
        esco = esco_mappings.get(role_id, esco_mappings["DAN"])
        
        framework_text = "\n".join(framework_list)
        
        return f"""EQF Level {eqf_level}: {descriptor}

e-CF Mapping:
{framework_text}

ESCO Mapping: {esco} and transversal skills such as "green thinking" and "digital literacy.\""""
    
    def _generate_stackability(self, role_id: str, num_modules: int, eqf_level: int) -> str:
        """Generate stackability section exactly like Example_Curriculum.txt"""
        
        modules_progression = " → ".join([f"[ Module {i+1} ]" for i in range(num_modules)])
        
        return f"""Each module results in a digital badge and micro-credential. All {num_modules} stack toward the full {role_id} for Sustainability Certificate, referenced against EQF and compatible with NQFs and ECVET.

A visual progression map shows:

{modules_progression}
          ⤷        Certificate of Completion ({num_modules} modules, EQF {eqf_level})"""
    
    def _generate_work_based(self, role_id: str) -> str:
        """Generate work-based learning section exactly like Example_Curriculum.txt"""
        
        wbl_options = {
            "DAN": ["ESG reporting teams", "Real-world ESG data case"],
            "DSE": ["Green IT infrastructure teams", "Energy efficiency case"],
            "DSC": ["Sustainability consulting firms", "Client assessment case"],
            "DSL": ["C-suite strategy teams", "Strategic planning case"],
            "DSM": ["Program management offices", "Program coordination case"],
            "DSI": ["AI/ML teams", "Predictive modeling case"],
            "SBA": ["Business analysis teams", "Process analysis case"],
            "SDD": ["Development teams", "Green coding case"],
            "SSD": ["Design teams", "Sustainable design case"],
            "STS": ["Technical support teams", "System integration case"]
        }
        
        options = wbl_options.get(role_id, wbl_options["DAN"])
        
        return f"""Learners may opt for:

Mini-placement with {options[0]} (hybrid format)

{role_id} labs ({options[1]})

Recognition of Prior Learning (RPL) to shorten module 2"""
    
    def _generate_target_audiences(self, role_id: str) -> str:
        """Generate target audiences exactly like Example_Curriculum.txt"""
        
        role_name = self.role_definitions.get(role_id, {}).get('name', 'professionals')
        
        return f"""Junior/aspiring {role_name.lower()} moving into sustainability

Sustainability officers upskilling in {role_id.lower()} techniques

Professionals retraining from finance/ICT/environmental roles"""
    
    def _generate_support_qa(self, role_id: str) -> str:
        """Generate support and QA section exactly like Example_Curriculum.txt"""
        
        return f"""Instructors: {role_id} sustainability experts + tech trainers

Peer groups: Weekly asynchronous forums + monthly live sessions

Quality: Mapped to EQF and reviewed annually"""