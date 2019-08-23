# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import re
import json
import re
from sogou.items import SogouItem


class StoresSpider(scrapy.Spider):
    name = 'stores'
    allowed_domains = ['map.sogou.com']
    basic_url = "http://map.sogou.com/EngineV6/search/json?"

    def start_requests(self):
        city_names = ['合肥', '蚌埠', '淮南', '黄山', '安庆', '亳州', '池州', '滁州', '阜阳', '淮北', '六安', '马鞍山', '宿州', '铜陵', '芜湖', '宣城',
                      '福州', '厦门', '泉州', '龙岩', '南平', '宁德', '莆田', '三明', '漳州', '兰州', '白银', '定西', '嘉峪关', '金昌', '酒泉', '陇南',
                      '平凉', '庆阳', '天水', '武威', '张掖', '广州', '深圳', '东莞', '佛山', '惠州', '中山', '潮州', '河源', '江门', '揭阳', '茂名',
                      '梅州', '清远', '汕头', '汕尾', '韶关', '阳江', '云浮', '湛江', '肇庆', '珠海', '南宁', '百色', '北海', '崇左', '防城港', '贵港',
                      '桂林', '河池', '贺州', '来宾', '钦州', '梧州', '玉林', '贵阳', '安顺', '毕节', '六盘水', '铜仁', '遵义', '海口', '三亚', '五指山',
                      '琼海', '儋州', '文昌', '万宁', '东方', '定安', '屯昌', '澄迈', '临高', '石家庄', '保定', '沧州', '邯郸', '秦皇岛', '唐山', '邢台',
                      '承德', '衡水', '廊坊', '张家口', '郑州', '安阳', '鹤壁', '焦作', '开封', '洛阳', '漯河', '南阳', '平顶山', '濮阳', '三门峡', '商丘',
                      '新乡', '信阳', '许昌', '周口', '驻马店', '济源', '大庆', '大兴安岭', '鹤岗', '黑河', '鸡西', '佳木斯', '牡丹江', '七台河', '齐齐哈尔',
                      '双鸭山', '绥化', '伊春', '武汉', '鄂州', '黄冈', '黄石', '荆门', '荆州', '潜江', '神农架', '十堰', '随州', '天门', '仙桃', '咸宁',
                      '孝感', '宜昌', '长沙', '衡阳', '湘潭', '永州', '株洲', '常德', '郴州', '怀化', '娄底', '邵阳', '益阳', '岳阳', '张家界', '长春',
                      '吉林市', '白城', '白山', '辽源', '四平', '松原', '通化', '南京', '常州', '淮安', '连云港', '南通', '苏州', '泰州', '无锡', '徐州',
                      '扬州', '盐城', '镇江', '宿迁', '南昌', '九江', '抚州', '赣州', '吉安', '景德镇', '萍乡', '上饶', '新余', '宜春', '鹰潭', '沈阳',
                      '鞍山', '大连', '葫芦岛', '营口', '本溪', '朝阳', '丹东', '抚顺', '阜新', '锦州', '辽阳', '盘锦', '铁岭', '包头', '巴彦淖尔', '赤峰',
                      '鄂尔多斯', '呼伦贝尔', '通辽', '乌海', '乌兰察布', '银川', '固原', '石嘴山', '吴忠', '中卫', '西宁', '海东', '海南州', '济南', '青岛',
                      '临沂', '日照', '威海', '潍坊', '烟台', '滨州', '德州', '东营', '菏泽', '济宁', '聊城', '泰安', '枣庄', '淄博', '长治', '大同',
                      '晋城', '晋中', '临汾', '吕梁', '朔州', '忻州', '阳泉', '运城', '西安', '安康', '宝鸡', '汉中', '商洛', '铜川', '渭南', '咸阳',
                      '延安', '榆林', '成都', '巴中', '达州', '德阳', '广安', '广元', '乐山', '泸州', '眉山', '绵阳', '内江', '南充', '攀枝花', '遂宁',
                      '雅安', '宜宾', '资阳', '自贡', '拉萨', '阿里', '克拉玛依', '喀什', '石河子', '和田', '阿克苏', '阿勒泰', '塔城', '阿拉尔', '图木舒克',
                      '五家渠', '北屯', '铁门关', '可克达拉', '双河', '昆明', '保山', '丽江', '临沧', '普洱', '曲靖', '玉溪', '昭通', '杭州', '宁波',
                      '绍兴', '台州', '温州', '舟山', '湖州', '嘉兴', '金华', '丽水', '衢州', '台北', '香港', '澳门']
        categories = ['景点', '酒吧', '洗浴', 'KTV', '租房', '二手房', '银行', '超市', '医院', '药店', '4S店', '电影院']
        for city in city_names:
            for category in categories:
                params = {
                    'what': 'keyword:' + category,
                    'othercityflag': 1,
                    'thiscity': city,
                    'lastcity': city,
                    'userdata': 3,
                    'encrypt': 1,
                    'pageinfo': '1,10',
                    'locationsort': 0,
                    'version': 7,
                    'ad': 0,
                    'resultTypes': 'poi,busline',
                    'reqid': '1565943783834884',
                    'cb': 'parent.IFMS.search',
                    'range': 'bound:5792000, 496000, 18096000, 7808000: 0',
                    'appid': 1361,
                    'level': 11,
                    'exact': 1,
                    'submittime': 0
                }
                yield scrapy.Request(url=self.basic_url + urlencode(params), callback=self.parse_tags, method="POST",
                                     meta={'city': city, 'keyword': category})
                yield scrapy.Request(url=self.basic_url + urlencode(params), callback=self.parse_tag, method="POST",
                                      meta={'city':city, 'keyword':category, 'page':1})

    def parse_tags(self, response):  # get more specific categories
        city = response.meta.get('city')
        category = response.meta.get('keyword')
        json_str = ''.join(re.findall('.*?search\((.*?),document.*?', response.text))
        json_text = json.loads(json_str)
        moretypes = json_text.get('response', {}).get('category', {}).get('typelist', '')
        if moretypes:
            types_names = [type['name'] for type in moretypes][1:]
        else:  # no more categories
            types_names = [category]

        for name in types_names:
            params = {
                'what': 'keyword:' + name,
                'othercityflag': 1,
                'thiscity': city,
                'lastcity': city,
                'userdata': 3,
                'encrypt': 1,
                'pageinfo': '1,10',
                'locationsort': 0,
                'version': 7,
                'ad': 0,
                'resultTypes': 'poi',
                'reqid': '1566303258900985',
                'cb': 'parent.IFMS.search',
                'range': 'bound:12993625,3695500,13105875,3739500:0',
                'appid': 1361,
                'level': 11,
                'exact': 1,
                'submittime': 0,
                'cateid': 'hefei-%25E5%25B7%259D%25E8%258F%259C'
            }
            yield scrapy.Request(url=self.basic_url + urlencode(params), callback=self.parse_tag, method="POST",
                                 meta={'city': city, 'keyword': name, 'category': category, 'page': 1})

    def parse_tag(self, response):
        keyword = response.meta.get('keyword')
        page = response.meta.get('page')
        city = response.meta.get('city')
        category = response.meta.get('category')

        json_str = ''.join(re.findall('.*?search\((.*?),document.*?', response.text))
        json_text = json.loads(json_str)
        stores = json_text.get('response', {}).get('category', '')

        # iterate all pages
        if stores and page == 1:
            resultcount = (stores.get('content', {}).get('resultcount', 0) + 9) // 10
            for page in range(2, resultcount + 1):
                params = {
                    'what': 'keyword:' + keyword,
                    'othercityflag': 1,
                    'thiscity': city,
                    'lastcity': city,
                    'userdata': 3,
                    'encrypt': 1,
                    'pageinfo': str(page) + ',10',
                    'locationsort': 0,
                    'version': 7,
                    'ad': 0,
                    'resultTypes': 'poi',
                    'reqid': '1566303258900985',
                    'cb': 'parent.IFMS.search',
                    'range': 'bound:12993625,3695500,13105875,3739500:0',
                    'appid': 1361,
                    'level': 11,
                    'exact': 1,
                    'submittime': 0,
                    'cateid': 'hefei-%25E5%25B7%259D%25E8%258F%259C'
                }
                yield scrapy.Request(url=self.basic_url + urlencode(params), callback=self.parse_tag, method="POST",
                                     meta={'city': city, 'keyword': keyword, 'page': page})

        # get each page's stores' basic info
        if stores:
            stores = stores.get('content', {}).get('feature', '')
            for store in stores:
                item = SogouItem()
                if category:
                    item['category'] = category
                    item['tag'] = [keyword]
                else:
                    item['category'] = keyword
                    item['tag'] = []
                item['name'] = store.get('caption', '')
                item['address'] = store.get('detail', {}).get('address', '')
                item['province'] = store.get('detail', {}).get('province', '')
                item['phone'] = store.get('detail', {}).get('phone', '').split(';')
                item['city'] = store.get('detail', {}).get('city', '')
                item['price'] = store.get('fields', {}).get('Map_JDprice', {}).get('value', '')
                item['score'] = store.get('fields', {}).get('Map_JDscore', {}).get('value', '')
                item['commentcount'] = store.get('fields', {}).get('Map_JDRecordCount', {}).get('value', '')
                item['link'] = 'http://map.sogou.com/poi/1_' + store.get('dataid', '') + '.htm'
                yield scrapy.Request(url=item['link'], callback=self.parse_site,
                                     meta={'item': item})

    def parse_site(self, response):
        item = response.meta.get('item')
        json_str = re.sub('\r|\n|\t', '', response.text)
        json_str = ''.join(re.findall('.*?var GbParam = \{result:(.*?)\,nCommentCount.*?', json_str, re.S))
        json_text = json.loads(json_str)
        item['province'] = json_text.get('province', '')
        item['lat'] = json_text.get('y', '')
        item['lng'] = json_text.get('x', '')
        yield item


