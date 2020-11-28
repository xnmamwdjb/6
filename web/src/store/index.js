import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userInfo:JSON.parse(localStorage.getItem("userInfo")),
    token:JSON.parse(localStorage.getItem("token"))
  },
  mutations: {
    setuserInfo(state,v) {
      localStorage.setItem('userInfo',JSON.stringify(v));
      state.userInfo = v;
    },
    setToken(state,v) {
      localStorage.setItem('token',JSON.stringify(v));
      state.token = v;
    }
  },
  actions: {
  },
  modules: {
  }
})
