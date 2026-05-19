const GraphVis = {
    svg: null,
    simulation: null,
    nodesData: [],
    linksData: [],
    width: 0,
    height: 0,

    COLOR: {
        Movie: '#4361ee',
        Person: '#f72585',
        Genre: '#4cc9f0',
        Country: '#7209b7',
        Language: '#06d6a0',
        Year: '#ffd166',
    },

    init() {
        const container = document.getElementById('graph-container');
        this.width = container.clientWidth;
        this.height = container.clientHeight;

        this.svg = d3.select('#graph-container')
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        this.svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', (event) => {
            this.svg.selectAll('g.main').attr('transform', event.transform);
        }));

        this.svg.append('g').attr('class', 'main');

        window.addEventListener('resize', () => {
            this.width = container.clientWidth;
            this.height = container.clientHeight;
            this.svg.attr('width', this.width).attr('height', this.height);
        });
    },

    loadEntity(entityType, doubanId) {
        fetch(`/api/graph/entity/${entityType}/${doubanId}`)
            .then(r => r.json())
            .then(data => {
                if (data.error) { alert(data.error); return; }
                this.render(data.nodes, data.links);
            })
            .catch(err => console.error('Graph load error:', err));
    },

    loadPath(fromId, toId, callback) {
        fetch(`/api/graph/path?from_id=${fromId}&to_id=${toId}`)
            .then(r => r.json())
            .then(data => {
                if (data.error) { callback(data.error); return; }
                this.render(data.nodes, data.links);
                callback(null);
            })
            .catch(err => callback(err.message));
    },

    render(nodes, links) {
        this.nodesData = nodes.map(n => ({...n}));
        this.linksData = links.map(l => ({...l}));

        const g = this.svg.select('g.main');
        g.selectAll('*').remove();

        // 箭头定义
        g.append('defs').selectAll('marker')
            .data(['end'])
            .enter().append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#999');

        // 连线
        const link = g.append('g').selectAll('line')
            .data(links)
            .enter().append('line')
            .attr('stroke', '#ccc')
            .attr('stroke-width', d => d.type === 'COLLABORATED_WITH' ? 2 : 1)
            .attr('stroke-dasharray', d => d.type === 'SIMILAR_TO' ? '5,5' : null)
            .attr('marker-end', 'url(#arrowhead)');

        // 连线标签
        const linkLabel = g.append('g').selectAll('text')
            .data(links)
            .enter().append('text')
            .text(d => d.type.replace(/_/g, ' '))
            .attr('font-size', '8')
            .attr('fill', '#999')
            .attr('text-anchor', 'middle');

        // 节点
        const node = g.append('g').selectAll('g')
            .data(nodes)
            .enter().append('g')
            .style('cursor', 'pointer');

        node.append('circle')
            .attr('r', d => {
                const base = 12;
                if (d.label === 'Movie') return base + (d.rating || 5) * 1.5;
                if (d.label === 'Person') return base;
                return 8;
            })
            .attr('fill', d => this.COLOR[d.label] || '#999')
            .attr('stroke', '#fff')
            .attr('stroke-width', 1.5);

        node.append('text')
            .text(d => {
                const displayName = d.title || d.name || d.value || '';
                return displayName.length > 8 ? displayName.slice(0, 8) + '…' : displayName;
            })
            .attr('dy', 22)
            .attr('text-anchor', 'middle')
            .attr('font-size', '10')
            .attr('fill', '#333');

        // Hover tooltip
        const tooltip = document.getElementById('graph-tooltip');
        node.on('mouseover', (event, d) => {
            tooltip.style.display = 'block';
            while (tooltip.firstChild) tooltip.removeChild(tooltip.firstChild);
            const strong = document.createElement('strong');
            strong.textContent = d.label;
            tooltip.appendChild(strong);
            tooltip.appendChild(document.createElement('br'));
            tooltip.appendChild(document.createTextNode(d.title || d.name || d.value || ''));
            if (d.rating) {
                tooltip.appendChild(document.createElement('br'));
                tooltip.appendChild(document.createTextNode('评分: ' + d.rating));
            }
            if (d.year) {
                tooltip.appendChild(document.createElement('br'));
                tooltip.appendChild(document.createTextNode('年份: ' + d.year));
            }
        }).on('mousemove', (event) => {
            tooltip.style.left = (event.offsetX + 12) + 'px';
            tooltip.style.top = (event.offsetY - 10) + 'px';
        }).on('mouseout', () => {
            tooltip.style.display = 'none';
        }).on('click', (event, d) => {
            if (d.label === 'Movie' || d.label === 'Person') {
                const etype = d.label === 'Movie' ? 'movie' : 'person';
                this.loadEntity(etype, d.douban_id || d.id);
            }
        });

        // 力学仿真
        this.simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide(30))
            .on('tick', () => {
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);

                linkLabel
                    .attr('x', d => (d.source.x + d.target.x) / 2)
                    .attr('y', d => (d.source.y + d.target.y) / 2);

                node.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');
            });

        // 拖拽
        node.call(d3.drag()
            .on('start', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            })
        );
    },
};
