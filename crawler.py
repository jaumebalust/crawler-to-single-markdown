import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import html2text


# Set the domain to crawl
domain = "https://livewire.laravel.com"


# DON'T CHANGE ANYTHING BELOW THIS LINE

# Set up a list to save the urls to visit
to_crawl = set()
# Set up a list to save the urls already visited
crawled = set()
# The domain you want to crawl

root = urlparse(domain).netloc.split('.')[0]


# Directory where you want to save the markdown files
output_dir = "markdown_files/"+root

# Initialize the HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.ignore_emphasis = False

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_links(url):
    """Returns a list of links from the given webpage"""
    page_links = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
             
            #check that links are not external links
            linkCandidate = urljoin(url, href)
            if href and linkCandidate.startswith(domain):
                print(f"Found link: {linkCandidate}")
                page_links.append(linkCandidate)

                
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting {url}: {e}")
    return page_links

def crawl(url):
    """Crawl a web page and extract other page links."""

    print(f"Crawling: {url}")
    

    # Remove the url from the to_crawl only if it's there and add it to crawled if it's not there

    if url in to_crawl:
        to_crawl.remove(url)
    
    if url not in crawled:
        crawled.add(url)

    # Get links from the webpage
    for link in get_links(url):
        # check that urlparse(url).netloc is contained in domain
        if link not in crawled and link not in to_crawl:
            
            #if link ends with pdf, don't add it to to_crawl
            if link.endswith('.pdf'):
                print(f"Found pdf link: {link}")
            else:
                to_crawl.add(link)

    # Save the page as Markdown
    save_as_markdown(url)

def save_as_markdown(url):
    """Save the given webpage as a markdown file"""
    try:
        response = requests.get(url)
        html = response.text
        markdown = converter.handle(html)
        # Create a valid filename from the URL
        filename = urlparse(url).path.strip('/').replace('/', '_')
        if not filename:
            filename = 'index'
        filename += '.md'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Saved Markdown: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting {url}: {e}")

# Start crawling the website from the root
to_crawl.add(domain)
while to_crawl:
    crawl(to_crawl.pop())

print("Finished crawling.")

import os

def combine_markdown_files(input_dir, output_dir, output_filename):
    """
    Combine all markdown files in the input_dir into one markdown file in output_dir.
    
    :param input_dir: Directory containing the markdown files to combine
    :param output_dir: Directory where the combined markdown file will be saved
    :param output_filename: The name of the combined markdown output file
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Combine markdown files
    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as outfile:
        # Walk through the input directory
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                # Check for markdown files
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    # Write the content of each markdown file into the combined file
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read() + '\n\n')

    print(f"All markdown files have been combined into {os.path.join(output_dir, output_filename)}")

# Example usage:
input_directory = output_dir  # Directory where your markdown files are stored
output_directory = 'one_file/'+root       # Directory where the combined markdown file should be stored
output_file_name = root+'.md'    # Name of the combined markdown file

combine_markdown_files(input_directory,output_directory , output_file_name)
