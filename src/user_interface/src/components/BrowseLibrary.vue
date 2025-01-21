<template>
    <div>
        <h1>Browse Library</h1>
        <form @submit.prevent="searchMovies">
            <label for="searchTitle">Movie Title:</label>
            <input type="text" id="searchTitle" v-model="searchQuery" required />
            <button type="submit">Search</button>
        </form>

        <div id="searchResults">
            <div v-for="movie in movies" :key="movie.imdbID" class="movie-entry">
                <h2 class="movie-title">{{ movie.Title }}</h2>
                <p class="movie-year">{{ movie.Year }}</p>
                <img class="movie-poster" :src="movie.Poster !== 'N/A' ? movie.Poster : placeholderPoster"
                    alt="Movie Poster" />
                <button @click="addToWatchlist(movie)">Add to Watchlist</button>
                <button @click="addToWatched(movie)">Add to Watched</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            apiUrl: "http://165.227.245.243/browse-library",
            searchQuery: "",
            movies: [],
            placeholderPoster: "https://via.placeholder.com/150",
        };
    },
    methods: {
        async searchMovies() {
            try {
                const response = await fetch(`${this.apiUrl}/search?title=${this.searchQuery}`, {
                    method: "GET",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const result = await response.json();
                    this.movies = result.Search || [];
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Search error:", err);
                alert("An unexpected error occurred while searching.");
            }
        },
        async addToWatchlist(movie) {
            const token = localStorage.getItem("token");
            try {
                const response = await fetch(`${this.apiUrl}/watchlist`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ movie }),
                });

                if (response.ok) {
                    alert("Movie added to watchlist");
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Add to watchlist error:", err);
                alert("An unexpected error occurred while adding to watchlist.");
            }
        },
        async addToWatched(movie) {
            const token = localStorage.getItem("token");
            try {
                const response = await fetch(`${this.apiUrl}/watched`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ movie }),
                });

                if (response.ok) {
                    alert("Movie added to watched list");
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Add to watched error:", err);
                alert("An unexpected error occurred while adding to watched.");
            }
        },
    },
};
</script>

<style scoped>
.movie-entry {
    margin-bottom: 20px;
}

.movie-poster {
    max-width: 150px;
    margin: 10px 0;
}
</style>