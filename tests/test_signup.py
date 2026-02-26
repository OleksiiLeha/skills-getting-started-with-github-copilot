"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities"""
    
    def test_signup_new_participant_success(self, client, reset_activities):
        """AAA: Successfully sign up a new participant"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]
    
    def test_signup_with_special_characters_in_name(self, client, reset_activities):
        """AAA: Sign up for activity with special characters in name"""
        # Arrange
        activity_name = "Programming Class"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert email in client.get("/activities").json()[activity_name]["participants"]
    
    def test_signup_duplicate_email_fails(self, client, reset_activities):
        """AAA: Attempting duplicate signup returns 400 error"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """AAA: Signing up for non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_multiple_different_activities(self, client, reset_activities):
        """AAA: Same student can sign up for multiple activities"""
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Drama Club"
        
        # Act
        response1 = client.post(f"/activities/{activity1}/signup?email={email}")
        response2 = client.post(f"/activities/{activity2}/signup?email={email}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
    
    def test_signup_with_various_email_formats(self, client, reset_activities):
        """AAA: Signup works with valid email formats"""
        # Arrange
        activity_name = "Science Club"
        emails = [
            "john.doe@mergington.edu",
            "jane123@mergington.edu",
            "student+tag@mergington.edu"
        ]
        
        # Act
        import urllib.parse
        for email in emails:
            encoded = urllib.parse.quote(email, safe='')
            response = client.post(
                f"/activities/{activity_name}/signup?email={encoded}"
            )
            
            # Assert
            assert response.status_code == 200
        
        # Verify all were added
        activities = client.get("/activities").json()
        for email in emails:
            assert email in activities[activity_name]["participants"]
    
    def test_signup_updates_participants_list_immediately(self, client, reset_activities):
        """AAA: New participant appears in activities list immediately"""
        # Arrange
        activity_name = "Tennis Team"
        email = "newtennis@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Check count increased
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
