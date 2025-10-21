'''
-----------------------------------------------------------------------
File: browser_utils.py
Creation Time: Oct 20th 2025
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2025 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

import os
import time
import platform
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional, List, Dict, Tuple
from .linkedin_config import (
    LINKEDIN_EMAIL, LINKEDIN_PASSWORD, SEARCH_TERMS, SEARCH_LOCATION,
    HEADLESS, BROWSER_TIMEOUT, PAGE_LOAD_TIMEOUT, OUTPUT_DIR, 
    SCREENSHOTS_DIR, LINKEDIN_BASE_URL, LINKEDIN_JOBS_URL
)


class LinkedInBrowser:
    """
    Handles browser automation for LinkedIn Easy Apply workflow.
    """
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary output directories."""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(os.path.join(OUTPUT_DIR, SCREENSHOTS_DIR), exist_ok=True)
    
    def _get_screen_resolution(self) -> Tuple[int, int]:
        """
        Get the screen resolution dynamically based on the operating system.
        
        Returns:
            Tuple[int, int]: (width, height) of the screen
        """
        system = platform.system()
        
        # macOS - Use AppKit for direct access to screen frame
        if system == "Darwin":
            try:
                from AppKit import NSScreen
                frame = NSScreen.mainScreen().frame()
                width = int(frame.size.width)
                height = int(frame.size.height)
                print(f"🖥️ Detected macOS resolution: {width}x{height}")
                return width, height
            except ImportError:
                print("⚠️ AppKit not available, trying alternative method...")
                return self._get_screen_resolution_fallback()
            except Exception as e:
                print(f"⚠️ macOS resolution detection failed: {e}")
                return self._get_screen_resolution_fallback()
        
        # Windows - Use wmic command
        elif system == "Windows":
            try:
                import subprocess
                result = subprocess.run([
                    'wmic', 'path', 'Win32_VideoController', 'get', 
                    'CurrentHorizontalResolution,CurrentVerticalResolution', '/format:value'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    width, height = None, None
                    for line in lines:
                        if 'CurrentHorizontalResolution=' in line:
                            width = int(line.split('=')[1].strip())
                        elif 'CurrentVerticalResolution=' in line:
                            height = int(line.split('=')[1].strip())
                    
                    if width and height:
                        print(f"🖥️ Detected Windows resolution: {width}x{height}")
                        return width, height
            except Exception as e:
                print(f"⚠️ Windows resolution detection failed: {e}")
        
        # Linux - Use xrandr command
        elif system == "Linux":
            try:
                import subprocess
                result = subprocess.run(['xrandr'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '*' in line and 'x' in line:
                            parts = line.split()
                            for part in parts:
                                if 'x' in part and '*' in part:
                                    resolution = part.replace('*', '').split('+')[0]
                                    if 'x' in resolution:
                                        width, height = resolution.split('x')
                                        width = int(width.strip())
                                        height = int(height.strip())
                                        print(f"🖥️ Detected Linux resolution: {width}x{height}")
                                        return width, height
            except Exception as e:
                print(f"⚠️ Linux resolution detection failed: {e}")
        
        # Fallback to default resolution
        print("⚠️ Using fallback screen resolution")
        return 1920, 1080
    
    def _get_screen_resolution_fallback(self) -> Tuple[int, int]:
        """
        Fallback method for macOS when AppKit is not available.
        
        Returns:
            Tuple[int, int]: (width, height) of the screen
        """
        try:
            import subprocess
            # Use osascript as fallback for macOS
            script = '''
            tell application "System Events"
                set screenResolution to size of desktop
                return (item 1 of screenResolution) & "x" & (item 2 of screenResolution)
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                effective_resolution = result.stdout.strip()
                if 'x' in effective_resolution:
                    width, height = effective_resolution.split('x')
                    width = int(width.strip())
                    height = int(height.strip())
                    print(f"🖥️ Detected macOS resolution (fallback): {width}x{height}")
                    return width, height
        except Exception as e:
            print(f"⚠️ Fallback resolution detection failed: {e}")
        
        return 1920, 1080
    
    def _wait_for_page_load(self, timeout=10000):
        """
        Wait for page to load with multiple fallback approaches.
        
        Args:
            timeout (int): Timeout in milliseconds
        """
        try:
            # Try domcontentloaded first (most reliable when it works)
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except:
            print("⚠️ DOM content loaded timeout, trying alternative approach...")
            try:
                # Fallback to networkidle
                self.page.wait_for_load_state("networkidle", timeout=timeout//2)
            except:
                print("⚠️ Network idle timeout, continuing anyway...")
                # Final fallback - just wait a bit
                time.sleep(2)
    
    def start_browser(self) -> bool:
        """
        Initialize Playwright browser and create context.
        
        Returns:
            bool: True if browser started successfully, False otherwise
        """
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=HEADLESS,
                args=['--no-sandbox', '--disable-dev-shm-usage', '--start-maximized']
            )
            
            # Get dynamic screen resolution
            screen_width, screen_height = self._get_screen_resolution()
            print(f"🖥️ Detected screen resolution: {screen_width}x{screen_height}")
            
            # Create context with user agent to avoid detection
            self.context = self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": screen_width, "height": screen_height}
            )
            
            self.page = self.context.new_page()
            self.page.set_default_timeout(BROWSER_TIMEOUT)
            
            print("✅ Browser started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            return False
    
    def login_to_linkedin(self) -> bool:
        """
        Login to LinkedIn using provided credentials.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
                print("❌ LinkedIn credentials not configured. Please update linkedin_config.py")
                return False
            
            print("🔐 Logging into LinkedIn...")
            self.page.goto(LINKEDIN_BASE_URL)
            self._wait_for_page_load(timeout=10000)
            
            # Check if already logged in by looking for profile elements
            try:
                self.page.wait_for_selector(".global-nav__me", timeout=5000)
                print("✅ Already logged into LinkedIn")
                return True
            except:
                pass  # Not logged in, continue with login process
            
            # Navigate to login page - try multiple approaches
            login_success = False
            
            # Method 1: Look for "Sign in with email" button on homepage
            try:
                sign_in_email_button = self.page.locator("a[data-test-id='home-hero-sign-in-cta']")
                if sign_in_email_button.is_visible():
                    sign_in_email_button.click()
                    try:
                        self.page.wait_for_load_state("networkidle", timeout=10000)
                    except:
                        print("⚠️ Sign in email button click timeout, continuing...")
                    login_success = True
                    print("📧 Found 'Sign in with email' button")
            except:
                pass
            
            # Method 2: Look for "Sign in with email" by text content
            if not login_success:
                try:
                    sign_in_email_text = self.page.locator("text=Sign in with email")
                    if sign_in_email_text.is_visible():
                        sign_in_email_text.click()
                        try:
                            self.page.wait_for_load_state("networkidle", timeout=10000)
                        except:
                            print("⚠️ Sign in email text click timeout, continuing...")
                        login_success = True
                        print("📧 Found 'Sign in with email' by text")
                except:
                    pass
            
            # Method 3: Look for generic "Sign in" text
            if not login_success:
                try:
                    sign_in_button = self.page.locator("text=Sign in").first
                    if sign_in_button.is_visible():
                        sign_in_button.click()
                        try:
                            self.page.wait_for_load_state("networkidle", timeout=10000)
                        except:
                            print("⚠️ Generic sign in button click timeout, continuing...")
                        login_success = True
                        print("📧 Found generic 'Sign in' button")
                except:
                    pass
            
            # Method 4: Look for sign in link in header
            if not login_success:
                try:
                    header_sign_in = self.page.locator("a[href*='/login']")
                    if header_sign_in.is_visible():
                        header_sign_in.click()
                        try:
                            self.page.wait_for_load_state("networkidle", timeout=10000)
                        except:
                            print("⚠️ Header sign in link click timeout, continuing...")
                        login_success = True
                        print("📧 Found header sign in link")
                except:
                    pass
            
            # Method 5: Navigate directly to login URL
            if not login_success:
                try:
                    self.page.goto("https://www.linkedin.com/login")
                    try:
                        self.page.wait_for_load_state("networkidle", timeout=10000)
                    except:
                        print("⚠️ Direct login URL timeout, continuing...")
                    login_success = True
                    print("🔗 Navigated directly to login page")
                except:
                    pass
            
            if not login_success:
                print("❌ Could not find sign in button or navigate to login page")
                return False
            
            # Wait for login form to be visible - try multiple selectors
            form_found = False
            try:
                self.page.wait_for_selector("#username", timeout=10000)
                form_found = True
            except:
                try:
                    self.page.wait_for_selector("input[name='session_key']", timeout=5000)
                    form_found = True
                except:
                    try:
                        self.page.wait_for_selector("input[type='email']", timeout=5000)
                        form_found = True
                    except:
                        pass
            
            if not form_found:
                print("❌ Login form not found")
                self._take_screenshot("login_form_not_found")
                return False
            
            # Fill email - try multiple selectors
            email_filled = False
            try:
                email_field = self.page.locator("#username")
                email_field.clear()
                email_field.fill(LINKEDIN_EMAIL)
                email_filled = True
            except:
                try:
                    email_field = self.page.locator("input[name='session_key']")
                    email_field.clear()
                    email_field.fill(LINKEDIN_EMAIL)
                    email_filled = True
                except:
                    try:
                        email_field = self.page.locator("input[type='email']")
                        email_field.clear()
                        email_field.fill(LINKEDIN_EMAIL)
                        email_filled = True
                    except:
                        pass
            
            if not email_filled:
                print("❌ Could not fill email field")
                return False
            
            # Fill password - try multiple selectors
            password_filled = False
            try:
                password_field = self.page.locator("#password")
                password_field.clear()
                password_field.fill(LINKEDIN_PASSWORD)
                password_filled = True
            except:
                try:
                    password_field = self.page.locator("input[name='session_password']")
                    password_field.clear()
                    password_field.fill(LINKEDIN_PASSWORD)
                    password_filled = True
                except:
                    try:
                        password_field = self.page.locator("input[type='password']")
                        password_field.clear()
                        password_field.fill(LINKEDIN_PASSWORD)
                        password_filled = True
                    except:
                        pass
            
            if not password_filled:
                print("❌ Could not fill password field")
                return False
            
            # Click sign in button - try multiple selectors
            submit_clicked = False
            try:
                sign_in_submit = self.page.locator("button[type='submit']")
                sign_in_submit.click()
                submit_clicked = True
            except:
                try:
                    sign_in_submit = self.page.locator("button:has-text('Sign in')")
                    sign_in_submit.click()
                    submit_clicked = True
                except:
                    try:
                        sign_in_submit = self.page.locator("input[type='submit']")
                        sign_in_submit.click()
                        submit_clicked = True
                    except:
                        pass
            
            if not submit_clicked:
                print("❌ Could not click submit button")
                return False
            
            # Wait for login to complete with robust approach
            self._wait_for_page_load(timeout=10000)
            
            # Additional wait for page to stabilize
            # time.sleep(3)

            # Check URL for successful login
            current_url = self.page.url
            if "linkedin.com/feed" in current_url or "linkedin.com/in/" in current_url:
                print("✅ Successfully logged into LinkedIn (URL check)")
                return True

            # Check if login was successful by looking for profile elements
            try:
                self.page.wait_for_selector(".global-nav__me", timeout=10000)
                print("✅ Successfully logged into LinkedIn")
                return True
            except:
                # Alternative check - look for feed or profile elements
                try:
                    self.page.wait_for_selector("[data-test-id='main-feed']", timeout=5000)
                    print("✅ Successfully logged into LinkedIn (feed detected)")
                    return True
                except:
                    pass
                
                print("❌ Login failed - could not find profile elements")
                self._take_screenshot("login_failed")
                return False
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            self._take_screenshot("login_error")
            return False
    
    def navigate_to_jobs(self, search_term: str) -> bool:
        """
        Navigate to LinkedIn Jobs and search for the given term.
        
        Args:
            search_term (str): Job title to search for
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print(f"🔍 Searching for jobs: {search_term}")
            
            # Navigate to jobs page
            jobs_url = f"{LINKEDIN_JOBS_URL}?keywords={search_term.replace(' ', '%20')}"
            
            # Handle search location (can be string or list)
            if SEARCH_LOCATION:
                if isinstance(SEARCH_LOCATION, list):
                    # Use first location for now (can be enhanced later)
                    location = SEARCH_LOCATION[0]
                else:
                    location = SEARCH_LOCATION
                jobs_url += f"&location={location.replace(' ', '%20')}"
            
            print(f"🌐 Navigating to: {jobs_url}")
            self.page.goto(jobs_url)
            self._wait_for_page_load(timeout=15000)
            
            # Check if we're on the jobs page by looking for multiple indicators
            jobs_page_indicators = [
                "li[data-occludable-job-id]",  # Most reliable for new LinkedIn structure
                "li[data-job-id]",  # Alternative data attribute
                "[data-job-id]",  # Any element with job ID
                ".jobs-search-results__list-item",  # Traditional class
                ".jobs-search-results__list",  # Container class
                "li[data-job-id]",  # List item with job ID
                ".jobs-search-results__list li"  # Any li in jobs list
            ]
            try:
                for indicator in jobs_page_indicators:
                    self.page.wait_for_selector(indicator, timeout=5000)
                    print(f"✅ Job search page loaded successfully (found: {indicator})")
                    break
            except:
                print("❌ Job search page did not load properly")
                self._take_screenshot("job_search_page_load_failed")
                return False
            
            # Extract total job count from the blue panel
            total_jobs = self._get_total_job_count()
            if total_jobs > 0:
                print(f"📊 Total jobs found: {total_jobs}")
                return True
            else:
                print("❌ No jobs found for this search")
                return False
                
        except Exception as e:
            print(f"❌ Failed to navigate to jobs: {e}")
            self._take_screenshot("jobs_navigation_error")
            return False
    
    def _get_total_job_count(self) -> int:
        """
        Extract the total job count from the blue results panel.
        
        Returns:
            int: Total number of jobs found, 0 if not found
        """
        try:
            # Look for the results count in the blue panel
            # Format: "577 results" in span with class "jobs-search-results-list__subtitle"
            results_text = self.page.locator(".jobs-search-results-list__subtitle span").inner_text()
            
            if results_text and "results" in results_text:
                # Extract number from text like "577 results"
                import re
                match = re.search(r'(\d+)', results_text)
                if match:
                    total_count = int(match.group(1))
                    return total_count
            
            # Alternative selector if the first one doesn't work
            try:
                results_text = self.page.locator(".jobs-search-results-list__text").inner_text()
                if results_text and "results" in results_text:
                    import re
                    match = re.search(r'(\d+)', results_text)
                    if match:
                        total_count = int(match.group(1))
                        return total_count
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Could not extract total job count: {e}")
        
        return 0
    
    def get_job_listings(self, max_jobs: int = 25) -> List[Dict]:
        """
        Extract job listings from the current page with pagination support.
        
        Args:
            max_jobs (int): Maximum number of jobs to extract (default: 25)
            
        Returns:
            List[Dict]: List of job information dictionaries
        """
        try:
            print(f"🔍 Extracting job listings (max: {max_jobs})...")
            
            # Try multiple selectors to find job cards (robust approach for dynamic class names)
            job_cards = None
            visible_jobs = 0
            
            # Method 1: Look for li elements with data-occludable-job-id attribute
            try:
                job_cards = self.page.locator("li[data-occludable-job-id]")
                visible_jobs = job_cards.count()
                if visible_jobs > 0:
                    print(f"📋 Found {visible_jobs} jobs using data-occludable-job-id selector")
            except:
                pass
            
            # Method 2: Look for li elements with data-job-id attribute
            if visible_jobs == 0:
                try:
                    job_cards = self.page.locator("li[data-job-id]")
                    visible_jobs = job_cards.count()
                    if visible_jobs > 0:
                        print(f"📋 Found {visible_jobs} jobs using data-job-id selector")
                except:
                    pass
            
            # Method 3: Look for traditional class-based selector
            if visible_jobs == 0:
                try:
                    job_cards = self.page.locator(".jobs-search-results__list-item")
                    visible_jobs = job_cards.count()
                    if visible_jobs > 0:
                        print(f"📋 Found {visible_jobs} jobs using traditional class selector")
                except:
                    pass
            
            # Method 4: Look for any li element within the jobs list container
            if visible_jobs == 0:
                try:
                    job_cards = self.page.locator(".jobs-search-results__list li")
                    visible_jobs = job_cards.count()
                    if visible_jobs > 0:
                        print(f"📋 Found {visible_jobs} jobs using container-based selector")
                except:
                    pass
            
            if visible_jobs == 0:
                print("❌ No job listings found on the page")
                self._take_screenshot("no_job_listings")
                return []
            
            print(f"📋 Found {visible_jobs} jobs on current page")
            
            jobs = []
            jobs_to_process = min(visible_jobs, max_jobs)
            
            for i in range(jobs_to_process):
                try:
                    job_card = job_cards.nth(i)
                    job_info = self._extract_job_details(job_card, i)
                    if job_info:
                        jobs.append(job_info)
                        print(f"📋 Found job: {job_info['title']} at {job_info['company']} {'(Easy Apply)' if job_info['has_easy_apply'] else ''}")
                    
                except Exception as e:
                    print(f"⚠️ Error extracting job {i}: {e}")
                    continue
            
            print(f"✅ Successfully extracted {len(jobs)} job listings")
            return jobs
            
        except Exception as e:
            print(f"❌ Error getting job listings: {e}")
            self._take_screenshot("job_listings_error")
            return []
    
    def _extract_job_details(self, job_card, index: int) -> Dict:
        """
        Extract details from a single job card using robust selectors.
        First checks for Easy Apply availability before extracting details.
        
        Args:
            job_card: Playwright locator for the job card
            index (int): Index of the job card
            
        Returns:
            Dict: Job information dictionary or None if no Easy Apply
        """
        try:
            # First, check if Easy Apply is available - skip if not
            has_easy_apply = self._check_easy_apply_availability(job_card)
            if not has_easy_apply:
                print(f"⏭️ Skipping job {index} - No Easy Apply option available")
                return None
            
            # Initialize job details
            title = "Unknown"
            company = "Unknown"
            location = "Unknown"
            job_link = ""
            
            # Extract job title with improved selectors
            try:
                # Try multiple selectors for job title
                title_selectors = [
                    "h3 a",  # Most common for job listings
                    "h1 a",  # Job details page
                    "a[data-control-name='job_card_title']",
                    "a[href*='/jobs/view/']",
                    ".job-card-list__title a",
                    ".jobs-unified-top-card__job-title a",
                    "a.job-card-list__title"
                ]
                
                for selector in title_selectors:
                    try:
                        title_element = job_card.locator(selector)
                        if title_element.is_visible():
                            title = title_element.inner_text().strip()
                            if title and title != "Unknown":
                                break
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Error extracting title: {e}")
            
            # Extract company name with improved selectors
            try:
                company_selectors = [
                    "h4 a",  # Most common for company names
                    ".job-card-container__metadata-item a",
                    "a[data-control-name='job_card_company']",
                    ".jobs-unified-top-card__company-name a",
                    ".job-card-list__company-name a",
                    "h4"
                ]
                
                for selector in company_selectors:
                    try:
                        company_element = job_card.locator(selector)
                        if company_element.is_visible():
                            company = company_element.inner_text().strip()
                            if company and company != "Unknown":
                                break
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Error extracting company: {e}")
            
            # Extract location with improved selectors
            try:
                location_selectors = [
                    ".job-card-container__metadata-item",
                    "[data-control-name='job_card_location']",
                    ".jobs-unified-top-card__bullet",
                    ".job-card-list__location",
                    "span:has-text(',')"  # Look for spans with commas (likely locations)
                ]
                
                for selector in location_selectors:
                    try:
                        location_element = job_card.locator(selector)
                        if location_element.is_visible():
                            location_text = location_element.inner_text().strip()
                            # Extract location from text like "San Francisco, CA · 1 month ago · Over 100 applicants"
                            if location_text and "·" in location_text:
                                location = location_text.split("·")[0].strip()
                            else:
                                location = location_text
                            
                            if location and location != "Unknown":
                                break
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Error extracting location: {e}")
            
            # Get job link and clean it
            try:
                # Try to get link from title element or any job link
                link_selectors = [
                    "h3 a",
                    "h1 a", 
                    "a[href*='/jobs/view/']",
                    "a[data-control-name='job_card_title']"
                ]
                
                for selector in link_selectors:
                    try:
                        link_element = job_card.locator(selector)
                        if link_element.is_visible():
                            job_link = link_element.get_attribute("href")
                            if job_link:
                                # Clean the job link by removing query parameters
                                if not job_link.startswith("http"):
                                    job_link = f"{LINKEDIN_BASE_URL}{job_link}"
                                
                                # Remove query parameters to get clean URL
                                if "?" in job_link:
                                    job_link = job_link.split("?")[0]
                                break
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Error extracting job link: {e}")
            
            return {
                "title": title.strip(),
                "company": company.strip(),
                "location": location.strip(),
                "link": job_link,
                "has_easy_apply": has_easy_apply,
                "index": index
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting job details for index {index}: {e}")
            return None
    
    def _check_easy_apply_availability(self, job_card) -> bool:
        """
        Check if Easy Apply is available for a job card.
        
        Args:
            job_card: Playwright locator for the job card
            
        Returns:
            bool: True if Easy Apply is available, False otherwise
        """
        try:
            # Multiple selectors for Easy Apply button
            easy_apply_selectors = [
                "button[aria-label*='Easy Apply']",
                "button:has-text('Easy Apply')",
                "[data-control-name='job_card_apply']",
                ".jobs-apply-button",
                "span:has-text('Easy Apply')",
                "button:has-text('Apply')",
                ".jobs-s-apply button",
                ".jobs-apply-button--top-card button",
                "button[data-job-id]",
                "button[aria-label*='Apply']"
            ]
            
            for selector in easy_apply_selectors:
                try:
                    easy_apply_button = job_card.locator(selector)
                    if easy_apply_button.is_visible():
                        return True
                except:
                    continue
            
            # Also check for any button with "Apply" or "Easy" in text
            try:
                all_buttons = job_card.locator("button")
                for i in range(all_buttons.count()):
                    try:
                        button = all_buttons.nth(i)
                        if button.is_visible():
                            button_text = button.text_content().lower()
                            if "easy apply" in button_text or "apply" in button_text:
                                return True
                    except:
                        continue
            except:
                pass
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking Easy Apply availability: {e}")
            return False
    
    def navigate_to_next_page(self) -> bool:
        """
        Navigate to the next page of job results.
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            # Look for "Next" button or pagination controls
            next_button = self.page.locator("button[aria-label='Next']")
            if next_button.is_visible():
                next_button.click()
                self._wait_for_page_load(timeout=10000)
                print("✅ Navigated to next page")
                return True
            
            # Alternative: Look for page number buttons
            try:
                # Find current page number and look for next page
                current_page = self.page.locator(".artdeco-pagination__indicator--number.artdeco-pagination__indicator--number--selected")
                if current_page.is_visible():
                    current_page_num = int(current_page.inner_text())
                    next_page_button = self.page.locator(f".artdeco-pagination__indicator--number:has-text('{current_page_num + 1}')")
                    if next_page_button.is_visible():
                        next_page_button.click()
                        self._wait_for_page_load(timeout=10000)
                        print(f"✅ Navigated to page {current_page_num + 1}")
                        return True
            except:
                pass
            
            # Alternative: Look for arrow navigation
            try:
                arrow_button = self.page.locator(".artdeco-pagination__button--next")
                if arrow_button.is_visible():
                    arrow_button.click()
                    self._wait_for_page_load(timeout=10000)
                    print("✅ Navigated to next page (arrow)")
                    return True
            except:
                pass
            
            print("❌ No next page button found")
            return False
            
        except Exception as e:
            print(f"❌ Failed to navigate to next page: {e}")
            self._take_screenshot("pagination_error")
            return False
    
    def get_all_job_listings(self, max_jobs: int = 100) -> List[Dict]:
        """
        Get job listings from multiple pages with pagination support.
        
        Args:
            max_jobs (int): Maximum number of jobs to extract across all pages
            
        Returns:
            List[Dict]: List of job information dictionaries from all pages
        """
        try:
            all_jobs = []
            page_count = 0
            max_pages = (max_jobs // 25) + 1  # LinkedIn shows ~25 jobs per page
            
            print(f"🔍 Extracting jobs from multiple pages (max: {max_jobs})")
            
            while len(all_jobs) < max_jobs and page_count < max_pages:
                page_count += 1
                print(f"📄 Processing page {page_count}...")
                
                # Get jobs from current page
                jobs_per_page = min(25, max_jobs - len(all_jobs))
                current_page_jobs = self.get_job_listings(max_jobs=jobs_per_page)
                
                if not current_page_jobs:
                    print("❌ No more jobs found")
                    break
                
                all_jobs.extend(current_page_jobs)
                print(f"📊 Total jobs collected so far: {len(all_jobs)}")
                
                # Try to navigate to next page
                if len(all_jobs) < max_jobs and page_count < max_pages:
                    if not self.navigate_to_next_page():
                        print("❌ No more pages available")
                        break
                    
                    # Wait for new page to load
                    time.sleep(2)
            
            print(f"✅ Successfully extracted {len(all_jobs)} jobs from {page_count} pages")
            return all_jobs
            
        except Exception as e:
            print(f"❌ Error getting all job listings: {e}")
            self._take_screenshot("all_job_listings_error")
            return []
    
    def click_easy_apply(self, job_index: int) -> bool:
        """
        Click the Easy Apply button for a specific job.
        
        Args:
            job_index (int): Index of the job in the current listings
            
        Returns:
            bool: True if Easy Apply button clicked successfully
        """
        try:
            # Try multiple selectors for job cards
            job_card_selectors = [
                "li[data-occludable-job-id]",
                "li[data-job-id]",
                ".jobs-search-results__list-item",
                ".jobs-search-results__list li"
            ]
            
            job_card = None
            for selector in job_card_selectors:
                try:
                    job_cards = self.page.locator(selector)
                    if job_cards.count() > job_index:
                        job_card = job_cards.nth(job_index)
                        break
                except:
                    continue
            
            if not job_card:
                print("❌ Job card not found")
                return False
            
            # Try multiple selectors for Easy Apply button
            easy_apply_selectors = [
                "button[aria-label*='Easy Apply']",
                "button:has-text('Easy Apply')",
                ".jobs-apply-button",
                "button[data-job-id]",
                "button:has-text('Apply')",
                ".jobs-s-apply button",
                ".jobs-apply-button--top-card button",
                "button[aria-label*='Apply']",
                "[data-control-name='job_card_apply']"
            ]
            
            for selector in easy_apply_selectors:
                try:
                    easy_apply_button = job_card.locator(selector)
                    if easy_apply_button.is_visible():
                        easy_apply_button.scroll_into_view_if_needed()
                        time.sleep(1)
                        easy_apply_button.click()
                        
                        # Wait for Easy Apply modal to open
                        self.page.wait_for_selector(".jobs-easy-apply-modal", timeout=10000)
                        print("✅ Easy Apply modal opened")
                        return True
                except:
                    continue
            
            print("❌ Easy Apply button not found for this job")
            return False
            
        except Exception as e:
            print(f"❌ Failed to click Easy Apply: {e}")
            self._take_screenshot("easy_apply_error")
            return False
    
    def close_easy_apply_modal(self) -> bool:
        """
        Close the Easy Apply modal.
        
        Returns:
            bool: True if modal closed successfully
        """
        try:
            # Try to find and click close button
            close_button = self.page.locator("button[aria-label='Dismiss']")
            if close_button.is_visible():
                close_button.click()
                time.sleep(1)
                return True
            
            # Alternative: press Escape key
            self.page.keyboard.press("Escape")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"⚠️ Error closing modal: {e}")
            return False
    
    def _take_screenshot(self, filename_prefix: str) -> str:
        """
        Take a screenshot for debugging purposes.
        
        Args:
            filename_prefix (str): Prefix for the screenshot filename
            
        Returns:
            str: Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            screenshot_path = os.path.join(OUTPUT_DIR, SCREENSHOTS_DIR, filename)
            self.page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"⚠️ Failed to take screenshot: {e}")
            return ""
    
    def close_browser(self):
        """Close the browser and cleanup resources."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()
