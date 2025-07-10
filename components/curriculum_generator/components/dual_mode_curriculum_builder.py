# scripts/curriculum_generator/components/dual_mode_curriculum_builder.py
"""
Dual-Mode Enhanced Curriculum Builder - Profile-First + Plan B
Integrates Enhanced Educational Profile Builder with Competency-Based Module Selection
Supports both competency-driven (profile-first) and direct curriculum generation modes
Maintains full backward compatibility while adding rich competency-driven capabilities
"""

from typing import Dict, List, Any, Tuple, Optional
import json
from pathlib import Path
from datetime import datetime

# Import enhanced components
from scripts.curriculum_generator.components.enhanced_profile_builder import EnhancedEducationalProfileBuilder
from scripts.curriculum_generator.components.competency_module_selector import CompetencyModuleSelector


class DualModeEnhancedCurriculumBuilder:
    """Enhanced curriculum builder supporting both Profile-First and Plan B modes"""

    def __init__(self, modules: List[Dict[str, Any]], role_definitions: Dict[str, Any]):
        self.modules = modules
        self.role_definitions = role_definitions
        
        # Initialize enhanced components
        self.enhanced_profile_builder = EnhancedEducationalProfileBuilder(
            role_definitions=role_definitions
        )
        
        self.competency_module_selector = CompetencyModuleSelector(
            modules=modules
        )
        
        print(f"🚀 DualModeEnhancedCurriculumBuilder initialized")
        print(f"   - Enhanced Profile Builder: Ready")
        print(f"   - Competency Module Selector: Ready")
        print(f"   - Modules available: {len(modules)}")

    def build_curriculum_profile_first(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        PRIMARY MODE: Profile-First Competency-Driven Curriculum Generation
        """
        
        print(f"\n🌱 PROFILE-FIRST MODE: Building competency-driven curriculum")
        print(f"   Role: {role_name} ({role_id})")
        print(f"   Topic: {topic}")
        print(f"   EQF Level: {eqf_level} | Target ECTS: {target_ects}")
        
        # Step 1: Generate Rich Educational Profile
        educational_profile = self.enhanced_profile_builder.build_rich_educational_profile(
            role_id=role_id,
            role_name=role_name,
            topic=topic,
            eqf_level=eqf_level,
            target_ects=target_ects,
            role_info=role_info or self.role_definitions.get(role_id, {})
        )
        
        # Step 2: Extract Competency Requirements for Module Selection
        competency_requirements = educational_profile.get('competency_requirements', {})
        
        if not competency_requirements:
            print(f"⚠️ No competency requirements found, falling back to Plan B mode")
            return self.build_curriculum_plan_b(
                role_id, role_name, topic, eqf_level, target_ects, role_info
            )
        
        # Step 3: Competency-Driven Module Selection
        selected_modules, selection_metadata = self.competency_module_selector.select_modules_competency_driven(
            competency_requirements=competency_requirements,
            role_id=role_id,
            topic=topic,
            target_ects=target_ects,
            eqf_level=eqf_level
        )
        
        # Step 4: Organize into Competency-Based Semesters
        semesters = self._organize_competency_based_semesters(
            selected_modules, educational_profile, target_ects
        )
        
        # Step 5: Build Complete Curriculum Structure
        curriculum = self._build_complete_curriculum_structure(
            mode='profile_first',
            role_id=role_id,
            role_name=role_name,
            topic=topic,
            eqf_level=eqf_level,
            target_ects=target_ects,
            selected_modules=selected_modules,
            semesters=semesters,
            educational_profile=educational_profile,
            selection_metadata=selection_metadata,
            role_info=role_info
        )
        
        print(f"✅ PROFILE-FIRST: Competency-driven curriculum generated successfully!")
        return curriculum

    def build_curriculum_plan_b(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        PLAN B MODE: Direct Curriculum Generation (Backward Compatible)
        """
        
        print(f"\n📚 PLAN B MODE: Direct curriculum generation")
        print(f"   Role: {role_name} ({role_id})")
        print(f"   Topic: {topic}")
        print(f"   EQF Level: {eqf_level} | Target ECTS: {target_ects}")
        
        # Step 1: Direct Module Selection (no competency requirements)
        selected_modules, selection_metadata = self.competency_module_selector.select_modules_direct_mode(
            role_id=role_id,
            topic=topic,
            target_ects=target_ects,
            eqf_level=eqf_level
        )
        
        # Step 2: Generate Basic Educational Profile (for consistency)
        educational_profile = self._generate_basic_educational_profile(
            role_id, role_name, topic, eqf_level, target_ects, role_info
        )
        
        # Step 3: Organize into Standard Semesters
        semesters = self._organize_standard_semesters(
            selected_modules, target_ects
        )
        
        # Step 4: Build Complete Curriculum Structure
        curriculum = self._build_complete_curriculum_structure(
            mode='plan_b',
            role_id=role_id,
            role_name=role_name,
            topic=topic,
            eqf_level=eqf_level,
            target_ects=target_ects,
            selected_modules=selected_modules,
            semesters=semesters,
            educational_profile=educational_profile,
            selection_metadata=selection_metadata,
            role_info=role_info
        )
        
        print(f"✅ PLAN B: Direct curriculum generated successfully!")
        return curriculum

    def build_curriculum_auto_mode(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any] = None,
        prefer_profile_first: bool = True
    ) -> Dict[str, Any]:
        """
        AUTO MODE: Intelligently choose between Profile-First and Plan B
        """
        
        print(f"\n🎯 AUTO MODE: Intelligent curriculum generation")
        
        if prefer_profile_first:
            try:
                # Attempt Profile-First mode
                curriculum = self.build_curriculum_profile_first(
                    role_id, role_name, topic, eqf_level, target_ects, role_info
                )
                
                # Validate quality of profile-first result
                if self._validate_profile_first_quality(curriculum):
                    print(f"✅ AUTO MODE: Using Profile-First curriculum (high quality)")
                    return curriculum
                else:
                    print(f"⚠️ AUTO MODE: Profile-First quality insufficient, using Plan B")
            
            except Exception as e:
                print(f"⚠️ AUTO MODE: Profile-First failed ({e}), using Plan B")
        
        # Fallback to Plan B
        return self.build_curriculum_plan_b(
            role_id, role_name, topic, eqf_level, target_ects, role_info
        )

    def _organize_competency_based_semesters(
        self,
        selected_modules: List[Dict[str, Any]],
        educational_profile: Dict[str, Any],
        target_ects: int
    ) -> List[Dict[str, Any]]:
        """Organize modules into semesters based on competency development progression"""
        
        # Extract competency structure
        enhanced_competencies = educational_profile.get('enhanced_competencies', [])
        modular_structure = educational_profile.get('modular_structure', {})
        
        # Determine number of semesters
        num_semesters = max(1, target_ects // 90)  # Roughly 90 ECTS per year
        target_ects_per_semester = target_ects // num_semesters
        
        print(f"📅 Organizing {len(selected_modules)} modules into {num_semesters} competency-based semesters")
        
        semesters = []
        
        # Categorize modules by competency level/type
        foundational_modules = []
        specialized_modules = []
        advanced_modules = []
        
        for module in selected_modules:
            module_eqf = module.get('eqf_level', 6)
            module_name = module.get('name', '').lower()
            
            # Categorize based on content and EQF level
            if 'foundation' in module_name or 'introduction' in module_name or 'basic' in module_name:
                foundational_modules.append(module)
            elif 'advanced' in module_name or 'expert' in module_name or module_eqf >= 7:
                advanced_modules.append(module)
            else:
                specialized_modules.append(module)
        
        # Distribute modules across semesters with competency progression
        if num_semesters == 1:
            # Single semester - mix all types
            semesters.append(self._create_semester(
                semester_number=1,
                modules=selected_modules,
                focus_area="Comprehensive Digital Sustainability",
                competency_focus=enhanced_competencies[:3] if enhanced_competencies else []
            ))
        
        elif num_semesters == 2:
            # Two semesters - foundation + specialization
            semester_1_modules = foundational_modules + specialized_modules[:len(specialized_modules)//2]
            semester_2_modules = specialized_modules[len(specialized_modules)//2:] + advanced_modules
            
            semesters.append(self._create_semester(
                semester_number=1,
                modules=semester_1_modules,
                focus_area="Foundation and Core Competencies",
                competency_focus=enhanced_competencies[:len(enhanced_competencies)//2]
            ))
            
            semesters.append(self._create_semester(
                semester_number=2,
                modules=semester_2_modules,
                focus_area="Advanced Practice and Specialization",
                competency_focus=enhanced_competencies[len(enhanced_competencies)//2:]
            ))
        
        else:
            # Multiple semesters - progressive competency development
            modules_per_semester = len(selected_modules) // num_semesters
            
            for i in range(num_semesters):
                start_idx = i * modules_per_semester
                end_idx = start_idx + modules_per_semester if i < num_semesters - 1 else len(selected_modules)
                
                semester_modules = selected_modules[start_idx:end_idx]
                competency_start = (i * len(enhanced_competencies)) // num_semesters
                competency_end = ((i + 1) * len(enhanced_competencies)) // num_semesters
                
                focus_areas = ["Foundation", "Development", "Specialization", "Advanced Practice", "Mastery"]
                focus_area = focus_areas[min(i, len(focus_areas) - 1)]
                
                semesters.append(self._create_semester(
                    semester_number=i + 1,
                    modules=semester_modules,
                    focus_area=focus_area,
                    competency_focus=enhanced_competencies[competency_start:competency_end]
                ))
        
        print(f"   ✅ Created {len(semesters)} competency-based semesters")
        return semesters

    def _organize_standard_semesters(
        self,
        selected_modules: List[Dict[str, Any]],
        target_ects: int
    ) -> List[Dict[str, Any]]:
        """Organize modules into standard semesters (Plan B mode)"""
        
        num_semesters = max(1, target_ects // 90)
        modules_per_semester = len(selected_modules) // num_semesters
        
        print(f"📅 Organizing {len(selected_modules)} modules into {num_semesters} standard semesters")
        
        semesters = []
        
        for i in range(num_semesters):
            start_idx = i * modules_per_semester
            end_idx = start_idx + modules_per_semester if i < num_semesters - 1 else len(selected_modules)
            
            semester_modules = selected_modules[start_idx:end_idx]
            
            semesters.append(self._create_semester(
                semester_number=i + 1,
                modules=semester_modules,
                focus_area=f"Semester {i + 1} Focus",
                competency_focus=[]
            ))
        
        return semesters

    def _create_semester(
        self,
        semester_number: int,
        modules: List[Dict[str, Any]],
        focus_area: str,
        competency_focus: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create detailed semester structure"""
        
        semester_ects = sum(m.get('ects', 5) for m in modules)
        competency_focus = competency_focus or []
        
        # Generate learning objectives from competency focus
        learning_objectives = []
        if competency_focus:
            for comp in competency_focus:
                comp_outcomes = comp.get('learning_outcomes', [])
                learning_objectives.extend(comp_outcomes[:2])  # Take first 2 outcomes per competency
        
        if not learning_objectives:
            learning_objectives = [
                f"Complete {focus_area.lower()} modules successfully",
                f"Demonstrate competency in semester {semester_number} focus areas",
                f"Apply learning to practical sustainability challenges"
            ]
        
        return {
            'semester_number': semester_number,
            'semester_name': f"Semester {semester_number}",
            'focus_area': focus_area,
            'target_ects': semester_ects,
            'duration_weeks': 15,
            'modules': [self._format_module_for_semester(m) for m in modules],
            'learning_objectives': learning_objectives[:5],  # Limit to 5 objectives
            'competency_focus': [comp.get('competency_name', '') for comp in competency_focus],
            'assessment_strategy': {
                'formative_assessment': True,
                'competency_based': bool(competency_focus),
                'portfolio_development': semester_number > 1,
                'capstone_project': semester_number == max(2, semester_number) and semester_ects >= 30
            },
            'work_based_percentage': 0.2 if any(m.get('is_work_based', False) for m in modules) else 0.0
        }

    def _format_module_for_semester(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """Format module for semester display"""
        return {
            'module_id': module.get('id', ''),
            'module_name': module.get('name', ''),
            'module_code': module.get('code', module.get('id', '')),
            'title': module.get('name', ''),
            'ects': module.get('ects', 5),
            'thematic_area': module.get('thematic_area', 'General'),
            'eqf_level': module.get('eqf_level', 6),
            'delivery_methods': module.get('delivery_methods', ['blended']),
            'is_work_based': module.get('is_work_based', False)
        }

    def _generate_basic_educational_profile(
        self,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        role_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate basic educational profile for Plan B mode"""
        
        role_info = role_info or self.role_definitions.get(role_id, {})
        
        return {
            'profile_id': f"EP_{role_id}_{eqf_level}_{datetime.now().strftime('%Y%m%d')}",
            'role_id': role_id,
            'role_name': role_name,
            'profile_title': f'{role_name} Educational Profile',
            'profile_type': 'standard_direct',
            'creation_date': datetime.now().isoformat(),
            'version': '3.1_plan_b',
            'target_eqf_level': eqf_level,
            'target_ects': target_ects,
            'topic_focus': topic,
            'generation_mode': 'plan_b',
            'learning_mode': 'topic_based',
            'delivery_methods': ['blended', 'online'],
            'entry_requirements': self._get_basic_entry_requirements(eqf_level),
            'assessment_methods': self._get_basic_assessment_methods(eqf_level),
            'role_context': {
                'main_area': role_info.get('main_area', 'Digital Sustainability'),
                'industry_sectors': role_info.get('industry_sectors', ['Technology', 'Consulting']),
                'career_pathways': ['Professional', 'Senior Professional', 'Team Lead'],
                'typical_employers': ['Technology Companies', 'Consulting Firms', 'Government']
            }
        }

    def _build_complete_curriculum_structure(
        self,
        mode: str,
        role_id: str,
        role_name: str,
        topic: str,
        eqf_level: int,
        target_ects: int,
        selected_modules: List[Dict[str, Any]],
        semesters: List[Dict[str, Any]],
        educational_profile: Dict[str, Any],
        selection_metadata: Dict[str, Any],
        role_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Build complete curriculum structure with enhanced metadata"""
        
        actual_ects = sum(m.get('ects', 5) for m in selected_modules)
        
        curriculum = {
            'curriculum_id': f"CURR_{role_id}_{topic.upper().replace(' ', '_')}_{eqf_level}_{datetime.now().strftime('%Y%m%d')}",
            'metadata': {
                'title': f"{role_name} in {topic}",
                'role_id': role_id,
                'role_name': role_name,
                'topic': topic,
                'eqf_level': eqf_level,
                'target_ects': target_ects,
                'actual_ects': actual_ects,
                'num_semesters': len(semesters),
                'num_modules': len(selected_modules),
                'generated_date': datetime.now().isoformat(),
                'generation_mode': mode,
                'compliance_frameworks': ['T3.2', 'T3.4', 'EQF', 'ECTS', 'ECVET'],
                'generator_version': 'DSCG v3.1-DUAL_MODE'
            },
            'educational_profile': educational_profile,
            'curriculum_structure': {
                'semester_breakdown': semesters,
                'total_semesters': len(semesters),
                'modular_design': True,
                'flexible_pathways': mode == 'profile_first',
                'competency_based': mode == 'profile_first'
            },
            'modules': self._format_modules_for_output(selected_modules),
            'learning_pathways': self._build_learning_pathways(semesters, mode),
            'assessment_framework': self._build_assessment_framework(semesters, educational_profile, mode),
            'quality_metrics': self._calculate_enhanced_quality_metrics(
                selected_modules, target_ects, selection_metadata, mode
            ),
            'selection_metadata': selection_metadata,
            'competency_framework': self._extract_competency_framework(educational_profile) if mode == 'profile_first' else None
        }
        
        return curriculum

    def _format_modules_for_output(self, modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format modules for curriculum output"""
        return [
            {
                'id': module.get('id', ''),
                'title': module.get('name', ''),
                'code': module.get('code', module.get('id', '')),
                'description': module.get('description', ''),
                'ects': module.get('ects', 5),
                'eqf_level': module.get('eqf_level', 6),
                'thematic_area': module.get('thematic_area', 'General'),
                'topics': module.get('topics', []),
                'skills': module.get('skills', []),
                'prerequisites': module.get('prerequisites', []),
                'delivery_methods': module.get('delivery_methods', ['blended']),
                'is_work_based': module.get('is_work_based', False)
            }
            for module in modules
        ]

    def _validate_profile_first_quality(self, curriculum: Dict[str, Any]) -> bool:
        """Validate quality of profile-first curriculum generation"""
        
        educational_profile = curriculum.get('educational_profile', {})
        selection_metadata = curriculum.get('selection_metadata', {})
        
        # Check if rich competency data is present
        has_competencies = len(educational_profile.get('enhanced_competencies', [])) >= 3
        
        # Check competency coverage
        competency_req = selection_metadata.get('competency_requirements', {})
        topic_coverage = competency_req.get('topic_coverage_percentage', 0)
        has_good_coverage = topic_coverage >= 60
        
        # Check module selection quality
        ects_efficiency = selection_metadata.get('ects_efficiency', 0)
        has_good_ects = ects_efficiency >= 80
        
        return has_competencies and has_good_coverage and has_good_ects

    def _build_learning_pathways(self, semesters: List[Dict], mode: str) -> Dict[str, Any]:
        """Build learning pathways based on mode"""
        if mode == 'profile_first':
            return {
                'competency_driven_pathway': {
                    'description': 'Competency-based progression through sustainability expertise',
                    'duration_months': len(semesters) * 4,
                    'flexibility': 'high',
                    'competency_checkpoints': len(semesters)
                },
                'accelerated_pathway': {
                    'description': 'Intensive competency development',
                    'duration_months': max(1, len(semesters) * 3),
                    'flexibility': 'medium'
                }
            }
        else:
            return {
                'linear_pathway': {
                    'description': 'Standard semester-by-semester progression',
                    'duration_months': len(semesters) * 4,
                    'flexibility': 'medium'
                }
            }

    def _build_assessment_framework(self, semesters: List[Dict], educational_profile: Dict, mode: str) -> Dict[str, Any]:
        """Build assessment framework based on mode and profile"""
        
        base_framework = {
            'assessment_principles': [
                'Continuous assessment',
                'Portfolio development',
                'Applied learning demonstration'
            ]
        }
        
        if mode == 'profile_first':
            enhanced_competencies = educational_profile.get('enhanced_competencies', [])
            
            base_framework.update({
                'competency_based_assessment': True,
                'competency_checkpoints': len(enhanced_competencies),
                'assessment_methods': list(set([
                    method 
                    for comp in enhanced_competencies 
                    for method in comp.get('assessment_methods', [])
                ])),
                'capstone_requirements': {
                    'required': len(semesters) >= 2,
                    'format': 'competency_portfolio',
                    'ects_allocation': min(15, sum(s.get('target_ects', 0) for s in semesters) * 0.1)
                }
            })
        else:
            base_framework.update({
                'topic_based_assessment': True,
                'capstone_requirements': {
                    'required': len(semesters) >= 2,
                    'format': 'project',
                    'ects_allocation': 10
                }
            })
        
        return base_framework

    def _calculate_enhanced_quality_metrics(
        self, 
        modules: List[Dict], 
        target_ects: int, 
        selection_metadata: Dict, 
        mode: str
    ) -> Dict[str, Any]:
        """Calculate enhanced quality metrics based on selection mode"""
        
        actual_ects = sum(m.get('ects', 5) for m in modules)
        ects_efficiency = selection_metadata.get('ects_efficiency', 
                                               min((actual_ects / target_ects) * 100, 100) if target_ects > 0 else 100)
        
        base_metrics = {
            'ects_efficiency': round(ects_efficiency, 1),
            'module_count': len(modules),
            'selection_mode': mode
        }
        
        if mode == 'profile_first':
            competency_req = selection_metadata.get('competency_requirements', {})
            base_metrics.update({
                'competency_coverage': round(competency_req.get('topic_coverage_percentage', 0), 1),
                'competency_alignment': 'high' if competency_req.get('topic_coverage_percentage', 0) >= 70 else 'medium',
                'topic_relevance': 8.5,  # High for competency-driven
                'pedagogical_coherence': 9.0  # High for competency-based design
            })
        else:
            topic_analysis = selection_metadata.get('topic_analysis', {})
            base_metrics.update({
                'topic_relevance': round(min(topic_analysis.get('average_topic_relevance', 0) / 10, 10), 1),
                'topic_coverage': 75.0,  # Standard for direct mode
                'flexibility_score': 70.0
            })
        
        return base_metrics

    def _extract_competency_framework(self, educational_profile: Dict) -> Dict[str, Any]:
        """Extract competency framework for curriculum metadata"""
        
        enhanced_competencies = educational_profile.get('enhanced_competencies', [])
        
        return {
            'total_competencies': len(enhanced_competencies),
            'competency_categories': list(set([
                comp.get('competency_category', 'General') 
                for comp in enhanced_competencies
            ])),
            'competency_levels': list(set([
                comp.get('competency_level', 'Standard')
                for comp in enhanced_competencies
            ])),
            'framework_mappings': {
                'DigComp': list(set([
                    mapping
                    for comp in enhanced_competencies
                    for mapping in comp.get('framework_mappings', {}).get('DigComp', [])
                ])),
                'GreenComp': list(set([
                    mapping
                    for comp in enhanced_competencies  
                    for mapping in comp.get('framework_mappings', {}).get('GreenComp', [])
                ]))
            }
        }

    def _get_basic_entry_requirements(self, eqf_level: int) -> Dict[str, str]:
        """Get basic entry requirements based on EQF level"""
        if eqf_level >= 7:
            return {
                'academic': "Bachelor's degree or equivalent",
                'professional': "2-3 years relevant experience",
                'technical': "Digital literacy and sustainability awareness"
            }
        else:
            return {
                'academic': "Upper secondary education or equivalent",
                'professional': "Basic work experience preferred",
                'technical': "Basic digital skills"
            }

    def _get_basic_assessment_methods(self, eqf_level: int) -> List[str]:
        """Get basic assessment methods based on EQF level"""
        base_methods = ['Portfolio assessment', 'Project work', 'Written assignment']
        
        if eqf_level >= 7:
            base_methods.extend(['Research project', 'Professional presentation', 'Case study analysis'])
        
        return base_methods

    # Backward compatibility method
    def build_curriculum_with_semesters(self, role_id: str, role_name: str, topic: str, eqf_level: int, target_ects: int, role_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Backward compatibility method - defaults to auto mode with profile-first preference"""
        return self.build_curriculum_auto_mode(
            role_id=role_id,
            role_name=role_name, 
            topic=topic,
            eqf_level=eqf_level,
            target_ects=target_ects,
            role_info=role_info,
            prefer_profile_first=True
        )
