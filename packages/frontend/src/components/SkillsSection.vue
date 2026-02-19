<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  skills: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Catégoriser les compétences par type
const skillCategories = {
  'Frontend': ['Vue.js', 'React', 'JavaScript', 'TypeScript', 'Tailwind', 'HTML', 'CSS', 'Vite'],
  'Backend': ['Python', 'FastAPI', 'Node.js', 'Express', 'Flask', 'Django'],
  'Bases de données': ['PostgreSQL', 'MongoDB', 'MySQL', 'Firebase'],
  'Outils & DevOps': ['Git', 'Docker', 'GitHub', 'Vercel', 'AWS', 'Linux'],
  'Autres': []
}

const categorizedSkills = computed(() => {
  const result = {}
  const usedSkills = new Set()

  // Remplir les catégories existantes
  for (const [category, keywords] of Object.entries(skillCategories)) {
    if (category === 'Autres') continue
    result[category] = []
    
    props.skills.forEach(skill => {
      const matches = keywords.some(keyword => 
        skill.toLowerCase().includes(keyword.toLowerCase()) || 
        keyword.toLowerCase().includes(skill.toLowerCase())
      )
      if (matches) {
        result[category].push(skill)
        usedSkills.add(skill)
      }
    })
  }

  // Compétences non catégorisées dans "Autres"
  result['Autres'] = props.skills.filter(skill => !usedSkills.has(skill))

  // Supprimer catégories vides
  return Object.fromEntries(
    Object.entries(result).filter(([_, skills]) => skills.length > 0)
  )
})

const categoryEmojis = {
  'Frontend': '🎨',
  'Backend': '⚙️',
  'Bases de données': '💾',
  'Outils & DevOps': '🛠️',
  'Autres': '⭐'
}

const categoryColors = {
  'Frontend': { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-blue-300', tag: 'bg-blue-500' },
  'Backend': { bg: 'bg-purple-100', text: 'text-purple-700', border: 'border-purple-300', tag: 'bg-purple-500' },
  'Bases de données': { bg: 'bg-green-100', text: 'text-green-700', border: 'border-green-300', tag: 'bg-green-500' },
  'Outils & DevOps': { bg: 'bg-orange-100', text: 'text-orange-700', border: 'border-orange-300', tag: 'bg-orange-500' },
  'Autres': { bg: 'bg-indigo-100', text: 'text-indigo-700', border: 'border-indigo-300', tag: 'bg-indigo-500' }
}
</script>

<template>
  <div class="space-y-3">
    <!-- Titre -->
    <div>
      <h3 v-if="loading" class="h-7 w-32 bg-gray-300 rounded animate-pulse"></h3>
      <h3 v-else class="text-2xl font-bold text-gray-800">💡 Compétences</h3>
    </div>

    <!-- Skeleton de chargement -->
    <div v-if="loading" class="space-y-2">
      <div v-for="n in 3" :key="n" class="space-y-2">
        <div class="h-5 w-24 bg-gray-300 rounded animate-pulse"></div>
        <div class="flex flex-wrap gap-2">
          <div v-for="i in 5" :key="i" class="h-8 w-16 bg-gray-300 rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>

    <!-- Catégories de compétences - Disposition compacte -->
    <div v-else class="grid grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="(categorySkills, category) in categorizedSkills"
        :key="category"
        class="space-y-2"
      >
        <!-- En-tête de catégorie -->
        <div 
          :class="[
            'inline-flex items-center gap-1 px-3 py-1 rounded-lg font-medium text-sm border',
            categoryColors[category].bg,
            categoryColors[category].text,
            categoryColors[category].border
          ]"
        >
          <span class="text-base">{{ categoryEmojis[category] }}</span>
          <span>{{ category }}</span>
          <span class="ml-1 px-1 py-0 bg-white rounded text-xs font-bold">
            {{ categorySkills.length }}
          </span>
        </div>

        <!-- Tags de compétences -->
        <div class="flex flex-wrap gap-1">
          <button
            v-for="skill in categorySkills"
            :key="skill"
            :class="[
              'px-2 py-1 rounded-full font-medium text-white text-xs transition-all duration-200',
              'hover:shadow-lg hover:scale-105 active:scale-95',
              categoryColors[category].tag
            ]"
          >
            {{ skill }}
          </button>
        </div>
      </div>

      <!-- Statistiques compactes -->
      <div v-if="Object.keys(categorizedSkills).length > 0" class="lg:col-span-3 mt-2 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between flex-wrap gap-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">📊</span>
            <div>
              <p class="text-xs text-gray-600">Total</p>
              <p class="text-xl font-bold text-gray-800">{{ skills.length }}</p>
            </div>
          </div>
          <div class="flex gap-3 flex-wrap">
            <div v-for="(categorySkills, category) in categorizedSkills" :key="category" class="text-center text-xs">
              <p class="text-gray-600">{{ category }}</p>
              <p :class="['font-bold', categoryColors[category].text]">{{ categorySkills.length }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>
