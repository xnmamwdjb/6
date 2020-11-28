<template>
    <div id="app" >

    <el-container>
        <el-header>
            
            <el-menu
            :default-active='$route.path'
            
            class="el-menu-demo nav"
            mode="horizontal"
            @select="handleSelect"
            background-color="#333"
            text-color="#fff"
            active-text-color="rgb(230, 162, 60)"
            router>

            <!-- <img class="logo" src="../assets/pic/login/avatar.jpg" alt=""> -->
            <el-menu-item index="/searchquiz"><i class="el-icon-ziyuan"></i>首页</el-menu-item>
            <el-menu-item index="/searchteacher"><i class="el-icon-sousuo"></i>找老师</el-menu-item>
            <el-menu-item index="/aboutus" ><i class="el-icon-guanzhu"></i>关于我们</el-menu-item>


            <el-dropdown class="bt" v-if="isshow">
                <el-avatar 
                :src="srcurl" 
                :fit="fit" 
                @error="errorHandler"
                alt="fail"></el-avatar>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="turnToLogin" icon="el-icon-zhanghao">登录</el-dropdown-item>
                    <!-- <el-dropdown-item command="msgbox" icon="el-icon-plus">我的收件箱</el-dropdown-item> -->
                    <el-dropdown-item @click.native="turnToReg" icon="el-icon-bianji">注册</el-dropdown-item>
                    
                </el-dropdown-menu>
            </el-dropdown>
            
            <el-dropdown class="bt" v-if="!isshow">
            <span class="el-dropdown-link">
                <i class="el-icon-message"></i>
                消息<i class="el-icon-caret-bottom el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="reply" class="clearfix">
                    <i class="el-icon-pinglun"></i>
                    回复我的
                    <el-badge class="mark" :value="12" />
                </el-dropdown-item>
                <el-dropdown-item @click.native="sysmsg" class="clearfix">
                    <i class="el-icon-xiaoxi"></i>
                    系统消息
                    <el-badge class="mark" :value="3" />
                </el-dropdown-item>
            </el-dropdown-menu>
            </el-dropdown>
            
            <el-dropdown class="bt" v-if="!isshow">
                <el-avatar 
                :src="srcurl" 
                :fit="fit" 
                @error="errorHandler"
                alt="fail"></el-avatar>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="info" icon="el-icon-gerenzhongxin">个人中心</el-dropdown-item>
                    <!-- <el-dropdown-item command="msgbox" icon="el-icon-plus">我的收件箱</el-dropdown-item> -->
                    <el-dropdown-item @click.native="wallet" icon="el-icon-qianbao">我的钱包</el-dropdown-item>
                    <el-dropdown-item @click.native="order" icon="el-icon-gouwuche">我的订单</el-dropdown-item>
                    <el-dropdown-item @click.native="logout" icon="el-icon-tuichu">登出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>

            

            </el-menu>
        </el-header>

    <el-main >
        <router-view></router-view>
    </el-main>
    </el-container>       
        
        

    </div>
</template>

<script>
import axios from 'axios'
export default {
    inject:['reload'],
    data() {
        return {
            iconSize:{
                width:'20px',
                height:'20px'
            },
            // activeIndex: this.index,
            isshow:true,
            fit: 'fill',
            srcurl: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        };
    },
    mounted() {
        this.changeisshow();
    },
    methods: {
        // judgetoken(){
            // 
        // },
        info(){
            const routeinfo = this.$router.resolve({
                    // name:"/info",
                    path:"/info",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routeinfo.href, '_blank');
        },
        wallet(){
            const routewallet = this.$router.resolve({
                    // name:"/info",
                    path:"/wallet",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routewallet.href, '_blank');
        },
        order(){
            const routeorder = this.$router.resolve({
                    // name:"/info",
                    path:"/order",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routeorder.href, '_blank');
        },
        reply(){
            const routereply = this.$router.resolve({
                    // name:"/info",
                    path:"/reply",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routereply.href, '_blank');
        },
        sysmsg(){
            const routesysmsg = this.$router.resolve({
                    // name:"/info",
                    path:"/sysmsg",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routesysmsg.href, '_blank');
        },
        errorHandler() {
        return true
        },
        changeisshow() {
            // const tokenstr=window.sessionStorage.getItem('token');
            const vuexUser=this.$store.state.userInfo;
            const vuexToken=this.$store.state.token;
            // const userstr=window.sessionStorage.getItem('currentUser');
            // const tokenstr="testtoken"
            if(vuexToken){
                this.isshow=false;
                // console.log(tokenstr);
                console.log(vuexUser);
                console.log(vuexToken);
                // console.log(userstr);
            }
            else{
                this.isshow=true;
                // console.log(tokenstr);
                console.log(vuexUser);
                console.log(vuexToken);
                // console.log(userstr);
            }
        },
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
            console.log(key);
        },
        turnToLogin(){
            this.$router.push('/login')
        },
        turnToReg(){
            this.$router.push('/register')
        },
        logout(){
            window.sessionStorage.clear();
            this.$store.commit('setuserInfo','');
            this.$store.commit('setToken','');
            this.reload()
            // this.changeisshow();
            // this.$router.push('/homepage')
        }
    }

}
</script>

<style lang="less" scoped>


.nav {
    // position: fixed;
    // top: 0px;
    width: 100%;
    box-shadow: 0 0 20px;
    height: 60px;
}


.bt {
    float: right;
    margin-right: 20px;
    // line-height: 60px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    border-radius: 30px;

}

.el-header, .el-main {
    padding: 0px;
}
.el-dropdown-link {
    cursor: pointer;
    color: #FFF;
    line-height: 60px;
}
.el-icon-arrow-down {
    font-size: 12px;
}
.el-avatar {
    margin-top: 11px;
}
</style>