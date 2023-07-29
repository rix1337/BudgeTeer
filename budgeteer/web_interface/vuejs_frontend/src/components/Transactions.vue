<script setup>
import {useStore} from 'vuex'
import {useToast} from 'vue-toastification'
import axios from 'axios'

const store = useStore()
const toast = useToast()

store.commit('getOpenTransactions')

function saveOpenTransactions(name) {
  axios.post('api/json/' + name + '/', store.state.data.open_transactions)
      .then(function () {
        console.log(name + ' gespeichert.')
      }, function () {
        store.commit("getSettings")
        console.log('Konnte ' + name + ' nicht speichern!')
        toast.error('Konnte ' + name + ' nicht speichern!')
      })
}
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
                    <input v-model="store.state.data.open_transactions[index].label"
                           class="form-control">
                  </div>
                  <input v-model="store.state.data.open_transactions[index].amount"
                         type="number"
                         step="0.01"
                         class="form-control">
                  <div class="input-group-append">
                    <span class="input-group-text"> €</span>
                  </div>
                  <div class="input-group-append">
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
                    <button
                        class="btn btn-outline-danger"
                        type="button"
                        @click="store.state.data.open_transactions.splice(index, 1)"
                    >
                      <i class="bi bi-trash3"/>
                    </button>
                  </div>
                </div>
              </div>
              <div class="row justify-content-center mt-2">
                <button
                    class="btn btn-outline-primary"
                    type="button"
                    @click="store.state.data.open_transactions.push({label:'',amount:''})"
                >
                  Transaktion hinzufügen
                </button>
                <button
                    class="btn btn-outline-success"
                    type="button"
                    @click="saveOpenTransactions('open_transactions')">
                  Speichern
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>