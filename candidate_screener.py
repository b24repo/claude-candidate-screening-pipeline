#!/usr/bin/env python3
"""
AI Candidate Screening Pipeline MVP
A production-quality automated resume screening system using Claude API.

This module provides automated candidate screening with:
- Resume parsing and structured data extraction
- Skill-based candidate scoring
- Interview question generation
- Personalized hiring recommendations
"""

import json
import os
import sys
import argparse
from typing import TypedDict, Optional, Literal
from dataclasses import dataclass, asdict
from datetime import datetime
import re


# ============================================================================
# Type Definitions
# ============================================================================

class CandidateData(TypedDict):
    """Structured candidate information extracted from resume."""
    name: str
    email: str
    phone: Optional[str]
    skills: list[str]
    experience_years: int
    education: list[str]
    past_roles: list[str]
    summary: str


class JobRequirements(TypedDict):
    """Job requirements for scoring candidates."""
    title: str
    required_skills: list[str]
    minimum_experience_years: int
    preferred_skills: list[str]
    nice_to_have_skills: list[str]
    minimum_education: str


class ScoringCriteria(TypedDict):
    """Weighted scoring criteria."""
    required_skills_weight: float
    preferred_skills_weight: float
    experience_weight: float
    education_weight: float
    soft_skills_weight: float


@dataclass
class ScreeningReport:
    """Final screening report for a candidate."""
    candidate_name: str
    candidate_email: str
    job_title: str
    screening_date: str

    # Scores
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float

    # Analysis
    matched_required_skills: list[str]
    missing_required_skills: list[str]
    matched_preferred_skills: list[str]
    experience_assessment: str
    education_assessment: str

    # Recommendation
    recommendation: Literal["hire", "pass", "review"]
    confidence: Literal["high", "medium", "low"]
    reasoning: str

    # Interview questions
    interview_questions: list[str]

    # Metadata
    extracted_candidate_data: dict


# ============================================================================
# Demo Data
# ============================================================================

SAMPLE_RESUME_STRONG = """
JOHN SMITH
john.smith@email.com | (555) 123-4567 | LinkedIn.com/in/johnsmith

PROFESSIONAL SUMMARY
Results-driven Digital Marketing Manager with 7 years of experience building and executing
integrated marketing campaigns. Proven track record increasing brand awareness by 250% and
driving 40% revenue growth through data-driven strategies.

CORE COMPETENCIES
- Digital Marketing Strategy & Campaign Management
- Google Analytics & Data Analysis
- Content Marketing & SEO
- Email Marketing Automation
- Social Media Marketing & Community Management
- Market Research & Competitive Analysis
- Marketing Automation (HubSpot, Marketo)
- Project Management
- Team Leadership & Cross-functional Collaboration

PROFESSIONAL EXPERIENCE

Senior Digital Marketing Manager | TechCorp Inc. | 2021 - Present
- Led cross-functional team of 5 marketing professionals managing $2M annual budget
- Designed and executed integrated digital campaigns resulting in 45% increase in qualified leads
- Implemented marketing automation workflows reducing manual work by 60%
- Managed SEO strategy resulting in 120% increase in organic traffic
- A/B tested landing pages achieving 35% improvement in conversion rate

Digital Marketing Specialist | GrowthWave Agency | 2019 - 2021
- Managed digital marketing campaigns for 15+ B2B SaaS clients
- Developed content marketing strategy generating 500K monthly impressions
- Optimized Google Ads campaigns reducing cost-per-acquisition by 28%
- Trained junior team members on marketing analytics and reporting
- Increased email marketing engagement rates by 42%

Marketing Coordinator | SmartBrand Solutions | 2016 - 2019
- Created and executed social media campaigns across 4 platforms
- Analyzed marketing metrics and prepared monthly performance reports
- Supported product launches with integrated marketing communications
- Collaborated with sales team to develop marketing materials and leads lists

EDUCATION
Master of Business Administration (MBA) in Marketing | University of California | 2016
Bachelor of Science in Business Administration | State University | 2015

CERTIFICATIONS
- Google Analytics Certification (2020)
- HubSpot Inbound Marketing Certification (2021)
- Google Ads Certification (2022)

ADDITIONAL SKILLS
- Advanced Excel & Google Sheets
- Figma & Canva (Design basics)
- Python for data analysis (beginner)
- Salesforce & CRM systems
"""

