<template>
    <div id="app" v-if="reset">
    <!-- 路由占位符 -->
    <div class="uploadavatar bordercut">
        <div class="ava">
        <div class="upic">
            <el-avatar shape="circle" :size="200" :fit="fit" :src="userInfo.imageUrl"></el-avatar>
        </div>
        <el-upload
        class="avatar-uploader"
        action=""
        :accept="'image/*'"
        :show-file-list="false"
        
        
        :limit="1"
        :auto-upload="false"
        :on-change="handleAvatarChangeIcon"
		ref="uploadicon"
        >
        <!-- :on-progress="handleProgress" -->
            <!-- <img v-if="userInfo.imageUrl" :src="userInfo.imageUrl" class="avatar"> -->
            <i  class="el-icon-paizhao avatar-uploader-icon"></i>
        </el-upload>
        </div>
        <div class="uploadbutton">
            <el-button plain @click="uploadavatar">更新照片<i class="el-icon-tupian el-icon--right"></i></el-button>
        </div>
    </div>

    <div class="changemsg bordercut">
        <div class="regForm">
            <el-form :model="userInfo" 
            ref="regFormRef"
            label-width="80px"
            :rules="rules">
                <!-- 用户名 -->
                <el-form-item label="姓名">
                    <!-- :disabled="true" -->
                    <el-input 
                    
                    prefix-icon="el-icon-zhanghao"
                    v-model="userInfo.username"
                    clearable></el-input>
                </el-form-item>


                <!-- 手机号 -->
                <el-form-item label="手机号">
                    <el-input 
                    prefix-icon="el-icon-yuyin"
                    v-model="userInfo.phone" 
                    clearable></el-input>
                </el-form-item>

                <!-- 擅长科目 -->
                <el-form-item label="擅长科目">
                    <el-checkbox-group v-model="userInfo.type">
                        <el-checkbox label="理科" name="type"></el-checkbox>
                        <el-checkbox label="工科" name="type"></el-checkbox>
                        <el-checkbox label="文科" name="type"></el-checkbox>
                        <!-- <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox> -->
                    </el-checkbox-group>
                </el-form-item>

                <el-tag
                    type="info"
                    effect="dark"
                    :key="tag"
                    v-for="tag in userInfo.dynamicTags"
                    closable
                    :disable-transitions="false"
                    @close="handleClose(tag)">
                        {{tag}}
                </el-tag>
                <el-input
                    class="input-new-tag"
                    v-if="inputVisible"
                    v-model="inputValue"
                    ref="saveTagInput"
                    size="small"
                    @keyup.enter.native="handleInputConfirm"
                    @blur="handleInputConfirm">
                </el-input>
                <el-button type="info" plain v-else class="button-new-tag" size="small" @click="showInput">增加新标签</el-button>


                    <!-- 提交按钮 -->
                <el-form-item class="uploadbutton">
                    <el-button plain @click="onSubmit" >保存信息<i class="el-icon-upload el-icon--right"></i></el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

    <div class="myrole bordercut">
        <span>我的身份：</span>
        <strong class="grey">{{userInfo.role}}</strong>
        <br>
        <el-button type="warning" icon="el-icon-biaoqian" @click="turnToInd">审核成为老师</el-button> 
    </div>

    </div>
</template>

