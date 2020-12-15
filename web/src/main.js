import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
import './assets/CSS/global.css'
import qs from 'qs'
Vue.prototype.$qs = qs;
Vue.config.productionTip = false
import './assets/icon/iconfont.css'
import Axios from 'axios'
// import store from './store'
Axios.defaults.baseURL='http://127.0.0.1:8899'
// Vue.prototype.$http = axios



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
