<script setup>
import {defineEmits, defineProps, ref} from 'vue';

const props = defineProps({
  title: String,
  modelValue: String // Using modelValue instead of date
});

const emits = defineEmits(['update:modelValue'])

// Create a ref to store the local copy of the date
const localDate = ref(props.modelValue)

function updateDate(index) {
  if (localDate.value === null) {
    // set to today
    localDate.value = new Date().toLocaleDateString('en-CA', {year: 'numeric', month: '2-digit'})
  }

  const date = new Date(localDate.value)
  date.setMonth(date.getMonth() + index)
  date.setDate(1) // Set day to 1 to avoid out-of-range issues
  const outputDate = date.toLocaleDateString('en-CA', {year: 'numeric', month: '2-digit'}) // en-CA yields YYYY-MM
  localDate.value = outputDate

  emits('update:modelValue', outputDate)
}

function clearDate() {
  localDate.value = null
  emits('update:modelValue', null)
}
</script>

<template>

  <div class="col-md-auto p-1">
    <button class="btn btn-outline-primary"
            type="button"
            @click="updateDate(-1)">
      <i class="bi bi-arrow-left"/>
    </button>
    <!-- Show modelValue if its not null else show infinity symbol-->

    {{ props.title }} <span v-if="modelValue !== null">{{ modelValue }} </span>
    <span v-else>&#8734; </span>
    <button class="btn btn-outline-primary"
            type="button"
            @click="updateDate(1)">
      <i class="bi bi-arrow-right"/>
    </button>
    <button class="btn btn-outline-secondary"
            @click="clearDate">
      &#8734;
    </button>
  </div>
</template>