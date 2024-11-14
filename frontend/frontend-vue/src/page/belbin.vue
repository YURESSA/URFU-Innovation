<template>
  <div class="page__wrapper" v-if="isLoading">
    <chapter-one-header></chapter-one-header>
    <charapter-one-main class="main" :test="test"></charapter-one-main>
  </div>
  <div v-else>
    Загрузка...
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import { computed, ref, onMounted } from 'vue';
import ChapterOneHeader from '@/components/belbin/chapter-one-header.vue';
import CharapterOneMain from '@/components/belbin/charapter-one-main.vue';

const store = useDataStore();
const isLoading = ref(false);

onMounted(async () => {
  await store.fetchBelbin();
  isLoading.value = true;
});
const test = computed(() => store.getBelbin);
</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100vw;
  background-color: #eee5e5;
}

.main{
  padding: 40px 0;
}
</style>