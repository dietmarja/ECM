import random
from typing import List, Dict, Optional

class LearningOutcomesGenerator:
    """
    Generates detailed, Bloom's Taxonomy aligned learning outcomes 
    for digital sustainability modules with proper EQF level complexity
    """
    
    def __init__(self):
        """Initialize the learning outcomes generator with EQF-specific taxonomy verbs"""
        
        # EQF-specific Bloom's taxonomy verbs with appropriate complexity
        self.eqf_specific_verbs = {
            4: {
                "knowledge": ["identify", "describe", "explain", "list", "recognize", "recall"],
                "skills": ["apply", "demonstrate", "implement", "operate", "perform", "use"],
                "attitude": ["acknowledge", "follow", "participate", "assist", "comply"]
            },
            5: {
                "knowledge": ["analyze", "compare", "categorize", "examine", "distinguish", "interpret"],
                "skills": ["analyze", "execute", "solve", "calculate", "modify", "organize"],
                "attitude": ["respond", "discuss", "help", "participate", "engage"]
            },
            6: {
                "knowledge": ["evaluate", "assess", "critique", "judge", "recommend", "justify"],
                "skills": ["design", "create", "develop", "formulate", "plan", "construct"],
                "attitude": ["value", "support", "advocate", "commit", "defend"]
            },
            7: {
                "knowledge": ["synthesize", "integrate", "consolidate", "coordinate", "systematize"],
                "skills": ["evaluate complex systems", "design comprehensive frameworks", "create innovative solutions", "establish methodologies", "optimize strategic approaches"],
                "attitude": ["organize values", "prioritize principles", "synthesize beliefs", "integrate perspectives"]
            },
            8: {
                "knowledge": ["architect", "pioneer", "establish paradigms", "transform disciplines", "advance frontiers"],
                "skills": ["architect enterprise solutions", "transform industry practices", "pioneer breakthrough methodologies", "establish new frameworks", "advance professional standards"],
                "attitude": ["characterize professional identity", "embody values", "model excellence", "influence communities"]
            }
        }
        
        # EQF level descriptors for context
        self.eqf_descriptors = {
            4: {
                "knowledge": "factual and theoretical knowledge in broad contexts",
                "skills": "range of cognitive and practical skills",
                "autonomy": "self-management within guidelines"
            },
            5: {
                "knowledge": "comprehensive, specialized, factual and theoretical knowledge",
                "skills": "wide range of cognitive and practical skills",
                "autonomy": "exercise management and supervision"
            },
            6: {
                "knowledge": "advanced knowledge involving critical understanding",
                "skills": "advanced skills demonstrating mastery and innovation", 
                "autonomy": "manage complex technical or professional activities"
            },
            7: {
                "knowledge": "highly specialized knowledge with critical awareness",
                "skills": "specialized problem-solving for research and innovation",
                "autonomy": "manage and transform complex, unpredictable contexts"
            },
            8: {
                "knowledge": "knowledge at the most advanced frontier between fields",
                "skills": "most advanced and specialized skills and techniques",
                "autonomy": "substantial authority, innovation, autonomy, scholarly integrity"
            }
        }
        
        # Domain-specific knowledge areas for digital sustainability
        self.knowledge_areas = {
            "sustainability": [
                "sustainability frameworks and standards",
                "environmental impact assessment methodologies", 
                "circular economy principles",
                "corporate social responsibility reporting",
                "sustainable development goals",
                "ecological footprint calculation",
                "lifecycle assessment approaches",
                "environmental regulations compliance",
                "social sustainability indicators",
                "ESG reporting requirements"
            ],
            "digital": [
                "energy-efficient computing",
                "sustainable software engineering practices",
                "data center optimization", 
                "digital technology evaluation frameworks",
                "IT infrastructure management",
                "green coding principles",
                "system architecture efficiency",
                "digital measurement methodologies",
                "cloud computing optimization",
                "sustainable IT procurement"
            ],
            "data": [
                "data analytics methodologies",
                "sustainability metrics",
                "data visualization techniques",
                "carbon footprint measurement",
                "environmental data modeling",
                "impact measurement frameworks",
                "data integration approaches", 
                "predictive modeling for sustainability",
                "sustainability performance indicators",
                "data collection strategies"
            ],
            "management": [
                "sustainability strategy development",
                "change management approaches",
                "stakeholder engagement techniques",
                "project management methodologies",
                "sustainable business models",
                "organizational transformation frameworks",
                "digital leadership principles",
                "resource optimization strategies",
                "risk assessment methodologies", 
                "sustainability governance structures"
            ]
        }
        
        # EQF-specific complexity modifiers
        self.complexity_modifiers = {
            4: ["basic", "fundamental", "standard", "routine"],
            5: ["comprehensive", "specialized", "systematic", "detailed"], 
            6: ["advanced", "complex", "innovative", "sophisticated"],
            7: ["highly specialized", "strategic", "transformational", "comprehensive"],
            8: ["cutting-edge", "pioneering", "paradigm-shifting", "frontier"]
        }

    def get_eqf_appropriate_verb(self, eqf_level: int, domain: str = "knowledge") -> str:
        """Get EQF-appropriate verb ensuring proper complexity progression"""
        if eqf_level not in self.eqf_specific_verbs:
            eqf_level = min(self.eqf_specific_verbs.keys(), key=lambda x: abs(x - eqf_level))
        
        if domain not in self.eqf_specific_verbs[eqf_level]:
            domain = "knowledge"
            
        verbs = self.eqf_specific_verbs[eqf_level][domain]
        return random.choice(verbs)

    def get_complexity_modifier(self, eqf_level: int) -> str:
        """Get appropriate complexity modifier for EQF level"""
        if eqf_level not in self.complexity_modifiers:
            eqf_level = min(self.complexity_modifiers.keys(), key=lambda x: abs(x - eqf_level))
        return random.choice(self.complexity_modifiers[eqf_level])

    def validate_eqf_compliance(self, outcome: str, eqf_level: int) -> bool:
        """Validate that learning outcome matches EQF level expectations"""
        outcome_lower = outcome.lower()
        
        # Check for inappropriate verbs at higher EQF levels
        if eqf_level >= 7:
            inappropriate_verbs = ["apply basic", "interpret", "analyze basic", "identify simple"]
            if any(verb in outcome_lower for verb in inappropriate_verbs):
                return False
                
        if eqf_level == 8:
            # EQF 8 should have advanced verbs
            required_indicators = ["architect", "transform", "pioneer", "establish", "advance"]
            if not any(indicator in outcome_lower for indicator in required_indicators):
                return False
                
        return True

    def get_content_area(self, module_name: str, module_type: List[str], thematic_area: str) -> Dict[str, str]:
        """Determine content areas based on module attributes"""
        content_areas = {}
        
        # Determine knowledge area
        if "sustainability" in module_name.lower() or "esg" in module_name.lower():
            content_areas["knowledge"] = random.choice(self.knowledge_areas["sustainability"])
        elif "data" in module_name.lower() or "analytics" in module_name.lower():
            content_areas["knowledge"] = random.choice(self.knowledge_areas["data"])
        elif any(tech in module_name.lower() for tech in ["software", "code", "digital", "technology"]):
            content_areas["knowledge"] = random.choice(self.knowledge_areas["digital"])
        elif any(mgmt in module_name.lower() for mgmt in ["manage", "strategy", "governance", "leadership"]):
            content_areas["knowledge"] = random.choice(self.knowledge_areas["management"])
        else:
            # Default to thematic area
            if thematic_area.lower() in self.knowledge_areas:
                content_areas["knowledge"] = random.choice(self.knowledge_areas[thematic_area.lower()])
            else:
                content_areas["knowledge"] = random.choice(self.knowledge_areas["sustainability"])
        
        return content_areas

    def generate_learning_outcomes(self,
                                 module_name: str,
                                 module_type: List[str], 
                                 eqf_level: int,
                                 thematic_area: str,
                                 count: int = 4) -> List[str]:
        """
        Generate EQF-compliant learning outcomes using proper Bloom's taxonomy
        
        Args:
            module_name: Name of the module
            module_type: List of module types
            eqf_level: EQF level (4-8)
            thematic_area: Overall thematic area
            count: Number of learning outcomes to generate
            
        Returns:
            List of EQF-compliant learning outcome statements
        """
        outcomes = []
        content_areas = self.get_content_area(module_name, module_type, thematic_area)
        complexity_modifier = self.get_complexity_modifier(eqf_level)
        
        # Generate knowledge outcome with EQF-appropriate verb
        knowledge_verb = self.get_eqf_appropriate_verb(eqf_level, "knowledge")
        knowledge_area = content_areas["knowledge"]
        
        if eqf_level <= 5:
            knowledge_outcome = f"{knowledge_verb.capitalize()} {complexity_modifier} {knowledge_area} in digital sustainability contexts"
        elif eqf_level == 6:
            knowledge_outcome = f"{knowledge_verb.capitalize()} {complexity_modifier} {knowledge_area} and their applications in organizational sustainability initiatives"
        elif eqf_level == 7:
            knowledge_outcome = f"{knowledge_verb.capitalize()} {complexity_modifier} frameworks incorporating {knowledge_area} for organizational transformation"
        else:  # EQF 8
            knowledge_outcome = f"{knowledge_verb.capitalize()} {complexity_modifier} paradigms advancing {knowledge_area} across industry sectors"
            
        outcomes.append(knowledge_outcome)
        
        # Generate skills outcome with EQF-appropriate complexity
        skills_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
        
        if eqf_level <= 5:
            skills_outcome = f"{skills_verb.capitalize()} {complexity_modifier} digital sustainability tools and methodologies"
        elif eqf_level == 6:
            skills_outcome = f"{skills_verb.capitalize()} {complexity_modifier} solutions addressing complex sustainability challenges"
        elif eqf_level == 7:
            skills_outcome = f"{skills_verb.capitalize()} {complexity_modifier} strategic approaches for organizational sustainability transformation"
        else:  # EQF 8
            skills_outcome = f"{skills_verb.capitalize()} {complexity_modifier} methodologies that advance professional practice in digital sustainability"
            
        outcomes.append(skills_outcome)
        
        # Generate attitude/professional outcome
        attitude_verb = self.get_eqf_appropriate_verb(eqf_level, "attitude")
        
        if eqf_level <= 5:
            attitude_outcome = f"{attitude_verb.capitalize()} professional responsibility in implementing digital sustainability practices"
        elif eqf_level == 6:
            attitude_outcome = f"{attitude_verb.capitalize()} ethical leadership principles in complex sustainability decision-making"
        elif eqf_level == 7:
            attitude_outcome = f"{attitude_verb.capitalize()} values-based approaches to drive organizational sustainability transformation"
        else:  # EQF 8
            attitude_outcome = f"{attitude_verb.capitalize()} professional excellence and scholarly integrity in advancing digital sustainability practice"
            
        outcomes.append(attitude_outcome)
        
        # Validate all outcomes for EQF compliance
        validated_outcomes = []
        for outcome in outcomes:
            if self.validate_eqf_compliance(outcome, eqf_level):
                validated_outcomes.append(outcome)
            else:
                # Regenerate non-compliant outcome
                corrected_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
                corrected_outcome = f"{corrected_verb.capitalize()} {complexity_modifier} digital sustainability practices appropriate for EQF level {eqf_level}"
                validated_outcomes.append(corrected_outcome)
        
        return validated_outcomes

    def generate_program_learning_outcomes(self,
                                         role_name: str,
                                         eqf_level: int,
                                         thematic_area: str,
                                         count: int = 6) -> List[str]:
        """
        Generate program-level learning outcomes with proper EQF progression
        """
        outcomes = []
        descriptor = self.eqf_descriptors[eqf_level]
        complexity_modifier = self.get_complexity_modifier(eqf_level)
        
        # Knowledge outcome
        knowledge_verb = self.get_eqf_appropriate_verb(eqf_level, "knowledge")
        knowledge_outcome = f"{knowledge_verb.capitalize()} {descriptor['knowledge']} within digital sustainability domains"
        outcomes.append(knowledge_outcome)
        
        # Skills outcome
        skills_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
        skills_outcome = f"{skills_verb.capitalize()} {descriptor['skills']} to address {complexity_modifier} sustainability challenges"
        outcomes.append(skills_outcome)
        
        # Autonomy/responsibility outcome
        autonomy_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
        autonomy_outcome = f"{autonomy_verb.capitalize()} professional capabilities to {descriptor['autonomy']} in digital sustainability contexts"
        outcomes.append(autonomy_outcome)
        
        # Role-specific outcome
        role_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
        if eqf_level >= 7:
            role_outcome = f"{role_verb.capitalize()} {complexity_modifier} {role_name.lower()} competencies that advance organizational sustainability transformation"
        else:
            role_outcome = f"{role_verb.capitalize()} {complexity_modifier} {role_name.lower()} competencies for professional practice"
        outcomes.append(role_outcome)
        
        # Validate all outcomes
        validated_outcomes = []
        for outcome in outcomes:
            if self.validate_eqf_compliance(outcome, eqf_level):
                validated_outcomes.append(outcome)
        
        return validated_outcomes

    def enhance_existing_outcomes(self,
                                outcomes: List[str],
                                module_name: str, 
                                eqf_level: int) -> List[str]:
        """
        Enhance existing outcomes to ensure EQF compliance
        """
        enhanced_outcomes = []
        
        for outcome in outcomes:
            # Check if outcome needs EQF compliance fix
            if not self.validate_eqf_compliance(outcome, eqf_level):
                # Replace with EQF-appropriate verb
                appropriate_verb = self.get_eqf_appropriate_verb(eqf_level, "skills")
                complexity_modifier = self.get_complexity_modifier(eqf_level)
                
                enhanced_outcome = f"{appropriate_verb.capitalize()} {complexity_modifier} {module_name.lower()} methodologies appropriate for EQF level {eqf_level}"
                enhanced_outcomes.append(enhanced_outcome)
            else:
                enhanced_outcomes.append(outcome)
                
        return enhanced_outcomes