SAMPLE_RESUME_WEAK = """
JANE DOE
jane.doe@email.com

SUMMARY
Recently graduated student looking for marketing opportunities. Have done some social media
work and basic content creation. Eager to learn and grow in the marketing field.

EXPERIENCE
Social Media Intern | LocalBusiness.com | 2024 - Present
- Posted content on Facebook and Instagram
- Wrote blog articles on various topics
- Created social media graphics
- Responded to customer inquiries

School Projects | University | 2022-2024
- Created marketing presentation for class project
- Designed poster for university event
- Participated in marketing club

EDUCATION
Bachelor of Science in Communications | University | Expected May 2024
Relevant Coursework: Introduction to Marketing, Digital Communications, Social Media 101

SKILLS
- Social media
- Writing
- Microsoft Office
- Instagram & TikTok
- Graphic design (basic)
"""

SAMPLE_JOB_REQUIREMENTS: JobRequirements = {
    "title": "Digital Marketing Manager",
    "required_skills": ["Digital Marketing Strategy", "Google Analytics", "Content Marketing", "Email Marketing"],
    "minimum_experience_years": 5,
    "preferred_skills": ["Marketing Automation", "SEO", "A/B Testing", "Data Analysis"],
    "nice_to_have_skills": ["Python", "Figma", "Salesforce", "CRM"],
    "minimum_education": "Bachelor's Degree"
}

SCORING_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.35,
    "preferred_skills_weight": 0.20,
    "experience_weight": 0.25,
    "education_weight": 0.10,
    "soft_skills_weight": 0.10
}


# ============================================================================
# Claude Integration (Mock and Real)
# ============================================================================

def extract_candidate_data_with_claude(resume_text: str) -> CandidateData:
    """
    Extract structured candidate data from resume using Claude API.

    In production, this would use the actual Claude API.
    For demo mode, returns realistic extracted data.

    Args:
        resume_text: Raw resume text to parse

    Returns:
        Structured candidate data as TypedDict
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Error: anthropic package not installed. Using demo mode extraction.")
        return extract_candidate_data_demo(resume_text)

    # Check if API key is available
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY not set. Using demo mode extraction.")
        return extract_candidate_data_demo(resume_text)

    try:
        client = Anthropic()

        prompt = f"""Extract structured candidate information from this resume.
        Return ONLY valid JSON (no markdown, no code blocks) with these exact fields:
        - name: Full name
        - email: Email address
        - phone: Phone number (or null)
        - skills: List of technical and professional skills
        - experience_years: Total years of relevant experience (integer)
        - education: List of degrees/certifications
        - past_roles: List of job titles held
        - summary: 2-3 sentence professional summary

        Resume:
        {resume_text}

        Return only the JSON object, no other text."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        extracted = json.loads(response_text)
        return CandidateData(
            name=extracted.get("name", "Unknown"),
            email=extracted.get("email", "unknown@email.com"),
            phone=extracted.get("phone"),
            skills=extracted.get("skills", []),
            experience_years=int(extracted.get("experience_years", 0)),
            education=extracted.get("education", []),
            past_roles=extracted.get("past_roles", []),
            summary=extracted.get("summary", "")
        )
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        print("Falling back to demo mode extraction.")
        return extract_candidate_data_demo(resume_text)


