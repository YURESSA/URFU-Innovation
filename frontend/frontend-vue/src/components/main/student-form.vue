<template>
  <div class="form__wrapper">
    <div class="form">
      <h3>Заполните данные</h3>
      <form ref="studentForm" method="post" @submit="handleSubmit">
        <input type="text" name="full_name" placeholder="ФИО" required >
        <input type="tel" name="phone_number" placeholder="Номер телефона" required >
        <input type="text" name="telegram_id" placeholder="Телеграмм" required >
        <button ref="sumbitButton" type="submit"><span>Перейти к тесту</span></button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';
import { useDataStore } from '@/stores/store.js';

const store = useDataStore();
const router = useRouter();
const studentForm = ref(null);
const sumbitButton = ref(null);

const props = defineProps(['testUrl']);

function handleSubmit(event) {
  event.preventDefault();
  const formData = new FormData(studentForm.value);
  sumbitButton.value.disabled = true;
  
  axios.post('http://127.0.0.1:5000/api/register-user', formData)
    .then(response => {
      console.log('Данные успешно отправлены!');

      const sessionId = response.data.telegram_id;
      if (sessionId) {
        Cookies.set('session', sessionId, { expires: 7 }); // Сохраняем сессию на 7 дней
      }
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
.form__wrapper{
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

.form{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 60px 60px;

  background-color: whitesmoke;
  border-radius: 14px;
}

form{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

input{
  border: 1px solid #2b2a28;
  border-radius: 7px;
  width: 347px;
  height: 55px;
  background-color: #c7c7c7;
  padding: 5px 10px;
  font-size: 24px;
}

button{
  border: 0.50px solid #2b2a28;
  border-radius: 7px;

  background-color: #57c0cf;

  padding: 10px 25px;
}

button:hover{
  background-color: #2bd8f3;
}
</style>