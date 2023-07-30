<script setup>
import {useStore} from 'vuex'

const store = useStore()

store.commit('getOpenTransactions')
</script>


<template>
  <div class="container">
    <div class="row my-3">
      <div class="col-md-10 offset-md-1">
        <div class="card text-center shadow my-3">
          <div class="card-header">
            <h1>
              <i class="bi bi-clock-history"/> Offene Transaktionen
            </h1>
          </div>
          <div class="card-body">
            <div class="row justify-content-center mt-2">
              <div v-for="(item, index) in store.state.data.open_transactions" :key="item" class="transaction">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <input :disabled="store.state.locked"
                           v-model="store.state.data.open_transactions[index].label"
                           class="form-control">
                  </div>
                  <input :disabled="store.state.locked"
                         v-model="store.state.data.open_transactions[index].amount"
                         type="number"
                         step="0.01"
                         class="form-control">
                  <div class="input-group-append">
                    <span class="input-group-text"> €</span>
                  </div>
                  <div v-if="!store.state.locked" class="input-group-append">
                    <button
                        class="btn btn-outline-primary"
                        type="button"
                        @click="store.state.data.open_transactions.splice(index - 1, 0, store.state.data.open_transactions.splice(index, 1)[0])"
                    >
                      <i class="bi bi-arrow-up"/>
                    </button>
                    <button
                        class="btn btn-outline-primary"
                        type="button"
                        @click="store.state.data.open_transactions.splice(index + 1, 0, store.state.data.open_transactions.splice(index, 1)[0])"
                    >
                      <i class="bi bi-arrow-down"/>
                    </button>
                  </div>
                  <div class="input-group-append">
                    <button
                        class="btn btn-outline-danger"
                        type="button"
                        @click="store.state.data.open_transactions.splice(index, 1) && store.commit('setModifiedWhileLocked', true)"
                    >
                      <i class="bi bi-trash3"/>
                    </button>
                  </div>
                </div>
              </div>
              <div class="row justify-content-center mt-2">
                <button v-if="!store.state.locked"
                    class="btn btn-outline-primary"
                    type="button"
                    @click="store.state.data.open_transactions.push({label:'',amount:''})"
                >
                  Transaktion hinzufügen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>