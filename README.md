# AI Candidate Screening Pipeline MVP

A production-quality automated resume screening system using Claude AI.

## Features

- **Resume Parsing**: Extracts structured candidate data
- **Intelligent Scoring**: Weighted criteria (Skills 35%, Experience 25%, Preferred 20%, Education 10%, Soft Skills 10%)
- **Interview Questions**: 5 personalized questions per candidate
- **Hiring Recommendation**: HIRE (80+) / REVIEW (60-79) / PASS (<60)
- **Demo Mode**: Works without API key
- **JSON Output**: Structured reports for integration

## Quick Start

```bash
pip install -r requirements.txt
python candidate_screener.py --demo strong
python candidate_screener.py --demo weak
python candidate_screener.py --resume resume.txt --output report.json
```

## Architecture

```
candidate_screener.py (980+ lines)
├── Claude API Integration (with fallback)
├── Regex-based Demo Mode
├── Weighted Scoring Engine
├── Interview Question Generator
└── CLI Interface
```

## Technology

Python | Claude API | TypedDict | JSON | Regex
