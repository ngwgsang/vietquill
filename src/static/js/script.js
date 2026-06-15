document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('input-text');
    const semanticSlider = document.getElementById('semantic-slider');
    const syntacticSlider = document.getElementById('syntactic-slider');
    const lexicalSlider = document.getElementById('lexical-slider');
    const numCandidatesSelect = document.getElementById('num-candidates');
    const numBeamsSelect = document.getElementById('num-beams');
    
    const semanticVal = document.getElementById('semantic-val');
    const syntacticVal = document.getElementById('syntactic-val');
    const lexicalVal = document.getElementById('lexical-val');
    
    const paraphraseBtn = document.getElementById('paraphrase-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const paraphraseList = document.getElementById('paraphrase-list');

    // Update labels on slider input
    semanticSlider.addEventListener('input', () => {
        semanticVal.textContent = semanticSlider.value;
    });
    
    syntacticSlider.addEventListener('input', () => {
        syntacticVal.textContent = syntacticSlider.value;
    });
    
    lexicalSlider.addEventListener('input', () => {
        lexicalVal.textContent = lexicalSlider.value;
    });

    const metricTags = document.querySelectorAll('.metric-tag');
    let activeMetrics = new Set();
    
    // Global state
    let currentCandidates = [];
    let currentOriginalText = '';
    let currentSort = { column: 'overall_score', direction: 'desc' };

    // Initialize active metrics from DOM
    metricTags.forEach(tag => {
        if (tag.classList.contains('active')) {
            activeMetrics.add(tag.dataset.metric);
        }
        
        // Add click listener for tags
        tag.addEventListener('click', () => {
            const metric = tag.dataset.metric;
            if (activeMetrics.has(metric)) {
                activeMetrics.delete(metric);
                tag.classList.remove('active');
            } else {
                activeMetrics.add(metric);
                tag.classList.add('active');
            }
            
            // Re-render if we have data
            if (currentCandidates.length > 0) {
                const sorted = sortCandidates(currentCandidates, currentSort.column, currentSort.direction);
                paraphraseList.innerHTML = '';
                paraphraseList.appendChild(renderResultsTable(sorted, currentOriginalText));
            }
        });
    });

    // Function to sort candidates
    function sortCandidates(candidates, column, direction) {
        if (!column) return candidates;
        return [...candidates].sort((a, b) => {
            let valA, valB;
            
            if (column === 'text') {
                valA = a.text.toLowerCase();
                valB = b.text.toLowerCase();
            } else if (['semantic_score', 'syntactic_score', 'lexical_score'].includes(column)) {
                valA = a.scores[column];
                valB = b.scores[column];
            } else if (column === 'overall_score') {
                valA = a.overall_score;
                valB = b.overall_score;
            } else {
                valA = a.metrics[column] || 0;
                valB = b.metrics[column] || 0;
            }
            
            if (valA < valB) return direction === 'asc' ? -1 : 1;
            if (valA > valB) return direction === 'asc' ? 1 : -1;
            return 0;
        });
    }

    const modal = document.getElementById('comparison-modal');
    const closeModal = document.getElementById('close-modal');
    const originalComp = document.getElementById('original-comparison');
    const paraphraseComp = document.getElementById('paraphrase-comparison');
    const originalTree = document.getElementById('original-tree');
    const paraphraseTree = document.getElementById('paraphrase-tree');
    const treeLoading = document.getElementById('tree-loading');
    const treeContainer = document.getElementById('tree-container');

    closeModal.addEventListener('click', () => modal.classList.add('hidden'));
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    async function compareWords(original, paraphrase) {
        // --- 1. Lexical Comparison (Synchronous) ---
        const getTokens = (text) => {
            return text.split(/\s+/).filter(t => t.length > 0).flatMap(part => {
                const subTokens = [];
                let current = part;
                while (current.length > 0 && /[.,!?;:]/.test(current[0])) {
                    subTokens.push(current[0]);
                    current = current.substring(1);
                }
                const trailing = [];
                while (current.length > 0 && /[.,!?;:]/.test(current[current.length - 1])) {
                    trailing.unshift(current[current.length - 1]);
                    current = current.substring(0, current.length - 1);
                }
                if (current.length > 0) subTokens.push(current);
                return [...subTokens, ...trailing];
            });
        };

        const tokens1 = getTokens(original);
        const tokens2 = getTokens(paraphrase);
        const t1 = tokens1.map(t => t.toLowerCase());
        const t2 = tokens2.map(t => t.toLowerCase());

        let matched1 = new Array(tokens1.length).fill(false);
        let matched2 = new Array(tokens2.length).fill(false);

        while (true) {
            let best = null;
            for (let i = 0; i < tokens1.length; i++) {
                if (matched1[i]) continue;
                for (let j = 0; j < tokens2.length; j++) {
                    if (matched2[j]) continue;
                    let len = 0;
                    while (i + len < tokens1.length && j + len < tokens2.length &&
                           !matched1[i + len] && !matched2[j + len] &&
                           t1[i + len] === t2[j + len]) {
                        len++;
                    }
                    if (len > 0 && (!best || len > best.len)) {
                        best = { i, j, len };
                    }
                }
            }

            if (!best || best.len === 0) break;
            
            if (best.len === 1) {
                const isStable = 
                    (best.i > 0 && matched1[best.i-1]) || 
                    (best.i < tokens1.length-1 && matched1[best.i+1]) ||
                    (best.j > 0 && matched2[best.j-1]) ||
                    (best.j < tokens2.length-1 && matched2[best.j+1]);
                
                if (!isStable) {
                    break; 
                }
            }

            for (let k = 0; k < best.len; k++) {
                matched1[best.i + k] = true;
                matched2[best.j + k] = true;
            }
        }

        let html1 = '';
        for (let i = 0; i < tokens1.length; i++) {
            if (matched1[i]) {
                html1 += tokens1[i] + ' ';
            } else {
                let hunk = tokens1[i];
                while (i + 1 < tokens1.length && !matched1[i + 1]) {
                    i++;
                    hunk += ' ' + tokens1[i];
                }
                html1 += `<span class="highlight-red">${hunk}</span> `;
            }
        }

        let html2 = '';
        for (let j = 0; j < tokens2.length; j++) {
            if (matched2[j]) {
                html2 += tokens2[j] + ' ';
            } else {
                let hunk = tokens2[j];
                while (j + 1 < tokens2.length && !matched2[j + 1]) {
                    j++;
                    hunk += ' ' + tokens2[j];
                }
                html2 += `<span class="highlight-blue">${hunk}</span> `;
            }
        }

        originalComp.innerHTML = html1.trim();
        paraphraseComp.innerHTML = html2.trim();
        
        // --- Helper: Parse Bracketed Tree String ---
        function parseTreeString(treeStr) {
            let tokens = treeStr.replace(/\(/g, ' ( ').replace(/\)/g, ' ) ').trim().split(/\s+/);
            if (tokens.length === 0) return null;
            
            function parse(tokens) {
                if (tokens.length === 0) return null;
                let token = tokens.shift();
                if (token === '(') {
                    let name = tokens.shift();
                    let node = { name: name, children: [] };
                    while (tokens.length > 0 && tokens[0] !== ')') {
                        node.children.push(parse(tokens));
                    }
                    tokens.shift(); // consume ')'
                    return node;
                } else {
                    return { name: token }; // Leaf node (word)
                }
            }
            return parse(tokens);
        }

        // --- Helper: Render D3 Tree ---
        function renderD3Tree(containerElement, treeData) {
            containerElement.innerHTML = ''; // clear previous
            if (!treeData) {
                containerElement.innerHTML = '<span style="color:red">Failed to parse tree data.</span>';
                return;
            }

            const containerRect = containerElement.getBoundingClientRect();
            // Fallback dimensions if container is hidden/0
            const width = containerRect.width || 600;
            const height = 400;

            const margin = { top: 40, right: 20, bottom: 40, left: 20 };

            const svg = d3.select(containerElement)
                .append('svg')
                .attr('width', '100%')
                .attr('height', height)
                .call(d3.zoom().on("zoom", (event) => {
                    svgGroup.attr("transform", event.transform);
                }))
                .on("dblclick.zoom", null); // disable double click zoom for better UX

            const svgGroup = svg.append('g')
                .attr('transform', `translate(${margin.left}, ${margin.top})`);

            // Creates a hierarchy from the nested JSON object
            const root = d3.hierarchy(treeData, d => d.children);

            // Compute tree layout
            // We use standard tree layout, orienting top-to-bottom
            const treeLayout = d3.tree().nodeSize([60, 60]);
            
            function update(source) {
                const treeData = treeLayout(root);
                const nodes = treeData.descendants();
                const links = treeData.descendants().slice(1);

                // Normalize for fixed-depth
                nodes.forEach(d => { d.y = d.depth * 80; });

                // Find center to align
                let minX = d3.min(nodes, d => d.x);
                let maxX = d3.max(nodes, d => d.x);
                let yOffset = margin.top;
                let xOffset = (width - (maxX - minX)) / 2 - minX;
                if(xOffset < margin.left) xOffset = margin.left;
                
                // Initial zoom/pan to center the tree
                if(source === root) {
                    const transform = d3.zoomIdentity.translate(xOffset, yOffset).scale(0.8);
                    svg.call(d3.zoom().transform, transform);
                }

                // ****************** Nodes section ***************************
                const node = svgGroup.selectAll('g.node')
                    .data(nodes, d => d.id || (d.id = ++i));

                const nodeEnter = node.enter().append('g')
                    .attr('class', 'node')
                    .attr('transform', d => `translate(${d.x},${d.y})`)
                    .on('click', (event, d) => {
                        if (d.children) {
                            d._children = d.children;
                            d.children = null;
                        } else {
                            d.children = d._children;
                            d._children = null;
                        }
                        update(d);
                    })
                    .on('mouseover', function(event, d) {
                        d3.select(this).select('.node-rect').classed('hover', true);
                        d3.select(this).select('.node-text').classed('hover', true);
                        // Highlight descendants
                        const descendants = d.descendants().map(desc => desc.id);
                        svgGroup.selectAll('.link')
                            .filter(l => descendants.includes(l.id))
                            .classed('highlight', true);
                        svgGroup.selectAll('.node')
                            .filter(n => descendants.includes(n.id))
                            .classed('highlight', true);
                    })
                    .on('mouseout', function(event, d) {
                        d3.select(this).select('.node-rect').classed('hover', false);
                        d3.select(this).select('.node-text').classed('hover', false);
                        // Remove highlight
                        svgGroup.selectAll('.link').classed('highlight', false);
                        svgGroup.selectAll('.node').classed('highlight', false);
                    });

                // Add Rectangles for non-leaf nodes
                const rectEnter = nodeEnter.filter(d => d.children || d._children)
                    .append('rect')
                    .attr('class', d => `node-rect ${d.data.status ? 'node-' + d.data.status : ''}`)
                    .attr('width', 50)
                    .attr('height', 24)
                    .attr('x', -25)
                    .attr('y', -12)
                    .attr('rx', 6)
                    .attr('ry', 6);
                
                rectEnter.append('title')
                    .text(d => {
                        if (d.data.status === 'preserved') return "Preserved constituent";
                        if (d.data.status === 'modified') return "Modified constituent";
                        if (d.data.status === 'added') return "Added constituent";
                        if (d.data.status === 'removed') return "Removed constituent";
                        return "";
                    });

                // Add labels for the nodes
                nodeEnter.append('text')
                    .attr('class', 'node-text')
                    .attr('dy', '.35em')
                    .attr('text-anchor', 'middle')
                    .text(d => d.data.name)
                    // Adjust styles based on leaf vs non-leaf
                    .style('font-weight', d => (d.children || d._children) ? '600' : '500')
                    .style('fill', d => (d.children || d._children) ? '#1e293b' : '#0f172a');
                
                // Style leaf nodes specifically
                nodeEnter.filter(d => !d.children && !d._children)
                    .select('.node-text')
                    .attr('class', 'node-text leaf-text');

                // UPDATE
                const nodeUpdate = nodeEnter.merge(node);
                nodeUpdate.transition().duration(200)
                    .attr('transform', d => `translate(${d.x},${d.y})`);

                // Update rect appearance based on collapse state (add class instead of inline styles)
                nodeUpdate.select('.node-rect')
                    .classed('node-collapsed', d => !!d._children)
                    .attr('class', d => `node-rect ${d._children ? 'node-collapsed' : ''} ${d.data.status ? 'node-' + d.data.status : ''}`);

                // Remove exiting nodes
                node.exit().transition().duration(200)
                    .attr('transform', d => `translate(${source.x},${source.y})`)
                    .remove();

                // ****************** links section ***************************
                const link = svgGroup.selectAll('path.link')
                    .data(links, d => d.id);

                const linkEnter = link.enter().insert('path', "g")
                    .attr('class', 'link')
                    .attr('d', d => {
                        const o = {x: source.x0 || source.x, y: source.y0 || source.y};
                        return diagonal(o, o);
                    });

                const linkUpdate = linkEnter.merge(link);
                linkUpdate.transition().duration(200)
                    .attr('d', d => diagonal(d, d.parent));

                link.exit().transition().duration(200)
                    .attr('d', d => {
                        const o = {x: source.x, y: source.y};
                        return diagonal(o, o);
                    })
                    .remove();

                // Store old positions for transition
                nodes.forEach(d => {
                    d.x0 = d.x;
                    d.y0 = d.y;
                });
                
                function diagonal(s, d) {
                    return `M ${s.x} ${s.y} C ${s.x} ${(s.y + d.y) / 2}, ${d.x} ${(s.y + d.y) / 2}, ${d.x} ${d.y}`;
                }
            }

            let i = 0; // for node IDs
            update(root);
        }

        // Show modal immediately with lexical changes and loading state for tree
        originalTree.innerHTML = '';
        paraphraseTree.innerHTML = '';
        treeContainer.classList.add('hidden');
        treeLoading.classList.remove('hidden');
        modal.classList.remove('hidden');

        // --- 2. Syntactic Comparison (Async API Call) ---
        try {
            const response = await fetch('/api/tree', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ original: original, paraphrase: paraphrase })
            });
            const data = await response.json();
            
            if (response.ok) {
                const tree1 = parseTreeString(data.original_tree);
                const tree2 = parseTreeString(data.paraphrase_tree);

                // Helper to extract leaves for jaccard comparison
                function getLeaves(node) {
                    if (!node) return [];
                    if (!node.children || node.children.length === 0) return [node.name.toLowerCase()];
                    let leaves = [];
                    for (let child of node.children) {
                        leaves = leaves.concat(getLeaves(child));
                    }
                    return leaves;
                }

                function jaccard(leaves1, leaves2) {
                    if (leaves1.length === 0 && leaves2.length === 0) return 1.0;
                    if (leaves1.length === 0 || leaves2.length === 0) return 0.0;
                    const set1 = new Set(leaves1);
                    const set2 = new Set(leaves2);
                    const intersection = new Set([...set1].filter(x => set2.has(x)));
                    const union = new Set([...set1, ...set2]);
                    return intersection.size / union.size;
                }

                // Recursively classify nodes
                function compareSubtrees(node1, node2) {
                    // Collect nodes by name at current level
                    const map1 = {}; const map2 = {};
                    if(node1 && node1.children) {
                        node1.children.forEach(c => {
                            if(c.children) { // only non-leaves
                                if(!map1[c.name]) map1[c.name] = [];
                                map1[c.name].push(c);
                            }
                        });
                    }
                    if(node2 && node2.children) {
                        node2.children.forEach(c => {
                            if(c.children) { // only non-leaves
                                if(!map2[c.name]) map2[c.name] = [];
                                map2[c.name].push(c);
                            }
                        });
                    }

                    // Process tree 1 (Original)
                    if(node1 && node1.children) {
                        node1.children.forEach(c1 => {
                            if(!c1.children) return; // skip leaves
                            let bestMatch = null;
                            let maxScore = -1;
                            if (map2[c1.name]) {
                                map2[c1.name].forEach(c2 => {
                                    if(c2.status) return; // already matched
                                    const l1 = getLeaves(c1);
                                    const l2 = getLeaves(c2);
                                    const score = jaccard(l1, l2);
                                    if (score > maxScore) {
                                        maxScore = score;
                                        bestMatch = c2;
                                    }
                                });
                            }

                            if (maxScore === 1.0) {
                                c1.status = 'preserved';
                                bestMatch.status = 'preserved';
                                compareSubtrees(c1, bestMatch);
                            } else if (maxScore > 0.0) {
                                c1.status = 'modified';
                                bestMatch.status = 'modified';
                                compareSubtrees(c1, bestMatch);
                            } else {
                                c1.status = 'removed';
                                // recursively mark all children as removed
                                function markRemoved(n) {
                                    if(n.children) {
                                        n.status = 'removed';
                                        n.children.forEach(markRemoved);
                                    }
                                }
                                markRemoved(c1);
                            }
                        });
                    }

                    // Process remaining in tree 2 (Paraphrase)
                    if(node2 && node2.children) {
                        node2.children.forEach(c2 => {
                            if(!c2.children) return; // skip leaves
                            if (!c2.status) {
                                c2.status = 'added';
                                // recursively mark all children as added
                                function markAdded(n) {
                                    if(n.children) {
                                        n.status = 'added';
                                        n.children.forEach(markAdded);
                                    }
                                }
                                markAdded(c2);
                            }
                        });
                    }
                }

                if (tree1 && tree2 && tree1.name === tree2.name) {
                    tree1.status = 'preserved';
                    tree2.status = 'preserved';
                    compareSubtrees(tree1, tree2);
                } else if (tree1 && tree2) {
                     tree1.status = 'modified';
                     tree2.status = 'modified';
                     compareSubtrees(tree1, tree2);
                }

                renderD3Tree(originalTree, tree1);
                renderD3Tree(paraphraseTree, tree2);
            } else {
                originalTree.innerHTML = '<span style="color:red">Error loading tree.</span>';
                paraphraseTree.innerHTML = '<span style="color:red">Error loading tree.</span>';
            }
        } catch (error) {
            console.error('Failed to fetch tree:', error);
            originalTree.innerHTML = '<span style="color:red">Error: ' + error.message + '</span>';
            paraphraseTree.innerHTML = '<span style="color:red">Error: ' + error.message + '</span>';
        } finally {
            treeLoading.classList.add('hidden');
            treeContainer.classList.remove('hidden');
        }
    }

    // Function to render results as a table
    function renderResultsTable(candidates, originalText) {
        const tableContainer = document.createElement('div');
        tableContainer.className = 'table-container';
        
        const table = document.createElement('table');
        table.className = 'results-table';
        
        const allHeaders = [
            { label: '#', key: null, always: true },
            { label: 'Paraphrase', key: 'text', always: true },
            { label: 'SEM', key: 'semantic_score', title: 'Semantic Score' },
            { label: 'SYN', key: 'syntactic_score', title: 'Syntactic Score' },
            { label: 'LEX', key: 'lexical_score', title: 'Lexical Score' },
            { label: 'BLEU', key: 'bleu', title: 'BLEU Score' },
            { label: 'BS', key: 'bertscore', title: 'BERTScore' },
            { label: 'JAC', key: 'jaccard_diversity', title: 'Jaccard Diversity' },
            { label: 'TED', key: 'ted', title: 'Tree Edit Distance' },
            { label: 'PARA', key: 'parascore', title: 'ParaScore' },
            { label: 'Score', key: 'overall_score', title: 'Overall Score' },
            { label: '', key: null, always: true }
        ];

        // Filter headers based on activeMetrics
        const headers = allHeaders.filter(h => h.always || activeMetrics.has(h.key));

        // Table Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        headers.forEach(h => {
            const th = document.createElement('th');
            if (h.title) th.title = h.title;
            th.textContent = h.label;
            
            if (h.key) {
                th.classList.add('sortable');
                if (currentSort.column === h.key) {
                    th.classList.add(currentSort.direction);
                }
                
                th.addEventListener('click', () => {
                    if (currentSort.column === h.key) {
                        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
                    } else {
                        currentSort.column = h.key;
                        currentSort.direction = 'desc';
                    }
                    
                    const sorted = sortCandidates(currentCandidates, currentSort.column, currentSort.direction);
                    paraphraseList.innerHTML = '';
                    paraphraseList.appendChild(renderResultsTable(sorted, originalText));
                });
            }
            
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Table Body
        const tbody = document.createElement('tbody');
        candidates.forEach((candidate, index) => {
            const tr = document.createElement('tr');
            if (candidate.is_best) tr.className = 'best-row';
            
            const scores = candidate.scores;
            const metrics = candidate.metrics;
            
            let rowHtml = `<td>${index + 1}</td>`;
            rowHtml += `<td class="text-cell">${candidate.text}</td>`;
            
            // Add cells based on headers
            headers.forEach(h => {
                if (h.always) return;
                
                if (['semantic_score', 'syntactic_score', 'lexical_score'].includes(h.key)) {
                    rowHtml += `<td class="score-cell">${scores[h.key]}</td>`;
                } else if (h.key === 'overall_score') {
                    rowHtml += `<td class="overall-cell"><strong>${candidate.overall_score}</strong></td>`;
                } else {
                    rowHtml += `<td class="metric-cell" data-metric="${h.key}">${metrics[h.key]}%</td>`;
                }
            });
            
            rowHtml += `
                <td>
                    <button class="table-copy-btn" title="Sao chép">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                    </button>
                </td>
            `;
            
            tr.innerHTML = rowHtml;

            // Text cell click listener for comparison
            const textCell = tr.querySelector('.text-cell');
            if (textCell) {
                textCell.title = "Nhấn để xem khác biệt từ vựng";
                textCell.addEventListener('click', () => {
                    compareWords(originalText, candidate.text);
                });
            }
            
            // Copy functionality for table row
            const copyBtn = tr.querySelector('.table-copy-btn');
            copyBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                navigator.clipboard.writeText(candidate.text).then(() => {
                    const originalSvg = copyBtn.innerHTML;
                    copyBtn.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    `;
                    tr.classList.add('copied');
                    setTimeout(() => {
                        copyBtn.innerHTML = originalSvg;
                        tr.classList.remove('copied');
                    }, 2000);
                });
            });
            
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        tableContainer.appendChild(table);
        return tableContainer;
    }

    // Handle Paraphrase button click
    paraphraseBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) {
            alert('Vui lòng nhập văn bản gốc!');
            return;
        }

        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        paraphraseBtn.disabled = true;

        const requestData = {
            text: text,
            semantic: parseInt(semanticSlider.value),
            syntactic: parseInt(syntacticSlider.value),
            lexical: parseInt(lexicalSlider.value),
            num_candidates: parseInt(numCandidatesSelect.value),
            num_beams: parseInt(numBeamsSelect.value)
        };

        try {
            const response = await fetch('/api/paraphrase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (response.ok) {
                currentCandidates = data.candidates;
                currentOriginalText = text; // Store globally
                currentSort = { column: 'overall_score', direction: 'desc' }; // Default sort
                
                const sorted = sortCandidates(currentCandidates, currentSort.column, currentSort.direction);
                paraphraseList.innerHTML = '';
                const table = renderResultsTable(sorted, currentOriginalText);
                paraphraseList.appendChild(table);
                
                resultsDiv.classList.remove('hidden');
                
                // Smooth scroll to results
                resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                alert('Lỗi: ' + (data.detail || 'Không thể kết nối đến máy chủ'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi gọi API');
        } finally {
            loadingDiv.classList.add('hidden');
            paraphraseBtn.disabled = false;
        }
    });
});