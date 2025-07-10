# scripts/curriculum_generator/core/domain_knowledge_adapter.py
"""
Domain Knowledge Adapter - Unified interface for different domain knowledge sources
Ensures compatibility between various domain knowledge providers and AssessmentGenerator
"""

from typing import List, Dict, Any, Protocol, Union
from abc import ABC, abstractmethod

class DomainKnowledgeProtocol(Protocol):
    """Protocol defining the interface expected by AssessmentGenerator"""
    
    def get_assessment_methods_for_topic(self, topic: str, eqf_level: int) -> List[str]:
        """Get appropriate assessment methods for topic and EQF level"""
        ...
    
    def get_industry_relevance(self, topic: str) -> List[str]:
        """Get industry contexts relevant to topic"""
        ...
    
    def get_all_competency_mappings(self, topic: str) -> Dict[str, List[str]]:
        """Get competency framework mappings for topic"""
        ...

class DomainKnowledgeAdapter:
    """
    Adapter that wraps various domain knowledge sources to provide
    consistent interface to AssessmentGenerator
    """
    
    def __init__(self, domain_source: Any):
        """
        Initialize adapter with a domain knowledge source
        
        Args:
            domain_source: Any object that provides domain knowledge
                          (GeneralIndustryContentGenerator, EnhancedCompetencyMapper, etc.)
        """
        self.domain_source = domain_source
        self._validate_source()
    
    def _validate_source(self) -> None:
        """Validate that the domain source has required methods or can be adapted"""
        
        # Check if source already implements the protocol
        required_methods = [
            'get_assessment_methods_for_topic',
            'get_industry_relevance', 
            'get_all_competency_mappings'
        ]
        
        self._native_support = all(
            hasattr(self.domain_source, method) and callable(getattr(self.domain_source, method))
            for method in required_methods
        )
        
        if self._native_support:
            print(f"✅ ADAPTER: Domain source {type(self.domain_source).__name__} has native AssessmentGenerator support")
        else:
            print(f"🔧 ADAPTER: Domain source {type(self.domain_source).__name__} requires adaptation")
            self._setup_fallback_methods()
    
    def _setup_fallback_methods(self) -> None:
        """Setup fallback methods for sources that don't implement the full protocol"""
        
        # Default assessment methods by EQF level
        self._default_assessment_methods = {
            4: ["practical_assignment", "skills_demonstration", "workplace_project"],
            5: ["practical_assignment", "case_study", "portfolio"],
            6: ["case_study", "project_work", "written_exam"],
            7: ["research_project", "case_study", "presentation"],
            8: ["research_project", "scholarly_paper", "conference_presentation"]
        }
        
        # Default industry mappings
        self._default_industries = {
            "sustainability": ["Environmental Services", "Renewable Energy", "Corporate Sustainability"],
            "data": ["Data Analytics", "Business Intelligence", "Environmental Monitoring"],
            "software": ["Green Software", "Environmental Technology", "Sustainability Platforms"],
            "management": ["Sustainability Management", "Environmental Strategy", "ESG Leadership"],
            "default": ["Digital Sustainability", "Environmental Technology", "Green Innovation"]
        }
        
        # Default competency frameworks
        self._default_competencies = {
            "e-CF": [
                "A.1: IS and Business Strategy Alignment",
                "B.1: Application Development", 
                "E.2: Project and Portfolio Management"
            ],
            "DigComp": [
                "1.2: Evaluating Data and Information",
                "3.1: Developing Digital Content",
                "5.1: Solving Technical Problems"
            ],
            "GreenComp": [
                "1.1: Systems Thinking",
                "2.2: Sustainable Development",
                "4.2: Transformative Action"
            ]
        }
    
    def get_assessment_methods_for_topic(self, topic: str, eqf_level: int) -> List[str]:
        """Get assessment methods - with adaptation if needed"""
        
        if self._native_support:
            return self.domain_source.get_assessment_methods_for_topic(topic, eqf_level)
        
        # Fallback logic
        methods = self._default_assessment_methods.get(eqf_level, self._default_assessment_methods[6])
        
        # Topic-specific adjustments
        topic_lower = topic.lower()
        if "software" in topic_lower or "development" in topic_lower:
            methods = ["coding_assignment", "software_project", "technical_documentation"]
        elif "data" in topic_lower or "analysis" in topic_lower:
            methods = ["data_analysis_project", "technical_report", "case_study"]
        elif "management" in topic_lower or "leadership" in topic_lower:
            methods = ["strategic_project", "case_study", "presentation"]
        
        print(f"🔧 ADAPTER: Fallback assessment methods for '{topic}' (EQF {eqf_level}): {methods}")
        return methods
    
    def get_industry_relevance(self, topic: str) -> List[str]:
        """Get industry relevance - with adaptation if needed"""
        
        if self._native_support:
            return self.domain_source.get_industry_relevance(topic)
        
        # Fallback logic
        topic_lower = topic.lower()
        industries = []
        
        for category, industry_list in self._default_industries.items():
            if category in topic_lower or category == "default":
                industries.extend(industry_list)
        
        # Remove duplicates
        unique_industries = list(dict.fromkeys(industries))
        if not unique_industries:
            unique_industries = self._default_industries["default"]
        
        print(f"🔧 ADAPTER: Fallback industry relevance for '{topic}': {len(unique_industries)} industries")
        return unique_industries
    
    def get_all_competency_mappings(self, topic: str) -> Dict[str, List[str]]:
        """Get competency mappings - with adaptation if needed"""
        
        if self._native_support:
            return self.domain_source.get_all_competency_mappings(topic)
        
        # Fallback logic - return default competency frameworks
        mappings = {
            framework: competencies.copy()
            for framework, competencies in self._default_competencies.items()
        }
        
        print(f"🔧 ADAPTER: Fallback competency mappings for '{topic}': {list(mappings.keys())}")
        return mappings
    
    def __getattr__(self, name: str) -> Any:
        """
        Delegate any other method calls to the underlying domain source
        This allows the adapter to be transparent for other operations
        """
        if hasattr(self.domain_source, name):
            return getattr(self.domain_source, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    @classmethod
    def create_compatible_source(cls, domain_source: Any) -> 'DomainKnowledgeAdapter':
        """
        Factory method to create a compatible domain knowledge source
        
        Args:
            domain_source: Any domain knowledge provider
            
        Returns:
            DomainKnowledgeAdapter that ensures compatibility
        """
        return cls(domain_source)

class MockDomainKnowledge:
    """
    Enhanced mock domain knowledge provider for testing and fallback scenarios
    Implements the full DomainKnowledgeProtocol
    """
    
    def __init__(self):
        """Initialize with realistic mock data"""
        
        self.assessment_methods = {
            4: ["practical_assignment", "skills_demonstration", "portfolio"],
            5: ["case_study", "practical_assignment", "presentation"],
            6: ["project_work", "case_study", "written_exam"],
            7: ["research_project", "advanced_analysis", "peer_review"],
            8: ["original_research", "scholarly_contribution", "innovation_project"]
        }
        
        self.industries = [
            "Digital Sustainability", "Environmental Technology", "Green Innovation",
            "Renewable Energy", "Carbon Management", "Sustainability Consulting"
        ]
        
        self.competency_mappings = {
            "e-CF": [
                "A.1: IS and Business Strategy Alignment",
                "B.1: Application Development",
                "E.2: Project and Portfolio Management"
            ],
            "DigComp": [
                "1.2: Evaluating Data and Information",
                "3.1: Developing Digital Content", 
                "5.1: Solving Technical Problems"
            ],
            "GreenComp": [
                "1.1: Systems Thinking",
                "2.2: Sustainable Development",
                "4.2: Transformative Action"
            ]
        }
    
    def get_assessment_methods_for_topic(self, topic: str, eqf_level: int) -> List[str]:
        """Get assessment methods for topic and EQF level"""
        methods = self.assessment_methods.get(eqf_level, self.assessment_methods[6])
        print(f"🤖 MOCK: Assessment methods for '{topic}' (EQF {eqf_level}): {methods}")
        return methods
    
    def get_industry_relevance(self, topic: str) -> List[str]:
        """Get industry contexts for topic"""
        print(f"🤖 MOCK: Industry relevance for '{topic}': {len(self.industries)} industries")
        return self.industries.copy()
    
    def get_all_competency_mappings(self, topic: str) -> Dict[str, List[str]]:
        """Get competency framework mappings"""
        mappings = {
            framework: competencies.copy()
            for framework, competencies in self.competency_mappings.items()
        }
        print(f"🤖 MOCK: Competency mappings for '{topic}': {list(mappings.keys())}")
        return mappings

# Convenience functions for easy usage

def create_compatible_domain_knowledge(domain_source: Any) -> DomainKnowledgeAdapter:
    """
    Create a domain knowledge source compatible with AssessmentGenerator
    
    Args:
        domain_source: Any domain knowledge provider
        
    Returns:
        Adapted domain knowledge source ready for use with AssessmentGenerator
    """
    return DomainKnowledgeAdapter.create_compatible_source(domain_source)

def create_mock_domain_knowledge() -> MockDomainKnowledge:
    """
    Create a mock domain knowledge source for testing
    
    Returns:
        Mock domain knowledge source with realistic data
    """
    return MockDomainKnowledge()
