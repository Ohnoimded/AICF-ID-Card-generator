import unittest
from unittest.mock import Mock, patch
from AicfCardGenerator.ProfileScraper import profile_scraper

class TestProfileScraper(unittest.TestCase):

    @patch('AicfCardGenerator.ProfileScraper.requests.get')
    def test_scrape_profile_from_api(self, mock_requests_get):
        self.scraper = profile_scraper

        # Mock the response from the API for testing
        mock_response = {
            "player": {
                "id": 123456,
                "first_name": "John Smith",
                "middle_name": None,
                "last_name": "Smithson",
                "email": "*****",
                "mother_tounge": "Malayalam",
                "player_type": "player",
                "address": "******",
                "city": "1234",
                "district": "1234",
                "state": "12",
                "mobile": "9********9",
                "gender": "M",
                "poi": 0,
                "date_of_birth": "2000",
                "fide_id": None,
                "aicf_id": "123456KL2023",
                "type": 1
            },
            "photo": {
                "id": 123456,
                "entity_id": 123456,
                "entity": "contact_passport_photo",
                "thumb": None,
                "small": None,
                "medium": None,
                "large": "https://assets.aicf.in/contacts/large/6f73f8c3-c166-4861-97f1-cdsdfsdfsdf.png",
                "original": "https://assets.aicf.in/contacts/large/6f73f8c3-c166-4861-97f1-cdsdfsdfsdf.png",
                "default": 0,
                "status": 1,
                "created_at": "2023-08-09 21:19:28"
            },
            "membership_status": True,
            "membership_expire_at": "2024-03-31T23:59:59.000000Z",
            "order_status": 1,
            "location": {
                "city_name": "Kochi",
                "district_name": "Kochi",
                "state_name": "Kerala"
            }
        }

        # Configure the mock_requests_get to return the mock_response
        mock_requests_get.return_value.json.return_value = mock_response

        # Test scraping profile using the mock response
        profile_data = self.scraper.scrape_profile_from_api("123456KL2023")

        # Expected profile data based on the mock response
        expected_data = {
            "url": "https://prs.aicf.in/players/123456KL2023",
            "Image": "https://assets.aicf.in/contacts/large/6f73f8c3-c166-4861-97f1-cdsdfsdfsdf.png",
            "AICF ID": "123456KL2023",
            "FIDE ID": "",
            "Name": "John Smith Smithson",
            "Gender": "M",
            "Age": "23",  
            "State": "Kerala",
            "Registration Type": "Player",
            "Valid Upto": "2024-03-31"
        }

        self.assertEqual(profile_data, expected_data, msg="Success")

if __name__ == '__main__':
    unittest.main()
