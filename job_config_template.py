"""
Job Configuration Templates
Customize these job profiles for different roles at your organization.

Usage:
    from job_config_template import JOBS
    requirements = JOBS['digital_marketing_manager']
    report = screen_candidate(resume_text, job_requirements=requirements)
"""

from typing import TypedDict


class JobRequirements(TypedDict):
    """Job requirements for candidate scoring."""
    title: str
    required_skills: list[str]
    minimum_experience_years: int
    preferred_skills: list[str]
    nice_to_have_skills: list[str]
    minimum_education: str


class ScoringCriteria(TypedDict):
    """Weighted scoring criteria for different roles."""
    required_skills_weight: float
    preferred_skills_weight: float
    experience_weight: float
    education_weight: float
    soft_skills_weight: float


# ============================================================================
# Marketing Roles
# ============================================================================

DIGITAL_MARKETING_MANAGER: JobRequirements = {
    "title": "Digital Marketing Manager",
    "required_skills": [
        "Digital Marketing Strategy",
        "Google Analytics",
        "Content Marketing",
        "Email Marketing"
    ],
    "minimum_experience_years": 5,
    "preferred_skills": [
        "Marketing Automation",
        "SEO",
        "A/B Testing",
        "Data Analysis",
        "Social Media Marketing"
    ],
    "nice_to_have_skills": [
        "Python",
        "Figma",
        "Salesforce",
        "CRM",
        "Paid Advertising"
    ],
    "minimum_education": "Bachelor's Degree"
}

SOCIAL_MEDIA_MANAGER: JobRequirements = {
    "title": "Social Media Manager",
    "required_skills": [
        "Social Media Marketing",
        "Content Creation",
        "Community Management",
        "Platform Analytics"
    ],
    "minimum_experience_years": 2,
    "preferred_skills": [
        "Copywriting",
        "Graphic Design",
        "Video Editing",
        "A/B Testing",
        "Social Media Strategy"
    ],
    "nice_to_have_skills": [
        "Influencer Relations",
        "Crisis Management",
        "Scheduling Tools",
        "Paid Social Ads",
        "Photography"
    ],
    "minimum_education": "High School or Certificate"
}

CONTENT_STRATEGIST: JobRequirements = {
    "title": "Content Strategist",
    "required_skills": [
        "Content Strategy",
        "SEO",
        "Copywriting",
        "Editorial Planning"
    ],
    "minimum_experience_years": 3,
    "preferred_skills": [
        "Analytics",
        "User Research",
        "Content Management Systems",
        "Audience Segmentation",
        "Project Management"
    ],
    "nice_to_have_skills": [
        "Video Scripting",
        "Graphic Design",
        "Publishing Platforms",
        "Keyword Research Tools",
        "Marketing Automation"
    ],
    "minimum_education": "Bachelor's Degree"
}

SEO_SPECIALIST: JobRequirements = {
    "title": "SEO Specialist",
    "required_skills": [
        "SEO",
        "Keyword Research",
        "Technical SEO",
        "Analytics"
    ],
    "minimum_experience_years": 3,
    "preferred_skills": [
        "Link Building",
        "Content Optimization",
        "Google Search Console",
        "Schema Markup",
        "Competitor Analysis"
    ],
    "nice_to_have_skills": [
        "Python",
        "HTML/CSS",
        "JavaScript Basics",
        "SEO Tools",
        "Report Writing"
    ],
    "minimum_education": "High School or Certificate"
}

PPC_SPECIALIST: JobRequirements = {
    "title": "PPC Specialist",
    "required_skills": [
        "Google Ads",
        "Paid Advertising",
        "Analytics",
        "Campaign Management"
    ],
    "minimum_experience_years": 2,
    "preferred_skills": [
        "Facebook Ads",
        "LinkedIn Ads",
        "A/B Testing",
        "Conversion Tracking",
        "Budget Management"
    ],
    "nice_to_have_skills": [
        "Python",
        "Data Analysis",
        "Tag Management",
        "CRM Integration",
        "Marketing Automation"
    ],
    "minimum_education": "High School or Certificate"
}

# ============================================================================
# Design Roles
# ============================================================================

GRAPHIC_DESIGNER: JobRequirements = {
    "title": "Graphic Designer",
    "required_skills": [
        "Graphic Design",
        "Adobe Creative Suite",
        "Visual Communication",
        "Layout Design"
    ],
    "minimum_experience_years": 2,
    "preferred_skills": [
        "UX/UI Design",
        "Figma",
        "Branding",
        "Web Design",
        "Typography"
    ],
    "nice_to_have_skills": [
        "Adobe XD",
        "Sketch",
        "Illustration",
        "Motion Graphics",
        "HTML/CSS Basics"
    ],
    "minimum_education": "High School or Certificate"
}

WEB_DESIGNER: JobRequirements = {
    "title": "Web Designer",
    "required_skills": [
        "Web Design",
        "Figma",
        "Responsive Design",
        "User Experience"
    ],
    "minimum_experience_years": 3,
    "preferred_skills": [
        "Adobe XD",
        "Prototyping",
        "Wireframing",
        "HTML/CSS",
        "JavaScript Basics"
    ],
    "nice_to_have_skills": [
        "Interaction Design",
        "Accessibility",
        "Design Systems",
        "Motion Design",
        "CMS Knowledge"
    ],
    "minimum_education": "High School or Certificate"
}

