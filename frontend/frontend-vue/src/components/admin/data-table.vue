<template>
  <DataTable class="table" removableSort scrollable scrollHeight="750px" :value="dataBase" tableStyle="max-width: 60vw;">
    <button @click="exportExcel">Скачать Excel</button>
    <Column field="test_name" sortable  header="Тест"></Column>
    <Column field="full_name" sortable  header="ФИО"></Column>
    <Column field="sections" header="Результат">
      <template #body="dataBase">
        <div class="data-result">
          <span class="name" v-for="(value, key) in dataBase.data.sections" :key="key">
            {{ key }} <span class="result">{{ value }} </span>
          </span>
        </div>
      </template>
    </Column>
    <Column field="phone_number" header="Номер телефона"></Column>
    <Column field="telegram_id" header="Телеграмм" style="min-width: 150px">
      <template #body="dataBase">
        <a :href="`https://t.me/${dataBase.data.telegram_id.slice(1)}`">{{ dataBase.data.telegram_id }} </a>
      </template>
    </Column>
    <Column field="timestamp" sortable  header="Дата прохождения"></Column>
  </DataTable>
</template>

<script setup>
import { defineProps } from 'vue';
import { baseUrl } from '@/stores/store';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import axios from 'axios';

const props = defineProps({
  dataBase: Array,
})

function exportExcel() {
  axios.get(`${baseUrl}/api/save-test-results`, {
    responseType: 'blob',
    withCredentials: true
  })
  .then(response => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a'); 
    link.href = url;
    link.setAttribute('download', 'test_results.xlsx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
  .catch(error =>{
    console.error('Произошла ошибка', error)
  })
}
</script>

<style scoped>
.table{
  background-color: rgb(123, 221, 221);
  padding: 10px;
  border-radius: 10px;
}

.data-result{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.result{
  color: green;
}

.tg{
  min-width: 2000px;
}

thead > tr{
  background-color: rgb(123, 221, 221);
}

</style>