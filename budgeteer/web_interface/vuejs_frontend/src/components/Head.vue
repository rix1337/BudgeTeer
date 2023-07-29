<script setup>
import {useStore} from 'vuex'
import {computed, onMounted, ref} from 'vue'
import {useToast} from 'vue-toastification'
import axios from 'axios'

const store = useStore()
const toast = useToast()

store.commit('getBalances')

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

const current_budget = computed({
  // getter
  get() {
    let transactions_total_amount = 0
    for (let i = 0; i < store.state.data.open_transactions.length; i++) {
      let amount = parseFloat(store.state.data.open_transactions[i].amount)
      if (!isNaN(amount)) {
        transactions_total_amount += amount
      }
    }

    let balances_total_amount = 0
    for (let i = 0; i < store.state.data.balances.length; i++) {
      let amount = parseFloat(store.state.data.balances[i].balance)
      if (!isNaN(amount) && store.state.data.balances[i].type === "checking") {
        balances_total_amount += amount
      }
    }

    let current_budget_total_amount = 0
    for (let i = 0; i < store.state.data.budgets.length; i++) {
      for (let j = 0; j < store.state.data.budgets[i].entries.length; j++) {
        let amount = parseFloat(store.state.data.budgets[i].entries[j].amount)
        // TODO: check if valid_from_to is in current month
        if (!isNaN(amount) && !store.state.data.budgets[i].entries[j].booked) {
          current_budget_total_amount += amount
        }
      }
    }

    return (balances_total_amount + transactions_total_amount + current_budget_total_amount).toFixed(2)
  }
})

const current_month = ref(
    new Date().toLocaleString('default', {month: 'long'})
)
</script>


<template>
  <div class="container">
    <div class="row my-3">
      <div class="col-md-10 offset-md-1">
        <div class="card text-center shadow my-3">
          <div class="card-header">
            <h1>
              <i class="bi bi-cash-coin"/> BudgeTeer
            </h1>
            <p>Projekt von
              <a href="https://github.com/rix1337/BudgeTeer/releases/latest" target="_blank">RiX</a> {{ version }}
              <span v-if="update"> (Update verfügbar!)</span>
            </p>
          </div>
          <div class="card-body">
            <div class="row justify-content-center mt-2">
              <h2>Restbudget {{ current_month }}: {{ current_budget }} €</h2>
              <div class="row justify-content-center mt-2">
                <div v-for="(item, index) in store.state.data.balances" :key="item" class="balance">
                  <div class="input-group">
                    <div class="input-group-prepend">
                      <input :disabled="store.state.locked"
                             v-model="store.state.data.balances[index].label"
                             class="form-control">
                    </div>
                    <input :disabled="store.state.locked"
                           v-model="store.state.data.balances[index].balance"
                           type="number"
                           step="0.01"
                           class="form-control">
                    <div class="input-group-append">
                      <span class="input-group-text"> €</span>
                    </div>
                    <div v-if="!store.state.locked"
                         class="input-group-append">
                      <select :disabled="store.state.locked"
                              v-model="store.state.data.balances[index].type"
                              class="form-control">
                        <option value="checking">Girokonto</option>
                        <option value="savings">Sparkonto</option>
                      </select>
                    </div>
                    <div v-if="!store.state.locked"
                         class="input-group-append">
                      <button
                          class="btn btn-outline-primary"
                          type="button"
                          @click="store.state.data.balances.splice(index - 1, 0, store.state.data.balances.splice(index, 1)[0])"
                      >
                        <i class="bi bi-arrow-up"/>
                      </button>
                      <button
                          class="btn btn-outline-primary"
                          type="button"
                          @click="store.state.data.balances.splice(index + 1, 0, store.state.data.balances.splice(index, 1)[0])"
                      >
                        <i class="bi bi-arrow-down"/>
                      </button>
                      <button
                          class="btn btn-outline-danger"
                          type="button"
                          @click="store.state.data.balances.splice(index, 1)"
                      >
                        <i class="bi bi-trash3"/>
                      </button>
                    </div>
                  </div>
                </div>
                <div v-if="!store.state.locked" class="row justify-content-center mt-2">
                  <button
                      class="btn btn-outline-primary"
                      type="button"
                      @click="store.state.data.balances.push({label:'',amount:''})"
                  >
                    Konto hinzufügen
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
