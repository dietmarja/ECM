# scripts/curriculum_generator/domain/competency_mapper.py
"""
Enhanced Competency framework mapping logic - FIXED VERSION
Maps curriculum components to comprehensive industry competency frameworks
Eliminates truncated entries and provides complete competency descriptions
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class EnhancedCompetencyMapper:
    """Enhanced mapper with comprehensive framework integration"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.standards_dir = project_root / 'input' / 'standards'
        
        # Load comprehensive framework standards
        self.ecf_esco_framework = self._load_framework_standard('standard_ecf_esco.json')
        self.greencomp_framework = self._load_framework_standard('standard_greencomp.json')
        
        # Build competency lookup tables
        self.competency_database = self._build_competency_database()
        
        print(f"✅ Enhanced Competency Mapper initialized with {len(self.competency_database)} competencies")
        
    def _load_framework_standard(self, filename: str) -> Dict:
        """Load framework standard file"""
        try:
            filepath = self.standards_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ Framework standard not found: {filename}")
                return {}
        except Exception as e:
            print(f"❌ Error loading framework standard {filename}: {e}")
            return {}
    
    def _build_competency_database(self) -> Dict[str, Dict]:
        """Build comprehensive competency database from all frameworks"""
        database = {}
        
        # Process e-CF competencies
        ecf_competencies = self.ecf_esco_framework.get('e_cf_competencies', {})
        for category, competencies in ecf_competencies.items():
            for comp_id, comp_data in competencies.items():
                database[comp_data['competency_id']] = {
                    'id': comp_data['competency_id'],
                    'title': comp_data['title'],
                    'description': comp_data['description'],
                    'framework': 'e-CF',
                    'level_range': comp_data.get('level_range', [4, 5, 6]),
                    'related_skills': comp_data.get('related_skills', []),
                    'application_examples': comp_data.get('application_examples', []),
                    'sustainability_context': comp_data.get('sustainability_context', ''),
                    'category': category
                }
        
        # Process ESCO competencies
        esco_competencies = self.ecf_esco_framework.get('esco_competencies', {})
        for category, competencies in esco_competencies.items():
            for comp_id, comp_data in competencies.items():
                database[comp_data['competency_id']] = {
                    'id': comp_data['competency_id'],
                    'title': comp_data['title'],
                    'description': comp_data['description'],
                    'framework': 'ESCO',
                    'level': comp_data.get('level', 5),
                    'related_skills': comp_data.get('related_skills', []),
                    'application_examples': comp_data.get('application_examples', []),
                    'domain_area': comp_data.get('domain_area', ''),
                    'category': category
                }
        
        # Process GreenComp competencies
        greencomp_areas = self.greencomp_framework.get('competency_areas', {})
        for area, competencies in greencomp_areas.items():
            for comp_id, comp_data in competencies.items():
                database[comp_data['competency_id']] = {
                    'id': comp_data['competency_id'],
                    'title': comp_data['title'],
                    'description': comp_data['description'],
                    'framework': 'GreenComp',
                    'level': comp_data.get('level', 'Foundation'),
                    'related_skills': comp_data.get('related_skills', []),
                    'application_examples': comp_data.get('application_examples', []),
                    'digital_context': comp_data.get('digital_context', ''),
                    'domain_area': comp_data.get('domain_area', ''),
                    'competency_area': area
                }
        
        return database
    
    def get_competencies_for_role(self, role_id: str, eqf_level: int = 6) -> List[Dict]:
        """Get comprehensive competency mappings for a specific role"""
        
        # Get role-specific mappings from frameworks
        role_mappings = []
        
        # e-CF/ESCO role mappings
        ecf_role_mappings = self.ecf_esco_framework.get('competency_mapping_rules', {}).get('role_mappings', {})
        if role_id in ecf_role_mappings:
            for comp_id in ecf_role_mappings[role_id]:
                if comp_id in self.competency_database:
                    competency = self.competency_database[comp_id].copy()
                    competency['mapping_confidence'] = 'high'
                    competency['mapping_source'] = 'role_specific'
                    role_mappings.append(competency)
        
        # GreenComp role mappings
        greencomp_role_mappings = self.greencomp_framework.get('role_competency_mappings', {})
        if role_id in greencomp_role_mappings:
            for comp_id in greencomp_role_mappings[role_id]:
                if comp_id in self.competency_database:
                    competency = self.competency_database[comp_id].copy()
                    competency['mapping_confidence'] = 'high'
                    competency['mapping_source'] = 'role_specific'
                    role_mappings.append(competency)
        
        # Add EQF-level appropriate competencies
        eqf_mappings = self.ecf_esco_framework.get('competency_mapping_rules', {}).get('eqf_level_mappings', {})
        if str(eqf_level) in eqf_mappings:
            for comp_id in eqf_mappings[str(eqf_level)]:
                if comp_id in self.competency_database:
                    # Check if not already added
                    if not any(c['id'] == comp_id for c in role_mappings):
                        competency = self.competency_database[comp_id].copy()
                        competency['mapping_confidence'] = 'medium'
                        competency['mapping_source'] = 'eqf_level'
                        role_mappings.append(competency)
        
        # Remove duplicates and sort by framework
        unique_mappings = []
        seen_ids = set()
        
        for mapping in role_mappings:
            if mapping['id'] not in seen_ids:
                unique_mappings.append(mapping)
                seen_ids.add(mapping['id'])
        
        # Sort by framework priority: GreenComp, e-CF, ESCO
        framework_priority = {'GreenComp': 1, 'e-CF': 2, 'ESCO': 3}
        unique_mappings.sort(key=lambda x: framework_priority.get(x['framework'], 4))
        
        return unique_mappings
    
    def generate_complete_framework_table(self, role_id: str, eqf_level: int = 6) -> Dict[str, List[Dict]]:
        """Generate complete framework alignment table with full descriptions"""
        
        competencies = self.get_competencies_for_role(role_id, eqf_level)
        
        framework_table = {
            'GreenComp': [],
            'e-CF': [],
            'ESCO': []
        }
        
        for comp in competencies:
            framework = comp['framework']
            if framework in framework_table:
                # Create complete entry with NO truncation
                entry = {
                    'competency_id': comp['id'],
                    'title': comp['title'],
                    'full_description': comp['description'],  # FULL description, no truncation
                    'level': comp.get('level', comp.get('level_range', [eqf_level])),
                    'related_skills': comp.get('related_skills', []),
                    'application_examples': comp.get('application_examples', []),
                    'sustainability_context': comp.get('sustainability_context', ''),
                    'digital_context': comp.get('digital_context', ''),
                    'mapping_confidence': comp.get('mapping_confidence', 'medium'),
                    'mapping_source': comp.get('mapping_source', 'framework'),
                    'domain_area': comp.get('domain_area', ''),
                    'category': comp.get('category', comp.get('competency_area', ''))
                }
                framework_table[framework].append(entry)
        
        return framework_table
    
    def enhance_module_with_competencies(self, module: Dict, role_id: str, eqf_level: int = 6) -> Dict:
        """INTEGRATION METHOD: Enhance module with complete framework mappings"""
        
        # Create enhanced module copy
        enhanced_module = module.copy()
        
        # Get module-specific competencies
        module_competencies = self.map_module_to_competencies(module, role_id, eqf_level)
        
        # Add complete framework mappings to module
        framework_mappings = {
            'GreenComp': [],
            'e-CF': [],
            'ESCO': []
        }
        
        for comp in module_competencies:
            framework = comp['framework']
            if framework in framework_mappings:
                framework_mappings[framework].append({
                    'competency_id': comp['id'],
                    'title': comp['title'],
                    'description': comp['description'],  # Complete description
                    'application_example': comp.get('application_examples', [''])[0] if comp.get('application_examples') else '',
                    'relevance_score': comp.get('relevance_score', 0.5),
                    'mapping_confidence': comp.get('mapping_confidence', 'medium')
                })
        
        # Add to module
        enhanced_module['framework_mappings'] = framework_mappings
        enhanced_module['competency_alignment_summary'] = {
            'total_competencies': len(module_competencies),
            'framework_distribution': {
                'GreenComp': len(framework_mappings['GreenComp']),
                'e-CF': len(framework_mappings['e-CF']),
                'ESCO': len(framework_mappings['ESCO'])
            },
            'average_relevance': sum(c.get('relevance_score', 0.5) for c in module_competencies) / len(module_competencies) if module_competencies else 0.5
        }
        
        print(f"   🗺️ Enhanced {module.get('title', 'Module')} with {len(module_competencies)} competency mappings")
        
        return enhanced_module
    
    def map_module_to_competencies(self, module: Dict, role_id: str, eqf_level: int = 6) -> List[Dict]:
        """Map a specific module to relevant competencies"""
        
        module_title = module.get('title', '').lower()
        module_keywords = [kw.lower() for kw in module.get('keywords', [])]
        module_description = module.get('description', '').lower()
        
        relevant_competencies = []
        all_competencies = self.get_competencies_for_role(role_id, eqf_level)
        
        for comp in all_competencies:
            relevance_score = self._calculate_module_competency_relevance(
                module_title, module_keywords, module_description, comp
            )
            
            if relevance_score > 0.3:  # Relevance threshold
                comp_mapping = comp.copy()
                comp_mapping['relevance_score'] = relevance_score
                comp_mapping['module_alignment'] = self._explain_module_alignment(module, comp)
                relevant_competencies.append(comp_mapping)
        
        # Sort by relevance score
        relevant_competencies.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant_competencies[:6]  # Return top 6 most relevant
    
    def _calculate_module_competency_relevance(self, title: str, keywords: List[str], 
                                             description: str, competency: Dict) -> float:
        """Calculate how relevant a competency is to a module"""
        
        score = 0.0
        
        # Check title alignment
        comp_title = competency['title'].lower()
        comp_description = competency['description'].lower()
        
        # Keyword matching
        for keyword in keywords:
            if keyword in comp_title:
                score += 0.3
            if keyword in comp_description:
                score += 0.2
        
        # Application examples matching
        for example in competency.get('application_examples', []):
            example_lower = example.lower()
            for keyword in keywords:
                if keyword in example_lower:
                    score += 0.2
        
        # Related skills matching
        for skill in competency.get('related_skills', []):
            skill_lower = skill.lower()
            for keyword in keywords:
                if keyword in skill_lower:
                    score += 0.1
        
        # Sustainability context matching (for digital sustainability topics)
        sustainability_terms = ['sustainability', 'environmental', 'green', 'carbon', 'energy']
        if any(term in title or term in ' '.join(keywords) for term in sustainability_terms):
            if competency['framework'] == 'GreenComp':
                score += 0.3
            if 'sustainability' in comp_description:
                score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _explain_module_alignment(self, module: Dict, competency: Dict) -> str:
        """Explain how a module aligns with a competency"""
        
        module_title = module.get('title', '')
        comp_title = competency['title']
        framework = competency['framework']
        
        # Generate contextual explanation
        if competency['framework'] == 'GreenComp':
            return f"Module '{module_title}' develops {framework} competency '{comp_title}' through practical application of sustainability principles in digital contexts."
        elif competency['framework'] == 'e-CF':
            return f"Module '{module_title}' builds {framework} competency '{comp_title}' through hands-on technical skill development and professional practice."
        else:  # ESCO
            return f"Module '{module_title}' supports {framework} competency '{comp_title}' by developing relevant professional skills and knowledge."
    
    def generate_curriculum_competency_report(self, modules: List[Dict], role_id: str, 
                                            eqf_level: int = 6) -> Dict:
        """Generate comprehensive competency mapping report for entire curriculum"""
        
        print(f"🗺️ Generating competency report for {role_id} (EQF {eqf_level})")
        
        # Get overall framework alignment
        framework_table = self.generate_complete_framework_table(role_id, eqf_level)
        
        # Map each module
        module_mappings = []
        for module in modules:
            module_comps = self.map_module_to_competencies(module, role_id, eqf_level)
            module_mappings.append({
                'module_title': module.get('title', ''),
                'module_ects': module.get('ects', 5),
                'competency_mappings': module_comps,
                'total_mapped_competencies': len(module_comps)
            })
        
        # Calculate coverage statistics
        all_mapped_competencies = set()
        for module_mapping in module_mappings:
            for comp in module_mapping['competency_mappings']:
                all_mapped_competencies.add(comp['id'])
        
        total_available = len(self.get_competencies_for_role(role_id, eqf_level))
        coverage_percentage = (len(all_mapped_competencies) / total_available * 100) if total_available > 0 else 0
        
        # Framework distribution
        framework_distribution = {'GreenComp': 0, 'e-CF': 0, 'ESCO': 0}
        for comp_id in all_mapped_competencies:
            if comp_id in self.competency_database:
                framework = self.competency_database[comp_id]['framework']
                framework_distribution[framework] += 1
        
        report = {
            'role_id': role_id,
            'eqf_level': eqf_level,
            'framework_alignment_table': framework_table,
            'module_competency_mappings': module_mappings,
            'coverage_statistics': {
                'total_available_competencies': total_available,
                'total_mapped_competencies': len(all_mapped_competencies),
                'coverage_percentage': round(coverage_percentage, 1),
                'framework_distribution': framework_distribution
            },
            'competency_gaps': self._identify_competency_gaps(framework_table, all_mapped_competencies),
            'recommendations': self._generate_competency_recommendations(role_id, eqf_level, coverage_percentage)
        }
        
        print(f"✅ Competency report generated: {coverage_percentage:.1f}% coverage, {len(all_mapped_competencies)} competencies mapped")
        
        return report
    
    def _identify_competency_gaps(self, framework_table: Dict, mapped_competencies: set) -> List[Dict]:
        """Identify important competencies that are not covered"""
        
        gaps = []
        
        for framework, competencies in framework_table.items():
            for comp in competencies:
                if comp['competency_id'] not in mapped_competencies:
                    if comp.get('mapping_confidence') == 'high':  # Only report high-confidence gaps
                        gaps.append({
                            'competency_id': comp['competency_id'],
                            'title': comp['title'],
                            'framework': framework,
                            'importance': 'high' if comp.get('mapping_source') == 'role_specific' else 'medium',
                            'recommendation': f"Consider adding module content that develops {comp['title']} competency"
                        })
        
        return gaps[:5]  # Return top 5 gaps
    
    def _generate_competency_recommendations(self, role_id: str, eqf_level: int, 
                                           coverage_percentage: float) -> List[str]:
        """Generate recommendations for improving competency coverage"""
        
        recommendations = []
        
        if coverage_percentage < 60:
            recommendations.append("Consider adding more specialized modules to improve competency coverage")
        
        if coverage_percentage > 90:
            recommendations.append("Excellent competency coverage - consider curriculum optimization")
        
        # Role-specific recommendations
        if role_id in ['DSL', 'DSM']:
            recommendations.append("Ensure strong coverage of leadership and strategic competencies")
        elif role_id in ['DAN', 'DSI']:
            recommendations.append("Focus on analytical and technical competencies")
        elif role_id in ['SDD', 'SSD']:
            recommendations.append("Emphasize practical and implementation competencies")
        
        # EQF-specific recommendations
        if eqf_level >= 7:
            recommendations.append("Include advanced research and innovation competencies")
        elif eqf_level <= 5:
            recommendations.append("Focus on foundational and practical competencies")
        
        return recommendations


