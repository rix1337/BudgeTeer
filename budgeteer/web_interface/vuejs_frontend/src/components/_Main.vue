<script setup>
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap-icons/font/bootstrap-icons.css'
import "bootstrap"

import Head from './Head.vue'
import Settings from './Settings.vue'
import Transactions from "./Transactions.vue"
import Budgets from "./Budgets.vue"
</script>

<template>
  <main>
    <!--- Main Items -->
    <Head/>
    <Transactions/>
    <Budgets/>
    <!-- Offcanvas Items -->
    <Settings/>
  </main>
</template>
