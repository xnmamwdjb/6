<template>
    
        <el-select
        @change="onInputChange"
        v-model="value"
        filterable
        remote
        reserve-keyword
        placeholder="请输入标签关键词"
        :remote-method="remoteMethod"
        :loading="loading">
                <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                </el-option>
        </el-select>
    
    
</template>

<script>
import axios from 'axios';
//! mockURL
// var baseURL="https://www.fastmock.site/mock/b07d1d1630880597e9844bfed33c61fc/SEP";

export default {
    name: "keySearch",
    data() {
        return {
            options: [],
            value: [],
            list: [],        
            loading: false,        
            states: [], 
        }
    },
    //改为select格式
    mounted() {
        this.list = this.states.map(item => {
            return {value: `value:${item}`,label: `label:${item}` }
        });
    },
    //? 解决监听问题
    computed: {
        listSet(){
            return this.states.map(item => {                
                return { value: `value:${item}`, label: `${item}` }; 
            }); 
        }
    },
    methods: {
        // 输入时调用
        remoteMethod(query) {
            console.log(query);
            let that = this;
            if(query !== '') {
                this.loading = true;
                let postData = this.$qs.stringify({                
                    tag:query                
                });            
                const result =axios({           
                    method: 'post',            
                    url:'/teacher/getKey',            
                    data:postData            
                }).then((res)=>{                
                if(res.data!='error')                    
                that.states=res.data                
	            // console.log(this.states);            
                });
                setTimeout(() => {
                    that.loading = false;
                    that.options = that.listSet.filter(item => {
                        return item.label.toLowerCase()
                        .indexOf(query.toLowerCase()) > -1;
                    });
                },2000);
            }
            else {
                that.options = [];
            }
        },
        onInputChange(val) {
            let str = val.split(":")
            this.$emit('setTag',str[1])
        },
        
    }

}
</script>

<style lang="less" scoped>

</style>