import requests
from bs4 import BeautifulSoup
import openpyxl as opx


class News_Request():
    """работа парсера для получения информации с новостного сайта The Guardian"""

    def __init__(self, idea, topic, s, sl_href, name_sl, file):
        self.idea = idea
        self.topic = topic
        self.s = s
        self.sl_href = sl_href
        self.name_sl = name_sl
        self.file = file

    def categories(self):
        """"Проверка, есть ли запрошенная категория новостейб после чего составляется ссылка"""

        CATEGORIES = {'мир': "world",
                      'новости англии': "uk-news",
                      'коронавирус': "world/coronavirus-outbreak",
                      'климатический кризис': "environment/climate-crisis",
                      'окружающая среда': "uk/environment",
                      'наука': "science",
                      'мировые разработки': "global-development",
                      'футбол': "football",
                      'технологии': "uk/technology",
                      'бизнес': "uk/business",
                      'кто умер': "obituaries",
                      'редакция': "profile/editorial",
                      'активисты': "index/contributors",
                      'мультфильмы': "cartoons/archive",
                      'видео': "type/video+tone/comment",
                      'литература': "tone/letters",
                      }

        try:
            self.topic = CATEGORIES[self.idea]
            parser.url()
        except KeyError:
            print("No categories = your request")
            exit()

    def url(self):
        """Получение информации со странички сайта"""

        url = f"https://www.theguardian.com/{self.topic}"
        print("Topic :", self.topic)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        self.s = soup.find_all("a", class_="u-faux-block-link__overlay js-headline-text")
        parser.list()

    def list(self):
        """Преобразование полученных кусков HTML в чистые ссылки и заголовки путем удаления лишнего"""

        text_s = str(self.s)
        text_s = text_s.split("<a")
        self.sl_href = []
        self.name_sl = []
        for item in text_s:
            item = item.replace('class="u-faux-block-link__overlay js-headline-text" data-link-name="article" href="',
                                "")
            item = item.replace('aria-hidden="true" ', "")
            item = item.replace('" tabindex="-1"', " ")
            item = item.replace('</a>,', "")
            item = item.replace('>', " ")
            item = item.replace('</a ]', "")
            sl = item.split(" ")
            sd = []
            c = 0
            for element in sl:
                ln = len(sl)
                if "//" in element:
                    self.sl_href.append(element)
                elif (element not in self.sl_href) and ('""' not in element):
                    c += 1
                    sd.append(element)
                    if c == (ln - 1):
                        self.name_sl.append(" ".join(sd))
        parser.output()

    def output(self):
        """Вывод полученной информации"""

        print("Links")
        for num in range(len(self.sl_href)):
            print(num,
                  "------- link:", self.sl_href[num],
                  "------- article:", self.name_sl[num].upper(),
                  sep="\n \t")
        print("Total number of articles :", len(self.sl_href))
        parser.info()

    def info(self):
        """Удаляем предидущий лист в Excel файле,
        затем создаем новый и записываем в его колонки ссылки на статьи и темы статей"""

        sheet = self.file.active
        self.file.remove(sheet)
        sheet = self.file.create_sheet("Link and Article")
        self.file.save("information.xlsx")
        sheet = self.file.active
        sheet["A1"] = "LINKS"
        sheet["B1"] = "ARTICLE"
        for element in range(len(self.sl_href)):
            sheet[f"A{element + 2}"] = self.sl_href[element]
            sheet[f"B{element + 2}"] = self.name_sl[element]
        self.file.save("information.xlsx")
        self.file.close()


idea = input("what kinds of news do you want? : ")
topic = False
s = False
sl_href = False
name_sl = False
file = opx.open("information.xlsx")

parser = News_Request(idea, topic, s, sl_href, name_sl, file)
parser.categories()
