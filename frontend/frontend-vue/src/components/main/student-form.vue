<template>
  <div class="form__wrapper" @click="emit('closeForm')">
    <div class="relative__wrapper" @click.stop>
      <button class="close-form" @click="emit('closeForm')">
        <img src="@public/assets/main-page/cross-circle-svgrepo-com.svg" alt="">
      </button>
      
      <!-- Форма входа -->
      <div class="form" v-if="login">
        <h3>Войдите в профиль</h3>
        <form ref="loginForm" @submit.prevent="handleLoginSubmit">
          <div class="input-wrapper">
            <label for="telegram_id">Телеграм</label>
            <input
              type="text"
              v-model="loginData.telegram_id"
              name="telegram_id"
              autocomplete="off"
              placeholder="@UserName или @+79998881122"
              required
              @input="validateTelegramId('login')"
              :class="{ 'invalid': !validations.login.telegramValid && loginData.telegram_id }">
          </div>
          
          <div class="input-wrapper">
            <label for="password">Пароль</label>
            <input
              type="password"
              v-model="loginData.password"
              name="password"
              autocomplete="off"
              placeholder="Введите ваш пароль"
              required>
          </div>
          
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          
          <button 
            ref="loginButton" 
            class="submit" 
            type="submit" 
            :disabled="!validations.login.telegramValid || isLoading">
            <span>{{ isLoading ? 'Вход...' : 'Войти' }}</span>
          </button>
        </form>
        
        <p class="p__bold">
          Нет аккаунта? 
          <button class="switch-login" type="button" @click="switchToRegister">Зарегистрироваться</button>
        </p>
      </div>
      
      <!-- Форма регистрации -->
      <div class="form" v-if="!login">
        <h3>Регистрация</h3>
        <form ref="registerForm" @submit.prevent="handleRegisterSubmit">
          <div class="input-wrapper">
            <label for="full_name">ФИО</label>
            <input 
              type="text" 
              v-model="registerData.full_name"
              name="full_name" 
              autocomplete="off" 
              placeholder="Иванов Иван Иванович" 
              required>
          </div>
          
          <div class="input-wrapper">
            <label for="phone_number">Номер телефона</label>
            <input
              type="tel"
              v-model="registerData.phone_number"
              name="phone_number"
              autocomplete="off"
              placeholder="+7XXXXXXXXXX"
              required
              @input="validatePhoneNumber"
              :class="{ 'invalid': !validations.register.phoneValid && registerData.phone_number.length > 2 }">
          </div>
          
          <div class="input-wrapper">
            <label for="telegram_id">Телеграм</label>
            <input
              type="text"
              v-model="registerData.telegram_id"
              name="telegram_id"
              autocomplete="off"
              placeholder="@UserName или @+79998881122"
              required
              @input="validateTelegramId('register')"
              :class="{ 'invalid': !validations.register.telegramValid && registerData.telegram_id }">
          </div>
          
          <div class="input-wrapper">
            <label for="password">Пароль</label>
            <input
              type="password"
              v-model="registerData.password"
              name="password"
              autocomplete="off"
              placeholder="Введите ваш пароль"
              required
              minlength="6">
          </div>
          
          <div class="approval">
            <input type="checkbox" class="checkbox" v-model="agreed" required>
            <p class="p__bold">
              Нажимая кнопку "Зарегистрироваться" вы даёте свое согласие на 
              <a href="https://ozi.urfu.ru/fileadmin/user_upload/site_15891/ZI/UrFU_Polozhenie_o_personalnykh_dannykh.pdf" target="_blank">
                обработку введенной персональной информации
              </a>
            </p>
          </div>
          
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          
          <button 
            ref="registerButton" 
            class="submit" 
            type="submit" 
            :disabled="!validations.register.phoneValid || !validations.register.telegramValid || !agreed || isLoading">
            <span>{{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useDataStore } from '@/stores/store.js';

const router = useRouter();
const dataStore = useDataStore();
const props = defineProps(['testUrl']);
const emit = defineEmits(['closeForm']);

// Состояние формы
const login = ref(true);
const agreed = ref(false);
const isLoading = ref(false);

// Данные форм
const loginData = reactive({
  telegram_id: '',
  password: ''
});

const registerData = reactive({
  full_name: '',
  phone_number: '+7',
  telegram_id: '',
  password: ''
});

// Валидация
const validations = reactive({
  login: {
    telegramValid: false
  },
  register: {
    phoneValid: false,
    telegramValid: false
  }
});

// Ошибки из store
const errorMessage = computed(() => dataStore.authError);

// Ссылки на кнопки
const loginButton = ref(null);
const registerButton = ref(null);

// Ссылки на формы
const loginForm = ref(null);
const registerForm = ref(null);

// Методы валидации
const validatePhoneNumber = (event) => {
  let input = event.target.value;
  
  // Если поле пустое, начинаем с +7
  if (!input || input === '') {
    registerData.phone_number = '+7';
    validations.register.phoneValid = false;
    return;
  }
  
  // Убеждаемся что начинается с +7
  if (!input.startsWith('+7')) {
    input = '+7' + input.replace(/[^\d]/g, '');
  } else {
    input = '+7' + input.slice(2).replace(/[^\d]/g, '');
  }
  
  // Ограничиваем длину
  if (input.length > 12) {
    input = input.slice(0, 12);
  }
  
  registerData.phone_number = input;
  validations.register.phoneValid = registerData.phone_number.length === 12;
};

const validateTelegramId = (formType) => {
  let input = formType === 'login' ? loginData.telegram_id : registerData.telegram_id;
  
  // Обработка ссылок
  if (input.startsWith('https://t.me/')) {
    input = '@' + input.slice(13);
  }
  
  // Удаляем пробелы и спецсимволы кроме @, _, +
  input = input.replace(/[^a-zA-Z0-9_+@]/g, '');
  
  // Убеждаемся что начинается с @
  if (input && !input.startsWith('@')) {
    input = '@' + input;
  }
  
  // Ограничиваем длину
  if (input.length > 33) {
    input = input.slice(0, 33);
  }
  
  if (formType === 'login') {
    loginData.telegram_id = input;
    validations.login.telegramValid = /^@[a-zA-Z0-9_+]{5,32}$/.test(input);
  } else {
    registerData.telegram_id = input;
    validations.register.telegramValid = /^@[a-zA-Z0-9_+]{5,32}$/.test(input);
  }
};

// Переключение между формами
const switchToRegister = () => {
  login.value = false;
  dataStore.clearAuthError();
  
  // Очищаем данные
  loginData.telegram_id = '';
  loginData.password = '';
};

const switchToLogin = () => {
  login.value = true;
  dataStore.clearAuthError();
  
  // Очищаем данные
  registerData.full_name = '';
  registerData.phone_number = '+7';
  registerData.telegram_id = '';
  registerData.password = '';
  agreed.value = false;
  
  // Сбрасываем валидацию
  validations.register.phoneValid = false;
  validations.register.telegramValid = false;
};

// Обработчик входа
const handleLoginSubmit = async () => {
  if (!validations.login.telegramValid) {
    return;
  }
  
  isLoading.value = true;
  document.body.classList.remove('modal-open');
  
  const formData = new FormData();
  formData.append('telegram_id', loginData.telegram_id);
  formData.append('password', loginData.password);
  
  const result = await dataStore.loginUser(formData);
  
  if (result.success) {
    router.push(props.testUrl);
    emit('closeForm');
  }
  
  isLoading.value = false;
};

// Обработчик регистрации
const handleRegisterSubmit = async () => {
  if (!validations.register.phoneValid || !validations.register.telegramValid) {
    return;
  }
  
  if (!agreed.value) {
    return;
  }
  
  isLoading.value = true;
  document.body.classList.remove('modal-open');
  
  const formData = new FormData();
  formData.append('full_name', registerData.full_name);
  formData.append('phone_number', registerData.phone_number);
  formData.append('telegram_id', registerData.telegram_id);
  formData.append('password', registerData.password);
  
  const result = await dataStore.registerUser(formData);

  console.log(result)
  
  if (result.success) {
    alert('Регистрация успешна! Теперь вы можете войти.');
    switchToLogin();
  }
  
  isLoading.value = false;
};
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
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
}

