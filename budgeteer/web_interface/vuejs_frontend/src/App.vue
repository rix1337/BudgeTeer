<script setup>
import "@/assets/scss/app.scss"
import {useDark, useToggle} from "@vueuse/core"
import {useStore} from 'vuex'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const store = useStore()
</script>

<template>
  <router-view/>

  <div class="sticky-bottom float-end">
    <button v-if="store.state.locked"
            class="btn btn-outline-success"
            type="button"
            @click="store.commit('setLocked', false)"><i class="bi bi-unlock"/>
    </button>
    <button v-else
            class="btn btn-outline-danger"
            type="button"
            @click="store.commit('setLocked', true)"><i class="bi bi-lock"/>
    </button>

    <button type="button" class="btn btn-outline-secondary bg-dark m-3 text-warning" @click="toggleDark()">
      <i v-if="isDark" class="bi bi-sun"/>
      <i v-else class="bi bi-moon-stars"/>
    </button>
  </div>
</template>
