import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'primeicons/primeicons.css'


// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const app = createApp(App)
const pinia = createPinia()
const vuetify = createVuetify({
    components,
    directives,
  })



app.use(vuetify)
app.use(pinia)
app.use(router)
// Make BootstrapVue available throughout your project

app.mount('#app')
