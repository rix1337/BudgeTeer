<script setup>
import "@/assets/scss/app.scss"
import {useDark, useToggle} from "@vueuse/core"
import {useStore} from 'vuex'
import {useToast} from 'vue-toastification'
import axios from "axios"
import {onMounted, ref} from "vue"

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
  store.commit('setModifiedWhileLocked', false)
}

onMounted(() => {
  getVersion()
  setInterval(getVersion, 300 * 1000)
})

function openReleaseNotes() {
  window.open("https://github.com/rix1337/BudgeTeer/releases/latest", "_blank")
}

const version = ref("")
const update = ref(false)

function getVersion() {
  axios.get('api/version/')
      .then(function (res) {
        version.value = res.data.version.ver
        console.info("%c BudgeTeer %c ".concat(version.value, " "), "color: white; background: #303030; font-weight: 700; font-size: 24px; font-family: Monospace;", "color: #303030; background: white; font-weight: 700; font-size: 24px; font-family: Monospace;");
        console.info("%c ❤ Projekt unterstützen %c ".concat("https://github.com/sponsors/rix1337 ❤", " "), "color: white; background: #dc3545; font-weight: 700;", "color: #dc3545; background: white; font-weight: 700;")
        update.value = res.data.version.update_ready
        store.commit('setDocker', res.data.version.docker)
        if (update.value) {
          scrollingTitle("BudgeTeer - Update verfügbar! - ")
          console.log('Update steht bereit! Weitere Informationen unter https://github.com/rix1337/BudgeTeer/releases/latest')
          toast.info("Update steht bereit! Weitere Informationen unter:\nhttps://github.com/rix1337/BudgeTeer/releases/latest", {
            timeout: 15000,
            onClick: openReleaseNotes,
          })
        }
      }, function () {
        console.log('Konnte Version nicht abrufen!')
        toast.error('Konnte Version nicht abrufen!')
      })
}

function scrollingTitle(titleText) {
  document.title = titleText
  setTimeout(function () {
    scrollingTitle(titleText.substr(1) + titleText.substr(0, 1))
  }, 200)
}
</script>

<template>
  <router-view/>

  <div id="footer">
    <div class="container text-center">
      <p class="text-bg-dark credit">BudgeTeer {{ version }} by <a href="https://github.com/rix1337/BudgeTeer/"
                                                                   target="_blank"
                                                                   rel="noopener noreferrer">RiX</a></p>
    </div>
  </div>

  <div class="sticky-bottom float-end">
    <div class="col-md-auto p-1">
      <button v-if="store.state.modified_while_locked"
              class="btn btn-outline-warning bg-dark m-1"
              type="button"
              @click="saveOnLock()"><i class="bi bi-save"/>
      </button>
      <button v-else-if="store.state.locked"
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
              class="btn btn-outline-primary bg-dark m-1"
              data-bs-target="#offcanvasBottomSettings"
              data-bs-toggle="offcanvas"
              type="button"
              @click='store.commit("getSettings")'><i class="bi bi-gear"/>
      </button>
    </div>
  </div>
</template>
