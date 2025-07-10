# scripts/curriculum_generator/components/profile_validator.py
"""
EU Educational Profile Compliance Validator
Validates educational profiles against EU educational profile standards
Addresses all D2.1 compliance issues and T3.2/T3.4 requirements
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ComplianceLevel(Enum):
    COMPLIANT = "✅ Compliant"
    WARNING = "⚠️ Warning"
    NON_COMPLIANT = "❌ Non-Compliant"

@dataclass
class ValidationResult:
    level: ComplianceLevel
    message: str
    details: Optional[str] = None

class EUProfileComplianceValidator:
    """
    Comprehensive validator for EU educational profile compliance
    """
    
    def __init__(self):
        self.validation_results = []
        self.compliance_score = 0
        self.total_checks = 0
        
    def validate_profile(self, profile: Dict) -> Dict[str, List[ValidationResult]]:
        """
        Validate a single educational profile against EU standards
        """
        results = {
            'structure_compliance': [],
            'learning_outcomes_quality': [],
            'eqf_progression': [],
            'role_differentiation': [],
            'curriculum_separation': []
        }
        
        # Structure Compliance Checks
        results['structure_compliance'].extend(self._validate_profile_structure(profile))
        
        # Learning Outcomes Quality
        results['learning_outcomes_quality'].extend(self._validate_learning_outcomes(profile))
        
        # EQF Progression Logic
        results['eqf_progression'].extend(self._validate_eqf_progression(profile))
        
        # Role Differentiation
        results['role_differentiation'].extend(self._validate_role_differentiation(profile))
        
        # Curriculum vs Profile Separation
        results['curriculum_separation'].extend(self._validate_curriculum_separation(profile))
        
        return results
    
    def _validate_profile_structure(self, profile: Dict) -> List[ValidationResult]:
        """Validate basic profile structure compliance"""
        results = []
        
        # Required fields check
        required_fields = [
            'id', 'profile_name', 'role_description', 'core_competency_areas',
            'learning_outcomes_by_eqf', 'framework_alignment', 'career_progression',
            'entry_requirements_by_eqf', 'assessment_philosophy', 'industry_application'
        ]
        
        missing_fields = [field for field in required_fields if field not in profile]
        if missing_fields:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                f"Missing required fields: {', '.join(missing_fields)}"
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                "All required profile structure fields present"
            ))
        
        # Role description quality
        if 'role_description' in profile:
            desc_length = len(profile['role_description'].split())
            if desc_length < 20:
                results.append(ValidationResult(
                    ComplianceLevel.WARNING,
                    f"Role description too brief ({desc_length} words). Should be 20+ words for strategic context."
                ))
            elif desc_length > 60:
                results.append(ValidationResult(
                    ComplianceLevel.WARNING,
                    f"Role description too detailed ({desc_length} words). Should be strategic, not operational."
                ))
            else:
                results.append(ValidationResult(
                    ComplianceLevel.COMPLIANT,
                    f"Role description appropriately detailed ({desc_length} words)"
                ))
        
        return results
    
    def _validate_learning_outcomes(self, profile: Dict) -> List[ValidationResult]:
        """Validate learning outcomes quality and integration"""
        results = []
        
        if 'learning_outcomes_by_eqf' not in profile:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                "Missing learning_outcomes_by_eqf section"
            ))
            return results
        
        outcomes = profile['learning_outcomes_by_eqf']
        
        # Check for repetitive patterns (D2.1 issue)
        all_outcomes = []
        for eqf_level, level_outcomes in outcomes.items():
            all_outcomes.extend(level_outcomes)
        
        repetitive_patterns = self._detect_repetitive_patterns(all_outcomes)
        if repetitive_patterns:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                f"Repetitive learning outcome patterns detected: {', '.join(repetitive_patterns)}"
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                "Learning outcomes show proper differentiation and integration"
            ))
        
        # Check outcome integration quality
        integration_score = self._assess_outcome_integration(all_outcomes)
        if integration_score >= 0.8:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                f"Learning outcomes well-integrated (score: {integration_score:.2f})"
            ))
        elif integration_score >= 0.6:
            results.append(ValidationResult(
                ComplianceLevel.WARNING,
                f"Learning outcomes moderately integrated (score: {integration_score:.2f})"
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                f"Learning outcomes poorly integrated (score: {integration_score:.2f})"
            ))
        
        # Check for role-specific content
        role_specificity = self._assess_role_specificity(profile)
        if role_specificity >= 0.7:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                f"Strong role-specific content (score: {role_specificity:.2f})"
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.WARNING,
                f"Moderate role-specific content (score: {role_specificity:.2f})"
            ))
        
        return results
    
    def _validate_eqf_progression(self, profile: Dict) -> List[ValidationResult]:
        """Validate EQF level progression logic"""
        results = []
        
        if 'learning_outcomes_by_eqf' not in profile:
            return results
        
        outcomes = profile['learning_outcomes_by_eqf']
        eqf_levels = sorted([int(level) for level in outcomes.keys()])
        
        if len(eqf_levels) < 2:
            results.append(ValidationResult(
                ComplianceLevel.WARNING,
                f"Only one EQF level defined. Consider adding progression levels."
            ))
            return results
        
        # Check progression logic
        progression_valid = True
        progression_details = []
        
        for i in range(len(eqf_levels) - 1):
            lower_level = str(eqf_levels[i])
            higher_level = str(eqf_levels[i + 1])
            
            complexity_increase = self._assess_complexity_increase(
                outcomes[lower_level], outcomes[higher_level]
            )
            
            if complexity_increase >= 0.3:
                progression_details.append(f"EQF {lower_level}→{higher_level}: Good progression")
            else:
                progression_valid = False
                progression_details.append(f"EQF {lower_level}→{higher_level}: Insufficient complexity increase")
        
        if progression_valid:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                "EQF progression shows appropriate complexity increase",
                "\n".join(progression_details)
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                "EQF progression lacks sufficient complexity differentiation",
                "\n".join(progression_details)
            ))
        
        return results
    
    def _validate_role_differentiation(self, profile: Dict) -> List[ValidationResult]:
        """Validate role-specific differentiation"""
        results = []
        
        # Check distinctive features
        if 'distinctive_features' in profile:
            features = profile['distinctive_features']
            if len(features) >= 3:
                results.append(ValidationResult(
                    ComplianceLevel.COMPLIANT,
                    f"Sufficient distinctive features defined ({len(features)})"
                ))
            else:
                results.append(ValidationResult(
                    ComplianceLevel.WARNING,
                    f"Limited distinctive features ({len(features)}). Consider adding more role-specific characteristics."
                ))
        
        # Check industry application specificity
        if 'industry_application' in profile:
            industries = profile['industry_application']
            if len(industries) >= 4:
                results.append(ValidationResult(
                    ComplianceLevel.COMPLIANT,
                    f"Good industry scope coverage ({len(industries)} sectors)"
                ))
            else:
                results.append(ValidationResult(
                    ComplianceLevel.WARNING,
                    f"Limited industry scope ({len(industries)} sectors)"
                ))
        
        # Check career progression logic
        if 'career_progression' in profile:
            progression = profile['career_progression']
            logical_progression = self._validate_career_logic(progression, profile.get('id', ''))
            if logical_progression:
                results.append(ValidationResult(
                    ComplianceLevel.COMPLIANT,
                    "Career progression logic is appropriate for role"
                ))
            else:
                results.append(ValidationResult(
                    ComplianceLevel.NON_COMPLIANT,
                    "Career progression logic has inconsistencies"
                ))
        
        return results
    
    def _validate_curriculum_separation(self, profile: Dict) -> List[ValidationResult]:
        """Validate proper separation of profile vs curriculum concerns"""
        results = []
        
        # Check for curriculum-level details that should NOT be in profiles
        curriculum_violations = []
        
        # Check for ECTS details
        profile_str = json.dumps(profile, default=str).lower()
        if 'ects' in profile_str:
            curriculum_violations.append("ECTS details")
        
        # Check for module codes
        if re.search(r'[a-z]{2,4}-\d{3}', profile_str, re.IGNORECASE):
            curriculum_violations.append("Module codes")
        
        # Check for semester references
        if 'semester' in profile_str:
            curriculum_violations.append("Semester details")
        
        # Check for detailed assessment percentages
        if re.search(r'\d+%', profile_str):
            curriculum_violations.append("Assessment percentages")
        
        if curriculum_violations:
            results.append(ValidationResult(
                ComplianceLevel.NON_COMPLIANT,
                f"Curriculum-level details found: {', '.join(curriculum_violations)}",
                "Profiles should contain strategic information only"
            ))
        else:
            results.append(ValidationResult(
                ComplianceLevel.COMPLIANT,
                "Proper separation of profile and curriculum concerns"
            ))
        
        # Check assessment philosophy vs detailed methods
        if 'assessment_philosophy' in profile:
            philosophy = profile['assessment_philosophy']
            if 'approach' in philosophy and 'methods' in philosophy:
                methods = philosophy['methods']
                if all(len(method.split()) <= 5 for method in methods):
                    results.append(ValidationResult(
                        ComplianceLevel.COMPLIANT,
                        "Assessment philosophy appropriately high-level"
                    ))
                else:
                    results.append(ValidationResult(
                        ComplianceLevel.WARNING,
                        "Assessment methods may be too detailed for profile level"
                    ))
        
        return results
    
    def _detect_repetitive_patterns(self, outcomes: List[str]) -> List[str]:
        """Detect repetitive patterns in learning outcomes"""
        patterns = []
        
        # Common repetitive starters
        repetitive_starters = [
            "apply.*principles",
            "implement.*standards",
            "develop.*strategies",
            "the learner will be able to"
        ]
        
        for starter in repetitive_starters:
            matches = [outcome for outcome in outcomes if re.search(starter, outcome, re.IGNORECASE)]
            if len(matches) > len(outcomes) * 0.5:  # More than 50% use same pattern
                patterns.append(starter)
        
        return patterns
    
    def _assess_outcome_integration(self, outcomes: List[str]) -> float:
        """Assess how well-integrated learning outcomes are"""
        integration_keywords = [
            'synthesize', 'integrate', 'design', 'lead', 'innovate', 
            'influence', 'establish', 'develop comprehensive',
            'coordinate', 'facilitate', 'evaluate'
        ]
        
        integrated_count = 0
        for outcome in outcomes:
            if any(keyword in outcome.lower() for keyword in integration_keywords):
                integrated_count += 1
        
        return integrated_count / len(outcomes) if outcomes else 0
    
    def _assess_role_specificity(self, profile: Dict) -> float:
        """Assess role-specific content quality"""
        role_id = profile.get('id', '')
        role_specific_terms = {
            'DAN': ['analytics', 'data', 'visualization', 'statistics'],
            'DSE': ['infrastructure', 'engineering', 'optimization', 'architecture'],
            'DSL': ['leadership', 'strategy', 'governance', 'transformation'],
            'DSM': ['management', 'implementation', 'coordination', 'operations'],
            'DSC': ['consulting', 'advisory', 'assessment', 'recommendations'],
            'DSI': ['research', 'machine learning', 'modeling', 'innovation'],
            'SBA': ['business analysis', 'performance', 'ROI', 'process'],
            'SDD': ['development', 'coding', 'software', 'programming'],
            'SSD': ['design', 'solutions', 'circular', 'regenerative'],
            'STS': ['technical support', 'configuration', 'platforms', 'systems']
        }
        
        profile_text = json.dumps(profile, default=str).lower()
        relevant_terms = role_specific_terms.get(role_id, [])
        
        if not relevant_terms:
            return 0.5  # Unknown role
        
        term_count = sum(1 for term in relevant_terms if term in profile_text)
        return term_count / len(relevant_terms)
    
    def _assess_complexity_increase(self, lower_outcomes: List[str], higher_outcomes: List[str]) -> float:
        """Assess complexity increase between EQF levels"""
        complexity_indicators = {
            'low': ['implement', 'apply', 'use', 'follow', 'support'],
            'medium': ['design', 'develop', 'manage', 'coordinate', 'analyze'],
            'high': ['innovate', 'lead', 'influence', 'establish', 'transform']
        }
        
        def get_complexity_score(outcomes):
            total_score = 0
            for outcome in outcomes:
                outcome_lower = outcome.lower()
                if any(indicator in outcome_lower for indicator in complexity_indicators['high']):
                    total_score += 3
                elif any(indicator in outcome_lower for indicator in complexity_indicators['medium']):
                    total_score += 2
                elif any(indicator in outcome_lower for indicator in complexity_indicators['low']):
                    total_score += 1
            return total_score / len(outcomes) if outcomes else 0
        
        lower_score = get_complexity_score(lower_outcomes)
        higher_score = get_complexity_score(higher_outcomes)
        
        return (higher_score - lower_score) / 3.0  # Normalize to 0-1 scale
    
    def _validate_career_logic(self, progression: Dict, role_id: str) -> bool:
        """Validate career progression logic for role"""
        # Check for logical progression patterns
        levels = ['entry_level', 'mid_level', 'senior_level', 'executive_level']
        
        role_consistency_patterns = {
            'DAN': ['analyst', 'data'],
            'DSE': ['engineer', 'infrastructure'],
            'DSL': ['leader', 'director', 'chief'],
            'DSM': ['manager', 'director'],
            'DSC': ['consultant', 'advisor'],
            'DSI': ['scientist', 'researcher'],
            'SBA': ['analyst', 'business'],
            'SDD': ['developer', 'engineer'],
            'SSD': ['designer', 'architect'],
            'STS': ['specialist', 'technical']
        }
        
        patterns = role_consistency_patterns.get(role_id, [])
        if not patterns:
            return True  # Can't validate unknown role
        
        # Check if progression titles maintain role consistency
        for level in levels:
            if level in progression:
                title = progression[level].lower()
                if not any(pattern in title for pattern in patterns):
                    return False
        
        return True

def validate_all_profiles(profiles_path: str) -> Dict:
    """
    Validate all educational profiles in the file
    """
    validator = EUProfileComplianceValidator()
    
    try:
        with open(profiles_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
    except Exception as e:
        return {'error': f"Failed to load profiles: {str(e)}"}
    
    validation_report = {
        'overall_compliance': {},
        'profile_results': {},
        'summary': {
            'total_profiles': len(profiles),
            'compliant_profiles': 0,
            'warning_profiles': 0,
            'non_compliant_profiles': 0
        }
    }
    
    for profile in profiles:
        profile_id = profile.get('id', 'unknown')
        results = validator.validate_profile(profile)
        
        # Calculate profile compliance score
        total_checks = sum(len(category_results) for category_results in results.values())
        compliant_checks = sum(
            1 for category_results in results.values() 
            for result in category_results 
            if result.level == ComplianceLevel.COMPLIANT
        )
        
        compliance_score = compliant_checks / total_checks if total_checks > 0 else 0
        
        # Determine overall profile status
        has_non_compliant = any(
            result.level == ComplianceLevel.NON_COMPLIANT
            for category_results in results.values()
            for result in category_results
        )
        
        if has_non_compliant:
            profile_status = 'non_compliant'
            validation_report['summary']['non_compliant_profiles'] += 1
        elif compliance_score >= 0.8:
            profile_status = 'compliant'
            validation_report['summary']['compliant_profiles'] += 1
        else:
            profile_status = 'warning'
            validation_report['summary']['warning_profiles'] += 1
        
        validation_report['profile_results'][profile_id] = {
            'status': profile_status,
            'compliance_score': compliance_score,
            'results': results
        }
    
    # Overall compliance assessment
    overall_score = validation_report['summary']['compliant_profiles'] / len(profiles)
    validation_report['overall_compliance'] = {
        'score': overall_score,
        'status': 'compliant' if overall_score >= 0.8 else 'needs_improvement',
        'recommendation': _get_overall_recommendation(validation_report)
    }
    
    return validation_report

def _get_overall_recommendation(report: Dict) -> str:
    """Generate overall recommendation based on validation results"""
    summary = report['summary']
    
    if summary['non_compliant_profiles'] == 0 and summary['warning_profiles'] == 0:
        return "All profiles meet EU educational profile standards. Ready for production use."
    elif summary['non_compliant_profiles'] == 0:
        return f"All profiles compliant with minor warnings ({summary['warning_profiles']} profiles). Consider addressing warnings for optimal compliance."
    else:
        return f"Significant compliance issues found ({summary['non_compliant_profiles']} non-compliant profiles). Address critical issues before production use."

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        profiles_path = sys.argv[1]
    else:
        profiles_path = "/Users/dietmar/Dropbox/NCI/DIGITAL4Business/digital4sustainability/python/DSCG/input/educational_profiles/educational_profiles.json"
    
    # Run validation
    report = validate_all_profiles(profiles_path)
    
    if 'error' in report:
        print(f"❌ Validation Error: {report['error']}")
        sys.exit(1)
    
    # Print summary report
    print("🔍 EU Educational Profile Compliance Validation Report")
    print("=" * 60)
    
    summary = report['summary']
    print(f"📊 Overall Status: {report['overall_compliance']['status'].upper()}")
    print(f"📈 Compliance Score: {report['overall_compliance']['score']:.1%}")
    print(f"📋 Total Profiles: {summary['total_profiles']}")
    print(f"✅ Compliant: {summary['compliant_profiles']}")
    print(f"⚠️  Warnings: {summary['warning_profiles']}")
    print(f"❌ Non-Compliant: {summary['non_compliant_profiles']}")
    print()
    print(f"💡 Recommendation: {report['overall_compliance']['recommendation']}")
    
    # Detailed results for non-compliant profiles
    if summary['non_compliant_profiles'] > 0:
        print("\n🚨 Critical Issues Found:")
        print("-" * 40)
        
        for profile_id, profile_result in report['profile_results'].items():
            if profile_result['status'] == 'non_compliant':
                print(f"\n📄 Profile: {profile_id}")
                for category, results in profile_result['results'].items():
                    for result in results:
                        if result.level == ComplianceLevel.NON_COMPLIANT:
                            print(f"   ❌ {result.message}")
                            if result.details:
                                print(f"      Details: {result.details}")
