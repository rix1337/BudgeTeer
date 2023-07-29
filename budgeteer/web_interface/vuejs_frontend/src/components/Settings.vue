<script setup>
import {useStore} from 'vuex'
import {computed, ref} from 'vue'
import {useToast} from "vue-toastification"
import {submitForm} from '@formkit/vue'
import axios from 'axios'

const store = useStore()
const toast = useToast()

function saveSettings() {
  spin_settings.value = true
  axios.post('api/settings/', store.state.settings)
      .then(function () {
        console.log('Einstellungen gespeichert! Neustart des BudgeTeers wird dringend empfohlen!')
        toast.success('Einstellungen gespeichert! Neustart des BudgeTeers wird dringend empfohlen!')
        store.commit("getSettings")
        spin_settings.value = false
      }, function () {
        store.commit("getSettings")
        spin_settings.value = false
        console.log('Konnte Einstellungen nicht speichern! Bitte die angegebenen Werte auf Richtigkeit prüfen.')
        toast.error('Konnte Einstellungen nicht speichern! Bitte die angegebenen Werte auf Richtigkeit prüfen.')
      })
}

const spin_settings = ref(false)

const password_changed = computed(() => (store.state.settings.general.auth_hash.length > 0))

function submitSettings() {
  submitForm('settings')
}
</script>


<template>
  <div class="text-center">
    <div id="offcanvasBottomSettings" aria-labelledby="offcanvasBottomSettingsLabel" class="offcanvas offcanvas-bottom"
         tabindex="-1">
      <div class="offcanvas-header">
        <h3 id="offcanvasBottomSettingsLabel" class="offcanvas-title"><i class="bi bi-gear"/> Einstellungen</h3>
        <button aria-label="Close" class="btn-close text-reset" data-bs-dismiss="offcanvas" type="button"></button>
      </div>
      <div class="offcanvas-body">
        <h4 v-if="!store.state.misc.loaded_settings">Einstellungen werden geladen...</h4>
        <div v-if="store.state.misc.loaded_settings" id="accordionSettings" class="accordion">
          <FormKit id="settings" #default="{ value }"
                   :actions="false"
                   incomplete-message="Es müssen alle Felder korrekt ausgefüllt werden! Fehler sind rot markiert."
                   messages-class="text-danger mt-4"
                   type="form"
                   @submit="saveSettings()"
          >
            <div class="accordion-item">
              <h2 id="headingGeneral" class="accordion-header">
                <button aria-controls="collapseGeneral" aria-expanded="false" class="accordion-button collapsed"
                        data-bs-target="#collapseGeneral"
                        data-bs-toggle="collapse" type="button">
                  Allgemein
                </button>
              </h2>
              <div id="collapseGeneral" aria-labelledby="headingGeneral" class="accordion-collapse collapse"
                   data-bs-parent="#accordionSettings">
                <div class="accordion-body">
                  <div v-if="!store.state.misc.docker">
                    <FormKit v-model="store.state.settings.general.port"
                             help="Hier den Port des Webservers wählen."
                             help-class="text-muted"
                             input-class="form-control bg-light mb-2"
                             label="Port"
                             messages-class="text-danger"
                             outer-class="mb-4"
                             placeholder="Bspw. 9090"
                             type="number"
                             validation="required|between:1024,65535"
                             validation-visibility="live"/>
                  </div>
                  <FormKit v-model="store.state.settings.general.prefix"
                           help="Hier den Prefix des Webservers wählen (nützlich für Reverse-Proxies)."
                           help-class="text-muted"
                           input-class="form-control bg-light mb-2"
                           label="Prefix"
                           messages-class="text-danger"
                           outer-class="mb-4"
                           placeholder="Bspw. feedcrawler"
                           type="text"
                           validation="alpha"
                           validation-visibility="live"/>
                  <FormKit v-model="store.state.settings.general.auth_user"
                           :validation="value.auth_hash ? 'required' : ''"
                           help="Hier den Nutzernamen für BudgeTeer eingeben."
                           help-class="text-muted"
                           input-class="form-control bg-light mb-2"
                           label="Nutzername"
                           messages-class="text-danger"
                           name="auth_user"
                           outer-class="mb-4"
                           placeholder="Bspw. rix1337"
                           type="text"/>
                  <FormKit v-model="store.state.settings.general.auth_hash"
                           :validation="(password_changed && value.auth_user) ? 'required|length:6' : ''"
                           help="Hier das Passwort für BudgeTeer angeben."
                           help-class="text-muted"
                           input-class="form-control bg-light mb-2"
                           label="Passwort"
                           messages-class="text-danger"
                           name="auth_hash"
                           outer-class="mb-4"
                           placeholder="Bspw. ●●●●●●●●"
                           type="password"
                           validation-visibility="live"/>
                </div>
              </div>
            </div>
          </FormKit>
        </div>
        <div>
          <button v-if="store.state.misc.loaded_settings" class="btn btn-primary mt-4" type="submit"
                  @click="submitSettings">
            <span v-if="spin_settings" class="spinner-border spinner-border-sm" role="status"></span>
            <i v-if="!spin_settings" class="bi bi-save"/> Speichern
          </button>
          <button v-else class="btn btn-dark disabled">
            <span class="spinner-border spinner-border-sm" role="status"></span> Lädt...
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Center Selects */
select {
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
  text-align-last: center;
}
</style>
