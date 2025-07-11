
# Curriculum Creator (CG)

**A Framework for Multi-Objective Curriculum Optimization with Learning Unit-Level Analysis**


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Framework Validation](https://img.shields.io/badge/frameworks-7\%20validated-green.svg)](#framework-validation)

---

## Overview

The Curriculum Generator (GC) generates modular curricula and educational profiles that balance competence coverage, regulatory compliance, and resource efficiency across multiple educational frameworks. GC formalizes curriculum design as a multi-objective optimization problem, producing competence-aligned curricula that comply with international standards such as CS2023, EQF, and ESCO.

### Key Features

- **🎯 Multi-Objective Optimization**: Systematic balancing of competence coverage, resource efficiency, and compliance
- **📚 Enhanced Curriculum Generation**: 10 core professional curricula with educational standards compliance
- **🏛️ Standards Compliance**: Full validation against 7 major international frameworks + EQF level compliance
- **🔧 Modular Architecture**: 90-learning unit repository enabling flexible curriculum composition
- **🌐 Web Interface**: Production-ready Flask application for interactive curriculum design
- **📊 Comprehensive Analysis Suite**: Unified engine for repository, framework, learning unit, and cross-framework analysis
- **🎯 Multi-Level Insights**: Individual learning unit performance analysis with enhancement recommendations
- **⚡ Streamlined Codebase**: Clean directory structure with organized scripts and data
- **⚙️ Configuration-Driven**: Comprehensive settings.json for all analysis parameters and thresholds
- **🎨 Visual Mapping**: Optional visual curriculum mapping for enhanced understanding and pathway guidance
- **🇬🇧 British Standards**: Compliant with British educational terminology and spelling
- **📋 Framework Alignment**: Direct mapping to GreenComp and e-CF frameworks with detailed traceability

### Academic Impact

GC provides quantitative evidence for automated curriculum generation effectiveness:
- **Framework Alignment**: ESCO (74.4\%), CS2023 (58.9\%), e-CF (46.7%)
- **High Optimization Quality**: 0.66 objective function score
- **Resource Efficiency**: 44.7\% learning unit sharing coefficient
- **Comprehensive Coverage**: 90 learning units across 10 professional roles
- **Educational Standards**: Full EQF compliance with level-appropriate language and competence descriptors

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dietmarja/GC.git
cd GC

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas; import numpy; import sklearn; print('GC dependencies installed')"
```

### Essential Commands

#### Enhanced Curriculum Generation (Recommended)
```bash
# Navigate to Analysis scripts directory
cd analysis/scripts

# Generate enhanced curricula with visual mapping (default)
python generate_curricula_toggle.py

# Generate enhanced curricula without visual mapping (faster)
python generate_curricula_toggle.py --no-visual-map
```
*The enhanced curriculum generator (`generate_curricula_toggle.py`) addresses educational standards critique, ensures British spelling compliance, removes outdated framework references, and implements proper EQF-level language. Visual mapping provides additional curriculum visualization and pathway guidance for stakable credentials.*

**Enhanced Curriculum Generator Features:**
- ✅ **Educational Standards Compliance**: Proper EQF level language and competence descriptors
- ✅ **British Terminology**: Uses "competence/competences" instead of "competency/competencies"
- ✅ **Framework Alignment**: Direct mapping to GreenComp and e-CF with detailed traceability
- ✅ **Learning Unit Structure**: Replaces "module" terminology with "learning unit" throughout
- ✅ **Pathway Guidance**: Clear positioning within stackable credential systems
- ✅ **No Fallbacks**: Exclusively reads from modules_v5.json for data integrity
- ✅ **Multiple Formats**: Generates JSON, HTML, and DOCX outputs for each curriculum

#### Comprehensive Analysis (Traditional)
```bash
# Run complete GC analysis suite (uses config/settings.json)
python ecm_comprehensive_analysis.py
```
*This single script performs repository-level, framework-level, learning unit-level, and cross-framework analysis with full visualization and export capabilities. All parameters are configured via `config/settings.json`.*

#### Configuration Management
```bash
# Test path resolution first (recommended)
cd analysis/scripts
python test_paths.py  # Verify all paths are correctly resolved

# Edit analysis parameters
nano ../../config/settings.json

# Test configuration loading
python -c "from ecm_comprehensive_analysis import GCAnalysisEngine; engine = GCAnalysisEngine(); print('✅ Config loaded')"
```

#### Educational Profiles Generation
```bash
# Generate educational profiles (uses config/settings.json)
python generate_educational_profiles.py
```
*Generates educational_profiles.json and educational_profiles_short.json with comprehensive professional development pathways.*

#### Legacy Curriculum Generation
```bash
# Generate basic curricula (legacy method)
cd generators
python generate_curricula.py

# Generate educational profiles (legacy method)
python generate_educational_profiles.py
```
*Legacy generators use settings.json for input/output paths and formats. Curricula are generated in JSON and HTML formats by default.*

#### Web Interface
```bash
# Start interactive web application
cd web
python app.py
# Access at http://localhost:5001
```

---

## Enhanced Curriculum Generation Details

### Generated Curricula Structure

The enhanced curriculum generator produces **10 professional curricula** with the following specifications:

| No. | Title | Role | EQF Level | ECTS | Filename |
|-----|-------|------|-----------|------|----------|
| 01 | Basic Sustainability Skills | Data Analyst (DAN) | 5 | 0.5 | 01_DAN_5_05 |
| 02 | Digital Sustainability Fundamentals | Manager (DSM) | 6 | 1.0 | 02_DSM_6_10 |
| 03 | Sustainable IT Operations | Engineer (DSE) | 5 | 2.0 | 03_DSE_5_20 |
| 04 | Digital Sustainability Leadership | Leader (DSL) | 6 | 5.0 | 04_DSL_6_50 |
| 05 | Digital Sustainability Consultancy | Consultant (DSC) | 6 | 10.0 | 05_DSC_6_100 |
| 06 | Sustainability Data Analysis | Data Analyst (DAN) | 5 | 7.5 | 06_DAN_5_75 |
| 07 | Advanced Leadership Programme | Leader (DSL) | 7 | 30.0 | 07_DSL_7_30 |
| 08 | Professional Consultancy Certificate | Consultant (DSC) | 6 | 45.0 | 08_DSC_6_45 |
| 09 | Master's Level Leadership | Leader (DSL) | 7 | 120.0 | 09_DSL_7_120 |
| 10 | Advanced Consultancy Degree | Consultant (DSC) | 7 | 180.0 | 10_DSC_7_180 |

### Professional Roles Defined

- **DAN**: Sustainability Data Analyst - ESG reporting and compliance specialist
- **DSM**: Digital Sustainability Manager - Implementation and cross-functional coordination
- **DSE**: Digital Sustainability Engineer - Sustainable IT infrastructure and operations
- **DSL**: Digital Sustainability Leader - Strategic transformation and organizational change
- **DSC**: Digital Sustainability Consultant - Advisory services and solution design

### Curriculum Features

**Educational Standards Compliance:**
- EQF Level appropriate language (e.g., EQF 5: "Contribute to" not "Lead")
- Authentic role differentiation with professional context
- Direct framework mapping (GreenComp and e-CF with specific descriptors)
- British educational terminology throughout

**Output Formats:**
- **JSON**: Structured data with complete learning unit information
- **HTML**: Professional web-ready format with enhanced styling
- **DOCX**: Print-ready documents with proper formatting

**Learning Unit Structure:**
- Authentic learning outcomes using Tuning methodology
- Framework alignment with traceability
- Workload distribution (contact, self-study, workplace hours)
- Assessment strategies tailored to each curriculum
- Pathway guidance for stackable credentials

---

## Analysis Capabilities

### Framework Validation

GC validates learning units against 7 international frameworks:

| Framework | Domain | Authority | Alignment Score |
|-----------|---------|-----------|----------------|
| **ESCO** | Professional Skills | European Commission | **74.4%** |
| **CS2023** | Computing Curriculum | IEEE/ACM | **58.9%** |
| **e-CF** | ICT Competencies | CEN | **46.7%** |
| **DigComp 2.2** | Digital Literacy | European Commission | **40.0%** |
| **EQF Level 7** | Academic Qualification | European Union | **15.6%** |
| **O*NET** | Occupational Standards | US Department of Labor | **14.4%** |
| **PMBOK** | Project Management | PMI | **13.3%** |

### Learning Unit-Level Analysis Features

- **Quality Scoring**: Weighted formula combining similarity metrics and alignment rates
- **Versatility Classification**: 4-tier system from Highly Versatile to Specialized  
- **Framework Suitability**: Excellent/Good/Moderate/Poor classification per framework
- **Cross-Framework Insights**: Performance consistency and excellence counts
- **Enhancement Recommendations**: Data-driven improvement guidance
- **Comprehensive Visualizations**: Executive dashboard with 4-panel analysis

*See Detailed Analysis Documentation below for complete technical specifications, formulas, and thresholds.*

---

## Detailed Analysis Documentation

### Analysis Methods

#### 1. **Semantic Similarity Calculation**
```
Method: TF-IDF Vectorization + Cosine Similarity
Threshold: 0.1 (competencies below this are considered non-aligned)
Limitation: May underperform on short, domain-specific texts
```

#### 2. **Learning Unit-Level Metrics**
For each learning unit against each framework:

- **max_similarity**: Highest similarity score with any framework competency
- **mean_similarity**: Average similarity across ALL framework competencies  
- **alignment_rate**: Percentage of framework competencies above 0.1 threshold
- **quality_score**: Weighted formula: `0.4 × max_similarity + 0.3 × mean_similarity + 0.3 × alignment_rate`
- **alignments_count**: Number of framework competencies above threshold

#### 3. **Classification Systems**

**Learning Unit Suitability** (per framework):
- **Excellent**: quality_score ≥ 0.6 AND alignment_rate ≥ 0.3
- **Good**: quality_score ≥ 0.4 AND alignment_rate ≥ 0.2  
- **Moderate**: quality_score ≥ 0.25 AND alignment_rate ≥ 0.1
- **Poor**: Below moderate thresholds

**Learning Unit Versatility** (cross-framework):
- **Highly Versatile**: Excellent in 3+ frameworks
- **Versatile**: Good+ in 4+ frameworks
- **Moderately Versatile**: Good+ in 2+ frameworks  
- **Specialized**: Good+ in <2 frameworks

#### 4. **Cross-Framework Analysis**
- **versatility_score**: Average quality_score across all 7 frameworks
- **consistency_score**: Performance stability = `1 - standard_deviation(quality_scores)`
- **excellent_frameworks**: Count of frameworks where learning unit scores "Excellent"
- **good_frameworks**: Count of frameworks where learning unit scores "Good" or "Excellent"

### Complete Output Files Reference

#### CSV Files (9 files)

**learning_unit_quality_matrix.csv** *(630 rows: 90 learning units × 7 frameworks)*
```
Columns:
- learning_unit_id: Learning unit identifier (e.g., "LU001")
- learning_unit_name: Full learning unit name
- framework: Framework ID (ESCO, CS2023, etc.)
- framework_name: Full framework name
- quality_score: Calculated quality score (0-1)
- max_similarity: Highest similarity with framework
- alignment_rate: % of framework competencies aligned
- suitability: Excellence classification
- thematic_area: Learning unit subject area
- eqf_level: European Qualifications Framework level
```

**learning_unit_versatility.csv** *(90 rows: one per learning unit)*
```
Columns:
- learning_unit_id: Learning unit identifier
- learning_unit_name: Full learning unit name  
- thematic_area: Subject area
- versatility_score: Average quality across frameworks
- consistency_score: Performance stability
- excellent_frameworks: Count of excellent performances
- good_frameworks: Count of good+ performances
- versatility_class: Classification category
```

**Framework Rankings** *(7 files: one per framework)*
- `ESCO_rankings.csv`, `CS2023_rankings.csv`, `DigComp_rankings.csv`, `EQF_rankings.csv`, `e_CF_rankings.csv`, `ONET_rankings.csv`, `PMBOK_rankings.csv`
- *90 rows each (learning units ranked by framework performance)*
```
Columns:
- rank: Position in framework (1 = best)
- learning_unit_id: Learning unit identifier
- learning_unit_name: Full learning unit name
- quality_score: Framework-specific quality score
- suitability: Excellence classification
```

#### JSON Files (1 file)

**analysis_summary.json** *(Complete analysis metadata)*
```
Contents:
- analysis_date: Timestamp of analysis
- total_learning_units: Count of learning units analyzed (90)
- total_frameworks: Count of frameworks (7)
- versatility_statistics: Cross-framework summary stats
  - total_learning_units, highly_versatile, versatile, etc.
  - avg_versatility, most_versatile_learning_unit
- framework_statistics: Per-framework performance stats
  - avg_quality, excellent/good/moderate/poor counts
  - best_learning_unit, worst_learning_unit per framework
```

#### Visualization Files (1 file)

**ecm_learning_unit_analysis.png** *(4-panel executive dashboard, 16×12 inches, 300 DPI)*

- **Panel 1**: Average Learning Unit Quality by Framework (bar chart with values)
- **Panel 2**: Learning Unit Versatility Distribution (histogram with mean line)
- **Panel 3**: Versatility Classification (pie chart with percentages)
- **Panel 4**: Learning Unit Suitability by Framework (stacked bar chart)

### Usage Examples

#### Academic Research
```python
# Load quality matrix for statistical analysis
quality_df = pd.read_csv('results/learning_unit_quality_matrix.csv')

# Calculate framework alignment correlations
framework_pivot = quality_df.pivot(index='learning_unit_id', columns='framework', values='quality_score')
correlation_matrix = framework_pivot.corr()
```

#### Curriculum Design
```python
# Find best learning units for ESCO-compliant curriculum
esco_rankings = pd.read_csv('results/ESCO_rankings.csv')
top_learning_units = esco_rankings[esco_rankings['suitability'].isin(['Excellent', 'Good'])].head(20)

# Find versatile learning units for multi-framework compliance
versatility_df = pd.read_csv('results/learning_unit_versatility.csv')
core_learning_units = versatility_df[versatility_df['versatility_class'] == 'Highly Versatile']
```

#### Quality Assessment
```python
# Identify learning units needing improvement
low_performers = versatility_df[versatility_df['versatility_score'] < 0.3]

# Find framework-specific gaps
for framework in ['ESCO', 'CS2023', 'DigComp']:
    rankings = pd.read_csv(f'results/{framework}_rankings.csv')
    poor_learning_units = rankings[rankings['suitability'] == 'Poor']
    print(f"{framework}: {len(poor_learning_units)} learning units need enhancement")
```

### Performance Specifications

**File Sizes**:
- learning_unit_quality_matrix.csv: ~45KB
- learning_unit_versatility.csv: ~8KB  
- Framework rankings: ~6KB each (7 files)
- analysis_summary.json: ~12KB
- ecm_learning_unit_analysis.png: ~850KB
- **Total Output**: ~950KB per analysis run

**Runtime Performance**:
- TF-IDF Analysis: 5-6 minutes for complete 90×7 matrix
- SBERT Analysis: ~2-3 minutes estimated (when implemented)
- Enhanced Curriculum Generation: ~2-3 minutes for 10 curricula
- Memory Usage: <512MB peak
- Recommended: 4GB+ RAM systems

---

## Generated Outputs

### Enhanced Curriculum Outputs *(Generated via generate_curricula_toggle.py)*
```
output/curricula/                            # Default location (configurable)
├── 01_DAN_5_05.json                        # Basic Sustainability Skills
├── 01_DAN_5_05.html                        # Professional web format
├── 01_DAN_5_05.docx                        # Print-ready document
├── 02_DSM_6_10.json                        # Digital Sustainability Fundamentals
├── 02_DSM_6_10.html
├── 02_DSM_6_10.docx
├── ... (continues for all 10 curricula)
├── 09_DSL_7_120.json                       # Master's Level Leadership
├── 09_DSL_7_120.html
├── 09_DSL_7_120.docx
├── 10_DSC_7_180.json                       # Advanced Consultancy Degree
├── 10_DSC_7_180.html
└── 10_DSC_7_180.docx
```
**Total**: 30 files (3 formats × 10 curricula) with enhanced educational standards compliance

### Analysis Results *(see Detailed Analysis Documentation above for complete specifications)*
```
analysis/results/
├── learning_unit_quality_matrix.csv         # 630 rows: 90×7 learning unit-framework performance matrix
├── learning_unit_versatility.csv            # 90 rows: cross-framework versatility analysis  
├── ESCO_rankings.csv                        # 90 rows: learning units ranked by ESCO performance
├── CS2023_rankings.csv                      # 90 rows: learning units ranked by CS2023 performance
├── DigComp_rankings.csv                     # 90 rows: learning units ranked by DigComp performance
├── EQF_rankings.csv                         # 90 rows: learning units ranked by EQF performance
├── e_CF_rankings.csv                        # 90 rows: learning units ranked by e-CF performance
├── ONET_rankings.csv                        # 90 rows: learning units ranked by O*NET performance
├── PMBOK_rankings.csv                       # 90 rows: learning units ranked by PMBOK performance
├── analysis_summary.json                    # Complete metadata and statistics
└── ecm_learning_unit_analysis.png           # 4-panel executive dashboard (850KB)
```
**Total**: 11 files (~950KB) generated per analysis run

### Educational Profiles (Generated via generate_educational_profiles.py)

**Sample Generated Profiles:**
- **Digital Sustainability Professional** (comprehensive programme)
- **Data Analytics for Sustainability** (specialised programme)  
- **Sustainable Technology Leadership** (executive programme)

**Output Locations (configurable in settings.json):**
```
output/profiles/                             # Default location
├── educational_profiles.json                # Comprehensive profiles
├── educational_profiles_short.json          # Condensed profiles
├── digital_sustainability_professional.json
├── digital_sustainability_professional.html
├── data_analytics_for_sustainability.json
├── data_analytics_for_sustainability.html
├── sustainable_technology_leadership.json
└── sustainable_technology_leadership.html
```

**Features:**
- Multiple learning pathways per profile
- EQF level alignment (6-8)
- Industry sector mapping
- Career progression frameworks
- Implementation guidance
- Flexible delivery modes

---

## Development Roadmap

### ✅ Current Features (v1.2)
- [x] Enhanced curriculum generation with educational standards compliance
- [x] Learning unit-level framework analysis
- [x] 90-learning unit repository validation
- [x] 7 international framework support
- [x] Comprehensive visualization suite
- [x] CSV export capabilities
- [x] Versatility classification system
- [x] British educational terminology compliance
- [x] Direct framework mapping (GreenComp, e-CF)
- [x] Visual mapping toggle functionality

### 🚧 To-Do List

#### **🎯 High Priority: SBERT-Based Similarity Enhancement**

**Current Limitation**: TF-IDF + cosine similarity has limitations with short, domain-specific texts, leading to low similarity scores that may not reflect true semantic relationships.

**Proposed Solution**: Replace with SBERT (Sentence-BERT) for improved semantic understanding.

**Specification**:
- **Model**: `paraphrase-MiniLM-L6-v2` (384-dimensional embeddings)
- **Library**: `sentence-transformers` via HuggingFace
- **Method**: 
  ```python
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
  embeddings = model.encode(competency_texts)
  similarity_matrix = cosine_similarity(embeddings)
  ```

**Benefits**:
- Captures semantic similarity even with different phrasing
- More robust for short, abstract competency descriptions
- Better cross-domain alignment detection
- Improved learning unit-level comparison accuracy

**Current Blockers**:
- Hardware compatibility: `sentence-transformers >= 2.3` requires PyTorch ≥ 2.1
- Non-AVX macOS systems cannot run recent PyTorch versions
- Legacy system compatibility issues

**Implementation Options**:
1. **Clean Environment**: Create conda env with `torch==1.13.1` + `sentence-transformers==2.2.2`
2. **ONNX Migration**: Use ONNX-based SBERT (no PyTorch dependency)
3. **Cloud Execution**: Run analysis on Colab/M1 Mac/Linux systems
4. **Alternative Models**: Explore lighter semantic models (e.g., Universal Sentence Encoder)

**Expected Outcomes**:
- Improved alignment scores reflecting true semantic relationships
- Better learning unit versatility classification accuracy
- More reliable framework compatibility assessment
- Enhanced curriculum design recommendations

#### **📊 Medium Priority Enhancements**
- [ ] Interactive web dashboard improvements
- [ ] Real-time curriculum optimization
- [ ] Multi-language framework support
- [ ] Export to LMS formats (SCORM, xAPI)
- [ ] Integration with institutional systems
- [ ] Enhanced visual mapping capabilities
- [ ] Stackable credentials tracking system

#### **🔬 Research Extensions**
- [ ] Longitudinal curriculum effectiveness tracking
- [ ] Student outcome correlation analysis
- [ ] Industry feedback integration
- [ ] AI-powered curriculum personalization
- [ ] Cross-border certification validation

### **⚠️ Known Issues**
- Low TF-IDF similarity scores may indicate method limitations rather than poor alignment
- Framework terminology differences affect automatic matching
- Learning unit descriptions may need standardization for optimal analysis

---

## Usage Examples

### Enhanced Curriculum Generation
```python
# From analysis/scripts/ directory
from generate_curricula_toggle import EnhancedD4SCurriculumGenerator

# Initialize with visual mapping (default)
generator = EnhancedD4SCurriculumGenerator(visual_mapping=True)

# Generate all 10 curricula with educational standards compliance
files = generator.generate_all_curricula()

# Output includes JSON, HTML, and DOCX for each curriculum
print(f"Generated {len(files)} files (30 total: 3 formats × 10 curricula)")
print(f"Output location: {generator.output_dir}")

# Without visual mapping (faster generation)
generator_fast = EnhancedD4SCurriculumGenerator(visual_mapping=False)
files_fast = generator_fast.generate_all_curricula()
```

### Basic Analysis
```python
# From analysis/scripts/ directory
from ecm_comprehensive_analysis import GCAnalysisEngine

# Initialize with automatic config loading from settings.json
engine = GCAnalysisEngine()  # Loads config/settings.json automatically

# Run complete analysis suite
engine.load_learning_units()
engine.define_frameworks()
engine.analyze_learning_units()          # Learning unit-level analysis
engine.analyze_versatility()             # Cross-framework analysis

# Generate comprehensive outputs (locations from settings.json)
engine.create_visualizations()           # Executive dashboard
engine.export_results()                  # CSV and JSON files
summary = engine.generate_report()       # Console report with config info
```

### Configuration Customization
```python
# Load with custom config file
engine = GCAnalysisEngine(config_path='../../config/custom_settings.json')

# Access configuration parameters
print(f"Similarity threshold: {engine.similarity_threshold}")
print(f"Output directory: {engine.output_dir}")
print(f"Quality weights: {engine.quality_weights}")

# Configuration drives all analysis parameters:
# - Similarity thresholds
# - Classification criteria  
# - Output formats and locations
# - Framework weights
# - Visualization settings
```

### Educational Profiles Generation
```python
# From analysis/scripts/ directory
from generate_educational_profiles import GCProfilesGenerator

# Initialize generator (auto-load from config/settings.json)
profiles_gen = GCProfilesGenerator()

# Generate educational profiles
profile_files = profiles_gen.generate_sample_profiles()

# All output paths and formats controlled by settings.json
print(f"Profiles saved to: {profiles_gen.output_dir}")
```

### Custom Framework Integration
```python
# Add custom framework
custom_framework = {
    'name': 'Custom Industry Framework',
    'domain': 'Industry Specific',
    'authority': 'Industry Body',
    'competencies': [
        'Industry competency 1',
        'Industry competency 2',
        # ... additional competencies
    ]
}

engine.frameworks['CUSTOM'] = custom_framework
```

---

## Performance

### Analysis Benchmarks
- **Comprehensive Analysis**: ~5-6 minutes for complete 90×7 matrix (current TF-IDF method)
- **Enhanced Curriculum Generation**: ~2-3 minutes for 10 curricula (30 files)
- **SBERT Analysis**: ~2-3 minutes estimated (when implemented)
- **Visualization Generation**: ~30 seconds
- **Data Export**: ~10 seconds
- **Memory Usage**: <512MB for complete analysis

### Scalability
- **Learning Unit Capacity**: Tested with 90 learning units, scales to 500+
- **Framework Support**: 7 current, architected for 20+
- **Analysis Methods**: Both TF-IDF and SBERT (planned)
- **Curriculum Generation**: Tested with 10 curricula, scales to 50+

---

## Directory Structure

```
GC/
├── README.md                              # This comprehensive guide
├── requirements.txt                       # Python dependencies
├── analysis/                              # Analysis engines
│   ├── scripts/                          # Main analysis scripts
│   │   ├── ecm_comprehensive_analysis.py  # Complete analysis suite
│   │   ├── generate_curricula_toggle.py   # Enhanced curriculum generator
│   │   ├── generate_educational_profiles.py # Educational profiles generator
│   │   └── test_paths.py                  # Path verification utility
│   └── results/                          # Analysis outputs
├── generators/                           # Legacy curriculum generators
│   ├── generate_curricula.py             # Basic curriculum generator
│   └── generate_educational_profiles.py  # Basic profile generator
├── web/                                  # Web interface
│   └── app.py                            # Flask application
├── input/                                # Source data
│   ├── modules/modules_v5.json           # 90-learning unit repository
│   └── educational_profiles/             # Professional profiles
├── output/                               # Generated outputs
│   ├── curricula/                        # Generated curricula
│   └── profiles/                         # Educational profiles
└── config/                               # Configuration files
    └── settings.json                     # Main configuration file
```

---

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhanced-curricula`)
3. Install dependencies (`pip install -r requirements.txt`)
4. Run tests (`python -m pytest tests/`)
5. Commit changes (`git commit -m 'Add enhanced curriculum generation'`)
6. Push to branch (`git push origin feature/enhanced-curricula`)
7. Open Pull Request

