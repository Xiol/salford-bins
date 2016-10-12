UPRN="111111111111"
PUSHOVER_TOKEN="asdfasdfasdfasdfasdfasdfasdfasdfasdf"
WHO=["asdfasdfasdfasdfasdfasdf","lkjlkjhkljhlkjhlkjhlkjhlkjhlkt"]

from bs4 import BeautifulSoup
import requests
import time
import datetime

class SalfordBins:
    def __init__(self, uprn):
        self.uprn = uprn
        self.binurl = "http://www.salford.gov.uk/bins-and-recycling/bin-collection-days/your-bin-collections/?UPRN={}".format(uprn)
        self.html = ""
        self.soup = None
        self.dateformat = "%A %d %B %Y"
        self._load_html()

    def _load_html(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Cache-Control": "no-cache",
            "DNT": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
        }
        self.html = requests.get(self.binurl, headers=headers).text
        self.soup = BeautifulSoup(self.html, 'html.parser').find(id="standard-page").find(class_="clearfix")

    def _parse_dates(self, dates):
        return [time.strftime("%Y-%m-%d", time.strptime(date, self.dateformat)) for date in dates]

    def _get_black_bin_dates(self):
        dates = [x.text for x in self.soup.find(class_="black").find('ul').find_all('li')]
        return self._parse_dates(dates)

    def _get_pink_bin_dates(self):
        dates = [x.text for x in self.soup.find(class_="pink").find('ul').find_all('li')]
        return self._parse_dates(dates)

    def _get_brown_bin_dates(self):
        dates = [x.text for x in self._select_bluebrown('brown').find('ul').find_all('li')]
        return self._parse_dates(dates)

    def _get_blue_bin_dates(self):
        dates = [x.text for x in self._select_bluebrown('blue').find('ul').find_all('li')]
        return self._parse_dates(dates)

    def _select_bluebrown(self, what):
        # They use the same class for blue and brown, bastards
        bluebrown = self.soup.find_all(class_="bluebrown")
        for entry in bluebrown:
            if what == 'brown' and 'Brown bins' in entry.text:
                return entry
            if what == 'blue' and 'Blue bins' in entry.text:
                return entry
        raise ValueError("Could not find {} entry in page".format(what))

    def whats_out_today(self):
        td = datetime.datetime.now()+datetime.timedelta(days=1)
        tomorrow = time.strftime("%Y-%m-%d", td.timetuple())

        out = []

        if tomorrow in self._get_black_bin_dates():
            out.append("Black")

        if tomorrow in self._get_pink_bin_dates():
            out.append("Pink")

        if tomorrow in self._get_blue_bin_dates():
            out.append("Blue")

        if tomorrow in self._get_brown_bin_dates():
            out.append("Brown")

        return out

    def do_pushover(self, apptoken, who):
        out = self.whats_out_today()

        if not out:
            return

        for w in who:
            data = {
                "token": apptoken,
                "user": w,
                "message": "Bins out today: {}".format(', '.join(out))
            }
            resp = requests.post("https://api.pushover.net/1/messages.json", data=data)

if __name__ == '__main__':
    sb = SalfordBins(UPRN)
    sb.do_pushover(PUSHOVER_TOKEN, WHO)
