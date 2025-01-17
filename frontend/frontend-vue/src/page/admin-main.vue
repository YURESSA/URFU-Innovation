<template>
  <div class="body">
    <admin-header @openForm="openForm" @openList="openList"/>
    <data-table :dataBase="dataBase" v-if="isLoading"/>
    <p v-if="!isLoading">Загрузка таблицы...</p>
    <add-new-admin @closeForm="closeForm" v-if="isFormVisible"/>
    <admins-list @closeList="closeList" :admins="admins"  v-if="isListVisible"/>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useDataStore, baseUrl } from '@/stores/store.js';
import { useRouter } from 'vue-router';
import AdminHeader from '@/components/admin/admin-header.vue';
import DataTable from '@/components/admin/data-table.vue';
import AddNewAdmin from '@/components/admin/add-new-admin.vue';
import AdminsList from '@/components/admin/admins-list.vue';

const store = useDataStore();
const isLoading = ref(false);
const router = useRouter();
const isFormVisible = ref(false)
const isListVisible = ref(false)
const admins = computed(() => store.getAdmins);

function openForm(){
  isFormVisible.value = true
  document.body.classList.add('modal-open')
}

function closeForm(){
  isFormVisible.value = false
  document.body.classList.remove('modal-open')
}

async function fetchAdmins() {
    await store.fetchAdmins();
    isListVisible.value = true; 
  }

function openList(){
  fetchAdmins();
  document.body.classList.add('modal-open')
  console.log(admins.value)
}

function closeList(){
  isListVisible.value = false
  document.body.classList.remove('modal-open')
}


onMounted(async () => {
  try{
    await store.fetchDataBase();
    isLoading.value = true;
  } catch {
    router.push('/admin');
  }
});

const dataBase = computed(() => store.getDataBase.results);
</script>

<style scoped>

.body{
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  background-color: rgb(231, 231, 231);
}

.modal__wrapper{
  position: absolute;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(12, 11, 11, 0.842);
  width: 100%;
  height: 100%;
}

.form__wrapper{
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(38, 122, 122);
  height: 550px;
  width: 600px;
  border-radius: 15px;
}

.form{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

form{
  display: flex;
  flex-direction: column;
  gap: 30px;
}

input {
  border: 1px solid #2b2a28;
  border-radius: 7px;
  width: 347px;
  height: 30px;
  background-color: #c7c7c7;
  padding: 5px 10px;
  font-size: 20px;
}

button {
  border: 0.50px solid #2b2a28;
  border-radius: 7px;

  background-color: #35818d;
  margin-top: 35px;
  padding: 10px 25px;
}

button:hover {
  background-color: #4597a3;
}

button:disabled {
  background-color: #555858;
}

h3{
  text-align: center;
}

.modal-open{
  overflow: hidden;
}
</style>