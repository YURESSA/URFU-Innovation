<template>
  <div v-if="data"> <router-view /></div>
  <div v-else>Загрузка...</div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useDataStore } from '@/stores/store.js';

const store = useDataStore();

onMounted(() => {
  store.fetchTests();
});

const data = computed(() => store.getTests);
</script>

<style scoped>
</style>
