from scripts.curriculum_generator.domain.competency_mapper import EnhancedCompetencyMapper
"""
Qualification Pathway Generator for T3.2/T3.4 Compliance - Improved Version
"""

def generate_qualification_pathway_section(course_ects, role="DAN", eqf_level=6, target_group="company_staff"):
    """Generate complete qualification pathway HTML section with visual chart"""
    
    try:
        if isinstance(course_ects, str):
            course_ects = float(course_ects)
        
        ects_text = f"This course contributes {course_ects} ECTS credits to your learning record."
        
        pathway_html = f'''

        <!-- QUALIFICATION PATHWAY SECTION - T3.2/T3.4 Compliance -->
        <section class="pathway-section" style="background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%); padding: 30px; margin: 20px 0; border-radius: 10px; border: 2px solid #4CAF50;">
            <h2 style="color: #d32f2f; font-size: 1.6em; margin-bottom: 15px; border-bottom: 2px solid #f57c00; padding-bottom: 8px;">🎓 Qualification Pathway</h2>
            
            <div style="background: white; border: 1px solid #ddd; border-radius: 8px; margin: 20px 0; padding: 20px; overflow-x: auto;">
                <div style="position: relative; height: 280px; min-width: 800px; margin: 40px 0;">
                    <!-- Timeline axis -->
                    <div style="position: absolute; bottom: 40px; left: 0; right: 0; height: 2px; background: #666;"></div>
                    
                    <!-- Time markers -->
                    <div style="position: absolute; left: 15%; bottom: 10px; font-size: 10px; color: #666; text-align: center; transform: translateX(-50%); font-weight: bold;">Month 3</div>
                    <div style="position: absolute; left: 35%; bottom: 10px; font-size: 10px; color: #666; text-align: center; transform: translateX(-50%); font-weight: bold;">Month 8</div>
                    <div style="position: absolute; left: 55%; bottom: 10px; font-size: 10px; color: #666; text-align: center; transform: translateX(-50%); font-weight: bold;">Month 15</div>
                    <div style="position: absolute; left: 75%; bottom: 10px; font-size: 10px; color: #666; text-align: center; transform: translateX(-50%); font-weight: bold;">Year 2</div>
                    
                    <!-- Generic Staircase progression blocks -->
                    <div style="position: absolute; left: 10%; bottom: 60px; width: 15%; height: 80px; background: #e3f2fd; border: 2px solid #2196F3; border-radius: 6px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-size: 11px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        <strong>Foundation</strong><br>
                        5 ECTS Total<br>
                        Basic Certificate<br>
                        <span style="font-size: 9px; font-weight: bold; color: #666;">📚 FOUNDATION</span>
                    </div>
                    
                    <div style="position: absolute; left: 30%; bottom: 100px; width: 18%; height: 80px; background: #e8f5e8; border: 2px solid #4CAF50; border-radius: 6px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-size: 11px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        <strong>Professional</strong><br>
                        15 ECTS Total<br>
                        Professional Certificate<br>
                        <span style="font-size: 9px; font-weight: bold; color: #666;">📊 CAREER READY</span>
                    </div>
                    
                    <div style="position: absolute; left: 52%; bottom: 140px; width: 18%; height: 80px; background: #fff3e0; border: 2px solid #ff9800; border-radius: 6px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-size: 11px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        <strong>Advanced</strong><br>
                        30 ECTS Total<br>
                        Advanced Diploma<br>
                        <span style="font-size: 9px; font-weight: bold; color: #666;">🎓 SENIOR LEVEL</span>
                    </div>
                    
                    <div style="position: absolute; left: 72%; bottom: 180px; width: 25%; height: 80px; background: #f3e5f5; border: 2px solid #9c27b0; border-radius: 6px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-size: 11px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        <strong>Expert</strong><br>
                        60+ ECTS Total<br>
                        Master-Level Program<br>
                        <span style="font-size: 9px; font-weight: bold; color: #666;">⭐ LEADERSHIP</span>
                    </div>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; margin-top: 20px; border-left: 4px solid #4CAF50;">
                <h4 style="margin-top: 0; color: #333;">📋 How Qualification Stacking Works</h4>
                <p style="margin: 10px 0; color: #555;"><strong>Sequential Building:</strong> Each qualification builds on the previous one, creating a complete staircase of credentials. {ects_text}</p>
                
                <p style="margin: 10px 0; color: #555;"><strong>What Each Box Represents:</strong> 
                <span style="background: #e3f2fd; padding: 2px 6px; border-radius: 3px;">Foundation = Basic Skills</span> • 
                <span style="background: #e8f5e8; padding: 2px 6px; border-radius: 3px;">Professional = Job-Ready</span> • 
                <span style="background: #fff3e0; padding: 2px 6px; border-radius: 3px;">Advanced = Senior Role</span> • 
                <span style="background: #f3e5f5; padding: 2px 6px; border-radius: 3px;">Expert = Leadership</span>
                </p>
                
                <p style="margin: 10px 0; color: #555;"><strong>Staircase Progression:</strong> Each step represents a higher level of expertise and career advancement. The height shows increasing responsibility and professional recognition.</p>
            </div>

            <h3 style="color: #d32f2f; margin-top: 30px;">🛤️ Complete Career Pathways</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin: 20px 0;">
                <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #ddd; border-left: 4px solid #2196F3;">
                    <h4 style="margin-top: 0; margin-bottom: 15px; font-size: 1.1em;">📊 Data Analytics Specialist Pathway</h4>
                    <div style="margin: 15px 0;">
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #2196F3; font-size: 0.9em;">
                            <strong>Step 1:</strong> Data Foundations (5 ECTS)<br><em>→ Foundation Certificate in Data Skills</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #2196F3; font-size: 0.9em;">
                            <strong>Step 2:</strong> Analytics & Visualization (10 ECTS)<br><em>→ 15 ECTS Professional Certificate</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #2196F3; font-size: 0.9em;">
                            <strong>Step 3:</strong> Advanced Data Science (15 ECTS)<br><em>→ 30 ECTS Advanced Diploma</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #2196F3; font-size: 0.9em;">
                            <strong>Step 4:</strong> Strategic Analytics Leadership (30 ECTS)<br><em>→ 60 ECTS Expert Qualification</em>
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e8f5e8 100%); padding: 12px; border-radius: 6px; margin-top: 15px; text-align: center; font-size: 0.9em;">
                        <strong>Expert Role:</strong> Chief Data Officer / Analytics Director
                    </div>
                </div>

                <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #ddd; border-left: 4px solid #4CAF50;">
                    <h4 style="margin-top: 0; margin-bottom: 15px; font-size: 1.1em;">👔 Sustainability Management Pathway</h4>
                    <div style="margin: 15px 0;">
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #4CAF50; font-size: 0.9em;">
                            <strong>Step 1:</strong> Sustainability Fundamentals (5 ECTS)<br><em>→ Foundation Certificate in Sustainability</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #4CAF50; font-size: 0.9em;">
                            <strong>Step 2:</strong> Environmental Management (10 ECTS)<br><em>→ 15 ECTS Professional Certificate</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #4CAF50; font-size: 0.9em;">
                            <strong>Step 3:</strong> Strategic Sustainability Planning (15 ECTS)<br><em>→ 30 ECTS Advanced Diploma</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #4CAF50; font-size: 0.9em;">
                            <strong>Step 4:</strong> Executive Leadership & Governance (30 ECTS)<br><em>→ 60 ECTS Expert Qualification</em>
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e8f5e8 100%); padding: 12px; border-radius: 6px; margin-top: 15px; text-align: center; font-size: 0.9em;">
                        <strong>Expert Role:</strong> Chief Sustainability Officer
                    </div>
                </div>

                <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #ddd; border-left: 4px solid #ff9800;">
                    <h4 style="margin-top: 0; margin-bottom: 15px; font-size: 1.1em;">🔧 Technical Engineering Pathway</h4>
                    <div style="margin: 15px 0;">
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #ff9800; font-size: 0.9em;">
                            <strong>Step 1:</strong> Green Technology Basics (5 ECTS)<br><em>→ Foundation Certificate in Green Tech</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #ff9800; font-size: 0.9em;">
                            <strong>Step 2:</strong> Sustainable Systems Design (10 ECTS)<br><em>→ 15 ECTS Professional Certificate</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #ff9800; font-size: 0.9em;">
                            <strong>Step 3:</strong> Advanced Green Infrastructure (15 ECTS)<br><em>→ 30 ECTS Advanced Diploma</em>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #ff9800; font-size: 0.9em;">
                            <strong>Step 4:</strong> Innovation Leadership & R&D (30 ECTS)<br><em>→ 60 ECTS Expert Qualification</em>
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e8f5e8 100%); padding: 12px; border-radius: 6px; margin-top: 15px; text-align: center; font-size: 0.9em;">
                        <strong>Expert Role:</strong> Chief Technology Officer
                    </div>
                </div>
            </div>

            <div style="background: #e3f2fd; padding: 15px; border-radius: 6px; margin-top: 20px; border-left: 4px solid #2196F3;">
                <p style="margin: 0; color: #333; font-style: italic;"><strong>💡 Pathway Flexibility:</strong> You can switch between pathways at any stage up to the Professional Certificate level. Your foundational skills transfer across all specializations.</p>
            </div>
        </section>

        '''
        
        return pathway_html
        
    except Exception as e:
        return f'<!-- Qualification Pathway Error: {str(e)} -->'

