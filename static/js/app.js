(function () {
    GraphVis.init();
    Search.init();
    Recommend.init();

    // 加载图谱统计
    fetch('/api/graph/stats')
        .then(r => r.json())
        .then(data => {
            document.getElementById('stat-movies').textContent = data.movie_count || '--';
            document.getElementById('stat-persons').textContent = data.person_count || '--';
            document.getElementById('stat-genres').textContent = data.genre_count || '--';
            document.getElementById('stat-relations').textContent = data.relation_count || '--';
        });

    // 路径分析
    document.getElementById('path-search').addEventListener('click', () => {
        const fromName = document.getElementById('path-from').value.trim();
        const toName = document.getElementById('path-to').value.trim();
        if (!fromName || !toName) {
            document.getElementById('path-result').textContent = '请输入起点和终点';
            return;
        }

        Promise.all([
            fetch('/api/search?q=' + encodeURIComponent(fromName)).then(r => r.json()),
            fetch('/api/search?q=' + encodeURIComponent(toName)).then(r => r.json()),
        ]).then(([fromRes, toRes]) => {
            const fromId = (fromRes.movies[0] || fromRes.persons[0] || {}).douban_id;
            const toId = (toRes.movies[0] || toRes.persons[0] || {}).douban_id;

            if (!fromId || !toId) {
                document.getElementById('path-result').textContent = '未找到对应实体';
                return;
            }

            GraphVis.loadPath(fromId, toId, (err) => {
                if (err) {
                    document.getElementById('path-result').textContent = '未找到连接路径（6跳内）';
                } else {
                    document.getElementById('path-result').textContent = '已找到 ' + fromName + ' → ' + toName + ' 的路径';
                }
            });
        });
    });

    // 默认加载一个起始实体
    fetch('/api/search?q=周星驰')
        .then(r => r.json())
        .then(data => {
            if (data.persons.length > 0) {
                GraphVis.loadEntity('person', data.persons[0].douban_id);
            }
        });
})();
