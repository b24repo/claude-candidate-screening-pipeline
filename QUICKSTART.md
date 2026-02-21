# Quick Start Guide - AI Candidate Screening Pipeline

Get up and running in 2 minutes. No API key needed for demo mode.

## Installation (30 seconds)

```bash
cd MVP2_Candidate_Screening
# Optional: pip install -r requirements.txt
```

That's it! The demo mode works with just Python 3.7+

## See It In Action (1 minute)

### Option 1: Demo with Sample Data (Easiest)

```bash
# See how it works with a strong candidate
python candidate_screener.py --demo strong

# Or try a weak candidate
python candidate_screener.py --demo weak
```

You'll see a detailed screening report with scores, matched skills, and interview questions.

### Option 2: Save to JSON (For Integration Testing)

```bash
python candidate_screener.py --demo strong --output report.json

# Then view or process the JSON
cat report.json
```

## What You Get

Each screening produces:

1. **Overall Score** (0-100) with Recommendation (HIRE/REVIEW/PASS)
2. **Component Scores**:
   - Skills Match (required, preferred, nice-to-have)
   - Experience Level
   - Education Assessment
3. **Skills Analysis**:
   - What they have (matched required/preferred skills)
   - What they're missing (critical gaps)
4. **Interview Questions** (5 personalized questions)

## Example Output

```
Candidate: John Smith
Position: Digital Marketing Manager
Overall Score: 91.5/100
Recommendation: HIRE
Confidence: HIGH

Skills Match: 95.0/100
  Matched: Digital Marketing, Google Analytics, Content Marketing, Email Marketing
  Missing: (none)

Experience: 7 years (exceeds 5 year requirement)
Education: Master's Degree

Interview Questions:
1. Can you walk us through your most successful project...
2. How have you evolved your approach...
3. Tell us about a time you had to develop a skill...
4. Describe your leadership style...
5. What attracts you to this role...
```

## With Your Own Resume

```bash
# Paste resume text into resume.txt
# Then run:
python candidate_screener.py --resume resume.txt

# Or output to JSON:
python candidate_screener.py --resume resume.txt --output my_report.json
```

## Production Setup (With Claude API)

```bash
# 1. Get API key from https://console.anthropic.com
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. Install Python package
pip install anthropic

# 3. Run screening
python candidate_screener.py --resume resume.txt --output report.json
```

With the API, candidate extraction is more accurate, and interview questions are AI-generated and personalized.

## Integrate With Automation Platforms

### n8n
1. Set up HTTP webhook trigger
2. Add HTTP request node calling this script via API
3. Parse JSON output
4. Route based on recommendation field

### Make.com
Similar HTTP setup with Make's routing

### Zapier
Use Zapier's webhook connector or code execution

See README.md for detailed integration examples.

## Customize for Your Roles

Edit `SAMPLE_JOB_REQUIREMENTS` in `candidate_screener.py`:

```python
SAMPLE_JOB_REQUIREMENTS: JobRequirements = {
    "title": "Your Job Title",
    "required_skills": ["Skill1", "Skill2", "Skill3"],
    "minimum_experience_years": 5,
    "preferred_skills": ["PrefSkill1"],
    "nice_to_have_skills": ["NiceSkill1"],
    "minimum_education": "Bachelor's Degree"
}
```

Adjust scoring weights if needed:

```python
SCORING_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.35,  # Technical skills
    "preferred_skills_weight": 0.20,
    "experience_weight": 0.25,       # Years of experience
    "education_weight": 0.10,
    "soft_skills_weight": 0.10       # Leadership, communication
}
```

## All Commands

```bash
# Demo mode
python candidate_screener.py --demo strong
python candidate_screener.py --demo weak

# With file
python candidate_screener.py --resume path/to/resume.txt

# Output options
python candidate_screener.py --demo strong --output report.json
python candidate_screener.py --resume resume.txt --json-only

# Help
python candidate_screener.py --help
```

## Testing the Output

Check the included reports:
- `strong_report.json` - Example of a 91.5/100 candidate (HIRE)
- `weak_report.json` - Example of a 16.8/100 candidate (PASS)
- `sample_output.json` - Full schema documentation

## Architecture at a Glance

```
Resume Input
    ↓
Extract Candidate Data (Claude API or regex)
    ↓
Score Against Requirements
    ├─ Skill matching
    ├─ Experience level
    └─ Education assessment
    ↓
Generate Interview Questions (Claude API or templates)
    ↓
Make Recommendation (HIRE/REVIEW/PASS)
    ↓
JSON Report Output
```

## Key Features

✓ **No API key needed** for demo mode
✓ **Production-ready** code with type hints
✓ **Configurable** job requirements and weights
✓ **Personalized** questions based on candidate profile
✓ **Clear recommendations** with confidence levels
✓ **Fallback architecture** (API fails gracefully)
✓ **Integration-ready** JSON output

## Next Steps

1. Try the demo to see quality of output
2. Customize job requirements for your roles
3. Test with real resumes
4. Integrate with your applicant tracking system
5. Deploy as API server for automation platforms

## Questions?

- See README.md for detailed documentation
- Review candidate_screener.py code comments
- Check sample_output.json for expected output format

---

**Ready to automate screening?** You have a production-quality system ready to deploy.