.relative__wrapper {
  position: relative;
  width: 90%;
  max-width: 590px;
  margin: 0 auto;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 60px 40px;
  /* width: 100%;? */
  max-width: 470px;
  background-color: whitesmoke;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form > h3 {
  margin-bottom: 30px;
  font-size: 28px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 15px;
}

label {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
  padding-left: 5px;
  color: #444;
}

input {
  border: 2px solid #ddd;
  border-radius: 8px;
  height: 50px;
  background-color: white;
  padding: 5px 15px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #57c0cf;
  box-shadow: 0 0 0 3px rgba(87, 192, 207, 0.2);
}

input.invalid {
  border-color: #ff6b6b;
}

input.invalid:focus {
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
}

input::placeholder {
  color: #999;
  font-size: 14px;
}

.approval {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin: 20px 0 10px;
  text-align: left;
}

.approval > p {
  margin: 0;
}

.checkbox {
  width: 18px;
  height: 18px;
  min-width: 18px;
  margin-top: 2px;
  cursor: pointer;
}

.checkbox:checked {
  accent-color: #57c0cf;
}

.submit {
  border: none;
  border-radius: 8px;
  background-color: #57c0cf;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit:hover:not(:disabled) {
  background-color: #2bd8f3;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(43, 216, 243, 0.3);
}

.submit:active:not(:disabled) {
  transform: translateY(0);
}

.submit:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.submit {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
  font-size: 18px;
}

.switch-login {
  all: unset;
  color: #57c0cf;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  margin-left: 5px;
  transition: color 0.3s ease;
}

.switch-login:hover {
  color: #2bd8f3;
}

.p__bold {
  margin-top: 20px;
  font-size: 16px;
  color: #666;
}

.error {
  text-align: center;
  min-height: 20px;
  font-size: 16px;
  font-weight: 500;
  color: #ff6b6b;
  margin: 10px 0 5px;
}

.close-form {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 0;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.close-form:hover {
  background-color: #f0f0f0;
  transform: rotate(90deg);
  border-color: #57c0cf;
}

.close-form img {
  width: 20px;
  height: 20px;
}

/* Адаптивность */
@media screen and (max-width: 768px) {
  .form {
    padding: 40px 30px 30px;
    max-width: 400px;
  }
  
  .form > h3 {
    font-size: 24px;
  }
  
  input {
    height: 45px;
    font-size: 15px;
  }
  
  label {
    font-size: 16px;
  }
}

@media screen and (max-width: 480px) {
  .form {
    padding: 30px 20px 25px;
  }
  
  .form > h3 {
    font-size: 22px;
    margin-bottom: 20px;
  }
  
  .approval {
    gap: 8px;
  }
  
  .approval p {
    font-size: 14px;
  }
  
  .close-form {
    top: 10px;
    right: 10px;
  }
}

@media screen and (max-width: 360px) {
  .form {
    padding: 25px 15px 20px;
  }
  
  .form > h3 {
    font-size: 20px;
  }
  
  input {
    height: 40px;
    font-size: 14px;
  }
  
  .submit {
    font-size: 16px;
    padding: 10px 20px;
  }
}
</style>