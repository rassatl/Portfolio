<script setup>
defineProps({
  type: {
    type: String,
    default: 'card', // 'card', 'text', 'title'
    validator: (value) => ['card', 'text', 'title', 'timeline-card'].includes(value)
  },
  count: {
    type: Number,
    default: 1
  }
})
</script>

<template>
  <!-- Skeleton pour carte de projet -->
  <div v-if="type === 'card'" class="bg-white rounded-xl shadow-lg p-6 border-2 border-green-300">
    <div class="flex justify-between items-start mb-3">
      <div class="h-8 w-2/3 bg-gray-300 rounded animate-pulse"></div>
      <div class="h-6 w-16 bg-gray-300 rounded animate-pulse"></div>
    </div>
    <div class="space-y-2 mb-4">
      <div class="h-4 bg-gray-300 rounded animate-pulse"></div>
      <div class="h-4 bg-gray-300 rounded animate-pulse"></div>
      <div class="h-4 bg-gray-300 rounded animate-pulse w-5/6"></div>
    </div>
    <div class="h-6 w-24 bg-gray-300 rounded animate-pulse"></div>
  </div>

  <!-- Skeleton pour titre -->
  <div v-else-if="type === 'title'" class="h-14 w-96 bg-gray-300 rounded-lg animate-pulse mx-auto"></div>

  <!-- Skeleton pour texte -->
  <div v-else-if="type === 'text'" class="h-6 w-80 bg-gray-300 rounded animate-pulse mx-auto"></div>

  <!-- Skeleton pour carte de timeline -->
  <div v-else-if="type === 'timeline-card'" class="flex gap-4">
    <div class="flex-shrink-0">
      <div class="w-12 h-12 bg-gray-300 rounded-full animate-pulse"></div>
    </div>
    <div class="flex-1 bg-white rounded-xl shadow-lg p-6 border-2 border-blue-300">
      <div class="h-6 w-32 bg-gray-300 rounded animate-pulse mb-2"></div>
      <div class="h-7 w-48 bg-gray-300 rounded animate-pulse mb-3"></div>
      <div class="space-y-2">
        <div class="h-4 bg-gray-300 rounded animate-pulse"></div>
        <div class="h-4 bg-gray-300 rounded animate-pulse w-5/6"></div>
      </div>
    </div>
  </div>
</template>
