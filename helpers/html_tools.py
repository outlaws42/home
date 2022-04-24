from bs4 import BeautifulSoup  # Needs to be installed through pip
import requests

class HT():
  def html_info(self,tag,url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        find_status = soup.find(tag)
        final_status = find_status.text.strip()
    except requests.exceptions.RequestException as e:
        print(e)
        final_status = "Can't connect"
        print(final_status)
    return final_status

if __name__ == "__main__":
  app = HT()
