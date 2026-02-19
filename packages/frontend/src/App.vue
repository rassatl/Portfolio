<script setup>
import Navigation from './components/Navigation.vue'
</script>

<template>
  <div id="app" class="min-h-screen">
    <Navigation />
    <RouterView v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </RouterView>
  </div>
</template>

<style scoped>
</style>