# Legacy compatibility wrapper
class CompetencyMapper(EnhancedCompetencyMapper):
    """Legacy wrapper for backwards compatibility"""
    
    def __init__(self, domain_knowledge):
        # Extract project root from domain knowledge or use default
        if hasattr(domain_knowledge, 'project_root'):
            project_root = domain_knowledge.project_root
        else:
            project_root = Path(__file__).parent.parent.parent.parent
        
        super().__init__(project_root)
        self.domain_knowledge = domain_knowledge  # Store for legacy compatibility
    
    def map_component_to_frameworks(self, component: Dict) -> List[Dict]:
        """Legacy method - maps component to frameworks"""
        
        # Extract component information
        component_name = component.get('component_name', component.get('title', ''))
        role_id = component.get('role_id', 'DSM')  # Default role
        eqf_level = component.get('eqf_level', 6)  # Default EQF level
        
        # Create mock module for mapping
        mock_module = {
            'title': component_name,
            'keywords': component.get('skills', []),
            'description': component.get('description', ''),
            'ects': component.get('ects', 5)
        }
        
        # Use enhanced mapping
        competencies = self.map_module_to_competencies(mock_module, role_id, eqf_level)
        
        # Convert to legacy format
        legacy_mappings = []
        for comp in competencies:
            legacy_mappings.append({
                'component_id': component.get('component_id', ''),
                'component_name': component_name,
                'framework': comp['framework'],
                'competency_id': comp['id'],
                'competency_title': comp['title'],
                'competency_description': comp['description'],  # Full description
                'mapping_type': 'enhanced',
                'confidence': comp.get('mapping_confidence', 'medium'),
                'relevance_score': comp.get('relevance_score', 0.5)
            })
        
        return legacy_mappings
    
    def generate_competency_report(self, curriculum_components: List[Dict]) -> Dict:
        """Legacy method - generates competency report"""
        
        # Extract role information from first component
        role_id = curriculum_components[0].get('role_id', 'DSM') if curriculum_components else 'DSM'
        eqf_level = curriculum_components[0].get('eqf_level', 6) if curriculum_components else 6
        
        # Convert components to modules format
        modules = []
        for component in curriculum_components:
            modules.append({
                'title': component.get('component_name', component.get('title', '')),
                'keywords': component.get('skills', []),
                'description': component.get('description', ''),
                'ects': component.get('ects', 5)
            })
        
        # Use enhanced report generation
        enhanced_report = self.generate_curriculum_competency_report(modules, role_id, eqf_level)
        
        # Convert to legacy format for compatibility
        legacy_report = {
            'total_mappings': enhanced_report['coverage_statistics']['total_mapped_competencies'],
            'frameworks_covered': list(enhanced_report['coverage_statistics']['framework_distribution'].keys()),
            'framework_coverage': enhanced_report['coverage_statistics']['framework_distribution'],
            'mapping_details': [],
            'coverage_statistics': enhanced_report['coverage_statistics']
        }
        
        # Add mapping details
        for module_mapping in enhanced_report['module_competency_mappings']:
            for comp in module_mapping['competency_mappings']:
                legacy_report['mapping_details'].append({
                    'component_id': module_mapping['module_title'],
                    'component_name': module_mapping['module_title'],
                    'framework': comp['framework'],
                    'competency_id': comp['id'],
                    'mapping_type': 'enhanced',
                    'confidence': comp.get('mapping_confidence', 'medium')
                })
        
        return legacy_report
