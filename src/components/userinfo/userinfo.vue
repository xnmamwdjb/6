<template>
    <div id="app">
    <!-- 路由占位符 -->
    <div class="banner">
        <!-- <el-page-header @back="goBack" content="详情页面"></el-page-header> -->
    </div>
    <div class="maincontainer">
        <div class="asidenav">
            <el-menu
            :default-active='$route.path'
            class="el-menu-vertical-demo"
            background-color="rgb(250, 250, 250)"
            active-text-color="#fff"
            :unique-opened="true"
            router>
                <el-menu-item index="/info">
                    <i class="el-icon-gerenzhongxin"></i>
                    <span slot="title">我的信息</span>
                </el-menu-item>
                <el-menu-item index="/wallet">
                    <i class="el-icon-qianbao"></i>
                    <span slot="title">我的钱包</span>
                </el-menu-item>
                <el-menu-item index="/order">
                    <i class="el-icon-gouwuche"></i>
                    <span slot="title">我的订单</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="main"><router-view></router-view></div>
    </div>
    <div class="footer"></div>
    </div>
</template>

<script>

export default {
    methods: {
        goBack() {
            this.$router.push('/Homepage')
        }
    }
}
</script>

<style >
.banner {
    height: 160px;
    background-image: url("../../assets/pic/userinfo/banner.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    margin-bottom: 10px;
}

.maincontainer {
    width: 900px;
    height: 800px;
    margin: 0 auto;
    border: 2px solid rgb(221, 221, 221);
    /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); */
    box-shadow: 20px 20px rgba(0, 0, 0, 0.1);
    /* border-radius: 50px; */
    display: flex;
}
.asidenav {
    flex: 1;
    background-color: rgb(250, 250, 250);
}
.main {
    flex:4;
    background-color: rgb(255, 255, 255);
    background-image: url("../../assets/pic/userinfo/longBook.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    padding-top: 20px;
    padding-left: 10px;
    padding-right: 10px;
}
.asidenav .el-menu-item.is-active {
    background-color: #642716 !important
}
.asidenav .el-menu-item:hover{
    background-color: #e6b76d !important
}
.footer {
    width: 100%;
    height: 100px;
    background-color: #fff;
    margin-top: 20px;
}
</style>