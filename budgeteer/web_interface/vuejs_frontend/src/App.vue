<script setup>
import "@/assets/scss/app.scss"
import {useDark, useToggle} from "@vueuse/core"
import {useStore} from 'vuex'
import {useToast} from 'vue-toastification'
import axios from "axios";

const isDark = useDark()
const toggleDark = useToggle(isDark)

const store = useStore()
const toast = useToast()

function saveJSON(name) {
  axios.post('api/json/' + name + '/', store.state.data[name])
      .then(function () {
        console.log(name + ' gespeichert.')
      }, function () {
        console.log('Konnte ' + name + ' nicht speichern!')
        toast.error('Konnte ' + name + ' nicht speichern!')
      })
}

function saveOnLock() {
  saveJSON('balances')
  saveJSON('budgets')
  saveJSON('open_transactions')
  store.commit('setLocked', true)
}
</script>

<template>
  <router-view/>

  <div class="sticky-bottom float-end">
    <div class="col-md-auto p-1">
      <button v-if="store.state.locked"
              class="btn btn-outline-success bg-dark m-1"
              type="button"
              @click="store.commit('setLocked', false)"><i class="bi bi-unlock"/>
      </button>
      <button v-else
              class="btn btn-outline-danger bg-dark m-1"
              type="button"
              @click="saveOnLock()"><i class="bi bi-lock"/>
      </button>

      <button type="button" class="btn btn-outline-secondary bg-dark text-warning m-1"
              @click="toggleDark()">
        <i v-if="isDark" class="bi bi-sun"/>
        <i v-else class="bi bi-moon-stars"/>
      </button>

      <button aria-controls="offcanvasBottomSettings"
              class="btn btn-outline-primary bg-dark m-2"
              data-bs-target="#offcanvasBottomSettings"
              data-bs-toggle="offcanvas"
              type="button"
              @click='store.commit("getSettings")'><i class="bi bi-gear"/>
      </button>
    </div>
  </div>
</template>
