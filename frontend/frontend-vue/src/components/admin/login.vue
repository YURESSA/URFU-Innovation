<template>
  <div class="form__wrapper">
    <div class="form">
      <h3>Вход</h3>
      <form ref="studentForm" method="post">
        <input type="text" name="username" autocomplete="off" placeholder="Логин" required>
        <input type="password" name="password" autocomplete="off" placeholder="Пароль" required>
        <button ref="sumbitButton" type="submit" @click="submitData">Войти</button>
        <p v-if="!isValid" class="error">Неверный логин или пароль</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { baseUrl } from '@/stores/store.js';
import {useRouter} from 'vue-router';

const isValid = ref(true);
const sumbitButton = ref(null);
const router = useRouter();
const studentForm = ref(null);

function submitData(event){
  event.preventDefault();
  const formData = new FormData(studentForm.value);
  sumbitButton.value.disabled = true;

  axios.post(`${baseUrl}/api/login`, formData, {
    withCredentials: true,
  })
  .then(response => {
    console.log('Вход выполнен');
    router.push('/admin/database');
  })
  .catch(error =>{
    router.push('/admin');
    console.error('Произошла ошибка', error)
    isValid.value = false
    sumbitButton.value.disabled = false;
  })
}
</script>

<style scoped>
.form__wrapper{
  display: flex;
  justify-content: center;
  align-items: flex-start;
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
  padding-top: 120px;
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
  margin-top: 60px;
  padding: 10px 25px;
}

button:hover {
  background-color: #4597a3;
}


.error{
  font-size: 20px;
  font-weight: 600;
  color: brown;
  margin: 0;
  text-align: center;
}
</style>