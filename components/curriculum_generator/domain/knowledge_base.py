# scripts/curriculum_generator/domain/knowledge_base.py
"""
Digital Sustainability domain knowledge base - PHASE 2 ENHANCED
Enhanced topic relationships, keywords, and competency mappings.
Improved scoring for carbon footprint and other key topics.
"""

from typing import Dict, List, Set, Any, Optional
import re


class DigitalSustainabilityKnowledge:
    """Domain knowledge for Digital Sustainability - PHASE 2 ENHANCED"""
    
    def __init__(self):
        self.domain_name = "Digital Sustainability"
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        """Initialize the enhanced digital sustainability knowledge base"""
        
        # PHASE 2: Enhanced core topics with better keywords and relationships
        self.core_topics = {
            "Green Software Development": {
                "keywords": [
                    "green", "software", "sustainable", "energy", "efficient", 
                    "carbon", "footprint", "optimization", "eco-friendly",
                    "environmental", "renewable", "clean", "low-power", "programming"
                ],
                "related_topics": ["Carbon Footprint Measurement", "Energy-Efficient Algorithms"],
                "specializations": ["Green Coding Practices", "Sustainable Architecture"],
                "complexity_level": "intermediate"
            },
            
            "Carbon Footprint Measurement": {
                "keywords": [
                    "carbon", "footprint", "measurement", "emission", "ghg",
                    "greenhouse", "gas", "co2", "assessment", "monitoring",
                    "tracking", "reporting", "scope", "lifecycle", "quantification",
                    "calculation", "analysis", "environmental", "impact", "data"
                ],
                "related_topics": ["Green Software Development", "Digital Carbon Accounting", "Data Analytics for Sustainability"],
                "specializations": ["LCA Tools", "Carbon Metrics", "Environmental Data Analysis"],
                "complexity_level": "advanced"
            },
            
            "Sustainable AI": {
                "keywords": [
                    "ai", "artificial", "intelligence", "machine", "learning",
                    "sustainable", "green", "efficient", "energy", "model",
                    "training", "inference", "optimization", "federated", "carbon",
                    "environmental", "algorithms", "data", "predictive"
                ],
                "related_topics": ["Energy-Efficient Algorithms", "Green ML", "Carbon Footprint Measurement"],
                "specializations": ["Efficient Neural Networks", "Green Training"],
                "complexity_level": "advanced"
            },
            
            "Data Center Sustainability": {
                "keywords": [
                    "data", "center", "datacenter", "server", "cooling",
                    "energy", "pue", "efficiency", "renewable", "infrastructure",
                    "virtualization", "cloud", "green", "sustainable", "carbon",
                    "monitoring", "optimization"
                ],
                "related_topics": ["Cloud Computing Sustainability", "Energy Management"],
                "specializations": ["PUE Optimization", "Green Infrastructure"],
                "complexity_level": "intermediate"
            },
            
            "Digital Circular Economy": {
                "keywords": [
                    "circular", "economy", "digital", "lifecycle", "reuse",
                    "recycle", "sustainable", "waste", "reduction", "sharing",
                    "platform", "resource", "optimization", "efficiency",
                    "business", "models"
                ],
                "related_topics": ["Sustainable Business Models", "Digital Transformation"],
                "specializations": ["Platform Economics", "Resource Sharing"],
                "complexity_level": "intermediate"
            },
            
            "IoT Sustainability": {
                "keywords": [
                    "iot", "internet", "things", "sensors", "devices",
                    "energy", "efficient", "low", "power", "battery",
                    "wireless", "smart", "sustainable", "monitoring",
                    "environmental"
                ],
                "related_topics": ["Smart Cities", "Environmental Monitoring"],
                "specializations": ["Low-Power Design", "Smart Grid"],
                "complexity_level": "intermediate"
            },
            
            "Blockchain Sustainability": {
                "keywords": [
                    "blockchain", "cryptocurrency", "bitcoin", "ethereum",
                    "proof", "stake", "consensus", "energy", "efficient",
                    "sustainable", "green", "carbon", "neutral", "traceability"
                ],
                "related_topics": ["Sustainable Finance", "Green Crypto"],
                "specializations": ["PoS Protocols", "Energy-Efficient Mining"],
                "complexity_level": "advanced"
            },
            
            # PHASE 2: Additional enhanced topics
            "Data Analytics for Sustainability": {
                "keywords": [
                    "data", "analytics", "analysis", "sustainability", "environmental",
                    "visualization", "intelligence", "carbon", "footprint", "measurement",
                    "monitoring", "assessment", "reporting", "insights", "metrics"
                ],
                "related_topics": ["Carbon Footprint Measurement", "Environmental Intelligence"],
                "specializations": ["Environmental Data Analysis", "Sustainability Metrics"],
                "complexity_level": "intermediate"
            }
        }
        
        # Competency framework mappings
        self.competency_mappings = {
            "e-CF": {
                "Green Software Development": ["e-CF:B.1", "e-CF:A.6"],
                "Carbon Footprint Measurement": ["e-CF:D.12", "e-CF:E.7"],
                "Sustainable AI": ["e-CF:B.1", "e-CF:C.4"],
                "Data Center Sustainability": ["e-CF:C.2", "e-CF:D.10"],
                "Digital Circular Economy": ["e-CF:A.1", "e-CF:E.2"],
                "IoT Sustainability": ["e-CF:B.1", "e-CF:C.3"],
                "Blockchain Sustainability": ["e-CF:B.1", "e-CF:D.11"],
                "Data Analytics for Sustainability": ["e-CF:C.4", "e-CF:D.12"]
            },
            "ESCO": {
                "Green Software Development": ["ESCO:O*NET:15-1132.00"],
                "Carbon Footprint Measurement": ["ESCO:O*NET:19-2041.00"],
                "Sustainable AI": ["ESCO:O*NET:15-1132.00"],
                "Data Center Sustainability": ["ESCO:O*NET:15-1142.00"],
                "Digital Circular Economy": ["ESCO:O*NET:11-3021.00"],
                "IoT Sustainability": ["ESCO:O*NET:17-2061.00"],
                "Blockchain Sustainability": ["ESCO:O*NET:15-1132.00"],
                "Data Analytics for Sustainability": ["ESCO:O*NET:15-1199.00"]
            }
        }
        
        # Industry relevance mappings
        self.industry_mappings = {
            "technology": ["Green Software Development", "Sustainable AI", "IoT Sustainability"],
            "consulting": ["Carbon Footprint Measurement", "Digital Circular Economy", "Data Analytics for Sustainability"],
            "finance": ["Blockchain Sustainability", "Digital Circular Economy"],
            "energy": ["Data Center Sustainability", "IoT Sustainability"],
            "healthcare": ["IoT Sustainability", "Sustainable AI"],
            "manufacturing": ["Digital Circular Economy", "IoT Sustainability"]
        }
        
    def get_topic_keywords(self, topic: str) -> List[str]:
        """Get keywords for a given topic"""
        if topic in self.core_topics:
            return self.core_topics[topic]["keywords"]
        
        # Try fuzzy matching
        for core_topic in self.core_topics:
            if self._fuzzy_match(topic, core_topic):
                return self.core_topics[core_topic]["keywords"]
                
        # Return enhanced generic sustainability keywords if no match
        return ["sustainable", "green", "environmental", "efficient", "carbon", "energy", "optimization", "measurement"]
        
    def get_related_topics(self, topic: str) -> List[str]:
        """Get topics related to the given topic"""
        if topic in self.core_topics:
            return self.core_topics[topic]["related_topics"]
            
        # Try fuzzy matching
        for core_topic in self.core_topics:
            if self._fuzzy_match(topic, core_topic):
                return self.core_topics[core_topic]["related_topics"]
                
        return []
        
    def get_specializations(self, topic: str) -> List[str]:
        """Get specializations for a given topic"""
        if topic in self.core_topics:
            return self.core_topics[topic]["specializations"]
            
        # Try fuzzy matching
        for core_topic in self.core_topics:
            if self._fuzzy_match(topic, core_topic):
                return self.core_topics[core_topic]["specializations"]
                
        return []
        
    def get_complexity_level(self, topic: str) -> str:
        """Get complexity level for a topic"""
        if topic in self.core_topics:
            return self.core_topics[topic]["complexity_level"]
            
        # Try fuzzy matching
        for core_topic in self.core_topics:
            if self._fuzzy_match(topic, core_topic):
                return self.core_topics[core_topic]["complexity_level"]
                
        return "intermediate"
        
    def get_competency_mappings(self, topic: str, framework: str = "e-CF") -> List[str]:
        """Get competency mappings for a topic and framework"""
        if framework in self.competency_mappings:
            if topic in self.competency_mappings[framework]:
                return self.competency_mappings[framework][topic]
                
            # Try fuzzy matching
            for core_topic in self.core_topics:
                if self._fuzzy_match(topic, core_topic):
                    if core_topic in self.competency_mappings[framework]:
                        return self.competency_mappings[framework][core_topic]
                        
        return []
        
    def get_all_competency_mappings(self, topic: str) -> Dict[str, List[str]]:
        """Get all competency mappings for a topic across all frameworks"""
        all_mappings = {}
        
        for framework in self.competency_mappings:
            mappings = self.get_competency_mappings(topic, framework)
            if mappings:
                all_mappings[framework] = mappings
                
        return all_mappings
        
    def get_industry_relevance(self, topic: str) -> List[str]:
        """Get industries relevant to a topic"""
        relevant_industries = []
        
        for industry, topics in self.industry_mappings.items():
            if topic in topics:
                relevant_industries.append(industry)
            else:
                # Check fuzzy matching
                for mapped_topic in topics:
                    if self._fuzzy_match(topic, mapped_topic):
                        relevant_industries.append(industry)
                        break
                        
        return relevant_industries
        
    def score_module_relevance(self, module: Dict[str, Any], topic: str) -> float:
        """PHASE 2 ENHANCED: Score how relevant a module is to a topic with improved algorithm"""
        score = 0.0
        
        # Get topic keywords
        topic_keywords = self.get_topic_keywords(topic)
        topic_keywords_set = set(kw.lower() for kw in topic_keywords)
        
        # Module data extraction
        module_name = module.get('name', '').lower()
        module_desc = module.get('description', '').lower()
        
        # PHASE 2: Enhanced scoring algorithm
        
        # 1. Score based on module name (highest weight)
        name_words = set(re.findall(r'\b\w+\b', module_name))
        name_matches = len(name_words.intersection(topic_keywords_set))
        score += name_matches * 4.0  # Increased from 3.0
        
        # 2. Score based on description
        desc_words = set(re.findall(r'\b\w+\b', module_desc))
        desc_matches = len(desc_words.intersection(topic_keywords_set))
        score += desc_matches * 2.5  # Increased from 2.0
        
        # 3. Handle module keywords/topics properly
        module_topics = module.get('topics', [])
        if module_topics:
            module_topics_text = ' '.join(module_topics).lower()
            topics_words = set(re.findall(r'\b\w+\b', module_topics_text))
            topics_matches = len(topics_words.intersection(topic_keywords_set))
            score += topics_matches * 5.0  # Increased from 4.0
        
        # 4. Handle legacy 'keywords' field if it exists
        module_keywords = module.get('keywords', [])
        if module_keywords:
            if isinstance(module_keywords, str):
                module_keywords = [kw.strip() for kw in module_keywords.split(',')]
            module_keywords_set = set(kw.lower() for kw in module_keywords)
            keyword_matches = len(module_keywords_set.intersection(topic_keywords_set))
            score += keyword_matches * 5.0  # Increased from 4.0
        
        # 5. Enhanced: Check extended_description field
        extended_desc = module.get('extended_description', '')
        if extended_desc:
            extended_words = set(re.findall(r'\b\w+\b', extended_desc.lower()))
            extended_matches = len(extended_words.intersection(topic_keywords_set))
            score += extended_matches * 2.0  # Increased from 1.5
        
        # 6. Enhanced: Direct topic name matching (high score)
        topic_lower = topic.lower()
        if topic_lower in module_name:
            score += 20.0  # Increased from 15.0
        if topic_lower in module_desc:
            score += 15.0  # Increased from 10.0
        
        # 7. PHASE 2: Special boosting for carbon footprint measurement
        if 'carbon footprint' in topic_lower or 'carbon' in topic_lower:
            carbon_boost_terms = ['carbon', 'footprint', 'emission', 'measurement', 'assessment', 'environmental', 'data']
            for term in carbon_boost_terms:
                if term in module_name:
                    score += 10.0
                if term in module_desc:
                    score += 6.0
                if term in module_topics_text if module_topics else '':
                    score += 8.0
        
        # 8. Bonus for exact topic match in topics array
        if module_topics:
            for mod_topic in module_topics:
                if self._fuzzy_match(topic, mod_topic):
                    score += 25.0  # Increased from 20.0
                    break
        
        # 9. PHASE 2: Additional semantic matching
        topic_words = set(topic_lower.split())
        all_module_text = f"{module_name} {module_desc} {extended_desc.lower() if extended_desc else ''}"
        
        for topic_word in topic_words:
            if len(topic_word) > 2 and topic_word in all_module_text:
                score += 8.0
        
        return min(score, 100)  # Cap at 100
        
    def _fuzzy_match(self, text1: str, text2: str, threshold: float = 0.5) -> bool:
        """Enhanced fuzzy matching with lower threshold for better matching"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return False
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return False
            
        similarity = intersection / union
        return similarity >= threshold  # Lowered from 0.6 to 0.5
        
    def get_all_topics(self) -> List[str]:
        """Get all available topics"""
        return list(self.core_topics.keys())
        
    def get_assessment_methods_for_topic(self, topic: str, eqf_level: int) -> List[str]:
        """Get appropriate assessment methods for a topic and EQF level"""
        base_methods = ["written_exam", "practical_assignment", "project_work"]
        
        complexity = self.get_complexity_level(topic)
        
        if eqf_level >= 7:  # Masters level
            if complexity == "advanced":
                return ["research_project", "dissertation", "case_study", "peer_review"]
            else:
                return ["project_work", "portfolio", "case_study", "presentation"]
        elif eqf_level == 6:  # Bachelor level
            if complexity == "advanced":
                return ["project_work", "case_study", "practical_assignment", "written_exam"]
            else:
                return ["practical_assignment", "project_work", "written_exam", "presentation"]
        else:  # Lower levels
            return ["practical_assignment", "written_exam", "skills_demonstration"]
