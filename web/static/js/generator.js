// DSCG Web Interface Generator - Enhanced with UOL Support
class DSCGGenerator {
    constructor() {
        this.baseURL = '/api';
        this.currentJob = null;
        this.init();
    }

    init() {
        this.loadRoles();
        this.setupEventHandlers();
        this.setupFormValidation();
    }

    async loadRoles() {
        try {
            const response = await fetch(`${this.baseURL}/roles`);
            const data = await response.json();
            
            if (data.roles) {
                this.populateRolesDropdown(data.roles);
                console.log(`✅ Loaded ${data.roles.length} roles`);
            }
        } catch (error) {
            console.error('Error loading roles:', error);
            this.showError('Failed to load roles');
        }
    }

    populateRolesDropdown(roles) {
        const roleSelect = document.getElementById('role-select');
        if (!roleSelect) return;

        // Clear existing options
        roleSelect.innerHTML = '<option value="">Select a role...</option>';

        // Group roles by main area
        const rolesByArea = {};
        roles.forEach(role => {
            const area = role.main_area || 'Other';
            if (!rolesByArea[area]) {
                rolesByArea[area] = [];
            }
            rolesByArea[area].push(role);
        });

        // Add grouped options
        Object.keys(rolesByArea).sort().forEach(area => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = area;
            
            rolesByArea[area].forEach(role => {
                const option = document.createElement('option');
                option.value = role.id;
                option.textContent = `${role.id} - ${role.name}`;
                option.dataset.eqfLevels = JSON.stringify(role.eqf_levels);
                option.dataset.defaultEcts = JSON.stringify(role.default_ects);
                optgroup.appendChild(option);
            });
            
            roleSelect.appendChild(optgroup);
        });
    }

    setupEventHandlers() {
        // Role selection handler
        const roleSelect = document.getElementById('role-select');
        if (roleSelect) {
            roleSelect.addEventListener('change', (e) => {
                this.onRoleChange(e.target);
            });
        }

        // EQF level change handler
        const eqfSelect = document.getElementById('eqf-select');
        if (eqfSelect) {
            eqfSelect.addEventListener('change', (e) => {
                this.onEQFChange(e.target);
            });
        }

        // ECTS input handler
        const ectsInput = document.getElementById('ects-input');
        if (ectsInput) {
            ectsInput.addEventListener('input', (e) => {
                this.onECTSChange(e.target);
            });
        }

        // UOL input handler - NEW
        const uolInput = document.getElementById('uol-input');
        if (uolInput) {
            uolInput.addEventListener('input', (e) => {
                this.onUOLChange(e.target);
            });
        }

        // Generate button
        const generateBtn = document.getElementById('generate-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateCurriculum();
            });
        }

        // Download buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('download-btn')) {
                this.downloadFile(e.target.dataset.file);
            }
            if (e.target.classList.contains('download-bundle-btn')) {
                this.downloadBundle(e.target.dataset.jobId);
            }
        });
    }

    onRoleChange(roleSelect) {
        const selectedOption = roleSelect.selectedOptions[0];
        if (!selectedOption || !selectedOption.value) return;

        const eqfLevels = JSON.parse(selectedOption.dataset.eqfLevels || '[]');
        const defaultEcts = JSON.parse(selectedOption.dataset.defaultEcts || '{}');

        // Update EQF levels dropdown
        this.updateEQFLevels(eqfLevels);
        
        // Update ECTS suggestion
        const eqfSelect = document.getElementById('eqf-select');
        if (eqfSelect && eqfSelect.value) {
            this.updateECTSSuggestion(defaultEcts, eqfSelect.value);
        }

        this.validateForm();
    }

    onEQFChange(eqfSelect) {
        const roleSelect = document.getElementById('role-select');
        const selectedRole = roleSelect.selectedOptions[0];
        
        if (selectedRole && selectedRole.dataset.defaultEcts) {
            const defaultEcts = JSON.parse(selectedRole.dataset.defaultEcts);
            this.updateECTSSuggestion(defaultEcts, eqfSelect.value);
        }

        this.validateForm();
    }

    onECTSChange(ectsInput) {
        this.updateUOLSuggestion();
        this.validateForm();
    }

    onUOLChange(uolInput) {
        this.validateUOLConstraints();
        this.validateForm();
    }

    updateEQFLevels(levels) {
        const eqfSelect = document.getElementById('eqf-select');
        if (!eqfSelect) return;

        eqfSelect.innerHTML = '<option value="">Select EQF level...</option>';
        
        levels.forEach(level => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = `EQF Level ${level}`;
            eqfSelect.appendChild(option);
        });
    }

    updateECTSSuggestion(defaultEcts, eqfLevel) {
        const ectsInput = document.getElementById('ects-input');
        const suggestionEl = document.getElementById('ects-suggestion');
        
        if (!ectsInput || !suggestionEl) return;

        const suggested = defaultEcts[eqfLevel] || defaultEcts[eqfLevel.toString()] || 60;
        suggestionEl.textContent = `Suggested: ${suggested} ECTS`;
        
        if (!ectsInput.value) {
            ectsInput.value = suggested;
            this.updateUOLSuggestion();
        }
    }

    updateUOLSuggestion() {
        const ectsInput = document.getElementById('ects-input');
        const uolInput = document.getElementById('uol-input');
        const uolSuggestion = document.getElementById('uol-suggestion');
        
        if (!ectsInput || !uolInput || !uolSuggestion) return;

        const ects = parseFloat(ectsInput.value) || 0;
        
        if (ects > 0) {
            let suggestedUOL;
            if (ects <= 5) {
                suggestedUOL = 2;
            } else if (ects <= 15) {
                suggestedUOL = 4;
            } else if (ects <= 30) {
                suggestedUOL = 6;
            } else {
                suggestedUOL = 8;
            }
            
            uolSuggestion.textContent = `Suggested: ${suggestedUOL} units (${(ects/suggestedUOL).toFixed(1)} ECTS each)`;
            
            if (!uolInput.value) {
                uolInput.value = suggestedUOL;
            }
        } else {
            uolSuggestion.textContent = '';
        }
    }

    validateUOLConstraints() {
        const ectsInput = document.getElementById('ects-input');
        const uolInput = document.getElementById('uol-input');
        const uolError = document.getElementById('uol-error');
        
        if (!ectsInput || !uolInput || !uolError) return true;

        const ects = parseFloat(ectsInput.value) || 0;
        const uol = parseInt(uolInput.value) || 0;

        uolError.textContent = '';

        if (uol < 2 || uol > 10) {
            uolError.textContent = 'Units of Learning must be between 2-10';
            return false;
        }

        if (ects > 0 && uol > 0) {
            const ectsPerUnit = ects / uol;
            if (ectsPerUnit < 0.1) {
                uolError.textContent = `ECTS per unit too small (${ectsPerUnit.toFixed(2)}). Minimum 0.1 ECTS per unit required.`;
                return false;
            }
        }

        return true;
    }

    setupFormValidation() {
        // Real-time validation
        const form = document.getElementById('curriculum-form');
        if (form) {
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                input.addEventListener('change', () => this.validateForm());
                input.addEventListener('input', () => this.validateForm());
            });
        }
    }

    validateForm() {
        const roleSelect = document.getElementById('role-select');
        const eqfSelect = document.getElementById('eqf-select');
        const ectsInput = document.getElementById('ects-input');
        const uolInput = document.getElementById('uol-input');
        const generateBtn = document.getElementById('generate-btn');

        if (!roleSelect || !eqfSelect || !ectsInput || !uolInput || !generateBtn) return;

        const isValid = roleSelect.value && 
                       eqfSelect.value && 
                       ectsInput.value && 
                       uolInput.value &&
                       this.validateUOLConstraints();

        generateBtn.disabled = !isValid;
        
        if (isValid) {
            generateBtn.classList.remove('btn-secondary');
            generateBtn.classList.add('btn-primary');
        } else {
            generateBtn.classList.remove('btn-primary');
            generateBtn.classList.add('btn-secondary');
        }
    }

    async generateCurriculum() {
        const form = document.getElementById('curriculum-form');
        if (!form) return;

        const formData = new FormData(form);
        const data = {
            role: formData.get('role'),
            eqf_level: parseInt(formData.get('eqf_level')),
            ects: parseFloat(formData.get('ects')),
            uol: parseInt(formData.get('uol')), // NEW: UOL support
            topic: formData.get('topic') || '',
            theme: formData.get('theme') || 'material_gray',
            formats: Array.from(formData.getAll('formats'))
        };

        // Show progress
        this.showProgress(true);
        this.updateProgress(0, 'Starting curriculum generation...');

        try {
            const response = await fetch(`${this.baseURL}/generate/curriculum`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.currentJob = result.job_id;
                this.pollJobStatus(result.job_id);
            } else {
                throw new Error(result.error || 'Generation failed');
            }

        } catch (error) {
            console.error('Generation error:', error);
            this.showError(`Generation failed: ${error.message}`);
            this.showProgress(false);
        }
    }

    async pollJobStatus(jobId) {
        try {
            const response = await fetch(`${this.baseURL}/jobs/${jobId}`);
            const job = await response.json();

            this.updateProgress(job.progress, job.message);

            if (job.status === 'completed') {
                this.showProgress(false);
                this.showResults(job);
            } else if (job.status === 'failed') {
                this.showProgress(false);
                this.showError(`Generation failed: ${job.message}`);
            } else {
                // Continue polling
                setTimeout(() => this.pollJobStatus(jobId), 1000);
            }

        } catch (error) {
            console.error('Polling error:', error);
            this.showProgress(false);
            this.showError('Failed to check generation status');
        }
    }

    showProgress(show) {
        const progressSection = document.getElementById('progress-section');
        if (progressSection) {
            progressSection.style.display = show ? 'block' : 'none';
        }
    }

    updateProgress(percent, message) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');

        if (progressBar) {
            progressBar.style.width = `${percent}%`;
            progressBar.setAttribute('aria-valuenow', percent);
        }

        if (progressText) {
            progressText.textContent = message;
        }
    }

    showResults(job) {
        const resultsSection = document.getElementById('results-section');
        const resultsContent = document.getElementById('results-content');

        if (!resultsSection || !resultsContent) return;

        const preview = job.curriculum_preview || {};
        const files = job.output_files || [];

        let html = `
            <div class="alert alert-success">
                <h5>✅ Curriculum Generation Completed</h5>
                <p>Generated ${preview.total_units || 0} learning units with ${preview.total_ects || 0} ECTS using ${job.backend || 'UOL_v2'} backend</p>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📊 Generation Summary</div>
                        <div class="card-body">
                            <p><strong>Role:</strong> ${job.role}</p>
                            <p><strong>Topic:</strong> ${preview.topic_used || 'Generic'}</p>
                            <p><strong>EQF Level:</strong> ${job.eqf_level}</p>
                            <p><strong>Total ECTS:</strong> ${preview.total_ects || 0}</p>
                            <p><strong>Units of Learning:</strong> ${job.uol}</p>
                            <p><strong>Theme:</strong> ${job.theme}</p>
                            <p><strong>Backend:</strong> ${job.backend || 'UOL_v2'}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📁 Generated Files</div>
                        <div class="card-body">
        `;

        if (files.length > 0) {
            files.forEach(file => {
                const filename = file.split('/').pop();
                const isHTML = filename.endsWith('.html');
                const isJSON = filename.endsWith('.json');
                
                html += `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span>${isHTML ? '🌐' : '📄'} ${filename}</span>
                        <button class="btn btn-sm btn-outline-primary download-btn" data-file="${filename}">
                            Download
                        </button>
                    </div>
                `;
            });

            html += `
                    <hr>
                    <button class="btn btn-primary download-bundle-btn" data-job-id="${job.job_id || this.currentJob}">
                        📦 Download All as ZIP
                    </button>
            `;
        } else {
            html += '<p class="text-muted">No files generated</p>';
        }

        html += `
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContent.innerHTML = html;
        resultsSection.style.display = 'block';
    }

    async downloadFile(filename) {
        try {
            const response = await fetch(`${this.baseURL}/download/${filename}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                throw new Error('Download failed');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showError(`Download failed: ${error.message}`);
        }
    }

    async downloadBundle(jobId) {
        try {
            const response = await fetch(`${this.baseURL}/download/bundle/${jobId}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `curriculum_bundle_${jobId}.zip`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                throw new Error('Bundle download failed');
            }
        } catch (error) {
            console.error('Bundle download error:', error);
            this.showError(`Bundle download failed: ${error.message}`);
        }
    }

    showError(message) {
        const errorSection = document.getElementById('error-section');
        const errorMessage = document.getElementById('error-message');

        if (errorSection && errorMessage) {
            errorMessage.textContent = message;
            errorSection.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorSection.style.display = 'none';
            }, 5000);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new DSCGGenerator();
});
