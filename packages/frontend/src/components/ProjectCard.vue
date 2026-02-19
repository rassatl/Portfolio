<script setup>
import SkillTag from './SkillTag.vue'
import { formatDate } from '../composables/useFormatters'

defineProps({
  project: {
    type: Object,
    required: true
  },
  compact: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div
    :class="[
      'bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 border-green-300',
      compact ? 'max-w-sm' : ''
    ]"
  >
    <div class="flex justify-between items-start mb-3">
      <h2 class="text-2xl font-bold text-gray-800">{{ project.title }}</h2>
      <span class="text-sm text-gray-500 font-semibold whitespace-nowrap ml-2">
        {{ formatDate(project.date) }}
      </span>
    </div>
    
    <p class="text-gray-600 mb-4 leading-relaxed">
      {{ project.description || 'Aucune description disponible' }}
    </p>
    
    <!-- Tags de compétences -->
    <div v-if="project.skills && project.skills.length > 0" class="mb-4">
      <div class="flex flex-wrap gap-2">
        <SkillTag
          v-for="skill in project.skills"
          :key="skill"
          :skill="skill"
          variant="default"
          size="md"
        />
      </div>
    </div>
    
    <!-- Liens -->
    <div class="flex gap-3">
      <a
        v-if="project.github && project.github !== '#'"
        :href="project.github"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-2 text-green-600 hover:text-green-700 font-semibold transition-colors"
      >
        <span>🐙</span>
        <span>GitHub</span>
      </a>
      
      <a
        v-if="project.lien"
        :href="project.lien"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold transition-colors"
      >
        <span>🌐</span>
        <span>Voir le site</span>
      </a>
    </div>
  </div>
</template>
