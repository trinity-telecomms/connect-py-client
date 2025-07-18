from connect_client.exceptions.error_responses import ErrorResponse


class TestErrorResponse:
    """Test suite for ErrorResponse factory class"""
    
    def test_not_found_response(self):
        """Test not found error response creation"""
        response = ErrorResponse.not_found("Company")
        
        assert response == {
            "error": "not_found",
            "message": "Company not found",
            "status_code": 404
        }
    
    def test_unauthorized_response(self):
        """Test unauthorized error response creation"""
        response = ErrorResponse.unauthorized()
        
        assert response == {
            "error": "unauthorised",
            "message": "Unauthorised request",
            "status_code": 401
        }
    
    def test_api_error_response(self):
        """Test API error response creation"""
        response = ErrorResponse.api_error()
        
        assert response == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500
        }