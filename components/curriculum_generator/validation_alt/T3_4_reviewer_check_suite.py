#!/usr/bin/env python3
"""
T3.4 Reviewer Check Suite - Micro-Credentials & Certifications
EU Project Reviewer Validation for Task 3.4 Deliverable

TASK T3.4 OBJECTIVES:
- Design Digital Sustainability Skills certifications for each programme
- Link certifications to specific job roles
- Create individual certifications for shorter courses
- Assign micro-credentials to each learning outcome
- Develop stackable system of micro-credentials
- Create outcomes-based qualifications framework
- Implement ECVET and ECTS principles
- Reference qualifications to NQFs and EQF
- Ensure coherent system linking job roles, skills, certifications
- Achieve national and European recognition
"""

import json
import sys
import re
from pathlib import Path
from datetime import date

class T34ReviewerCheckSuite:
    """
    Reviewer validation suite for T3.4 deliverable compliance
    """
    
    def __init__(self, input_dir="input"):
        self.input_dir = Path(input_dir)
        self.review_results = {
            "review_date": date.today().isoformat(),
            "reviewer": "EU_Project_Reviewer",
            "task": "T3.4_Micro_Credentials_Certifications",
            "deliverable": "Output_6_EU_Recognised_Micro_Credentials_Certifications",
            "compliance_checks": {},
            "critical_findings": [],
            "recommendations": [],
            "overall_rating": "PENDING"
        }
        
    def run_t34_compliance_review(self):
        """Run comprehensive T3.4 compliance review"""
        print("🔍 === T3.4 REVIEWER CHECK SUITE ===")
        print("📋 Task: Micro-Credentials & Certifications Design")
        print("🎯 Deliverable: EU Recognised Micro-Credentials & Certifications")
        print(f"📅 Review Date: {date.today().isoformat()}")
        
        # Core T3.4 Requirements Validation
        self.check_certification_design()              # Digital sustainability skills certifications
        self.check_job_role_linking()                 # Link to specific job roles
        self.check_micro_credential_assignment()      # Micro-credentials per learning outcome
        self.check_stackable_system()                 # Stackable micro-credentials system
        self.check_outcomes_based_framework()         # Outcomes-based qualifications framework
        self.check_ects_ecvet_implementation()        # ECTS and ECVET principles
        self.check_nqf_eqf_referencing()             # NQF and EQF referencing
        self.check_coherent_system_integration()      # Coherent system integration
        self.check_recognition_compliance()           # Recognition standards compliance
        self.check_eu_framework_alignment()           # EU micro-credentials framework alignment
        
        # Generate compliance report
        self.generate_t34_compliance_report()
        
        return self.review_results["overall_rating"] in ["EXCELLENT", "SATISFACTORY"]
    
    def check_certification_design(self):
        """T3.4 Requirement: Digital Sustainability Skills certifications design"""
        print("\n🏆 === Certification Design Implementation ===")
        
        # Check for certification structure in nano credentials
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if not nano_file.exists():
            self.review_results["critical_findings"].append("CRITICAL: No nano credentials for certification analysis")
            self.review_results["compliance_checks"]["certification_design"] = "FAILED - No data"
            return
        
        with open(nano_file, 'r') as f:
            nano_data = json.load(f)
            if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                nano_credentials = nano_data['nano_credentials']
            else:
                nano_credentials = nano_data
        
        # Analyze certification-related elements
        certification_elements = {
            "awarding_body": 0,
            "quality_assurance": 0,
            "grade_achieved": 0,
            "supervision_verification": 0
        }
        
        digital_sustainability_focus = 0
        
        for nano in nano_credentials:
            # Check certification elements
            if 'awarding_body' in nano:
                certification_elements["awarding_body"] += 1
            
            if 'quality_assurance' in nano:
                certification_elements["quality_assurance"] += 1
            
            optional_elements = nano.get('optional_elements', {})
            if 'grade_achieved' in optional_elements:
                certification_elements["grade_achieved"] += 1
            
            if 'supervision_verification' in optional_elements:
                certification_elements["supervision_verification"] += 1
            
            # Check for digital sustainability focus
            learning_outcome = nano.get('learning_outcome', {})
            statement = learning_outcome.get('statement', '').lower()
            if any(term in statement for term in ['sustainability', 'digital', 'green', 'environment', 'carbon']):
                digital_sustainability_focus += 1
        
        total_nanos = len(nano_credentials)
        ds_percentage = (digital_sustainability_focus / total_nanos) * 100
        
        print(f"   📊 Certification Design Analysis:")
        print(f"      Total Credentials: {total_nanos}")
        print(f"      Digital Sustainability Focus: {digital_sustainability_focus} ({ds_percentage:.1f}%)")
        print(f"      Certification Elements:")
        for element, count in certification_elements.items():
            percentage = (count / total_nanos) * 100
            print(f"         {element.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        
        # Compliance assessment
        if ds_percentage >= 80 and all(count > 0 for count in certification_elements.values()):
            print("   ✅ COMPLIANCE: Comprehensive certification design for digital sustainability")
            self.review_results["compliance_checks"]["certification_design"] = "EXCELLENT"
        elif ds_percentage >= 60 and sum(certification_elements.values()) >= total_nanos * 2:
            print("   ✅ COMPLIANCE: Good certification design implementation")
            self.review_results["compliance_checks"]["certification_design"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient certification design elements")
            self.review_results["compliance_checks"]["certification_design"] = "FAILED"
    
    def check_job_role_linking(self):
        """T3.4 Requirement: Link certifications to specific job roles"""
        print("\n💼 === Job Role Linking Implementation ===")
        
        # Check for job role mappings in relationships or configurations
        roles_file = self.input_dir / "roles" / "roles.json"
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        
        job_role_mappings = 0
        
        if roles_file.exists():
            with open(roles_file, 'r') as f:
                roles_data = json.load(f)
            
            print(f"   📊 Available Job Roles: {len(roles_data)}")
            
            # Show sample roles
            for i, role in enumerate(roles_data[:3]):
                print(f"      Role {i+1}: {role.get('name', 'Unknown')}")
                print(f"         Skills: {len(role.get('skills', []))}")
                print(f"         EQF Level: {role.get('target_eqf_level', 'Not specified')}")
        
        # Check nano credentials for workplace context (job role indicators)
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            for nano in nano_credentials:
                workplace_relevance = nano.get('workplace_relevance', {})
                immediate_app = workplace_relevance.get('immediate_applicability', {})
                contexts = immediate_app.get('application_contexts', [])
                
                if contexts:
                    job_role_mappings += 1
            
            mapping_percentage = (job_role_mappings / len(nano_credentials)) * 100
            
            print(f"   📊 Job Role Linking:")
            print(f"      Credentials with Workplace Context: {job_role_mappings}/{len(nano_credentials)} ({mapping_percentage:.1f}%)")
        
        # Compliance assessment
        role_count = len(roles_data) if roles_file.exists() else 0
        
        if role_count >= 5 and job_role_mappings >= len(nano_credentials) * 0.7:
            print("   ✅ COMPLIANCE: Strong job role linking implementation")
            self.review_results["compliance_checks"]["job_role_linking"] = "EXCELLENT"
        elif role_count >= 3 and job_role_mappings >= len(nano_credentials) * 0.5:
            print("   ✅ COMPLIANCE: Adequate job role linking")
            self.review_results["compliance_checks"]["job_role_linking"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient job role linking")
            self.review_results["compliance_checks"]["job_role_linking"] = "FAILED"
    
    def check_micro_credential_assignment(self):
        """T3.4 Requirement: Assign micro-credentials to each learning outcome"""
        print("\n🎯 === Micro-Credential Assignment per Learning Outcome ===")
        
        # Check relationship between learning outcomes and micro-credentials
        rel_file = self.input_dir / "relationships" / "nano_to_micro.json"
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        
        if not rel_file.exists():
            print("   ❌ NON-COMPLIANT: No relationship mappings found")
            self.review_results["compliance_checks"]["micro_credential_assignment"] = "FAILED"
            return
        
        with open(rel_file, 'r') as f:
            relationships = json.load(f)
        
        nano_to_micro = relationships.get('nano_to_micro_mapping', {})
        micro_to_nano = relationships.get('micro_to_nano_mapping', {})
        
        # Analyze assignment coverage
        total_nanos = len(nano_to_micro)
        total_micros = len(micro_to_nano)
        
        # Check for learning outcome specificity in nano credentials
        learning_outcome_specificity = 0
        
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            for nano in nano_credentials:
                learning_outcome = nano.get('learning_outcome', {})
                if isinstance(learning_outcome, dict) and 'statement' in learning_outcome:
                    learning_outcome_specificity += 1
        
        assignment_coverage = (learning_outcome_specificity / len(nano_credentials)) * 100 if nano_credentials else 0
        
        print(f"   📊 Assignment Analysis:")
        print(f"      Nano-to-Micro Mappings: {total_nanos}")
        print(f"      Micro-to-Nano Mappings: {total_micros}")
        print(f"      Learning Outcome Specificity: {learning_outcome_specificity}/{len(nano_credentials)} ({assignment_coverage:.1f}%)")
        
        # Check for one-to-one or one-to-many relationships
        assignment_patterns = {}
        for micro_id, mapping in micro_to_nano.items():
            nano_count = len(mapping.get('nano_credential_ids', []))
            pattern = f"1_micro_to_{nano_count}_nanos"
            assignment_patterns[pattern] = assignment_patterns.get(pattern, 0) + 1
        
        print(f"      Assignment Patterns: {assignment_patterns}")
        
        # Compliance assessment
        if assignment_coverage >= 90 and total_nanos == len(nano_credentials):
            print("   ✅ COMPLIANCE: Complete micro-credential assignment per learning outcome")
            self.review_results["compliance_checks"]["micro_credential_assignment"] = "EXCELLENT"
        elif assignment_coverage >= 75 and total_nanos >= len(nano_credentials) * 0.8:
            print("   ✅ COMPLIANCE: Good micro-credential assignment coverage")
            self.review_results["compliance_checks"]["micro_credential_assignment"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Incomplete micro-credential assignment")
            self.review_results["compliance_checks"]["micro_credential_assignment"] = "FAILED"
    
    def check_stackable_system(self):
        """T3.4 Requirement: Stackable system of micro-credentials"""
        print("\n📚 === Stackable Micro-Credentials System ===")
        
        # Check for stackability elements in nano credentials
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if not nano_file.exists():
            self.review_results["compliance_checks"]["stackable_system"] = "FAILED - No data"
            return
        
        with open(nano_file, 'r') as f:
            nano_data = json.load(f)
            if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                nano_credentials = nano_data['nano_credentials']
            else:
                nano_credentials = nano_data
        
        # Analyze stackability implementation
        stackability_features = {
            "vertical_stacking": 0,
            "horizontal_stacking": 0,
            "dependency_graph": 0,
            "contribution_percentage": 0
        }
        
        for nano in nano_credentials:
            stackability = nano.get('stackability_elements', {})
            
            if 'vertical_stacking' in stackability:
                stackability_features["vertical_stacking"] += 1
            
            if 'horizontal_stacking' in stackability:
                stackability_features["horizontal_stacking"] += 1
            
            if 'dependency_graph' in stackability:
                stackability_features["dependency_graph"] += 1
            
            # Check for contribution percentages (mathematical stacking)
            vertical = stackability.get('vertical_stacking', {})
            if 'contribution_percentage' in vertical:
                stackability_features["contribution_percentage"] += 1
        
        total_nanos = len(nano_credentials)
        
        print(f"   📊 Stackability Analysis:")
        for feature, count in stackability_features.items():
            percentage = (count / total_nanos) * 100
            print(f"      {feature.replace('_', ' ').title()}: {count}/{total_nanos} ({percentage:.1f}%)")
        
        # Check for stacking rules in relationships
        rel_file = self.input_dir / "relationships" / "nano_to_micro.json"
        stacking_rules_defined = False
        
        if rel_file.exists():
            with open(rel_file, 'r') as f:
                relationships = json.load(f)
            
            stacking_rules = relationships.get('stacking_rules', {})
            stacking_rules_defined = bool(stacking_rules)
            
            print(f"      Stacking Rules Defined: {'✅' if stacking_rules_defined else '❌'}")
        
        # Compliance assessment
        avg_stackability = sum(stackability_features.values()) / len(stackability_features)
        stackability_percentage = (avg_stackability / total_nanos) * 100
        
        if stackability_percentage >= 80 and stacking_rules_defined:
            print("   ✅ COMPLIANCE: Comprehensive stackable micro-credentials system")
            self.review_results["compliance_checks"]["stackable_system"] = "EXCELLENT"
        elif stackability_percentage >= 60 or stacking_rules_defined:
            print("   ✅ COMPLIANCE: Good stackability implementation")
            self.review_results["compliance_checks"]["stackable_system"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient stackability features")
            self.review_results["compliance_checks"]["stackable_system"] = "FAILED"
    
    def check_outcomes_based_framework(self):
        """T3.4 Requirement: Outcomes-based qualifications framework"""
        print("\n📊 === Outcomes-Based Qualifications Framework ===")
        
        # Check for learning outcome structure and qualification mapping
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if not nano_file.exists():
            self.review_results["compliance_checks"]["outcomes_framework"] = "FAILED - No data"
            return
        
        with open(nano_file, 'r') as f:
            nano_data = json.load(f)
            if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                nano_credentials = nano_data['nano_credentials']
            else:
                nano_credentials = nano_data
        
        # Analyze outcomes-based structure
        outcomes_analysis = {
            "bloom_taxonomy": 0,
            "action_verbs": 0,
            "measurable_outcomes": 0,
            "assessment_alignment": 0
        }
        
        bloom_levels = set()
        
        for nano in nano_credentials:
            learning_outcome = nano.get('learning_outcome', {})
            
            # Check Bloom's taxonomy implementation
            bloom_level = learning_outcome.get('bloom_taxonomy_level')
            if bloom_level:
                outcomes_analysis["bloom_taxonomy"] += 1
                bloom_levels.add(bloom_level)
            
            # Check action verbs
            action_verb = learning_outcome.get('action_verb')
            if action_verb:
                outcomes_analysis["action_verbs"] += 1
            
            # Check measurable outcome statements
            statement = learning_outcome.get('statement', '')
            if statement and len(statement) > 10:  # Basic measurability check
                outcomes_analysis["measurable_outcomes"] += 1
            
            # Check assessment alignment
            assessment = nano.get('assessment_type', {})
            if assessment and isinstance(assessment, dict):
                outcomes_analysis["assessment_alignment"] += 1
        
        total_nanos = len(nano_credentials)
        
        print(f"   📊 Outcomes-Based Framework Analysis:")
        for feature, count in outcomes_analysis.items():
            percentage = (count / total_nanos) * 100
            print(f"      {feature.replace('_', ' ').title()}: {count}/{total_nanos} ({percentage:.1f}%)")
        
        print(f"      Bloom's Taxonomy Levels Used: {list(bloom_levels)}")
        print(f"      Taxonomy Diversity: {len(bloom_levels)}/6 levels")
        
        # Check for qualification types in configuration
        config_file = self.input_dir / "config" / "three_tier_config.yaml"
        qualification_types_defined = False
        
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                module_config = config.get('module_config', {})
                qualification_types = module_config.get('qualification_types', {})
                qualification_types_defined = bool(qualification_types)
                
                print(f"      Qualification Types Defined: {'✅' if qualification_types_defined else '❌'}")
                
                if qualification_types:
                    print(f"      Available Qualifications: {list(qualification_types.keys())}")
                
            except ImportError:
                print("      ⚠️  YAML not available for config analysis")
        
        # Compliance assessment
        avg_outcomes_compliance = sum(outcomes_analysis.values()) / len(outcomes_analysis)
        outcomes_percentage = (avg_outcomes_compliance / total_nanos) * 100
        
        if outcomes_percentage >= 90 and len(bloom_levels) >= 4 and qualification_types_defined:
            print("   ✅ COMPLIANCE: Comprehensive outcomes-based qualifications framework")
            self.review_results["compliance_checks"]["outcomes_framework"] = "EXCELLENT"
        elif outcomes_percentage >= 70 and len(bloom_levels) >= 3:
            print("   ✅ COMPLIANCE: Good outcomes-based framework implementation")
            self.review_results["compliance_checks"]["outcomes_framework"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient outcomes-based framework")
            self.review_results["compliance_checks"]["outcomes_framework"] = "FAILED"
    
    def check_ects_ecvet_implementation(self):
        """T3.4 Requirement: ECTS and ECVET principles implementation"""
        print("\n💳 === ECTS and ECVET Implementation ===")
        
        # Check ECTS implementation
        micro_file = self.input_dir / "micro_credentials.json"
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        
        ects_implementation = {
            "ects_present": False,
            "ects_range_valid": False,
            "ects_coherent": False,
            "workload_defined": False
        }
        
        if micro_file.exists():
            with open(micro_file, 'r') as f:
                micro_credentials = json.load(f)
            
            # Check ECTS implementation in micro credentials
            ects_values = []
            for micro in micro_credentials:
                ects = micro.get('ects_points')
                if ects is not None:
                    ects_values.append(float(ects))
            
            if ects_values:
                ects_implementation["ects_present"] = True
                
                # Check valid ECTS range (should be reasonable values)
                if all(0.1 <= ects <= 60 for ects in ects_values):
                    ects_implementation["ects_range_valid"] = True
        
        # Check nano credentials for detailed ECTS and workload
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Check for notional workload (ECVET principle)
            workload_count = 0
            nano_ects_total = 0
            
            for nano in nano_credentials:
                notional_workload = nano.get('notional_workload', {})
                if notional_workload and isinstance(notional_workload, dict):
                    workload_count += 1
                
                nano_ects = nano.get('ects_credits', 0)
                nano_ects_total += nano_ects
            
            if workload_count > 0:
                ects_implementation["workload_defined"] = True
            
            # Check ECTS coherence between micro and nano
            micro_ects_total = sum(ects_values) if ects_values else 0
            if abs(nano_ects_total - micro_ects_total) < 2.0:  # 2 ECTS tolerance
                ects_implementation["ects_coherent"] = True
        
        print(f"   📊 ECTS/ECVET Implementation:")
        for feature, status in ects_implementation.items():
            status_emoji = "✅" if status else "❌"
            print(f"      {status_emoji} {feature.replace('_', ' ').title()}")
        
        # Additional ECVET checks
        ecvet_features = 0
        
        # Check for learning outcomes (ECVET requirement)
        if nano_file.exists() and nano_credentials:
            learning_outcomes_count = sum(1 for nano in nano_credentials if 'learning_outcome' in nano)
            if learning_outcomes_count == len(nano_credentials):
                ecvet_features += 1
                print(f"      ✅ Learning Outcomes Defined: {learning_outcomes_count}/{len(nano_credentials)}")
        
        # Check for assessment criteria (ECVET requirement)
        assessment_count = sum(1 for nano in nano_credentials if 'assessment_type' in nano) if nano_file.exists() and nano_credentials else 0
        if assessment_count > 0:
            ecvet_features += 1
            print(f"      ✅ Assessment Criteria: {assessment_count}/{len(nano_credentials) if nano_credentials else 0}")
        
        # Compliance assessment
        ects_score = sum(ects_implementation.values())
        
        if ects_score >= 3 and ecvet_features >= 2:
            print("   ✅ COMPLIANCE: Comprehensive ECTS and ECVET implementation")
            self.review_results["compliance_checks"]["ects_ecvet"] = "EXCELLENT"
        elif ects_score >= 2 and ecvet_features >= 1:
            print("   ✅ COMPLIANCE: Good ECTS and ECVET implementation")
            self.review_results["compliance_checks"]["ects_ecvet"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient ECTS and ECVET implementation")
            self.review_results["compliance_checks"]["ects_ecvet"] = "FAILED"
    
    def check_nqf_eqf_referencing(self):
        """T3.4 Requirement: Reference qualifications to NQFs and EQF"""
        print("\n🏛️ === NQF and EQF Referencing ===")
        
        # Check EQF referencing in credentials
        micro_file = self.input_dir / "micro_credentials.json"
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        
        eqf_referencing = {
            "eqf_levels_present": False,
            "eqf_range_valid": False,
            "eqf_consistent": False,
            "three_tier_alignment": False
        }
        
        if micro_file.exists():
            with open(micro_file, 'r') as f:
                micro_credentials = json.load(f)
            
            # Check EQF levels in micro credentials
            eqf_levels = []
            for micro in micro_credentials:
                eqf_level = micro.get('eqf_level')
                if eqf_level is not None:
                    eqf_levels.append(eqf_level)
            
            if eqf_levels:
                eqf_referencing["eqf_levels_present"] = True
                
                # Check valid EQF range (1-8)
                if all(1 <= level <= 8 for level in eqf_levels):
                    eqf_referencing["eqf_range_valid"] = True
                
                # Check consistency (not too much variation)
                eqf_range = max(eqf_levels) - min(eqf_levels)
                if eqf_range <= 4:  # Reasonable range
                    eqf_referencing["eqf_consistent"] = True
        
        # Check three-tier framework alignment
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Check for EQF alignment across tiers
            three_tier_alignment_count = 0
            
            for nano in nano_credentials:
                three_tier_elements = nano.get('three_tier_framework_elements', {})
                parent_micro = three_tier_elements.get('parent_micro_credential', {})
                
                if parent_micro:
                    three_tier_alignment_count += 1
            
            if three_tier_alignment_count > 0:
                eqf_referencing["three_tier_alignment"] = True
        
        print(f"   📊 EQF/NQF Referencing:")
        for feature, status in eqf_referencing.items():
            status_emoji = "✅" if status else "❌"
            print(f"      {status_emoji} {feature.replace('_', ' ').title()}")
        
        # Check for specific EQF levels covered (T3.2 requires 4-8)
        if micro_file.exists() and eqf_levels:
            covered_levels = set(eqf_levels)
            required_levels = {4, 5, 6, 7, 8}
            coverage = len(covered_levels.intersection(required_levels))
            
            print(f"      EQF Levels Covered: {sorted(covered_levels)}")
            print(f"      T3.2 Compliance (4-8): {coverage}/5 levels")
        
        # Compliance assessment
        eqf_score = sum(eqf_referencing.values())
        
        if eqf_score >= 3 and coverage >= 4:
            print("   ✅ COMPLIANCE: Comprehensive EQF/NQF referencing")
            self.review_results["compliance_checks"]["nqf_eqf_referencing"] = "EXCELLENT"
        elif eqf_score >= 2 and coverage >= 3:
            print("   ✅ COMPLIANCE: Good EQF/NQF referencing")
            self.review_results["compliance_checks"]["nqf_eqf_referencing"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient EQF/NQF referencing")
            self.review_results["compliance_checks"]["nqf_eqf_referencing"] = "FAILED"
    
    def check_coherent_system_integration(self):
        """T3.4 Requirement: Coherent system linking job roles, skills, certifications"""
        print("\n🔗 === Coherent System Integration ===")
        
        # Check for integration between all system components
        integration_components = {
            "job_roles": False,
            "skills_mapping": False,
            "certifications": False,
            "micro_credentials": False,
            "curricula": False,
            "learning_outcomes": False
        }
        
        # Check job roles
        roles_file = self.input_dir / "roles" / "roles.json"
        if roles_file.exists():
            integration_components["job_roles"] = True
        
        # Check skills mapping (in nano credentials workplace relevance)
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Check for skills mapping
            skills_mapped = 0
            certifications_present = 0
            learning_outcomes_present = 0
            
            for nano in nano_credentials:
                # Skills mapping through workplace relevance
                workplace_relevance = nano.get('workplace_relevance', {})
                if workplace_relevance:
                    skills_mapped += 1
                
                # Certifications through awarding body
                if nano.get('awarding_body'):
                    certifications_present += 1
                
                # Learning outcomes
                learning_outcome = nano.get('learning_outcome', {})
                if learning_outcome:
                    learning_outcomes_present += 1
            
            total_nanos = len(nano_credentials)
            
            if skills_mapped > 0:
                integration_components["skills_mapping"] = True
            if certifications_present > 0:
                integration_components["certifications"] = True
            if learning_outcomes_present == total_nanos:
                integration_components["learning_outcomes"] = True
        
        # Check micro-credentials
        micro_file = self.input_dir / "micro_credentials.json"
        if micro_file.exists():
            integration_components["micro_credentials"] = True
        
        # Check curricula (modules)
        modules_file = self.input_dir / "modules" / "modules.json"
        if modules_file.exists():
            integration_components["curricula"] = True
        
        # Check relationships (key integration indicator)
        rel_file = self.input_dir / "relationships" / "nano_to_micro.json"
        relationships_present = rel_file.exists()
        
        print(f"   📊 System Integration Components:")
        for component, present in integration_components.items():
            status_emoji = "✅" if present else "❌"
            print(f"      {status_emoji} {component.replace('_', ' ').title()}")
        
        print(f"      ✅ Cross-Tier Relationships: {'✅' if relationships_present else '❌'}")
        
        # Check for mapping completeness
        if nano_file.exists():
            mapping_stats = {
                "skills_coverage": (skills_mapped / total_nanos) * 100,
                "certification_coverage": (certifications_present / total_nanos) * 100,
                "learning_outcome_coverage": (learning_outcomes_present / total_nanos) * 100
            }
            
            print(f"   📊 Integration Coverage:")
            for stat, percentage in mapping_stats.items():
                print(f"      {stat.replace('_', ' ').title()}: {percentage:.1f}%")
        
        # Compliance assessment
        integration_score = sum(integration_components.values())
        total_components = len(integration_components)
        
        if integration_score >= 5 and relationships_present:
            print("   ✅ COMPLIANCE: Comprehensive coherent system integration")
            self.review_results["compliance_checks"]["coherent_system"] = "EXCELLENT"
        elif integration_score >= 4 and relationships_present:
            print("   ✅ COMPLIANCE: Good system integration")
            self.review_results["compliance_checks"]["coherent_system"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient system integration")
            self.review_results["compliance_checks"]["coherent_system"] = "FAILED"
    
    def check_recognition_compliance(self):
        """T3.4 Requirement: Recognition standards compliance"""
        print("\n🏅 === Recognition Standards Compliance ===")
        
        # Check for recognition-enabling features
        recognition_features = {
            "institutional_validation": False,
            "quality_assurance": False,
            "awarding_body_defined": False,
            "assessment_standards": False,
            "transparency_elements": False
        }
        
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if nano_file.exists():
            with open(nano_file, 'r') as f:
                nano_data = json.load(f)
                if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                    nano_credentials = nano_data['nano_credentials']
                else:
                    nano_credentials = nano_data
            
            # Analyze recognition features
            institutional_validation_count = 0
            quality_assurance_count = 0
            awarding_body_count = 0
            assessment_standards_count = 0
            transparency_count = 0
            
            for nano in nano_credentials:
                # Institutional validation
                validation_status = nano.get('validation_status')
                if validation_status:
                    institutional_validation_count += 1
                
                # Quality assurance
                qa = nano.get('quality_assurance')
                if qa and qa != 'TBD':
                    quality_assurance_count += 1
                
                # Awarding body
                awarding_body = nano.get('awarding_body')
                if awarding_body and isinstance(awarding_body, list) and awarding_body:
                    awarding_body_count += 1
                
                # Assessment standards
                assessment = nano.get('assessment_type', {})
                if assessment and isinstance(assessment, dict):
                    assessment_standards_count += 1
                
                # Transparency (title, learning outcomes, ECTS)
                if (nano.get('title') and 
                    nano.get('learning_outcome') and 
                    nano.get('ects_credits')):
                    transparency_count += 1
            
            total_nanos = len(nano_credentials)
            
            # Determine feature presence
            if institutional_validation_count > 0:
                recognition_features["institutional_validation"] = True
            if quality_assurance_count >= total_nanos * 0.8:
                recognition_features["quality_assurance"] = True
            if awarding_body_count >= total_nanos * 0.8:
                recognition_features["awarding_body_defined"] = True
            if assessment_standards_count >= total_nanos * 0.8:
                recognition_features["assessment_standards"] = True
            if transparency_count >= total_nanos * 0.9:
                recognition_features["transparency_elements"] = True
            
            print(f"   📊 Recognition Feature Coverage:")
            for feature, present in recognition_features.items():
                status_emoji = "✅" if present else "❌"
                feature_name = feature.replace('_', ' ').title()
                print(f"      {status_emoji} {feature_name}")
        
        # Check for EU micro-credentials framework compliance
        eu_compliance_indicators = 0
        
        # Check for issuer location (EU requirement)
        eu_issuers = 0
        for nano in nano_credentials:
            issuer_location = nano.get('issuer_location', [])
            if isinstance(issuer_location, list) and any('EU' in loc or 'Europe' in loc for loc in issuer_location):
                eu_issuers += 1
        
        if eu_issuers > 0:
            eu_compliance_indicators += 1
            print(f"      ✅ EU Issuer Location: {eu_issuers}/{total_nanos}")
        
        # Check for date of issuing (EU requirement)
        dates_present = sum(1 for nano in nano_credentials if nano.get('date_of_issuing'))
        if dates_present >= total_nanos * 0.8:
            eu_compliance_indicators += 1
            print(f"      ✅ Date of Issuing: {dates_present}/{total_nanos}")
        
        # Compliance assessment
        recognition_score = sum(recognition_features.values())
        
        if recognition_score >= 4 and eu_compliance_indicators >= 2:
            print("   ✅ COMPLIANCE: Strong recognition standards compliance")
            self.review_results["compliance_checks"]["recognition_compliance"] = "EXCELLENT"
        elif recognition_score >= 3 and eu_compliance_indicators >= 1:
            print("   ✅ COMPLIANCE: Good recognition standards")
            self.review_results["compliance_checks"]["recognition_compliance"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient recognition standards")
            self.review_results["compliance_checks"]["recognition_compliance"] = "FAILED"
    
    def check_eu_framework_alignment(self):
        """T3.4 Requirement: EU micro-credentials framework alignment"""
        print("\n🇪🇺 === EU Micro-Credentials Framework Alignment ===")
        
        # Check compliance with EU Council Recommendation 2022/C 243/02
        eu_mandatory_elements = [
            "learner_identification",
            "title", 
            "issuer_location",
            "awarding_body",
            "date_of_issuing",
            "learning_outcome",
            "ects_credits",
            "notional_workload",
            "assessment_type",
            "quality_assurance",
            "participation_form"
        ]
        
        nano_file = self.input_dir / "nano_credentials" / "nano_credentials_spec_compliant.json"
        if not nano_file.exists():
            self.review_results["compliance_checks"]["eu_framework_alignment"] = "FAILED - No data"
            return
        
        with open(nano_file, 'r') as f:
            nano_data = json.load(f)
            if isinstance(nano_data, dict) and 'nano_credentials' in nano_data:
                nano_credentials = nano_data['nano_credentials']
            else:
                nano_credentials = nano_data
        
        # Check EU mandatory elements compliance
        eu_compliance = {}
        
        for element in eu_mandatory_elements:
            compliant_count = 0
            for nano in nano_credentials:
                if element in nano and nano[element] is not None:
                    compliant_count += 1
            
            compliance_rate = (compliant_count / len(nano_credentials)) * 100
            eu_compliance[element] = compliance_rate
        
        print(f"   📊 EU Mandatory Elements Compliance:")
        for element, rate in eu_compliance.items():
            status_emoji = "✅" if rate >= 80 else "⚠️" if rate >= 60 else "❌"
            print(f"      {status_emoji} {element.replace('_', ' ').title()}: {rate:.1f}%")
        
        # Check for nano-credentials specific enhancements
        nano_enhancements = {
            "three_tier_framework_elements": 0,
            "stackability_elements": 0,
            "action_mapping_elements": 0,
            "workplace_relevance": 0
        }
        
        for nano in nano_credentials:
            for enhancement in nano_enhancements:
                if enhancement in nano:
                    nano_enhancements[enhancement] += 1
        
        print(f"   📊 Nano-Credentials Enhancements:")
        for enhancement, count in nano_enhancements.items():
            percentage = (count / len(nano_credentials)) * 100
            status_emoji = "✅" if percentage >= 80 else "⚠️" if percentage >= 60 else "❌"
            print(f"      {status_emoji} {enhancement.replace('_', ' ').title()}: {percentage:.1f}%")
        
        # Overall EU framework compliance
        avg_compliance = sum(eu_compliance.values()) / len(eu_compliance)
        avg_enhancements = sum(nano_enhancements.values()) / len(nano_enhancements) / len(nano_credentials) * 100
        
        print(f"   📈 Overall EU Compliance: {avg_compliance:.1f}%")
        print(f"   📈 Enhancement Implementation: {avg_enhancements:.1f}%")
        
        # Compliance assessment
        if avg_compliance >= 90 and avg_enhancements >= 80:
            print("   ✅ COMPLIANCE: Excellent EU framework alignment with enhancements")
            self.review_results["compliance_checks"]["eu_framework_alignment"] = "EXCELLENT"
        elif avg_compliance >= 80 and avg_enhancements >= 60:
            print("   ✅ COMPLIANCE: Good EU framework alignment")
            self.review_results["compliance_checks"]["eu_framework_alignment"] = "SATISFACTORY"
        else:
            print("   ❌ NON-COMPLIANT: Insufficient EU framework alignment")
            self.review_results["compliance_checks"]["eu_framework_alignment"] = "FAILED"
    
    def generate_t34_compliance_report(self):
        """Generate T3.4 compliance report"""
        print("\n📋 === T3.4 COMPLIANCE REPORT ===")
        
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
            score = compliance_scores.get(result.split()[0], 0)
            total_score += score
            max_score += 3
        
        compliance_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        print(f"📊 T3.4 Compliance Summary:")
        for check, result in self.review_results["compliance_checks"].items():
            status_emoji = "✅" if result.startswith("EXCELLENT") or result.startswith("SATISFACTORY") else "❌"
            print(f"   {status_emoji} {check.replace('_', ' ').title()}: {result}")
        
        print(f"\n📈 Overall T3.4 Compliance: {compliance_percentage:.1f}%")
        
        # Determine overall rating
        if compliance_percentage >= 85:
            self.review_results["overall_rating"] = "EXCELLENT"
            print("🎉 REVIEWER VERDICT: EXCELLENT - Fully compliant with T3.4 requirements")
            print("    Framework exceeds EU micro-credentials standards")
        elif compliance_percentage >= 70:
            self.review_results["overall_rating"] = "SATISFACTORY"
            print("✅ REVIEWER VERDICT: SATISFACTORY - Meets T3.4 requirements")
            print("    Framework aligns well with EU micro-credentials framework")
        elif compliance_percentage >= 50:
            self.review_results["overall_rating"] = "NEEDS_IMPROVEMENT"
            print("⚠️  REVIEWER VERDICT: NEEDS IMPROVEMENT - Partial T3.4 compliance")
            print("    Framework requires enhancements for full compliance")
        else:
            self.review_results["overall_rating"] = "NON_COMPLIANT"
            print("❌ REVIEWER VERDICT: NON-COMPLIANT - Significant T3.4 gaps")
            print("    Framework needs major improvements for EU recognition")
        
        # Critical findings
        if self.review_results["critical_findings"]:
            print(f"\n🚨 Critical Findings:")
            for finding in self.review_results["critical_findings"]:
                print(f"   • {finding}")
        
        # Recommendations
        recommendations = []
        for check, result in self.review_results["compliance_checks"].items():
            if result.startswith("FAILED") or result.startswith("PARTIAL"):
                recommendations.append(f"Enhance {check.replace('_', ' ')}")
        
        if recommendations:
            print(f"\n💡 Reviewer Recommendations:")
            for rec in recommendations:
                print(f"   • {rec}")
        
        # EU Recognition Assessment
        print(f"\n🇪🇺 EU Recognition Readiness:")
        if compliance_percentage >= 80:
            print("   🟢 HIGH - Ready for EU recognition processes")
        elif compliance_percentage >= 65:
            print("   🟡 MEDIUM - Minor improvements needed for EU recognition")
        else:
            print("   🔴 LOW - Significant work required for EU recognition")
        
        # Save detailed report
        report_dir = Path("output/validation_reports/t34_review")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        detailed_report = {
            **self.review_results,
            "compliance_percentage": compliance_percentage,
            "total_checks": len(self.review_results["compliance_checks"]),
            "passed_checks": len([r for r in self.review_results["compliance_checks"].values() 
                                 if r.startswith("EXCELLENT") or r.startswith("SATISFACTORY")]),
            "eu_recognition_readiness": "HIGH" if compliance_percentage >= 80 else "MEDIUM" if compliance_percentage >= 65 else "LOW"
        }
        
        report_file = report_dir / f"T3_4_compliance_report_{date.today().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(detailed_report, f, indent=2)
        
        print(f"\n📁 Detailed compliance report saved: {report_file}")

def main():
    """Run T3.4 reviewer check suite"""
    reviewer = T34ReviewerCheckSuite()
    success = reviewer.run_t34_compliance_review()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
