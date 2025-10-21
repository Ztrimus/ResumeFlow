'''
-----------------------------------------------------------------------
File: unseen_questions.py
Creation Time: Oct 20th 2025
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2025 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class UnseenQuestionsHandler:
    """
    Handles unseen questions encountered during Easy Apply process.
    Stores questions and allows for manual answers to be added.
    """
    
    def __init__(self, file_path: str = "output/unseen_questions.json"):
        self.file_path = file_path
        self.unseen_questions = self._load_unseen_questions()
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Ensure the output directory exists."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def _load_unseen_questions(self) -> Dict:
        """Load existing unseen questions from file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {
            "questions": {},
            "last_updated": None,
            "total_questions": 0
        }
    
    def _save_unseen_questions(self):
        """Save unseen questions to file."""
        self.unseen_questions["last_updated"] = datetime.now().isoformat()
        self.unseen_questions["total_questions"] = len(self.unseen_questions["questions"])
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.unseen_questions, f, indent=2, ensure_ascii=False)
    
    def add_unseen_question(self, question: str, question_type: str, options: List[str] = None, context: str = None) -> str:
        """
        Add a new unseen question and return a default answer.
        
        Args:
            question (str): The question text
            question_type (str): Type of question (text, yes_no, multiple_choice, etc.)
            options (List[str]): Available options for multiple choice questions
            context (str): Additional context about the question
            
        Returns:
            str: Default answer for the question
        """
        question_key = self._normalize_question(question)
        
        if question_key not in self.unseen_questions["questions"]:
            self.unseen_questions["questions"][question_key] = {
                "original_question": question,
                "question_type": question_type,
                "options": options or [],
                "context": context or "",
                "first_encountered": datetime.now().isoformat(),
                "encounter_count": 1,
                "suggested_answer": self._get_default_answer(question_type),
                "manual_answer": None,
                "status": "unanswered"
            }
            print(f"📝 New unseen question added: {question}")
        else:
            # Update encounter count
            self.unseen_questions["questions"][question_key]["encounter_count"] += 1
            print(f"📝 Question encountered again: {question}")
        
        self._save_unseen_questions()
        
        # Return the suggested or manual answer
        question_data = self.unseen_questions["questions"][question_key]
        return question_data.get("manual_answer") or question_data.get("suggested_answer", "Yes")
    
    def _normalize_question(self, question: str) -> str:
        """Normalize question text for consistent storage."""
        return question.strip().lower().replace("?", "").replace(":", "")
    
    def _get_default_answer(self, question_type: str) -> str:
        """Get default answer based on question type."""
        defaults = {
            "text": "Please see my resume for details.",
            "yes_no": "Yes",
            "multiple_choice": "Other",
            "number": "1",
            "date": "01/01/2024",
            "email": "saurabhzinjad@gmail.com",
            "phone": "+1234567890"
        }
        return defaults.get(question_type, "Yes")
    
    def update_question_answer(self, question: str, answer: str):
        """
        Update the manual answer for a question.
        
        Args:
            question (str): The question text
            answer (str): The manual answer
        """
        question_key = self._normalize_question(question)
        
        if question_key in self.unseen_questions["questions"]:
            self.unseen_questions["questions"][question_key]["manual_answer"] = answer
            self.unseen_questions["questions"][question_key]["status"] = "answered"
            self._save_unseen_questions()
            print(f"✅ Updated answer for: {question}")
        else:
            print(f"❌ Question not found: {question}")
    
    def get_question_answer(self, question: str) -> str:
        """
        Get the answer for a question (manual or default).
        
        Args:
            question (str): The question text
            
        Returns:
            str: The answer for the question
        """
        question_key = self._normalize_question(question)
        
        if question_key in self.unseen_questions["questions"]:
            question_data = self.unseen_questions["questions"][question_key]
            return question_data.get("manual_answer") or question_data.get("suggested_answer", "Yes")
        
        return "Yes"  # Default fallback
    
    def get_unanswered_questions(self) -> List[Dict]:
        """Get list of unanswered questions."""
        unanswered = []
        for question_data in self.unseen_questions["questions"].values():
            if question_data.get("status") == "unanswered":
                unanswered.append(question_data)
        return unanswered
    
    def get_question_stats(self) -> Dict:
        """Get statistics about unseen questions."""
        total = len(self.unseen_questions["questions"])
        answered = sum(1 for q in self.unseen_questions["questions"].values() 
                      if q.get("status") == "answered")
        unanswered = total - answered
        
        return {
            "total_questions": total,
            "answered_questions": answered,
            "unanswered_questions": unanswered,
            "last_updated": self.unseen_questions.get("last_updated")
        }
    
    def export_questions_for_review(self, output_file: str = "output/questions_for_review.md"):
        """Export questions in a markdown format for easy review."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Unseen Questions Review\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            stats = self.get_question_stats()
            f.write(f"## Statistics\n")
            f.write(f"- Total Questions: {stats['total_questions']}\n")
            f.write(f"- Answered: {stats['answered_questions']}\n")
            f.write(f"- Unanswered: {stats['unanswered_questions']}\n\n")
            
            f.write("## Questions\n\n")
            
            for i, (question_key, question_data) in enumerate(self.unseen_questions["questions"].items(), 1):
                f.write(f"### {i}. {question_data['original_question']}\n")
                f.write(f"**Type:** {question_data['question_type']}\n")
                f.write(f"**Context:** {question_data.get('context', 'N/A')}\n")
                f.write(f"**Encountered:** {question_data['encounter_count']} times\n")
                f.write(f"**Status:** {question_data.get('status', 'unanswered')}\n")
                
                if question_data.get('options'):
                    f.write(f"**Options:** {', '.join(question_data['options'])}\n")
                
                f.write(f"**Suggested Answer:** {question_data.get('suggested_answer', 'N/A')}\n")
                
                if question_data.get('manual_answer'):
                    f.write(f"**Manual Answer:** {question_data['manual_answer']}\n")
                
                f.write("\n---\n\n")
        
        print(f"📄 Questions exported to: {output_file}")
    
    def print_summary(self):
        """Print a summary of unseen questions."""
        stats = self.get_question_stats()
        print(f"\n📊 Unseen Questions Summary:")
        print(f"   Total Questions: {stats['total_questions']}")
        print(f"   Answered: {stats['answered_questions']}")
        print(f"   Unanswered: {stats['unanswered_questions']}")
        print(f"   Last Updated: {stats['last_updated']}")
        
        if stats['unanswered_questions'] > 0:
            print(f"\n❓ Unanswered Questions:")
            for question_data in self.get_unanswered_questions():
                print(f"   - {question_data['original_question']}")
                print(f"     Type: {question_data['question_type']}")
                print(f"     Encountered: {question_data['encounter_count']} times")
                print()
