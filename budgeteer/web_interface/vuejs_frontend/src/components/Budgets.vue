<script setup>
import {useStore} from 'vuex'
import {ref} from 'vue'
import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'

const store = useStore()


store.commit('getBudgets')


function prettifyAmount(amount) {
  return parseFloat(amount).toFixed(2)
}

function calculateCategoryTotal(i) {
  let total = 0
  for (let j = 0; j < store.state.data.budgets[i].entries.length; j++) {
    if (showEntry(store.state.data.budgets[i].entries[j])) {
      let amount = parseFloat(store.state.data.budgets[i].entries[j].amount)
      if (!isNaN(amount)) {
        total += amount
      }
    }
  }
  return prettifyAmount(total)
}

function displayMonthIsCurrentMonth() {
  let check_display_month = new Date(display_month.value)
  let check_current_month = new Date()
  return check_display_month.getMonth() === check_current_month.getMonth() && check_display_month.getFullYear() === check_current_month.getFullYear()
}

const display_month = ref(new Date().toISOString().slice(0, 7))
const display_month_index = ref(0)

function updateDisplayMonth(index) {
  display_month_index.value += index
  let indexed_date = new Date().setMonth(new Date().getMonth() + display_month_index.value)
  display_month.value = new Date(indexed_date).toISOString().slice(0, 7)
}

function showEntry(entry) {
  if (store.state.locked && displayMonthIsCurrentMonth()) {
    return !entry.booked && checkEntryInDisplayMonth(entry)
  } else {
    return checkEntryInDisplayMonth(entry)
  }
}

function checkEntryInDisplayMonth(entry) {
  let current_month = new Date(display_month.value)
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
</script>

<template>
  <div class="container">
    <div class="row my-3">
      <div class="col-md-10 offset-md-1">
        <div class="card text-center shadow my-3">
          <div class="card-header">
            <h1>
              <i class="bi bi-currency-euro"/> Budgets {{ display_month }}
            </h1>
            <div class="col-md-auto p-1">
              <button :disabled="display_month_index <= 0"
                      class="btn btn-outline-primary"
                      type="button"
                      @click="updateDisplayMonth(-1)">
                <i class="bi bi-arrow-left"/>
              </button>
              <button :disabled="display_month_index >= 13"
                      class="btn btn-outline-primary"
                      type="button"
                      @click="updateDisplayMonth(1)">
                <i class="bi bi-arrow-right"/>
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="row justify-content-center mt-2">
              <div class="accordion" id="accordionBudgets">
                <div v-for="(budget, category_index) in store.state.data.budgets" :key="budget" class="accordion-item">
                  <h2 class="accordion-header" :id="'heading' + category_index">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            :data-bs-target="'#collapse' + category_index" aria-expanded="false"
                            :aria-controls="'collapse' + category_index">
                      {{ store.state.data.budgets[category_index].category }}: {{
                        calculateCategoryTotal(category_index)
                      }} €
                    </button>
                  </h2>
                  <div :id="'collapse' + category_index" class="accordion-collapse collapse"
                       :aria-labelledby="'heading' + category_index"
                       data-bs-parent="#accordionBudgets">
                    <div class="accordion-body">
                      <div v-for="(item, entry_index) in store.state.data.budgets[category_index].entries" :key="item">
                        <div
                            v-if="showEntry(store.state.data.budgets[category_index].entries[entry_index])"
                            class="input-group">
                          <div class="input-group-prepend">
                            <input :disabled="store.state.locked"
                                   v-model="store.state.data.budgets[category_index].entries[entry_index].label"
                                   class="form-control">
                          </div>
                          <input :disabled="store.state.locked"
                                 v-model="store.state.data.budgets[category_index].entries[entry_index].amount"
                                 type="number"
                                 step="0.01"
                                 class="form-control">
                          <div class="input-group-append">
                            <span class="input-group-text"> €</span>
                          </div>
                          <div v-if="!store.state.locked" class="input-group-append">
                            <button
                                v-if="displayMonthIsCurrentMonth() && store.state.data.budgets[category_index].entries[entry_index].booked"
                                class="btn btn-outline-danger"
                                type="button"
                                @click="store.state.data.budgets[category_index].entries[entry_index].booked = false">
                              <i class="bi bi-x"/>
                            </button>
                            <button
                                class="btn btn-outline-primary"
                                type="button"
                                @click="store.state.data.budgets[category_index].entries.splice(entry_index - 1, 0, store.state.data.budgets[category_index].entries.splice(entry_index, 1)[category_index])"
                            >
                              <i class="bi bi-arrow-up"/>
                            </button>
                            <button
                                class="btn btn-outline-primary"
                                type="button"
                                @click="store.state.data.budgets[category_index].entries.splice(entry_index + 1, 0, store.state.data.budgets[category_index].entries.splice(entry_index, 1)[category_index])"
                            >
                              <i class="bi bi-arrow-down"/>
                            </button>
                            <button
                                class="btn btn-outline-danger"
                                type="button"
                                @click="store.state.data.budgets[category_index].entries.splice(entry_index, 1)"
                            >
                              <i class="bi bi-trash3"/>
                            </button>
                          </div>
                          <div class="input-group-append">
                            <button
                                v-if="displayMonthIsCurrentMonth() && store.state.locked && !store.state.data.budgets[category_index].entries[entry_index].booked"
                                class="btn btn-outline-success"
                                type="button"
                                @click="store.state.data.budgets[category_index].entries[entry_index].booked = true">
                              <i class="bi bi-check2"/>
                            </button>
                          </div>
                        </div>
                        <div v-if="!store.state.locked">
                          Aktiv: {{ store.state.data.budgets[category_index].entries[entry_index].valid_from_to }}
                          <!-- ToDo date-picker broken. It currently cant work with Input YYYY-MM Dates-->
                          <date-picker
                              v-model:value="store.state.data.budgets[category_index].entries[entry_index].valid_from_to"
                              type="month"
                              format="MMMM YYYY"
                              range="true"/>
                        </div>
                      </div>
                      <button v-if="!store.state.locked"
                              class="btn btn-outline-primary"
                              type="button"
                              @click="store.state.data.budgets[category_index].entries.push({label:'',amount:'', valid_from_to: [null, null], booked: false})"
                      > Eintrag hinzufügen
                      </button>
                    </div>
                  </div>

                </div>
              </div>
              <div class="row justify-content-center mt-2">
                <button v-if="!store.state.locked"
                        class="btn btn-outline-primary"
                        type="button"
                        @click="store.state.data.budgets.push({category:'ToDo',amount:'', entries: []})"
                >
                  Kategorie hinzufügen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>