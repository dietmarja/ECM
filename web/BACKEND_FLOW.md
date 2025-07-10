# DSCG Backend Curriculum Development Flow

## Main Entry Points

### Web Interface
POST /api/generate/curriculum
├── Input validation
├── Role information lookup
├── EnhancedCurriculumBuilder.build_curriculum_with_semesters()
├── OutputManager.save_curriculum()
└── Return job status + file paths

### CLI Interface
python3 -m scripts.curriculum_generator.main
├── Argument parsing
├── CurriculumGenerator.generate_curriculum()
├── EnhancedCurriculumBuilder.build_curriculum_with_semesters()
└── OutputManager.save_curriculum()

## Core Backend Components

1. **EnhancedCurriculumBuilder** (`scripts/curriculum_generator/components/curriculum_builder.py`)
   - Main curriculum generation logic
   - Semester breakdown and module selection
   - Educational profile integration

2. **EducationalProfilesManager** (`scripts/curriculum_generator/domain/educational_profiles.py`)
   - Generates T3.2 compliant educational profiles
   - Role-specific competency mapping

3. **OutputManager** (`scripts/curriculum_generator/core/output_manager.py`)
   - Handles file generation (JSON, HTML)
   - File saving and path management

4. **RoleManager** (`scripts/curriculum_generator/domain/role_manager.py`)
   - Role definition and validation
   - EQF level and ECTS management
