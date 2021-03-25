import Vue from 'vue'
import App from './App.vue'
import GAuth from 'vue-google-oauth2'
import { CLIENT_ID } from './client_config'

const gauthOption = {
  clientId: CLIENT_ID,
  scope: 'email',
  prompt: 'consent',
  fetch_basic_profile: false
}

Vue.use(GAuth, gauthOption)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

