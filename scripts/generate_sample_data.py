"""
生成电影知识图谱样本数据
结合豆瓣 Top250 列表页数据 + 手工整理的经典电影详情，构建完整的知识图谱数据集。
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 经典电影详情数据 (中文电影为主，使用豆瓣公开信息)
MOVIE_DETAILS = {
    "1292052": {  # The Shawshank Redemption
        "title": "肖申克的救赎", "year": 1994, "rating": 9.7,
        "duration": 142, "summary": "银行家安迪因被误判杀害妻子及其情人而被关进肖申克监狱，凭借才智和毅力用二十年时间完成越狱。",
        "genres": ["剧情", "犯罪"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1047973", "name": "弗兰克·德拉邦特", "role": "director"}],
        "writers": [{"douban_id": "1047973", "name": "弗兰克·德拉邦特", "role": "writer"},
                     {"douban_id": "1027225", "name": "斯蒂芬·金", "role": "writer"}],
        "actors": [{"douban_id": "1054521", "name": "蒂姆·罗宾斯", "role_name": "安迪·杜佛兰"},
                    {"douban_id": "1054534", "name": "摩根·弗里曼", "role_name": "瑞德"},
                    {"douban_id": "1041174", "name": "鲍勃·冈顿", "role_name": "典狱长"}],
    },
    "1291546": {  # 霸王别姬
        "title": "霸王别姬", "year": 1993, "rating": 9.6,
        "duration": 171, "summary": "段小楼与程蝶衣从小在京剧班学艺，两人合演《霸王别姬》名震京城，历经中国半个世纪的社会变迁。",
        "genres": ["剧情", "爱情", "同性"], "countries": ["中国大陆", "中国香港"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1023045", "name": "陈凯歌", "role": "director"}],
        "writers": [{"douban_id": "1023045", "name": "陈凯歌", "role": "writer"},
                     {"douban_id": "1041515", "name": "李碧华", "role": "writer"}],
        "actors": [{"douban_id": "1003494", "name": "张国荣", "role_name": "程蝶衣"},
                    {"douban_id": "1023514", "name": "张丰毅", "role_name": "段小楼"},
                    {"douban_id": "1016899", "name": "巩俐", "role_name": "菊仙"}],
    },
    "1292722": {  # 阿甘正传
        "title": "阿甘正传", "year": 1994, "rating": 9.5,
        "duration": 142, "summary": "智商只有75的阿甘，凭借跑步天赋和纯真的心，经历了美国几十年的历史变迁。",
        "genres": ["剧情", "爱情"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1053561", "name": "罗伯特·泽米吉斯", "role": "director"}],
        "actors": [{"douban_id": "1054450", "name": "汤姆·汉克斯", "role_name": "阿甘"},
                    {"douban_id": "1048027", "name": "罗宾·怀特", "role_name": "珍妮"}],
    },
    "1295644": {  # 这个杀手不太冷
        "title": "这个杀手不太冷", "year": 1994, "rating": 9.4,
        "duration": 110, "summary": "职业杀手莱昂无意中搭救了一个全家被杀害的小女孩玛蒂尔达，两人在相处中产生了超越年龄的情感。",
        "genres": ["剧情", "动作", "犯罪"], "countries": ["法国"], "languages": ["英语", "法语"],
        "directors": [{"douban_id": "1031876", "name": "吕克·贝松", "role": "director"}],
        "actors": [{"douban_id": "1010509", "name": "让·雷诺", "role_name": "莱昂"},
                    {"douban_id": "1054454", "name": "娜塔莉·波特曼", "role_name": "玛蒂尔达"},
                    {"douban_id": "1013847", "name": "加里·奥德曼", "role_name": "斯坦斯菲尔德"}],
    },
    "1292063": {  # 美丽人生
        "title": "美丽人生", "year": 1997, "rating": 9.6,
        "duration": 116, "summary": "犹太人圭多和儿子被关进集中营，他哄骗儿子这是一场游戏，用生命保护了儿子的童心。",
        "genres": ["剧情", "喜剧", "爱情", "战争"], "countries": ["意大利"], "languages": ["意大利语"],
        "directors": [{"douban_id": "1045105", "name": "罗伯托·贝尼尼", "role": "director"}],
        "actors": [{"douban_id": "1045105", "name": "罗伯托·贝尼尼", "role_name": "圭多"}],
    },
    "1291561": {  # 千与千寻
        "title": "千与千寻", "year": 2001, "rating": 9.4,
        "duration": 125, "summary": "少女千寻随父母误入神灵世界，为救回变成猪的父母，她在汤屋工作并逐渐成长。",
        "genres": ["剧情", "动画", "奇幻"], "countries": ["日本"], "languages": ["日语"],
        "directors": [{"douban_id": "1054418", "name": "宫崎骏", "role": "director"}],
        "actors": [{"douban_id": "1025452", "name": "柊瑠美", "role_name": "千寻(配音)"}],
    },
    "1292720": {  # 泰坦尼克号
        "title": "泰坦尼克号", "year": 1997, "rating": 9.4,
        "duration": 194, "summary": "穷画家杰克和贵族少女罗丝在泰坦尼克号上相恋，船撞冰山后杰克为救罗丝而牺牲。",
        "genres": ["剧情", "爱情", "灾难"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1022571", "name": "詹姆斯·卡梅隆", "role": "director"}],
        "actors": [{"douban_id": "1041029", "name": "莱昂纳多·迪卡普里奥", "role_name": "杰克"},
                    {"douban_id": "1054446", "name": "凯特·温丝莱特", "role_name": "罗丝"}],
    },
    "1291549": {  # 放牛班的春天
        "title": "放牛班的春天", "year": 2004, "rating": 9.3,
        "duration": 97, "summary": "音乐教师马修来到一所问题儿童寄宿学校，用音乐打开了孩子们封闭的心扉。",
        "genres": ["剧情", "音乐"], "countries": ["法国"], "languages": ["法语"],
        "directors": [{"douban_id": "1056315", "name": "克里斯托夫·巴拉蒂", "role": "director"}],
        "actors": [{"douban_id": "1045064", "name": "杰拉尔·朱尼奥", "role_name": "马修"}],
    },
    "1291841": {  # 教父
        "title": "教父", "year": 1972, "rating": 9.3,
        "duration": 175, "summary": "维托·柯里昂是美国最有权势的黑手党家族首领，小儿子迈克尔从不愿涉足家族事业到最终继承父业。",
        "genres": ["剧情", "犯罪"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1054419", "name": "弗朗西斯·福特·科波拉", "role": "director"}],
        "actors": [{"douban_id": "1054451", "name": "马龙·白兰度", "role_name": "维托·柯里昂"},
                    {"douban_id": "1054452", "name": "阿尔·帕西诺", "role_name": "迈克尔·柯里昂"}],
    },
    "1292001": {  # 海上钢琴师
        "title": "海上钢琴师", "year": 1998, "rating": 9.3,
        "duration": 165, "summary": "1900年在一艘豪华邮轮上被遗弃的婴儿，成长为天才钢琴师，却一生未曾踏上陆地。",
        "genres": ["剧情", "音乐"], "countries": ["意大利"], "languages": ["英语"],
        "directors": [{"douban_id": "1018983", "name": "朱塞佩·托纳多雷", "role": "director"}],
        "actors": [{"douban_id": "1041136", "name": "蒂姆·罗斯", "role_name": "1900"}],
    },
    "1292213": {  # 大话西游之大圣娶亲
        "title": "大话西游之大圣娶亲", "year": 1995, "rating": 9.2,
        "duration": 99, "summary": "至尊宝穿越时空回到五百年前，遇到了紫霞仙子，在情与义之间做出选择。",
        "genres": ["喜剧", "爱情", "奇幻", "古装"], "countries": ["中国香港"], "languages": ["粤语"],
        "directors": [{"douban_id": "1027846", "name": "刘镇伟", "role": "director"}],
        "actors": [{"douban_id": "1048026", "name": "周星驰", "role_name": "至尊宝/孙悟空"},
                    {"douban_id": "1019053", "name": "朱茵", "role_name": "紫霞仙子"},
                    {"douban_id": "1016771", "name": "吴孟达", "role_name": "二当家"}],
    },
    "1291543": {  # 功夫
        "title": "功夫", "year": 2004, "rating": 8.8,
        "duration": 100, "summary": "小混混阿星误闯猪笼城寨，卷入了斧头帮与隐世高手的争斗，最终领悟真正的功夫。",
        "genres": ["动作", "喜剧", "奇幻"], "countries": ["中国大陆", "中国香港"], "languages": ["粤语", "汉语普通话"],
        "directors": [{"douban_id": "1048026", "name": "周星驰", "role": "director"}],
        "writers": [{"douban_id": "1048026", "name": "周星驰", "role": "writer"}],
        "actors": [{"douban_id": "1048026", "name": "周星驰", "role_name": "阿星"},
                    {"douban_id": "1016751", "name": "元秋", "role_name": "包租婆"},
                    {"douban_id": "1028689", "name": "元华", "role_name": "包租公"},
                    {"douban_id": "1014745", "name": "黄圣依", "role_name": "芳儿"}],
    },
    "1291544": {  # 让子弹飞
        "title": "让子弹飞", "year": 2010, "rating": 9.0,
        "duration": 132, "summary": "北洋年间，土匪张牧之劫了县长马邦德的火车，冒充县长去鹅城上任，与恶霸黄四郎展开较量。",
        "genres": ["剧情", "喜剧", "动作"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1027903", "name": "姜文", "role": "director"}],
        "writers": [{"douban_id": "1027903", "name": "姜文", "role": "writer"}],
        "actors": [{"douban_id": "1027903", "name": "姜文", "role_name": "张牧之"},
                    {"douban_id": "1006959", "name": "葛优", "role_name": "马邦德"},
                    {"douban_id": "1044899", "name": "周润发", "role_name": "黄四郎"}],
    },
    "1291552": {  # 无间道
        "title": "无间道", "year": 2002, "rating": 9.3,
        "duration": 101, "summary": "警方卧底陈永仁和黑帮卧底刘建明各自潜伏在对方组织中，一场关于身份的较量就此展开。",
        "genres": ["剧情", "犯罪", "悬疑"], "countries": ["中国香港"], "languages": ["粤语"],
        "directors": [{"douban_id": "1028682", "name": "刘伟强", "role": "director"},
                       {"douban_id": "1274988", "name": "麦兆辉", "role": "director"}],
        "actors": [{"douban_id": "1054424", "name": "刘德华", "role_name": "刘建明"},
                    {"douban_id": "1006583", "name": "梁朝伟", "role_name": "陈永仁"},
                    {"douban_id": "1041381", "name": "黄秋生", "role_name": "黄志诚"},
                    {"douban_id": "1004439", "name": "曾志伟", "role_name": "韩琛"}],
    },
    "1291560": {  # 龙猫
        "title": "龙猫", "year": 1988, "rating": 9.2,
        "duration": 86, "summary": "两姐妹随父亲搬到乡下，在森林中遇到了可爱的龙猫，展开了一系列奇妙冒险。",
        "genres": ["动画", "奇幻", "冒险"], "countries": ["日本"], "languages": ["日语"],
        "directors": [{"douban_id": "1054418", "name": "宫崎骏", "role": "director"}],
    },
    "1292220": {  # 楚门的世界
        "title": "楚门的世界", "year": 1998, "rating": 9.3,
        "duration": 103, "summary": "楚门从小生活在一个巨大的摄影棚中，他的整个人生都是一档直播节目，直到他开始怀疑这个世界。",
        "genres": ["剧情", "科幻"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1027823", "name": "彼得·威尔", "role": "director"}],
        "actors": [{"douban_id": "1054435", "name": "金·凯瑞", "role_name": "楚门"}],
    },
    "1292365": {  # 活着
        "title": "活着", "year": 1994, "rating": 9.3,
        "duration": 132, "summary": "福贵一家在几十年的历史变迁中经历了种种苦难，但始终坚韧地活着。",
        "genres": ["剧情", "历史", "家庭"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1023027", "name": "张艺谋", "role": "director"}],
        "actors": [{"douban_id": "1006959", "name": "葛优", "role_name": "福贵"},
                    {"douban_id": "1016899", "name": "巩俐", "role_name": "家珍"}],
    },
    "1291843": {  # 黑客帝国
        "title": "黑客帝国", "year": 1999, "rating": 9.1,
        "duration": 136, "summary": "程序员尼奥发现看似正常的世界实际上是机器创造的虚拟现实，他加入反抗军对抗机器统治。",
        "genres": ["动作", "科幻"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1027779", "name": "沃卓斯基姐妹", "role": "director"}],
        "actors": [{"douban_id": "1040997", "name": "基努·里维斯", "role_name": "尼奥"}],
    },
    "1292274": {  # 蝙蝠侠：黑暗骑士
        "title": "蝙蝠侠：黑暗骑士", "year": 2008, "rating": 9.2,
        "duration": 152, "summary": "蝙蝠侠面对混乱使者小丑的挑战，在正义与秩序之间做出艰难抉择。",
        "genres": ["剧情", "动作", "科幻", "犯罪"], "countries": ["美国", "英国"], "languages": ["英语"],
        "directors": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "director"}],
        "actors": [{"douban_id": "1006956", "name": "克里斯蒂安·贝尔", "role_name": "蝙蝠侠"},
                    {"douban_id": "1006948", "name": "希斯·莱杰", "role_name": "小丑"}],
    },
    "1291858": {  # 鬼子来了
        "title": "鬼子来了", "year": 2000, "rating": 9.3,
        "duration": 139, "summary": "抗战末期，挂甲台村民马大三被迫看管一个日本俘虏和一个翻译，引发了一系列悲剧。",
        "genres": ["剧情", "历史", "战争"], "countries": ["中国大陆"], "languages": ["汉语普通话", "日语"],
        "directors": [{"douban_id": "1027903", "name": "姜文", "role": "director"}],
        "actors": [{"douban_id": "1027903", "name": "姜文", "role_name": "马大三"}],
    },
    "1291572": {  # 指环王：王者无敌
        "title": "指环王：王者无敌", "year": 2003, "rating": 9.3,
        "duration": 201, "summary": "弗罗多和山姆深入魔多销毁至尊魔戒，阿拉贡率领人类大军进行最后的决战。",
        "genres": ["剧情", "动作", "奇幻", "冒险"], "countries": ["新西兰", "美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1041124", "name": "彼得·杰克逊", "role": "director"}],
        "actors": [{"douban_id": "1041126", "name": "伊利亚·伍德", "role_name": "弗罗多"}],
    },
}


def generate_full_dataset():
    """结合 Top250 列表数据和详情数据生成完整数据集"""
    top250_path = os.path.join(DATA_DIR, 'movies_top250.json')
    if not os.path.exists(top250_path):
        print(f"Warning: {top250_path} not found. Run the Top250 list scraper first.")
        return

    with open(top250_path, 'r', encoding='utf-8') as f:
        top250 = json.load(f)

    all_persons = {}
    movies_out = []
    persons_out = []

    for movie in top250:
        douban_id = movie.get('douban_id')
        if douban_id in MOVIE_DETAILS:
            detail = MOVIE_DETAILS[douban_id]
            movie_full = {
                'douban_id': douban_id,
                'title': detail['title'],
                'year': detail['year'],
                'rating': detail['rating'],
                'duration': detail['duration'],
                'summary': detail['summary'],
                'poster_url': movie.get('pic_url'),
                'genres': detail.get('genres', []),
                'countries': detail.get('countries', []),
                'languages': detail.get('languages', []),
                'directors': detail.get('directors', []),
                'writers': detail.get('writers', []),
                'actors': detail.get('actors', []),
                'related_movie_ids': [],
            }
            movies_out.append(movie_full)

            # 收集所有人物
            for person_list in [detail.get('directors', []), detail.get('writers', []), detail.get('actors', [])]:
                for p in person_list:
                    pid = p.get('douban_id')
                    if pid and pid not in all_persons:
                        all_persons[pid] = {'douban_id': pid, 'name': p['name']}
        else:
            # 不在详情数据库中的电影，只有基本信息
            movie_full = {
                'douban_id': douban_id,
                'title': movie['title'],
                'year': None,
                'rating': movie['rating'],
                'duration': None,
                'summary': '',
                'poster_url': movie.get('pic_url'),
                'genres': [],
                'countries': [],
                'languages': [],
                'directors': [],
                'writers': [],
                'actors': [],
                'related_movie_ids': [],
            }
            movies_out.append(movie_full)

    # 为人物补充性别和出生年份信息
    PERSON_EXTRA = {
        "1048026": {"gender": "男", "birth_year": 1962, "birthplace": "中国香港", "alias": "Stephen Chow"},
        "1027903": {"gender": "男", "birth_year": 1963, "birthplace": "河北唐山", "alias": "Jiang Wen"},
        "1016771": {"gender": "男", "birth_year": 1953, "birthplace": "中国香港", "alias": "Ng Man-tat"},
        "1016751": {"gender": "女", "birth_year": 1950, "birthplace": "中国香港", "alias": "Yuen Qiu"},
        "1028689": {"gender": "男", "birth_year": 1952, "birthplace": "中国香港", "alias": "Yuen Wah"},
        "1006959": {"gender": "男", "birth_year": 1957, "birthplace": "北京", "alias": "Ge You"},
        "1016899": {"gender": "女", "birth_year": 1965, "birthplace": "辽宁沈阳", "alias": "Gong Li"},
        "1019053": {"gender": "女", "birth_year": 1971, "birthplace": "中国香港", "alias": "Athena Chu"},
        "1054424": {"gender": "男", "birth_year": 1961, "birthplace": "中国香港", "alias": "Andy Lau"},
        "1006583": {"gender": "男", "birth_year": 1962, "birthplace": "中国香港", "alias": "Tony Leung"},
        "1003494": {"gender": "男", "birth_year": 1956, "birthplace": "中国香港", "alias": "Leslie Cheung"},
        "1023514": {"gender": "男", "birth_year": 1956, "birthplace": "湖南长沙", "alias": "Zhang Fengyi"},
        "1054418": {"gender": "男", "birth_year": 1941, "birthplace": "日本东京", "alias": "Hayao Miyazaki"},
        "1023027": {"gender": "男", "birth_year": 1951, "birthplace": "陕西西安", "alias": "Zhang Yimou"},
        "1044899": {"gender": "男", "birth_year": 1955, "birthplace": "中国香港", "alias": "Chow Yun-fat"},
        "1054521": {"gender": "男", "birth_year": 1958, "birthplace": "美国", "alias": "Tim Robbins"},
        "1054534": {"gender": "男", "birth_year": 1937, "birthplace": "美国", "alias": "Morgan Freeman"},
        "1054450": {"gender": "男", "birth_year": 1956, "birthplace": "美国", "alias": "Tom Hanks"},
        "1010509": {"gender": "男", "birth_year": 1948, "birthplace": "摩洛哥卡萨布兰卡", "alias": "Jean Reno"},
        "1054434": {"gender": "男", "birth_year": 1970, "birthplace": "英国伦敦", "alias": "Christopher Nolan"},
        "1023045": {"gender": "男", "birth_year": 1952, "birthplace": "北京", "alias": "Chen Kaige"},
        "1022571": {"gender": "男", "birth_year": 1954, "birthplace": "加拿大", "alias": "James Cameron"},
        "1054419": {"gender": "男", "birth_year": 1939, "birthplace": "美国", "alias": "Francis Ford Coppola"},
        "1054452": {"gender": "男", "birth_year": 1940, "birthplace": "美国", "alias": "Al Pacino"},
        "1041029": {"gender": "男", "birth_year": 1974, "birthplace": "美国", "alias": "Leonardo DiCaprio"},
        "1048027": {"gender": "女", "birth_year": 1966, "birthplace": "美国", "alias": "Robin Wright"},
        "1041381": {"gender": "男", "birth_year": 1961, "birthplace": "中国香港", "alias": "Anthony Wong"},
        "1004439": {"gender": "男", "birth_year": 1953, "birthplace": "中国香港", "alias": "Eric Tsang"},
        "1047973": {"gender": "男", "birth_year": 1959, "birthplace": "法国", "alias": "Frank Darabont"},
        "1013847": {"gender": "男", "birth_year": 1958, "birthplace": "英国伦敦", "alias": "Gary Oldman"},
        "1054446": {"gender": "女", "birth_year": 1975, "birthplace": "英国", "alias": "Kate Winslet"},
        "1006956": {"gender": "男", "birth_year": 1974, "birthplace": "英国", "alias": "Christian Bale"},
        "1054435": {"gender": "男", "birth_year": 1962, "birthplace": "加拿大", "alias": "Jim Carrey"},
        "1040997": {"gender": "男", "birth_year": 1964, "birthplace": "黎巴嫩贝鲁特", "alias": "Keanu Reeves"},
    }

    for pid, person in all_persons.items():
        extra = PERSON_EXTRA.get(pid, {})
        person.update(extra)
        person.setdefault('gender', None)
        person.setdefault('birth_year', None)
        person.setdefault('birthplace', None)
        person.setdefault('alias', None)
        persons_out.append(person)

    # 保存
    movies_path = os.path.join(DATA_DIR, 'movies.jsonl')
    persons_path = os.path.join(DATA_DIR, 'persons.jsonl')

    with open(movies_path, 'w', encoding='utf-8') as f:
        for m in movies_out:
            f.write(json.dumps(m, ensure_ascii=False) + '\n')

    with open(persons_path, 'w', encoding='utf-8') as f:
        for p in persons_out:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')

    print(f'Generated {len(movies_out)} movies -> {movies_path}')
    print(f'Generated {len(persons_out)} persons -> {persons_path}')

    # 统计
    genres = set()
    for m in movies_out:
        for g in m.get('genres', []):
            genres.add(g)
    print(f'Unique genres: {len(genres)} - {sorted(genres)}')
    movies_with_data = sum(1 for m in movies_out if m['genres'] or m['directors'])
    print(f'Movies with full detail: {movies_with_data}/{len(movies_out)}')
    print('Done!')


if __name__ == '__main__':
    generate_full_dataset()
