<template>
    <div id="app">
    <!-- 路由占位符 -->
    <div class="uploadavatar bordercut">
        <el-upload
        class="avatar-uploader"
        action="https://www.mocky.io/v2/5185415ba171ea3a00704eed/posts/"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <div class="uploadbutton">
            <el-button plain @click="uploadavatar">上传头像<i class="el-icon-tupian el-icon--right"></i></el-button>
        </div>
    </div>

    <div class="changemsg bordercut">
        <div class="regForm">
            <el-form :model="regForm" 
            ref="regFormRef"
            label-width="80px"
            :rules="rules">
                <!-- 用户名 -->
                <el-form-item label="姓名">
                    <el-input :disabled="true"
                    prefix-icon="el-icon-zhanghao"
                    v-model="regForm.username"
                    clearable></el-input>
                </el-form-item>


                <!-- 手机号 -->
                <el-form-item label="手机号">
                    <el-input 
                    prefix-icon="el-icon-yuyin"
                    v-model="regForm.phone" 
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

                <el-tag
                    type="info"
                    effect="dark"
                    :key="tag"
                    v-for="tag in dynamicTags"
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
        <strong class="grey">{{role}}</strong>
        <br>
        <el-link 
        href="/identity"
        type="warning"
        icon="el-icon-biaoqian"
        :underline="false"
        >审核成为老师</el-link>
    </div>

    </div>
</template>

<script>
import axios from'axios'
export default {
    data(){
        return{
            role:'学生',
            imageUrl:'',
            regForm: {
                username: 'admin',
                phone: '12345678910',
                type: ['理科'],
            },
            dynamicTags: ['需要老师', '大三', '慢热'],
            inputVisible: false,
            inputValue: '',
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 2, max: 4, message: '长度在 2 到 4 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    { min: 11, max: 11, message: '长度为11位手机号', trigger: 'blur' }
                ]
            }
        }
    },
    methods:{
        handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
        console.log(this.imageUrl);
        //TODO 上传成功的钩子
        },
        beforeAvatarUpload(file) {
            const isJPG = file.type === 'image/jpeg';
            const isLt2M = file.size / 1024 / 1024 < 2;

            if (!isJPG) {
                this.$message.error('上传头像图片只能是 JPG 格式!');
            }
            if (!isLt2M) {
                this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            return isJPG && isLt2M;
        },

        uploadavatar(){
            console.log(this.imageUrl);
        },

        onSubmit() {
            console.log(this.dynamicTags);
            console.log(this.regForm.phone);
            console.log(this.regForm.type);
            this.$refs.regFormRef.validate((valid)=>{
            if(!valid) return;
        
            let that=this;
            const result = axios.post('http://localhost:8888/addUser',
                this.$qs.stringify({
                    username: that.regForm.username,
                    userpassword: that.regForm.password,
                    phone: that.regForm.phone,
                    type: that.regForm.type,
                    tag: that.dynamicTags,
                })).then(function (resp) {
                    console.log(resp.data)
                    if (resp.data) {
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