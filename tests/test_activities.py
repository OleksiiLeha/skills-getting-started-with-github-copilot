"""Tests for GET /activities endpoint using AAA pattern"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""
    
    def test_get_all_activities_returns_success(self, client, reset_activities):
        """AAA: Get all activities and verify response"""
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count
    
    def test_activities_contain_required_fields(self, client, reset_activities):
        """AAA: Verify activity objects have required structure"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_activities_have_initial_participants(self, client, reset_activities):
        """AAA: Verify some activities have pre-populated participants"""
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert activities["Chess Club"]["participants"] == expected_chess_participants
    
    def test_activities_respect_max_participants(self, client, reset_activities):
        """AAA: Verify max_participants is properly set"""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert activities["Chess Club"]["max_participants"] == 12
        assert activities["Programming Class"]["max_participants"] == 20
        assert activities["Basketball League"]["max_participants"] == 20
