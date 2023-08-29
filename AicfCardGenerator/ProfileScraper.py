import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests

# Exception for wrong AICF Reg. no.
class AICFRegistrationError(Exception):
    def __init__(self, message="Player not found! Please enter valid AICF ID"):
        self.message = message
        super().__init__(self.message)

class ProfileScraper:
    def __init__(self):
        pass

    # Optional method to save a CSV file of all the accessed profiles
    # ONLY FOR TESTING
    def save_to_csv(self, profile_data):
        df = pd.DataFrame([profile_data])
        csv_file = "data/profile_data.csv"
        df.to_csv(csv_file, mode='a', index=False, header=False)  # Save DataFrame to CSV

    # Optional profile image saving method. 
    # ONLY FOR TESTING  
    def save_img(self, profile_data):
        f = open('images/profile.png', 'wb')
        f.write(requests.get(profile_data).content)
        f.close()

    # USE ONLY THIS WHEN YOU IMPORT THIS MODULE IN OTHER PROGRAMS Only to select between methods. 
    # If with_api=False, the website scarping will run. NOT RECOMMENDED
    def scrape_profile(self, id, with_api=True):
        if with_api:
            data = self.scrape_profile_from_api(id)
            self.save_to_csv(data)
            return data
        else:                                       # NOT RECOMMENDED
            data = self.scrape_profile_from_website(id)
            self.save_to_csv(data)
            return data

    # Default: Scrapes with the AICF API
    def scrape_profile_from_api(self, id):
        url = f"https://admin.aicf.in/api/aicfid/{id}"
        try:
            response = requests.get(url=url)

            if response.status_code ==422:
                raise AICFRegistrationError("Player not found! Please enter valid AICF ID")
            response.raise_for_status()
            data = response.json()
        

            # To check if the profile has validity or not
            if data['membership_status'] == False:
                validity = 'Expired'
            else:
                validity=datetime.strptime(data['membership_expire_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
            
            # For some profiles, year of birth is not provided. This handles that
            if data['player']['date_of_birth']==None:
                age=''
            else:
                age=str(datetime.today().year - int(data['player']['date_of_birth']))

            # Handling names with middle name
            name = data['player']['first_name'] + \
                ' ' + data['player']['last_name']
            if data['player']['middle_name']:
                name = data['player']['first_name'] + ' '+\
                    data['player']['middle_name'] + ' ' +data['player']['last_name']
                
            profile_data = {
                "url":f"https://prs.aicf.in/players/{id}",
                "Image": data['photo']['large'],
                "AICF ID": data['player']['aicf_id'],
                "FIDE ID": "",
                "Name": name,
                "Gender": data['player']['gender'],
                "Age": age,
                "State": data['location']['state_name'],
                "Registration Type": data['player']['player_type'].title(),
                "Valid Upto": validity
            }

            # Some profiles have a FIDE ID, most don't. This part handles that for the profile_data
            fide_id=data['player']['fide_id']
            if fide_id is not None:
                profile_data['FIDE ID']=fide_id                

            # Optional save profile image. 
            # ONLY FOR TESTING
            # self.save_img(profile_data['Image']) 
            return profile_data
        
        except requests.exceptions.RequestException as req_err:
            raise AICFRegistrationError("An error occurred during API request: {}".format(req_err))

    # UNSTABLE scraping method. NEVER USE IT unless the API is not accesible and is only for internal use at AICF
    # Not going to be tested
    def scrape_profile_from_website(self, id):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options)
        url = f"https://prs.aicf.in/players/{id[0:-6]}"
        
        # The main scraping part
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 15)

            button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".ant-btn.ant-btn-primary.ant-btn-lg")))
            button.click()

            # Wait for the profile info to appear after clicking the button
            profile_info = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".ant-descriptions-row")))

            # Find all div elements with the specified class and structure
            div_elements = self.driver.find_elements(
                By.CSS_SELECTOR, ".ant-row > .ant-col.ant-col-8")

            try:
                if len(div_elements) >= 2:
                    second_div_element = div_elements[1]
                    image_element = second_div_element.find_element(
                        By.TAG_NAME, "img")

                    image_src = image_element.get_attribute("src")
                    # print("Image Source:", image_src)
            except:
                print("Profile Image not found")
                image_src = ""
            print(profile_info[6].text)
            try:
                age=str(datetime.today().year - int(profile_info[2].text.split(' ')[-1]))
            except:
                age=''

            profile_data = {
                "url":f"https://prs.aicf.in/players/{id}",
                "Image": image_src,
                "AICF ID": profile_info[5].text.split(' ')[-1],
                "FIDE ID": profile_info[4].text.split(' ')[-1],
                "Name": "",
                "Gender": profile_info[2].text.split(' ')[1],
                "Age": age,
                "State": "",
                "Registration Type": "",
                "Valid Upto": ""
            }

            if profile_data['FIDE ID'] == 'ID':
                profile_data['FIDE ID'] = ""

            # Adding data to the dict after splitting the strings
            for i in range(len(profile_info)):
                temp = profile_info[i].text.split('\n')
                if len(temp) > 1 and temp[0] in profile_data:
                    profile_data[temp[0]] = temp[1]
            profile_data["Registration Type"] = profile_data["Registration Type"].title()

        except self.AICFRegistrationError:
            return None
        finally:
            self.driver.quit()

        # self.save_img(profile_data['Image'])
        return profile_data


profile_scraper = ProfileScraper()

if __name__ == "__main__":
    # Profile ID to scrape
    id = 'your_aicf_id'

    # Scrape profile data using API
    data_api = profile_scraper.scrape_profile(id, with_api=True)
    print("Data from API:", data_api)

    # # Scrape profile data from website
    # data_website = profile_scraper.scrape_profile(id, with_api=False)
    # print("Data from Website:", data_website)