<template>
  <header>
    <div class="interaction">
      <button @click="exportAll">Выгрузить всех пользователей</button>
      <button @click="exportNew">Выгрузить новых пользователей</button>
      <button @click="emit('openForm')">Добавить нового администратора</button>
      <button @click="emit('openList')">Список администраторов</button>
      <button @click="logout" class="icon-btn"><img src="@public/assets/admin/exit-svg.svg">Выйти</button>
    </div>
  </header>
</template>

<script setup>
import { defineEmits } from 'vue';
import axios from 'axios';
import { baseUrl } from '@/stores/store';
import {useRouter} from 'vue-router';

const router = useRouter();

const emit = defineEmits(['openForm', 'openList'])

const logout = () =>{
  axios.get(`${baseUrl}/logout`, {
    withCredentials: true
  })
  .then(response => {
    router.push('/admin');
  })
}

const exportAll = () => {
  axios.get(`${baseUrl}/bitrix/users/export-all`, {
    responseType: 'blob',
    withCredentials: true
  })
  .then(response => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'all_users.xlsx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
  .catch(error => console.error('Ошибка экспорта всех пользователей:', error));
}

const exportNew = () => {
  axios.get(`${baseUrl}/bitrix/users/export-new`, {
    responseType: 'blob',
    withCredentials: true
  })
  .then(response => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'new_users.xlsx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
  .catch(error => console.error('Ошибка экспорта новых пользователей:', error));
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

</style>