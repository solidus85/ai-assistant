# Project Folder Structure

## Root Directory Organization

The project has been reorganized for better maintainability:

### Core Application Files
- `run.py` - Application entry point
- `config.py` - Configuration classes
- `requirements.txt` - Python dependencies
- `CLAUDE.md` - Project context for Claude
- `start.bat` - Windows batch file to start app

### Application Code
- `app/` - Main Flask application
  - `__init__.py` - App factory
  - `routes.py` - Main routes
  - `api/` - API blueprints
  - `services/` - Business logic
  - `models/` - Data models (future use)
  - `utils/` - Utilities

### Static Assets
- `static/`
  - `css/` - Modularized CSS files
    - `main.css` - Main CSS entry point (imports all others)
    - `base/` - Reset, animations
    - `layout/` - Container, header
    - `components/` - UI components (buttons, chat, messages, etc.)
    - `utilities/` - Responsive design

### Scripts
- `scripts/`
  - `setup/` - Setup and configuration scripts
    - `setup_*.sh` - Model setup scripts
    - `configure_*.sh` - Configuration scripts
  - `debug/` - Testing and debugging scripts
    - `debug_app.py` - Test Ollama connectivity
    - `test_*.py` - Various test scripts
    - `compare_accuracy.py` - Model comparison
  - `utilities/` - Utility scripts
    - `start_*.sh` - Start scripts
    - `check_models.sh` - Model checking

### Documentation
- `docs/`
  - `README_structure.md` - App structure docs
  - `accuracy_comparison.md` - Model accuracy comparison
  - `prompt_display_info.md` - Prompt display feature docs

### Other Files
- `templates/` - HTML templates
- `venv/` - Python virtual environment
- `app_old.py` - Old app version (backup)
- `model_configs.py` - Model configurations
- `ollama_accuracy.env` - Environment variables
- `Modelfile.q5_k_m` - Model configuration file

## CSS Architecture

The CSS has been modularized into:
- **Base**: Reset styles and animations
- **Layout**: Page structure (container, header)
- **Components**: Individual UI elements
- **Utilities**: Helper classes and responsive design

Each component has its own CSS file for better maintainability.