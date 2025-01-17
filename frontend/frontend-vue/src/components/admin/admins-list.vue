<template>
  <div class="modal__wrapper" @click="emit('closeList')">
    <div class="form__wrapper" @click.stop>
      <h3>Список администраторов</h3>
        <div class="list">
          <div class="list-element" v-for="(item, i) in admins.admins" :key="i">
            <div class="info">
              <p>Роль: {{ item.role}}</p>
              <p>Имя пользователя: {{ item.username }}</p>
            </div>
            <div class="interact">
              <button @click="deletAdmin(item.username)">Удалить администратора</button>
              <button @click="transferSuperAdmin(item.username)">Передать супер админа</button>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, defineEmits, defineProps } from 'vue';
import { useDataStore, baseUrl } from '@/stores/store.js';
import { useRouter } from 'vue-router';

const store = useDataStore();
const isLoading = ref(false);
const router = useRouter();
const emit = defineEmits(['closeForm'])
const props = defineProps({
  admins: Object
})

function deletAdmin(username){
  store.fetchDeletAdmin(username)
  .then(() => {
    alert(`Администратор "${username}" успешно удалён!`);
  })
  .catch(error => {
      alert(`Ошибка при удалении администратора: ${error.message || 'Неизвестная ошибка'}`);
      if (error.response) {
        console.error('Ответ сервера с ошибкой:', error.response.data);
      } else {
        console.error('Ошибка без ответа сервера:', error);
      }
  });
}

function transferSuperAdmin(username){
  store.TransferSuperAdmin(username)
  .then(() => {
    alert(`Права переданы "${username}" успешно!`);
  })
  .catch(error => {
      alert(`Ошибка при передаче прав администратора: ${error.message || 'Неизвестная ошибка'}`);
      if (error.response) {
        console.error('Ответ сервера с ошибкой:', error.response.data);
      } else {
        console.error('Ошибка без ответа сервера:', error);
      }
  });
}

console.log(props.admins.admins)

onMounted(async () => {
  try{
    await store.fetchDataBase();
    isLoading.value = true;
  } catch {
    router.push('/admin');
  }
});

</script>

<style scoped>
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
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  background-color: rgb(38, 122, 122);
  height: 75%;
  width: 50%;
  border-radius: 15px;
}

.list{
  display: flex;
  flex-direction: column;
  width: 100%;
  padding : 25px 50px;
  gap: 5px;
}

.list-element{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 15px 5px;
  background-color: rgb(31, 158, 158);
  width: 100%;
  border-radius: 5px;
}

.info{
  display: flex;
}

.interact{
  display: flex;
}

button {
  border: 0.50px solid #2b2a28;
  border-radius: 7px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #35818d;
  padding: 10px 10px;
  font-size: 14px;
}

button:not(:first-of-type){
  margin-left: 15px;
}

button:hover {
  background-color: #4597a3;
}

button:disabled {
  background-color: #555858;
}

h3{
  text-align: center;
  margin-top: 40px;
}

p{
  margin: 0;
}

p:not(:first-of-type){
  margin-left: 20px;
}
</style>