def get_framework_mapping(role):
    """Get enhanced framework mapping for the role using comprehensive competency database"""
    
    print(f"🗺️ PATHWAY: Getting framework mapping for role {role}")
    
    try:
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent.parent
        mapper = EnhancedCompetencyMapper(project_root)
        
        # Get comprehensive competencies for role
        competencies = mapper.get_competencies_for_role(role, 6)  # Default EQF 6
        
        print(f"🗺️ PATHWAY: Found {len(competencies)} competencies for {role}")
        
        # Convert to expected format
        framework_mappings = []
        for comp in competencies[:6]:  # Top 6 most relevant
            framework_mappings.append({
                "competency": comp['title'],
                "framework": comp['framework'],
                "reference": f"{comp['id']} - {comp['title'][:50]}",
                "description": comp['description'][:100] + "..." if len(comp['description']) > 100 else comp['description'],
                "application_example": comp.get('application_examples', [''])[0] if comp.get('application_examples') else '',
                "confidence": comp.get('mapping_confidence', 'medium')
            })
        
        print(f"🗺️ PATHWAY: Returning {len(framework_mappings)} enhanced mappings")
        return framework_mappings
        
    except Exception as e:
        print(f"❌ PATHWAY: Enhanced mapping failed: {e}")
        # Fallback to original hardcoded mappings
        return get_original_framework_mapping(role)

