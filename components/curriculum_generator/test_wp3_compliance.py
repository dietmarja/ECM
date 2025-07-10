#!/usr/bin/env python3
# scripts/curriculum_generator/test_wp3_compliance.py
"""
Test WP3 Compliance - Generate professional-grade curricula following ChatGPT template
"""

import sys
import json
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Create roles.json for testing
roles_content = """[
  {
    "id": "DAN", 
    "name": "Data Analyst",
    "description": "Analyzes and visualizes data to drive sustainability insights",
    "main_area": "Data",
    "core_skills": ["data_analysis", "data_visualization", "sustainability_reporting"]
  }
]"""

with open(project_root / "roles.json", "w") as f:
    f.write(roles_content)

from scripts.curriculum_generator.components.wp3_compliant_generator import WP3CompliantGenerator
from scripts.curriculum_generator.components.enhanced_module_selector import EnhancedModuleSelector

def test_wp3_compliance():
    """Test WP3-compliant curriculum generation"""
    
    print("🎯 TESTING WP3-COMPLIANT CURRICULUM GENERATION")
    print("Following ChatGPT's revised outline template")
    print("=" * 70)
    
    # Initialize components
    module_selector = EnhancedModuleSelector())
    wp3_generator = WP3CompliantGenerator(project_root)
    
    # Test scenario: Data Analyst 1.5 ECTS (following ChatGPT template)
    role_id = "DAN"
    eqf_level = 5
    ects = 1.5
    topic = "Digital Sustainability"
    
    print(f"📋 Test Scenario: {role_id} EQF{eqf_level} {ects}ECTS")
    print(f"🎯 Following ChatGPT template structure")
    
    try:
        # Select modules
        selected_modules, _ = module_selector.select_modules_for_curriculum(
            role_id=role_id,
            topic=topic,
            eqf_level=eqf_level,
            ects=ects,
            min_score_threshold=0.2
        )
        
        print(f"   📦 Selected {len(selected_modules)} modules")
        
        # Generate WP3-compliant curriculum
        wp3_curriculum = wp3_generator.generate_wp3_compliant_curriculum(
            role_id=role_id,
            eqf_level=eqf_level,
            ects=ects,
            selected_modules=selected_modules,
            topic=topic
        )
        
        # Display key WP3 compliance features
        print(f"\n✅ WP3-COMPLIANT CURRICULUM GENERATED")
        print("-" * 50)
        
        metadata = wp3_curriculum['metadata']
        print(f"📋 Title: {metadata['title']}")
        print(f"🎓 EQF Level: {metadata['eqf_level']} ({metadata['total_study_hours']} study hours)")
        print(f"🧩 Modules: {metadata['module_count']} named modules")
        print(f"📜 Format: {metadata['credential_format']}")
        
        # Show modular structure
        print(f"\n📚 MODULAR STRUCTURE (Following ChatGPT Template)")
        print("-" * 50)
        modules = wp3_curriculum['modular_structure']
        
        for module in modules:
            print(f"   {module['module_number']}. {module['title']}")
            print(f"      📊 {module['study_hours']} hours | {module['ects_credits']} ECTS")
            print(f"      🎯 Outcomes: {len(module['learning_outcomes'])}")
            print(f"      🏅 Micro-credential: {module['micro_credential']}")
            print()
        
        # Show programme learning outcomes
        print(f"🎯 PROGRAMME LEARNING OUTCOMES (EQF-Aligned)")
        print("-" * 50)
        outcomes = wp3_curriculum['programme_learning_outcomes']
        print(f"   {outcomes['introduction']}")
        for i, outcome in enumerate(outcomes['specific_outcomes'][:3], 1):
            print(f"   {i}. {outcome}")
        
        # Show framework compliance
        print(f"\n🌐 FRAMEWORK MAPPING (Cross-Border Recognition)")
        print("-" * 50)
        framework = wp3_curriculum['framework_mapping']
        print(f"   📊 EQF Level {framework['eqf_alignment']['level']}: {framework['eqf_alignment']['descriptor'][:60]}...")
        print(f"   🔧 e-CF Competencies: {len(framework['e_cf_mapping']['competencies'])} mapped")
        print(f"   👥 ESCO Occupation: {framework['esco_mapping']['occupation_code']}")
        
        # Show assessment strategy
        print(f"\n📝 ASSESSMENT STRATEGY (Competency-Mapped)")
        print("-" * 50)
        assessment = wp3_curriculum['assessment_strategy']
        for component in assessment['components']:
            print(f"   📊 {component['component']}: {component['weight_percentage']}% - {component['description'][:50]}...")
        
        # Show stackability
        print(f"\n🧩 STACKABILITY & MICRO-CREDENTIALING")
        print("-" * 50)
        stack = wp3_curriculum['stackability_and_micro_credentialing']
        print(f"   🏅 Individual badges: {len(stack['micro_credentials']['individual_badges'])}")
        print(f"   📜 Certificate: {stack['micro_credentials']['certificate_completion']['name']}")
        print(f"   🔄 Progression: {stack['progression_pathway']['visual_map'][:60]}...")
        
        # Compliance verification
        print(f"\n🔍 WP3 COMPLIANCE VERIFICATION")
        print("-" * 50)
        compliance = wp3_curriculum['compliance_verification']
        print(f"   ✅ Overall Compliance: {compliance['overall_compliance']}")
        print(f"   📊 Compliance Score: {compliance['compliance_percentage']:.1f}%")
        
        if compliance['failed_criteria']:
            print(f"   ⚠️  Failed Criteria: {', '.join(compliance['failed_criteria'])}")
        else:
            print(f"   🎉 All WP3 criteria met!")
        
        # Compare with ChatGPT template
        print(f"\n🆚 CHATGPT TEMPLATE COMPLIANCE CHECK")
        print("-" * 50)
        
        template_checks = {
            "Named Modules": len(modules) >= 3 and all(m['title'] for m in modules),
            "ECTS Distribution": all(m['ects_credits'] > 0 for m in modules),
            "EQF Alignment": bool(framework['eqf_alignment']['descriptor']),
            "Framework Mapping": len(framework['e_cf_mapping']['competencies']) > 0,
            "Assessment Strategy": len(assessment['components']) >= 4,
            "Micro-Credentials": len(stack['micro_credentials']['individual_badges']) > 0,
            "Work-Based Learning": bool(wp3_curriculum['work_based_integration']),
            "Target Audiences": len(wp3_curriculum['target_audiences']) >= 3
        }
        
        passed_checks = sum(template_checks.values())
        total_checks = len(template_checks)
        
        for check_name, passed in template_checks.items():
            status = "✅ PASS" if passed else "❌ FAIL" 
            print(f"   {check_name}: {status}")
        
        print(f"\n🏆 FINAL ASSESSMENT")
        print("=" * 50)
        print(f"📊 ChatGPT Template Compliance: {passed_checks}/{total_checks} ({passed_checks/total_checks*100:.1f}%)")
        
        if passed_checks >= 7:
            print(f"🎉 SUCCESS: Professional-grade WP3-compliant curriculum!")
            print(f"💡 This addresses ChatGPT's specific criticisms:")
            print(f"   ✅ Named modules with specific content")
            print(f"   ✅ Proper ECTS distribution and study hours")
            print(f"   ✅ EQF descriptor alignment")
            print(f"   ✅ Framework mapping for recognition")
            print(f"   ✅ Competency-based assessment strategy")
            print(f"   ✅ Stackable micro-credentialing system")
            return True
        else:
            print(f"⚠️  NEEDS IMPROVEMENT: Still missing key WP3 elements")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_wp3_compliance()
    sys.exit(0 if success else 1)
