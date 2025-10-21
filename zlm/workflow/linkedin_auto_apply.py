'''
-----------------------------------------------------------------------
File: linkedin_auto_apply.py
Creation Time: Oct 20th 2025
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2025 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

import os
import csv
import time
from datetime import datetime
from typing import List, Dict
from .browser_utils import LinkedInBrowser
from .form_handler import EasyApplyFormHandler
from .linkedin_config import (
    SEARCH_TERMS, MAX_APPLICATIONS, OUTPUT_DIR, CSV_FILE, FAILED_CSV
)


class LinkedInAutoApply:
    """
    Main orchestrator for LinkedIn Easy Apply automation workflow.
    """
    
    def __init__(self):
        self.browser = LinkedInBrowser()
        self.form_handler = None
        self.applied_jobs = []
        self.failed_jobs = []
        self._setup_output_files()
    
    def _setup_output_files(self):
        """Create CSV files for tracking applications."""
        try:
            # Create applied jobs CSV
            applied_csv_path = os.path.join(OUTPUT_DIR, CSV_FILE)
            if not os.path.exists(applied_csv_path):
                with open(applied_csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Job ID', 'Title', 'Company', 'Location', 'Job Link',
                        'Date Applied', 'Status', 'Error Message'
                    ])
            
            # Create failed jobs CSV
            failed_csv_path = os.path.join(OUTPUT_DIR, FAILED_CSV)
            if not os.path.exists(failed_csv_path):
                with open(failed_csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Job ID', 'Title', 'Company', 'Location', 'Job Link',
                        'Date Failed', 'Status', 'Error Message'
                    ])
                    
        except Exception as e:
            print(f"⚠️ Error setting up output files: {e}")
    
    def run_automation(self) -> bool:
        """
        Run the complete LinkedIn Easy Apply automation workflow.
        
        Returns:
            bool: True if automation completed successfully
        """
        try:
            print("🚀 Starting LinkedIn Easy Apply Automation")
            print("=" * 50)
            
            # Start browser
            if not self.browser.start_browser():
                print("❌ Failed to start browser")
                return False
            
            # Login to LinkedIn
            if not self.browser.login_to_linkedin():
                print("❌ Failed to login to LinkedIn")
                return False
            
            # Process each search term
            for search_term in SEARCH_TERMS:
                print(f"\n🔍 Processing search term: {search_term}")
                print("-" * 30)
                
                if not self._process_search_term(search_term):
                    print(f"⚠️ Failed to process search term: {search_term}")
                    continue
            
            # Print summary
            self._print_summary()
            
            print("\n✅ Automation completed!")
            return True
            
        except Exception as e:
            print(f"❌ Automation failed: {e}")
            return False
        
        finally:
            # Always close browser
            self.browser.close_browser()
    
    def _process_search_term(self, search_term: str) -> bool:
        """
        Process a single search term and apply to jobs one by one.
        
        Args:
            search_term (str): Job title to search for
            
        Returns:
            bool: True if processing completed successfully
        """
        try:
            # Navigate to jobs page
            if not self.browser.navigate_to_jobs(search_term):
                return False
            
            # Get job listings
            jobs = self.browser.get_job_listings()
            if not jobs:
                print("❌ No jobs found")
                return False
            
            print(f"📋 Found {len(jobs)} job listings")
            
            # Apply to jobs one by one (up to MAX_APPLICATIONS)
            applications_count = 0
            for job_index, job in enumerate(jobs):
                if applications_count >= MAX_APPLICATIONS:
                    print(f"⏹️ Reached maximum applications limit ({MAX_APPLICATIONS})")
                    break
                
                print(f"\n📝 Processing job {job_index + 1}: {job['title']} at {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Has Easy Apply: {job.get('has_easy_apply', False)}")
                
                # Skip if no Easy Apply
                if not job.get('has_easy_apply', False):
                    print(f"⏭️ Skipping job {job_index + 1} - No Easy Apply option available")
                    continue
                
                # Apply to this specific job using the job index
                success = self._apply_to_job_by_index(job_index, job)
                
                if success:
                    applications_count += 1
                    print(f"✅ Application {applications_count} completed successfully")
                else:
                    print(f"❌ Application {applications_count + 1} failed")
                
                # Wait between applications to avoid being flagged
                print("⏳ Waiting before next application...")
                time.sleep(5)  # Increased delay between applications
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing search term '{search_term}': {e}")
            return False
    
    def _apply_to_job_by_index(self, job_index: int, job_info: Dict) -> bool:
        """
        Apply to a specific job using Easy Apply by job index (stays on same page).
        
        Args:
            job_index (int): Index of the job in the current listings
            job_info (Dict): Information about the job
            
        Returns:
            bool: True if application successful
        """
        try:
            # Initialize form handler
            self.form_handler = EasyApplyFormHandler(self.browser.page)
            
            # Process complete Easy Apply workflow using job index
            success, error_message = self.form_handler.process_easy_apply_by_index(job_index, job_info)
            
            if success:
                self._log_applied_job(job_info)
                return True
            else:
                self._log_failed_job(job_info, error_message)
                return False
                
        except Exception as e:
            error_msg = f"Application error: {str(e)}"
            print(f"❌ {error_msg}")
            self._log_failed_job(job_info, error_msg)
            return False
    
    def _apply_to_job(self, job_info: Dict) -> bool:
        """
        Apply to a specific job using Easy Apply.
        
        Args:
            job_info (Dict): Information about the job
            
        Returns:
            bool: True if application successful
        """
        try:
            # Initialize form handler
            self.form_handler = EasyApplyFormHandler(self.browser.page)
            
            # Process complete Easy Apply workflow
            success, error_message = self.form_handler.process_easy_apply(job_info)
            
            if success:
                self._log_applied_job(job_info)
                return True
            else:
                self._log_failed_job(job_info, error_message)
                return False
                
        except Exception as e:
            error_msg = f"Application error: {str(e)}"
            print(f"❌ {error_msg}")
            self._log_failed_job(job_info, error_msg)
            return False
    
    def _log_applied_job(self, job_info: Dict):
        """Log a successfully applied job to CSV."""
        try:
            job_id = f"job_{int(time.time())}"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            applied_job = {
                'Job ID': job_id,
                'Title': job_info['title'],
                'Company': job_info['company'],
                'Location': job_info['location'],
                'Job Link': job_info['link'],
                'Date Applied': current_time,
                'Status': 'Applied',
                'Error Message': ''
            }
            
            self.applied_jobs.append(applied_job)
            
            # Write to CSV
            csv_path = os.path.join(OUTPUT_DIR, CSV_FILE)
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    applied_job['Job ID'], applied_job['Title'], applied_job['Company'],
                    applied_job['Location'], applied_job['Job Link'], applied_job['Date Applied'],
                    applied_job['Status'], applied_job['Error Message']
                ])
            
            print(f"📝 Logged applied job: {job_info['title']}")
            
        except Exception as e:
            print(f"⚠️ Error logging applied job: {e}")
    
    def _log_failed_job(self, job_info: Dict, error_message: str):
        """Log a failed job application to CSV."""
        try:
            job_id = f"job_{int(time.time())}"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            failed_job = {
                'Job ID': job_id,
                'Title': job_info['title'],
                'Company': job_info['company'],
                'Location': job_info['location'],
                'Job Link': job_info['link'],
                'Date Failed': current_time,
                'Status': 'Failed',
                'Error Message': error_message
            }
            
            self.failed_jobs.append(failed_job)
            
            # Write to CSV
            csv_path = os.path.join(OUTPUT_DIR, FAILED_CSV)
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    failed_job['Job ID'], failed_job['Title'], failed_job['Company'],
                    failed_job['Location'], failed_job['Job Link'], failed_job['Date Failed'],
                    failed_job['Status'], failed_job['Error Message']
                ])
            
            print(f"📝 Logged failed job: {job_info['title']} - {error_message}")
            
        except Exception as e:
            print(f"⚠️ Error logging failed job: {e}")
    
    def _print_summary(self):
        """Print a summary of the automation results."""
        print("\n" + "=" * 50)
        print("📊 AUTOMATION SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully applied: {len(self.applied_jobs)} jobs")
        print(f"❌ Failed applications: {len(self.failed_jobs)} jobs")
        print(f"📁 Output directory: {OUTPUT_DIR}")
        
        if self.applied_jobs:
            print("\n✅ APPLIED JOBS:")
            for job in self.applied_jobs:
                print(f"  • {job['Title']} at {job['Company']}")
        
        if self.failed_jobs:
            print("\n❌ FAILED JOBS:")
            for job in self.failed_jobs:
                print(f"  • {job['Title']} at {job['Company']} - {job['Error Message']}")
        
        # Export unseen questions for review
        if hasattr(self, 'form_handler') and self.form_handler:
            print("\n📝 Unseen Questions Summary:")
            self.form_handler.export_unseen_questions()


def main():
    """
    Main entry point for the LinkedIn Easy Apply automation.
    """
    print("🤖 LinkedIn Easy Apply Automation")
    print("=" * 40)
    
    # Check configuration
    from .linkedin_config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
    
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("❌ LinkedIn credentials not configured!")
        print("Please update linkedin_config.py with your credentials.")
        return
    
    # Run automation
    automation = LinkedInAutoApply()
    success = automation.run_automation()
    
    if success:
        print("\n🎉 Automation completed successfully!")
    else:
        print("\n💥 Automation failed. Check the logs for details.")


if __name__ == "__main__":
    main()
