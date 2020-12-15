<template>
    <div id="app" v-if="reset">
    <el-backtop :bottom="100">
        <div
        style="{
            height: 100%;
            width: 100%;
            background-color: #f2f5f6;
            box-shadow: 0 0 6px rgba(0,0,0, .12);
            text-align: center;
            line-height: 40px;
            color: #1989fa;
        }"
        >
            UP
        </div>
    </el-backtop>
    
    <div class="search">
        <keySearch @setTag="setTag"></keySearch>
        <domainSearch @setDomain="setDomain"></domainSearch>
        <el-button type="warning" round @click="selectTeacher">查询老师</el-button> 
        
    </div>


    <div class="show">
        <el-row :gutter="32">
            <el-col :span="6" 
            v-for="(item) in tabledata" 
            :key="item.teacherId" 
            >
                <div class="cardcontainer">
                    <el-card :body-style="{ padding: '5px'}" shadow="hover">                    
                        <img src="../../assets/pic/teacher/womanTeacher2.jpg" class="image">                    
                        <div>                    
                            <span>{{item.userName}}</span><br>                    
                            <div class="bottom clearfix">                    
                                <span class="tag">
                                    <el-tag type="warning" v-for="(tag) in item.tags" :key="tag">
                                        {{tag}}
                                    </el-tag>
                                </span>                    
                                <el-button type="text" class="button" @click="add(item)">查看</el-button>                    
                            </div>                
                        </div>                
                    </el-card> 
                </div>
            </el-col>
        </el-row>
    </div>
    <div class="footer"></div>

    </div>
</template>

<script>
import axios from 'axios';
//! mockURL
// var baseURL="https://www.fastmock.site/mock/b07d1d1630880597e9844bfed33c61fc/SEP";

import domainSearch from '@/components/searchteacher/domainSearch'
import keySearch from '@/components/searchteacher/keySearch';
export default {
    name: "app",
    components:{
        keySearch,
        domainSearch,
    },
    data(){
        return {
            tabledata: [],
            current_page: 1,
            total: null,
            pagesize: 8,
            listdata: {},
            reset: false,
            keyTag: null,
            domain: null,
            classnum: null,
            
        }
    },
    methods: {
        refresh(){
            this.reload()
        },
        add(item) {
            console.log(item.teacherId);
            this.$router.push({  
            // path: 'yourPath',   
            name: 'teacherDetail',  
            params: {   
                teacherId:item.teacherId 
            }  
            /*query: {  
                key: 'key',   
                msgKey: this.msg  
            }*/  
        })  
        },
        allAjax(){
            let that = this;
            const result = axios.get('/teacher/selectAllTeacher',{
                //params:{
                //    userid:that.$store.state.userInfo
                //}
                }).then((resp)=>{
                    // that.listdata=resp.data.array;
                    // this.$set(this.$data,'tabledata',resp.data.array);
                    this.tabledata=resp.data.array
                    console.log(resp.data.array);
                }).catch((resp)=>{
                    console.log(resp);
                })

                
            
        },
        setTag(value) {
            this.keyTag = value;
            console.log(this.keyTag);
        },
        setDomain(value) {
            this.domain = value;
            console.log(this.domain);
        },

        //^只按tag关键字查询
        keyTagAjax(){
            let postData = this.$qs.stringify({
                tag:this.keyTag
            });
            const result = axios({
                method: 'post',
                url: '/teacher/selectByTag',
                data:postData
            }).then((resp) => {
                if(resp)
                this.tabledata = resp.data
            });
        },

        //^ 只按领域查询
        domainAjax(){
            let postData = this.$qs.stringify({
                domain:this.domain
            });
            const result = axios({
                method: 'post',
                url: '/teacher/selectByDomain',
                data:postData
            }).then((resp) => {
                if(resp)
                this.tabledata = resp.data
            });
        },


        //^ Tag和领域查询
        tagdomainAjax(){
            let postData = this.$qs.stringify({
                tag:this.tag,
                domain:this.domain
            });
            const result = axios({
                method: 'post',
                url: '/teacher/selectBytagdomain',
                data:postData
            }).then((resp) => {
                if(resp)
                this.tabledata = resp.data
            });
        },








        //^ 发送查询请求
        selectTeacher(){
            if(this.keyTag && this.domain){
                console.log("keyTag domain不为空");
                this.tagdomainAjax();
            }
            else if(this.domain){
                console.log("domain不为空");
                this.domainAjax();
            } 
            else if(this.keyTag){
                console.log("keyTag不为空");
                this.keyTagAjax();
            }
            else{
                this.$message({
                    showClose: true,
                    message:'查询条件不能为空！QAQ',
                    center: true,
                    type: 'error'
                })
                this.allAjax();
            }
        },


    },


    
    beforeMount(){
        this.allAjax();
    },
    mounted() {
        
    },
    
    watch: {
        tabledata: function(){
            this.$nextTick(function(){
                this.reset = true;
            })
        }
    }
}
</script>

<style >
.footer {
    width: 100%;
    height: 100px;
    background-color: #fff;
    margin-top: 20px;
}
.search {
    width: 100%;
    height: 50px;
    background-color: #333;
    text-align: center;
    padding: 10px;
}

.show {
    margin-left: 15%;
    margin-right: 15%;
    /* background-color: #333; */
}
.cardcontainer {
    margin-top: 15px;
}
.bottom {    
margin-top: 13px;    
line-height: 12px;  
margin-left: 10px;
margin-right: 10px;
margin-bottom: 10px;
}
.button {   
    padding: 0;    
    float: right;  
}
.clearfix:before,  
.clearfix:after {      
    display: table;     
    content: "";  
}    
.clearfix:after {      
    clear: both  
}
.image {
    width: 100%;
    height: 200px;
}
</style>