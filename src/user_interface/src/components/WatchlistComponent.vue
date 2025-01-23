<template>
  <HeaderComponent />
  <div class="watchlist">
    <h1>My Watchlist</h1>
    <div v-if="movies.length">
      <div class="movie-grid">
        <div v-for="movie in movies" :key="movie.imdb_id" class="movie-entry">
          <img :src="movie.poster" alt="Movie Poster" class="movie-poster" />
          <div class="movie-details">
            <h3>{{ movie.Title }}</h3>
            <button @click="removeFromWatchlist(movie)">Remove from Watchlist</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No movies in your watchlist.</p>
    </div>
  </div>
</template>

<script>
import HeaderComponent from './HeaderComponent.vue';

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      apiUrl: "/service/watchlist",
      movies: []
    };
  },
  created() {
    this.fetchWatchlist();
  },
  methods: {
    async fetchWatchlist() {
      try {
        const response = await fetch(`${this.apiUrl}/get-movies`, {
          method: "GET",
          credentials: 'include',
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          alert("Watchlist fetched successfully!");
          const data = await response.json();
          this.movies = data["movies"] || [];
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
          this.$router.push("/signin");
        }
      } catch (err) {
        console.error("Add to watchlist error:", err);
        alert("An unexpected error occurred while fetching to watchlist.");
      }
    },
    async removeFromWatchlist(movie) {
      try {
        const body = JSON.stringify({
          imdb_id: movie["imdb_id"],
        });

        const response = await fetch(`${this.apiUrl}/remove-movie`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: body,
        });
        if (response.ok) {
          alert("Movie removed from watchlist successfully!");
          this.fetchWatchlist();
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (err) {
        console.error("Remove from watchlist error:", err);
        alert("An unexpected error occurred while removing from watchlist.");
      }
    }
  }
};
</script>

<style scoped>
.watchlist {
  padding: 20px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.movie-poster {
  width: 100%;
  height: auto;
  display: block;
}

.movie-entry {
  position: relative;
  overflow: hidden;
}

.movie-entry:hover .movie-details {
  opacity: 1;
}

.movie-details {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.movie-entry:hover .movie-details {
  opacity: 1;
}

.movie-details h3 {
  margin: 0 0 10px;
}

.movie-details button {
  margin-right: 10px;
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.movie-details button:hover {
  background-color: #f0f0f0;
}
</style>