<script>
import axios from'axios'
export default {
    data(){
        return{
            fit:'cover',
            fileraw:'',
            userInfo:{},
            inputVisible: false,
            inputValue: '',
            rules: {
                phone: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    { min: 11, max: 11, message: '长度为11位手机号', trigger: 'blur' }
                ]
            },
            reset:false
        }
    },
    methods:{
        handleAvatarChangeIcon(file,fileList){
            const isJPG = file.raw.type === 'image/jpeg'
            const isPNG = file.raw.type === 'image/png'
            const isLt2M = file.raw.size / 1024 / 1024 < 0.5
            this.hideUploadIcon = fileList.length >= 1;
            if (!isPNG && !isJPG) {
                this.$message.error('上传图片只能是 JPG/PNG 格式!')
                return false
            } else if (!isLt2M) {
                this.$message.error('上传图片大小不能超过 200kb!')
                return false
            } else if (isLt2M && (isPNG || isJPG)) {
                this.userInfo.imageUrl = URL.createObjectURL(file.raw);
                this.fileraw=file.raw//图片的url
            }
        },
        
        turnToInd() {
            const routeinfo = this.$router.resolve({
                    // name:"/info",
                    path:"/identity",
                    query: {
                        id:this.$store.state.userId
                    }
                });
                window.open(routeinfo.href, '_blank');
        },
        // TODO
        //handleProgress(event, file, fileList) {
        //    this.loading = true;  //  上传时执行loading事件
        //},

        uploadavatar(){
            if(!this.fileraw) {
                this.$message({
                            showClose: true,
                            message: '不能为空',
                            center: true,
                            type: 'error'
                        })
            }
            let formData = new FormData();

            // 把文件信息添加进如对象
            formData.append('url', this.fileraw)

            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'token':this.$store.state.token
                }
            }
            let that=this;
            // let postData = this.$qs.stringify({
            //     imageUrl:this.userInfo.imageUrl
            // });
            const result = axios.post('/user/updateAvatar',formData,config)
                .then(function (resp) {
                    // let { avatarUrl } = resp.data.imageUrl;
                    // console.log(resp.data.imageUrl);
                    // this.imageUrl= resp.data.imageUrl;
                    console.log(resp.data)
                    if (resp.data.success) {
                        that.$message({
                            showClose: true,
                            message: '上传成功',
                            center: true,
                            type: 'success'
            
                        })}
                    else{
                        that.$message({
                            showClose: true,
                            message: '上传失败',
                            center: true,
                            type: 'error'
                        })
                    }
                })
        },


        onSubmit() {
            console.log(this.dynamicTags);
            console.log(this.regForm.phone);
            console.log(this.regForm.type);
            this.$refs.regFormRef.validate((valid)=>{
            if(!valid) return;
        
            let that=this;
            let postData = this.$qs.stringify({
                username: that.userInfo.username,
                phone: that.userInfo.phone,
                type: that.userInfo.type,
                dynamicTags: that.userInfo.dynamicTags,
            });
            const result = axios({
                method: 'post',
                url: '/user/updateInfo',
                
                data:postData,
                headers: {
                    "token":this.$store.state.token
                },
            }).then(function (resp) {
                    console.log(resp.data)
                    if (resp.data.success) {
                        that.$message({
                            showClose: true,
                            message: '保存成功',
                            center: true,
                            type: 'success'
            
                        })}
                    else{
                        that.$message({
                            showClose: true,
                            message: '保存失败',
                            center: true,
                            type: 'error'
                        })
                    }
                })
        
            })
        },
        handleClose(tag) {
            this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
        },

        showInput() {
            this.inputVisible = true;
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },

        handleInputConfirm() {
            let inputValue = this.inputValue;
            if (inputValue) {
                this.dynamicTags.push(inputValue);
            }
            this.inputVisible = false;
            this.inputValue = '';
            console.log(this.dynamicTags);
        },


        userInfoAjax(){
            // this.teacherId=this.$route.params.teacherId
            // console.log(this.teacherId);
            console.log(this.$store.state.token);
            let that=this;
            const result = axios.get('/user/infoAjax',{
                
                params:{
                    userId:that.$store.state.userId
                },
                headers: {
                    token:that.$store.state.token
                },
                }).then((resp)=>{
                    if(resp.data.userState) {
                    that.userInfo=resp.data;
                    }
                    else {
                    this.$messagebox.confirm('可能您从未登录或登录状态失效', '您需要在登录状态才可获得联系方式', {
                        confirmButtonText: '前往重新登陆',
                        cancelButtonText: '放弃登录',
                        type: 'warning'
                    }).then(() => {
                        this.$router.push('/login')
                    }).catch(() => {
                        this.$message({
                            type: 'warning',
                            message: '已放弃登录！游客模式只能进行浏览哦'
                        });
                        this.$router.push('/homepage')
                    });
                    }
                    // console.log(resp.data);
                    // this.$set(this.$data,'tabledata',resp.data);
                }).catch((resp)=>{
                    console.log(resp.data.message);
                })
        },
        
    },

    beforeMount(){
        this.userInfoAjax();
    },
    mounted() {

    },
    watch: {
        userInfo: function(){
            this.$nextTick(function(){
                this.reset = true;
                console.log(this.reset);
            })
        }
    }


    
    
}
</script>

<style>
.bordercut {
    background-color: rgba(255, 255, 255, 0.856);
    border-bottom: 3px solid#e5e9ef;
    text-align: center;
}
.uploadavatar {
    width: 660px;
    height: 250px;
    padding: 20px;
    
    /* text-align: center; */
    
    /* margin: 0 10px; */
    /* padding-top: 10px; */
}
.ava {
    display: flex;
}
.upic {
    flex:1
}
.avatar-uploader {
    flex:1
}
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    /* width: 178px;
    height: 178px; */
    background-color: #fff;
    /* margin: 0 auto; */
    text-align: center;
    height: 178px;
    width: 178px;
}
.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}
.avatar-uploader-icon {
    font-size: 50px;
    color: #8c939d;
    margin-top: 55px;
    /* width: 178px; */
    /* height: 178px; */
    /* line-height: 178px; */
    /* text-align: center; */
}
.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
.uploadbutton {
    margin-top: 20px;
    /* margin-bottom: 10px; */
}
.changemsg {
    padding: 20px;
    padding-bottom: 0px;
    width: 660px;
    height: 350px;
}

.uploadbutton .el-form-item__content {
    margin-left: 0 !important
}
.uploadbutton .el-button {
    /* margin-left: 0; */
    padding: 10px 50px !important
}

.el-tag {
    /* margin-left: 5px; */
    margin-right: 10px;
}
.button-new-tag {
    /* margin-left: 5px; */
    margin-right: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
}
.input-new-tag {
    width: 90px;
    /* margin-left: 5px; */
    margin-right: 10px;
    vertical-align: bottom;
}
.myrole {
    width: 660px;
    padding: 20px;
    padding-bottom: 0px;
    height: 70px;
    text-align: left;
}
.myrole span {
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    font-size: 15px;

    /* color: pink; */
}
</style>