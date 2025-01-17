<template>
  <div class="page__wrapper">
    <header-result></header-result>
    <diagram :result="diagresult"></diagram>
    <output-result :data="result"></output-result>
    <p class="p__bold">Личная консультация и ответы на вопросы по диагностике – Беспамятных Елена Владимировна, <a href="tel:+79022701569">+79022701569</a></p>
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

p{
  max-width: 600px;
  line-height: 140%;
  margin: 0 auto;
  margin-top: 20px;
}

a{
  color: #57C0CF;
}

@media screen and (max-width: 980px) {
  p{
    max-width: 260px;
  }
}

</style>