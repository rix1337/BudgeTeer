<script setup>
import {useStore} from 'vuex'
import {useToast} from "vue-toastification"
import axios from 'axios'

const store = useStore()
const toast = useToast()

store.commit('getBalances')

function saveBalances(name) {
  axios.post('api/json/' + name + '/', store.state.data.balances)
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
              <i class="bi bi-bar-chart-line-fill"/> Kontostände
            </h1>
          </div>
          <div class="card-body">
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
                <button
                    class="btn btn-outline-success"
                    type="button"
                    @click="saveBalances('balances')">
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