import argparse
import glob
import markdown2
import os
import re
import hashlib
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def parse_hugo_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    parts = re.split(r'---\s*', content)
    metadata = parts[1]
    body = parts[2]

    meta_dict = {}
    for line in metadata.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            meta_dict[key.strip()] = value.strip()

    html_body = markdown2.markdown(body)

    return meta_dict, html_body

def create_guid(file_path, date):
    hash_input = f"{file_path}-{date}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

def create_wxr_element(meta_data, html_content, file_path):
    item = Element('item')
    title = SubElement(item, 'title')
    pubDate = SubElement(item, 'pubDate')
    creator = SubElement(item, 'dc:creator')
    guid = SubElement(item, 'guid', isPermaLink="false")
    content_encoded = SubElement(item, 'content:encoded')
    category = SubElement(item, 'category')

    title.text = meta_data.get('title', 'No Title')
    pubDate.text = datetime.strptime(meta_data.get('date', ''), "%Y-%m-%d %H:%M:%S %z").strftime("%a, %d %b %Y %H:%M:%S %z")
    creator.text = os.getenv('HUGO_WXR_CREATOR', 'admin')
    
    guid_text = create_guid(file_path, meta_data.get('date', ''))
    guid_base = os.getenv('HUGO_WXR_GUID', 'http://example.com/')
    guid.text = f"{guid_base}{guid_text}"

    content_encoded.text = html_content
    category.text = meta_data.get('categories', ['Uncategorized'])[0]

    return item

def create_wxr_document(items):
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')

    channel = SubElement(rss, 'channel')
    for item in items:
        channel.append(item)

    return minidom.parseString(tostring(rss)).toprettyxml(indent="   ")

def process_hugo_directory(content_dir):
    markdown_files = glob.glob(content_dir + '/**/*.md', recursive=True)
    wxr_items = []

    for file_path in markdown_files:
        try:
            meta_data, html_content = parse_hugo_markdown(file_path)
            wxr_item = create_wxr_element(meta_data, html_content, file_path)
            wxr_items.append(wxr_item)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    return wxr_items

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Hugo content to WordPress WXR format.")
    parser.add_argument('content_dir', help="Path to the Hugo content directory.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    wxr_items = process_hugo_directory(args.content_dir)
    wxr_document = create_wxr_document(wxr_items)

    print(wxr_document)

if __name__ == "__main__":
    main()
