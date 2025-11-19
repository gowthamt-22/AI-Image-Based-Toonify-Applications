"""
Test script for Toonify Authentication System
Run this to verify all authentication features
"""

from auth import AuthManager
from database import Database
import sys

def test_authentication_system():
    """Comprehensive test suite for authentication system"""
    
    print("=" * 60)
    print("TOONIFY AUTHENTICATION SYSTEM - TEST SUITE")
    print("=" * 60)
    
    auth = AuthManager()
    db = Database()
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    def run_test(test_name, test_func):
        """Helper to run individual tests"""
        test_results['total'] += 1
        print(f"\n[TEST {test_results['total']}] {test_name}")
        try:
            result = test_func()
            if result:
                print("✅ PASSED")
                test_results['passed'] += 1
                return True
            else:
                print("❌ FAILED")
                test_results['failed'] += 1
                return False
        except Exception as e:
            print(f"❌ FAILED with exception: {str(e)}")
            test_results['failed'] += 1
            return False
    
    # Test 1: Email Validation
    def test_email_validation():
        valid, _ = auth.validate_email_format("test@example.com")
        invalid1, _ = auth.validate_email_format("invalid-email")
        invalid2, _ = auth.validate_email_format("@example.com")
        return valid and not invalid1 and not invalid2
    
    run_test("Email Validation", test_email_validation)
    
    # Test 2: Password Strength Validation
    def test_password_strength():
        weak_password, _ = auth.validate_password_strength("weak")
        strong_password, _ = auth.validate_password_strength("Strong@Pass123")
        no_upper, _ = auth.validate_password_strength("weak@pass123")
        no_special, _ = auth.validate_password_strength("WeakPass123")
        return not weak_password and strong_password and not no_upper and not no_special
    
    run_test("Password Strength Validation", test_password_strength)
    
    # Test 3: Username Validation
    def test_username_validation():
        # This will fail if username exists, so we test format only
        valid, errors = auth.validate_username("validuser123")
        too_short, errors1 = auth.validate_username("ab")
        invalid_chars, errors2 = auth.validate_username("user@123")
        starts_with_num, errors3 = auth.validate_username("123user")
        
        # Valid username should pass format checks
        format_valid = len(errors) == 0 or "already taken" in str(errors)
        return format_valid and not too_short and not invalid_chars and not starts_with_num
    
    run_test("Username Validation", test_username_validation)
    
    # Test 4: Password Hashing
    def test_password_hashing():
        password = "TestPassword@123"
        hashed = auth.hash_password(password)
        
        # Hash should be different from original
        different = hashed != password
        
        # Should be able to verify
        verified = auth.verify_password(password, hashed)
        
        # Wrong password should fail
        wrong = not auth.verify_password("WrongPassword", hashed)
        
        return different and verified and wrong
    
    run_test("Password Hashing & Verification", test_password_hashing)
    
    # Test 5: User Registration
    def test_user_registration():
        # Try to register a test user
        success, message, user_id = auth.register_user(
            username="testuser_" + str(test_results['total']),
            email=f"testuser{test_results['total']}@example.com",
            password="TestPass@123",
            full_name="Test User"
        )
        
        if not success:
            print(f"   Registration message: {message}")
        
        return success and user_id is not None
    
    run_test("User Registration", test_user_registration)
    
    # Test 6: Duplicate Registration Prevention
    def test_duplicate_prevention():
        username = "duplicate_test"
        email = "duplicate@example.com"
        
        # First registration
        success1, _, _ = auth.register_user(username, email, "TestPass@123")
        
        # Try duplicate username
        success2, msg2, _ = auth.register_user(username, "other@example.com", "TestPass@123")
        
        # Try duplicate email
        success3, msg3, _ = auth.register_user("other_user", email, "TestPass@123")
        
        return success1 and not success2 and not success3
    
    run_test("Duplicate Registration Prevention", test_duplicate_prevention)
    
    # Test 7: User Login
    def test_user_login():
        # Create a test user for login
        email = "logintest@example.com"
        password = "LoginTest@123"
        
        # Register
        auth.register_user("logintest", email, password)
        
        # Try login
        success, message, user_data = auth.login_user(email, password)
        
        if success:
            print(f"   Logged in as: {user_data['username']}")
        
        return success and user_data is not None
    
    run_test("User Login", test_user_login)
    
    # Test 8: Invalid Login
    def test_invalid_login():
        success, _, _ = auth.login_user("nonexistent@example.com", "WrongPass@123")
        return not success
    
    run_test("Invalid Login Prevention", test_invalid_login)
    
    # Test 9: Database User Retrieval
    def test_database_retrieval():
        # Create and retrieve user
        email = "dbtest@example.com"
        auth.register_user("dbtest", email, "DbTest@123", "Database Test")
        
        user = db.get_user_by_email(email)
        return user is not None and user['email'] == email
    
    run_test("Database User Retrieval", test_database_retrieval)
    
    # Test 10: Failed Login Attempt Tracking
    def test_failed_attempts():
        email = "lockouttest@example.com"
        
        # Create user
        auth.register_user("lockouttest", email, "LockTest@123")
        
        # Make failed attempts
        for i in range(3):
            auth.login_user(email, "WrongPassword")
        
        # Check failed attempts count
        count = db.get_failed_login_attempts(email)
        return count >= 3
    
    run_test("Failed Login Attempt Tracking", test_failed_attempts)
    
    # Print Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {test_results['total']}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"Success Rate: {(test_results['passed']/test_results['total']*100):.1f}%")
    print("=" * 60)
    
    if test_results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! Authentication system is working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(test_authentication_system())