'''


get a list of categories' name: types_name

    def start_requests(self):
        url = "http://map.sogou.com/EngineV6/search/json?"
        params = {
            'what': 'keyword:%u9910%u996E',
            'othercityflag': 1,
            'thiscity': '%u5408%u80A5',
            'lastcity': '%u5408%u80A5',
            'userdata': 3,
            'encrypt': 1,
            'pageinfo': '1,10',
            'locationsort': 0,
            'version': 7,
            'ad': 0,
            'resultTypes': 'poi,busline',
            'reqid': '1565943783834884',
            'cb': 'parent.IFMS.search',
            'range': 'bound:5792000, 496000, 18096000, 7808000: 0',
            'appid': 1361,
            'level': 11,
            'exact': 1,
            'submittime': 0
        }
        headers = {
            'Content-Type':'application/json'
        }
        yield scrapy.Request(url=url + urlencode(params), callback=self.parse, method="POST", dont_filter=True)

    def parse(self, response):
        json_str = ''.join(re.findall('.*?search\((.*?),document.*?', response.text))
        json_text = json.loads(json_str)
        moretypes = json_text['response']['category']['typelist']
        types_names = [type['name'] for type in moretypes]






get a list of cities' name: city_names

    def start_requests(self):
        url = "http://map.sogou.com/EngineV6/search/json?"
        params = {
            'what': 'keyword:%u9910%u996E',
            'othercityflag': 1,
            'thiscity': '%u5168%u56FD',
            'lastcity': '%u5168%u56FD',
            'userdata': 3,
            'encrypt': 1,
            'pageinfo': '1,10',
            'locationsort': 0,
            'version': 7,
            'ad': 0,
            'resultTypes': 'poi,busline',
            'reqid': '1565943783834884',
            'cb': 'parent.IFMS.search',
            'range': 'bound:5792000, 496000, 18096000, 7808000: 0',
            'appid': 1361,
            'level': 4,
            'exact': 1,
            'submittime': 0
        }
        yield scrapy.Request(url=url + urlencode(params), callback=self.parse, method="POST", dont_filter=True)

    def parse(self, response):
        json_str = ''.join(re.findall('.*?search\((.*?),document.*?', response.text))
        json_text = json.loads(json_str)
        morecity = json_text['response']['category']['morecity']
        city_names = []
        for province in morecity:
            cities = province['cities']
            names = [city['name'] for city in cities]
            city_names.extend(names)
'''
