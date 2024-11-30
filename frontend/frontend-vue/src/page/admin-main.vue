<template>
  <div class="body">
    <admin-header />
    <data-table :dataBase="dataBase" v-if="isLoading"/>
    <p v-if="!isLoading">Загрузка таблицы...</p>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useDataStore } from '@/stores/store.js';
import { useRouter } from 'vue-router';
import AdminHeader from '@/components/admin/admin-header.vue';
import DataTable from '@/components/admin/data-table.vue';

const store = useDataStore();
const isLoading = ref(false);
const router = useRouter();

onMounted(async () => {
  try{
    await store.fetchDataBase();
    isLoading.value = true;
  } catch {
    router.push('/admin');
  }
});

const dataBase = computed(() => store.getDataBase.results);
console.log(dataBase.value)
</script>

<style scoped>
.body{
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  background-color: rgb(0, 77, 77);
}
</style>