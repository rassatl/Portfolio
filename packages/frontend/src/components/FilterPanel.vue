<script setup>
import SkillTag from './SkillTag.vue'

const props = defineProps({
  searchQuery: {
    type: String,
    required: true
  },
  selectedSkills: {
    type: Array,
    required: true
  },
  selectedYears: {
    type: Array,
    required: true
  },
  sortOrder: {
    type: String,
    required: true
  },
  filtersExpanded: {
    type: Boolean,
    required: true
  },
  allSkills: {
    type: Array,
    required: true
  },
  availableYears: {
    type: Array,
    required: true
  },
  filteredCount: {
    type: Number,
    required: true
  },
  totalCount: {
    type: Number,
    required: true
  },
  activeFiltersCount: {
    type: Number,
    default: 0
  },
  hasActiveFilters: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:searchQuery',
  'update:sortOrder',
  'update:filtersExpanded',
  'toggleSkill',
  'toggleYear',
  'resetFilters'
])
</script>

<template>
  <div class="bg-white rounded-xl shadow-md mb-8 border-2 border-green-300 overflow-hidden">
    <!-- Header cliquable -->
    <button
      @click="emit('update:filtersExpanded', !filtersExpanded)"
      class="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
    >
      <div class="flex items-center gap-3">
        <span class="text-2xl">🎯</span>
        <h3 class="text-xl font-bold text-gray-800">Filtres et recherche</h3>
        <span 
          v-if="activeFiltersCount > 0" 
          class="px-2 py-1 bg-green-600 text-white text-xs rounded-full font-semibold"
        >
          {{ activeFiltersCount }}
        </span>
      </div>
      <svg
        :class="['w-6 h-6 text-gray-600 transform transition-transform duration-300', filtersExpanded ? 'rotate-180' : '']"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Contenu des filtres avec transition -->
    <transition
      enter-active-class="transition-all duration-300 ease-out"
      leave-active-class="transition-all duration-300 ease-in"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-screen"
      leave-from-class="opacity-100 max-h-screen"
      leave-to-class="opacity-0 max-h-0"
    >
      <div v-show="filtersExpanded" class="px-6 pb-6">
        <!-- Barre de recherche -->
        <div class="mb-6 pt-2">
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            🔍 Rechercher un projet
          </label>
          <input
            :value="searchQuery"
            @input="emit('update:searchQuery', $event.target.value)"
            type="text"
            placeholder="Titre ou description..."
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none transition-colors"
          />
        </div>

        <!-- Filtres par compétences -->
        <div class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            🏷️ Filtrer par compétences
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="skill in allSkills"
              :key="skill"
              @click="emit('toggleSkill', skill)"
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
                selectedSkills.includes(skill)
                  ? 'bg-green-600 text-white shadow-md scale-105'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              {{ skill }}
              <span v-if="selectedSkills.includes(skill)" class="ml-1">✓</span>
            </button>
          </div>
        </div>

        <!-- Filtres par année -->
        <div v-if="availableYears.length > 0" class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            📅 Filtrer par année
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="year in availableYears"
              :key="year"
              @click="emit('toggleYear', year)"
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
                selectedYears.includes(year)
                  ? 'bg-blue-600 text-white shadow-md scale-105'
                  : 'bg-gray-100 text-gray-700 hover:bg-blue-100 hover:text-blue-700'
              ]"
            >
              {{ year }}
              <span v-if="selectedYears.includes(year)" class="ml-1">✓</span>
            </button>
          </div>
        </div>

        <!-- Tri par date -->
        <div class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            ⏰ Trier par date
          </label>
          <div class="flex gap-2">
            <button
              @click="emit('update:sortOrder', 'desc')"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2',
                sortOrder === 'desc'
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              <span>📉</span>
              <span>Plus récent d'abord</span>
            </button>
            <button
              @click="emit('update:sortOrder', 'asc')"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2',
                sortOrder === 'asc'
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              <span>📈</span>
              <span>Plus ancien d'abord</span>
            </button>
          </div>
        </div>

        <!-- Bouton de réinitialisation et compteur -->
        <div class="flex items-center justify-between pt-4 border-t-2 border-gray-200">
          <div class="text-sm text-gray-600">
            <span class="font-semibold text-lg">{{ filteredCount }}</span>
            projet{{ filteredCount > 1 ? 's' : '' }} trouvé{{ filteredCount > 1 ? 's' : '' }}
            <span v-if="activeFiltersCount > 0" class="text-green-700">
              ({{ totalCount }} au total)
            </span>
          </div>
          <button
            v-if="hasActiveFilters"
            @click="emit('resetFilters')"
            class="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-colors shadow-md"
          >
            🔄 Réinitialiser tous les filtres
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>
