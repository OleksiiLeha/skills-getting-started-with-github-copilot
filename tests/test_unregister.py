"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""
import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities"""
    
    def test_unregister_existing_participant_success(self, client, reset_activities):
        """AAA: Successfully unregister an existing participant"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known to be registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_removes_only_target_email(self, client, reset_activities):
        """AAA: Unregistering only removes the specified email"""
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        
        activities = client.get("/activities").json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]
    
    def test_unregister_nonexistent_participant_fails(self, client, reset_activities):
        """AAA: Unregistering non-existent participant returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """AAA: Unregistering from non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_twice_fails_second_time(self, client, reset_activities):
        """AAA: Cannot unregister same participant twice"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - First unregister succeeds
        response1 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Second unregister fails
        response2 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
    
    def test_signup_after_unregister_succeeds(self, client, reset_activities):
        """AAA: Can re-register after unregistering"""
        # Arrange
        activity_name = "Drama Club"
        email = "grace@mergington.edu"
        
        # Act - First unregister
        response1 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Then signup again
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
    
    def test_unregister_single_participant_activity(self, client, reset_activities):
        """AAA: Can unregister the only participant from an activity"""
        # Arrange
        activity_name = "Tennis Team"
        email = "lucas@mergington.edu"  # Only participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        activities = client.get("/activities").json()
        assert len(activities[activity_name]["participants"]) == 0
        assert email not in activities[activity_name]["participants"]
