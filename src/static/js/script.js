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

    // Function to create a candidate card
    function createCandidateCard(candidate) {
        const card = document.createElement('div');
        card.className = `result-card ${candidate.is_best ? 'best' : ''}`;
        
        let bestBadge = '';
        if (candidate.is_best) {
            bestBadge = '<div class="best-badge">Tốt nhất</div>';
        }

        const scores = candidate.scores;
        const metrics = candidate.metrics;
        
        card.innerHTML = `
            ${bestBadge}
            <button class="copy-btn" title="Sao chép">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
            </button>
            <p class="candidate-text">${candidate.text}</p>
            
            <div class="card-footer">
                <div class="scores-row">
                    <div class="score-tag" title="Predicted Semantic Score">SEM: <span>${scores.semantic_score}</span></div>
                    <div class="score-tag" title="Predicted Syntactic Score">SYN: <span>${scores.syntactic_score}</span></div>
                    <div class="score-tag" title="Predicted Lexical Score">LEX: <span>${scores.lexical_score}</span></div>
                </div>
            </div>

            <div class="quality-dashboard">
                <div class="dashboard-title">
                    <svg xmlns="http://www.w3.org/2000/svg" style="width:16px;height:16px" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Quality Dashboard
                </div>
                <div class="metrics-grid">
                    <div class="metric-item overall-score-section">
                        <div class="metric-name">Overall Quality Score</div>
                        <div class="metric-value">${candidate.overall_score}</div>
                    </div>
                    
                    <div class="metric-item" title="BLEU score measures n-gram overlap with the source. Higher is more similar.">
                        <div class="metric-label-row">
                            <span class="metric-name">BLEU</span>
                            <span class="metric-value">${metrics.bleu}%</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${metrics.bleu}%"></div>
                        </div>
                    </div>

                    <div class="metric-item" title="BERTScore uses contextual embeddings to measure semantic similarity.">
                        <div class="metric-label-row">
                            <span class="metric-name">BERTScore</span>
                            <span class="metric-value">${metrics.bertscore}%</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${metrics.bertscore}%"></div>
                        </div>
                    </div>

                    <div class="metric-item" title="Jaccard Diversity measures how different the vocabulary is from the source.">
                        <div class="metric-label-row">
                            <span class="metric-name">Jaccard Div.</span>
                            <span class="metric-value">${metrics.jaccard_diversity}%</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${metrics.jaccard_diversity}%"></div>
                        </div>
                    </div>

                    <div class="metric-item" title="Tree Edit Distance (TED) measures syntactic similarity based on constituency trees.">
                        <div class="metric-label-row">
                            <span class="metric-name">TED (Syntactic)</span>
                            <span class="metric-value">${metrics.ted}%</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${metrics.ted}%"></div>
                        </div>
                    </div>

                    <div class="metric-item" title="ParaScore is a reference-free metric that combines semantic similarity and fluency.">
                        <div class="metric-label-row">
                            <span class="metric-name">ParaScore</span>
                            <span class="metric-value">${metrics.parascore}%</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${metrics.parascore}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Copy functionality
        const copyBtn = card.querySelector('.copy-btn');
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(candidate.text).then(() => {
                const originalSvg = copyBtn.innerHTML;
                copyBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                `;
                setTimeout(() => {
                    copyBtn.innerHTML = originalSvg;
                }, 2000);
            });
        });

        return card;
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
                paraphraseList.innerHTML = '';
                data.candidates.forEach(candidate => {
                    const card = createCandidateCard(candidate);
                    paraphraseList.appendChild(card);
                });
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