def get_original_framework_mapping(role):
    """Original hardcoded framework mapping - kept as fallback"""
def get_original_framework_mapping(role):
    """Get framework mapping for the role"""
    mappings = {
        "DAN": [
            {"competency": "Data Reporting", "framework": "e-CF", "reference": "e-CF 1.3 - Information Management"},
            {"competency": "Critical Thinking", "framework": "DigComp", "reference": "Area 5.1 - Problem Solving"},
            {"competency": "Systems Thinking", "framework": "GreenComp", "reference": "Competence 3.2 - Systems Perspective"},
            {"competency": "Excel Proficiency", "framework": "DigComp", "reference": "Area 3.1 - Content Creation"},
            {"competency": "Quality Validation", "framework": "e-CF", "reference": "e-CF 1.8 - Quality Assurance"}
        ],
        "DSM": [
            {"competency": "Management Planning", "framework": "e-CF", "reference": "e-CF 2.1 - Business Strategy"},
            {"competency": "Stakeholder Engagement", "framework": "GreenComp", "reference": "Competence 1.3 - Collaboration"},
            {"competency": "Digital Leadership", "framework": "DigComp", "reference": "Area 2.1 - Communication"},
            {"competency": "Change Management", "framework": "e-CF", "reference": "e-CF 2.4 - Innovation Management"},
            {"competency": "Sustainability Planning", "framework": "GreenComp", "reference": "Competence 2.1 - Future Vision"}
        ]
    }
    return mappings.get(role, mappings["DAN"])
