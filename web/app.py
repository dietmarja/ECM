# web/app.py - Complete ECM Flask Web Application
"""
Educational Curriculum Modeller (ECM) - Web Interface
Complete Flask application for localhost testing and deployment
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, abort
import os
import sys
import json
import traceback
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime
import logging

# Setup project paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "scripts"))

# Import ECM components
try:
    from generate_curricula_toggle import EnhancedD4SCurriculumGenerator
    ECM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: ECM components not available: {e}")
    ECM_AVAILABLE = False

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'ecm-dev-secret-key-change-in-production'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    app.config['PROJECT_ROOT'] = PROJECT_ROOT
    app.config['DEBUG'] = True if config_name == 'development' else False
    
    # Ensure output directories exist
    output_dir = PROJECT_ROOT / "output" / "curricula"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html', 
                             ecm_available=ECM_AVAILABLE,
                             project_root=PROJECT_ROOT)
    
    @app.route('/generator')
    def generator():
        """Enhanced curriculum generator page"""
        if not ECM_AVAILABLE:
            flash('ECM components not available. Please check installation.', 'error')
            return redirect(url_for('index'))
        
        # Define available roles and specifications
        roles = {
            'DAN': {
                'title': 'Sustainability Data Analyst',
                'description': 'ESG reporting and compliance specialist',
                'eqf_levels': [5],
                'ects_range': [0.5, 7.5]
            },
            'DSM': {
                'title': 'Digital Sustainability Manager', 
                'description': 'Implementation and cross-functional coordination',
                'eqf_levels': [6],
                'ects_range': [1.0, 50.0]
            },
            'DSE': {
                'title': 'Digital Sustainability Engineer',
                'description': 'Sustainable IT infrastructure and operations', 
                'eqf_levels': [5],
                'ects_range': [2.0, 20.0]
            },
            'DSL': {
                'title': 'Digital Sustainability Leader',
                'description': 'Strategic transformation and organizational change',
                'eqf_levels': [6, 7],
                'ects_range': [5.0, 120.0]
            },
            'DSC': {
                'title': 'Digital Sustainability Consultant',
                'description': 'Advisory services and solution design',
                'eqf_levels': [6, 7], 
                'ects_range': [10.0, 180.0]
            }
        }
        
        return render_template('generator.html', 
                             roles=roles,
                             ecm_available=ECM_AVAILABLE)
    
    @app.route('/generate_curriculum', methods=['POST'])
    def generate_curriculum():
        """Generate curriculum using enhanced generator"""
        if not ECM_AVAILABLE:
            return jsonify({'error': 'ECM components not available'}), 500
        
        try:
            # Get form data
            role_id = request.form.get('role')
            eqf_level = int(request.form.get('eqf_level', 6))
            ects = float(request.form.get('ects', 5.0))
            visual_mapping = request.form.get('visual_mapping') == 'on'
            
            # Output format selection
            output_json = request.form.get('output_json') == 'on'
            output_html = request.form.get('output_html') == 'on'
            output_docx = request.form.get('output_docx') == 'on'
            
            if not any([output_json, output_html, output_docx]):
                flash('Please select at least one output format', 'warning')
                return redirect(url_for('generator'))
            
            # Initialize enhanced curriculum generator
            generator = EnhancedD4SCurriculumGenerator(
                visual_mapping=visual_mapping
            )
            
            # Find matching curriculum specification
            matching_spec = None
            for spec in generator.curricula_specs:
                if (spec['role_id'] == role_id and 
                    spec['eqf_level'] == eqf_level and 
                    abs(spec['ects'] - ects) < 0.1):
                    matching_spec = spec
                    break
            
            if not matching_spec:
                # Create custom curriculum specification
                matching_spec = {
                    'number': '99',
                    'id': f'{role_id}_{eqf_level}_Custom',
                    'title': f'Custom {role_id} Programme',
                    'role_id': role_id,
                    'eqf_level': eqf_level,
                    'ects': ects,
                    'description': f'Custom curriculum for {role_id} at EQF {eqf_level}',
                    'target_audience': 'Custom professional development programme',
                    'filename': f'custom_{role_id}_{eqf_level}_{int(ects*10)}',
                    'pathway_position': f'Custom Level {eqf_level} Professional Development'
                }
            
            # Generate curriculum
            logger.info(f"Generating curriculum: {matching_spec['id']}")
            curriculum = generator.generate_curriculum(matching_spec)
            
            # Create temporary directory for outputs
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Generate files
                generated_files = []
                
                if output_json:
                    json_path = temp_path / f"{matching_spec['filename']}.json"
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(curriculum, f, indent=2, ensure_ascii=False)
                    generated_files.append(json_path)
                
                if output_html:
                    html_path = generator.save_curriculum_html(curriculum, matching_spec['filename'])
                    # Copy to temp directory
                    temp_html_path = temp_path / f"{matching_spec['filename']}.html"
                    temp_html_path.write_text(html_path.read_text(encoding='utf-8'), encoding='utf-8')
                    generated_files.append(temp_html_path)
                
                if output_docx:
                    try:
                        docx_path = generator.save_curriculum_docx(curriculum, matching_spec['filename'])
                        # Copy to temp directory
                        temp_docx_path = temp_path / f"{matching_spec['filename']}.docx"
                        temp_docx_path.write_bytes(docx_path.read_bytes())
                        generated_files.append(temp_docx_path)
                    except Exception as e:
                        logger.warning(f"DOCX generation failed: {e}")
                        flash('DOCX generation failed. Install python-docx: pip install python-docx', 'warning')
                
                if not generated_files:
                    flash('No files generated', 'error')
                    return redirect(url_for('generator'))
                
                # If single file, send directly
                if len(generated_files) == 1:
                    file_path = generated_files[0]
                    return send_file(
                        file_path,
                        as_attachment=True,
                        download_name=file_path.name
                    )
                
                # If multiple files, create ZIP
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                zip_filename = f"ECM_{role_id}_EQF{eqf_level}_{ects}ECTS_{timestamp}.zip"
                zip_path = temp_path / zip_filename
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in generated_files:
                        zipf.write(file_path, file_path.name)
                
                return send_file(
                    zip_path,
                    as_attachment=True,
                    download_name=zip_filename
                )
        
        except Exception as e:
            logger.error(f"Curriculum generation error: {e}")
            logger.error(traceback.format_exc())
            flash(f'Generation error: {str(e)}', 'error')
            return redirect(url_for('generator'))
    
    @app.route('/generate_all_curricula', methods=['POST'])
    def generate_all_curricula():
        """Generate all 10 standard curricula"""
        if not ECM_AVAILABLE:
            return jsonify({'error': 'ECM components not available'}), 500
        
        try:
            visual_mapping = request.form.get('visual_mapping') == 'on'
            
            # Initialize generator
            generator = EnhancedD4SCurriculumGenerator(visual_mapping=visual_mapping)
            
            # Generate all curricula
            logger.info("Generating all 10 standard curricula...")
            generated_files = generator.generate_all_curricula()
            
            # Create ZIP with all generated files
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            zip_filename = f"ECM_All_Curricula_{timestamp}.zip"
            
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in generated_files:
                        file_path = Path(file_path)
                        if file_path.exists():
                            zipf.write(file_path, file_path.name)
                
                return send_file(
                    temp_zip.name,
                    as_attachment=True,
                    download_name=zip_filename
                )
        
        except Exception as e:
            logger.error(f"All curricula generation error: {e}")
            logger.error(traceback.format_exc())
            flash(f'Generation error: {str(e)}', 'error')
            return redirect(url_for('generator'))
    
    @app.route('/analysis')
    def analysis():
        """Analysis dashboard"""
        return render_template('analysis.html')
    
    @app.route('/run_analysis', methods=['POST'])
    def run_analysis():
        """Run ECM comprehensive analysis"""
        try:
            # Import analysis components
            from ecm_comprehensive_analysis import ECMAnalysisEngine
            
            # Initialize analysis engine
            engine = ECMAnalysisEngine()
            
            # Run analysis
            engine.load_learning_units()
            engine.define_frameworks()
            engine.analyze_learning_units()
            engine.analyze_versatility()
            
            # Generate outputs
            engine.create_visualizations()
            engine.export_results()
            summary = engine.generate_report()
            
            flash('Analysis completed successfully!', 'success')
            return jsonify({
                'status': 'success',
                'message': 'Analysis completed',
                'summary': summary
            })
        
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/status')
    def api_status():
        """API status endpoint"""
        return jsonify({
            'status': 'running',
            'ecm_available': ECM_AVAILABLE,
            'project_root': str(PROJECT_ROOT),
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/check_dependencies')
    def check_dependencies():
        """Check system dependencies"""
        dependencies = {
            'python_docx': False,
            'pandas': False,
            'numpy': False,
            'matplotlib': False,
            'sklearn': False
        }
        
        # Check each dependency
        for dep in dependencies:
            try:
                if dep == 'python_docx':
                    import docx
                else:
                    __import__(dep)
                dependencies[dep] = True
            except ImportError:
                pass
        
        return jsonify({
            'dependencies': dependencies,
            'all_available': all(dependencies.values())
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', 
                             error_code=404,
                             error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html',
                             error_code=500, 
                             error_message="Internal server error"), 500
    
    return app

# Create templates directory and basic templates
def create_templates():
    """Create basic HTML templates for the web interface"""
    templates_dir = PROJECT_ROOT / "web" / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ECM - Educational Curriculum Modeller{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .navbar-brand { font-weight: bold; }
        .card { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn-primary { background-color: #2c5530; border-color: #2c5530; }
        .btn-primary:hover { background-color: #1e3a22; border-color: #1e3a22; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-graduation-cap"></i> ECM
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                <a class="nav-link" href="{{ url_for('generator') }}">Generator</a>
                <a class="nav-link" href="{{ url_for('analysis') }}">Analysis</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    # Index template
    index_template = '''{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-body">
                <h1 class="card-title">Educational Curriculum Modeller (ECM)</h1>
                <p class="card-text lead">Multi-Objective Curriculum Optimization Framework</p>
                <p class="card-text">
                    ECM generates modular curricula and educational profiles that balance competence coverage, 
                    regulatory compliance, and resource efficiency across multiple educational frameworks.
                </p>
                
                {% if ecm_available %}
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> ECM components loaded successfully
                    </div>
                {% else %}
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i> ECM components not available. 
                        Please check installation.
                    </div>
                {% endif %}
                
                <div class="row mt-4">
                    <div class="col-md-6">
                        <h5>Key Features</h5>
                        <ul>
                            <li>10 professional curricula generation</li>
                            <li>Educational standards compliance</li>
                            <li>Multiple output formats (JSON, HTML, DOCX)</li>
                            <li>Framework analysis and visualization</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h5>Quick Actions</h5>
                        <a href="{{ url_for('generator') }}" class="btn btn-primary btn-lg d-block mb-2">
                            <i class="fas fa-cog"></i> Generate Curricula
                        </a>
                        <a href="{{ url_for('analysis') }}" class="btn btn-outline-primary d-block">
                            <i class="fas fa-chart-bar"></i> Run Analysis
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">System Status</h5>
                <p><strong>Project Root:</strong><br><small class="text-muted">{{ project_root }}</small></p>
                <button class="btn btn-outline-secondary btn-sm" onclick="checkDependencies()">
                    Check Dependencies
                </button>
                <div id="dependencies-status" class="mt-2"></div>
            </div>
        </div>
    </div>
</div>

<script>
function checkDependencies() {
    fetch('/check_dependencies')
        .then(response => response.json())
        .then(data => {
            const status = document.getElementById('dependencies-status');
            let html = '<small>';
            for (const [dep, available] of Object.entries(data.dependencies)) {
                const icon = available ? 'fa-check text-success' : 'fa-times text-danger';
                html += `<div><i class="fas ${icon}"></i> ${dep}</div>`;
            }
            html += '</small>';
            status.innerHTML = html;
        });
}
</script>
{% endblock %}'''
    
    # Generator template
    generator_template = '''{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Educational Curriculum Generator</h2>
                <p class="card-text">Generate professional curricula with educational standards compliance.</p>
                
                <form method="POST" action="{{ url_for('generate_curriculum') }}" onsubmit="return validateForm()">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="role" class="form-label">Professional Role</label>
                                <select class="form-select" id="role" name="role" required>
                                    {% for role_id, role_info in roles.items() %}
                                    <option value="{{ role_id }}">{{ role_info.title }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="mb-3">
                                <label for="eqf_level" class="form-label">EQF Level</label>
                                <select class="form-select" id="eqf_level" name="eqf_level" required>
                                    <option value="5">Level 5</option>
                                    <option value="6" selected>Level 6</option>
                                    <option value="7">Level 7</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="mb-3">
                                <label for="ects" class="form-label">ECTS Credits</label>
                                <input type="number" class="form-control" id="ects" name="ects" 
                                       min="0.5" max="180" step="0.5" value="5.0" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Output Formats</label>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="output_json" name="output_json" checked>
                            <label class="form-check-label" for="output_json">JSON</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="output_html" name="output_html" checked>
                            <label class="form-check-label" for="output_html">HTML</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="output_docx" name="output_docx">
                            <label class="form-check-label" for="output_docx">DOCX (Word Document)</label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="visual_mapping" name="visual_mapping">
                            <label class="form-check-label" for="visual_mapping">
                                Enable Visual Mapping (slower but more detailed)
                            </label>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-download"></i> Generate Curriculum
                    </button>
                </form>
                
                <hr>
                
                <form method="POST" action="{{ url_for('generate_all_curricula') }}">
                    <h5>Generate All Standard Curricula</h5>
                    <p class="text-muted">Generate all 10 professional curricula (30 files total)</p>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="visual_mapping_all" name="visual_mapping">
                            <label class="form-check-label" for="visual_mapping_all">
                                Enable Visual Mapping
                            </label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-download"></i> Generate All Curricula
                    </button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Role Information</h5>
                <div id="role-info">
                    {% for role_id, role_info in roles.items() %}
                    <div class="role-detail" data-role="{{ role_id }}" style="display: none;">
                        <h6>{{ role_info.title }}</h6>
                        <p><small>{{ role_info.description }}</small></p>
                        <p><strong>EQF Levels:</strong> {{ role_info.eqf_levels|join(', ') }}</p>
                        <p><strong>ECTS Range:</strong> {{ role_info.ects_range[0] }} - {{ role_info.ects_range[1] }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function validateForm() {
    const formats = ['output_json', 'output_html', 'output_docx'];
    const checked = formats.some(id => document.getElementById(id).checked);
    
    if (!checked) {
        alert('Please select at least one output format');
        return false;
    }
    return true;
}

// Show role information
document.getElementById('role').addEventListener('change', function() {
    const selectedRole = this.value;
    document.querySelectorAll('.role-detail').forEach(el => el.style.display = 'none');
    const roleDetail = document.querySelector(`[data-role="${selectedRole}"]`);
    if (roleDetail) roleDetail.style.display = 'block';
});

// Trigger initial role display
document.getElementById('role').dispatchEvent(new Event('change'));
</script>
{% endblock %}'''
    
    # Analysis template
    analysis_template = '''{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">ECM Analysis Dashboard</h2>
                <p class="card-text">Comprehensive framework analysis and learning unit evaluation.</p>
                
                <button id="run-analysis" class="btn btn-primary" onclick="runAnalysis()">
                    <i class="fas fa-play"></i> Run Comprehensive Analysis
                </button>
                
                <div id="analysis-progress" class="mt-3" style="display: none;">
                    <div class="alert alert-info">
                        <i class="fas fa-spinner fa-spin"></i> Running analysis... This may take 5-6 minutes.
                    </div>
                </div>
                
                <div id="analysis-results" class="mt-3"></div>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Analysis Features</h5>
                <ul>
                    <li>90 learning units analysis</li>
                    <li>7 international frameworks</li>
                    <li>Versatility classification</li>
                    <li>Quality scoring</li>
                    <li>Comprehensive visualizations</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<script>
function runAnalysis() {
    const button = document.getElementById('run-analysis');
    const progress = document.getElementById('analysis-progress');
    const results = document.getElementById('analysis-results');
    
    button.disabled = true;
    progress.style.display = 'block';
    results.innerHTML = '';
    
    fetch('/run_analysis', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            progress.style.display = 'none';
            button.disabled = false;
            
            if (data.status === 'success') {
                results.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> Analysis completed successfully!
                    </div>
                    <pre class="bg-light p-3 rounded">${data.summary || 'Analysis completed'}</pre>
                `;
            } else {
                results.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i> Analysis failed: ${data.message}
                    </div>
                `;
            }
        })
        .catch(error => {
            progress.style.display = 'none';
            button.disabled = false;
            results.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i> Network error: ${error.message}
                </div>
            `;
        });
}
</script>
{% endblock %}'''
    
    # Error template
    error_template = '''{% extends "base.html" %}
{% block content %}
<div class="text-center">
    <h1 class="display-1">{{ error_code }}</h1>
    <h2>{{ error_message }}</h2>
    <a href="{{ url_for('index') }}" class="btn btn-primary">
        <i class="fas fa-home"></i> Return Home
    </a>
</div>
{% endblock %}'''
    
    # Write templates
    (templates_dir / "base.html").write_text(base_template)
    (templates_dir / "index.html").write_text(index_template)
    (templates_dir / "generator.html").write_text(generator_template)
    (templates_dir / "analysis.html").write_text(analysis_template)
    (templates_dir / "error.html").write_text(error_template)
    
    print(f"✅ Templates created in {templates_dir}")

if __name__ == '__main__':
    # Create templates if they don't exist
    create_templates()
    
    # Create and run the Flask app
    app = create_app('development')
    
    print("🚀 Starting ECM Web Interface...")
    print(f"📂 Project Root: {PROJECT_ROOT}")
    print(f"🔧 ECM Available: {ECM_AVAILABLE}")
    print("🌐 Access at: http://localhost:5001")
    print("✨ Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5001, debug=True)