#!/usr/bin/env python3
# scripts/curriculum_generator/test_enhanced_fixes.py
"""
Test script for enhanced content specificity fixes
Tests the problematic DSC EQF7 180.0 ECTS scenario that was failing
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.curriculum_generator.components.content_specificity_engine import ContentSpecificityEngine
from scripts.curriculum_generator.components.module_content_integrator import ModuleContentIntegrator  
from scripts.curriculum_generator.components.enhanced_module_selector import EnhancedModuleSelector

def test_large_curriculum_fixes():
    """Test the fixes for large curriculum generation"""
    
    print("🧪 TESTING ENHANCED CONTENT SPECIFICITY FIXES")
    print("=" * 60)
    
    # Test parameters - the problematic scenario
    role_id = "DSC"
    eqf_level = 7
    ects = 180.0
    units = 18
    topic = "Digital Sustainability Consulting"
    
    print(f"📋 Test Scenario: {role_id} EQF{eqf_level} {ects}ECTS ({units} units)")
    print(f"🎯 Topic: {topic}")
    
    # Initialize enhanced components
    try:
        print("\n🔧 Initializing enhanced components...")
        
        module_selector = EnhancedModuleSelector())
        content_integrator = ModuleContentIntegrator(project_root)
        specificity_engine = ContentSpecificityEngine(project_root)
        
        print("✅ All components initialized successfully")
        
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
        return False
    
    # Test 1: Enhanced Module Selection
    print("\n📦 TEST 1: Enhanced Module Selection for Large Curriculum")
    try:
        selected_modules, selection_metadata = module_selector.select_modules_for_curriculum(
            role_id=role_id,
            topic=topic,
            eqf_level=eqf_level,
            ects=ects,
            min_score_threshold=0.2  # Lower threshold for large curricula
        )
        
        print(f"✅ Module selection successful:")
        print(f"   📊 Target modules: {selection_metadata['target_modules']}")
        print(f"   📦 Selected modules: {len(selected_modules)}")
        print(f"   🎯 Role alignment: {selection_metadata['role_alignment']:.1f}%")
        print(f"   📋 Coverage ratio: {selection_metadata['coverage_ratio']:.2f}")
        
        if len(selected_modules) < 20:
            print(f"   ⚠️  Warning: Large curriculum may need more modules")
        
    except Exception as e:
        print(f"❌ Module selection failed: {e}")
        return False
    
    # Test 2: Create Mock Learning Units
    print("\n🏗️  TEST 2: Creating Mock Learning Units")
    try:
        # Create 18 learning units for 180 ECTS curriculum
        base_units = []
        progression_levels = ["Foundation", "Development", "Application", "Integration", "Mastery", "Leadership"]
        
        for i in range(units):
            unit_ects = ects / units  # ~10 ECTS per unit
            progression = progression_levels[i % len(progression_levels)]
            
            unit = {
                "unit_number": i + 1,
                "title": f"Unit {i + 1}: Generic {progression}",
                "ects": unit_ects,
                "progression_level": progression,
                "learning_outcomes": [f"Generic outcome {i + 1}"],
                "unit_description": f"Generic description for unit {i + 1}",
                "content_source": "generic"
            }
            base_units.append(unit)
        
        print(f"✅ Created {len(base_units)} mock learning units")
        
    except Exception as e:
        print(f"❌ Mock unit creation failed: {e}")
        return False
    
    # Test 3: Enhanced Module Integration
    print("\n🔗 TEST 3: Enhanced Module Integration with Fixed Distribution")
    try:
        enhanced_units = content_integrator.integrate_modules_into_units(
            base_units=base_units,
            selected_modules=selected_modules,
            role_id=role_id,
            topic=topic,
            eqf_level=eqf_level
        )
        
        # Analyze integration results
        units_with_modules = sum(1 for unit in enhanced_units if unit.get('assigned_modules'))
        integration_percentage = (units_with_modules / len(enhanced_units)) * 100
        
        print(f"✅ Module integration completed:")
        print(f"   📊 Units processed: {len(enhanced_units)}")
        print(f"   🔗 Units with modules: {units_with_modules}/{len(enhanced_units)}")
        print(f"   📈 Integration rate: {integration_percentage:.1f}%")
        
        # Check for the critical issue
        units_without_modules = [unit for unit in enhanced_units if not unit.get('assigned_modules')]
        if units_without_modules:
            print(f"   ❌ CRITICAL ISSUE: {len(units_without_modules)} units still have no modules!")
            for unit in units_without_modules[:3]:  # Show first 3
                print(f"      - Unit {unit.get('unit_number')}: {unit.get('title', 'No title')}")
        else:
            print(f"   ✅ SUCCESS: All units have assigned modules!")
        
        # Get integration summary
        integration_summary = content_integrator.get_integration_summary()
        if integration_summary['integration_status'] == 'CRITICAL':
            print(f"   ⚠️  Integration status: {integration_summary['integration_status']}")
            print(f"   ⚠️  High severity warnings: {integration_summary['high_severity_warnings']}")
        
    except Exception as e:
        print(f"❌ Module integration failed: {e}")
        return False
    
    # Test 4: Content Specificity Analysis
    print("\n🚀 TEST 4: Content Specificity Analysis and Fixes")
    try:
        # Create mock curriculum structure
        curriculum_data = {
            "metadata": {
                "role_id": role_id,
                "eqf_level": eqf_level,
                "ects": ects,
                "topic": topic,
                "units": units
            },
            "learning_units": enhanced_units,
            "selected_modules": selected_modules
        }
        
        # Apply enhanced content specificity analysis
        enhanced_curriculum = specificity_engine.enhance_curriculum_with_specific_content(
            curriculum_data, selected_modules
        )
        
        # Analyze results
        metadata = enhanced_curriculum.get('content_specificity_metadata', {})
        d21_analysis = metadata.get('d21_gap_analysis', {})
        fixes_applied = metadata.get('fixes_applied', [])
        
        print(f"✅ Content specificity analysis completed:")
        print(f"   📊 D2.1 gap score: {d21_analysis.get('content_specificity_score', 0):.1f}%")
        print(f"   🎯 Gap coverage: {d21_analysis.get('gap_coverage', 'Unknown')}")
        print(f"   🔧 Fixes applied: {len(fixes_applied)}")
        for fix in fixes_applied:
            print(f"      - {fix}")
        
        warnings = metadata.get('content_warnings', {}).get('warnings', [])
        print(f"   ⚠️  Warnings: {len(warnings)}")
        
        # Check final integration status
        final_units = enhanced_curriculum.get('learning_units', [])
        final_units_with_modules = sum(1 for unit in final_units if unit.get('assigned_modules'))
        final_integration_rate = (final_units_with_modules / len(final_units)) * 100
        
        print(f"   📈 Final integration rate: {final_integration_rate:.1f}%")
        
        if final_integration_rate == 100.0:
            print(f"   🎉 SUCCESS: Complete module coverage achieved!")
        
    except Exception as e:
        print(f"❌ Content specificity analysis failed: {e}")
        return False
    
    # Test 5: Assessment Generation Fix
    print("\n📝 TEST 5: Assessment Generation Fix")
    try:
        assessment_fixed_curriculum = specificity_engine.fix_assessment_generation_errors(enhanced_curriculum)
        
        assessment_strategy = assessment_fixed_curriculum.get('assessment_strategy', {})
        assessments = assessment_strategy.get('assessments', [])
        
        print(f"✅ Assessment generation fix completed:")
        print(f"   📊 Assessments generated: {len(assessments)}")
        print(f"   🎯 Role-aligned: {assessment_strategy.get('role_aligned', False)}")
        print(f"   🔧 Generation fixed: {assessment_strategy.get('generation_fixed', False)}")
        
        # Check for title errors
        assessments_with_titles = sum(1 for assessment in assessments if assessment.get('title'))
        print(f"   📋 Assessments with titles: {assessments_with_titles}/{len(assessments)}")
        
        if assessments_with_titles == len(assessments):
            print(f"   ✅ SUCCESS: All assessments have proper titles!")
        
    except Exception as e:
        print(f"❌ Assessment generation fix failed: {e}")
        return False
    
    # Final Results Summary
    print("\n🏆 FINAL TEST RESULTS")
    print("=" * 60)
    
    success_metrics = {
        "Module Selection": len(selected_modules) >= 20,
        "Module Distribution": final_integration_rate == 100.0,
        "Role-Specific Content": any('role_aligned' in unit for unit in final_units),
        "Assessment Generation": assessment_strategy.get('generation_fixed', False),
        "Content Specificity": d21_analysis.get('content_specificity_score', 0) >= 80.0
    }
    
    passed_tests = sum(success_metrics.values())
    total_tests = len(success_metrics)
    
    print(f"📊 Test Results: {passed_tests}/{total_tests} passed")
    for test_name, passed in success_metrics.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    overall_success = passed_tests == total_tests
    if overall_success:
        print(f"\n🎉 ALL TESTS PASSED! Enhanced fixes are working correctly.")
        print(f"💡 The D2.1 curriculum generation problems have been resolved.")
    else:
        print(f"\n⚠️  Some tests failed. Review the issues above.")
    
    return overall_success

if __name__ == "__main__":
    success = test_large_curriculum_fixes()
    sys.exit(0 if success else 1)
