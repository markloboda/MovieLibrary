const apiUrl = "http://165.227.245.243/browse-library";

document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('searchTitle').value;

    const response = await fetch(`${apiUrl}/search?title=${title}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = '';  // Clear previous results

    if (response.ok) {
        const result = await response.json();
        const movies = result.Search || [];

        movies.forEach(movie => {
            const template = document.getElementById('movieTemplate').content.cloneNode(true);
            template.querySelector('.movie-title').textContent = movie.Title;
            template.querySelector('.movie-year').textContent = movie.Year;
            template.querySelector('.movie-poster').src = movie.Poster !== 'N/A' ? movie.Poster : '';
            template.querySelector('.add-to-watchlist').addEventListener('click', () => addToWatchlist(movie));
            template.querySelector('.add-to-watched').addEventListener('click', () => addToWatched(movie));
            searchResults.appendChild(template);
        });
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
});

async function addToWatchlist(movie) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${apiUrl}/watchlist`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ movie })
    });

    if (response.ok) {
        alert('Movie added to watchlist');
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
}

async function addToWatched(movie) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${apiUrl}/watched`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ movie })
    });

    if (response.ok) {
        alert('Movie added to watched list');
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
}