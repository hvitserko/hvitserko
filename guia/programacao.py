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


        desc_ids = {
                '624b1c8d4321e200073ee421',
                '65d9167818036500080e8780',
                '5f6df5a173d7340007c559f7',
                '625464a945b6a200079257d1',
                '65df71008b24c80008f04281',
                '65df704366eec8000898e32f',
                '65df713dec9fda0008b7a81d',
                '65df70b0f7f0af0008c3b316',
                '609ae66b359b270007869ff1',
                '5f7790b3ed0c88000720b241',
                '5da0c85bd2c9c10009370984',
                '62fa8176b9884200074ef5ae'
        }

        category_map = {
            'Sci-Fi': 'Science fiction',
            'Rom-Com': 'Romantic comedy',
            'Doc': 'Documentary',
        }

        special_tvg_ids = {
            'OuterMax.east.us',
            'Showtime.Extreme.-.Eastern.us',
            'Showtime.Women.HD.-.Eastern.us',
            'MGM+.HDTV.(East).(MGM+HD).us',
            'MGM+.Hits.HDTV.(East).(MGM+HTHD).us',
            'MGM+.Drive-In.(MGM+DI).us',
            'Crave2.-.East.ca',
            'Crave4.ca',
            'Lifetime.Movies.-.East.us',
            'Paramount.Network.USA.-.Eastern.Feed.us',
            'Hallmark.Drama.HDTV.(HALDRHD).us'
            '5f120e94a5714d00074576a1',
            '5f120f41b7d403000783a6d6',
            '61b790b985706b00072cb797',
            '5f12101f0b12f00007844c7c',
            '62545ed3dab4380007582f7c',
            '5f1210d14ae1f80007bafb1d',
            '633dcebd80386500074a2461',
            '5f171f988ab9780007fa95ea',
            '5f171d3442a0500007362f22',
            '6479ff764f5ba5000878dfe2',
            '5f12111c9e6c2c00078ef3bb',
            '5fa15ad6367e170007cdd098',
            '5f5a545d0dbf7f0007c09408',
            '5fa1612a669ba0000702017b',
            '5fa991b1f09e020007e78626',
            '5f171f032cd22e0007f17f3d',
            '62c5d32e2c48f9000715b6e9',
            '4675',
            '6800',
            '6802',
            '4677',
            '6806',
            '6804',
            '5ba3fb9c4b078e0f37ad34e8',
            '64b585f84ea480000838e446',
            '561d7d484dc7c8770484914a',
            '617b37b361e0fd0008cfd8c5',
            '5a4d3a00ad95e4718ae8d8db',
            '5b4e92e4694c027be6ecece1',
            '5b64a245a202b3337f09e51d',
            '5a66795ef91fef2c7031c599',
            '5f4d8594eb979c0007706de7',
            '5b4e69e08291147bd04a9fd7',
            '569546031a619b8f07ce6e25',
            '5c6dc88fcd232425a6e0f06e',
            '58af4c093a41ca9d4ecabe96',
            '663946c1b18d700008d9c168',
            '645e7828e1979c00087b75b4',
            '5f4d863b98b41000076cd061',
            '62ba60f059624e000781c436',
            '5f4d86f519358a00072b978e',
            '5ca525b650be2571e3943c63',
            '5f4d878d3d19b30007d2e782',
            '5cb0cae7a461406ffe3f5213',
            '5b4e94282d4ec87bdcbb87cd',
            '61f33318210549000806a530',
            '561c5b0dada51f8004c4d855',
            '5c665db3e6c01b72c4977bc2',
            '65a9b20f0c7ff50008d3a3b6',
            '58e55b14ad8e9c364d55f717',
            '5e20b730f2f8d5003d739db7-5fc705e2a2236e002d69f36d',
            '5e20b730f2f8d5003d739db7-5f6142d2fc6ce20041ec3c92',
            '5e20b730f2f8d5003d739db7-5fc705e2a2236e002d69f3ba',
            '5e20b730f2f8d5003d739db7-627e347795b0f50af26d78f9',
            '5e20b730f2f8d5003d739db7-62b45f15b4508e0eedacdf26',
            '604b79c558393100078faeef',
            '5f6df5a173d7340007c559f7',
            '64c92f965580090008084968',
            '656f389c3944b60008e5bdab',
            '65d9167818036500080e8780',
            '625464a945b6a200079257d1',
            '63988c2750108d00072e2686',
            '63988a50be012600070f5db3',
            '646663b01593940008990a57',
            '633dc392e0282400071b0d39',
            '624b1c8d4321e200073ee421',
            '5ff609de50ab210008025c1b',
            '65df71008b24c80008f04281',
            '65df704366eec8000898e32f',
            '65df713dec9fda0008b7a81d',
            '65df70b0f7f0af0008c3b316',
            '609ae66b359b270007869ff1',
            '5812b7d3249444e05d09cc49',
            '65652f7fc0fc88000883537a',
            '637e55347427a40007fac703',
            '5f7790b3ed0c88000720b241',
            '5da0c85bd2c9c10009370984',
            '5f4ec10ed9636f00089b8c89',
            '60f74ba51c82ac000776c669',
            '660d7268e8fba80008521de8',
            '7bdac47dd6dd5204b00b1d0e4cbc9684',
            'bdf6b34e48585f588789f7e7857a84a6'
        }
        
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

                if tvg_id in special_tvg_ids and title_element is not None:
                    date_element = programme.find('date')
                    if date_element is not None and date_element.text:
                        raw_date = date_element.text.strip()
                        year = raw_date[:4] if len(raw_date) >= 4 else None
                    else:
                        year = None

                    categories = [
                        cat.text.strip()
                        for cat in programme.findall('category')
                        if cat.text
                    ]
                    category = categories[1] if len(categories) > 1 else (categories[0] if categories else None)

                    if category in category_map:
                        category = category_map[category]

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
