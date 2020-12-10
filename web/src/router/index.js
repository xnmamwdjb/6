import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Homepage from '@/components/Homepage'
import Register from '@/components/Register'
import Login from '@/components/Login'
import searchquiz from '@/components/searchquiz/searchquiz'
import searchteacher from '@/components/searchteacher/searchteacher'
import aboutus from '@/components/aboutus/aboutus'
import userinfo from '@/components/userinfo/userinfo'
import info from '@/components/userinfo/info'
import wallet from '@/components/userinfo/wallet'
import order from '@/components/userinfo/order'
import identity from '@/components/userinfo/identity'
import teacherDetail from '@/components/teacherPair/teacherDetail'

Vue.use(VueRouter)

const routes = [
  {path:'/', redirect:'/Homepage'},
  {path:'/Login', component: Login },
  {path:'/Register', component: Register },
  {path:'/Homepage', 
  component: Homepage, 
  redirect:'/searchteacher',
  children:[
    {path:'/searchquiz', component: searchquiz},
    {path:'/searchteacher', component: searchteacher},
    {path:'/teacherDetail/:teacherId', component: teacherDetail, name: 'teacherDetail'},
    {path:'/aboutus', component: aboutus},
    
    {path:'/userinfo', 
    component: userinfo,
    redirect:'/info',
    children:[
      {path:'/info', component: info},
      {path:'/wallet', component: wallet},
      {path:'/order', component: order},
      {path:'/identity', component: identity },
    ]
    },

    
  
  ] 
  },
  
]

const router = new VueRouter({
  routes
})

export default router
