import streamlit as st
import requests
from bs4 import BeautifulSoup
import pyperclip
import base64


def pirateBay(query, page='1'):
    allTorrents = []
    url = f'https://thehiddenbay.com/search/{query}/{page}/99/0'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("table#searchResult tr")

    for element in rows:
        data_elements = element.select('font.detDesc')

        if len(data_elements) == 0:
            continue

        data = data_elements[0].get_text().replace('Size', '').replace('Uploaded', '').replace('ULed', 'Uploaded').split(', ')
        date = data[0] if len(data) >= 1 else ''
        size = data[1] if len(data) >= 2 else ''
        uploader = element.select('font.detDesc a')[0].get_text()

        torrent = {
            'Name': element.select('a.detLink')[0].get_text(),
            'Size': size,
            'DateUploaded': date,
            'Category': element.select('td.vertTh center a')[0].get_text(),
            'Seeders': element.select('td')[2].get_text(),
            'Leechers': element.select('td')[3].get_text(),
            'UploadedBy': uploader,
            'Url': element.select('a.detLink')[0].get('href'),
            'Magnet': element.select('a[href^="magnet:"]')[0].get('href')
        }

        if torrent['Name']:
            allTorrents.append(torrent)

    return allTorrents


def search_torrent(query):
    result = pirateBay(query)

    if result:
        return result
    else:
        return None


def copy_to_clipboard(text):
    pyperclip.copy(text)


def main():
    st.title("Torrent Search App")
    query = st.text_input("Enter the torrent you want to search:")
    search_button = st.button("Search")

    if search_button:
        if query:
            st.info(f"Searching for {query}...")
            results = search_torrent(query)

            if results:
                st.success(f"Found {len(results)} torrents.")
                st.markdown("---")
                for torrent in results:
                    st.write("Name:", torrent['Name'])
                    st.write("Magnet Link:", torrent['Magnet'])
                    copy_button = st.empty()
                    copy_button.markdown(
                        f'<button class="btn btn-primary" onclick="copyToClipboard(\'{torrent["Magnet"]}\')">Copy Magnet Link</button>',
                        unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.warning("No torrents found.")
        else:
            st.warning("Please enter a search query.")


if __name__ == "__main__":
    main()
        
