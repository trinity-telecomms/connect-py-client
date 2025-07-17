import pytest
import responses
from unittest.mock import patch, MagicMock

from connect_client.modules.orgs import OrgsAPI
from connect_client.exceptions import ConnectAPIError


class TestOrgsAPI:
    """Test suite for OrgsAPI class"""
    
    def test_init(self, mock_client):
        """Test OrgsAPI initialization"""
        orgs_api = OrgsAPI(mock_client)
        assert orgs_api.client == mock_client
        assert orgs_api._cache == mock_client.cache
    
    def test_get_company_success(self, mock_client, mock_company_response):
        """Test successful company retrieval"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (200, mock_company_response)
            
            result = orgs_api.get_company(1)
            
            assert result == mock_company_response
            mock_request.assert_called_once()
    
    def test_get_company_invalid_id_type(self, mock_client):
        """Test get_company with invalid ID type"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company("invalid")
    
    def test_get_company_invalid_id_zero(self, mock_client):
        """Test get_company with zero ID"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company(0)
    
    def test_get_company_invalid_id_negative(self, mock_client):
        """Test get_company with negative ID"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company(-1)
    
    def test_get_company_not_found(self, mock_client):
        """Test get_company when company not found"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (404, {"error": "Not found"})
            
            with pytest.raises(ConnectAPIError, match="Company with ID 1 not found"):
                orgs_api.get_company(1)
    
    def test_get_company_forbidden(self, mock_client):
        """Test get_company when access forbidden"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (403, {"error": "Forbidden"})
            
            with pytest.raises(ConnectAPIError, match="Insufficient permissions to access company"):
                orgs_api.get_company(1)
    
    def test_get_company_server_error(self, mock_client):
        """Test get_company with server error"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (500, {"error": "Internal server error"})
            
            with pytest.raises(ConnectAPIError, match="API returned status 500"):
                orgs_api.get_company(1)
    
    def test_get_company_unexpected_exception(self, mock_client):
        """Test get_company with unexpected exception"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.side_effect = Exception("Network error")
            
            with pytest.raises(ConnectAPIError, match="Failed to get company from Connect API: Network error"):
                orgs_api.get_company(1)
    
    def test_get_company_folders_success(self, mock_client, mock_company_folders_response):
        """Test successful company folders retrieval"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (200, mock_company_folders_response)
            
            result = orgs_api.get_company_folders(1)
            
            assert result == mock_company_folders_response
            mock_request.assert_called_once()
    
    def test_get_company_folders_with_filters(self, mock_client, mock_company_folders_response):
        """Test company folders retrieval with filters"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (200, mock_company_folders_response)
            
            filters = {"active": True, "limit": 10}
            result = orgs_api.get_company_folders(1, **filters)
            
            assert result == mock_company_folders_response
            mock_request.assert_called_once()
            # Check that params were passed correctly
            call_args = mock_request.call_args
            assert call_args[1]['params'] == filters
    
    def test_get_company_folders_invalid_id_type(self, mock_client):
        """Test get_company_folders with invalid ID type"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders("invalid")
    
    def test_get_company_folders_invalid_id_zero(self, mock_client):
        """Test get_company_folders with zero ID"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders(0)
    
    def test_get_company_folders_invalid_id_negative(self, mock_client):
        """Test get_company_folders with negative ID"""
        orgs_api = OrgsAPI(mock_client)
        
        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders(-1)
    
    def test_get_company_folders_not_found(self, mock_client):
        """Test get_company_folders when company not found"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (404, {"error": "Not found"})
            
            with pytest.raises(ConnectAPIError, match="Company with ID 1 not found"):
                orgs_api.get_company_folders(1)
    
    def test_get_company_folders_forbidden(self, mock_client):
        """Test get_company_folders when access forbidden"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (403, {"error": "Forbidden"})
            
            with pytest.raises(ConnectAPIError, match="Insufficient permissions to access company folders"):
                orgs_api.get_company_folders(1)
    
    def test_get_company_folders_server_error(self, mock_client):
        """Test get_company_folders with server error"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (500, {"error": "Internal server error"})
            
            with pytest.raises(ConnectAPIError, match="API returned status 500"):
                orgs_api.get_company_folders(1)
    
    def test_get_company_folders_non_list_response(self, mock_client):
        """Test get_company_folders with non-list response"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.return_value = (200, {"error": "Invalid response"})
            
            result = orgs_api.get_company_folders(1)
            
            assert result == []
    
    def test_get_company_folders_unexpected_exception(self, mock_client):
        """Test get_company_folders with unexpected exception"""
        orgs_api = OrgsAPI(mock_client)
        
        with patch.object(orgs_api, 'make_get_request') as mock_request:
            mock_request.side_effect = Exception("Network error")
            
            with pytest.raises(ConnectAPIError, match="Failed to get company folders from Connect API: Network error"):
                orgs_api.get_company_folders(1)
    
    def test_url_generation(self, mock_client):
        """Test URL generation for endpoints"""
        orgs_api = OrgsAPI(mock_client)
        
        from connect_client.modules.orgs.constants import PATH_MAP
        
        with patch.object(orgs_api, '_generate_url') as mock_generate:
            mock_generate.return_value = "https://api.example.com/api/v4/orgs/company/1/"
            
            with patch.object(orgs_api, 'make_get_request') as mock_request:
                mock_request.return_value = (200, {"id": 1})
                
                orgs_api.get_company(1)
                
                mock_generate.assert_called_once_with(
                    "company_by_id", 
                    PATH_MAP, 
                    company_id=1
                )