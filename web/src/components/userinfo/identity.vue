<template>
    <div id="app">
        <div class="container">

            <div class="banner">
                <!-- <el-page-header class="pageHeader" @back="goBack" content="注册页面"> -->
                <!-- </el-page-header> -->
                <el-link class="back" :underline="false" icon="el-icon-back" type="warning" @click="goBack">返回</el-link>
                <span class="cut">|</span>
                <span class="title1">审核页面</span>



            </div>

            <div class="regContainer">
                <!-- <div class="title"> -->
                        <!-- <div class="lt">用户名</div> -->
                        <!-- <div class="lt">密码</div> -->
                        <!-- <div class="lt">邮箱</div> -->
                <!-- </div> -->
                <div class="regForm">
                    <el-form :model="regForm" 
                    ref="regFormRef"
                    label-width="80px"
                    :rules="rules">
                    <!-- 用户名 -->
                    <el-form-item label="姓名" prop="username">
                        <el-input placeholder="请输入姓名"
                        prefix-icon="el-icon-user-solid"
                        v-model="regForm.username"
                        clearable></el-input>
                    </el-form-item>



                    <!-- 擅长科目 -->
                    <el-form-item label="擅长科目">
                      <el-checkbox-group v-model="regForm.type">
                        <el-checkbox label="理科" name="type"></el-checkbox>
                        <el-checkbox label="工科" name="type"></el-checkbox>
                        <el-checkbox label="文科" name="type"></el-checkbox>
                        <!-- <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox> -->
                      </el-checkbox-group>
                    </el-form-item>

                    <!-- 提交按钮 -->
                    <el-form-item class="btns">
                        <el-button  @click="onSubmit" >提交审核<i class="el-icon-upload el-icon--right"></i></el-button>
                    </el-form-item>
                  </el-form>
                </div>
            </div>

            <div class="footer"></div>
        </div>
    </div>
</template>

<script>
//! mockURL
// var baseURL=" https://www.fastmock.site/mock/b07d1d1630880597e9844bfed33c61fc/SEP";
import axios from 'axios';
export default {
  name: 'app',
  data() {
    return {
      regForm: {
        username: '',
        type: ["理科"],
      },
      rules: {
        username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 2, max: 4, message: '长度在 2 到 4 个字符', trigger: 'blur' }
        ],
        
      }
    }
  },
  methods: {

    goBack() {
        this.$router.push('/homepage')
    },
    onSubmit() {
        this.$refs.regFormRef.validate((valid)=>{
            if(!valid) return;
            let that=this;
            let postData=this.$qs.stringify({
                userId: this.$store.state.userInfo,
                userName: that.regForm.username,
                type: that.regForm.type
            })
            const result = axios({           
                method: 'post',            
                url:'/user/identity',            
                data:postData,
                headers: {
                    "token":this.$store.state.token
                },           
            }).then(function (resp) {
            console.log(resp.data);
        
            if (resp.data.success) {
                that.$message({
                showClose: true,
                message: '提交成功成功！请重新登录',
                center: true,
                type: 'success'
                })
                console.log(that.regForm.type);
                that.$router.push('/login')}
            else{
                that.$message({
                showClose: true,
                message: '提交失败',
                center: true,
                type: 'error'
                })
            }

            })
        })
    },


        // this.$message({
            // showClose: true,
            // message: '注册成功！登录以开始',
            // center: true,
            // type: 'success'
        // });
        // this.$router.push('/login')
        //?showClose: true,
        //?   message: '错了哦，这是一条错误消息',
        //?   type: 'error',
        //?   center: true,
    }



}
</script>

<style lang="less" scoped>
.container {
    background-color: rgb(214, 214, 214);
    height: 1000px;
    width: 100%;
    background-image: url("../../assets/pic/register/background.jpg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
}
.banner {
    height: 75px;
    width: 100%;
    background-color:rgba(212, 199, 183);
    box-shadow:  0 0 20px ;
    line-height: 75px;
    background-image: url("../../assets/pic/register/cut.png");
    // background-repeat: no-repeat;
    background-size: contain;
    background-position: 100px 30px;
}
.back {
    font-size: 25px;
    display: block;
    float: left;
    margin-left: 15px;
}
.cut {
    font-size: 30px;
    padding-left: 15px;
    padding-right: 15px;
    color: rgb(129, 129, 129);
    display: block;
    float: left;
}
.title1 {
    font-size: 30px;
    color: #333;
    display: block;
    float: left;
}

// .pageHeader {
    // padding: 25px;
// }

.regContainer {
    width: 700px;
    height: 700px;
    margin: auto;
    margin-top: 70px;
    // margin-bottom: 100px;
    background-color: #fff;
    box-shadow: 30px 30px rgba(0, 0, 0, 0.1);
    border-radius: 30px;
    border-top: 10px solid rgb(73, 73, 73);
    // border-bottom: 10px solid #333;
    background-color: rgba(255, 255, 255, 0.95);
    background-image: url("../../assets/pic/register/littleBanner.gif");
    background-repeat: no-repeat;
    background-position:30px 330px;
    // background-size: contain
}
.regForm {
    width: 400px;
    height: 200px;
    margin: auto;
    margin-top: 70px;
    // display: block;
    // float: left;
    // background-color: rgba(255, 255, 255, 0.6);
}
.btns {
    margin: auto;
    margin-top: 35px;
}
.el-button {
  margin-left: 0;
  padding: 10px 100px;
}
.el-button--default.is-disabled:hover{
  background-color: #4cc9f0;
  -webkit-box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
  -moz-box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
  box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
}



</style>