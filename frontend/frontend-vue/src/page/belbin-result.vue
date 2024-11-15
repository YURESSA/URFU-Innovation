<template>
  <div class="page__wrapper" v-if="isLoading">
    <header-result></header-result>
    <!-- <diagram></diagram> -->
  </div>
  <div v-else>
    Загрузка...
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import { computed, ref, onMounted } from 'vue';
import HeaderResult from '@/components/belbin-result/header-result.vue';
// import Diagram from '@/components/belbin-result/diagram.vue';

const store = useDataStore();
const isLoading = ref(false);

onMounted(async () => {
  await store.fetchBelbinResult();
  isLoading.value = true;
});

const result = computed(() => store.getBelbinResult);
console.log(result.value[0])
</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100vw;
  background-color: #eee5e5;
  padding-bottom: 50px;
}
</style>