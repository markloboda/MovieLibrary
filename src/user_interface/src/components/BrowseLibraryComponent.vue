<template>
  <HeaderComponent />
  <div class="browse-library">
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="Search for movies..." @keyup.enter="searchMovies" />
      <button @click="searchMovies">Search</button>
    </div>
    <div class="movie-grid">
      <div v-for="movie in movies" :key="movie.imdb_id" class="movie-entry">
        <img :src="movie.Poster" alt="Movie Poster" class="movie-poster" />
        <div class="movie-details">
          <h3>{{ movie.Title }}</h3>
          <button @click="addToWatchlist(movie)">Add to Watchlist</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "./HeaderComponent.vue";

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      apiUrl: "/service/browse-library",
      watchlistApiUrl: "/service/watchlist",
      searchQuery: "",
      movies: [],
    };
  },
  computed: {
    isUserLoggedIn() {
      return localStorage.getItem("activeUser") !== null;
    },
    getUserName() {
      return localStorage.getItem("activeUser").split("@")[0];
    },
  },
  methods: {
    async addToWatchlist(movie) {
      try {
        movie["imdb_id"] = movie["imdbID"];

        const body = JSON.stringify({
          title: movie["Title"],
          type: movie["Type"],
          imdb_id: movie["imdb_id"],
          added_date: Date.now(),
          year: movie["Year"],
          poster: movie["Poster"],
        });

        const response = await fetch(`${this.watchlistApiUrl}/add-movie`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: body,
        });
        if (response.ok) {
          alert("Movie added to watchlist successfully!");
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (err) {
        console.error("Add to watchlist error:", err);
        alert("An unexpected error occurred while adding to watchlist.");
      }
    },
    async searchMovies() {
      try {
        const response = await fetch(`${this.apiUrl}/search?title=${this.searchQuery}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          alert("Search successful!");
          const result = await response.json();
          this.movies = result.Search || [];
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (err) {
        console.error("Search error:", err);
        alert("An unexpected error occurred while searching for movies.");
      }
    },
  },
};
</script>

<style scoped>
.browse-library {
  padding: 20px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.movie-entry {
  position: relative;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: auto;
  display: block;
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

.search-bar {
  display: flex;
  align-items: center;
  flex: 1;
}

.search-bar input {
  flex: 0.8;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
