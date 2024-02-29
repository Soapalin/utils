from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import sys
from selenium_stealth import stealth
import random
import pypub

class WebNovelScraper:
    def __init__(self, first_chapter_link, title):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(1)

        stealth(self.driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

        self.first_chapter_link = first_chapter_link
        self.pdf_title = title
        self.epub = pypub.Epub(title)


    def driver_quit(self):
        self.driver.quit()

    def try_find_element(self,element, by=By.CSS_SELECTOR, value=""):
        try:
            result = element.find_element(by, value)
        except Exception as e:
            print(e)
            return ""
        else:
            return result

    def write_to_epub(self, ch_title, ch_content):
        chapter = pypub.create_chapter_from_text(ch_content, title=ch_title)

        # css = pypub.add_argument.('body { font-size: 14pt; }')
        self.epub.add_chapter(chapter)


    def get_n_chapters(self, start_chapter, nb_of_ch):
        # Open the SEEK website

        self.driver.get(self.first_chapter_link)

        for ch in range(nb_of_ch):
            ch_title = self.try_find_element(self.driver, by=By.CLASS_NAME, value="chr-title")
            if ch_title != "":
                print(ch_title.text)
                ch_title = ch_title.text
            ch_content = self.try_find_element(self.driver, by=By.ID, value="chr-content")
            if ch_content != "":
                ch_content = ch_content.text

            self.write_to_epub(ch_title, ch_content)

            next_ch_btn = self.driver.find_element(by=By.ID, value="next_chap_top")
            next_ch_btn.click()
            time.sleep(random.randint(3,4))


        self.epub.create(self.pdf_title + start_chapter + "-" + str(int(start_chapter) + nb_of_ch) + ".epub")


title="GlobalLord100DropRate"

web_nov = WebNovelScraper(first_chapter_link="https://novelnextz.com/novelnextz/global-lord-100-drop-rate/cchapter-201-201-secret-of-the-undead-kingdom-world-channel-lord-announcement", title=title)

# web_nov.write_to_pdf(chapter_range="1-100", ch_title="TEST", ch_content="HELLO WORLD")
web_nov.get_n_chapters("200", 200)