<template>
    <div class="login_container">

        <!-- <el-carousel :interval="4000" type="card" height="350px"> -->
            <!-- <el-carousel-item v-for="item in 6" :key="item"> -->
                <!-- <img class="avImg" :src="imgSrc[item-1]"  alt="示例图片"> -->
            <!-- </el-carousel-item> -->
        <!-- </el-carousel> -->

        <div class="login_box">
            <!-- 头像 -->
            <div class="avatar_box">
                <img  src="../assets/pic/login/avatar.jpg" alt="头像">
            </div>

            <!-- 登录表单 -->
            <div class="loginform">
                <el-form :model="loginForm" 
                ref="loginFormRef"
                label-width="0px"
                :rules="rules">
                    <!-- 用户名 -->
                    <el-form-item prop="phone">
                        <el-input placeholder="请输入手机号"
                        prefix-icon="el-icon-zhanghao"
                        v-model="loginForm.phone"
                        clearable></el-input>
                    </el-form-item>

                    <!-- 密码 -->
                    <el-form-item prop="password">
                        <el-input placeholder="请输入密码"
                        prefix-icon="el-icon-mima"
                        v-model="loginForm.password" 
                        show-password
                        clearable></el-input>
                    </el-form-item>

                    <!-- 提交按钮 -->
                    <el-form-item class="btns">
                        <el-button type="primary" @click="onSubmit" class="btns2">马上开始</el-button>
                        <el-button type="info" @click="onSubmit2">新用户</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
//! mockURL
// var baseURL="https://www.fastmock.site/mock/b07d1d1630880597e9844bfed33c61fc/SEP";
export default {
    data() {
        return {
            loginForm: {
                // 登录表单数据绑定对象
                phone: '15901700373',
                password: 'test',
            },
            
            rules: {
                phone: [
                    { required: true, message: '请输入手机号', trigger: 'blur' },
                    { min: 11, max: 11, message: '输入11位手机号', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
                ],
            }
        }
    },
    mounted(){
        
    },
    methods: {
        
        onSubmit(){
            this.$refs.loginFormRef.validate((valid)=>{
            if(!valid) return;
            let that=this;
            const result = axios.post('/user/login',
                this.$qs.stringify({
                    phone:that.loginForm.phone,
                    userpassword:that.loginForm.password
                })).then(function(resp){
                    console.log(resp)
                    if(resp.data.userState) {
                //console.log(that.loginForm.username)
                    that.$message({
                    showClose: true,
                    message: '登录成功！',
                    center: true,
                    type: 'success'
                    });
                    // window.sessionStorage.setItem('token',"testtoken");
                    // window.localStorage.setItem('token',resp.data.token);
                    // window.localStorage.setItem('currentUser',resp.data.userId);
                    // that.$store.state.token=resp.data.token;
                    // that.$store.state.currentUser=resp.data.userId;
                    that.$store.commit("setToken",resp.data.token);
                    that.$store.commit("setuserInfo",resp.data.userId);
                    that.$router.push('/homepage')
                }
                else{
                    that.$message({
                    showClose: true,
                    message: '登录失败！密码错误或账号不存在',
                    center: true,
                    type: 'error'
                });
                }
                })
            .catch(function (error){
            console.log(error)
            })
            })

                // window.sessionStorage.setItem('token',"testtoken");
                // this.$router.push('/homepage')
           // });
        },

        onSubmit2(){
            this.$router.push('/register')
        }

    }
}
</script>

<style lang="less" scoped>
    .login_container {
        background-image: url("../assets/pic/login/background.jpg");
        background-repeat: no-repeat;
        background-position: center top;
        background-attachment: fixed;
        // background-size: 120%, 100%;
        background-size: cover;
        background-color: rgb(51, 51, 51);
        height: 100%;
        width: 100%;
    }
    .login_box {
        width: 450px;
        height: 400px;
        background-color: #fff;
        border-radius: 5%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        box-shadow: 30px 30px rgba(0, 0, 0, 0.1);
    }
    .avatar_box {
        height: 200px;
        width: 200px;
        border: 1px solid #333;
        border-radius: 100%;
        padding: 5px;
        box-shadow: 0 0 10px;
        img {
            width: 100%;
            height: 100%;
            border-radius: 100%;
            background-color: rgb(95, 95, 102);
        }
        position: absolute;
        top: 0%;
        left: 50%;
        transform: translate(-50%,-50%);
        // transform: translate(50%,50%);
        // margin-top: 55px;
        // margin-left: 25px;
        background-color: rgb(141, 140, 140);
        // float: left;
        // display: block;
    }
    .loginform {
        // margin-top: 82px;
        width: 300px;
        // margin-top: 100px;
        // margin-right: 50px;
        margin: 0 auto;
        padding-top: 150px;
        box-sizing: border-box;
        // float: right;
        // display: block;
    }
    .btns {
        // padding: 0;
        // margin-top: 10px;
        // margin: 0 auto;
        padding-top: 10px;
        display: flex;
        justify-content: flex-end
        // margin-right: 30px;
    }

    .btns2 {
        margin-right: 15px;
    }

    .el-carousel__item h3 {
        color: #475669;
        font-size: 14px;
        opacity: 0.75;
        line-height: 200px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }

    .avImg {
        width: 100%;
        height: 100%;
    }


</style>