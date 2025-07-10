# scripts/curriculum_generator/core/output_manager.py
"""
Output Manager - FIXED to use correct quality metrics
NO duplicate quality metrics calculations
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class OutputManager:
    """Manages curriculum output generation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def save_curriculum(
        self,
        curriculum: Dict[str, Any],
        output_dir: str,
        topic: str,
        eqf_level: int,
        role_id: str
    ) -> List[str]:
        """Save curriculum files - FIXED to preserve quality metrics"""
        
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        topic_safe = topic.replace(' ', '_').replace('/', '_').upper()
        timestamp = datetime.now().strftime('%Y%m%d')
        base_filename = f"{role_id}_{topic_safe}_{eqf_level}_{timestamp}"
        
        files_created = []
        
        # Save JSON file (preserve original quality metrics)
        json_file = output_path / f"{base_filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(curriculum, f, indent=2, ensure_ascii=False)
        files_created.append(str(json_file))
        
        # Save HTML file
        html_file = output_path / f"{base_filename}.html"
        html_content = self._generate_html_output(curriculum)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        files_created.append(str(html_file))
        
        # Save summary JSON
        summary_file = output_path / f"{base_filename}_summary.json"
        summary = self._generate_summary(curriculum)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        files_created.append(str(summary_file))
        
        print(f"✅ Saved curriculum files: {len(files_created)} files")
        
        return files_created
    
    def _generate_summary(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Generate curriculum summary - FIXED to use original quality metrics"""
        
        metadata = curriculum.get('metadata', {})
        quality_metrics = curriculum.get('quality_metrics', {})
        
        # USE THE ORIGINAL QUALITY METRICS - don't recalculate!
        return {
            'curriculum_id': curriculum.get('curriculum_id', ''),
            'title': metadata.get('title', ''),
            'role_id': metadata.get('role_id', ''),
            'topic': metadata.get('topic', ''),
            'eqf_level': metadata.get('eqf_level', 0),
            'total_ects': metadata.get('actual_ects', 0),
            'total_modules': metadata.get('num_modules', 0),
            'semesters': metadata.get('num_semesters', 0),
            'generated_date': metadata.get('generated_date', ''),
            'quality_metrics': quality_metrics,  # PRESERVE original metrics
            'compliance_frameworks': metadata.get('compliance_frameworks', [])
        }
    
    def _generate_html_output(self, curriculum: Dict[str, Any]) -> str:
        """Generate HTML output - FIXED to show correct quality metrics"""
        
        metadata = curriculum.get('metadata', {})
        quality_metrics = curriculum.get('quality_metrics', {})
        semesters = curriculum.get('curriculum_structure', {}).get('semester_breakdown', [])
        
        # EXTRACT quality metrics from the curriculum object (don't recalculate)
        ects_efficiency = quality_metrics.get('ects_efficiency', 0)
        topic_relevance = quality_metrics.get('topic_relevance', 0)
        topic_coverage = quality_metrics.get('topic_coverage', 0)
        flexibility_score = quality_metrics.get('flexibility_score', 0)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata.get('title', 'Curriculum')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; font-weight: 300; }}
        .header .subtitle {{ font-size: 1.2em; opacity: 0.9; margin-top: 10px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .metric-card {{ background: #f8f9fa; padding: 25px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .metric-title {{ font-size: 0.9em; color: #6c757d; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.2em; font-weight: bold; color: #2c3e50; }}
        .semester {{ background: white; border: 1px solid #e9ecef; border-radius: 8px; margin-bottom: 25px; overflow: hidden; }}
        .semester-header {{ background: #f8f9fa; padding: 20px; border-bottom: 1px solid #e9ecef; }}
        .semester-title {{ font-size: 1.4em; font-weight: 600; color: #2c3e50; margin: 0; }}
        .semester-info {{ color: #6c757d; margin-top: 5px; }}
        .modules {{ padding: 20px; }}
        .module {{ background: #fdfdfe; border: 1px solid #f1f3f4; border-radius: 6px; padding: 15px; margin-bottom: 12px; }}
        .module-title {{ font-weight: 600; color: #2c3e50; margin-bottom: 5px; }}
        .module-details {{ color: #6c757d; font-size: 0.9em; }}
        .ects-badge {{ background: #667eea; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{metadata.get('title', 'Digital Sustainability Curriculum')}</h1>
            <div class="subtitle">
                EQF Level {metadata.get('eqf_level', 'N/A')} • 
                {metadata.get('actual_ects', 0)} ECTS • 
                {len(semesters)} Semesters •
                Generated {metadata.get('generated_date', '').split('T')[0] if metadata.get('generated_date') else 'N/A'}
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-title">ECTS Efficiency</div>
                <div class="metric-value">{ects_efficiency}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Topic Relevance</div>
                <div class="metric-value">{topic_relevance}/10</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Topic Coverage</div>
                <div class="metric-value">{topic_coverage}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Flexibility Score</div>
                <div class="metric-value">{flexibility_score}%</div>
            </div>
        </div>
        
        <h2>Semester Structure</h2>
        """
        
        for semester in semesters:
            semester_modules = semester.get('modules', [])
            html_content += f"""
        <div class="semester">
            <div class="semester-header">
                <div class="semester-title">{semester.get('semester_name', 'Semester')}</div>
                <div class="semester-info">
                    {semester.get('focus_area', 'General Focus')} • 
                    {semester.get('target_ects', 0)} ECTS • 
                    {len(semester_modules)} Modules
                </div>
            </div>
            <div class="modules">
            """
            
            for module in semester_modules:
                html_content += f"""
                <div class="module">
                    <div class="module-title">{module.get('module_name', 'Unknown Module')}</div>
                    <div class="module-details">
                        <span class="ects-badge">{module.get('ects', 0)} ECTS</span>
                        {module.get('thematic_area', 'General')} • 
                        {', '.join(module.get('delivery_methods', ['Unknown']))}
                    </div>
                </div>
                """
            
            html_content += """
            </div>
        </div>
            """
        
        html_content += """
    </div>
</body>
</html>
        """
        
        return html_content
