<template>
  <div id="app">
    <header>
      <h1>QTI3 Item Player</h1>
    </header>
    <main>
      <Qti3Player />
    </main>
  </div>
</template>

<script>
import Qti3Player from './Qti3Player.vue'

export default {
  name: 'App',
  components: {
    Qti3Player
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>