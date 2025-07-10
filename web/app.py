# web/app.py - Extended with DOCX support
"""
Enhanced Flask Web Interface with DOCX Download Support
Extension to existing web interface - add these routes and modify existing ones
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import sys
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import DOCX-enabled components
from scripts.curriculum_generator.core.output_manager import OutputManager
from scripts.curriculum_generator.components.docx_generator import DocxGenerator

# Add these routes to existing Flask app

@app.route('/generate_curriculum_with_docx', methods=['POST'])
def generate_curriculum_with_docx():
    """Generate curriculum with DOCX support"""
    try:
        # Get form data
        role_id = request.form.get('role')
        eqf_level = int(request.form.get('eqf_level'))
        ects = float(request.form.get('ects'))
        uol = int(request.form.get('uol'))
        topic = request.form.get('topic', 'Digital Sustainability')
        theme = request.form.get('theme', 'material_gray')
        
        # Format options
        output_json = request.form.get('output_json') == 'on'
        output_html = request.form.get('output_html') == 'on'
        output_docx = request.form.get('output_docx') == 'on'
        
        if not any([output_json, output_html, output_docx]):
            flash('Please select at least one output format', 'warning')
            return redirect(url_for('generator'))
        
        # Initialize enhanced output manager
        output_manager = OutputManager(project_root)
        
        # Check DOCX availability
        if output_docx and not output_manager.docx_available:
            flash('DOCX generation not available. Install python-docx: pip install python-docx', 'warning')
            output_docx = False
        
        # Import generation components
        from scripts.curriculum_generator.domain.role_manager import RoleManager
        from scripts.curriculum_generator.components.uol_learning_manager import UOLLearningManager
        from scripts.curriculum_generator.components.general_industry_content_generator import GeneralIndustryContentGenerator
        from scripts.curriculum_generator.main_enhanced_uol_final_fixed_v2 import apply_final_enhancements_v2, generate_final_html_v2
        
        # Generate curriculum
        role_manager = RoleManager(project_root)
        uol_manager = UOLLearningManager()
        content_generator = GeneralIndustryContentGenerator()
        
        role_info = role_manager.get_role(role_id)
        if not role_info:
            flash(f'Role {role_id} not found', 'error')
            return redirect(url_for('generator'))
        
        # Generate learning units
        base_units = uol_manager.distribute_ects_across_uol(
            total_ects=ects,
            uol=uol,
            role_id=role_id,
            topic=topic
        )
        
        # Enhance units with content
        enhanced_units = []
        for unit in base_units:
            concrete_title = content_generator.generate_concrete_unit_title(
                unit['unit_number'], 
                unit['progression_level'], 
                role_id, 
                topic
            )
            
            base_outcomes = content_generator.generate_specific_learning_outcomes(
                concrete_title,
                unit['progression_level'],
                role_id,
                topic,
                unit['ects']
            )
            
            enhanced_unit = {
                'unit_id': unit['unit_id'],
                'unit_number': unit['unit_number'],
                'unit_title': concrete_title,
                'progression_level': unit['progression_level'],
                'ects': unit['ects'],
                'estimated_hours': unit['estimated_hours'],
                'specific_learning_outcomes': base_outcomes,
                'delivery_approach': unit['delivery_approach'],
                'assessment_method': unit['assessment_method'],
                'framework_mappings': content_generator.get_framework_mappings(unit['progression_level'])
            }
            enhanced_units.append(enhanced_unit)
        
        # Create curriculum
        base_curriculum = {
            'metadata': {
                'role_id': role_id,
                'role_name': role_info['name'],
                'topic': topic,
                'eqf_level': eqf_level,
                'target_ects': ects,
                'actual_ects': sum(unit['ects'] for unit in enhanced_units),
                'units_requested': uol,
                'units_generated': len(enhanced_units),
                'generation_date': datetime.now().isoformat(),
                'system_version': 'Web_Interface_DOCX_v1.0'
            },
            'learning_units': enhanced_units
        }
        
        # Apply enhancements
        final_curriculum = apply_final_enhancements_v2(base_curriculum)
        
        # Generate HTML if needed
        html_content = ""
        if output_html or output_docx:  # DOCX generator might need HTML data
            html_content = generate_final_html_v2(final_curriculum, theme)
        
        # Create temporary directory for outputs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Generate outputs using enhanced output manager
            output_files = output_manager.save_curriculum_with_all_formats(
                curriculum=final_curriculum,
                curriculum_html=html_content,
                output_dir=str(temp_path),
                topic=topic,
                eqf_level=eqf_level,
                role_id=role_id,
                theme_name=theme,
                output_docx=output_docx,
                include_profile=False
            )
            
            # Filter files based on user selection
            selected_files = []
            for file_path in output_files:
                file_ext = file_path.suffix.lower()
                if ((file_ext == '.json' and output_json) or 
                    (file_ext == '.html' and output_html) or 
                    (file_ext == '.docx' and output_docx)):
                    selected_files.append(file_path)
            
            if not selected_files:
                flash('No files generated with selected formats', 'error')
                return redirect(url_for('generator'))
            
            # If single file, send directly
            if len(selected_files) == 1:
                file_path = selected_files[0]
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=file_path.name
                )
            
            # If multiple files, create ZIP
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            zip_filename = f"DSCG_{role_id}_EQF{eqf_level}_{ects}ECTS_{timestamp}.zip"
            zip_path = temp_path / zip_filename
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in selected_files:
                    zipf.write(file_path, file_path.name)
            
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=zip_filename
            )
    
    except Exception as e:
        flash(f'Generation error: {str(e)}', 'error')
        return redirect(url_for('generator'))

@app.route('/generate_educational_profile_with_docx', methods=['POST'])
def generate_educational_profile_with_docx():
    """Generate educational profile with DOCX support"""
    try:
        # Get form data
        role_id = request.form.get('role')
        eqf_level = int(request.form.get('eqf_level'))
        topic = request.form.get('topic', 'Digital Sustainability')
        theme = request.form.get('theme', 'material_gray')
        
        # Format options
        output_json = request.form.get('output_json') == 'on'
        output_html = request.form.get('output_html') == 'on'
        output_docx = request.form.get('output_docx') == 'on'
        
        if not any([output_json, output_html, output_docx]):
            flash('Please select at least one output format', 'warning')
            return redirect(url_for('eps'))
        
        # Initialize enhanced output manager
        output_manager = OutputManager(project_root)
        
        # Check DOCX availability
        if output_docx and not output_manager.docx_available:
            flash('DOCX generation not available. Install python-docx: pip install python-docx', 'warning')
            output_docx = False
        
        # Generate Educational Profile
        from scripts.curriculum_generator.domain.educational_profiles import EnhancedEducationalProfilesManager
        
        ep_manager = EnhancedEducationalProfilesManager(project_root)
        ep_data = ep_manager.generate_comprehensive_profile(role_id, eqf_level)
        
        if not ep_data:
            flash('Failed to generate educational profile', 'error')
            return redirect(url_for('eps'))
        
        # Create temporary directory for outputs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Generate outputs
            generated_files = output_manager.save_educational_profile_standalone(
                educational_profile=ep_data,
                topic=topic,
                eqf_level=eqf_level,
                output_docx=output_docx,
                theme_name=theme
            )
            
            # Convert string paths to Path objects and filter by selection
            selected_files = []
            for file_str in generated_files:
                file_path = Path(file_str)
                file_ext = file_path.suffix.lower()
                if ((file_ext == '.json' and output_json) or 
                    (file_ext == '.html' and output_html) or 
                    (file_ext == '.docx' and output_docx)):
                    selected_files.append(file_path)
            
            if not selected_files:
                flash('No files generated with selected formats', 'error')
                return redirect(url_for('eps'))
            
            # If single file, send directly
            if len(selected_files) == 1:
                file_path = selected_files[0]
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=file_path.name
                )
            
            # If multiple files, create ZIP
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            zip_filename = f"EP_{role_id}_EQF{eqf_level}_{timestamp}.zip"
            zip_path = temp_path / zip_filename
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in selected_files:
                    zipf.write(file_path, file_path.name)
            
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=zip_filename
            )
    
    except Exception as e:
        flash(f'Generation error: {str(e)}', 'error')
        return redirect(url_for('eps'))

@app.route('/check_docx_availability')
def check_docx_availability():
    """API endpoint to check if DOCX generation is available"""
    try:
        output_manager = OutputManager(project_root)
        return jsonify({
            'docx_available': output_manager.docx_available,
            'message': 'DOCX generation ready' if output_manager.docx_available else 'Install python-docx to enable DOCX generation'
        })
    except Exception as e:
        return jsonify({
            'docx_available': False,
            'message': f'Error checking DOCX availability: {str(e)}'
        })

# Add to existing template rendering - modify generator.html template
@app.route('/generator')
def generator():
    """Enhanced generator page with DOCX options"""
    # Check DOCX availability
    output_manager = OutputManager(project_root)
    docx_available = output_manager.docx_available
    
    # Get existing data (roles, themes, etc.)
    from scripts.curriculum_generator.domain.role_manager import RoleManager
    role_manager = RoleManager(project_root)
    roles = role_manager.get_all_roles()
    
    return render_template('generator.html', 
                         roles=roles,
                         docx_available=docx_available)

# JavaScript for frontend (add to templates)
"""
<!-- Add to generator.html template -->
<script>
// Check DOCX availability on page load
document.addEventListener('DOMContentLoaded', function() {
    fetch('/check_docx_availability')
        .then(response => response.json())
        .then(data => {
            const docxCheckbox = document.getElementById('output_docx');
            const docxLabel = document.querySelector('label[for="output_docx"]');
            
            if (!data.docx_available) {
                docxCheckbox.disabled = true;
                docxLabel.innerHTML += ' <small class="text-muted">(Install python-docx)</small>';
                docxLabel.title = data.message;
            }
        })
        .catch(error => {
            console.error('Error checking DOCX availability:', error);
        });
});

// Form validation
function validateGenerationForm() {
    const formats = ['output_json', 'output_html', 'output_docx'];
    const checked = formats.some(id => document.getElementById(id).checked);
    
    if (!checked) {
        alert('Please select at least one output format');
        return false;
    }
    return true;
}
</script>

<!-- Add to form in generator.html -->
<div class="form-group">
    <label>Output Formats:</label>
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
"""