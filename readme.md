# Crawler

## Installation
Install the required python3 packages with pip?

```bash
pip3 install requests beautifulsoup4 html2text
```


## Usage
Set the domain that you want to crawl in the `crawler.py` file.
```python
domain = 'https://livewire.laravel.com'
```

Run the crawler.

```bash
python3 crawler.py
```

## Output
The crawler will output:
- a list of files for each webpage in the markdown_files directory.
- a Markdown file in the one_file directory.

## Create your own OpenAI Assistant
Use the combined markdown file to create your assistant.

## License
MIT License https://opensource.org/license/mit/


