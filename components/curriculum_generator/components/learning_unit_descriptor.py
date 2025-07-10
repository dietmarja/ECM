#!/usr/bin/env python3
# scripts/curriculum_generator/components/learning_unit_descriptor.py
"""
Learning Unit Descriptor - Detailed time and ECTS breakdowns
Provides comprehensive descriptions of learning unit structure and duration
"""

import math
from typing import Dict, List, Any, Tuple
from datetime import timedelta

class LearningUnitDescriptor:
    """Manages detailed descriptions and time allocations for learning units"""
    
    def __init__(self):
        # Standard conversion rates
        self.ects_to_hours = 25  # 1 ECTS = 25-30 hours (using 25 for conservative estimate)
        self.study_hours_per_day = 8  # Full study day
        self.contact_hours_per_day = 6  # Contact/teaching time per day
        self.minutes_per_hour = 60
        
        # Learning activity breakdowns (percentages of total time)
        self.activity_breakdown = {
            'contact_learning': 0.40,     # 40% - lectures, seminars, workshops
            'guided_practice': 0.25,      # 25% - exercises, labs, tutorials  
            'independent_study': 0.20,    # 20% - reading, research, preparation
            'assessment_prep': 0.10,      # 10% - assignment work, exam prep
            'reflection_review': 0.05     # 5% - consolidation, review
        }
        
        # Delivery mode adjustments
        self.delivery_adjustments = {
            'intensive': {
                'days_per_week': 5,
                'hours_per_day': 8,
                'description': 'Full-time intensive delivery'
            },
            'standard': {
                'days_per_week': 3,
                'hours_per_day': 6,
                'description': 'Standard part-time delivery'
            },
            'flexible': {
                'days_per_week': 2,
                'hours_per_day': 4,
                'description': 'Flexible/evening delivery'
            },
            'online': {
                'days_per_week': 7,
                'hours_per_day': 3,
                'description': 'Self-paced online delivery'
            }
        }
    
    def calculate_unit_duration(self, ects: float, delivery_mode: str = 'standard') -> Dict[str, Any]:
        """Calculate detailed duration breakdown for a learning unit"""
        
        # Basic calculations
        total_hours = ects * self.ects_to_hours
        delivery_info = self.delivery_adjustments.get(delivery_mode, self.delivery_adjustments['standard'])
        
        # Calculate days and weeks
        hours_per_week = delivery_info['days_per_week'] * delivery_info['hours_per_day']
        total_weeks = math.ceil(total_hours / hours_per_week)
        total_days = math.ceil(total_hours / delivery_info['hours_per_day'])
        
        # Activity breakdown
        activities = {}
        for activity, percentage in self.activity_breakdown.items():
            activity_hours = total_hours * percentage
            activity_days = activity_hours / delivery_info['hours_per_day']
            activities[activity] = {
                'hours': round(activity_hours, 1),
                'days': round(activity_days, 1),
                'minutes': round(activity_hours * self.minutes_per_hour),
                'percentage': int(percentage * 100)
            }
        
        return {
            'ects': ects,
            'total_hours': total_hours,
            'total_days': total_days,
            'total_weeks': total_weeks,
            'total_minutes': total_hours * self.minutes_per_hour,
            'delivery_mode': delivery_mode,
            'delivery_description': delivery_info['description'],
            'schedule': {
                'days_per_week': delivery_info['days_per_week'],
                'hours_per_day': delivery_info['hours_per_day'],
                'hours_per_week': hours_per_week
            },
            'activity_breakdown': activities,
            'completion_timeframe': self._generate_completion_timeframe(total_weeks, delivery_mode)
        }
    
    def _generate_completion_timeframe(self, weeks: int, delivery_mode: str) -> str:
        """Generate human-readable completion timeframe"""
        if delivery_mode == 'intensive':
            if weeks <= 1:
                return f"Completed in {weeks} week (intensive format)"
            else:
                return f"Completed in {weeks} weeks (intensive format)"
        elif delivery_mode == 'online':
            return f"Self-paced completion in {weeks}-{weeks*2} weeks"
        else:
            if weeks <= 4:
                return f"Completed in {weeks} weeks"
            else:
                months = math.ceil(weeks / 4)
                return f"Completed in approximately {months} month(s)"
    
    def describe_learning_unit_structure(self, unit_number: int, ects: float, total_units: int, 
                                       topic: str, delivery_mode: str = 'standard') -> Dict[str, Any]:
        """Generate comprehensive learning unit description"""
        
        duration = self.calculate_unit_duration(ects, delivery_mode)
        
        # Unit position and progression
        position_desc = self._get_unit_position_description(unit_number, total_units)
        
        # Learning objectives by unit position
        objectives = self._generate_unit_objectives(unit_number, total_units, topic)
        
        # Week-by-week breakdown for longer units
        weekly_breakdown = self._generate_weekly_breakdown(duration, unit_number, total_units)
        
        return {
            'unit_number': unit_number,
            'unit_position': position_desc,
            'topic_focus': topic,
            'duration': duration,
            'learning_objectives': objectives,
            'weekly_breakdown': weekly_breakdown,
            'assessment_schedule': self._generate_assessment_schedule(duration),
            'prerequisite_completion': f"Unit {unit_number - 1}" if unit_number > 1 else "None",
            'leads_to': f"Unit {unit_number + 1}" if unit_number < total_units else "Course completion"
        }
    
    def _get_unit_position_description(self, unit_number: int, total_units: int) -> Dict[str, Any]:
        """Describe the unit's position in the overall curriculum"""
        
        percentage_complete = (unit_number / total_units) * 100
        
        if unit_number == 1:
            position_type = "Foundation"
            description = "Introduces fundamental concepts and establishes knowledge base"
        elif unit_number == total_units:
            position_type = "Capstone"
            description = "Integrates all learning and demonstrates comprehensive competency"
        elif unit_number <= total_units * 0.33:
            position_type = "Development"
            description = "Builds upon foundation with core skill development"
        elif unit_number <= total_units * 0.66:
            position_type = "Application"
            description = "Applies knowledge to practical scenarios and challenges"
        else:
            position_type = "Integration"
            description = "Synthesizes learning and prepares for advanced application"
        
        return {
            'type': position_type,
            'description': description,
            'progression_percentage': round(percentage_complete, 1),
            'sequence_position': f"{unit_number} of {total_units}"
        }
    
    def _generate_unit_objectives(self, unit_number: int, total_units: int, topic: str) -> List[str]:
        """Generate learning objectives based on unit position"""
        
        position = self._get_unit_position_description(unit_number, total_units)
        objectives = []
        
        if position['type'] == "Foundation":
            objectives = [
                f"Understand fundamental principles of {topic}",
                f"Identify key concepts and terminology in {topic}",
                f"Recognize the importance of {topic} in professional contexts",
                "Demonstrate basic competency in foundational skills"
            ]
        elif position['type'] == "Development":
            objectives = [
                f"Apply core {topic} principles to practical scenarios",
                f"Develop intermediate skills in {topic} methodologies",
                f"Analyze {topic} challenges and propose solutions",
                "Build confidence in professional skill application"
            ]
        elif position['type'] == "Application":
            objectives = [
                f"Implement {topic} strategies in workplace contexts",
                f"Evaluate {topic} solutions for effectiveness",
                f"Create original {topic} deliverables",
                "Demonstrate professional-level competency"
            ]
        elif position['type'] == "Integration":
            objectives = [
                f"Synthesize {topic} knowledge across multiple domains",
                f"Lead {topic} initiatives and projects",
                f"Mentor others in {topic} best practices",
                "Prepare for advanced professional roles"
            ]
        else:  # Capstone
            objectives = [
                f"Demonstrate mastery of {topic} competencies",
                f"Present comprehensive {topic} project or portfolio",
                f"Reflect on learning journey and future development",
                "Prepare for immediate professional application"
            ]
        
        return objectives
    
    def _generate_weekly_breakdown(self, duration: Dict[str, Any], unit_number: int, total_units: int) -> List[Dict[str, Any]]:
        """Generate week-by-week activity breakdown"""
        
        weeks = duration['total_weeks']
        breakdown = []
        
        for week_num in range(1, weeks + 1):
            if weeks == 1:
                # Single week intensive
                week_focus = "Complete unit - intensive format"
                activities = [
                    "Day 1-2: Core concept introduction and practice",
                    "Day 3-4: Application exercises and skill development", 
                    "Day 5: Assessment and consolidation"
                ]
            elif week_num == 1:
                # First week
                week_focus = "Foundation and Introduction"
                activities = [
                    "Introduce key concepts and terminology",
                    "Complete foundational reading and preparation",
                    "Begin practical exercises"
                ]
            elif week_num == weeks:
                # Final week
                week_focus = "Integration and Assessment"
                activities = [
                    "Complete practical applications",
                    "Assessment submission and review",
                    "Reflection and preparation for next unit"
                ]
            else:
                # Middle weeks
                week_focus = f"Development Week {week_num}"
                activities = [
                    "Guided practice and skill development",
                    "Independent study and research",
                    "Collaborative exercises and peer review"
                ]
            
            breakdown.append({
                'week_number': week_num,
                'focus': week_focus,
                'activities': activities,
                'contact_hours': duration['schedule']['hours_per_day'] * duration['schedule']['days_per_week'],
                'independent_hours': duration['activity_breakdown']['independent_study']['hours'] / weeks
            })
        
        return breakdown
    
    def _generate_assessment_schedule(self, duration: Dict[str, Any]) -> Dict[str, Any]:
        """Generate assessment timing and breakdown"""
        
        total_hours = duration['total_hours']
        assessment_hours = duration['activity_breakdown']['assessment_prep']['hours']
        
        if duration['total_weeks'] <= 1:
            # Single week
            schedule = {
                'formative': "Daily check-ins and practice exercises",
                'summative': "End-of-week comprehensive assessment",
                'timeline': "Continuous assessment throughout the week"
            }
        elif duration['total_weeks'] <= 3:
            # Short unit
            schedule = {
                'formative': "Weekly practice assignments",
                'summative': "Final week project or examination",
                'timeline': "Weeks 1-2: formative, Week 3: summative"
            }
        else:
            # Longer unit
            schedule = {
                'formative': "Bi-weekly assignments and peer reviews",
                'summative': "Major project or comprehensive examination",
                'timeline': f"Ongoing formative assessment, summative in final week"
            }
        
        return {
            'total_assessment_hours': assessment_hours,
            'assessment_percentage': duration['activity_breakdown']['assessment_prep']['percentage'],
            'schedule': schedule,
            'feedback_timeline': "Within 5 working days of submission"
        }
    
    def generate_curriculum_overview(self, units: List[Dict[str, Any]], total_ects: float) -> Dict[str, Any]:
        """Generate overview of entire curriculum structure"""
        
        total_hours = total_ects * self.ects_to_hours
        total_units = len(units)
        
        # Calculate total duration across different delivery modes
        duration_estimates = {}
        for mode in self.delivery_adjustments:
            mode_info = self.delivery_adjustments[mode]
            hours_per_week = mode_info['days_per_week'] * mode_info['hours_per_day']
            weeks = math.ceil(total_hours / hours_per_week)
            duration_estimates[mode] = {
                'weeks': weeks,
                'description': mode_info['description'],
                'completion_time': self._generate_completion_timeframe(weeks, mode)
            }
        
        # Unit size distribution
        unit_sizes = [unit.get('ects', 0) for unit in units]
        avg_unit_size = sum(unit_sizes) / len(unit_sizes) if unit_sizes else 0
        
        return {
            'curriculum_summary': {
                'total_ects': total_ects,
                'total_hours': total_hours,
                'total_units': total_units,
                'average_unit_size': round(avg_unit_size, 1),
                'unit_size_range': f"{min(unit_sizes):.1f} - {max(unit_sizes):.1f} ECTS" if unit_sizes else "N/A"
            },
            'duration_estimates': duration_estimates,
            'learning_progression': {
                'foundation_units': len([u for u in units if u.get('progression_level') == 'Foundation']),
                'development_units': len([u for u in units if u.get('progression_level') == 'Development']),
                'application_units': len([u for u in units if u.get('progression_level') == 'Application']),
                'integration_units': len([u for u in units if u.get('progression_level') == 'Integration'])
            },
            'time_allocation': {
                'contact_learning': f"{total_hours * self.activity_breakdown['contact_learning']:.0f} hours",
                'guided_practice': f"{total_hours * self.activity_breakdown['guided_practice']:.0f} hours",
                'independent_study': f"{total_hours * self.activity_breakdown['independent_study']:.0f} hours",
                'assessment': f"{total_hours * self.activity_breakdown['assessment_prep']:.0f} hours",
                'reflection': f"{total_hours * self.activity_breakdown['reflection_review']:.0f} hours"
            }
        }
