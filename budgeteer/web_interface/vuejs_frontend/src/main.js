import {createApp} from 'vue'
import {createStore} from 'vuex'
import axios from 'axios'
import router from './router'
import Toast, {TYPE, useToast} from "vue-toastification"
import "vue-toastification/dist/index.css"
import VueTippy from 'vue-tippy'
import 'tippy.js/dist/tippy.css'
import {defaultConfig, plugin} from '@formkit/vue'
import {de} from '@formkit/i18n'
import App from './App.vue'

const toast = useToast()

// The store is created here, and then passed to the Vue instance
// It contains the state of the application and is updated through calls to the BudgeTeer API
const store = createStore({
    state() {
        return {
            data: {
                balances: [],
                open_transactions: [],
                budgets: []
            },
            display_month: new Date().toISOString().slice(0, 7),
            locked: true,
            modified_while_locked: false,
            settings: {},
            misc: {
                loaded_settings: false,
                docker: false
            }
        }
    }, mutations: {
        setDisplayMonth(state, month) {
            state.display_month = month
        },
        getSettings(state) {
            axios.get('api/settings/')
                .then(function (res) {
                    state.settings = res.data.settings
                    state.misc.loaded_settings = true
                }, function () {
                    console.log('Konnte Einstellungen nicht abrufen!')
                    toast.error('Konnte Einstellungen nicht abrufen!')
                })
        }, getBalances(state) {
            axios.get('api/json/balances/')
                .then(function (res) {
                    state.data.balances = res.data.balances
                }, function () {
                    console.log('Konnte Kontostände nicht abrufen!')
                    toast.error('Konnte Kontostände nicht abrufen!')
                })
        }, getOpenTransactions(state) {
            axios.get('api/json/open_transactions/')
                .then(function (res) {
                    state.data.open_transactions = res.data.open_transactions
                }, function () {
                    console.log('Konnte offene Transaktionen nicht abrufen!')
                    toast.error('Konnte offene Transaktionen nicht abrufen!')
                })

        }, getBudgets(state) {
            axios.get('api/json/budgets/')
                .then(function (res) {
                    state.data.budgets = res.data.budgets
                }, function () {
                    console.log('Konnte Budgets nicht abrufen!')
                    toast.error('Konnte Budgets nicht abrufen!')
                })
        }, setDocker(state, docker) {
            state.misc.docker = docker
        }, setLocked(state, locked) {
            state.locked = locked
        }, setModifiedWhileLocked(state, modified) {
            if (modified) {
                document.title = "BudgeTeer (ungespeichert!)"
            } else {
                document.title = "BudgeTeer"
            }
            state.modified_while_locked = modified
        }
    }
})

const app = createApp(App)
app.use(store)
app.use(router)
app.use(Toast, {
    position: "top-center", draggable: false, maxToasts: 1, bodyClassName: ["toast-body"], toastDefaults: {
        [TYPE.ERROR]: {
            icon: 'bi bi-exclamation-triangle',
        }, [TYPE.WARNING]: {
            icon: 'bi bi-exclamation-circle',
        }, [TYPE.INFO]: {
            icon: 'bi bi-info-circle',
        }, [TYPE.SUCCESS]: {
            icon: 'bi bi-check-circle-fill', timeout: 3000,
        }
    }
})
app.use(VueTippy)

app.use(plugin, defaultConfig({
    // Define additional locales
    locales: {de}, // Define the active locale
    locale: 'de'
}))
app.mount('#app')
