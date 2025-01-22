<template>
  <div class="watchlist">
    <h1>My Watchlist</h1>
    <div v-if="movies.length">
      <div v-for="movie in movies" :key="movie.id" class="movie-item">
        <img :src="movie.poster" alt="Movie Poster" class="movie-poster" />
        <div class="movie-details">
          <h2>{{ movie.title }}</h2>
          <p>{{ movie.description }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No movies in your watchlist.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      apiUrl: "http://165.227.245.243/service/watchlist",
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
    }
  }
};
</script>

<style scoped>
.watchlist {
  padding: 20px;
}

.movie-item {
  display: flex;
  margin-bottom: 20px;
}

.movie-poster {
  width: 100px;
  height: 150px;
  margin-right: 20px;
}

.movie-details {
  flex: 1;
}

.movie-details h2 {
  margin: 0;
}

.movie-details p {
  margin: 5px 0 0;
}
</style>