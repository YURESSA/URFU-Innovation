<template>
  <div class="page__wrapper">
    <header-result></header-result>
    <diagram :result="diagresult"></diagram>
    <output-result :data="result.prefer_roles"></output-result>
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import { computed } from 'vue';
import HeaderResult from '@/components/belbin-result/header-result.vue';
import Diagram from '@/components/belbin-result/diagram.vue';
import OutputResult from '@/components/belbin-result/output-result.vue';

const store = useDataStore();
const result = computed(() => store.getBelbinResult);
console.log(result.value)

const diagresult = Object.entries(result.value.all_roles).map(([key, value]) => ({
      name: key,
      pl: value
    }))
</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100vw;
  background-color: #FEFEFE;
  padding-bottom: 50px;
  display: flex;
  flex-direction: column;
}
</style>