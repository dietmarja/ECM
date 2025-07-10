# web/enhanced_app.py
"""
Enhanced Flask Web Interface for DSCG with Intelligent Module Selection
Integrates all enhanced features: D2.1 compliance, smart module selection, bulk generation
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os
import tempfile
import zipfile
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import enhanced components
try:
    from scripts.curriculum_generator.components.enhanced_module_selector import EnhancedModuleSelector
    from scripts.curriculum_generator.components.content_specificity_engine import ContentSpecificityEngine
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced features not available: {e}")
    ENHANCED_FEATURES_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'dscg_enhanced_secret_key_2025'

class EnhancedDSCGWebInterface:
    """Enhanced web interface with intelligent module selection and D2.1 compliance"""
    
    def __init__(self):
        self.project_root = project_root
        if ENHANCED_FEATURES_AVAILABLE:
            self.module_selector = EnhancedModuleSelector(project_root)
            self.content_engine = ContentSpecificityEngine(project_root)
        else:
            self.module_selector = None
            self.content_engine = None
        
        self.roles_data = self._load_roles()
        self.generation_history = []
        
    def _load_roles(self) -> Dict[str, Any]:
        """Load role definitions"""
        try:
            roles_file = self.project_root / "input" / "roles" / "roles.json"
            with open(roles_file, 'r') as f:
                roles_list = json.load(f)
                return {role['id']: role for role in roles_list}
        except Exception as e:
            print(f"❌ Error loading roles: {e}")
            return {}
    
    def get_role_info(self, role_id: str) -> Dict[str, Any]:
        """Get detailed role information"""
        role = self.roles_data.get(role_id, {})
        
        # Add enhanced information if available
        if self.module_selector and role:
            role['enhanced_info'] = {
                'module_count': len(self.module_selector.modules_data),
                'content_categories': list(self.module_selector.content_categories.keys()),
                'has_intelligent_selection': True
            }
        
        return role
    
    def preview_module_selection(self, role_id: str, topic: str, eqf_level: int, 
                                target_modules: int = 8) -> Dict[str, Any]:
        """Preview intelligent module selection"""
        if not self.module_selector:
            return {"error": "Enhanced module selection not available"}
        
        try:
            selected_modules = self.module_selector.select_modules_for_curriculum(
                role_id, topic, eqf_level, target_modules
            )
            
            analysis = self.module_selector.analyze_curriculum_coverage(
                selected_modules, role_id, topic
            )
            
            return {
                "success": True,
                "selected_modules": [
                    {
                        "id": m.get("id", ""),
                        "name": m.get("name", ""),
                        "description": m.get("description", "")[:100] + "...",
                        "ects": m.get("ects_points", 0),
                        "role_relevance": m.get("role_relevance", {}).get(role_id, 0)
                    } for m in selected_modules[:5]  # Top 5 for preview
                ],
                "analysis": analysis,
                "total_modules_available": len(self.module_selector.modules_data)
            }
        except Exception as e:
            return {"error": f"Module selection failed: {str(e)}"}
    
    def generate_curriculum_enhanced(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate curriculum with enhanced features"""
        try:
            # Build command for enhanced generation
            cmd = [
                "python3", 
                str(self.project_root / "scripts/curriculum_generator/main_enhanced_uol_final_fixed_v2.py"),
                "--role", config["role"],
                "--eqf-level", str(config["eqf_level"]),
                "--ects", str(config["ects"]),
                "--uol", str(config["uol"]),
                "--topic", config["topic"],
                "--theme", config.get("theme", "eu_official"),
                "--output-json",
                "--force"
            ]
            
            if config.get("generate_docx", False):
                cmd.append("--output-docx")
            
            # Execute generation
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  cwd=self.project_root, timeout=120)
            
            success = result.returncode == 0
            
            if success:
                # Extract generated files information
                output_lines = result.stdout.split('\n')
                generated_files = []
                compliance_score = None
                d21_gaps = {}
                
                for line in output_lines:
                    if "Generated" in line and ("JSON:" in line or "HTML:" in line or "DOCX:" in line):
                        generated_files.append(line.strip())
                    elif "Role Alignment:" in line:
                        try:
                            compliance_score = float(line.split("Role Alignment:")[1].split("%")[0].strip())
                        except:
                            pass
                    elif "ESG Depth:" in line:
                        d21_gaps["esg_depth"] = "Covered" in line
                    elif "Regulatory Skills:" in line:
                        d21_gaps["regulatory_skills"] = "Covered" in line
                    elif "Technical Implementation:" in line:
                        d21_gaps["technical_implementation"] = "Covered" in line
                
                # Store in generation history
                generation_record = {
                    "config": config,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "compliance_score": compliance_score,
                    "d21_gaps_addressed": d21_gaps,
                    "generated_files": generated_files
                }
                self.generation_history.append(generation_record)
                
                return {
                    "success": True,
                    "message": "Curriculum generated successfully with enhanced module selection",
                    "compliance_score": compliance_score,
                    "d21_gaps_addressed": d21_gaps,
                    "generated_files": generated_files,
                    "enhanced_features_used": True
                }
            else:
                error_msg = result.stderr if result.stderr else "Unknown generation error"
                return {
                    "success": False,
                    "error": error_msg,
                    "enhanced_features_used": ENHANCED_FEATURES_AVAILABLE
                }
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Generation timeout (120 seconds)"}
        except Exception as e:
            return {"success": False, "error": f"Generation exception: {str(e)}"}
    
    def bulk_generate_d21_priority(self) -> Dict[str, Any]:
        """Run bulk generation for D2.1 priority areas"""
        try:
            cmd = [
                "python3",
                str(self.project_root / "scripts/enhanced_bulk_generator.py"),
                "--mode", "d21-priority",
                "--formats", "json", "html"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  cwd=self.project_root, timeout=600)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "D2.1 priority curricula generated successfully",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or "Bulk generation failed"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize enhanced interface
