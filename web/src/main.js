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
Axios.defaults.baseURL='https://www.fastmock.site/mock/b07d1d1630880597e9844bfed33c61fc/SEP'
// Vue.prototype.$http = axios



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
