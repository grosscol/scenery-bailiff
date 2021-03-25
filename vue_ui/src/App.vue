<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <TopBanner/>
    <LoginStatus/>
  </div>
</template>

<script>
import TopBanner from './components/TopBanner.vue'
import LoginStatus from './components/LoginStatus.vue'

export default {
  name: 'App',
  components: {
    TopBanner,
    LoginStatus
  }
}
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
