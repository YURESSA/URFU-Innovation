<template>
  <div v-if="isReady">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useDataStore } from '@/stores/store.js';

const store = useDataStore();
const isReady = ref(false); // Новый флаг

onMounted(async () => {
  try {
    // Выполняем параллельно для скорости
    await Promise.all([
      store.fetchTests(),
      store.checkAuth()
    ]);
  } finally {
    isReady.value = true; // Теперь приложение готово
  }
});
</script>