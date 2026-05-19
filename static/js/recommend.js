const Recommend = {
    init() {
        this.loadPopular();
    },

    loadPopular() {
        fetch('/api/recommend/popular')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('recommend-list');
                let html = '';
                for (const m of data.movies) {
                    html += '<div class="rec-item" data-id="' + m.douban_id + '">' +
                        '<span>' + m.title + '</span>' +
                        '<span class="rec-rating">' + m.rating + '</span>' +
                        '<br><small>' + (m.year || '') + '</small>' +
                    '</div>';
                }
                container.innerHTML = html;

                container.querySelectorAll('.rec-item').forEach(el => {
                    el.addEventListener('click', () => {
                        GraphVis.loadEntity('movie', el.dataset.id);
                        this.showSimilar(el.dataset.id);
                    });
                });
            });
    },

    showSimilar(doubanId) {
        const panel = document.getElementById('recommend-panel');
        const h3 = panel.querySelector('h3');
        h3.textContent = '同类推荐';

        fetch('/api/recommend/similar/' + doubanId)
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('recommend-list');
                let html = '';
                const movies = data.movies.slice(0, 6);
                for (const m of movies) {
                    html += '<div class="rec-item" data-id="' + m.douban_id + '">' +
                        '<span>' + m.title + '</span>' +
                        '<span class="rec-rating">' + m.rating + '</span>' +
                        '<br><small>' + (m.year || '') + '</small>' +
                    '</div>';
                }
                container.innerHTML = html;
                container.querySelectorAll('.rec-item').forEach(el => {
                    el.addEventListener('click', () => {
                        GraphVis.loadEntity('movie', el.dataset.id);
                        this.showSimilar(el.dataset.id);
                    });
                });
            });
    },

    showCollaboration(doubanId) {
        fetch('/api/recommend/collaboration/' + doubanId)
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('recommend-list');
                let html = '';
                for (const m of data.movies) {
                    html += '<div class="rec-item" data-id="' + m.douban_id + '">' +
                        '<span>' + m.title + '</span>' +
                        '<span class="rec-rating">' + m.rating + '</span>' +
                        '<br><small style="color:#888">' + (m.reason || '') + '</small>' +
                    '</div>';
                }
                container.innerHTML = html;
            });
    },
};