enhanced_interface = EnhancedDSCGWebInterface()

@app.route('/')
def index():
    """Enhanced home page"""
    return render_template('enhanced_index.html', 
                         enhanced_available=ENHANCED_FEATURES_AVAILABLE,
                         total_modules=len(enhanced_interface.module_selector.modules_data) if enhanced_interface.module_selector else 0)

@app.route('/generator')
def generator():
    """Enhanced curriculum generator page"""
    return render_template('enhanced_generator.html', 
                         roles=enhanced_interface.roles_data,
                         enhanced_available=ENHANCED_FEATURES_AVAILABLE)

@app.route('/api/preview_modules', methods=['POST'])
def api_preview_modules():
    """API endpoint for module selection preview"""
    data = request.json
    
    if not enhanced_interface.module_selector:
        return jsonify({"error": "Enhanced module selection not available"})
    
    preview = enhanced_interface.preview_module_selection(
        data.get('role'),
        data.get('topic', 'Digital Sustainability'),
        int(data.get('eqf_level', 6))
    )
    
    return jsonify(preview)

@app.route('/api/generate_curriculum', methods=['POST'])
def api_generate_curriculum():
    """API endpoint for enhanced curriculum generation"""
    data = request.json
    
    result = enhanced_interface.generate_curriculum_enhanced(data)
    return jsonify(result)

@app.route('/api/bulk_generate_d21', methods=['POST'])
def api_bulk_generate_d21():
    """API endpoint for D2.1 priority bulk generation"""
    result = enhanced_interface.bulk_generate_d21_priority()
    return jsonify(result)

@app.route('/api/role_info/<role_id>')
def api_role_info(role_id):
    """API endpoint for detailed role information"""
    role_info = enhanced_interface.get_role_info(role_id)
    return jsonify(role_info)

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard with generation history and compliance metrics"""
    
    # Calculate dashboard metrics
    metrics = {
        "total_generations": len(enhanced_interface.generation_history),
        "successful_generations": sum(1 for g in enhanced_interface.generation_history if g["success"]),
        "average_compliance": 0,
        "d21_coverage": {"esg": 0, "regulatory": 0, "technical": 0}
    }
    
    if enhanced_interface.generation_history:
        compliance_scores = [g.get("compliance_score", 0) for g in enhanced_interface.generation_history 
                           if g.get("compliance_score") is not None]
        if compliance_scores:
            metrics["average_compliance"] = sum(compliance_scores) / len(compliance_scores)
        
        # D2.1 gap coverage analysis
        for generation in enhanced_interface.generation_history:
            gaps = generation.get("d21_gaps_addressed", {})
            if gaps.get("esg_depth"):
                metrics["d21_coverage"]["esg"] += 1
            if gaps.get("regulatory_skills"):
                metrics["d21_coverage"]["regulatory"] += 1
            if gaps.get("technical_implementation"):
                metrics["d21_coverage"]["technical"] += 1
    
    return render_template('enhanced_dashboard.html', 
                         metrics=metrics,
                         generation_history=enhanced_interface.generation_history[-10:],  # Last 10
                         enhanced_available=ENHANCED_FEATURES_AVAILABLE)

@app.route('/modules')
def modules():
    """Enhanced modules explorer"""
    if not enhanced_interface.module_selector:
        flash("Enhanced module features not available", "warning")
        return redirect(url_for('index'))
    
    # Get module statistics
    modules = enhanced_interface.module_selector.modules_data
    module_stats = {
        "total_modules": len(modules),
        "by_category": {},
        "by_eqf_level": {},
        "by_thematic_area": {}
    }
    
    for module in modules:
        categories = enhanced_interface.module_selector.classify_module_content(module)
        for category in categories:
            module_stats["by_category"][category] = module_stats["by_category"].get(category, 0) + 1
        
        eqf = module.get("eqf_level", 6)
        module_stats["by_eqf_level"][f"EQF {eqf}"] = module_stats["by_eqf_level"].get(f"EQF {eqf}", 0) + 1
        
        area = module.get("thematic_area", "General")
        module_stats["by_thematic_area"][area] = module_stats["by_thematic_area"].get(area, 0) + 1
    
    return render_template('enhanced_modules.html', 
                         module_stats=module_stats,
                         sample_modules=modules[:10])  # Show first 10 as samples

if __name__ == '__main__':
    print("🚀 Starting Enhanced DSCG Web Interface")
    print(f"   🧠 Enhanced Features: {'✅ Available' if ENHANCED_FEATURES_AVAILABLE else '❌ Not Available'}")
    if enhanced_interface.module_selector:
        print(f"   📦 Total Modules: {len(enhanced_interface.module_selector.modules_data)}")
    print(f"   🌐 Access: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