def extract_candidate_data_demo(resume_text: str) -> CandidateData:
    """
    Demo mode: Extract candidate data using simple regex patterns.
    Provides realistic fallback when API is not available.
    """
    # Extract name (first meaningful text line)
    name_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+)', resume_text, re.MULTILINE)
    name = name_match.group(1) if name_match else "Unknown Candidate"

    # Extract email
    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', resume_text)
    email = email_match.group(1) if email_match else "unknown@email.com"

    # Extract phone
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text)
    phone = phone_match.group(0) if phone_match else None

    # Extract skills (look for skill keywords)
    skills_keywords = [
        "digital marketing", "analytics", "content marketing", "seo", "email marketing",
        "social media", "marketing automation", "hubspot", "google analytics", "data analysis",
        "a/b testing", "python", "figma", "salesforce", "crm", "excel", "canva",
        "copywriting", "market research", "project management", "leadership", "communication"
    ]
    skills = [s for s in skills_keywords if s.lower() in resume_text.lower()]

    # Extract years of experience
    exp_match = re.search(r'(\d+)\s+years?', resume_text)
    experience_years = int(exp_match.group(1)) if exp_match else 0

    # Extract education
    education = []
    if "MBA" in resume_text or "Master" in resume_text:
        education.append("Master's Degree")
    if "Bachelor" in resume_text or "B.S." in resume_text or "B.A." in resume_text:
        education.append("Bachelor's Degree")
    if "Associate" in resume_text:
        education.append("Associate Degree")
    if not education:
        education.append("High School or Certificate")

    # Extract past roles
    role_keywords = [
        "Manager", "Specialist", "Coordinator", "Director", "Analyst",
        "Developer", "Engineer", "Consultant", "Executive", "Officer"
    ]
    past_roles = []
    for line in resume_text.split('\n'):
        for keyword in role_keywords:
            if keyword in line and '|' in line:
                role = line.split('|')[0].strip()
                if role and len(role) < 60:
                    past_roles.append(role)
                    break

    # Create summary
    summary = "Experienced professional with demonstrated expertise in marketing and business operations."
    if experience_years >= 5:
        summary = f"Results-driven professional with {experience_years}+ years of marketing experience and proven success in campaign management and strategy."

    return CandidateData(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        experience_years=experience_years,
        education=education,
        past_roles=past_roles[:3],  # Limit to 3 most recent
        summary=summary
    )


# ============================================================================
# Scoring Logic
# ============================================================================

def calculate_skill_match_score(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
    nice_to_have: list[str]
) -> tuple[float, list[str], list[str], list[str]]:
    """
    Calculate skill matching score and return matched/missing skills.

    Returns:
        Tuple of (score: 0-100, matched_required, missing_required, matched_preferred)
    """
    candidate_skills_lower = [s.lower() for s in candidate_skills]

    # Check required skills
    matched_required = [
        s for s in required_skills
        if any(req.lower() in cand for req in [s] for cand in candidate_skills_lower)
    ]

    # Improved matching: check if skill contains required keyword
    matched_required = []
    for req_skill in required_skills:
        req_lower = req_skill.lower()
        if any(req_lower in cand_skill.lower() for cand_skill in candidate_skills):
            matched_required.append(req_skill)

    missing_required = [s for s in required_skills if s not in matched_required]

    # Check preferred skills
    matched_preferred = []
    for pref_skill in preferred_skills:
        pref_lower = pref_skill.lower()
        if any(pref_lower in cand_skill.lower() for cand_skill in candidate_skills):
            matched_preferred.append(pref_skill)

    # Calculate score
    required_match_rate = len(matched_required) / len(required_skills) if required_skills else 0
    preferred_match_rate = len(matched_preferred) / len(preferred_skills) if preferred_skills else 0

    skill_score = (required_match_rate * 70) + (preferred_match_rate * 30)

    return skill_score, matched_required, missing_required, matched_preferred


def calculate_experience_score(
    candidate_years: int,
    minimum_required: int
) -> tuple[float, str]:
    """
    Calculate experience score based on years.

    Returns:
        Tuple of (score: 0-100, assessment: str)
    """
    if candidate_years >= minimum_required:
        # Full points for meeting minimum
        bonus = min((candidate_years - minimum_required) * 5, 20)  # Max +20 bonus
        score = 80 + bonus
        assessment = f"Meets requirement with {candidate_years} years of experience"
    else:
        shortfall = minimum_required - candidate_years
        score = max(0, 80 - (shortfall * 15))
        assessment = f"Below target ({candidate_years} years vs {minimum_required} required)"

    return min(score, 100), assessment


