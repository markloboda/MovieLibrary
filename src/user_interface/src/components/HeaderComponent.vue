<template>
  <div class="header">
    <div class="home-logo">
      <router-link to="/">Movie Library</router-link>
    </div>
    <div class="user-button">
      <button v-if="isUserLoggedIn" @click="toggleUserMenu">{{ getUserName }}</button>
      <button v-else @click="openSignin">Sign In</button>
    </div>
    <div v-if="showUserMenu" class="user-menu" @click.self="toggleUserMenu">
      <button @click="openWatchlist">Watchlist</button>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showUserMenu: false,
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
    openSignin() {
      this.$router.push({ name: "SignIn" });
    },
    openWatchlist() {
      this.$router.push({ name: "Watchlist" });
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    logout() {
      localStorage.removeItem("activeUser");
      location.reload();
    },
  }
}
</script>

<style scoped>
.header {
  position: relative;
  background: #333;
  color: white;
  top: 0px;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-button {
  position: absolute;
  right: 20px;
}

.user-menu {
  position: absolute;
  top: 50px;
  right: 20px;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
}

.user-menu button {
  display: block;
  width: 100%;
}

.home-logo {
  font-size: 24px;
  font-weight: bold;
}
</style>