"""
数据清洗脚本
- 读取 movies.jsonl 和 persons.jsonl
- 去重（按 douban_id）
- 缺失值处理
- 类型标签标准化
- 输出清洗后的 JSONL 文件
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

GENRE_SYNONYMS = {
    '搞笑': '喜剧',
    '惊悚': '恐怖',
    '文艺': '剧情',
    '枪战': '动作',
    '武打': '动作',
    '悬疑惊悚': '悬疑',
    '科幻动作': '动作',
}


def clean_movies(input_path, output_path):
    seen_ids = set()
    cleaned = []
    raw_count = 0

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            raw_count += 1
            try:
                movie = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            douban_id = movie.get('douban_id')
            if not douban_id or douban_id in seen_ids:
                continue
            seen_ids.add(douban_id)

            # 标准化类型标签
            genres = movie.get('genres') or []
            genres = [GENRE_SYNONYMS.get(g, g) for g in genres]

            cleaned.append({
                'douban_id': douban_id,
                'title': movie.get('title', '').strip() if movie.get('title') else '',
                'year': int(movie['year']) if movie.get('year') else None,
                'rating': float(movie['rating']) if movie.get('rating') else None,
                'duration': int(movie['duration']) if movie.get('duration') else None,
                'summary': (movie.get('summary') or '').strip()[:500] if movie.get('summary') else '',
                'poster_url': movie.get('poster_url'),
                'genres': genres,
                'countries': movie.get('countries') or [],
                'languages': movie.get('languages') or [],
                'directors': movie.get('directors') or [],
                'writers': movie.get('writers') or [],
                'actors': movie.get('actors') or [],
            })

    with open(output_path, 'w', encoding='utf-8') as f:
        for m in cleaned:
            f.write(json.dumps(m, ensure_ascii=False) + '\n')

    print(f'Movies: {raw_count} raw => {len(cleaned)} cleaned')
    return cleaned


def clean_persons(input_path, output_path):
    seen_ids = set()
    cleaned = []
    raw_count = 0

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            raw_count += 1
            try:
                person = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            douban_id = person.get('douban_id')
            if not douban_id or douban_id in seen_ids:
                continue
            seen_ids.add(douban_id)

            name = (person.get('name') or '').strip()
            if not name:
                continue

            cleaned.append({
                'douban_id': douban_id,
                'name': name,
                'alias': (person.get('alias') or '').strip().split('/')[0] if person.get('alias') else None,
                'gender': person.get('gender'),
                'birth_year': int(person['birth_year']) if person.get('birth_year') else None,
                'birthplace': person.get('birthplace'),
            })

    with open(output_path, 'w', encoding='utf-8') as f:
        for p in cleaned:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')

    print(f'Persons: {raw_count} raw => {len(cleaned)} cleaned')
    return cleaned


def main():
    movies_in = os.path.join(DATA_DIR, 'movies.jsonl')
    movies_out = os.path.join(DATA_DIR, 'movies_cleaned.jsonl')
    persons_in = os.path.join(DATA_DIR, 'persons.jsonl')
    persons_out = os.path.join(DATA_DIR, 'persons_cleaned.jsonl')

    if os.path.exists(movies_in):
        clean_movies(movies_in, movies_out)
    else:
        print(f'Warning: {movies_in} not found, skipping movies')

    if os.path.exists(persons_in):
        clean_persons(persons_in, persons_out)
    else:
        print(f'Warning: {persons_in} not found, skipping persons')


if __name__ == '__main__':
    main()
