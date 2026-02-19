<script setup>
import { ref, computed } from 'vue'
import SkillTag from './SkillTag.vue'
import { formatDate } from '../composables/useFormatters'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['project-deleted'])

const showConfirmModal = ref(false)
const isDeleting = ref(false)
const userId = ref(localStorage.getItem('user_id'))

const canDelete = computed(() => {
  if (!userId.value || !props.project.user_id) return false
  return parseInt(userId.value) === props.project.user_id
})

async function deleteProject() {
  if (!canDelete.value) return
  
  isDeleting.value = true
  try {
    const response = await fetch(`http://127.0.0.1:8000/projects/${props.project.id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: parseInt(userId.value) })
    })
    
    if (response.ok) {
      showConfirmModal.value = false
      emit('project-deleted', props.project.id)
    } else {
      const error = await response.json()
      alert(`Erreur: ${error.detail || 'Impossible de supprimer le projet'}`)
    }
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression du projet')
  } finally {
    isDeleting.value = false
  }
}
</script>

<template>
  <div
    :class="[
      'bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 border-green-300 relative',
      compact ? 'max-w-sm' : ''
    ]"
  >
    <!-- Modal de confirmation -->
    <div v-if="showConfirmModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 rounded-lg">
      <div class="bg-white rounded-lg p-6 max-w-sm mx-4">
        <h3 class="text-xl font-bold text-gray-800 mb-2">Confirmer la suppression</h3>
        <p class="text-gray-600 mb-6">
          Êtes-vous sûr de vouloir supprimer le projet "<strong>{{ project.title }}</strong>" ?
          <br />
          <span class="text-sm text-red-600">Cette action est irréversible.</span>
        </p>
        <div class="flex gap-3 justify-end">
          <button
            @click="showConfirmModal = false"
            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
            :disabled="isDeleting"
          >
            Annuler
          </button>
          <button
            @click="deleteProject"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50"
            :disabled="isDeleting"
          >
            {{ isDeleting ? 'Suppression...' : 'Supprimer' }}
          </button>
        </div>
      </div>
    </div>

    <div class="flex justify-between items-start mb-3 gap-4">
      <h2 class="text-2xl font-bold text-gray-800 flex-1">{{ project.title }}</h2>
      <div class="ml-4 flex items-center gap-2 text-sm">
        <span
          :class="[
            'px-2 py-1 rounded-full font-semibold',
            project.type === 'professionnel' ? 'bg-purple-100 text-purple-800' : 'bg-teal-100 text-teal-800'
          ]"
        >
          {{ project.type === 'professionnel' ? 'Professionnel' : 'Personnel' }}
        </span>
      </div>
      <div class="flex items-center gap-2 whitespace-nowrap">
        <span class="text-sm text-gray-500 font-semibold">
          {{ formatDate(project.date) }}
        </span>
        <!-- Bouton supprimer si propriétaire -->
        <button
          v-if="canDelete"
          @click="showConfirmModal = true"
          class="px-2 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600 transition-colors"
          title="Supprimer ce projet"
        >
          🗑️
        </button>
      </div>
    </div>
    
    <p class="text-gray-600 mb-4 leading-relaxed">
      {{ project.description || 'Aucune description disponible' }}
    </p>
    
    <!-- Tags de compétences -->
    <div v-if="project.skills && project.skills.length > 0" class="mb-16">
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
    
    <!-- Liens en position absolue en bas à gauche -->
    <div class="absolute bottom-4 left-6 flex gap-3">
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
