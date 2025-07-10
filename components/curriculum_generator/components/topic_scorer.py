# scripts/curriculum_generator/components/topic_scorer.py
"""
Consolidated Topic Scorer - TRULY QUIET VERSION
Fixes verbose debug output and ensures proper scoring.
"""

from typing import Dict, List, Any, Optional, Tuple
import re
from pathlib import Path


class ConsolidatedTopicScorer:
    """Unified topic scoring system - QUIET VERSION"""
    
    def __init__(self):
        self.knowledge_base = None
        self.scoring_cache = {}
        self.debug_mode = False  # ALWAYS OFF unless explicitly enabled
        self.verbose_debug = False
        
        # Initialize knowledge base with proper error handling
        self._initialize_knowledge_base()
        
        # Enhanced keyword mappings
        self.semantic_mappings = {
            'carbon': ['carbon', 'emission', 'footprint', 'greenhouse', 'climate', 'co2', 'ghg', 'measurement', 'tracking', 'assessment'],
            'data': ['data', 'analytics', 'analysis', 'visualization', 'intelligence', 'mining', 'big', 'environmental'],
            'ai': ['artificial', 'intelligence', 'machine', 'learning', 'neural', 'algorithm', 'predictive', 'model', 'ml'],
            'green': ['green', 'sustainable', 'environmental', 'eco', 'renewable', 'clean', 'low-carbon'],
            'energy': ['energy', 'efficiency', 'consumption', 'optimization', 'power', 'renewable', 'carbon'],
            'sustainability': ['sustainability', 'sustainable', 'environmental', 'social', 'governance', 'esg']
        }
        
        self.sustainability_keywords = [
            'sustainability', 'sustainable', 'green', 'environment', 'environmental',
            'carbon', 'energy', 'efficiency', 'circular', 'renewable', 'climate',
            'emission', 'footprint', 'lifecycle', 'eco', 'digital'
        ]
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with error handling"""
        try:
            from scripts.curriculum_generator.domain.knowledge_base import DigitalSustainabilityKnowledge
            self.knowledge_base = DigitalSustainabilityKnowledge()
            if self.debug_mode:
                print("✅ Knowledge base initialized")
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Knowledge base not available: {e}")
            self.knowledge_base = None
    
    def score_module_topic_relevance(
        self, 
        module: Dict[str, Any], 
        target_topic: str,
        debug_label: str = "unknown"
    ) -> Tuple[float, Dict[str, Any]]:
        """
        MAIN METHOD: Score module relevance to target topic - QUIET VERSION
        """
        
        # Handle None topic gracefully
        if target_topic is None:
            return self._score_general_sustainability(module)
        
        # Check cache first
        cache_key = f"{module.get('id', 'unknown')}_{target_topic}"
        if cache_key in self.scoring_cache:
            return self.scoring_cache[cache_key]
        
        # Score using optimized method
        if self.knowledge_base:
            score, debug_info = self._score_with_knowledge_base_optimized(module, target_topic)
        else:
            score, debug_info = self._score_with_enhanced_fallback(module, target_topic)
        
        # Cache result
        result = (score, debug_info)
        self.scoring_cache[cache_key] = result
        
        return result
    
    def _score_with_knowledge_base_optimized(
        self, 
        module: Dict[str, Any], 
        target_topic: str
    ) -> Tuple[float, Dict[str, Any]]:
        """Optimized knowledge base scoring"""
        
        try:
            # Get base knowledge base score
            kb_score = self.knowledge_base.score_module_relevance(module, target_topic)
            
            # Apply boosting for specific topics
            boosted_score = self._apply_topic_boosting(module, target_topic, kb_score)
            
            debug_info = {
                'method': 'kb_optimized',
                'kb_score': kb_score,
                'boosted_score': boosted_score
            }
            
            return min(boosted_score, 100), debug_info
            
        except Exception:
            return self._score_with_enhanced_fallback(module, target_topic)
    
    def _apply_topic_boosting(
        self, 
        module: Dict[str, Any], 
        target_topic: str, 
        base_score: float
    ) -> float:
        """Apply topic-specific boosting"""
        
        module_name = module.get('name', '').lower()
        module_desc = module.get('description', '').lower()
        module_topics = module.get('topics', [])
        module_topics_text = ' '.join(module_topics).lower() if module_topics else ''
        
        boost = 0.0
        target_lower = target_topic.lower()
        
        # Carbon footprint specific boosting
        if 'carbon' in target_lower or 'footprint' in target_lower:
            carbon_terms = ['carbon', 'footprint', 'emission', 'greenhouse', 'climate', 'measurement', 'assessment', 'environmental']
            for term in carbon_terms:
                if term in module_name:
                    boost += 25
                if term in module_desc:
                    boost += 15
                if term in module_topics_text:
                    boost += 20
        
        # Data analytics boosting
        if 'data' in target_lower or 'analytics' in target_lower:
            data_terms = ['data', 'analytics', 'analysis', 'visualization', 'intelligence']
            for term in data_terms:
                if term in module_name:
                    boost += 20
                if term in module_desc:
                    boost += 12
                if term in module_topics_text:
                    boost += 15
        
        # General sustainability boost
        sustainability_terms = ['sustainable', 'sustainability', 'green', 'environmental']
        for term in sustainability_terms:
            if term in module_name:
                boost += 10
            if term in module_desc:
                boost += 6
        
        return base_score + boost
    
    def _score_with_enhanced_fallback(
        self, 
        module: Dict[str, Any], 
        target_topic: str
    ) -> Tuple[float, Dict[str, Any]]:
        """Enhanced fallback scoring"""
        
        module_name = module.get('name', '').lower()
        module_desc = module.get('description', '').lower()
        module_topics = module.get('topics', [])
        module_topics_text = ' '.join(module_topics).lower() if module_topics else ''
        
        target_lower = target_topic.lower()
        target_words = set(target_lower.split())
        
        score = 0.0
        
        # Direct topic matching
        if target_lower in module_name:
            score += 30
        if target_lower in module_desc:
            score += 20
        if target_lower in module_topics_text:
            score += 25
        
        # Word-by-word matching
        for word in target_words:
            if len(word) > 2:
                if word in module_name:
                    score += 15
                if word in module_desc:
                    score += 10
                if word in module_topics_text:
                    score += 12
        
        # Semantic mapping
        for word in target_words:
            if word in self.semantic_mappings:
                related_terms = self.semantic_mappings[word]
                for term in related_terms:
                    if term in module_name:
                        score += 8
                    if term in module_desc:
                        score += 5
                    if term in module_topics_text:
                        score += 6
        
        debug_info = {
            'method': 'enhanced_fallback',
            'target_words': list(target_words),
            'final_score': min(score, 100)
        }
        
        return min(score, 100), debug_info
    
    def _score_general_sustainability(self, module: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Score for general sustainability relevance"""
        
        module_name = module.get('name', '').lower()
        module_desc = module.get('description', '').lower()
        module_topics = module.get('topics', [])
        
        score = 50.0  # Base score
        
        # Check for sustainability indicators
        for indicator in self.sustainability_keywords:
            if indicator in module_name:
                score += 15
            if indicator in module_desc:
                score += 10
        
        # Check topics array
        if module_topics:
            module_topics_text = ' '.join(module_topics).lower()
            for indicator in self.sustainability_keywords:
                if indicator in module_topics_text:
                    score += 12
        
        debug_info = {
            'method': 'general_sustainability',
            'final_score': min(score, 90)
        }
        
        return min(score, 90), debug_info
    
    def get_scoring_summary(self, module_scores: List[Tuple[Dict, float, Dict]]) -> Dict[str, Any]:
        """Generate scoring summary"""
        
        if not module_scores:
            return {'error': 'No modules scored'}
        
        scores = [score for _, score, _ in module_scores]
        
        return {
            'total_modules': len(module_scores),
            'average_score': sum(scores) / len(scores),
            'max_score': max(scores),
            'min_score': min(scores),
            'scores_above_40': len([s for s in scores if s > 40]),
            'scores_above_60': len([s for s in scores if s > 60])
        }
    
    def clear_cache(self):
        """Clear scoring cache"""
        self.scoring_cache.clear()
