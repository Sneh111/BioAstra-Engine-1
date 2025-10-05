document.addEventListener('DOMContentLoaded', () => {
    const searchBox = document.getElementById('search-box');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    const performSearch = async () => {
        const query = searchBox.value;
        if (!query) return;

        resultsContainer.innerHTML = '<p class="loading">Searching for relevant papers...</p>';

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            displayResults(results);
        } catch (error) {
            resultsContainer.innerHTML = '<p class="error">An error occurred while searching.</p>';
        }
    };

    const displayResults = (results) => {
        resultsContainer.innerHTML = '';
        if (results.length === 0) {
            resultsContainer.innerHTML = '<p>No results found.</p>';
            return;
        }

        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result-item';
            
            // --- NEW: Added button and summary container ---
            resultElement.innerHTML = `
                <h3>${result.pmcid}</h3>
                <p>${result.snippet}</p>
                <button class="summarize-btn" data-id="${result.pmcid}">Summarize with AI</button>
                <div class="summary-content" id="summary-${result.pmcid}"></div>
            `;
            resultsContainer.appendChild(resultElement);
        });
    };

    // --- NEW: Event listener for the "Summarize" buttons ---
    resultsContainer.addEventListener('click', async (event) => {
        if (event.target.classList.contains('summarize-btn')) {
            const button = event.target;
            const paperId = button.dataset.id;
            const summaryContainer = document.getElementById(`summary-${paperId}`);

            summaryContainer.innerHTML = '<p class="loading">The AI is thinking... (this may take a minute)</p>';
            button.disabled = true; // Disable button while summarizing

            try {
                const response = await fetch(`/summarize?id=${paperId}`);
                const data = await response.json();
                
                // Format the summary nicely (e.g., replace bullet points)
                const formattedSummary = data.summary.replace(/\•/g, '<br>•').replace(/\*/g, '<br>•');
                summaryContainer.innerHTML = `<div class="summary-box">${formattedSummary}</div>`;

            } catch (error) {
                summaryContainer.innerHTML = '<p class="error">Failed to get summary.</p>';
                button.disabled = false; // Re-enable button on error
            }
        }
    });

    searchButton.addEventListener('click', performSearch);
    searchBox.addEventListener('keypress', (e) => e.key === 'Enter' && performSearch());
});