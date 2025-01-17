<template>
  <header>
    <div class="interaction">
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
  axios.get(`${baseUrl}/api/logout`, {
    withCredentials: true
  })
  .then(response => {
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

</style>