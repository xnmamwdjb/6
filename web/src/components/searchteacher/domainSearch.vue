<template>
    
    <el-select 
    @change="onDomainChange"
    v-model="domainValue" 
    clearable 
    placeholder="请选择领域">
        <el-option
        
        placeholder="请选择领域"
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
    name: "domainSearch",
    data() {
        return {
            options: [{
                value: '选修1',
                label: '数学学院'
            }, {
                value: '选项2',
                label: '英语学院'
            }, {
                value: '选项3',
                label: '信息学院'
            }, {
                value: '选项4',
                label: '社会学院'
            }, {
                value: '选项5',
                label: '艺术学院'
            }],
            domainValue: '' 
        }
    },
    methods: {
        onDomainChange() {
            let that = this;
            this.$emit('setDomain',that.domainValue)
        },
        
    }

}
</script>

<style lang="less" scoped>

</style>