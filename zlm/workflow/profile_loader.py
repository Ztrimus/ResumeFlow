'''
-----------------------------------------------------------------------
File: profile_loader.py
Creation Time: Oct 20th 2025
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2025 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

import json
import os
from typing import Dict, List, Any
from datetime import datetime

class ProfileLoader:
    """
    Loads and manages user profile data for LinkedIn Easy Apply automation.
    Extracts information from existing user_profile.json and provides Easy Apply answers.
    """
    
    def __init__(self, profile_path: str = "zlm/demo_data/enhanced_user_profile.json"):
        self.profile_path = profile_path
        self.profile_data = self._load_profile()
        self.easy_apply_answers = self._generate_easy_apply_answers()
        self.question_patterns = self._get_question_patterns()
        self.default_answers = self._get_default_answers()
    
    def _load_profile(self) -> Dict:
        """Load user profile from JSON file."""
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Profile file not found: {self.profile_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing profile JSON: {e}")
            return {}
    
    def _generate_easy_apply_answers(self) -> Dict[str, str]:
        """Generate Easy Apply answers based on profile data."""
        # Check if enhanced profile has easy_apply_answers
        if "easy_apply_answers" in self.profile_data:
            return self.profile_data["easy_apply_answers"]
        
        # Fallback to generated answers
        # Calculate years of experience
        total_years = self._calculate_total_experience()
        python_years = self._calculate_python_experience()
        ml_years = self._calculate_ml_experience()
        
        # Get current role
        current_role = self._get_current_role()
        
        # Get skills
        all_skills = self._get_all_skills()
        
        # Get education
        highest_degree = self._get_highest_degree()
        
        return {
            # Basic Information
            "What is your phone number?": self.profile_data.get("phone", ""),
            "What is your email address?": self.profile_data.get("email", ""),
            "What is your current location?": self._get_current_location(),
            "How many years of experience do you have?": str(total_years),
            "How many years of experience do you have in [specific field]?": str(total_years),
            
            # Work Authorization
            "Are you authorized to work in the United States?": "Yes",
            "Do you require visa sponsorship?": "No",
            "Are you willing to relocate?": "Yes",
            "Are you open to remote work?": "Yes",
            
            # Experience Questions
            "How many years of experience do you have in Python?": str(python_years),
            "How many years of experience do you have in Machine Learning?": str(ml_years),
            "How many years of experience do you have in AI?": str(ml_years),
            "How many years of experience do you have in Software Development?": str(total_years),
            "How many years of experience do you have in Data Science?": str(ml_years),
            "How many years of experience do you have in Cloud Computing?": "3",
            "How many years of experience do you have in DevOps?": "2",
            
            # Availability
            "When can you start?": "Immediate",
            "What is your notice period?": "2 weeks",
            "Are you available for full-time work?": "Yes",
            "Are you available for contract work?": "Yes",
            "Are you available for part-time work?": "No",
            
            # Skills and Technologies
            "Do you have experience with Python?": "Yes",
            "Do you have experience with Machine Learning?": "Yes",
            "Do you have experience with AI?": "Yes",
            "Do you have experience with Deep Learning?": "Yes",
            "Do you have experience with TensorFlow?": "Yes",
            "Do you have experience with PyTorch?": "Yes",
            "Do you have experience with AWS?": "Yes",
            "Do you have experience with Docker?": "Yes",
            "Do you have experience with Git?": "Yes",
            "Do you have experience with React?": "Yes",
            "Do you have experience with Node.js?": "Yes",
            "Do you have experience with PostgreSQL?": "Yes",
            "Do you have experience with MongoDB?": "Yes",
            "Do you have experience with Kubernetes?": "Yes",
            "Do you have experience with LangChain?": "Yes",
            "Do you have experience with MLOps?": "Yes",
            
            # Education
            "What is your highest level of education?": highest_degree,
            "What is your GPA?": "3.8",
            "When did you graduate?": "2025",
            "What university did you attend?": "Arizona State University",
            
            # Salary and Benefits
            "What is your salary expectation?": "Competitive",
            "What is your current salary?": "Confidential",
            "What benefits are you looking for?": "Standard benefits package",
            "What is your expected salary range?": "Competitive based on role and location",
            
            # Company-specific questions
            "Why do you want to work at this company?": "I am excited about the opportunity to contribute to innovative AI projects and grow with a dynamic team that values cutting-edge technology.",
            "What interests you about this role?": "The opportunity to work on cutting-edge AI/ML technology and solve complex problems that have real-world impact.",
            "How did you hear about this position?": "LinkedIn",
            "Do you have any questions for us?": "I would like to learn more about the team structure, growth opportunities, and the company's AI/ML roadmap.",
            "What makes you a good fit for this role?": f"I bring {total_years} years of experience in AI/ML with expertise in {', '.join(all_skills[:5])} and a proven track record of delivering production-ready solutions.",
            
            # Technical Questions
            "Describe your experience with [technology]": f"I have {total_years} years of experience with {', '.join(all_skills[:3])} and have worked on various AI/ML projects including research publications and production systems.",
            "What is your experience with cloud platforms?": f"I have experience with AWS, GCP, and Azure, having deployed and managed AI/ML models and data pipelines in cloud environments.",
            "Describe a challenging project you worked on": "I developed a multimodal AI system for media search that achieved 92% faster search speeds using AWS, CLIP, and vector databases, winning the Big Data Prize.",
            "What is your experience with MLOps?": "I have extensive experience with MLOps including model monitoring, CI/CD pipelines, and deployment strategies using tools like MLflow, Docker, and Kubernetes.",
            "Describe your experience with LLMs": "I have worked extensively with LLMs including fine-tuning, RAG systems, and prompt engineering, with published research on LLM safety and personalized resume generation.",
            
            # Behavioral Questions
            "Tell me about yourself": f"I am a {current_role} with {total_years} years of experience in AI/ML and software development. I am passionate about building production-ready AI systems and have published research in top-tier conferences.",
            "What are your strengths?": "Strong problem-solving skills, expertise in AI/ML frameworks, and ability to work in fast-paced environments. I have a proven track record of delivering impactful solutions.",
            "What are your weaknesses?": "I sometimes spend too much time perfecting details, but I'm working on balancing perfectionism with efficiency to deliver faster results.",
            "Where do you see yourself in 5 years?": "I see myself as a senior AI/ML engineer or AI team lead, contributing to innovative AI products and mentoring junior developers while continuing to advance the field through research.",
            "What motivates you?": "I am motivated by the opportunity to solve complex problems using AI/ML and create solutions that have real-world impact. I enjoy the challenge of building production-ready systems.",
            
            # Yes/No Questions
            "Are you willing to work overtime?": "Yes",
            "Are you willing to travel?": "Yes",
            "Do you have a valid driver's license?": "Yes",
            "Are you comfortable with public speaking?": "Yes",
            "Do you have any criminal convictions?": "No",
            "Are you currently employed?": "Yes",
            "Are you looking for a new opportunity?": "Yes",
            "Do you have any conflicts of interest?": "No",
            "Are you willing to relocate?": "Yes",
            "Are you open to remote work?": "Yes",
            "Do you have experience with team leadership?": "Yes",
            "Are you comfortable with mentoring?": "Yes"
        }
    
    def _calculate_total_experience(self) -> int:
        """Calculate total years of experience from work history."""
        try:
            work_experience = self.profile_data.get("work_experience", [])
            if not work_experience:
                return 6  # Default based on profile
            
            # Calculate from first job to present
            first_job = work_experience[-1]  # Last in list is earliest
            start_date = first_job.get("from_date", "")
            
            if "2019" in start_date:
                return 6
            elif "2020" in start_date:
                return 5
            else:
                return 6  # Default
        except:
            return 6
    
    def _calculate_python_experience(self) -> int:
        """Calculate years of Python experience."""
        try:
            work_experience = self.profile_data.get("work_experience", [])
            python_years = 0
            
            for job in work_experience:
                description = " ".join(job.get("description", []))
                if "Python" in description:
                    python_years += 1
            
            return max(python_years, 6)  # At least 6 years based on profile
        except:
            return 6
    
    def _calculate_ml_experience(self) -> int:
        """Calculate years of ML experience."""
        try:
            work_experience = self.profile_data.get("work_experience", [])
            ml_years = 0
            
            for job in work_experience:
                description = " ".join(job.get("description", []))
                if any(keyword in description.lower() for keyword in ["machine learning", "ml", "ai", "deep learning", "neural", "tensorflow", "pytorch"]):
                    ml_years += 1
            
            return max(ml_years, 5)  # At least 5 years based on profile
        except:
            return 5
    
    def _get_current_role(self) -> str:
        """Get current role from work experience."""
        try:
            work_experience = self.profile_data.get("work_experience", [])
            if work_experience:
                current_job = work_experience[0]  # First is most recent
                return current_job.get("role", "AI/ML Engineer")
            return "AI/ML Engineer"
        except:
            return "AI/ML Engineer"
    
    def _get_current_location(self) -> str:
        """Get current location from work experience."""
        try:
            work_experience = self.profile_data.get("work_experience", [])
            if work_experience:
                current_job = work_experience[0]  # First is most recent
                return current_job.get("location", "United States")
            return "United States"
        except:
            return "United States"
    
    def _get_all_skills(self) -> List[str]:
        """Get all skills from skill_section."""
        try:
            skill_sections = self.profile_data.get("skill_section", [])
            all_skills = []
            
            for section in skill_sections:
                skills = section.get("skills", [])
                all_skills.extend(skills)
            
            return all_skills
        except:
            return ["Python", "Machine Learning", "AI", "TensorFlow", "PyTorch"]
    
    def _get_highest_degree(self) -> str:
        """Get highest degree from education."""
        try:
            education = self.profile_data.get("education", [])
            if education:
                return education[0].get("degree", "Masters of Science in Computer Science")
            return "Masters of Science in Computer Science"
        except:
            return "Masters of Science in Computer Science"
    
    def _get_question_patterns(self) -> Dict[str, List[str]]:
        """Get question patterns for dynamic matching."""
        # Check if enhanced profile has question_patterns
        if "question_patterns" in self.profile_data:
            return self.profile_data["question_patterns"]
        
        # Fallback to default patterns
        return {
            "phone": ["phone", "contact", "number", "mobile"],
            "email": ["email", "e-mail", "contact"],
            "experience": ["experience", "years", "how long", "background"],
            "location": ["location", "where", "city", "state"],
            "authorization": ["authorized", "work permit", "visa", "sponsorship"],
            "relocation": ["relocate", "move", "location", "remote"],
            "availability": ["start", "available", "when", "notice"],
            "salary": ["salary", "compensation", "pay", "rate", "expectation"],
            "education": ["education", "degree", "university", "college", "gpa"],
            "skills": ["experience with", "familiar with", "knowledge of", "proficient in"]
        }
    
    def _get_default_answers(self) -> Dict[str, str]:
        """Get default answers for unmatched questions."""
        # Check if enhanced profile has default_answers
        if "default_answers" in self.profile_data:
            return self.profile_data["default_answers"]
        
        # Fallback to default answers
        return {
            "text": "Please see my resume for details.",
            "yes_no": "Yes",
            "multiple_choice": "Other",
            "number": "1",
            "date": "01/01/2024"
        }
    
    def get_question_answer(self, question: str) -> str:
        """Get answer for a specific question."""
        # Direct match first
        if question in self.easy_apply_answers:
            return self.easy_apply_answers[question]
        
        # Pattern matching
        question_lower = question.lower()
        for pattern_key, keywords in self.question_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                if pattern_key == "phone":
                    return self.profile_data.get("phone", "")
                elif pattern_key == "email":
                    return self.profile_data.get("email", "")
                elif pattern_key == "experience":
                    return str(self._calculate_total_experience())
                elif pattern_key == "location":
                    return self._get_current_location()
                elif pattern_key == "authorization":
                    return "Yes"
                elif pattern_key == "relocation":
                    return "Yes"
                elif pattern_key == "availability":
                    return "Immediate"
                elif pattern_key == "salary":
                    return "Competitive"
                elif pattern_key == "education":
                    return self._get_highest_degree()
                elif pattern_key == "skills":
                    return "Yes"
        
        # Default fallback
        return "Yes"
    
    def get_personal_info(self) -> Dict[str, str]:
        """Get personal information for form filling."""
        return {
            "first_name": self.profile_data.get("name", "").split()[0],
            "last_name": " ".join(self.profile_data.get("name", "").split()[1:]),
            "email": self.profile_data.get("email", ""),
            "phone": self.profile_data.get("phone", ""),
            "location": self._get_current_location(),
            "linkedin_url": self.profile_data.get("media", {}).get("linkedin", ""),
            "github_url": self.profile_data.get("media", {}).get("github", ""),
            "portfolio_url": self.profile_data.get("media", {}).get("github", "")
        }
    
    def get_experience_info(self) -> Dict[str, str]:
        """Get experience information."""
        return {
            "total_years": str(self._calculate_total_experience()),
            "years_in_ml": str(self._calculate_ml_experience()),
            "years_in_ai": str(self._calculate_ml_experience()),
            "years_in_python": str(self._calculate_python_experience()),
            "years_in_software_development": str(self._calculate_total_experience()),
            "current_role": self._get_current_role(),
            "seniority_level": "Mid-Level"
        }
    
    def get_skills_info(self) -> Dict[str, List[str]]:
        """Get skills information."""
        return {
            "programming_languages": ["Python", "JavaScript", "C++", "SQL", "Java"],
            "ml_frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "LangChain"],
            "databases": ["PostgreSQL", "MongoDB", "MySQL"],
            "cloud_platforms": ["AWS", "Google Cloud", "Azure"],
            "tools": ["Git", "Docker", "Kubernetes", "MLflow"]
        }
    
    def get_documents_info(self) -> Dict[str, str]:
        """Get document paths."""
        # Check if enhanced profile has documents
        if "documents" in self.profile_data:
            return self.profile_data["documents"]
        
        # Fallback to default documents
        return {
            "resume_path": "zlm/demo_data/user_resume.pdf",
            "cover_letter_path": "resources/cover_letter.pdf",
            "portfolio_url": self.profile_data.get("media", {}).get("github", ""),
            "github_url": self.profile_data.get("media", {}).get("github", "")
        }
    
    def get_application_preferences(self) -> Dict[str, Any]:
        """Get application preferences."""
        # Check if enhanced profile has application_preferences
        if "application_preferences" in self.profile_data:
            return self.profile_data["application_preferences"]
        
        # Fallback to default preferences
        return {
            "max_applications_per_day": 10,
            "preferred_job_types": ["Full-time", "Contract"],
            "avoid_companies": [],
            "preferred_companies": [],
            "minimum_salary": 80000,
            "maximum_commute_time": 60,
            "remote_work_preference": "Hybrid"
        }
    
    def print_profile_summary(self):
        """Print a summary of the loaded profile."""
        print(f"\n📋 Profile Summary:")
        print(f"   Name: {self.profile_data.get('name', 'N/A')}")
        print(f"   Email: {self.profile_data.get('email', 'N/A')}")
        print(f"   Phone: {self.profile_data.get('phone', 'N/A')}")
        print(f"   Current Role: {self._get_current_role()}")
        print(f"   Total Experience: {self._calculate_total_experience()} years")
        print(f"   ML Experience: {self._calculate_ml_experience()} years")
        print(f"   Python Experience: {self._calculate_python_experience()} years")
        print(f"   Skills: {len(self._get_all_skills())} skills")
        print(f"   Easy Apply Answers: {len(self.easy_apply_answers)} questions")
