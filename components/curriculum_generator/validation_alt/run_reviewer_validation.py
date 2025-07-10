#!/usr/bin/env python3
"""
EU Project Reviewer Validation Suite Runner
Comprehensive validation against T3.2 and T3.4 deliverable requirements
"""

import subprocess
import sys
from pathlib import Path
from datetime import date

def run_reviewer_validation():
    """Run both T3.2 and T3.4 reviewer validation suites"""
    
    print("🏛️ === EU PROJECT REVIEWER VALIDATION SUITE ===")
    print("📋 Comprehensive Assessment of Digital Sustainability Framework")
    print(f"📅 Review Date: {date.today().isoformat()}")
    print("🎯 Deliverables: T3.2 Educational Profiles & T3.4 Micro-Credentials")
    
    results = {
        "t3_2_result": False,
        "t3_4_result": False,
        "overall_success": False
    }
    
    # Ensure validation directory exists
    validation_dir = Path("scripts/validation")
    validation_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("🎓 T3.2 VALIDATION: Educational Profiles & Curricula Design")
    print("="*70)
    
    # Run T3.2 validation
    try:
        result_t32 = subprocess.run(
            ["python3", "scripts/validation/T3_2_reviewer_check_suite.py"],
            capture_output=True, text=True
        )
        
        if result_t32.returncode == 0:
            print("✅ T3.2 VALIDATION: PASSED")
            results["t3_2_result"] = True
        else:
            print("❌ T3.2 VALIDATION: FAILED")
        
        # Show summary output
        if result_t32.stdout:
            output_lines = result_t32.stdout.strip().split('\n')
            # Show the final verdict lines
            for line in output_lines:
                if "REVIEWER VERDICT" in line or "Compliance:" in line:
                    print(f"   {line}")
        
    except FileNotFoundError:
        print("❌ T3.2 VALIDATION: Script not found")
    except Exception as e:
        print(f"❌ T3.2 VALIDATION: Error - {e}")
    
    print("\n" + "="*70)
    print("🏅 T3.4 VALIDATION: Micro-Credentials & Certifications")
    print("="*70)
    
    # Run T3.4 validation
    try:
        result_t34 = subprocess.run(
            ["python3", "scripts/validation/T3_4_reviewer_check_suite.py"],
            capture_output=True, text=True
        )
        
        if result_t34.returncode == 0:
            print("✅ T3.4 VALIDATION: PASSED")
            results["t3_4_result"] = True
        else:
            print("❌ T3.4 VALIDATION: FAILED")
        
        # Show summary output
        if result_t34.stdout:
            output_lines = result_t34.stdout.strip().split('\n')
            # Show the final verdict lines
            for line in output_lines:
                if "REVIEWER VERDICT" in line or "Compliance:" in line or "EU Recognition" in line:
                    print(f"   {line}")
        
    except FileNotFoundError:
        print("❌ T3.4 VALIDATION: Script not found")
    except Exception as e:
        print(f"❌ T3.4 VALIDATION: Error - {e}")
    
    print("\n" + "="*70)
    print("📊 OVERALL EU PROJECT REVIEWER ASSESSMENT")
    print("="*70)
    
    # Overall assessment
    passed_validations = sum([results["t3_2_result"], results["t3_4_result"]])
    total_validations = 2
    
    print(f"📈 Validation Results: {passed_validations}/{total_validations}")
    print(f"📊 T3.2 Educational Profiles: {'✅ PASSED' if results['t3_2_result'] else '❌ FAILED'}")
    print(f"📊 T3.4 Micro-Credentials: {'✅ PASSED' if results['t3_4_result'] else '❌ FAILED'}")
    
    if passed_validations == 2:
        print("\n🎉 OVERALL REVIEWER VERDICT: EXCELLENT")
        print("✅ Framework fully complies with EU project deliverable requirements")
        print("🚀 Ready for EU recognition and cross-border implementation")
        results["overall_success"] = True
        
    elif passed_validations == 1:
        print("\n✅ OVERALL REVIEWER VERDICT: PARTIALLY COMPLIANT")
        print("⚠️  Framework meets some EU requirements but needs improvement")
        print("🔧 Address failing validation before full deployment")
        
    else:
        print("\n❌ OVERALL REVIEWER VERDICT: NON-COMPLIANT")
        print("🚨 Framework does not meet EU project deliverable requirements")
        print("📋 Significant work required before EU recognition")
    
    # Generate summary report
    generate_summary_report(results)
    
    return results["overall_success"]

def generate_summary_report(results):
    """Generate overall reviewer summary report"""
    
    summary_report = {
        "review_date": date.today().isoformat(),
        "reviewer_type": "EU_Project_Reviewer",
        "framework_version": "3.2.0",
        "deliverables_assessed": ["T3.2_Educational_Profiles", "T3.4_Micro_Credentials"],
        "validation_results": results,
        "overall_compliance": "COMPLIANT" if results["overall_success"] else "NON_COMPLIANT",
        "eu_readiness": "HIGH" if results["overall_success"] else "MEDIUM" if sum([results["t3_2_result"], results["t3_4_result"]]) == 1 else "LOW",
        "recommendations": []
    }
    
    # Add specific recommendations
    if not results["t3_2_result"]:
        summary_report["recommendations"].append("Improve T3.2 educational profiles and curricula design compliance")
    
    if not results["t3_4_result"]:
        summary_report["recommendations"].append("Enhance T3.4 micro-credentials and certification framework")
    
    if results["overall_success"]:
        summary_report["recommendations"].append("Proceed with EU recognition application process")
        summary_report["recommendations"].append("Begin cross-border certification discussions")
    
    # Save summary report
    report_dir = Path("output/validation_reports/reviewer_summary")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    import json
    report_file = report_dir / f"EU_reviewer_summary_{date.today().strftime('%Y%m%d')}.json"
    with open(report_file, 'w') as f:
        json.dump(summary_report, f, indent=2)
    
    print(f"\n📁 Summary report saved: {report_file}")
    print(f"📂 Detailed reports available in: output/validation_reports/")

def main():
    """Main execution function"""
    success = run_reviewer_validation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
