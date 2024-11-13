<template>
  <chapter-one-header></chapter-one-header>
  <div v-for="(item, i) in questions" :key="i">
    <test-priview :title="item.test_title" @click="openForm(item.test_url)"></test-priview>
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import {computed} from 'vue';
import ChapterOneHeader from '@/components/belbin/chapter-one-header.vue';
import TestPriview from '@/components/main/test-priview.vue';

const store = useDataStore();

const questions = computed(() => store.getBelbin);
console.log(questions)
</script>

<style scoped>

</style>