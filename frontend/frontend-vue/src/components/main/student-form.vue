<template>
  <div class="form__wrapper" @click="emit('closeForm')">
    <div class="relative__wrapper" @click.stop>
      <button class="close-form" @click="emit('closeForm')"><img src="@public/assets/main-page/cross-circle-svgrepo-com.svg" alt=""></button>
      <div class="form">
        <h3>Заполните данные</h3>
        <form ref="studentForm" method="post" @submit="handleSubmit">
          <div class="input-wrapper">
            <label for="full_name">ФИО</label>
            <input type="text" name="full_name" autocomplete="off" placeholder="Иванов Иван Иванович" required>
          </div>
          <div class="input-wrapper">
            <label for="full_name">Номер телефона</label>
            <input
            type="tel"
            v-model="phoneNumber"
            name="phone_number"
            autocomplete="off"
            required
            @input="validatePhoneNumber">
          </div>
          <div class="input-wrapper">
            <label for="full_name">Способ связи. Телеграмм или номер телефона</label>
            <input
            type="text"
            class="contact-data"
            v-model="telegramId"
            name="telegram_id"
            autocomplete="off"
            placeholder="@UserName или @+79998881122"
            required
            @input="validateTelegramId">
          </div>
          <div class="approval">
            <input type="checkbox" class="checkbox" required ><p class="p__bold"> Нажимая кнопку "Перейти к тесту" вы даёте свое согласие на <a href="https://ozi.urfu.ru/fileadmin/user_upload/site_15891/ZI/UrFU_Polozhenie_o_personalnykh_dannykh.pdf" target="_blank">обработку введенной персональной информации</a></p>
          </div>
          <button ref="sumbitButton" type="submit" :disabled="!validNumber || !validTelegram" ><span>Перейти к тесту</span></button>
          <p v-if="!validNumber || !validTelegram" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router';
import { baseUrl } from '@/stores/store.js';

const router = useRouter();
const studentForm = ref(null);
const sumbitButton = ref(null);

const props = defineProps(['testUrl']);
const emit = defineEmits(['closeForm'])

const phoneNumber = ref('+7');
const telegramId = ref('');
const validNumber = ref(false);
const validTelegram = ref(false);
const errorMessage = ref('');

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
  validNumber.value = phoneNumber.value.length === 12;
  if(!validNumber.value){
    errorMessage.value = 'Некорректный номер телефона'
  } else {
    errorMessage.value = '';
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
  validTelegram.value = /^@[a-zA-Z0-9_+]{5,32}$/.test(input);

  if (!validTelegram.value) {
    errorMessage.value = 'Некорректный телеграмм';
  } else {
    errorMessage.value = '';
  }
};

function handleSubmit(event) {
  event.preventDefault();
  alert('араара')
  document.body.classList.remove('modal-open');
  const formData = new FormData(studentForm.value);
  sumbitButton.value.disabled = true;

  axios.post(`${baseUrl}/api/register-user`, formData, {
    withCredentials: true,
  })
      .then(response => {
        router.push(props.testUrl);
        alert(response)
      })
      .catch(error => {
        console.error('Произошла ошибка:', error);
        alert(error)
      })
      .finally(() => {
        sumbitButton.value.disabled = false;
      });
}
</script>

<style scoped>
.form__wrapper {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;

  left: 0;
  top: 0;
  right: 0;
  bottom: 0;

  background-color: rgba(0, 0, 0, 0.8);
}

.relative__wrapper{
  position: relative;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
  padding: 60px 60px;

  background-color: whitesmoke;
  border-radius: 14px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-wrapper{
  display: flex;
  flex-direction: column;
  width: 85%;
}

label{
  font-size: 20px;
  font-weight: 600;
  padding-left: 5px;
}

.contact-data::placeholder { 
  font-size: 16px;
}

input {
  border: 1px solid #2b2a28;
  border-radius: 7px;
  width: 100%;
  height: 55px;
  background-color: #c7c7c7;
  padding: 5px 10px;
  font-size: 24px;
  margin-bottom: 30px;
}

.approval{
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 450px;
  gap: 10px;
}

.checkbox{
  width: 15px;
  height: 20px;
  margin: 0;
}

button {
  border: 0.50px solid #2b2a28;
  border-radius: 7px;
  background-color: #57c0cf;
  padding: 10px 25px;
  margin-top: 30px;
}

button:hover {
  background-color: #2bd8f3;
}

button:disabled{
  background-color: #6a858a;
}

.error{
  font-size: 20px;
  font-weight: 600;
  color: brown;
  margin: 0;
  position: absolute;
  bottom: 115px;
}

.close-form{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0;
  background-color: whitesmoke;
  border: none;
}

.close-form:hover{
  background-color: rgba(192, 192, 192, 0.623);
}

.close-form:active{
  background-color: rgba(146, 146, 146, 0.623);
}

@media screen and (max-width: 980px) {
  .form{
    padding: 20px 40px;
    height: 580px;
    max-width: 300px;
    gap: 20px;
  }
  .error{
    bottom: 52px;
  }
  form{
    transform: translateY(10%);
  }
  input{
    font-size: 14px;
    height: 34px;
  }
  .contact-data::placeholder { 
  font-size: 11px;
  }
  h3{
    position: absolute;
    top: 60px;
    left: 50%;
    transform: translateX(-55%);
    width: max-content;
  }
}
</style>