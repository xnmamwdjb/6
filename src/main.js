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
// import store from './store'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
