import yaml
import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# Load YAML
with open("podcast.yaml", "r") as f:
    podcast = yaml.safe_load(f)

# Create the root element
rss = Element("rss", version="2.0", attrib={"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
channel = SubElement(rss, "channel")

# Basic channel-level tags
SubElement(channel, "title").text = podcast["title"]
SubElement(channel, "itunes:subtitle").text = podcast["subtitle"]
SubElement(channel, "itunes:author").text = podcast["author"]
SubElement(channel, "description").text = podcast["description"]
SubElement(channel, "itunes:image", href=podcast["image"])
SubElement(channel, "language").text = podcast["language"]
SubElement(channel, "itunes:category", text=podcast["category"])

# Each item (episode)
for episode in podcast["item"]:
    item = SubElement(channel, "item")
    SubElement(item, "title").text = episode["title"]
    SubElement(item, "description").text = episode["description"]
    SubElement(item, "pubDate").text = episode["published"]
    
    # Add enclosure (media file)
    SubElement(item, "enclosure", attrib={
        "url": episode["file"],
        "length": episode["length"].replace(",", ""),  # Remove commas from numbers
        "type": podcast["format"]
    })
    
    SubElement(item, "itunes:duration").text = episode["duration"]

# Save RSS XML to file
tree = ElementTree(rss)
tree.write("podcast.xml", encoding="utf-8", xml_declaration=True)

print("✅ RSS feed generated as podcast.xml")
