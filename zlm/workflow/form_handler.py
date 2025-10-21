'''
-----------------------------------------------------------------------
File: form_handler.py
Creation Time: Oct 20th 2025
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2025 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

import time
import os
import re
from playwright.sync_api import Page, Locator
from typing import Dict, List, Optional, Tuple
from .linkedin_config import (
    PHONE_NUMBER, YEARS_OF_EXPERIENCE, REQUIRE_VISA, DEFAULT_RESUME_PATH
)
from .profile_loader import ProfileLoader
from .unseen_questions import UnseenQuestionsHandler


class EasyApplyFormHandler:
    """
    Handles the complete LinkedIn Easy Apply process including form filling and submission.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.applied_jobs = []
        self.failed_jobs = []
        self.unseen_questions_handler = UnseenQuestionsHandler()
        self.profile_loader = ProfileLoader()
    
    def process_easy_apply_by_index(self, job_index: int, job_info: Dict) -> Tuple[bool, str]:
        """
        Complete Easy Apply process for a job by index (stays on same page).
        
        Args:
            job_index (int): Index of the job in the current listings
            job_info (Dict): Information about the job being applied to
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            print(f"🎯 Starting Easy Apply process for: {job_info['title']} at {job_info['company']}")
            
            # Step 1: Click Easy Apply button by job index
            if not self._click_easy_apply_button_by_index(job_index):
                return False, "Could not click Easy Apply button"
            
            # Step 2: Wait for Easy Apply modal to open
            if not self._wait_for_easy_apply_modal():
                return False, "Easy Apply modal did not open"
            
            # Step 3: Process the Easy Apply form
            success, error_msg = self._process_easy_apply_form(job_info)
            
            if success:
                print(f"✅ Successfully applied to: {job_info['title']} at {job_info['company']}")
                self.applied_jobs.append(job_info)
            else:
                print(f"❌ Failed to apply to: {job_info['title']} at {job_info['company']}")
                print(f"   Error: {error_msg}")
                self.failed_jobs.append({**job_info, 'error': error_msg})
            
            # Step 4: Close the modal
            self._close_easy_apply_modal()
            
            return success, error_msg
            
        except Exception as e:
            error_msg = f"Error in Easy Apply process: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def process_easy_apply(self, job_info: Dict) -> Tuple[bool, str]:
        """
        Complete Easy Apply process for a job.
        
        Args:
            job_info (Dict): Information about the job being applied to
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            print(f"🎯 Starting Easy Apply process for: {job_info['title']} at {job_info['company']}")
            
            # Step 1: Click Easy Apply button
            if not self._click_easy_apply_button(job_info):
                return False, "Could not click Easy Apply button"
            
            # Step 2: Wait for Easy Apply modal to open
            if not self._wait_for_easy_apply_modal():
                return False, "Easy Apply modal did not open"
            
            # Step 3: Process the Easy Apply form
            success, error_msg = self._process_easy_apply_form(job_info)
            
            if success:
                print(f"✅ Successfully applied to: {job_info['title']} at {job_info['company']}")
                self.applied_jobs.append(job_info)
            else:
                print(f"❌ Failed to apply to: {job_info['title']} at {job_info['company']}")
                print(f"   Error: {error_msg}")
                self.failed_jobs.append({**job_info, 'error': error_msg})
            
            # Step 4: Close the modal
            self._close_easy_apply_modal()
            
            return success, error_msg
            
        except Exception as e:
            error_msg = f"Error in Easy Apply process: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def _click_easy_apply_button_by_index(self, job_index: int) -> bool:
        """Click the Easy Apply button for a job by index (stays on same page)."""
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
            
            # Multiple selectors for Easy Apply button within the job card
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
                    button = job_card.locator(selector)
                    if button.is_visible():
                        button.scroll_into_view_if_needed()
                        time.sleep(1)  # Small delay to ensure button is ready
                        button.click()
                        print(f"✅ Clicked Easy Apply button using selector: {selector}")
                        return True
                except:
                    continue
            
            # Try to find any button with "Apply" or "Easy" in text within the job card
            try:
                all_buttons = job_card.locator("button")
                for i in range(all_buttons.count()):
                    try:
                        button = all_buttons.nth(i)
                        if button.is_visible():
                            button_text = button.text_content().lower()
                            if "easy apply" in button_text or "apply" in button_text:
                                button.scroll_into_view_if_needed()
                                time.sleep(1)
                                button.click()
                                print(f"✅ Clicked Easy Apply button by text: {button_text}")
                                return True
                    except:
                        continue
            except:
                pass
            
            print("❌ Easy Apply button not found for this job")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking Easy Apply button: {e}")
            return False
    
    def _click_easy_apply_button(self, job_info: Dict) -> bool:
        """Click the Easy Apply button for a job."""
        try:
            # Multiple selectors for Easy Apply button
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
                    button = self.page.locator(selector)
                    if button.is_visible():
                        button.scroll_into_view_if_needed()
                        time.sleep(1)  # Wait for button to be ready
                        button.click()
                        print(f"✅ Clicked Easy Apply button using selector: {selector}")
                        return True
                except:
                    continue
            
            # Try to find any button with "Apply" or "Easy" in text
            try:
                all_buttons = self.page.locator("button")
                for i in range(all_buttons.count()):
                    try:
                        button = all_buttons.nth(i)
                        if button.is_visible():
                            button_text = button.text_content().lower()
                            if "easy apply" in button_text or "apply" in button_text:
                                button.scroll_into_view_if_needed()
                                time.sleep(1)
                                button.click()
                                print(f"✅ Clicked Easy Apply button by text: {button_text}")
                                return True
                    except:
                        continue
            except:
                pass
            
            print("❌ Could not find Easy Apply button")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking Easy Apply button: {e}")
            return False
    
    def _wait_for_easy_apply_modal(self) -> bool:
        """Wait for the Easy Apply modal to open."""
        try:
            # Wait for modal to appear
            modal_selectors = [
                ".jobs-easy-apply-modal",
                ".jobs-apply-modal",
                "[data-test-modal]",
                ".artdeco-modal"
            ]
            
            for selector in modal_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    print(f"✅ Easy Apply modal opened (selector: {selector})")
                    time.sleep(2)  # Wait for form to fully load
                    return True
                except:
                    continue
            
            print("❌ Easy Apply modal did not open")
            return False
            
        except Exception as e:
            print(f"❌ Error waiting for modal: {e}")
            return False
    
    def _process_easy_apply_form(self, job_info: Dict) -> Tuple[bool, str]:
        """Process the complete Easy Apply form."""
        try:
            step_count = 1
            max_steps = 10  # Prevent infinite loops
            
            while step_count <= max_steps:
                print(f"🔄 Processing Easy Apply step {step_count}")
                
                # Fill all form fields in current step
                self._fill_current_step()
                
                # Look for next/submit button
                next_button = self._find_next_or_submit_button()
                if not next_button:
                    return False, f"No next/submit button found in step {step_count}"
                
                # Check if this is the final step
                button_text = next_button.text_content().lower()
                if any(keyword in button_text for keyword in ["submit", "send", "apply", "finish"]):
                    print("✅ Found submit button - submitting application")
                    next_button.click()
                    time.sleep(3)  # Wait for submission
                    
                    # Check for success
                    if self._check_application_success():
                        return True, "Application submitted successfully"
                    else:
                        return False, "Application submission failed"
                else:
                    print(f"➡️ Moving to next step")
                    next_button.click()
                    time.sleep(2)  # Wait for next step to load
                    step_count += 1
            
            return False, f"Reached maximum steps ({max_steps}) without completion"
            
        except Exception as e:
            return False, f"Error processing form: {str(e)}"
    
    def _fill_current_step(self):
        """Fill all form fields in the current step."""
        try:
            # Fill text inputs
            self._fill_text_inputs()
            
            # Fill select dropdowns
            self._fill_select_dropdowns()
            
            # Fill radio buttons
            self._fill_radio_buttons()
            
            # Fill checkboxes
            self._fill_checkboxes()
            
            # Handle file uploads
            self._handle_file_uploads()
            
            # Handle questions
            self._handle_questions()
            
        except Exception as e:
            print(f"⚠️ Error filling current step: {e}")
    
    def _fill_text_inputs(self):
        """Fill text input fields with personalized data."""
        try:
            text_inputs = self.page.locator("input[type='text'], input[type='email'], input[type='tel'], input[type='number']")
            
            for i in range(text_inputs.count()):
                try:
                    input_field = text_inputs.nth(i)
                    if not input_field.is_visible():
                        continue
                    
                    # Get field information
                    field_info = self._get_field_info(input_field)
                    value = self._get_personalized_value(field_info)
                    
                    if value:
                        input_field.clear()
                        input_field.fill(value)
                        print(f"📝 Filled {field_info['label']}: {value}")
                        
                except Exception as e:
                    print(f"⚠️ Error filling text input {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error with text inputs: {e}")
    
    def _fill_select_dropdowns(self):
        """Fill select dropdown fields."""
        try:
            select_elements = self.page.locator("select")
            
            for i in range(select_elements.count()):
                try:
                    select_field = select_elements.nth(i)
                    if not select_field.is_visible():
                        continue
                    
                    field_info = self._get_field_info(select_field)
                    value = self._get_personalized_value(field_info)
                    
                    if value:
                        select_field.select_option(value)
                        print(f"📝 Selected {field_info['label']}: {value}")
                        
                except Exception as e:
                    print(f"⚠️ Error filling select {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error with select dropdowns: {e}")
    
    def _fill_radio_buttons(self):
        """Fill radio button fields."""
        try:
            radio_groups = self.page.locator("input[type='radio']")
            
            for i in range(radio_groups.count()):
                try:
                    radio_button = radio_groups.nth(i)
                    if not radio_button.is_visible():
                        continue
                    
                    field_info = self._get_field_info(radio_button)
                    should_select = self._should_select_radio(field_info)
                    
                    if should_select:
                        radio_button.check()
                        print(f"📝 Selected radio: {field_info['label']} = {field_info['value']}")
                        
                except Exception as e:
                    print(f"⚠️ Error with radio button {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error with radio buttons: {e}")
    
    def _fill_checkboxes(self):
        """Fill checkbox fields."""
        try:
            checkboxes = self.page.locator("input[type='checkbox']")
            
            for i in range(checkboxes.count()):
                try:
                    checkbox = checkboxes.nth(i)
                    if not checkbox.is_visible():
                        continue
                    
                    field_info = self._get_field_info(checkbox)
                    should_check = self._should_check_checkbox(field_info)
                    
                    if should_check:
                        checkbox.check()
                        print(f"📝 Checked: {field_info['label']}")
                        
                except Exception as e:
                    print(f"⚠️ Error with checkbox {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error with checkboxes: {e}")
    
    def _handle_file_uploads(self):
        """Handle file upload fields (resume upload)."""
        try:
            file_inputs = self.page.locator("input[type='file']")
            
            for i in range(file_inputs.count()):
                try:
                    file_input = file_inputs.nth(i)
                    if not file_input.is_visible():
                        continue
                    
                    # Use resume from profile loader
                    documents_info = self.profile_loader.get_documents_info()
                    resume_path = documents_info.get("resume_path", DEFAULT_RESUME_PATH)
                    if os.path.exists(resume_path):
                        file_input.set_input_files(resume_path)
                        print(f"📎 Uploaded resume: {resume_path}")
                    else:
                        print(f"⚠️ Resume file not found: {resume_path}")
                        
                except Exception as e:
                    print(f"⚠️ Error uploading file {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error with file uploads: {e}")
    
    def _handle_questions(self):
        """Handle question-answer sections in the form."""
        try:
            # Look for question containers
            question_containers = self.page.locator(".jobs-easy-apply-form-section, .form-section, .question")
            
            for i in range(question_containers.count()):
                try:
                    container = question_containers.nth(i)
                    if not container.is_visible():
                        continue
                    
                    # Extract question text
                    question_text = self._extract_question_text(container)
                    if not question_text:
                        continue
                    
                    # Get answer for the question
                    answer = self._get_question_answer(question_text, container)
                    
                    # Fill the answer
                    if answer:
                        self._fill_question_answer(container, answer, question_text)
                        
                except Exception as e:
                    print(f"⚠️ Error handling question {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error handling questions: {e}")
    
    def _get_field_info(self, field_element: Locator) -> Dict:
        """Get comprehensive information about a form field."""
        try:
            field_info = {
                'id': field_element.get_attribute("id") or "",
                'name': field_element.get_attribute("name") or "",
                'type': field_element.get_attribute("type") or "",
                'placeholder': field_element.get_attribute("placeholder") or "",
                'value': field_element.get_attribute("value") or "",
                'label': self._get_field_label(field_element),
                'required': field_element.get_attribute("required") is not None
            }
            return field_info
        except:
            return {'id': '', 'name': '', 'type': '', 'placeholder': '', 'value': '', 'label': '', 'required': False}
    
    def _get_field_label(self, field_element: Locator) -> str:
        """Get the label text for a form field."""
        try:
            # Try to find associated label
            field_id = field_element.get_attribute("id")
            if field_id:
                label = self.page.locator(f"label[for='{field_id}']")
                if label.is_visible():
                    return label.text_content().strip()
            
            # Try to find parent label
            parent_label = field_element.locator("xpath=..//label")
            if parent_label.is_visible():
                return parent_label.text_content().strip()
            
            # Try to find nearby text
            nearby_text = field_element.locator("xpath=..//text()")
            if nearby_text.is_visible():
                return nearby_text.text_content().strip()
            
            return ""
            
        except Exception:
            return ""
    
    def _get_personalized_value(self, field_info: Dict) -> Optional[str]:
        """Get personalized value for a form field."""
        field_text = f"{field_info['id']} {field_info['name']} {field_info['placeholder']} {field_info['label']}".lower()
        
        # Use profile loader to get answer
        return self.profile_loader.get_question_answer(field_text)
    
    def _should_select_radio(self, field_info: Dict) -> bool:
        """Determine if a radio button should be selected."""
        radio_text = f"{field_info['value']} {field_info['label']}".lower()
        
        # Yes/No questions
        if "yes" in radio_text and "no" not in radio_text:
            return True
        if "no" in radio_text and "yes" not in radio_text:
            return False
        
        # Experience levels
        total_years = self.profile_loader._calculate_total_experience()
        if "years" in radio_text and str(total_years) in field_info['value']:
            return True
        
        # Work authorization
        if "authorized" in radio_text and "yes" in radio_text:
            return True
        
        # Relocation
        if "relocate" in radio_text and "yes" in radio_text:
            return True
        
        return False
    
    def _should_check_checkbox(self, field_info: Dict) -> bool:
        """Determine if a checkbox should be checked."""
        checkbox_text = f"{field_info['label']}".lower()
        
        # Agreement checkboxes
        if any(keyword in checkbox_text for keyword in ["agree", "terms", "conditions", "policy"]):
            return True
        
        # Contact preferences
        if any(keyword in checkbox_text for keyword in ["contact", "notify", "update"]):
            return True
        
        return False
    
    def _extract_question_text(self, container: Locator) -> str:
        """Extract question text from a container."""
        try:
            # Look for question text in various elements
            question_selectors = [
                "h3", "h4", "h5", "h6", "p", "span", "div"
            ]
            
            for selector in question_selectors:
                try:
                    question_element = container.locator(selector).first
                    if question_element.is_visible():
                        text = question_element.text_content().strip()
                        if text and len(text) > 10:  # Reasonable question length
                            return text
                except:
                    continue
            
            return ""
        except:
            return ""
    
    def _get_question_answer(self, question_text: str, container: Locator) -> str:
        """Get answer for a question."""
        try:
            # First, try to get answer from profile loader
            answer = self.profile_loader.get_question_answer(question_text)
            if answer and answer != "Yes":  # If we got a specific answer
                return answer
            
            # If not found, add to unseen questions and get default answer
            question_type = self._determine_question_type(container)
            options = self._extract_question_options(container)
            
            answer = self.unseen_questions_handler.add_unseen_question(
                question_text, question_type, options
            )
            
            return answer
            
        except Exception as e:
            print(f"⚠️ Error getting question answer: {e}")
            return "Yes"  # Default fallback
    
    def _questions_match(self, config_question: str, form_question: str) -> bool:
        """Check if two questions match."""
        try:
            # Simple keyword matching
            config_words = set(config_question.lower().split())
            form_words = set(form_question.lower().split())
            
            # Check if there's significant overlap
            overlap = len(config_words.intersection(form_words))
            return overlap >= 2  # At least 2 words should match
            
        except:
            return False
    
    def _determine_question_type(self, container: Locator) -> str:
        """Determine the type of question."""
        try:
            # Check for radio buttons
            if container.locator("input[type='radio']").count() > 0:
                return "multiple_choice"
            
            # Check for checkboxes
            if container.locator("input[type='checkbox']").count() > 0:
                return "checkbox"
            
            # Check for text input
            if container.locator("input[type='text'], textarea").count() > 0:
                return "text"
            
            # Check for select
            if container.locator("select").count() > 0:
                return "dropdown"
            
            return "text"  # Default
            
        except:
            return "text"
    
    def _extract_question_options(self, container: Locator) -> List[str]:
        """Extract available options for a question."""
        try:
            options = []
            
            # Radio button options
            radio_options = container.locator("input[type='radio']")
            for i in range(radio_options.count()):
                try:
                    option = radio_options.nth(i)
                    label = self._get_field_label(option)
                    if label:
                        options.append(label)
                except:
                    continue
            
            # Checkbox options
            checkbox_options = container.locator("input[type='checkbox']")
            for i in range(checkbox_options.count()):
                try:
                    option = checkbox_options.nth(i)
                    label = self._get_field_label(option)
                    if label:
                        options.append(label)
                except:
                    continue
            
            # Select options
            select_options = container.locator("select option")
            for i in range(select_options.count()):
                try:
                    option = select_options.nth(i)
                    text = option.text_content().strip()
                    if text:
                        options.append(text)
                except:
                    continue
            
            return options
            
        except:
            return []
    
    def _fill_question_answer(self, container: Locator, answer: str, question_text: str):
        """Fill the answer for a question."""
        try:
            # Try different input types
            input_types = ["input[type='radio']", "input[type='checkbox']", "input[type='text']", "textarea", "select"]
            
            for input_type in input_types:
                try:
                    inputs = container.locator(input_type)
                    for i in range(inputs.count()):
                        try:
                            input_field = inputs.nth(i)
                            if not input_field.is_visible():
                                continue
                            
                            # For radio buttons and checkboxes, match by label
                            if input_type in ["input[type='radio']", "input[type='checkbox']"]:
                                label = self._get_field_label(input_field)
                                if answer.lower() in label.lower() or label.lower() in answer.lower():
                                    input_field.check()
                                    print(f"📝 Selected option: {label}")
                                    return
                            
                            # For text inputs, fill directly
                            elif input_type in ["input[type='text']", "textarea"]:
                                input_field.clear()
                                input_field.fill(answer)
                                print(f"📝 Filled text: {answer}")
                                return
                            
                            # For select dropdowns
                            elif input_type == "select":
                                input_field.select_option(answer)
                                print(f"📝 Selected: {answer}")
                                return
                                
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error filling question answer: {e}")
    
    def _find_next_or_submit_button(self) -> Optional[Locator]:
        """Find the next or submit button."""
        try:
            button_selectors = [
                "button[aria-label*='Continue']",
                "button[aria-label*='Next']",
                "button[aria-label*='Submit']",
                "button[aria-label*='Send']",
                "button[aria-label*='Apply']",
                "button:has-text('Continue')",
                "button:has-text('Next')",
                "button:has-text('Submit')",
                "button:has-text('Send')",
                "button:has-text('Apply')",
                "button:has-text('Review')",
                "button:has-text('Finish')"
            ]
            
            for selector in button_selectors:
                try:
                    button = self.page.locator(selector)
                    if button.is_visible():
                        return button
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error finding next button: {e}")
            return None
    
    def _check_application_success(self) -> bool:
        """Check if the application was submitted successfully."""
        try:
            # Look for success indicators
            success_indicators = [
                "application submitted",
                "successfully applied",
                "thank you",
                "application sent",
                "your application has been submitted"
            ]
            
            page_text = self.page.text_content().lower()
            for indicator in success_indicators:
                if indicator in page_text:
                    return True
            
            # Check for specific success elements
            success_elements = self.page.locator("text*='success', text*='submitted', text*='thank you'")
            if success_elements.count() > 0:
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking application success: {e}")
            return False
    
    def _close_easy_apply_modal(self):
        """Close the Easy Apply modal."""
        try:
            # Try to find close button
            close_selectors = [
                "button[aria-label='Dismiss']",
                "button[aria-label='Close']",
                "button:has-text('Close')",
                "button:has-text('Done')",
                ".artdeco-modal__dismiss"
            ]
            
            for selector in close_selectors:
                try:
                    close_button = self.page.locator(selector)
                    if close_button.is_visible():
                        close_button.click()
                        print("✅ Closed Easy Apply modal")
                        return
                except:
                    continue
            
            # Fallback: press Escape key
            self.page.keyboard.press("Escape")
            print("✅ Closed Easy Apply modal (Escape key)")
            
        except Exception as e:
            print(f"⚠️ Error closing modal: {e}")
    
    def get_application_stats(self) -> Dict:
        """Get statistics about applications."""
        return {
            "applied_jobs": len(self.applied_jobs),
            "failed_jobs": len(self.failed_jobs),
            "total_attempted": len(self.applied_jobs) + len(self.failed_jobs)
        }
    
    def export_unseen_questions(self):
        """Export unseen questions for review."""
        self.unseen_questions_handler.export_questions_for_review()
        self.unseen_questions_handler.print_summary()