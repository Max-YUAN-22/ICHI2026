# A Lightweight, Deployable AI Agent for Cancer Care Navigation: A Data-Driven Approach for Regions with Unique Epidemiological Profiles

A data-driven AI system for cancer care navigation in regions with unique epidemiological profiles.

## Overview

This repository contains the implementation code for a lightweight, deployable AI agent designed to support cancer care navigation. The system integrates Retrieval-Augmented Generation (RAG), multimodal interaction, and localized healthcare resources.

## System Components

- **Backend**: Flask-based RESTful API
- **Frontend**: Web interface with interactive components
- **Knowledge Base**: Integration with clinical guidelines and local health data
- **Core Modules**: Process navigation, risk alert system, multimodal functions

## Installation

### Prerequisites
- Python 3.9+
- 4GB RAM minimum

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the system
python app.py
```

Access the system at `http://localhost:5000`

## Project Structure

```
ICHI2026/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/                # Frontend templates
│   └── index.html
├── macau_cancer_data/        # Data directory
└── analyze_macau_data.py     # Data analysis utilities
```

## Key Features

- Localized process navigation workflow
- Data-driven risk alert system
- Multimodal interaction support (voice, image, visualization)
- Lightweight deployment design

## System Requirements

- **RAM**: 4GB minimum
- **Python**: 3.9+
- **OS**: Windows 10, macOS, or Linux

## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{yuan2026lightweight,
  title={A Lightweight, Deployable AI Agent for Cancer Care Navigation: A Data-Driven Approach for Regions with Unique Epidemiological Profiles},
  author={Yuan, Tianzuo},
  booktitle={IEEE International Conference on Healthcare Informatics (ICHI)},
  year={2026},
  organization={IEEE}
}
```

## Contact

For questions or inquiries, please contact: cc31642@um.edu.mo

## License

This project is licensed under the MIT License.

## Note

This repository contains the implementation code accompanying a research paper currently under review. Detailed experimental results and analysis are available in the paper.
