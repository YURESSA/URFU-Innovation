<template>
  <div class="body">
    <admin-header @openForm="openForm" />
    <data-table :dataBase="dataBase" v-if="isLoading"/>
    <p v-if="!isLoading">Загрузка таблицы...</p>
    <template v-if="!open">
      <div class="modal__wrapper">
        <div class="form__wrapper">
          <div class="form">
            <h3>Добавление нового администратора</h3>
            <form ref="adminForm" method="post" @submit="creatAdmin">
              <input type="text" name="username" autocomplete="off" placeholder="Логин" required>
              <input type="password" v-model="password1" name="password1" autocomplete="off" placeholder="Пароль" @input="validPassword" required>
              <input type="password" v-model="password2" name="password2" autocomplete="off" placeholder="Повторите пароль" @input="validPassword" required>
              <span>{{ errorMessage }}</span>
              <button ref="sumbitButton" type="submit" :disabled="!valid">Добавить</button>
            </form>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useDataStore, baseUrl } from '@/stores/store.js';
import { useRouter } from 'vue-router';
import axios from 'axios';
import AdminHeader from '@/components/admin/admin-header.vue';
import DataTable from '@/components/admin/data-table.vue';

const store = useDataStore();
const isLoading = ref(false);
const router = useRouter();
const open = ref(true);
const sumbitButton = ref(null);
const adminForm = ref(null);
const password1 = ref('')
const password2 = ref('')
const valid = ref(false)
const errorMessage = ref('')

function openForm(){
  open.value = false;
  document.body.classList.add('modal-open')
}

const validPassword = () =>{
  valid.value = password1.value === password2.value
  if(!valid.value){
    errorMessage.value = 'Пароли не совпадают'
  } else {
    errorMessage.value = ''
  }
}

function creatAdmin(event){
  event.preventDefault();
  const formData = new FormData(adminForm.value);
  sumbitButton.value.disabled = true;
  axios.post(`${baseUrl}/api/register`, formData, {
    withCredentials: true,
  })
  .then(response => {
    open.value = true
    alert('Администратор успешно добавлен')
  })
  .catch(error =>{
    alert('Произошла ошибка при добавлении администратора')
    console.log(error)
    sumbitButton.value.disabled = false;
  })
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