<template>
  <div class="page__wrapper">
    <chapter-one-header></chapter-one-header>
    <charapter-one-main class="main"></charapter-one-main>
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import { computed, ref, onMounted } from 'vue';
import ChapterOneHeader from '@/components/belbin/chapter-one-header.vue';
import CharapterOneMain from '@/components/belbin/charapter-one-main.vue';

const store = useDataStore();

const questions = computed(() => store.getBelbin);
console.log(questions.value.all_roles)
</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100vw;
  background-color: #eee5e5;
}

.main{
  margin-top: 40px;
}
</style>