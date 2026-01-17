<template>
  <div class="admin-table">
    <button @click="exportExcel">Скачать Excel</button>
    <DataTable class="table" removableSort scrollable scrollHeight="650px" :value="dataBase" tableStyle="max-width: 60vw;">
    
      <Column field="full_name" sortable>
        <template #header>
          <div class="title-header">
            ФИО
          </div>
        </template>
      </Column>
      <Column field="sections">
        <template #header>
          <span class="title-header">
            Результат
          </span>
        </template>
        <template #body="dataBase">
          <div class="data-result">
              <div class="data__result name" v-for="(value, key) in dataBase.data.sections" :key="key">
                <span>{{ key }}</span> <span class="result">{{ value }} </span>
              </div>
          </div>
        </template>
      </Column>
      <Column field="phone_number">
      <template #header>
          <span class="title-header">
            Номер&nbsp;телефона
          </span>
        </template>
      </Column>
      <Column field="telegram_id" style="min-width: 150px">
      <template #header>
          <span class="title-header">
            Телеграмм
          </span>
        </template>
        <template #body="dataBase">
          <a :href="`https://t.me/${dataBase.data.telegram_id.slice(1)}`">{{ dataBase.data.telegram_id }} </a>
        </template>
      </Column>
      <Column field="timestamp" sortable>
        <template #header>
          <span class="title-header">
            Дата&nbsp;прохождения
          </span>
        </template>
      </Column>
    </DataTable>
  </div>
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
  axios.get(`${baseUrl}/save-test-results`, {
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
  background-color: rgb(255, 255, 255);
  padding: 10px;
  border-radius: 10px;
}

.data-result{
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  gap: 10px;
}

.data__result{
  display: flex;
  justify-content: space-between;
  gap: 15px;
  width: 100%;

}

.result{
  color: #0a4e4e;
  font-weight: bold;
  margin-left: 4px;
}

.tg{
  min-width: 2000px;
}

th .title-header {
  font-weight: 700;
  margin-right: 4px;
  width: 140px;
  font-size: 16px;
}

button {
  margin-right: auto;

}

.admin-table {
  max-width: 1340px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

</style>