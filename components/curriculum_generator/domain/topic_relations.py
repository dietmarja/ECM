# scripts/curriculum_generator/domain/topic_relations.py
"""
Topic relationship management
Handles topic hierarchies, prerequisites, and learning pathways
"""

from typing import Dict, List, Set, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class TopicRelationManager:
    """Manages relationships between topics and learning progressions"""
    
    def __init__(self, domain_knowledge):
        self.domain_knowledge = domain_knowledge
        self.topic_graph = self._build_topic_graph()
    
    def _build_topic_graph(self) -> Dict[str, Dict]:
        """Build a graph of topic relationships"""
        graph = {}
        
        for topic_name, topic_info in self.domain_knowledge.topics.items():
            graph[topic_name] = {
                'related': topic_info.related_topics,
                'prerequisites': topic_info.prerequisite_topics or [],
                'specializations': topic_info.specializations,
                'eqf_levels': topic_info.eqf_levels or [4, 5, 6, 7, 8],
                'keywords': topic_info.keywords,
                'industries': topic_info.industry_relevance
            }
        
        return graph
    
    def get_learning_progression(self, start_topic: str, target_eqf: int) -> List[str]:
        """Get suggested learning progression starting from a topic"""
        progression = []
        visited = set()
        
        def build_progression(topic: str, current_eqf: int):
            if topic in visited or current_eqf > target_eqf:
                return
            
            visited.add(topic)
            
            if topic in self.topic_graph:
                topic_info = self.topic_graph[topic]
                
                # Add prerequisites first
                for prereq in topic_info['prerequisites']:
                    if prereq not in visited:
                        build_progression(prereq, current_eqf - 1)
                
                # Add current topic if appropriate for EQF level
                if current_eqf in topic_info['eqf_levels']:
                    progression.append(topic)
                
                # Add related topics at same level
                for related in topic_info['related']:
                    if related not in visited and current_eqf <= target_eqf:
                        build_progression(related, current_eqf)
        
        build_progression(start_topic, target_eqf)
        return progression
    
    def find_prerequisite_chain(self, topic: str) -> List[str]:
        """Find the complete prerequisite chain for a topic"""
        chain = []
        visited = set()
        
        def trace_prerequisites(current_topic: str):
            if current_topic in visited or current_topic not in self.topic_graph:
                return
            
            visited.add(current_topic)
            topic_info = self.topic_graph[current_topic]
            
            # Add prerequisites first (depth-first)
            for prereq in topic_info['prerequisites']:
                trace_prerequisites(prereq)
            
            # Add current topic
            if current_topic not in chain:
                chain.append(current_topic)
        
        trace_prerequisites(topic)
        return chain[:-1]  # Exclude the target topic itself
    
    def suggest_next_topics(self, completed_topics: List[str], target_eqf: int) -> List[Dict]:
        """Suggest next topics based on completed topics"""
        suggestions = []
        completed_set = set(completed_topics)
        
        for topic_name, topic_info in self.topic_graph.items():
            if topic_name in completed_set:
                continue
            
            # Check if prerequisites are met
            prerequisites_met = all(prereq in completed_set for prereq in topic_info['prerequisites'])
            
            # Check EQF level appropriateness
            eqf_appropriate = target_eqf in topic_info['eqf_levels']
            
            if prerequisites_met and eqf_appropriate:
                # Calculate relevance score
                relevance_score = self._calculate_topic_relevance(topic_name, completed_topics)
                
                suggestions.append({
                    'topic': topic_name,
                    'relevance_score': relevance_score,
                    'prerequisites_met': True,
                    'eqf_appropriate': True,
                    'related_to_completed': self._get_related_completed_topics(topic_name, completed_topics)
                })
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
        return suggestions
    
    def _calculate_topic_relevance(self, topic: str, completed_topics: List[str]) -> float:
        """Calculate how relevant a topic is based on completed topics"""
        if topic not in self.topic_graph:
            return 0.0
        
        topic_info = self.topic_graph[topic]
        relevance = 0.0
        
        # Base relevance
        relevance += 0.5
        
        # Bonus for being related to completed topics
        for completed in completed_topics:
            if completed in self.topic_graph:
                completed_info = self.topic_graph[completed]
                if topic in completed_info['related']:
                    relevance += 0.3
                if any(keyword in topic_info['keywords'] for keyword in completed_info['keywords']):
                    relevance += 0.2
        
        # Bonus for sharing industries
        for completed in completed_topics:
            if completed in self.topic_graph:
                completed_info = self.topic_graph[completed]
                shared_industries = set(topic_info['industries']) & set(completed_info['industries'])
                relevance += len(shared_industries) * 0.1
        
        return min(relevance, 1.0)  # Cap at 1.0
    
    def _get_related_completed_topics(self, topic: str, completed_topics: List[str]) -> List[str]:
        """Get list of completed topics related to the given topic"""
        related = []
        
        if topic not in self.topic_graph:
            return related
        
        topic_info = self.topic_graph[topic]
        
        for completed in completed_topics:
            if completed in topic_info['related']:
                related.append(completed)
            elif completed in self.topic_graph:
                completed_info = self.topic_graph[completed]
                if topic in completed_info['related']:
                    related.append(completed)
        
        return related
    
    def generate_curriculum_pathway(self, start_topic: str, target_ects: float, eqf_level: int) -> Dict:
        """Generate a complete curriculum pathway"""
        
        # Get prerequisite chain
        prerequisites = self.find_prerequisite_chain(start_topic)
        
        # Get learning progression
        progression = self.get_learning_progression(start_topic, eqf_level)
        
        # Estimate ECTS distribution
        total_topics = len(prerequisites) + len(progression)
        ects_per_topic = target_ects / total_topics if total_topics > 0 else target_ects
        
        pathway = {
            'start_topic': start_topic,
            'target_ects': target_ects,
            'eqf_level': eqf_level,
            'pathway_structure': {
                'prerequisites': [
                    {
                        'topic': topic,
                        'estimated_ects': ects_per_topic * 0.6,  # Prerequisites get less ECTS
                        'type': 'prerequisite'
                    } for topic in prerequisites
                ],
                'core_progression': [
                    {
                        'topic': topic,
                        'estimated_ects': ects_per_topic,
                        'type': 'core'
                    } for topic in progression
                ]
            },
            'total_estimated_ects': (len(prerequisites) * ects_per_topic * 0.6) + (len(progression) * ects_per_topic),
            'pathway_length': total_topics,
            'specialization_options': self.domain_knowledge.get_specializations(start_topic)
        }
        
        return pathway
    
    def validate_topic_sequence(self, topic_sequence: List[str]) -> Dict:
        """Validate that a sequence of topics follows logical prerequisites"""
        validation = {
            'is_valid': True,
            'issues': [],
            'recommendations': []
        }
        
        completed = set()
        
        for i, topic in enumerate(topic_sequence):
            if topic not in self.topic_graph:
                validation['issues'].append(f"Unknown topic: {topic}")
                validation['is_valid'] = False
                continue
            
            topic_info = self.topic_graph[topic]
            
            # Check prerequisites
            for prereq in topic_info['prerequisites']:
                if prereq not in completed:
                    validation['issues'].append(f"Topic '{topic}' requires prerequisite '{prereq}' which hasn't been completed")
                    validation['is_valid'] = False
                    validation['recommendations'].append(f"Add '{prereq}' before '{topic}'")
            
            completed.add(topic)
        
        return validation
    
    def export_topic_relationships(self) -> Dict:
        """Export topic relationship data for visualization"""
        relationships = {
            'nodes': [],
            'edges': []
        }
        
        # Add nodes
        for topic_name, topic_info in self.topic_graph.items():
            relationships['nodes'].append({
                'id': topic_name,
                'label': topic_name,
                'eqf_levels': topic_info['eqf_levels'],
                'keywords': topic_info['keywords'][:3],  # First 3 keywords
                'industries': topic_info['industries'][:2]  # First 2 industries
            })
        
        # Add edges
        for topic_name, topic_info in self.topic_graph.items():
            # Prerequisite edges
            for prereq in topic_info['prerequisites']:
                relationships['edges'].append({
                    'source': prereq,
                    'target': topic_name,
                    'type': 'prerequisite'
                })
            
            # Related topic edges
            for related in topic_info['related']:
                relationships['edges'].append({
                    'source': topic_name,
                    'target': related,
                    'type': 'related'
                })
        
        return relationships
