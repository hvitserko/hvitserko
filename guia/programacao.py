import os
import gzip
import xml.etree.ElementTree as ET
import requests

save_as_gz = False  # Set to True to save an additional .gz version

tvg_ids_file = os.path.join(os.path.dirname(__file__), 'id.txt')
output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mylist.xml')
output_file_gz = output_file + '.gz'

def fetch_and_extract_xml(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    if url.endswith('.gz'):
        try:
            decompressed_data = gzip.decompress(response.content)
            return ET.fromstring(decompressed_data)
        except Exception as e:
            print(f"Failed to decompress and parse XML from {url}: {e}")
            return None
    else:
        try:
            return ET.fromstring(response.content)
        except Exception as e:
            print(f"Failed to parse XML from {url}: {e}")
            return None

def filter_and_build_epg(urls):
    with open(tvg_ids_file, 'r') as file:
        valid_tvg_ids = set(line.strip() for line in file)

    root = ET.Element('tv')

    for url in urls:
        epg_data = fetch_and_extract_xml(url)
        if epg_data is None:
            continue

        rename_map = {
            '5f7790b3ed0c88000720b241': 'One Piece eng',
            '5da0c85bd2c9c10009370984': 'Naruto Eng',
        }

        for channel in epg_data.findall('channel'):
            tvg_id = channel.get('id')
            if tvg_id in valid_tvg_ids:
                # Se o ID estiver no dicionário, renomeia o display-name
                if tvg_id in rename_map:
                    for name in channel.findall('display-name'):
                        channel.remove(name)
                    new_display_name = ET.Element('display-name')
                    new_display_name.text = rename_map[tvg_id]
                    channel.append(new_display_name)
                root.append(channel)

        for programme in epg_data.findall('programme'):
            tvg_id = programme.get('channel')
            if tvg_id in valid_tvg_ids:
                title_element = programme.find('title')
                if title_element is not None and title_element.text == "Movie":
                    subtitle_element = programme.find('sub-title')
                    if subtitle_element is not None and subtitle_element.text:
                        title_element.text = subtitle_element.text

                if tvg_id == '624b1c8d4321e200073ee421':
                    desc_element = programme.find('desc')
                    if title_element is not None and desc_element is not None and desc_element.text:
                        title_element.text = desc_element.text.strip()

                if tvg_id == 'OuterMax.east.us' and title_element is not None:
                    date_element = programme.find('date')
                    year = date_element.text.strip() if date_element is not None and date_element.text else None

                    categories = [
                        cat.text.strip()
                        for cat in programme.findall('category')
                        if cat.text and cat.attrib.get('lang') == 'en'
                    ]
                    category = categories[1] if len(categories) > 1 else (categories[0] if categories else None)

                    if year:
                        if category:
                            suffix = f"({year}, {category})"
                        else:
                            suffix = f"({year})"

                        if suffix not in title_element.text:
                            title_element.text = f"{title_element.text.strip()}, {suffix}"

                root.append(programme)
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Salvo em {output_file}")

    if save_as_gz:
        with gzip.open(output_file_gz, 'wb') as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
        print(f"Salvo em {output_file_gz}")
	    
fontes = os.getenv("FONTES")
urls = [
        'https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz',
        'https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz',
        'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/Plex/us.xml',
        'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/br.xml',
        'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/us.xml',
        'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/Roku/all.xml',
        'https://raw.githubusercontent.com/rootcoder/epgtv/main/guide.xml.gz',
        'https://www.open-epg.com/generate/dJMkRZRhTB.xml.gz',
]

if __name__ == "__main__":
    filter_and_build_epg(urls)
