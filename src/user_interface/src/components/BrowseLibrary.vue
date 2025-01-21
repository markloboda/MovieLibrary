<template>
  <div class="browse-library">
    <div class="header">
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search for movies..." @keyup.enter="searchMovies" />
        <button @click="searchMovies">Search</button>
      </div>
      <button class="sign-in-button" @click="openLoginRegister">Sign In</button>
    </div>
    <div class="movie-list">
      <div v-for="movie in movies" :key="movie.imdbID" class="movie-entry">
        <img :src="movie.Poster" alt="Movie Poster" class="movie-poster" />
        <div class="movie-details">
          <h3>{{ movie.Title }}</h3>
          <button @click="addToWatchlist(movie)">Add to Watchlist</button>
          <button @click="addToWatched(movie)">Add to Watched</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      movies: [],
      apiUrl: 'http://165.227.245.243/browse-library'
    };
  },
  methods: {
    async searchMovies() {
      try {
        const response = await fetch(`${this.apiUrl}/search?title=${this.searchQuery}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        const result = await response.json();
        this.movies = result.Search || [];
      } catch (err) {
        console.error("Search error:", err);
        alert("An unexpected error occurred while searching for movies.");
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
    openLoginRegister() {
      this.$router.push({ name: 'LoginRegister' });
    }
  },
};
</script>

<style scoped>
.browse-library {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
}

.search-bar input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-bar button {
  margin-left: 10px;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.sign-in-button {
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.movie-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.movie-entry {
  display: flex;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.movie-poster {
  max-width: 150px;
  margin-right: 20px;
}

.movie-details {
  flex: 1;
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