def calculate_education_score(
    candidate_education: list[str],
    minimum_education: str
) -> tuple[float, str]:
    """
    Calculate education score.

    Returns:
        Tuple of (score: 0-100, assessment: str)
    """
    education_hierarchy = {
        "High School or Certificate": 1,
        "Associate Degree": 2,
        "Bachelor's Degree": 3,
        "Master's Degree": 4,
        "PhD": 5
    }

    required_level = education_hierarchy.get(minimum_education, 3)
    candidate_level = max(
        (education_hierarchy.get(edu, 0) for edu in candidate_education),
        default=0
    )

    if candidate_level >= required_level:
        score = 95
        assessment = f"Meets or exceeds requirement: {candidate_education[0]}"
    elif candidate_level == required_level - 1:
        score = 70
        assessment = f"One level below requirement: {candidate_education[0]}"
    else:
        score = max(0, 50 - (required_level - candidate_level) * 15)
        assessment = f"Below requirement: {candidate_education[0] if candidate_education else 'Not specified'}"

    return min(score, 100), assessment


def score_candidate(
    candidate_data: CandidateData,
    job_requirements: JobRequirements,
    weights: ScoringCriteria
) -> dict:
    """
    Calculate comprehensive candidate score against job requirements.

    Returns:
        Dictionary with all scoring components
    """
    # Skill matching
    skill_score, matched_req, missing_req, matched_pref = calculate_skill_match_score(
        candidate_data["skills"],
        job_requirements["required_skills"],
        job_requirements["preferred_skills"],
        job_requirements["nice_to_have_skills"]
    )

    # Experience matching
    exp_score, exp_assessment = calculate_experience_score(
        candidate_data["experience_years"],
        job_requirements["minimum_experience_years"]
    )

    # Education matching
    edu_score, edu_assessment = calculate_education_score(
        candidate_data["education"],
        job_requirements["minimum_education"]
    )

    # Soft skills assessment (from summary/roles)
    soft_skills_keywords = ["leadership", "communication", "collaboration", "management", "team"]
    soft_skill_score = 60
    if any(kw in candidate_data["summary"].lower() for kw in soft_skills_keywords):
        soft_skill_score = 80
    if any(kw in str(candidate_data["past_roles"]).lower() for kw in ["manager", "lead", "director"]):
        soft_skill_score = 90

    # Weighted overall score
    overall_score = (
        skill_score * weights["required_skills_weight"] +
        skill_score * weights["preferred_skills_weight"] * 0.5 +  # Preferred skills less important
        exp_score * weights["experience_weight"] +
        edu_score * weights["education_weight"] +
        soft_skill_score * weights["soft_skills_weight"]
    )

    return {
        "overall_score": round(overall_score, 1),
        "skills_score": round(skill_score, 1),
        "experience_score": round(exp_score, 1),
        "education_score": round(edu_score, 1),
        "matched_required_skills": matched_req,
        "missing_required_skills": missing_req,
        "matched_preferred_skills": matched_pref,
        "experience_assessment": exp_assessment,
        "education_assessment": edu_assessment
    }


# ============================================================================
# Interview Question Generation
# ============================================================================

def generate_interview_questions(
    candidate_data: CandidateData,
    job_requirements: JobRequirements,
    scoring_results: dict,
    api_fallback: bool = False
) -> list[str]:
    """
    Generate personalized interview questions based on candidate profile.

    Args:
        candidate_data: Extracted candidate information
        job_requirements: Job requirements
        scoring_results: Scoring results from candidate evaluation
        api_fallback: If True, use template-based questions instead of API

    Returns:
        List of interview questions
    """
    # Try to use Claude API if available
    if not api_fallback:
        try:
            from anthropic import Anthropic
            if os.environ.get("ANTHROPIC_API_KEY"):
                return _generate_questions_with_claude(
                    candidate_data, job_requirements, scoring_results
                )
        except Exception as e:
            print(f"Warning: Could not use Claude API for questions: {e}")

    # Fallback to template-based questions
    return _generate_questions_template(candidate_data, job_requirements, scoring_results)


