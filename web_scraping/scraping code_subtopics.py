import csv
import re
import requests
from bs4 import BeautifulSoup

class WebScrapping:
    
    def __init__(self, urls):
        self.urls = urls

    def get_subtopics(self, soup):
        subtopics = []
        # Find all h2 tags which are considered subtopics
        # Stop scraping after finding FAQs, using regex for that
        pattern = re.compile(r"^frequently-asked-.*")
        for h2 in soup.find_all("h2"):
            h2_id = h2.get("id") 
            if h2_id and pattern.match(h2_id):
                break
            
            subtopic_title = h2.text.strip()
            description = []
            code_snippets = []
            
            next_element = h2.find_next_sibling(["p", "ul", "gfg-tabs", "h2"])
            
            while next_element:
                if next_element.name in ["p", "ul"]:
                    description.append(next_element.get_text(separator=" ").strip())
                elif next_element.name == "gfg-tabs":
                    python_panels = next_element.find_all("gfg-panel", {"data-code-lang": "python3"})
                    for panel in python_panels:
                        div_tag = panel.find("div")
                        if div_tag:
                            code_snippets.append(div_tag.text.strip())
                elif next_element.name == "h2":
                    break
                next_element = next_element.find_next_sibling(["p", "ul", "code", "gfg-tabs", "h2"])
                
            subtopics.append((subtopic_title, " ".join(description), "\n".join(code_snippets)))

        return subtopics

    def scrape(self):
        all_subtopics = []

        for url in self.urls:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            subtopics = self.get_subtopics(soup)
            all_subtopics.extend(subtopics)
        
        return all_subtopics

    def write_to_csv(self, subtopics, file_path):
        with open(file_path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Subtopic", "Description", "Code Snippets"])
            writer.writerows(subtopics)

        print(f"Data successfully written to {file_path}")

# Define URLs

#reading from CSV files
urls = []
with open("E:\\Downloads\\GFG Links - Sheet1.csv", mode='r')as file:
    csvFile = csv.reader(file)
    for row in csvFile:
        urls.append(row[0]) #row[0] refers as first column of a csv file


# Instantiate and run scraper
scraper = WebScrapping(urls)
subtopics = scraper.scrape()
csv_file = "C:\\Users\\ntaba\\OneDrive\\Documents\\subtopics.csv"
scraper.write_to_csv(subtopics, csv_file)
