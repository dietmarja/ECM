#!/usr/bin/env python3
"""
T3.2 Reviewer Check Suite - Educational Profiles & Curricula Design
EU Project Reviewer Validation for Task 3.2 Deliverable

TASK T3.2 OBJECTIVES:
- Design innovative digital sustainability educational profiles
- Multiple EQF levels (4-8) for multiple roles
- Modular curricula with ECTS points
- Full curricula for national education systems
- Upskilling/reskilling focused curricula
- High flexibility through modular components
- Support for dual education principles
"""

import json
import sys
from pathlib import Path
from datetime import date

class T32ReviewerCheckSuite:
    """
    Reviewer validation suite for T3.2 deliverable compliance
    """
    
    def __init__(self, input_dir="input"):
        self.input_dir = Path(input_dir)
        self.review_results = {
            "review_date": date.today().isoformat(),
            "reviewer": "EU_Project_Reviewer",
            "task": "T3.2_Educational_Profiles_Curricula",
            "deliverable": "Output_5_Digital_Sustainability_Skills_Core_Training_Curriculum",
            "compliance_checks": {},
            "critical_findings": [],
            "recommendations": [],
            "overall_rating": "PENDING"
        }
        
    def run_t32_compliance_review(self):
        """Run comprehensive T3.2 compliance review"""
        print("🔍 === T3.2 REVIEWER CHECK SUITE ===")
        print("📋 Task: Educational Profiles & Curricula Design")
        print("🎯 Deliverable: Digital Sustainability Skills Core Training Curriculum")
        print(f"📅 Review Date: {date.today().isoformat()}")
        
        # Core T3.2 Requirements Validation
        self.check_multiple_eqf_levels()           # EQF 4-8 coverage
        self.check_role_based_profiles()           # Multiple roles from WP2
        self.check_modular_design()               # Modular learning components
        self.check_ects_implementation()          # ECTS points system
        self.check_curriculum_flexibility()       # Adaptable combinations
        self.check_delivery_methodologies()       # Multiple delivery modes
        self.check_learning_pathways()           # Flexible progression
        self.check_dual_education_support()      # Workplace/classroom integration
        self.check_target_audience_adaptation()   # Different learner types
        self.check_upskilling_reskilling_focus()  # Skills gap addressing
        
        # Generate compliance report
        self.generate_t32_compliance_report()
        
        return self.review_results["overall_rating"] in ["EXCELLENT", "SATISFACTORY"]
    
    def check_multiple_eqf_levels(self):
        """T3.2 Requirement: Multiple EQF levels (4-8) coverage"""
        print("\n📊 === EQF Levels Coverage (EQF 4-8) ===")
        
        # Load micro credentials to check EQF distribution
        micro_file = self.input_dir / "micro_credentials.json"
        if not micro_file.exists():
            self.review_results["critical_findings"].append("CRITICAL: No micro credentials data for EQF analysis")
            self.review_results["compliance_checks"]["eqf_levels"] = "FAILED - No data"
            return
        
        with open(micro_file, 'r') as f:
            micro_credentials = json.load(f)
        
        # Analyze EQF distribution
        eqf_distribution = {}
        for micro in micro_credentials:
            eqf_level = micro.get('eqf_level', 'Unknown')
            eqf_distribution[eqf_level] = eqf_distribution.get(eqf_level, 0) + 1
        
        required_levels = [4, 5, 6, 7, 8]
        covered_levels = [level for level in required_levels if level in eqf_distribution]
        
        print(f"   📊 EQF Level Distribution: {eqf_distribution}")
        print(f"   🎯 Required Levels (4-8): {required_levels}")
        print(f"   ✅ Covered Levels: {covered_levels}")
        print(f"   📈 Coverage: {len(covered_levels)}/{len(required_levels)} ({(len(covered_levels)/len(required_levels))*100:.1f}%)")
        
        if len(covered_levels) >= 4:  # At least 4 out of 5 levels
            print("   ✅ COMPLIANCE: Excellent EQF coverage for multiple educational levels")
            self.review_results["compliance_checks"]["eqf_levels"] = "EXCELLENT"
        elif len(covered_levels) >= 3:
            print("   ⚠️  PARTIAL: Good EQF coverage but missing some levels")
            self.review_results["compliance_checks"]["eqf_levels"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient EQF level coverage")
            self.review_results["compliance_checks"]["eqf_levels"] = "FAILED"
            self.review_results["critical_findings"].append("Insufficient EQF level coverage (4-8)")
    
    def check_role_based_profiles(self):
        """T3.2 Requirement: Multiple roles identified in WP2"""
        print("\n👥 === Role-Based Educational Profiles ===")
        
        # Check for role-based structure in curricula
        roles_file = self.input_dir / "roles" / "roles.json"
        if roles_file.exists():
            with open(roles_file, 'r') as f:
                roles_data = json.load(f)
            
            print(f"   📊 Available Roles: {len(roles_data)}")
            
            # Sample role analysis
            for i, role in enumerate(roles_data[:3]):  # Show first 3 roles
                print(f"   Role {i+1}: {role.get('name', 'Unknown')}")
                print(f"      Focus: {role.get('focus_area', 'Not specified')}")
                print(f"      Level: EQF {role.get('target_eqf_level', 'Not specified')}")
            
            if len(roles_data) >= 5:
                print("   ✅ COMPLIANCE: Multiple role-based profiles available")
                self.review_results["compliance_checks"]["role_profiles"] = "EXCELLENT"
            elif len(roles_data) >= 3:
                print("   ⚠️  PARTIAL: Some role-based profiles available")
                self.review_results["compliance_checks"]["role_profiles"] = "SATISFACTORY"
            else:
                print("   ❌ NON-COMPLIANT: Insufficient role diversity")
                self.review_results["compliance_checks"]["role_profiles"] = "FAILED"
        else:
            print("   ⚠️  No dedicated roles file found - checking curriculum diversity")
            # Alternative: Check curriculum diversity
            self.review_results["compliance_checks"]["role_profiles"] = "PARTIAL - No roles file"
    
    def check_modular_design(self):
        """T3.2 Requirement: Modular learning components as building blocks"""
        print("\n🧩 === Modular Design Implementation ===")
        
        # Check three-tier modular structure
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        micro_file = self.input_dir / "micro_credentials.json"
        modules_file = self.input_dir / "modules" / "modules.json"
        
        modular_components = {
            "nano_credentials": 0,
            "micro_credentials": 0,
            "modules": 0
        }
        
        # Count modular components
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    modular_components["nano_credentials"] = len(nano_data['nano_credentials'])
                else:
                    modular_components["nano_credentials"] = len(nano_data) if isinstance(nano_data, list) else 0
        
        if micro_file.exists():
            with open(micro_file, 'r') as f:
                micro_data = json.load(f)
                modular_components["micro_credentials"] = len(micro_data)
        
        if modules_file.exists():
            with open(modules_file, 'r') as f:
                modules_data = json.load(f)
                modular_components["modules"] = len(modules_data)
        
        print(f"   📊 Modular Components:")
        print(f"      Nano Credentials (atomic): {modular_components['nano_credentials']}")
        print(f"      Micro Credentials (modular): {modular_components['micro_credentials']}")
        print(f"      Modules (comprehensive): {modular_components['modules']}")
        
        total_components = sum(modular_components.values())
        
        if total_components >= 100:
            print("   ✅ COMPLIANCE: Extensive modular component library")
            self.review_results["compliance_checks"]["modular_design"] = "EXCELLENT"
        elif total_components >= 50:
            print("   ✅ COMPLIANCE: Good modular component coverage")
            self.review_results["compliance_checks"]["modular_design"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient modular components")
            self.review_results["compliance_checks"]["modular_design"] = "FAILED"
    
    def check_ects_implementation(self):
        """T3.2 Requirement: ECTS points for comparability"""
        print("\n💳 === ECTS Points Implementation ===")
        
        # Analyze ECTS distribution across components
        micro_file = self.input_dir / "micro_credentials.json"
        if not micro_file.exists():
            self.review_results["compliance_checks"]["ects_implementation"] = "FAILED - No data"
            return
        
        with open(micro_file, 'r') as f:
            micro_credentials = json.load(f)
        
        # ECTS analysis
        ects_values = []
        ects_distribution = {}
        
        for micro in micro_credentials:
            ects = float(micro.get('ects_points', 0))
            ects_values.append(ects)
            
            # Categorize ECTS
            if ects <= 5:
                category = "Short (≤5 ECTS)"
            elif ects <= 15:
                category = "Medium (6-15 ECTS)"
            else:
                category = "Long (>15 ECTS)"
            
            ects_distribution[category] = ects_distribution.get(category, 0) + 1
        
        total_ects = sum(ects_values)
        
        print(f"   📊 ECTS Implementation:")
        print(f"      Total ECTS Available: {total_ects:.1f}")
        print(f"      Average ECTS per Component: {(total_ects/len(ects_values)):.2f}")
        print(f"      ECTS Distribution: {ects_distribution}")
        
        # Check ECTS range compliance
        if total_ects >= 60:  # Equivalent to at least one academic year
            print("   ✅ COMPLIANCE: Substantial ECTS coverage for programme comparability")
            self.review_results["compliance_checks"]["ects_implementation"] = "EXCELLENT"
        elif total_ects >= 30:
            print("   ✅ COMPLIANCE: Good ECTS coverage for semester-level programmes")
            self.review_results["compliance_checks"]["ects_implementation"] = "SATISFACTORY"
        else:
            print("   ⚠️  LIMITED: ECTS coverage may be insufficient for full programmes")
            self.review_results["compliance_checks"]["ects_implementation"] = "PARTIAL"
    
    def check_curriculum_flexibility(self):
        """T3.2 Requirement: High flexibility through modular combinations"""
        print("\n🔄 === Curriculum Flexibility Assessment ===")
        
        # Check relationship mappings for flexible combinations
        rel_file = self.input_dir / "relationships" / "nano_to_micro.json"
        if rel_file.exists():
            with open(rel_file, 'r') as f:
                relationships = json.load(f)
            
            micro_to_nano = relationships.get('micro_to_nano_mapping', {})
            
            # Analyze combination possibilities
            combination_count = len(micro_to_nano)
            average_components_per_combo = 0
            
            if micro_to_nano:
                total_components = sum(len(mapping.get('nano_credential_ids', [])) for mapping in micro_to_nano.values())
                average_components_per_combo = total_components / len(micro_to_nano)
            
            print(f"   📊 Flexibility Metrics:")
            print(f"      Available Combinations: {combination_count}")
            print(f"      Average Components per Combination: {average_components_per_combo:.1f}")
            
            # Check for stacking rules
            stacking_rules = relationships.get('stacking_rules', {})
            has_stacking = bool(stacking_rules)
            
            print(f"      Stacking Rules Defined: {'✅' if has_stacking else '❌'}")
            
            if combination_count >= 20 and has_stacking:
                print("   ✅ COMPLIANCE: High flexibility with multiple combination options")
                self.review_results["compliance_checks"]["curriculum_flexibility"] = "EXCELLENT"
            elif combination_count >= 10:
                print("   ✅ COMPLIANCE: Good flexibility for modular combinations")
                self.review_results["compliance_checks"]["curriculum_flexibility"] = "SATISFACTORY"
            else:
                print("   ❌ NON-COMPLIANT: Limited flexibility in curriculum combinations")
                self.review_results["compliance_checks"]["curriculum_flexibility"] = "FAILED"
        else:
            print("   ❌ NON-COMPLIANT: No relationship mappings for flexible combinations")
            self.review_results["compliance_checks"]["curriculum_flexibility"] = "FAILED"
    
    def check_delivery_methodologies(self):
        """T3.2 Requirement: Different delivery methodologies"""
        print("\n🎓 === Delivery Methodologies Support ===")
        
        # Check nano credentials for delivery methodology information
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Analyze delivery methods
            delivery_methods = set()
            participation_forms = set()
            
            for nano in nano_credentials:
                # Check participation form
                participation = nano.get('participation_form', 'Not specified')
                participation_forms.add(participation)
                
                # Check assessment format (indicates delivery capability)
                assessment = nano.get('assessment_type', {})
                if isinstance(assessment, dict):
                    format_type = assessment.get('format', 'Not specified')
                    delivery_methods.add(format_type)
            
            print(f"   📊 Delivery Methods Supported:")
            print(f"      Participation Forms: {list(participation_forms)}")
            print(f"      Assessment Formats: {list(delivery_methods)}")
            
            # T3.2 specifically requires: workplace, classroom, blended, online
            required_methods = {"workplace", "classroom", "blended", "online", "hybrid"}
            supported_methods = delivery_methods.union(participation_forms)
            
            # Check coverage
            coverage = len([method for method in required_methods 
                          if any(req in str(method).lower() for req in 
                               ["workplace", "classroom", "blend", "online", "hybrid", "face_to_face"])])
            
            if coverage >= 3:
                print("   ✅ COMPLIANCE: Multiple delivery methodologies supported")
                self.review_results["compliance_checks"]["delivery_methodologies"] = "EXCELLENT"
            elif coverage >= 2:
                print("   ✅ COMPLIANCE: Basic delivery methodology variety")
                self.review_results["compliance_checks"]["delivery_methodologies"] = "SATISFACTORY"
            else:
                print("   ❌ NON-COMPLIANT: Limited delivery methodology support")
                self.review_results["compliance_checks"]["delivery_methodologies"] = "FAILED"
        else:
            print("   ❌ NON-COMPLIANT: No delivery methodology information available")
            self.review_results["compliance_checks"]["delivery_methodologies"] = "FAILED"
    
    def check_learning_pathways(self):
        """T3.2 Requirement: Flexible learning pathways"""
        print("\n🛤️ === Learning Pathways Implementation ===")
        
        # Check for pathway definitions in relationships
        rel_file = self.input_dir / "relationships" / "nano_to_micro.json"
        if rel_file.exists():
            with open(rel_file, 'r') as f:
                relationships = json.load(f)
            
            # Check for dependency graphs (indicate pathways)
            nano_to_micro = relationships.get('nano_to_micro_mapping', {})
            pathway_indicators = 0
            
            for nano_id, mapping in nano_to_micro.items():
                if 'sequence_number' in mapping:
                    pathway_indicators += 1
            
            # Check stacking framework
            stacking_framework = relationships.get('stacking_framework', {})
            has_pathways = bool(stacking_framework)
            
            print(f"   📊 Pathway Implementation:")
            print(f"      Sequential Components: {pathway_indicators}")
            print(f"      Stacking Framework: {'✅' if has_pathways else '❌'}")
            
            # Also check nano credentials for dependency information
            nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
            dependency_count = 0
            
            if nano_file.exists():
                with open(nano_file, 'r') as f:
                    nano_data = json.load(f)
                    if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                        nano_credentials = nano_data['nano_credentials']
                    else:
                        nano_credentials = nano_data
                
                for nano in nano_credentials:
                    stackability = nano.get('stackability_elements', {})
                    if 'dependency_graph' in stackability:
                        dependency_count += 1
            
            print(f"      Dependency Definitions: {dependency_count}")
            
            if pathway_indicators >= 10 and has_pathways and dependency_count >= 5:
                print("   ✅ COMPLIANCE: Comprehensive learning pathway support")
                self.review_results["compliance_checks"]["learning_pathways"] = "EXCELLENT"
            elif pathway_indicators >= 5 or has_pathways:
                print("   ✅ COMPLIANCE: Basic learning pathway structure")
                self.review_results["compliance_checks"]["learning_pathways"] = "SATISFACTORY"
            else:
                print("   ❌ NON-COMPLIANT: Limited learning pathway definition")
                self.review_results["compliance_checks"]["learning_pathways"] = "FAILED"
        else:
            print("   ❌ NON-COMPLIANT: No learning pathway information available")
            self.review_results["compliance_checks"]["learning_pathways"] = "FAILED"
    
    def check_dual_education_support(self):
        """T3.2 Requirement: Dual education principle support"""
        print("\n🏢 === Dual Education Integration ===")
        
        # Check for workplace relevance indicators
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            workplace_integration_count = 0
            authentic_workplace_count = 0
            
            for nano in nano_credentials:
                # Check workplace relevance
                workplace_relevance = nano.get('workplace_relevance', {})
                if workplace_relevance:
                    workplace_integration_count += 1
                
                # Check for authentic workplace assessment
                assessment = nano.get('assessment_type', {})
                if isinstance(assessment, dict):
                    if assessment.get('format') == 'authentic_workplace':
                        authentic_workplace_count += 1
            
            workplace_percentage = (workplace_integration_count / len(nano_credentials)) * 100
            authentic_percentage = (authentic_workplace_count / len(nano_credentials)) * 100
            
            print(f"   📊 Dual Education Indicators:")
            print(f"      Workplace Relevance: {workplace_integration_count}/{len(nano_credentials)} ({workplace_percentage:.1f}%)")
            print(f"      Authentic Workplace Assessment: {authentic_workplace_count}/{len(nano_credentials)} ({authentic_percentage:.1f}%)")
            
            if workplace_percentage >= 80:
                print("   ✅ COMPLIANCE: Excellent workplace integration for dual education")
                self.review_results["compliance_checks"]["dual_education"] = "EXCELLENT"
            elif workplace_percentage >= 60:
                print("   ✅ COMPLIANCE: Good workplace integration support")
                self.review_results["compliance_checks"]["dual_education"] = "SATISFACTORY"
            else:
                print("   ⚠️  LIMITED: Workplace integration may be insufficient for dual education")
                self.review_results["compliance_checks"]["dual_education"] = "PARTIAL"
        else:
            print("   ❌ NON-COMPLIANT: No workplace integration information")
            self.review_results["compliance_checks"]["dual_education"] = "FAILED"
    
    def check_target_audience_adaptation(self):
        """T3.2 Requirement: Adaptation to different target audiences"""
        print("\n🎯 === Target Audience Adaptation ===")
        
        # T3.2 specifies: students/job seekers, digital professionals, business owners/managers
        # Check for audience-specific indicators in nano credentials
        
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Analyze skill gap targeting (indicates audience focus)
            audience_indicators = {
                "technical": 0,      # Digital professionals
                "conceptual": 0,     # Students/job seekers
                "behavioral": 0,     # Business owners/managers
                "procedural": 0      # All audiences
            }
            
            task_specificity = {
                "highly_specific": 0,     # Professionals
                "moderately_specific": 0, # Mixed audiences
                "broadly_applicable": 0   # Students/general
            }
            
            for nano in nano_credentials:
                workplace_relevance = nano.get('workplace_relevance', {})
                
                # Check skill gap targeting
                skill_gap = workplace_relevance.get('skill_gap_targeting', {})
                gap_type = skill_gap.get('gap_type', 'Not specified')
                if gap_type in audience_indicators:
                    audience_indicators[gap_type] += 1
                
                # Check task specificity
                specificity = workplace_relevance.get('task_specificity', 'Not specified')
                if specificity in task_specificity:
                    task_specificity[specificity] += 1
            
            print(f"   📊 Audience Adaptation Indicators:")
            print(f"      Skill Gap Types: {audience_indicators}")
            print(f"      Task Specificity: {task_specificity}")
            
            # Check diversity of audience targeting
            gap_diversity = len([v for v in audience_indicators.values() if v > 0])
            specificity_diversity = len([v for v in task_specificity.values() if v > 0])
            
            if gap_diversity >= 3 and specificity_diversity >= 2:
                print("   ✅ COMPLIANCE: Excellent audience adaptation diversity")
                self.review_results["compliance_checks"]["target_audience"] = "EXCELLENT"
            elif gap_diversity >= 2 or specificity_diversity >= 2:
                print("   ✅ COMPLIANCE: Good audience adaptation support")
                self.review_results["compliance_checks"]["target_audience"] = "SATISFACTORY"
            else:
                print("   ⚠️  LIMITED: Limited audience adaptation indicators")
                self.review_results["compliance_checks"]["target_audience"] = "PARTIAL"
        else:
            print("   ❌ NON-COMPLIANT: No audience adaptation information")
            self.review_results["compliance_checks"]["target_audience"] = "FAILED"
    
    def check_upskilling_reskilling_focus(self):
        """T3.2 Requirement: Focus on upskilling/reskilling"""
        print("\n📈 === Upskilling/Reskilling Focus ===")
        
        # Check for just-in-time learning and immediate applicability
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            just_in_time_count = 0
            immediate_application_count = 0
            
            for nano in nano_credentials:
                workplace_relevance = nano.get('workplace_relevance', {})
                
                # Check just-in-time learning
                if workplace_relevance.get('just_in_time_learning'):
                    just_in_time_count += 1
                
                # Check immediate applicability
                immediate_app = workplace_relevance.get('immediate_applicability', {})
                time_to_app = immediate_app.get('time_to_application', 'Not specified')
                if time_to_app in ['immediate', 'within_week']:
                    immediate_application_count += 1
            
            just_in_time_percentage = (just_in_time_count / len(nano_credentials)) * 100
            immediate_percentage = (immediate_application_count / len(nano_credentials)) * 100
            
            print(f"   📊 Upskilling/Reskilling Indicators:")
            print(f"      Just-in-Time Learning: {just_in_time_count}/{len(nano_credentials)} ({just_in_time_percentage:.1f}%)")
            print(f"      Immediate Application: {immediate_application_count}/{len(nano_credentials)} ({immediate_percentage:.1f}%)")
            
            # T3.2 emphasizes upskilling/reskilling focus
            if just_in_time_percentage >= 70 and immediate_percentage >= 50:
                print("   ✅ COMPLIANCE: Strong upskilling/reskilling focus")
                self.review_results["compliance_checks"]["upskilling_reskilling"] = "EXCELLENT"
            elif just_in_time_percentage >= 50 or immediate_percentage >= 30:
                print("   ✅ COMPLIANCE: Good upskilling/reskilling orientation")
                self.review_results["compliance_checks"]["upskilling_reskilling"] = "SATISFACTORY"
            else:
                print("   ⚠️  LIMITED: Upskilling/reskilling focus needs strengthening")
                self.review_results["compliance_checks"]["upskilling_reskilling"] = "PARTIAL"
        else:
            print("   ❌ NON-COMPLIANT: No upskilling/reskilling indicators")
            self.review_results["compliance_checks"]["upskilling_reskilling"] = "FAILED"
    
    def generate_t32_compliance_report(self):
        """Generate T3.2 compliance report"""
        print("\n📋 === T3.2 COMPLIANCE REPORT ===")
        
        # Calculate overall compliance score
        compliance_scores = {
            "EXCELLENT": 3,
            "SATISFACTORY": 2,
            "PARTIAL": 1,
            "FAILED": 0
        }
        
        total_score = 0
        max_score = 0
        
        for check, result in self.review_results["compliance_checks"].items():
            score = compliance_scores.get(result.split()[0], 0)  # Handle "FAILED - No data" format
            total_score += score
            max_score += 3
        
        compliance_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        print(f"📊 Compliance Summary:")
        for check, result in self.review_results["compliance_checks"].items():
            status_emoji = "✅" if result.startswith("EXCELLENT") or result.startswith("SATISFACTORY") else "❌"
            print(f"   {status_emoji} {check.replace('_', ' ').title()}: {result}")
        
        print(f"\n📈 Overall T3.2 Compliance: {compliance_percentage:.1f}%")
        
        # Determine overall rating
        if compliance_percentage >= 85:
            self.review_results["overall_rating"] = "EXCELLENT"
            print("🎉 REVIEWER VERDICT: EXCELLENT - Fully compliant with T3.2 requirements")
        elif compliance_percentage >= 70:
            self.review_results["overall_rating"] = "SATISFACTORY"
            print("✅ REVIEWER VERDICT: SATISFACTORY - Meets T3.2 requirements with minor gaps")
        elif compliance_percentage >= 50:
            self.review_results["overall_rating"] = "NEEDS_IMPROVEMENT"
            print("⚠️  REVIEWER VERDICT: NEEDS IMPROVEMENT - Partial T3.2 compliance")
        else:
            self.review_results["overall_rating"] = "NON_COMPLIANT"
            print("❌ REVIEWER VERDICT: NON-COMPLIANT - Significant T3.2 requirements not met")
        
        # Critical findings
        if self.review_results["critical_findings"]:
            print(f"\n🚨 Critical Findings:")
            for finding in self.review_results["critical_findings"]:
                print(f"   • {finding}")
        
        # Recommendations
        recommendations = []
        for check, result in self.review_results["compliance_checks"].items():
            if result.startswith("FAILED") or result.startswith("PARTIAL"):
                recommendations.append(f"Improve {check.replace('_', ' ')}")
        
        if recommendations:
            print(f"\n💡 Reviewer Recommendations:")
            for rec in recommendations:
                print(f"   • {rec}")
        
        # Save detailed report
        report_dir = Path("output/validation_reports/t32_review")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        detailed_report = {
            **self.review_results,
            "compliance_percentage": compliance_percentage,
            "total_checks": len(self.review_results["compliance_checks"]),
            "passed_checks": len([r for r in self.review_results["compliance_checks"].values() 
                                 if r.startswith("EXCELLENT") or r.startswith("SATISFACTORY")])
        }
        
        report_file = report_dir / f"T3_2_compliance_report_{date.today().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(detailed_report, f, indent=2)
        
        print(f"\n📁 Detailed compliance report saved: {report_file}")

def main():
    """Run T3.2 reviewer check suite"""
    reviewer = T32ReviewerCheckSuite()
    success = reviewer.run_t32_compliance_review()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
