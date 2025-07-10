"""
Learning pathway generator component.
Creates structured learning paths and progression routes through the curriculum.
"""

from typing import Dict, List, Any, Optional, Tuple
import math


class PathwayGenerator:
    """Generates learning pathways and progression routes"""
    
    def __init__(self, domain_knowledge):
        self.domain_knowledge = domain_knowledge
        
    def generate_pathways(
        self,
        topic: str,
        eqf_level: int,
        selected_modules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate comprehensive learning pathways"""
        
        print(f"🛤️  Generating learning pathways for {len(selected_modules)} modules")
        
        # Generate different pathway types
        pathways = {
            "recommended_sequence": self._generate_recommended_sequence(selected_modules),
            "flexible_pathways": self._generate_flexible_pathways(selected_modules, topic),
            "specialization_tracks": self._generate_specialization_tracks(selected_modules, topic),
            "fast_track_options": self._generate_fast_track_options(selected_modules),
            "part_time_progression": self._generate_part_time_progression(selected_modules),
            "prerequisite_flow": self._generate_prerequisite_flow(selected_modules),
            "competency_progression": self._generate_competency_progression(selected_modules, topic)
        }
        
        print(f"✅ Generated {len(pathways)} pathway types")
        return pathways
        
    def _generate_recommended_sequence(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the recommended learning sequence"""
        
        # Sort modules by complexity and prerequisites
        def module_priority(module):
            score = 0
            
            # Favor modules with fewer prerequisites
            prereqs = module.get('prerequisites', [])
            if isinstance(prereqs, str):
                prereqs = [prereqs] if prereqs else []
            score -= len(prereqs) * 10
            
            # Consider complexity
            complexity = module.get('complexity', 'intermediate')
            complexity_scores = {'basic': -5, 'intermediate': 0, 'advanced': 5}
            score += complexity_scores.get(complexity, 0)
            
            # Consider EQF level
            score += module.get('eqf_level', 6) * 2
            
            # Favor foundational modules
            title_lower = module.get('title', '').lower()
            if any(word in title_lower for word in ['foundation', 'introduction', 'basic', 'fundamentals']):
                score -= 20
            elif any(word in title_lower for word in ['advanced', 'specialized', 'expert']):
                score += 15
                
            return score
            
        sorted_modules = sorted(modules, key=module_priority)
        
        # Create sequence with timing
        sequence = []
        current_period = 1
        current_ects = 0
        period_limit = 30  # ECTS per period
        
        for i, module in enumerate(sorted_modules):
            module_ects = module.get('ects', 5)
            
            # Check if we need to move to next period
            if current_ects + module_ects > period_limit and current_ects > 0:
                current_period += 1
                current_ects = 0
                
            sequence.append({
                "sequence_number": i + 1,
                "module_title": module['title'],
                "academic_period": current_period,
                "ects": module_ects,
                "cumulative_ects": sum(m.get('ects', 5) for m in sorted_modules[:i+1]),
                "rationale": self._get_placement_rationale(module, current_period, i)
            })
            
            current_ects += module_ects
            
        return {
            "total_periods": current_period,
            "sequence": sequence,
            "progression_notes": self._generate_progression_notes(sequence)
        }
        
    def _get_placement_rationale(self, module: Dict[str, Any], period: int, position: int) -> str:
        """Generate rationale for module placement"""
        
        rationales = []
        
        # Period-based rationale
        if period == 1:
            rationales.append("foundational learning")
        elif period == 2:
            rationales.append("skill development")
        else:
            rationales.append("advanced application")
            
        # Prerequisites rationale
        prereqs = module.get('prerequisites', [])
        if isinstance(prereqs, str):
            prereqs = [prereqs] if prereqs else []
        if prereqs:
            rationales.append("builds on prerequisite knowledge")
        else:
            rationales.append("no prerequisites required")
            
        # Complexity rationale
        complexity = module.get('complexity', 'intermediate')
        if complexity == 'basic':
            rationales.append("introductory level")
        elif complexity == 'advanced':
            rationales.append("requires solid foundation")
            
        return "; ".join(rationales)
        
    def _generate_progression_notes(self, sequence: List[Dict[str, Any]]) -> List[str]:
        """Generate notes about learning progression"""
        
        notes = []
        
        # Analyze progression
        periods = max(item['academic_period'] for item in sequence)
        if periods == 1:
            notes.append("Intensive single-period program requiring full-time commitment")
        elif periods == 2:
            notes.append("Two-period program allowing gradual skill development")
        else:
            notes.append(f"Extended {periods}-period program with comprehensive coverage")
            
        # Check for prerequisite flows
        prereq_modules = [item for item in sequence if 'prerequisite' in item['rationale']]
        if prereq_modules:
            notes.append(f"{len(prereq_modules)} modules have prerequisite dependencies")
            
        # Check ECTS distribution
        period_ects = {}
        for item in sequence:
            period = item['academic_period']
            period_ects[period] = period_ects.get(period, 0) + item['ects']
            
        balanced = all(20 <= ects <= 35 for ects in period_ects.values())
        if balanced:
            notes.append("Well-balanced ECTS distribution across periods")
        else:
            notes.append("Consider reviewing ECTS distribution for optimal workload")
            
        return notes
        
    def _generate_flexible_pathways(
        self, 
        modules: List[Dict[str, Any]], 
        topic: str
    ) -> List[Dict[str, Any]]:
        """Generate flexible pathway options"""
        
        pathways = []
        
        # Group modules by theme
        theme_groups = self._group_modules_by_theme(modules)
        
        # Create pathways based on different focuses
        focus_areas = self.domain_knowledge.get_specializations(topic)
        
        for focus in focus_areas[:3]:  # Limit to 3 flexible pathways
            pathway_modules = self._select_modules_for_focus(modules, focus)
            
            if len(pathway_modules) >= 3:  # Minimum viable pathway
                pathways.append({
                    "pathway_name": f"{focus} Focus",
                    "description": f"Specialized pathway emphasizing {focus.lower()}",
                    "modules": [m['title'] for m in pathway_modules],
                    "total_ects": sum(m.get('ects', 5) for m in pathway_modules),
                    "duration_estimate": f"{math.ceil(len(pathway_modules) / 4)} periods",
                    "target_competencies": self._get_focus_competencies(focus, topic)
                })
                
        # Add general flexible pathway
        pathways.append({
            "pathway_name": "Flexible General Track",
            "description": "Customizable pathway allowing student choice",
            "modules": [m['title'] for m in modules],
            "selection_criteria": "Students select based on interests and career goals",
            "minimum_core_modules": len(modules) // 2,
            "elective_options": len(modules) - (len(modules) // 2)
        })
        
        return pathways
        
    def _group_modules_by_theme(self, modules: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group modules by thematic similarity"""
        
        themes = {
            "technical": [],
            "management": [],
            "research": [],
            "practical": []
        }
        
        for module in modules:
            title_desc = (module.get('title', '') + ' ' + module.get('description', '')).lower()
            
            # Classify module
            if any(word in title_desc for word in ['management', 'strategy', 'governance', 'policy']):
                themes["management"].append(module)
            elif any(word in title_desc for word in ['research', 'analysis', 'study', 'investigation']):
                themes["research"].append(module)
            elif any(word in title_desc for word in ['practical', 'implementation', 'project', 'application']):
                themes["practical"].append(module)
            else:
                themes["technical"].append(module)
                
        return {k: v for k, v in themes.items() if v}  # Remove empty themes
        
    def _select_modules_for_focus(self, modules: List[Dict[str, Any]], focus: str) -> List[Dict[str, Any]]:
        """Select modules relevant to a specific focus area"""
        
        focus_keywords = focus.lower().split()
        relevant_modules = []
        
        for module in modules:
            relevance_score = 0
            module_text = (
                module.get('title', '') + ' ' + 
                module.get('description', '') + ' ' +
                ' '.join(module.get('keywords', []))
            ).lower()
            
            # Score based on keyword matches
            for keyword in focus_keywords:
                if keyword in module_text:
                    relevance_score += 2
                    
            # Bonus for exact focus match in title
            if focus.lower() in module.get('title', '').lower():
                relevance_score += 5
                
            if relevance_score > 0:
                module_copy = module.copy()
                module_copy['focus_relevance'] = relevance_score
                relevant_modules.append(module_copy)
                
        # Sort by relevance and return top modules
        relevant_modules.sort(key=lambda x: x['focus_relevance'], reverse=True)
        return relevant_modules[:6]  # Limit to 6 modules per focus
        
    def _get_focus_competencies(self, focus: str, topic: str) -> List[str]:
        """Get competencies for a specific focus area"""
        
        base_competencies = self.domain_knowledge.get_competency_mappings(topic)
        focus_competencies = []
        
        # Add focus-specific competencies
        if "software" in focus.lower():
            focus_competencies.extend([
                "Software design and development",
                "Code optimization techniques",
                "Software architecture principles"
            ])
        elif "measurement" in focus.lower():
            focus_competencies.extend([
                "Data analysis and interpretation",
                "Metrics design and implementation",
                "Reporting and communication"
            ])
        elif "management" in focus.lower():
            focus_competencies.extend([
                "Project management",
                "Strategic planning",
                "Team leadership"
            ])
        else:
            focus_competencies.extend([
                f"Specialized knowledge in {focus.lower()}",
                f"Practical application of {focus.lower()}",
                f"Problem-solving in {focus.lower()}"
            ])
            
        return focus_competencies[:5]  # Limit to 5 key competencies
        
    def _generate_specialization_tracks(
        self, 
        modules: List[Dict[str, Any]], 
        topic: str
    ) -> List[Dict[str, Any]]:
        """Generate specialization tracks"""
        
        specializations = self.domain_knowledge.get_specializations(topic)
        tracks = []
        
        for spec in specializations:
            track_modules = []
            core_modules = []
            elective_modules = []
            
            # Find modules matching this specialization
            for module in modules:
                relevance = self.domain_knowledge.score_module_relevance(module, spec)
                if relevance > 3:
                    if relevance > 6:
                        core_modules.append(module)
                    else:
                        elective_modules.append(module)
                        
            if core_modules:  # Only create track if we have core modules
                tracks.append({
                    "track_name": spec,
                    "description": f"Specialized track focusing on {spec.lower()}",
                    "core_modules": [m['title'] for m in core_modules],
                    "elective_modules": [m['title'] for m in elective_modules],
                    "total_ects": sum(m.get('ects', 5) for m in core_modules + elective_modules),
                    "career_outcomes": self._get_specialization_careers(spec),
                    "industry_relevance": self.domain_knowledge.get_industry_relevance(spec)
                })
                
        return tracks
        
    def _get_specialization_careers(self, specialization: str) -> List[str]:
        """Get career outcomes for specialization"""
        
        career_map = {
            "Green Coding Practices": [
                "Sustainable Software Developer",
                "Green IT Consultant",
                "Environmental Software Engineer"
            ],
            "Carbon Metrics": [
                "Carbon Analyst",
                "Sustainability Consultant",
                "Environmental Data Scientist"
            ],
            "Energy-Efficient Algorithms": [
                "Performance Engineer",
                "Green Computing Specialist",
                "Algorithm Optimization Expert"
            ]
        }
        
        return career_map.get(specialization, [
            f"{specialization} Specialist",
            f"{specialization} Consultant",
            f"{specialization} Manager"
        ])
        
    def _generate_fast_track_options(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate fast-track completion options"""
        
        total_ects = sum(module.get('ects', 5) for module in modules)
        
        # Intensive option
        intensive_duration = max(1, total_ects // 45)  # 45 ECTS per period max
        
        # Accelerated option  
        accelerated_duration = max(2, total_ects // 35)  # 35 ECTS per period
        
        return {
            "intensive_track": {
                "duration_periods": intensive_duration,
                "ects_per_period": total_ects // intensive_duration if intensive_duration > 0 else total_ects,
                "description": "Intensive full-time study with high workload",
                "requirements": ["Full-time availability", "Strong academic background"],
                "support_needed": ["Academic mentoring", "Peer study groups"]
            },
            "accelerated_track": {
                "duration_periods": accelerated_duration,
                "ects_per_period": total_ects // accelerated_duration if accelerated_duration > 0 else total_ects,
                "description": "Accelerated pace with moderate workload increase",
                "requirements": ["Good time management skills", "Prior experience preferred"],
                "support_needed": ["Regular check-ins", "Flexible scheduling"]
            },
            "prerequisites": self._identify_fast_track_prerequisites(modules)
        }
        
    def _generate_part_time_progression(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate part-time study progression"""
        
        total_ects = sum(module.get('ects', 5) for module in modules)
        
        # Standard part-time: 15-20 ECTS per period
        standard_duration = math.ceil(total_ects / 18)
        
        # Flexible part-time: 10-15 ECTS per period
        flexible_duration = math.ceil(total_ects / 12)
        
        return {
            "standard_part_time": {
                "duration_periods": standard_duration,
                "ects_per_period": "15-20",
                "time_commitment": "15-20 hours per week",
                "schedule_options": ["Evening classes", "Weekend intensives"],
                "module_sequencing": self._create_part_time_sequence(modules, 18)
            },
            "flexible_part_time": {
                "duration_periods": flexible_duration,
                "ects_per_period": "10-15", 
                "time_commitment": "10-15 hours per week",
                "schedule_options": ["Online learning", "Self-paced modules"],
                "module_sequencing": self._create_part_time_sequence(modules, 12)
            }
        }
        
    def _create_part_time_sequence(self, modules: List[Dict[str, Any]], ects_per_period: int) -> List[Dict[str, Any]]:
        """Create sequence optimized for part-time study"""
        
        sequence = []
        current_period = 1
        current_ects = 0
        
        # Sort modules for part-time suitability
        def part_time_priority(module):
            score = 0
            
            # Favor smaller modules for part-time study
            ects = module.get('ects', 5)
            if ects <= 5:
                score += 10
            elif ects >= 10:
                score -= 5
                
            # Favor theoretical over practical for part-time
            title = module.get('title', '').lower()
            if any(word in title for word in ['theory', 'principles', 'concepts']):
                score += 5
            elif any(word in title for word in ['lab', 'practical', 'workshop']):
                score -= 3
                
            return score
            
        sorted_modules = sorted(modules, key=part_time_priority, reverse=True)
        
        for module in sorted_modules:
            module_ects = module.get('ects', 5)
            
            if current_ects + module_ects > ects_per_period and current_ects > 0:
                current_period += 1
                current_ects = 0
                
            sequence.append({
                "period": current_period,
                "module": module['title'],
                "ects": module_ects,
                "delivery_mode": self._suggest_delivery_mode(module)
            })
            
            current_ects += module_ects
            
        return sequence
        
    def _suggest_delivery_mode(self, module: Dict[str, Any]) -> str:
        """Suggest delivery mode for part-time study"""
        
        title = module.get('title', '').lower()
        
        if any(word in title for word in ['practical', 'lab', 'workshop', 'project']):
            return "blended"
        elif any(word in title for word in ['theory', 'principles', 'analysis']):
            return "online"
        else:
            return "flexible"
            
    def _generate_prerequisite_flow(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate prerequisite flow diagram data"""
        
        flow = {
            "nodes": [],
            "connections": [],
            "levels": {}
        }
        
        # Create nodes for each module
        for i, module in enumerate(modules):
            flow["nodes"].append({
                "id": f"module_{i}",
                "title": module['title'],
                "ects": module.get('ects', 5),
                "eqf_level": module.get('eqf_level', 6)
            })
            
        # Create connections based on prerequisites
        for i, module in enumerate(modules):
            prereqs = module.get('prerequisites', [])
            if isinstance(prereqs, str):
                prereqs = [prereqs] if prereqs else []
                
            for prereq in prereqs:
                # Find prerequisite module
                for j, prereq_module in enumerate(modules):
                    if prereq.lower() in prereq_module.get('title', '').lower():
                        flow["connections"].append({
                            "from": f"module_{j}",
                            "to": f"module_{i}",
                            "type": "prerequisite"
                        })
                        
        return flow
        
    def _generate_competency_progression(
        self, 
        modules: List[Dict[str, Any]], 
        topic: str
    ) -> Dict[str, Any]:
        """Generate competency-based progression mapping"""
        
        competencies = self.domain_knowledge.get_competency_mappings(topic)
        
        progression = {
            "competency_levels": ["Awareness", "Understanding", "Application", "Mastery"],
            "competency_map": {},
            "module_competency_matrix": []
        }
        
        # Map modules to competencies and levels
        for module in modules:
            module_competencies = module.get('competencies', {})
            complexity = module.get('complexity', 'intermediate')
            
            # Determine competency level based on module complexity
            if complexity == 'basic':
                level = "Understanding"
            elif complexity == 'intermediate':
                level = "Application"
            else:
                level = "Mastery"
                
            progression["module_competency_matrix"].append({
                "module": module['title'],
                "competency_level": level,
                "developed_competencies": list(module_competencies.keys()) if module_competencies else [],
                "ects_contribution": module.get('ects', 5)
            })
            
        return progression
        
    def _identify_fast_track_prerequisites(self, modules: List[Dict[str, Any]]) -> List[str]:
        """Identify prerequisites for fast-track options"""
        
        prerequisites = [
            "Strong foundational knowledge in sustainability concepts",
            "Basic understanding of digital technologies",
            "Ability to commit to intensive study schedule"
        ]
        
        # Add specific prerequisites based on module complexity
        advanced_modules = [m for m in modules if m.get('complexity') == 'advanced']
        if len(advanced_modules) > len(modules) / 2:
            prerequisites.extend([
                "Prior experience in the field",
                "Strong analytical and problem-solving skills"
            ])
            
        return prerequisites
