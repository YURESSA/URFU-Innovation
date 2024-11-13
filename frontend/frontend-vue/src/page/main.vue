<template>
  <header>
    <div class="header__wrapper">
      <h1>Тесты</h1>
      <div class="logo">
        <img src="../assets/main-page/элемент-линии.svg" class="line" alt=""/>
        <img src="../assets/main-page/логотип ИИ 1.svg" class="urfu" alt="инновационная инфраструктура УрФУ"/>
      </div>
    </div>
    <h2>предпринимательских компетенций</h2>
  </header>
  <main>
    <div v-for="(item, i) in tests" :key="i">
      <router-link :to="item.test_url">
        <test-priview :title="item.test_title"></test-priview>
      </router-link>
    </div>
    <student-form class="hidden"></student-form>
  </main>
</template>

<script setup>
import TestPriview from '@/components/test-priview.vue'
import {computed} from 'vue';
import {useDataStore} from '@/stores/store.js';
import StudentForm from '@/components/student-form.vue';

const store = useDataStore();
const tests = computed(() => store.getTests);
console.log(tests)
</script>

<style scoped>
header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
  margin-bottom: 35px;
}

.header__wrapper {
  display: flex;
  align-items: center;
  width: 679px;
}

.logo {
  position: relative;
  margin-left: 30px;
}

.line {
  position: absolute;
  top: -140px;
}

.urfu {
  position: absolute;
  right: -320px;
  top: -30px;
}

h2 {
  font-size: 82px;
  max-width: 679px;
}

main {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.hidden {
  display: none;
}

.modal-open {
  overflow: hidden;
}

</style>