def _generate_questions_with_claude(
    candidate_data: CandidateData,
    job_requirements: JobRequirements,
    scoring_results: dict
) -> list[str]:
    """Generate questions using Claude API."""
    from anthropic import Anthropic

    client = Anthropic()

    missing_skills = scoring_results.get("missing_required_skills", [])
    matched_skills = scoring_results.get("matched_required_skills", [])

    prompt = f"""Generate 5 personalized interview questions for a candidate with this profile:

Candidate: {candidate_data['name']}
Experience: {candidate_data['experience_years']} years
Skills: {', '.join(candidate_data['skills'][:10])}
Past Roles: {', '.join(candidate_data['past_roles'])}

For Job: {job_requirements['title']}
Required Skills: {', '.join(job_requirements['required_skills'])}
Matched Skills: {', '.join(matched_skills)}
Missing Skills: {', '.join(missing_skills)}

Create questions that:
1. Probe technical competency in matched areas
2. Address gaps in missing required skills
3. Explore relevant past experience
4. Assess problem-solving and soft skills
5. Determine motivation and culture fit

Return only a JSON array of strings (the questions), no other text."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text.strip()

    # Clean up markdown if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    questions = json.loads(response_text)
    return questions if isinstance(questions, list) else _generate_questions_template(
        candidate_data, job_requirements, scoring_results
    )


def _generate_questions_template(
    candidate_data: CandidateData,
    job_requirements: JobRequirements,
    scoring_results: dict
) -> list[str]:
    """Generate questions using templates (fallback)."""
    questions = []
    missing_skills = scoring_results.get("missing_required_skills", [])

    # Core competency questions
    questions.append(
        f"Can you walk us through your most successful {job_requirements['title'].lower()} project "
        f"and the metrics you used to measure success?"
    )

    # Experience depth
    if candidate_data["experience_years"] >= 5:
        questions.append(
            "How have you evolved your approach to digital marketing strategy over the years, "
            "and what key lessons have you learned?"
        )
    else:
        questions.append(
            "What is your understanding of modern digital marketing best practices, "
            "and how do you stay current with industry trends?"
        )

    # Skill gaps
    if missing_skills:
        skill = missing_skills[0]
        questions.append(
            f"While we see you have strong {candidate_data['skills'][0] if candidate_data['skills'] else 'marketing'} skills, "
            f"how would you approach learning {skill} in this role?"
        )
    else:
        questions.append(
            "Tell us about a time when you had to develop a skill outside your comfort zone. "
            "How did you approach it?"
        )

    # Soft skills / team dynamics
    if "lead" in str(candidate_data["past_roles"]).lower() or "manager" in str(candidate_data["past_roles"]).lower():
        questions.append(
            "Describe your leadership style and how you approach managing and developing team members."
        )
    else:
        questions.append(
            "Tell us about a time you successfully collaborated with people from different departments "
            "or with different expertise. What made it effective?"
        )

    # Culture and motivation
    questions.append(
        "What attracts you to this role and our company, and where do you see yourself in 3 years?"
    )

    return questions


# ============================================================================
# Recommendation Logic
# ============================================================================

def generate_recommendation(scoring_results: dict, candidate_data: CandidateData) -> tuple[Literal["hire", "pass", "review"], Literal["high", "medium", "low"], str]:
    """
    Generate hiring recommendation based on scores.

    Returns:
        Tuple of (recommendation, confidence, reasoning)
    """
    overall_score = scoring_results["overall_score"]
    missing_required = scoring_results["missing_required_skills"]
    matched_required = scoring_results["matched_required_skills"]
    exp_score = scoring_results["experience_score"]

    # Recommendation logic
    if overall_score >= 80 and len(missing_required) == 0:
        recommendation = "hire"
        confidence = "high" if overall_score >= 90 else "medium"
        reasoning = f"Strong candidate with {overall_score}% overall score. Meets all required skills and experience requirements."

    elif overall_score >= 70 and len(missing_required) <= 1:
        recommendation = "review"
        confidence = "medium"
        if missing_required:
            reasoning = f"Solid candidate ({overall_score}%) but missing {missing_required[0]}. Worth reviewing for potential with training."
        else:
            reasoning = f"Good candidate ({overall_score}%) but slightly below ideal experience level. Recommend interview to assess potential."

    elif overall_score >= 60:
        recommendation = "review"
        confidence = "low"
        reasoning = f"Moderate candidate ({overall_score}%) with gaps in required skills. May be trainable but requires further assessment."

    else:
        recommendation = "pass"
        confidence = "high"
        reasoning = f"Does not meet minimum requirements ({overall_score}%). Missing multiple critical skills: {', '.join(missing_required[:2])}"

    return recommendation, confidence, reasoning


# ============================================================================
# Main Screening Pipeline
# ============================================================================

def screen_candidate(
    resume_text: str,
    job_requirements: JobRequirements = SAMPLE_JOB_REQUIREMENTS,
    scoring_weights: ScoringCriteria = SCORING_WEIGHTS
) -> ScreeningReport:
    """
    Execute full candidate screening pipeline.

    Args:
        resume_text: Raw resume text
        job_requirements: Job requirements for scoring
        scoring_weights: Weights for different scoring factors

    Returns:
        Complete screening report
    """
    # Step 1: Extract candidate data
    print("Extracting candidate information...")
    candidate_data = extract_candidate_data_with_claude(resume_text)

    # Step 2: Score candidate
    print("Scoring candidate against requirements...")
    scoring_results = score_candidate(candidate_data, job_requirements, scoring_weights)

    # Step 3: Generate interview questions
    print("Generating interview questions...")
    interview_questions = generate_interview_questions(
        candidate_data, job_requirements, scoring_results
    )

    # Step 4: Generate recommendation
    recommendation, confidence, reasoning = generate_recommendation(scoring_results, candidate_data)

    # Step 5: Create report
    report = ScreeningReport(
        candidate_name=candidate_data["name"],
        candidate_email=candidate_data["email"],
        job_title=job_requirements["title"],
        screening_date=datetime.now().isoformat(),

        overall_score=scoring_results["overall_score"],
        skills_score=scoring_results["skills_score"],
        experience_score=scoring_results["experience_score"],
        education_score=scoring_results["education_score"],

        matched_required_skills=scoring_results["matched_required_skills"],
        missing_required_skills=scoring_results["missing_required_skills"],
        matched_preferred_skills=scoring_results["matched_preferred_skills"],
        experience_assessment=scoring_results["experience_assessment"],
        education_assessment=scoring_results["education_assessment"],

        recommendation=recommendation,
        confidence=confidence,
        reasoning=reasoning,

        interview_questions=interview_questions,

        extracted_candidate_data={
            "name": candidate_data["name"],
            "email": candidate_data["email"],
            "phone": candidate_data["phone"],
            "skills": candidate_data["skills"],
            "experience_years": candidate_data["experience_years"],
            "education": candidate_data["education"],
            "past_roles": candidate_data["past_roles"],
            "summary": candidate_data["summary"]
        }
    )

    return report


# ============================================================================
# Output and Reporting
# ============================================================================

def report_to_json(report: ScreeningReport) -> dict:
    """Convert screening report to JSON-serializable dictionary."""
    return {
        "candidate": {
            "name": report.candidate_name,
            "email": report.candidate_email,
            "extracted_data": report.extracted_candidate_data
        },
        "screening": {
            "job_title": report.job_title,
            "screening_date": report.screening_date,
            "overall_score": report.overall_score,
            "recommendation": report.recommendation,
            "confidence": report.confidence,
            "reasoning": report.reasoning
        },
        "scores": {
            "overall": report.overall_score,
            "skills": report.skills_score,
            "experience": report.experience_score,
            "education": report.education_score
        },
        "skills_analysis": {
            "matched_required": report.matched_required_skills,
            "missing_required": report.missing_required_skills,
            "matched_preferred": report.matched_preferred_skills
        },
        "assessments": {
            "experience": report.experience_assessment,
            "education": report.education_assessment
        },
        "interview_questions": report.interview_questions
    }


def print_report(report: ScreeningReport) -> None:
    """Print human-readable screening report."""
    print("\n" + "=" * 80)
    print("CANDIDATE SCREENING REPORT")
    print("=" * 80)

    print(f"\nCandidate: {report.candidate_name}")
    print(f"Email: {report.candidate_email}")
    print(f"Position: {report.job_title}")
    print(f"Screening Date: {report.screening_date[:10]}")

    print(f"\n{'OVERALL SCORE':-^80}")
    print(f"Overall: {report.overall_score}/100 | Recommendation: {report.recommendation.upper()}")
    print(f"Confidence: {report.confidence.upper()}")

    print(f"\n{'SCORE BREAKDOWN':-^80}")
    print(f"Skills Match:        {report.skills_score:6.1f}/100")
    print(f"Experience:          {report.experience_score:6.1f}/100")
    print(f"Education:           {report.education_score:6.1f}/100")

    print(f"\n{'SKILLS ANALYSIS':-^80}")
    print(f"Matched Required Skills ({len(report.matched_required_skills)}):")
    for skill in report.matched_required_skills:
        print(f"  ✓ {skill}")

    if report.missing_required_skills:
        print(f"\nMissing Required Skills ({len(report.missing_required_skills)}):")
        for skill in report.missing_required_skills:
            print(f"  ✗ {skill}")

    if report.matched_preferred_skills:
        print(f"\nMatched Preferred Skills ({len(report.matched_preferred_skills)}):")
        for skill in report.matched_preferred_skills[:5]:
            print(f"  + {skill}")

    print(f"\n{'ASSESSMENTS':-^80}")
    print(f"Experience: {report.experience_assessment}")
    print(f"Education:  {report.education_assessment}")

    print(f"\n{'RECOMMENDATION':-^80}")
    print(f"{report.reasoning}")

    print(f"\n{'INTERVIEW QUESTIONS':-^80}")
    for i, question in enumerate(report.interview_questions, 1):
        print(f"\n{i}. {question}")

    print("\n" + "=" * 80)


# ============================================================================
# CLI Interface
# ============================================================================

def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Candidate Screening Pipeline - Automated resume screening using Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Demo mode (no API key needed)
  python candidate_screener.py --demo

  # Demo mode with strong candidate
  python candidate_screener.py --demo strong

  # Screen actual resume from file
  python candidate_screener.py --resume path/to/resume.txt

  # Screen with output to file
  python candidate_screener.py --demo --output results.json
        """
    )

    parser.add_argument(
        "--demo",
        nargs="?",
        const="strong",
        choices=["strong", "weak"],
        help="Run in demo mode with sample resume (strong or weak candidate)"
    )

    parser.add_argument(
        "--resume",
        type=str,
        help="Path to resume file to screen"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Save JSON report to specified file"
    )

    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output only JSON, suppress human-readable report"
    )

    args = parser.parse_args()

    # Determine which resume to use
    if args.demo:
        if args.demo == "strong":
            resume_text = SAMPLE_RESUME_STRONG
            print("Running in DEMO mode with STRONG candidate...")
        else:
            resume_text = SAMPLE_RESUME_WEAK
            print("Running in DEMO mode with WEAK candidate...")
    elif args.resume:
        try:
            with open(args.resume, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            print(f"Screening resume from: {args.resume}")
        except FileNotFoundError:
            print(f"Error: Resume file not found: {args.resume}")
            sys.exit(1)
    else:
        parser.print_help()
        print("\nError: Please provide --demo or --resume argument")
        sys.exit(1)

    # Run screening pipeline
    report = screen_candidate(resume_text)

    # Output results
    if not args.json_only:
        print_report(report)

    # Save to file if requested
    if args.output:
        report_json = report_to_json(report)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report_json, f, indent=2)
        print(f"\nReport saved to: {args.output}")
    else:
        # Always output JSON when --output not specified
        report_json = report_to_json(report)
        if args.json_only or args.demo:
            print("\nJSON Output:")
            print(json.dumps(report_json, indent=2))


if __name__ == "__main__":
    main()
