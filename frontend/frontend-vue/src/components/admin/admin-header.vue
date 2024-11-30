<template>
  <header>
    <div class="interaction">
      <button>Добавить нового администратора</button>
      <button @click="logout">Выйти <img src="/src/assets/admin/exit-svg.svg"></button>
    </div>
  </header>
</template>

<script setup>
import axios from 'axios';
import { baseUrl } from '@/stores/store';
import {useRouter} from 'vue-router';
import Cookies from 'js-cookie';

const router = useRouter();

const logout = () =>{
  axios.get(`${baseUrl}/api/logout`,{
    withCredentials: true,
  })
  .then(response => {
    console.log(response.data.message);
    console.log(document.cookie);
    Cookies.remove('session');
    console.log(document.cookie);
    router.push('/admin');
  })
}
</script>

<style scoped>
header{
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.interaction{
  padding: 20px;
  display: flex;
  gap: 20px;
  max-height: max-content;
  max-width: max-content;
}

button {
  display: flex;
  align-items: center;
  font-size: 16px;
  gap: 10px;
  border: 0.50px solid #2b2a28;
  border-radius: 7px;
  background-color: #4597a3;
  padding: 10px 25px;
}

button:hover{
  background-color: #35818d;
}
</style>