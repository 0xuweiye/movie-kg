const Search = {
    escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    },

    init() {
        const input = document.getElementById('search-input');
        let debounceTimer;
        input.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => this.doSearch(input.value), 300);
        });

        document.getElementById('filter-apply').addEventListener('click', () => this.doFilter());
        this.loadFilterOptions();
    },

    doSearch(query) {
        if (!query.trim()) {
            document.getElementById('search-results').innerHTML = '';
            return;
        }
        fetch('/api/search?q=' + encodeURIComponent(query))
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('search-results');
                let html = '';
                const all = data.movies.concat(data.persons);
                for (const item of all) {
                    const label = item.type === 'movie' ? '电影' : '人物';
                    const name = this.escapeHtml(item.title || item.name);
                    html += '<div class="search-item" data-type="' + this.escapeHtml(item.type) + '" data-id="' + this.escapeHtml(item.douban_id) + '" data-name="' + name + '">' +
                        '<span class="type-tag ' + this.escapeHtml(item.type) + '">' + label + '</span>' + name +
                        (item.year ? ' (' + this.escapeHtml(item.year) + ')' : '') +
                        (item.rating ? ' ★' + this.escapeHtml(item.rating) : '') +
                    '</div>';
                }
                if (all.length === 0) html = '<div class="search-item" style="color:#999">无结果</div>';
                container.innerHTML = html;

                container.querySelectorAll('.search-item[data-id]').forEach(el => {
                    el.addEventListener('click', () => {
                        const etype = el.dataset.type;
                        GraphVis.loadEntity(etype, el.dataset.id);
                        container.innerHTML = '';
                        document.getElementById('search-input').value = el.dataset.name;
                    });
                });
            });
    },

    loadFilterOptions() {
        fetch('/api/genres').then(r => r.json()).then(genres => {
            const sel = document.getElementById('filter-genre');
            genres.forEach(g => {
                sel.innerHTML += '<option value="' + this.escapeHtml(g.name) + '">' + this.escapeHtml(g.name) + ' (' + g.count + ')</option>';
            });
        });
        fetch('/api/countries').then(r => r.json()).then(countries => {
            const sel = document.getElementById('filter-country');
            countries.forEach(c => {
                sel.innerHTML += '<option value="' + this.escapeHtml(c.name) + '">' + this.escapeHtml(c.name) + ' (' + c.count + ')</option>';
            });
        });
    },

    doFilter() {
        const params = new URLSearchParams();
        const genre = document.getElementById('filter-genre').value;
        const yearFrom = document.getElementById('filter-year-from').value;
        const yearTo = document.getElementById('filter-year-to').value;
        const country = document.getElementById('filter-country').value;
        if (genre) params.set('genre', genre);
        if (yearFrom) params.set('year_from', yearFrom);
        if (yearTo) params.set('year_to', yearTo);
        if (country) params.set('country', country);

        fetch('/api/filter?' + params.toString())
            .then(r => r.json())
            .then(data => {
                if (data.movies.length > 0) {
                    const nodes = [];
                    const links = [];
                    const centerId = 'filter-center';
                    nodes.push({id: centerId, label: 'Genre', name: genre || country || '筛选结果'});
                    for (const m of data.movies) {
                        const mId = m.douban_id;
                        nodes.push({id: mId, label: 'Movie', douban_id: mId, title: m.title, year: m.year, rating: m.rating});
                        links.push({source: centerId, target: mId, type: 'FILTER_RESULT'});
                    }
                    GraphVis.render(nodes, links);
                }
            });
    },
};
