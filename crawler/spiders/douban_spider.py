import re
import scrapy
from crawler.items import MovieItem, PersonItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'CONCURRENT_REQUESTS': 1,
    }

    def parse(self, response):
        """解析 Top250 列表页，进入每部电影详情页"""
        for item in response.css('div.item'):
            movie_url = item.css('div.pic a::attr(href)').get()
            if movie_url:
                yield response.follow(movie_url, callback=self.parse_movie)

        next_page = response.css('span.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_movie(self, response):
        """解析电影详情页，提取 MovieItem，并发现人物"""
        movie = MovieItem()
        douban_id_match = re.search(r'subject/(\d+)/', response.url)
        movie['douban_id'] = douban_id_match.group(1) if douban_id_match else None
        movie['title'] = response.css('span[property="v:itemreviewed"]::text').get()

        year_text = response.css('span.year::text').get()
        movie['year'] = re.search(r'\d{4}', year_text).group(0) if year_text else None

        rating = response.css('strong.ll.rating_num::text').get()
        movie['rating'] = float(rating) if rating else None

        duration_text = response.css('span[property="v:runtime"]::text').get()
        duration_match = re.search(r'\d+', duration_text) if duration_text else None
        movie['duration'] = int(duration_match.group(0)) if duration_match else None

        movie['summary'] = response.css('span[property="v:summary"]::text').get()
        movie['poster_url'] = response.css('img[rel="v:image"]::attr(src)').get()

        movie['genres'] = response.css('span[property="v:genre"]::text').getall()
        movie['countries'] = self._extract_info_list(response, '制片国家/地区:')
        movie['languages'] = self._extract_info_list(response, '语言:')

        movie['directors'] = self._extract_persons(response, '导演', 'director')
        movie['writers'] = self._extract_persons(response, '编剧', 'writer')
        movie['actors'] = self._extract_actors(response)

        movie['related_movie_ids'] = response.css('div.recommendations-bd a::attr(href)').reall(
            r'subject/(\d+)/'
        )

        yield movie

    def parse_person(self, response):
        """解析人物详情页"""
        person = PersonItem()
        person_douban_id_match = re.search(r'celebrity/(\d+)/', response.url)
        person['douban_id'] = person_douban_id_match.group(1) if person_douban_id_match else None
        person['name'] = response.css('h1::text').get()

        alias_text = ''
        info_items = response.css('div.info ul li')
        for li in info_items:
            text = li.css('::text').getall()
            text = ''.join(t.strip() for t in text)
            if '更多外文名' in text:
                alias_text = text.replace('更多外文名:', '').strip()
            elif '性别' in text:
                person['gender'] = text.replace('性别:', '').strip()
            elif '出生日期' in text:
                birth_match = re.search(r'\d{4}', text)
                person['birth_year'] = birth_match.group(0) if birth_match else None
            elif '出生地' in text:
                person['birthplace'] = text.replace('出生地:', '').strip()

        person['alias'] = alias_text if alias_text else None

        yield person

    def _extract_persons(self, response, label, default_role):
        """从页面信息栏提取导演/编剧列表"""
        persons = []
        info_items = response.css('div#info span')
        in_section = False
        for span in info_items:
            span_text = span.css('::text').get() or ''
            if label in span_text:
                in_section = True
                continue
            if in_section:
                links = span.css('a')
                for a in links:
                    href = a.css('::attr(href)').get() or ''
                    pid = re.search(r'celebrity/(\d+)/', href)
                    persons.append({
                        'douban_id': pid.group(1) if pid else None,
                        'name': a.css('::text').get(),
                        'role': default_role,
                    })
                if links:
                    break
        return persons

    def _extract_actors(self, response):
        """从演员区块提取主演列表（最多取前10位）"""
        actors = []
        actor_spans = response.css('span.actor span a')
        for a in actor_spans[:10]:
            href = a.css('::attr(href)').get() or ''
            pid = re.search(r'celebrity/(\d+)/', href)
            actors.append({
                'douban_id': pid.group(1) if pid else None,
                'name': a.css('::text').get(),
                'role_name': None,
            })
        return actors

    def _extract_info_list(self, response, label):
        """从信息栏提取逗号分隔的列表字段（如国家、语言）"""
        info_text = response.css('div#info::text').getall()
        info_text = ''.join(info_text)
        pattern = re.escape(label) + r'\s*(.+?)(?:\n|<br>)'
        match = re.search(pattern, info_text)
        if match:
            return [s.strip() for s in match.group(1).split('/')]
        return []