# ============================================================================
# Development Roles
# ============================================================================

FRONTEND_DEVELOPER: JobRequirements = {
    "title": "Frontend Developer",
    "required_skills": [
        "JavaScript",
        "HTML",
        "CSS",
        "React"
    ],
    "minimum_experience_years": 3,
    "preferred_skills": [
        "TypeScript",
        "Vue.js",
        "REST API",
        "Git",
        "Testing"
    ],
    "nice_to_have_skills": [
        "Next.js",
        "Webpack",
        "GraphQL",
        "Accessibility",
        "Performance Optimization"
    ],
    "minimum_education": "Bachelor's Degree"
}

BACKEND_DEVELOPER: JobRequirements = {
    "title": "Backend Developer",
    "required_skills": [
        "Python",
        "SQL",
        "API Development",
        "Database Design"
    ],
    "minimum_experience_years": 3,
    "preferred_skills": [
        "Django",
        "FastAPI",
        "REST APIs",
        "Git",
        "Cloud Services"
    ],
    "nice_to_have_skills": [
        "Docker",
        "Kubernetes",
        "Redis",
        "GraphQL",
        "Microservices"
    ],
    "minimum_education": "Bachelor's Degree"
}

# ============================================================================
# Scoring Weights by Role
# ============================================================================

# For roles where hard skills are critical (development, design)
TECHNICAL_ROLE_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.45,
    "preferred_skills_weight": 0.25,
    "experience_weight": 0.15,
    "education_weight": 0.05,
    "soft_skills_weight": 0.10
}

# For marketing roles where balance is key
MARKETING_ROLE_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.35,
    "preferred_skills_weight": 0.20,
    "experience_weight": 0.25,
    "education_weight": 0.10,
    "soft_skills_weight": 0.10
}

# For management roles where soft skills matter
MANAGEMENT_ROLE_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.30,
    "preferred_skills_weight": 0.15,
    "experience_weight": 0.25,
    "education_weight": 0.15,
    "soft_skills_weight": 0.15
}

# Entry-level friendly weights
ENTRY_LEVEL_WEIGHTS: ScoringCriteria = {
    "required_skills_weight": 0.25,
    "preferred_skills_weight": 0.15,
    "experience_weight": 0.15,
    "education_weight": 0.25,
    "soft_skills_weight": 0.20
}

# ============================================================================
# Job Catalog
# ============================================================================

JOBS = {
    # Marketing
    "digital_marketing_manager": DIGITAL_MARKETING_MANAGER,
    "social_media_manager": SOCIAL_MEDIA_MANAGER,
    "content_strategist": CONTENT_STRATEGIST,
    "seo_specialist": SEO_SPECIALIST,
    "ppc_specialist": PPC_SPECIALIST,

    # Design
    "graphic_designer": GRAPHIC_DESIGNER,
    "web_designer": WEB_DESIGNER,

    # Development
    "frontend_developer": FRONTEND_DEVELOPER,
    "backend_developer": BACKEND_DEVELOPER,
}

WEIGHTS = {
    "technical": TECHNICAL_ROLE_WEIGHTS,
    "marketing": MARKETING_ROLE_WEIGHTS,
    "management": MANAGEMENT_ROLE_WEIGHTS,
    "entry_level": ENTRY_LEVEL_WEIGHTS,
}

# ============================================================================
# Usage Examples
# ============================================================================

"""
Example: Screen candidate for Digital Marketing Manager

from job_config_template import JOBS, WEIGHTS
from candidate_screener import screen_candidate

resume_text = open("resume.txt").read()
job = JOBS['digital_marketing_manager']
weights = WEIGHTS['marketing']

report = screen_candidate(resume_text, job, weights)
"""

"""
Example: Screen multiple candidates for different roles

from job_config_template import JOBS, WEIGHTS
from candidate_screener import screen_candidate
import json

candidates = [
    ("resume1.txt", "digital_marketing_manager"),
    ("resume2.txt", "social_media_manager"),
    ("resume3.txt", "seo_specialist"),
]

results = []
for resume_path, job_key in candidates:
    with open(resume_path) as f:
        resume_text = f.read()

    job = JOBS[job_key]
    weights = WEIGHTS['marketing']

    report = screen_candidate(resume_text, job, weights)
    results.append(report)

# Save all results
with open("screening_results.json", "w") as f:
    json.dump([to_json(r) for r in results], f, indent=2)
"""

"""
Example: Create a custom job profile

from job_config_template import JobRequirements

MY_CUSTOM_ROLE: JobRequirements = {
    "title": "Marketing Analyst",
    "required_skills": [
        "Data Analysis",
        "Google Analytics",
        "Excel",
        "Marketing Knowledge"
    ],
    "minimum_experience_years": 2,
    "preferred_skills": [
        "Python",
        "SQL",
        "Tableau",
        "Statistical Analysis"
    ],
    "nice_to_have_skills": [
        "R",
        "Power BI",
        "Machine Learning",
        "A/B Testing"
    ],
    "minimum_education": "Bachelor's Degree"
}
"""