### Priority Contributions Needed
- **SBERT Implementation**: Help with semantic similarity upgrade
- **Testing Suite**: Comprehensive unit and integration tests
- **Documentation**: API documentation and tutorials
- **Benchmarking**: Performance comparison studies
- **Visual Mapping Enhancement**: Advanced curriculum visualization
- **Multi-language Support**: International framework expansion

---

## Citation

```bibtex
@inproceedings{ecm2026,
    title={The Curriculum Generator (GC): A Framework for Multi-Objective Curriculum Optimization with Enhanced Standards Compliance},
    author={Anonymous Author1 and Anonymous Author2},
    booktitle={Proceedings of The 57th ACM Technical Symposium on Computer Science Education},
    series={SIGCSE TS '26},
    year={2026},
    publisher={ACM},
    note={Enhanced with educational standards compliance and learning unit-based architecture}
}
```




## Updates 

analysis/scripts/generate_educational_profiles.py is generating the educational_profiles educational_profiles_short.json.

analysis/scripts/generate_curricula_toggle.py is the enhanced curriculum generator addressing educational standards critique and compliance requirements.


---

## Support

### Documentation
- **Installation Guide**: Quick start section above
- **API Reference**: See code documentation
- **Examples**: Usage examples section
- **Enhanced Curriculum Generation**: generate_curricula_toggle.py documentation

### Community
- **Issues**: [GitHub Issues](https://github.com/dietmarja/GC/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dietmarja/GC/discussions)
- **SBERT Help**: Tag issues with `enhancement` + `similarity`
- **Curriculum Standards**: Tag issues with `curriculum` + `standards`

### Contact
- **Research Inquiries**: Contact via paper authors
- **Technical Support**: GitHub Issues
- **SBERT Implementation**: Open to collaboration
- **Educational Standards**: Contact for compliance guidance

---

## Acknowledgments

- **European Commission**: Framework definitions and validation standards
- **IEEE/ACM**: Computing curriculum guidelines (CS2023)
- **Research Community**: Feedback and validation support
- **HuggingFace**: Sentence-transformers library for future SBERT integration
- **Educational Standards Bodies**: EQF and British educational terminology guidance

---

**GC v1.2** - *Advancing Educational Technology through Multi-Level Curriculum Optimization with Enhanced Standards Compliance*

*Supporting evidence-based curriculum design with enhanced educational standards compliance and learning unit-based architecture*
