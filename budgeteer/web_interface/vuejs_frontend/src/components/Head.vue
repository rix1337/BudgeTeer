<script setup>
import {useStore} from 'vuex'
import {computed, ref} from 'vue'

const store = useStore()

store.commit('getBalances')

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
        if (!isNaN(amount) && checkEntryInDisplayMonthAndNotBooked(store.state.data.budgets[i].entries[j])) {
          current_budget_total_amount += amount
        }
      }
    }

    return (balances_total_amount + transactions_total_amount + current_budget_total_amount).toFixed(2)
  }
})

function checkEntryInDisplayMonthAndNotBooked(entry) {
  if (!entry.booked) {
    let current_month = new Date()
    let valid_from = new Date("1970-01-01")
    let valid_to = new Date("2100-01-01")

    if (entry.valid_from_to[0] !== null) {
      valid_from = new Date(entry.valid_from_to[0])
    }
    if (entry.valid_from_to[1] !== null) {
      valid_to = new Date(entry.valid_from_to[1])
    }

    return current_month >= valid_from && current_month <= valid_to
  }
  return false
}

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
            <h1><i class="bi-cash-coin"/> Verfügbar im {{ current_month }}: {{ current_budget }} €</h1>
          </div>
          <div class="card-body">
            <div class="row justify-content-center mt-2">
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
