<template>
  <div id="app">
    <BrowseLibrary />
  </div>
</template>

<script>
import BrowseLibrary from "./components/BrowseLibrary.vue";

export default {
  components: {
    BrowseLibrary,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
