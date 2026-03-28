import requests
import sys
import json
from datetime import datetime

class MultiTaskChatboxTester:
    def __init__(self, base_url="https://carebot-wellness.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:500]}")

            return success, response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_healthcare_chat(self):
        """Test healthcare chat functionality"""
        success, response = self.run_test(
            "Healthcare Chat",
            "POST",
            "chat",
            200,
            data={
                "session_id": self.session_id,
                "message": "I want to lose weight. What exercises do you recommend?",
                "agent_type": "healthcare"
            }
        )
        return success, response

    def test_support_chat(self):
        """Test customer support chat"""
        success, response = self.run_test(
            "Customer Support Chat",
            "POST",
            "chat",
            200,
            data={
                "session_id": self.session_id,
                "message": "I have an issue with my account",
                "agent_type": "support"
            }
        )
        return success, response

    def test_customer_service_chat(self):
        """Test customer service chat"""
        success, response = self.run_test(
            "Customer Service Chat",
            "POST",
            "chat",
            200,
            data={
                "session_id": self.session_id,
                "message": "Can you tell me about your products?",
                "agent_type": "customer_service"
            }
        )
        return success, response

    def test_chat_history(self, agent_type):
        """Test chat history retrieval"""
        return self.run_test(
            f"Chat History - {agent_type}",
            "GET",
            f"chat/history/{self.session_id}/{agent_type}",
            200
        )

    def test_job_application(self):
        """Test job application submission"""
        job_data = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "address": "123 Main St, City, State 12345",
            "position_applied": "Software Developer",
            "education": "Bachelor's in Computer Science",
            "experience": "3 years of web development experience",
            "skills": "Python, JavaScript, React, FastAPI",
            "reference_name": "Jane Smith",
            "reference_contact": "jane.smith@company.com",
            "reference_relationship": "Former Manager"
        }
        return self.run_test(
            "Job Application Submission",
            "POST",
            "job-application",
            200,
            data=job_data
        )

    def test_get_job_applications(self):
        """Test retrieving job applications"""
        return self.run_test(
            "Get Job Applications",
            "GET",
            "job-applications",
            200
        )

    def test_feedback_submission(self):
        """Test feedback submission"""
        feedback_data = {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "rating": 5,
            "category": "service",
            "feedback_text": "Excellent service! Very helpful and responsive."
        }
        return self.run_test(
            "Feedback Submission",
            "POST",
            "feedback",
            200,
            data=feedback_data
        )

    def test_get_feedback(self):
        """Test retrieving feedback"""
        return self.run_test(
            "Get Feedback",
            "GET",
            "feedback",
            200
        )

    def test_appointment_booking(self):
        """Test appointment booking"""
        appointment_data = {
            "patient_name": "Bob Wilson",
            "email": "bob@example.com",
            "phone": "+1987654321",
            "address": "456 Oak Ave, City, State 67890",
            "date_of_birth": "1985-05-15",
            "appointment_date": "2024-12-20",
            "appointment_time": "14:30",
            "reason": "Regular checkup and health consultation",
            "medical_history": "No significant medical history"
        }
        return self.run_test(
            "Appointment Booking",
            "POST",
            "appointments",
            200,
            data=appointment_data
        )

    def test_get_appointments(self):
        """Test retrieving appointments"""
        return self.run_test(
            "Get Appointments",
            "GET",
            "appointments",
            200
        )

def main():
    print("🚀 Starting Multi Task Chatbox API Testing...")
    print("=" * 60)
    
    tester = MultiTaskChatboxTester()
    
    # Test basic connectivity
    print("\n📡 Testing Basic Connectivity...")
    tester.test_root_endpoint()
    
    # Test chat functionality with AI
    print("\n🤖 Testing AI Chat Functionality...")
    healthcare_success, healthcare_response = tester.test_healthcare_chat()
    support_success, support_response = tester.test_support_chat()
    customer_service_success, customer_service_response = tester.test_customer_service_chat()
    
    # Test chat history
    print("\n📚 Testing Chat History...")
    if healthcare_success:
        tester.test_chat_history("healthcare")
    if support_success:
        tester.test_chat_history("support")
    if customer_service_success:
        tester.test_chat_history("customer_service")
    
    # Test form submissions
    print("\n📝 Testing Form Submissions...")
    tester.test_job_application()
    tester.test_feedback_submission()
    tester.test_appointment_booking()
    
    # Test data retrieval
    print("\n📊 Testing Data Retrieval...")
    tester.test_get_job_applications()
    tester.test_get_feedback()
    tester.test_get_appointments()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())