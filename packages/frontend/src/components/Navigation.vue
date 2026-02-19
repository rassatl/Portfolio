<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const isActive = (name) => computed(() => route.name === name)
</script>

<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <div class="text-xl font-bold text-gray-800">
          Mon Portfolio
        </div>
        <div class="flex gap-6">
          <RouterLink
            to="/"
            class="px-4 py-2 rounded-lg transition-colors duration-200"
            :class="isActive('home').value 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-700 hover:bg-gray-100'"
          >
            Accueil
          </RouterLink>
          <RouterLink
            to="/projets"
            class="px-4 py-2 rounded-lg transition-colors duration-200"
            :class="isActive('projets').value 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-700 hover:bg-gray-100'"
          >
            Projets
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
</style>
