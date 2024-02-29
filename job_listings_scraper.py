from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import sys 
from selenium_stealth import stealth

class Job:
    def __init__():
        pass

class JobScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(0.5)

        stealth(self.driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


        self.all_jobs = []
        self.all_jobs_csv = ["jobTitle,jobCompany,jobLocation,jobListingDate"]

    def reset_job_struct(self):
        self.all_jobs = []
        self.all_jobs_csv = ["jobTitle,jobCompany,jobLocation,jobListingDate"]


    def driver_quit(self):
        self.driver.quit()


    def save_jobs_to_csv(self,filename):
        now = datetime.datetime.today().strftime("%w_%b_%Y_%H_%M_%S")
        with open(filename + now + ".csv", "w") as f:
            for job in self.all_jobs_csv:
                f.write(job + "\n")

    def try_find_element(self,element, by=By.CSS_SELECTOR, value=""):
        try:
            result = element.find_element(by, value)
        except Exception as e:
            print(e)
            return ""
        else:
            return result
        



    def get_SEEK_jobs(self, searchLocation="Sunshine Coast"):
        # Open the SEEK website
        self.driver.get('https://www.seek.com.au/')


        keyword = self.driver.find_element(by=By.ID, value="keywords-input")

        keyword.send_keys("Software Engineer")
        location = self.driver.find_element(by=By.ID, value= "SearchBar__Where")
        location.send_keys(searchLocation)

        submitButton = self.driver.find_element(by=By.ID, value="searchButton")
        submitButton.click()

        job_divs = self.driver.find_elements(by=By.TAG_NAME, value="article")
        for job in job_divs:
            print("===============")
            jobTitle = job.find_element(By.CSS_SELECTOR, "[data-automation='jobTitle']")
            print(jobTitle.text)
            jobCompany = self.try_find_element(job, By.CSS_SELECTOR, "[data-automation='jobCompany']")
            if jobCompany != "":
                print(jobCompany.text)
                jobCompany = jobCompany.text
            else:
                print("No Job Company")
            jobListingDate = self.try_find_element(job, By.CSS_SELECTOR, "[data-automation='jobListingDate']")
            if jobListingDate != "":
                print(jobListingDate.text)
                jobListingDate = jobListingDate.text
            else:
                print("No Job Listing Date")
            jobLocation = job.find_element(By.CSS_SELECTOR, "[data-automation='jobLocation']")
            print(jobLocation.text)
            # print(jobSalary.text)
            jobDescription = job.find_element(By.CSS_SELECTOR, "[data-automation='jobShortDescription']")
            print(jobDescription.text)
            benefits = job.find_elements(By.TAG_NAME, value="li")
            jobBenefits = ""
            for ben in benefits:
                print(ben.text)
                jobBenefits = jobBenefits + ben.text + "\\n"

            

            self.all_jobs.append({
                'jobTitle': "\"" + jobTitle.text + "\"",
                'jobCompany': "\"" + jobCompany + "\"",
                'jobListingDate': "\"" + jobListingDate + "\"",
                'jobLocation': "\"" + jobLocation.text + "\"",
                'jobDescription': "\"" + jobDescription.text + "\"",
                'jobBenefits': "\"" + jobBenefits + "\"",
            })
            self.all_jobs_csv.append(f"\"{jobTitle.text}\",\"{jobCompany}\",\"{jobLocation.text}\",\"{jobListingDate}\",\"{jobDescription.text}\",\"{jobBenefits}\"")
        self.save_jobs_to_csv(filename=f"SEEK_jobs_{searchLocation}_")
        self.reset_job_struct()

    def get_INDEED_jobs(self, searchLocation="Sunshine Coast QLD"):
        self.driver.get('https://au.indeed.com/')

        what = self.driver.find_element(by=By.ID, value="text-input-what")
        time.sleep(1)
        what.send_keys("Software Engineer")
        time.sleep(1)
        where = self.driver.find_element(by=By.ID, value="text-input-where")
        where.send_keys(searchLocation)
        time.sleep(1)

        submitButton = self.driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
        submitButton.click()
        time.sleep(3)

        allResults = self.driver.find_elements(By.CLASS_NAME, "cardOutline")
        for res in allResults:
            jobTitle = res.find_element(By.CLASS_NAME, "jobTitle").text
            print(jobTitle)

            jobCompany = res.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
            print(jobCompany)

            descriptions = res.find_elements(By.TAG_NAME, "li")
            print(len(descriptions))
            jobDescription = ""
            for des in descriptions:
                jobDescription = jobDescription + des.text + "\\n"

            print(jobDescription)

            self.all_jobs_csv.append(f"\"{jobTitle}\",\"{jobCompany}\",{searchLocation},,\"{jobDescription}\",")

        self.save_jobs_to_csv(filename=f"INDEED_jobs_{searchLocation}_")





job_scraper = JobScraper()

# job_scraper.get_INDEED_jobs()
job_scraper.get_SEEK_jobs()


# time.sleep(30)
job_scraper.driver_quit()