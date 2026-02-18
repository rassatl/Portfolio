<script setup>
defineProps({
  skill: {
    type: String,
    required: true
  },
  variant: {
    type: String,
    default: 'default', // 'default', 'selected', 'clickable'
    validator: (value) => ['default', 'selected', 'clickable'].includes(value)
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg'
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

defineEmits(['click'])

const sizeClasses = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-3 py-1 text-xs',
  lg: 'px-4 py-2 text-sm'
}

const variantClasses = {
  default: 'bg-green-100 text-green-700',
  selected: 'bg-green-600 text-white shadow-md scale-105',
  clickable: 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700 cursor-pointer'
}
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1 rounded-full font-medium transition-all duration-200',
      sizeClasses[size],
      variantClasses[variant]
    ]"
    @click="$emit('click')"
  >
    {{ skill }}
    <span v-if="variant === 'selected'" class="text-xs">✓</span>
  </span>
</template>
