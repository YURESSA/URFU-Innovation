<template>
  <div class="form__wrapper">
    <div class="form">
      <h3>Заполните данные</h3>
      <form ref="studentForm" method="post" @submit="handleSubmit">
        <input type="text" name="full_name" autocomplete="off" placeholder="ФИО" required>
        <input 
        type="tel" 
        v-model="phoneNumber"
        name="phone_number" 
        autocomplete="off" 
        required
        @input="validatePhoneNumber">
        <input 
        type="text" 
        v-model="telegramId"
        name="telegram_id" 
        autocomplete="off" 
        placeholder="Телеграмм: @userName" 
        required
        @input="validateTelegramId">
        <button ref="sumbitButton" type="submit" ><span>Перейти к тесту</span></button>
        <p v-if="!isValid" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router';
import {useDataStore} from '@/stores/store.js';
import { baseUrl } from '@/stores/store.js';

const store = useDataStore();
const router = useRouter();
const studentForm = ref(null);
const sumbitButton = ref(null);

const props = defineProps(['testUrl']);

const phoneNumber = ref('+7')
const telegramId = ref('')
const isValid = ref(true);
const errorMessage = ref('')

const validatePhoneNumber = (event) =>{
  let input = event.target.value;
  if (!input.startsWith('+7')) {
    input = '+7';
  }
  input = '+7' + input.slice(2).replace(/[^\d]/g, '');
  if (input.length > 12) {
    input = input.slice(0, 12);
  }
  phoneNumber.value = input;
  isValid.value = phoneNumber.value.length === 12;
  if(!isValid.value){
    errorMessage.value = 'Некорректный номер телефона'
  }
}

const validateTelegramId = (event) => {
  let input = event.target.value;
  if (input.startsWith('https://t.me/')) {
    input = '@' + input.slice(13);
  }
  if (input.length > 33) {
    input = input.slice(0, 33);
  }
  telegramId.value = input;
  isValid.value = /^@[a-zA-Z0-9_]{5,32}$/.test(input);

  if (!isValid.value) {
    errorMessage.value = 'Некорректный телеграмм';
  } else {
    errorMessage.value = '';
  }
};

function handleSubmit(event) {
  event.preventDefault();
  const formData = new FormData(studentForm.value);
  sumbitButton.value.disabled = true;

  axios.post(`${baseUrl}/api/register-user`, formData, {
    withCredentials: true,
  })
      .then(response => {
        console.log('Данные успешно отправлены!');
        router.push(props.testUrl);
      })
      .catch(error => {
        console.error('Произошла ошибка:', error);
      })
      .finally(() => {
        sumbitButton.value.disabled = false;
      });
}
</script>

<style scoped>
.form__wrapper {
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;

  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10;

  background-color: rgba(0, 0, 0, 0.8);
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 60px 60px;

  background-color: whitesmoke;
  border-radius: 14px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

input {
  border: 1px solid #2b2a28;
  border-radius: 7px;
  width: 347px;
  height: 55px;
  background-color: #c7c7c7;
  padding: 5px 10px;
  font-size: 24px;
}

button {
  border: 0.50px solid #2b2a28;
  border-radius: 7px;

  background-color: #57c0cf;

  padding: 10px 25px;
}

button:hover {
  background-color: #2bd8f3;
}
</style>