const url = "http://127.0.0.1:59702";

document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('searchTitle').value;

    const response = await fetch(`${url}/search?title=${title}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = ''; // Clear previous results

    if (response.ok) {
        const result = await response.json();
        const movies = result.Search || [];

        movies.forEach(movie => {
            const template = document.getElementById('movieTemplate').content.cloneNode(true);
            template.querySelector('.movie-title').textContent = movie.Title;
            template.querySelector('.movie-year').textContent = movie.Year;
            template.querySelector('.movie-poster').src = movie.Poster !== 'N/A' ? movie.Poster : '';
            searchResults.appendChild(template);
        });
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
});