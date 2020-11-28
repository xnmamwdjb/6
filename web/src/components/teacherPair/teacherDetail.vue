<template>
    <div id="app" v-if="reset">
    
    <div class="tbanner">
        <!-- <el-page-header @back="goBack" content="详情页面"></el-page-header> -->
    </div>
    <div class="tmaincontainer">
        <div class="tpic">
            <el-avatar shape="circle" :size="400" :fit="fit" :src="teacherMsg.picURL"></el-avatar>
        </div>
        <div class="tmain">
            <span class="label">姓名：</span><span class="msg">{{teacherMsg.teacherName}}</span>
            <el-divider><i class="el-icon-arrow-up"></i></el-divider>
            <span class="label">擅长领域：</span><span class="msg">{{teacherMsg.teacherDomain}}</span>
            <el-divider><i class="el-icon-arrow-up"></i></el-divider>
            <span class="label">其他信息：</span><span class="msg">{{teacherMsg.teacherInfo}}</span>
            <el-divider><i class="el-icon-arrow-up"></i></el-divider>
            
            <div class="tbt">
                <span class="label">需要宇币：</span><span>{{teacherMsg.price}}枚</span>
                <el-divider><i class="el-icon-qianbao"></i></el-divider>
                <el-button type="primary" icon="el-icon-fenxiang" @click="onPay">获得联系方式</el-button>
            </div>
        </div>
    </div>
    <div class="footer"></div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name:"teacherDetail",
    data() {
        return {
            teacherId:'',
            fit: 'cover',
            reset: false,
            teacherMsg:{},
            //teacherMsg: {
            //    teacherName:"张小勤",
            //    teacherDomain:"信息学院",
            //    teacherInfo:"JAVA人",
            //    price: 16,
            //    picURL:"https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
            //}
        }//
    },
    methods: {
        
        onPay() {
            console.log(this.teacherId);
            console.log(this.$store.state.token);
            let user =  this.$qs.stringify({
                userId:this.$store.state.userId
            })

            let postData = this.$qs.stringify({
                teacherId:this.teacherId,
                userId:this.$store.state.userId
            });

            const result = axios({
                method: 'post',
                url: '/global/getUserState',
                data: user,
                headers: {
                    "token":this.$store.state.token
                },
            }).then((resp) => {
                if(resp.data.userState) {
                    this.$messagebox.confirm('即将扣除指定宇币！', '提示', {
                        confirmButtonText: '确定支付',
                        cancelButtonText: '取消支付',
                        type: 'warning'
                    }).then(() => {
                        //! 确定支付的回调函数
                        const result2 = axios({
                            method:'post',
                            url:'/teacher/getPhone',
                            data:postData,
                            headers: {
                                "token":this.$store.state.token
                            }
                        })
                        if(resp.data.payState) {
                            this.$message({
                                type: 'success',
                                message: '支付成功！情等待老师接受^^'
                            });
                        }
                        else {
                            this.$message({
                                type: 'error',
                                message: '支付失败！请检查您的余额QAQ'
                            });
                        }
                    }).catch(() => {
                        this.$message({
                            type: 'info',
                            message: '已取消支付'
                        });          
                    });
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
                    });
                }
            });
        },
        TeacherInfoAjax(){
            this.teacherId=this.$route.params.teacherId
            // console.log(this.teacherId);
            let that=this;
            const result = axios.get('/teacher/infoAjax',{
                params:{
                    teacherId:that.teacherId
                }
                }).then((resp)=>{
                    that.teacherMsg=resp.data;
                    // console.log(resp.data);
                    // this.$set(this.$data,'tabledata',resp.data);
                }).catch((resp)=>{
                    console.log(resp.message);
                })
        },
        
    },
    beforeMount(){
        this.TeacherInfoAjax();
    },
    mounted() {

    },
    watch: {
        teacherMsg: function(){
            this.$nextTick(function(){
                this.reset = true;
                console.log(this.reset);
            })
        }
    }
}
</script>

<style >
.tbanner {
    height: 160px;
    background-image: url("../../assets/pic/teacher/banner.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    margin-bottom: 10px;
}

.tmaincontainer {
    width: 900px;
    height: 500px;
    margin: 0 auto;
    border: 2px solid rgb(221, 221, 221);
    /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); */
    box-shadow: 20px 20px rgba(0, 0, 0, 0.1);
    /* border-radius: 50px; */
    display: flex;
}
.tpic {
    flex:1;
    padding-left: 10px;
    padding-top: 50px;
    /* padding-right: 10px; */
    background-color: #dacbc0;
    background-image: url("../../assets/pic/teacher/bg2.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    text-align: center;
    border-right: 1px dashed #dcdfe6;
}
.tmain {
    flex:1;
    /* background-color: rgb(255, 255, 255); */
    background-image: url("../../assets/pic/teacher/background.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    /* opacity: 70%; */
    padding-top: 20px;
    padding-left: 10px;
    padding-right: 10px;
}

.label {
    font-size: 22px;
    font-family: Microsoft YaHei;
}

.msg {
    font-size: 18px;
    font-family: Hiragino Sans GB;
}
.footer {
    width: 100%;
    height: 100px;
    background-color: #fff;
    margin-top: 20px;
}

.tbt {
    float: right;
}
</style>